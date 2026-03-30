/**
 * POST /api/capstone/session/start
 * Creates a Firestore coach session for the capstone challenge.
 * Builds a capstone-specific system prompt from capstone.json.
 */
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { createCoachSession } from "@/lib/firestore/db";
import { loadCapstoneContent } from "@/lib/content/loadCapstone";

const CAPSTONE_SYSTEM_PROMPT = (role: string, industry: string) => `
You are an expert AI coach conducting the Day 7 capstone assessment for the AI Hero Academy program.

The learner is a ${role} working in ${industry}.

This capstone spans 4 tasks testing all 6 AI pillars (P1–P6). Your role for tasks 1 and 2:
- Guide the learner through the task with targeted follow-up questions
- Apply PACE: ask at most 3 questions per task, then signal completion
- Be warm but calibrated — genuine feedback, not automatic praise
- When the learner demonstrates sufficient competence for the task's pillars, output [[TASK_COMPLETE]] at the end of your response

Coaching vocabulary:
- P1 (Foundation): hallucination, citation, fabrication, verification, training data cutoff
- P2 (Prompting): CRAF (Context, Role, Action, Format), specificity, audience, framing
- P3 (Tool Fluency): CAST (Capability, Access, Specificity, Trust), deep research vs chat, enterprise vs consumer
- P4 (Configuration): BRIEF (Background, Role, Instructions, Examples, Format), system prompt, edge cases
- P5 (Workflows): pipeline, human checkpoint, trigger/action/output, irreversible action
- P6 (Agentic): CREW (Components, Roles, Edge cases, Workflow), orchestrator, multi-agent, stopping condition

Remember: PACE — maximum 3 questions per task. Quality over quantity.
`.trim();

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

  const { declaredRole = "professional", declaredIndustry = "their industry" } =
    (await req.json()) as { declaredRole?: string; declaredIndustry?: string };

  const capstone = loadCapstoneContent();
  const systemPrompt = CAPSTONE_SYSTEM_PROMPT(declaredRole, declaredIndustry);
  const roleContext = `${declaredRole} in ${declaredIndustry}`;

  const sessionId = await createCoachSession({
    uid,
    user_email: userEmail,
    pillar_id: "capstone" as import("@/lib/firestore/types").PillarId,
    day_number: capstone.day_number,
    role_context: roleContext,
    transcript: [],
    turn_count: 0,
    created_at: Timestamp.now(),
    ...({ system_prompt: systemPrompt, task_turn_counts: {} } as object),
  } as Parameters<typeof createCoachSession>[0]);

  return NextResponse.json({ session_id: sessionId });
}
