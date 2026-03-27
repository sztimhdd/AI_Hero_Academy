import { NextRequest } from "next/server";
import { cookies } from "next/headers";
import { getAdminAuth } from "@/lib/firebase/admin";
import { getCoachSession, updateCoachSessionTurns, logAiCall } from "@/lib/firestore/db";
import {
  isTurnBlocked,
  hasMasterySignal,
  makeTaskCompleteEvent,
  stripMasteryToken,
  formatSseEvent,
  TURN_BUDGET,
} from "@/lib/coach/pace";
import type { CoachMessage } from "@/lib/coach/types";

const GEMINI_MODEL = "gemini-2.0-flash";
const GEMINI_STREAM_URL = (apiKey: string) =>
  `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:streamGenerateContent?key=${apiKey}&alt=sse`;

export async function POST(req: NextRequest) {
  // Auth
  const sessionCookie = (await cookies()).get("__session")?.value;
  if (!sessionCookie) {
    return errorSse("Unauthorized");
  }

  let uid: string;
  let userEmail: string;
  try {
    const decoded = await getAdminAuth().verifySessionCookie(sessionCookie, true);
    uid = decoded.uid;
    userEmail = decoded.email ?? "";
  } catch {
    return errorSse("Unauthorized");
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return errorSse("AI service unavailable");
  }

  const {
    session_id,
    task_id,
    user_message,
    conversation_history = [],
  }: {
    session_id: string;
    task_id: string;
    user_message: string;
    conversation_history: CoachMessage[];
  } = await req.json();

  if (!session_id || !task_id || !user_message) {
    return errorSse("session_id, task_id and user_message required");
  }

  // Load session from Firestore
  const sessionDoc = await getCoachSession(session_id);
  if (!sessionDoc || sessionDoc.uid !== uid) {
    return errorSse("Session not found");
  }

  const taskTurnCounts = (sessionDoc.task_turn_counts as Record<string, number>) ?? {};
  const currentCount = taskTurnCounts[task_id] ?? 0;

  // ── PACE: Block Q4 ──────────────────────────────────────────────────────────
  if (isTurnBlocked(currentCount)) {
    return singleEventSse(
      formatSseEvent(makeTaskCompleteEvent("budget_exhausted", task_id))
    );
  }

  // Increment the turn count in Firestore (atomic)
  const newCount = await updateCoachSessionTurns(session_id, task_id);

  // Build Gemini request messages
  const systemPrompt = sessionDoc.system_prompt as string;
  const contents = [
    ...conversation_history.map((m) => ({
      role: m.role,
      parts: [{ text: m.content }],
    })),
    { role: "user", parts: [{ text: user_message }] },
  ];

  const start = Date.now();
  let geminiRes: Response;
  try {
    geminiRes = await fetch(GEMINI_STREAM_URL(apiKey), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        system_instruction: { parts: [{ text: systemPrompt }] },
        contents,
        generationConfig: {
          temperature: 0.4,
          maxOutputTokens: 1024,
        },
      }),
    });
  } catch {
    return errorSse("AI service error");
  }

  if (!geminiRes.ok || !geminiRes.body) {
    return errorSse(`Gemini error ${geminiRes.status}`);
  }

  const encoder = new TextEncoder();
  const decoder = new TextDecoder();

  const stream = new ReadableStream({
    async start(controller) {
      const enqueue = (data: string) => controller.enqueue(encoder.encode(data));

      let accumulatedText = "";
      let promptTokens = 0;
      let completionTokens = 0;

      const reader = geminiRes.body!.getReader();

      try {
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          // SSE lines arrive as "data: <json>\n\n"
          const lines = buffer.split("\n");
          buffer = lines.pop() ?? ""; // keep incomplete last line

          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const raw = line.slice(6).trim();
            if (!raw || raw === "[DONE]") continue;

            let chunk: Record<string, unknown>;
            try {
              chunk = JSON.parse(raw);
            } catch {
              continue;
            }

            // Extract text from the Gemini SSE chunk
            const text =
              (chunk?.candidates as Array<{ content?: { parts?: Array<{ text?: string }> } }>)?.[0]
                ?.content?.parts?.[0]?.text ?? "";

            if (text) {
              // Remove mastery token from the streamed text before forwarding
              const cleanText = text.replace("[[TASK_COMPLETE]]", "");
              accumulatedText += text; // accumulate original (with token) for post-stream check

              if (cleanText) {
                enqueue(formatSseEvent({ type: "text", content: cleanText }));
              }
            }

            // Capture token usage if present
            const usage = chunk?.usageMetadata as
              | { promptTokenCount?: number; candidatesTokenCount?: number }
              | undefined;
            if (usage) {
              promptTokens = usage.promptTokenCount ?? 0;
              completionTokens = usage.candidatesTokenCount ?? 0;
            }
          }
        }
      } finally {
        reader.releaseLock();
      }

      // ── Post-stream: check for mastery / budget exhaustion ──────────────
      if (hasMasterySignal(accumulatedText)) {
        enqueue(formatSseEvent(makeTaskCompleteEvent("mastery_early_exit", task_id)));
      } else if (newCount >= TURN_BUDGET) {
        enqueue(formatSseEvent(makeTaskCompleteEvent("budget_exhausted", task_id)));
      }

      enqueue("data: [DONE]\n\n");
      controller.close();

      // Log AI call (non-blocking)
      const latency = Date.now() - start;
      logAiCall({
        uid,
        user_email: userEmail,
        model: GEMINI_MODEL,
        prompt_tokens: promptTokens,
        completion_tokens: completionTokens,
        latency_ms: latency,
        route: "/api/coach/stream",
      }).catch(() => {});
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      "X-Accel-Buffering": "no",
    },
  });
}

function errorSse(message: string): Response {
  return singleEventSse(
    formatSseEvent({ type: "error", message }) + "data: [DONE]\n\n"
  );
}

function singleEventSse(data: string): Response {
  return new Response(data, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
    },
  });
}

// Keep this file usable in Edge or Node runtimes
export const dynamic = "force-dynamic";
