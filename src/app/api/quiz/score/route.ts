import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAdminAuth } from "@/lib/firebase/admin";
import { upsertTrainingProgress, logAiCall } from "@/lib/firestore/db";
import { loadPillarContent } from "@/lib/content/loadPillar";
import type { PillarId } from "@/lib/firestore/types";

const GEMINI_MODEL = "gemini-2.0-flash";
const PILLAR_ORDER: PillarId[] = ["p1", "p2", "p3", "p4", "p5", "p6"];

async function scoreOpenAnswer(
  question: string,
  rubric: Record<string, string>,
  answer: string,
  maxScore: number,
  apiKey: string
): Promise<number> {
  const rubricText = Object.entries(rubric)
    .map(([score, desc]) => `Score ${score}: ${desc}`)
    .join("\n");

  const prompt = `You are scoring a quiz response. Score only based on the rubric provided.

Question: ${question}

Rubric:
${rubricText}

Learner's answer: ${answer}

Return ONLY valid JSON with this exact shape: {"score": <number>, "reasoning": "<one sentence>"}
The score must be one of the values from the rubric (e.g. 0, 0.5, 1). No other text.`;

  const start = Date.now();
  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${apiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { maxOutputTokens: 100, temperature: 0.1 },
        }),
        signal: AbortSignal.timeout(8000),
      }
    );

    if (!res.ok) return 0;

    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text?.trim() ?? "";

    // Parse JSON from the response
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) return 0;
    const parsed = JSON.parse(jsonMatch[0]);
    const score = Number(parsed.score);

    // Clamp to valid range
    return Math.min(Math.max(score, 0), maxScore);
  } catch {
    return 0;
  }
}

export async function POST(req: NextRequest) {
  const sessionCookie = (await cookies()).get("__session")?.value;
  if (!sessionCookie) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  let uid: string;
  let userEmail: string;
  try {
    const decoded = await getAdminAuth().verifySessionCookie(sessionCookie, true);
    uid = decoded.uid;
    userEmail = decoded.email ?? "";
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return NextResponse.json({ error: "AI service unavailable" }, { status: 503 });
  }

  const {
    pillar_id,
    mcq_answers,
    open_answer,
    session_id,
  }: {
    pillar_id: PillarId;
    mcq_answers: Record<string, string>;
    open_answer: string;
    session_id?: string;
  } = await req.json();

  if (!pillar_id || !mcq_answers) {
    return NextResponse.json({ error: "pillar_id and mcq_answers required" }, { status: 400 });
  }

  const pillarContent = loadPillarContent(pillar_id);
  const { items, pass_threshold, max_score, fail_guidance } = pillarContent.quiz;

  let totalScore = 0;
  const itemResults: Array<{
    item_id: string;
    score: number;
    correct?: boolean;
    explanation?: string;
  }> = [];

  for (const item of items) {
    if (item.type === "mcq") {
      const selected = mcq_answers[item.item_id];
      const correct = selected === item.correct_answer;
      const score = correct ? item.score_weight : 0;
      totalScore += score;
      itemResults.push({
        item_id: item.item_id,
        score,
        correct,
        explanation: !correct ? item.explanation : undefined,
      });
    } else if (item.type === "open_rubric") {
      const answer = open_answer ?? "";
      const score = await scoreOpenAnswer(
        item.question,
        item.rubric ?? {},
        answer,
        item.max_score ?? item.score_weight,
        apiKey
      );
      totalScore += score;
      itemResults.push({ item_id: item.item_id, score });

      // Log the AI scoring call
      logAiCall({
        uid,
        user_email: userEmail,
        model: GEMINI_MODEL,
        prompt_tokens: 0,
        completion_tokens: 0,
        latency_ms: 0,
        route: "/api/quiz/score",
      }).catch(() => {});
    }
  }

  const roundedScore = Math.round(totalScore * 10) / 10;
  const passed = roundedScore >= pass_threshold;
  const now = Timestamp.now();

  if (passed) {
    // Determine next pillar
    const currentIdx = PILLAR_ORDER.indexOf(pillar_id);
    const nextPillarId = currentIdx >= 0 && currentIdx < PILLAR_ORDER.length - 1
      ? PILLAR_ORDER[currentIdx + 1]
      : null;

    await Promise.all([
      upsertTrainingProgress(uid, pillar_id, {
        quiz_passed: true,
        quiz_score: roundedScore,
        quiz_completed_at: now,
      }),
      ...(nextPillarId
        ? [upsertTrainingProgress(uid, nextPillarId, { is_locked: false })]
        : []),
    ]);

    // Fire synthesis — non-blocking fire-and-forget
    if (session_id) {
      fetch(`${req.nextUrl.origin}/api/synthesis/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Cookie: req.headers.get("cookie") ?? "",
        },
        body: JSON.stringify({ session_id, pillar_id }),
      }).catch(() => {});
    }

    return NextResponse.json({
      pass: true,
      score: roundedScore,
      max_score,
      next_pillar_id: nextPillarId,
      item_results: itemResults,
    });
  }

  // Failed — return hints
  const hints = itemResults
    .filter((r) => r.score === 0 && r.explanation)
    .map((r) => ({ item_id: r.item_id, hint: r.explanation! }));

  return NextResponse.json({
    pass: false,
    score: roundedScore,
    max_score,
    fail_guidance,
    hints,
    item_results: itemResults,
  });
}
