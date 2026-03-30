import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { logAiCall } from "@/lib/firestore/db";

const FALLBACK_QUESTION =
  "Describe a recent work task where you think AI could have helped you. What stopped you from using it?";

const GEMINI_MODEL = "gemini-2.0-flash";

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

  const { declared_role, declared_industry, daily_work_desc } = await req.json();

  if (!declared_role || !daily_work_desc) {
    return NextResponse.json({ question: FALLBACK_QUESTION, source: "fallback" });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return NextResponse.json({ question: FALLBACK_QUESTION, source: "fallback" });
  }

  const prompt = `Generate one scenario-based diagnostic question for a ${declared_role}${declared_industry ? ` in ${declared_industry}` : ""}. The scenario should involve a realistic task from their daily work: ${daily_work_desc}. The question should reveal how the learner currently uses AI tools — without using jargon or signalling what the 'correct' answer is. Under 50 words. Return only the question text, no preamble.`;

  const start = Date.now();
  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${apiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { maxOutputTokens: 100, temperature: 0.7 },
        }),
        signal: AbortSignal.timeout(5000), // 5s timeout → fallback
      }
    );

    if (!res.ok) throw new Error(`Gemini ${res.status}`);

    const data = await res.json();
    const question =
      data?.candidates?.[0]?.content?.parts?.[0]?.text?.trim() ?? FALLBACK_QUESTION;

    const latency = Date.now() - start;
    await logAiCall({
      uid,
      user_email: userEmail,
      model: GEMINI_MODEL,
      prompt_tokens: data?.usageMetadata?.promptTokenCount ?? 0,
      completion_tokens: data?.usageMetadata?.candidatesTokenCount ?? 0,
      latency_ms: latency,
      route: "/api/diagnostic/generate-question",
    }).catch(() => {}); // non-blocking

    return NextResponse.json({ question, source: "gemini" });
  } catch {
    return NextResponse.json({ question: FALLBACK_QUESTION, source: "fallback" });
  }
}
