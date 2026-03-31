/**
 * POST /api/capstone/score-upload
 * Scores the capstone Task 4 open design submission using Gemini.
 * Accepts base64 image or plain text.
 * Returns { p5_score: 0|1|2, p6_score: 0|1|2 }
 */
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { getUser } from "@/lib/firestore/db";
import { loadCapstoneContent } from "@/lib/content/loadCapstone";

const GEMINI_MODEL = "gemini-2.0-flash";
const GEMINI_URL = (key: string) =>
  `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${key}`;

export async function POST(req: NextRequest) {
  let uid: string;
  try {
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return NextResponse.json({ error: "AI unavailable" }, { status: 503 });

  const {
    task4_text,
    task4_image_base64,
    task4_mime_type,
    declared_role,
    declared_industry,
  } = (await req.json()) as {
    task4_text: string;
    task4_image_base64?: string | null;
    task4_mime_type?: string | null;
    declared_role?: string;
    declared_industry?: string;
  };

  const userProfile = await getUser(uid);
  const capstone = loadCapstoneContent(userProfile?.lang ?? "en");
  const task4 = capstone.sections[3]!;
  const rubric = task4.coach_rubric ?? {};

  const rubricText = JSON.stringify(rubric, null, 2);
  const systemPrompt = `You are scoring a capstone submission for an AI skills program.
The learner is a ${declared_role ?? "professional"} in ${declared_industry ?? "their industry"}.

Score the following open design submission against this rubric:
${rubricText}

Return ONLY valid JSON in this exact format (no markdown, no explanation):
{"p5_score": <0|1|2>, "p6_score": <0|1|2>}

Where:
- p5_score: score for the Workflow design (0=no workflow, 1=partial, 2=complete CAST/pipeline with checkpoint)
- p6_score: score for the Agentic system design (0=single assistant, 1=2 agents partial, 2=complete CREW design)
If the learner only completed one option (A or B), score the other as 0.`;

  const parts: object[] = [
    { text: `Submission text:\n${task4_text || "(no text provided)"}` },
  ];

  if (task4_image_base64 && task4_mime_type) {
    parts.push({
      inline_data: { mime_type: task4_mime_type, data: task4_image_base64 },
    });
  }

  const body = {
    system_instruction: { parts: [{ text: systemPrompt }] },
    contents: [{ role: "user", parts }],
    generationConfig: { temperature: 0.1, maxOutputTokens: 256 },
  };

  const res = await fetch(GEMINI_URL(apiKey), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    return NextResponse.json({ p5_score: 0, p6_score: 0 });
  }

  const data = await res.json();
  const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text ?? "{}";

  try {
    const scores = JSON.parse(raw.trim()) as { p5_score: number; p6_score: number };
    return NextResponse.json({
      p5_score: Math.min(2, Math.max(0, Math.round(scores.p5_score ?? 0))),
      p6_score: Math.min(2, Math.max(0, Math.round(scores.p6_score ?? 0))),
    });
  } catch {
    return NextResponse.json({ p5_score: 1, p6_score: 1 }); // Graceful fallback
  }
}
