/**
 * POST /api/synthesis/run
 *
 * Runs after each day's quiz pass. Fire-and-forget from /api/quiz/score.
 * Reads the coach session transcript, extracts learning signals via Gemini,
 * and appends them to the learner model in Firestore.
 *
 * Never blocks the learner — failures are logged only.
 */
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { FieldValue } from "firebase-admin/firestore";
import { getFirestore } from "firebase-admin/firestore";
import { getAdminAuth } from "@/lib/firebase/admin";
import { getCoachSession, upsertLearnerModel, logAiCall, getLearnerModel } from "@/lib/firestore/db";
import { COLLECTIONS } from "@/lib/firestore/types";
import type { PillarId } from "@/lib/firestore/types";

const GEMINI_MODEL = "gemini-2.0-flash";

interface SynthesisOutput {
  daily_summary: string;
  natural_strengths: string[];
  recurring_gaps: string[];
  preferred_framing?: "examples" | "challenge" | "abstract" | "concrete";
  memorable_quote?: string;
}

async function runSynthesis(
  transcript: Array<{ role: string; content: string }>,
  pillarId: PillarId,
  apiKey: string
): Promise<SynthesisOutput | null> {
  const transcriptText = transcript
    .map((t) => `${t.role === "user" ? "Learner" : "Coach"}: ${t.content}`)
    .join("\n\n");

  if (!transcriptText.trim()) return null;

  const prompt = `Analyze this AI coaching session transcript and extract learning signals.

TRANSCRIPT:
${transcriptText}

Extract and return ONLY valid JSON with this exact shape:
{
  "daily_summary": "<one concise sentence capturing the key insight demonstrated today>",
  "natural_strengths": ["<strength 1>", "<strength 2 if observed>"],
  "recurring_gaps": ["<gap 1>", "<gap 2 if observed>"],
  "preferred_framing": "<one of: examples | challenge | abstract | concrete — or omit if unclear>",
  "memorable_quote": "<a verbatim phrase from the learner that captures their learning voice, or omit if none stands out>"
}

Rules:
- natural_strengths: at most 2 items, only genuine strengths demonstrated in practice
- recurring_gaps: at most 2 items, only if the learner struggled with something repeatedly
- preferred_framing: only include if the learner responded noticeably better to one style
- memorable_quote: verbatim from the learner's messages only, under 30 words
- daily_summary must be specific to today's content, not generic`;

  const start = Date.now();
  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${apiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { maxOutputTokens: 400, temperature: 0.2 },
        }),
        signal: AbortSignal.timeout(15000),
      }
    );

    if (!res.ok) return null;

    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text?.trim() ?? "";
    const latency = Date.now() - start;

    logAiCall({
      uid: "synthesis",
      user_email: "synthesis",
      model: GEMINI_MODEL,
      prompt_tokens: data?.usageMetadata?.promptTokenCount ?? 0,
      completion_tokens: data?.usageMetadata?.candidatesTokenCount ?? 0,
      latency_ms: latency,
      route: "/api/synthesis/run",
    }).catch(() => {});

    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) return null;

    return JSON.parse(jsonMatch[0]) as SynthesisOutput;
  } catch {
    return null;
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
    return NextResponse.json({ ok: false, reason: "no_api_key" });
  }

  const { session_id, pillar_id }: { session_id: string; pillar_id: PillarId } =
    await req.json();

  if (!session_id || !pillar_id) {
    return NextResponse.json({ ok: false, reason: "missing_params" });
  }

  try {
    const sessionDoc = await getCoachSession(session_id);
    if (!sessionDoc || sessionDoc.uid !== uid) {
      return NextResponse.json({ ok: false, reason: "session_not_found" });
    }

    const transcript = (sessionDoc.transcript as Array<{ role: string; content: string }>) ?? [];
    const synthesis = await runSynthesis(transcript, pillar_id, apiKey);

    if (!synthesis) {
      return NextResponse.json({ ok: false, reason: "synthesis_failed" });
    }

    // Build atomic update — append to arrays, never overwrite
    const db = getFirestore();
    const modelRef = db.collection(COLLECTIONS.LEARNER_MODEL).doc(uid);
    const existing = await getLearnerModel(uid);

    const updates: Record<string, unknown> = {
      uid,
      user_email: userEmail,
      [`daily_summaries.${pillar_id}`]: synthesis.daily_summary,
      last_updated: FieldValue.serverTimestamp(),
    };

    if (synthesis.natural_strengths?.length) {
      updates.natural_strengths = FieldValue.arrayUnion(...synthesis.natural_strengths);
    }
    if (synthesis.recurring_gaps?.length) {
      updates.recurring_gaps = FieldValue.arrayUnion(...synthesis.recurring_gaps);
    }
    if (synthesis.memorable_quote) {
      updates.memorable_quotes = FieldValue.arrayUnion(synthesis.memorable_quote);
    }

    // Consolidate preferred_framing after 2+ consistent days
    if (synthesis.preferred_framing) {
      const currentFraming = existing?.preferred_framing;
      if (!currentFraming || currentFraming === synthesis.preferred_framing) {
        updates.preferred_framing = synthesis.preferred_framing;
      }
    }

    await modelRef.set(updates, { merge: true });

    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ ok: false, reason: "internal_error" });
  }
}
