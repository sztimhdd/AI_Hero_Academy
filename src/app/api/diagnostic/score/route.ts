import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAuthFromCookies } from "@/lib/auth/verify";
import {
  upsertUser,
  createDiagnosticSession,
  initTrainingProgress,
} from "@/lib/firestore/db";
import { PillarScores } from "@/lib/firestore/types";
import diagnosticQuestions from "../../../../../content/diagnostic_pillar.json";

interface ScorePayload {
  // Onboarding profile fields
  declared_role: string;
  declared_industry: string;
  daily_work_desc: string;
  current_ai_usage: string;
  primary_motivation: "save_time" | "quality" | "career" | "explore";
  // MCQ answers: { q_p1: "b", q_p2: "a", ... }
  mcq_answers: Record<string, string>;
  // Open question
  ai_question_text: string;
  ai_question_answer: string;
}

export async function POST(req: NextRequest) {
  let uid: string;
  let userEmail: string;
  let displayName: string;
  const photoURL = "";

  try {
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
    userEmail = auth.email;
    displayName = auth.displayName;
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body: ScorePayload = await req.json();

  // ── Score MCQs ─────────────────────────────────────────────────────────────
  // Each correct MCQ answer = 100 points for that pillar; wrong = 20 (baseline credit)
  const pillarScores: PillarScores = { p1: 20, p2: 20, p3: 20, p4: 20, p5: 20, p6: 20 };
  const itemScores: Record<string, number> = {};

  for (const q of diagnosticQuestions.questions) {
    const answer = body.mcq_answers[q.id];
    const score = answer === q.correct ? 100 : 20;
    pillarScores[q.pillar as keyof PillarScores] = score;
    itemScores[q.id] = score;
  }

  // p6 has no MCQ — default to 50 (neutral baseline)
  pillarScores.p6 = 50;

  const overallScore = Math.round(
    Object.values(pillarScores).reduce((a, b) => a + b, 0) / 6
  );

  const now = Timestamp.now();

  // ── Write UserProfile ──────────────────────────────────────────────────────
  await upsertUser(uid, {
    uid,
    user_email: userEmail,
    display_name: displayName,
    profile_photo_url: photoURL,
    declared_role: body.declared_role,
    declared_industry: body.declared_industry,
    daily_work_desc: body.daily_work_desc,
    current_ai_usage: body.current_ai_usage,
    primary_motivation: body.primary_motivation,
    program_started_at: now,
    streak_days: 1,
    last_active_date: new Date().toISOString().slice(0, 10),
  });

  // ── Write DiagnosticSession ────────────────────────────────────────────────
  const sessionId = await createDiagnosticSession({
    uid,
    user_email: userEmail,
    completed_at: now,
    pillar_scores: pillarScores,
    overall_score: overallScore,
    item_scores: itemScores,
    session_number: 1,
    ai_question_used: body.ai_question_text,
    ai_question_answer: body.ai_question_answer,
  });

  // ── Write TrainingProgress (p1 unlocked, rest locked) ─────────────────────
  await initTrainingProgress(uid, userEmail);

  return NextResponse.json({
    status: "ok",
    session_id: sessionId,
    pillar_scores: pillarScores,
    overall_score: overallScore,
  });
}
