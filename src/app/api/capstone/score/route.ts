/**
 * POST /api/capstone/score
 * Aggregates all 4 task scores, writes progress to Firestore, triggers credential on pass.
 */
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { upsertTrainingProgress } from "@/lib/firestore/db";
import { loadCapstoneContent } from "@/lib/content/loadCapstone";

const GEMINI_MODEL = "gemini-2.0-flash";
const GEMINI_URL = (key: string) =>
  `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${key}`;

type CoachMessage = { role: string; content: string };
type PillarScores = { p1: number; p2: number; p3: number; p4: number; p5: number; p6: number };

/** Ask Gemini to score a conversation against a rubric. Returns scores 0-2 per pillar. */
async function scoreConversation(
  conversation: CoachMessage[],
  rubric: Record<string, Record<string, string>>,
  pillarsToScore: string[],
  role: string,
  industry: string,
  apiKey: string
): Promise<Record<string, number>> {
  const convoText = conversation
    .map((m) => `${m.role === "user" ? "Learner" : "Coach"}: ${m.content}`)
    .join("\n\n");

  const rubricText = JSON.stringify(rubric, null, 2);
  const keys = pillarsToScore.map((p) => `${p}_score`).join(", ");
  const prompt = `You are scoring an AI capstone assessment conversation.
Learner is a ${role} in ${industry}.

Rubric:
${rubricText}

Conversation:
${convoText}

Return ONLY valid JSON with keys ${keys}, each value 0, 1, or 2 based on the rubric. No markdown.`;

  const body = {
    contents: [{ role: "user", parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.1, maxOutputTokens: 256 },
  };

  const res = await fetch(GEMINI_URL(apiKey), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    // Fallback: partial credit
    return Object.fromEntries(pillarsToScore.map((p) => [`${p}_score`, 1]));
  }

  const data = await res.json();
  const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text ?? "{}";
  try {
    const scores = JSON.parse(raw.trim()) as Record<string, number>;
    return Object.fromEntries(
      pillarsToScore.map((p) => [
        `${p}_score`,
        Math.min(2, Math.max(0, Math.round(scores[`${p}_score`] ?? 1))),
      ])
    );
  } catch {
    return Object.fromEntries(pillarsToScore.map((p) => [`${p}_score`, 1]));
  }
}

/** Build coaching feedback for a failed attempt using Gemini. */
async function buildFailFeedback(
  pillarScores: PillarScores,
  apiKey: string
): Promise<string> {
  const failedPillars = (Object.entries(pillarScores) as [string, number][])
    .filter(([, v]) => v < 1)
    .map(([k]) => k.toUpperCase());

  if (failedPillars.length === 0) return "You were very close! Review the sections above and try again.";

  const prompt = `A learner failed the AI Hero Academy capstone. The pillars below scored 0/2:
${failedPillars.join(", ")}

Write 3-4 sentences of warm, specific coaching feedback explaining:
1. Which specific section(s) they should improve
2. What a stronger response looks like (concrete)
3. An encouraging close

Keep it under 120 words. No bullet points.`;

  const body = {
    contents: [{ role: "user", parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.5, maxOutputTokens: 200 },
  };

  const res = await fetch(GEMINI_URL(apiKey), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) return "Review the sections where you scored below passing and try again. You're close!";
  const data = await res.json();
  return data?.candidates?.[0]?.content?.parts?.[0]?.text ?? "Review and retake — you're close!";
}

export async function POST(req: NextRequest) {
  let uid: string;
  let userEmail: string;
  try {
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
    userEmail = auth.email;
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return NextResponse.json({ error: "AI unavailable" }, { status: 503 });

  const {
    task1_conversation,
    task2_conversation,
    task3_score,      // pre-computed client-side MCQ aggregate (0-2)
    task4_image_base64,
    task4_mime_type,
    task4_text,
    declared_role = "professional",
    declared_industry = "their industry",
  } = (await req.json()) as {
    task1_conversation: CoachMessage[];
    task2_conversation: CoachMessage[];
    task3_score: number;
    task4_image_base64?: string | null;
    task4_mime_type?: string | null;
    task4_text: string;
    declared_role?: string;
    declared_industry?: string;
  };

  const capstone = loadCapstoneContent();
  const rubric1 = capstone.sections[0]?.coach_rubric ?? {};
  const rubric2 = capstone.sections[1]?.coach_rubric ?? {};

  // Score all tasks in parallel
  const [task1Scores, task2Scores, task4ScoresRes] = await Promise.all([
    scoreConversation(task1_conversation, rubric1, ["p1", "p2"], declared_role, declared_industry, apiKey),
    scoreConversation(task2_conversation, rubric2, ["p3", "p4"], declared_role, declared_industry, apiKey),
    // Score task 4 via Gemini (same logic as score-upload but inline)
    (async () => {
      const task4Section = capstone.sections[3]!;
      const r = task4Section.coach_rubric ?? {};
      const parts: object[] = [
        { text: `Design submission:\n${task4_text || "(none)"}` },
      ];
      if (task4_image_base64 && task4_mime_type) {
        parts.push({ inline_data: { mime_type: task4_mime_type, data: task4_image_base64 } });
      }
      const sysPrompt = `Score this AI capstone design submission. Return JSON: {"p5_score":<0|1|2>,"p6_score":<0|1|2>}. Rubric: ${JSON.stringify(r)}`;
      const res = await fetch(GEMINI_URL(apiKey), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          system_instruction: { parts: [{ text: sysPrompt }] },
          contents: [{ role: "user", parts }],
          generationConfig: { temperature: 0.1, maxOutputTokens: 128 },
        }),
      });
      if (!res.ok) return { p5_score: 1, p6_score: 1 };
      const d = await res.json();
      const raw = d?.candidates?.[0]?.content?.parts?.[0]?.text ?? "{}";
      try {
        const s = JSON.parse(raw.trim()) as { p5_score: number; p6_score: number };
        return {
          p5_score: Math.min(2, Math.max(0, Math.round(s.p5_score ?? 1))),
          p6_score: Math.min(2, Math.max(0, Math.round(s.p6_score ?? 1))),
        };
      } catch { return { p5_score: 1, p6_score: 1 }; }
    })(),
  ]);

  // Merge MCQ signal: task3_score (0-2) partially informs p1,p2 (min boost of 0.5 each, capped at 2)
  const mcqBoost = task3_score >= 1.5 ? 0.5 : 0;
  const pillarScores: PillarScores = {
    p1: Math.min(2, (task1Scores["p1_score"] ?? 1) + (task3_score >= 1 ? mcqBoost : 0)),
    p2: Math.min(2, (task1Scores["p2_score"] ?? 1) + (task3_score >= 1.5 ? mcqBoost : 0)),
    p3: Math.min(2, (task2Scores["p3_score"] ?? 1)),
    p4: Math.min(2, (task2Scores["p4_score"] ?? 1)),
    p5: Math.min(2, (task4ScoresRes.p5_score ?? 1)),
    p6: Math.min(2, (task4ScoresRes.p6_score ?? 1)),
  };

  // overall_score on 4.0 scale: sum(pillars) / 12 * 4
  const sum = Object.values(pillarScores).reduce((a, b) => a + b, 0);
  const overallScore = Math.round((sum / 12) * 4 * 10) / 10;
  const passed = overallScore >= 2.5;

  // Write to Firestore
  await upsertTrainingProgress(uid, "capstone" as import("@/lib/firestore/types").PillarId, {
    quiz_passed: passed,
    quiz_score: overallScore,
    quiz_completed_at: Timestamp.now(),
    user_email: userEmail,
  });

  let feedback: string | null = null;
  if (!passed) {
    feedback = await buildFailFeedback(pillarScores, apiKey);
  }

  return NextResponse.json({ passed, overall_score: overallScore, pillar_scores: pillarScores, feedback });
}
