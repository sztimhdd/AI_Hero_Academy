/**
 * Assembles the final coach system prompt from:
 * - The pillar's coach_system_prompt_template (from content/pillars/*.json)
 * - The learner's UserProfile fields
 * - The learner's LearnerModel (prior pillar context for 7-day arc continuity)
 * - Language instruction (ZH if lang === "zh")
 *
 * Server-side only — called by /api/coach/session/start.
 */

import type { UserProfile, LearnerModel, PillarId } from "@/lib/firestore/types";

const ZH_LANGUAGE_INSTRUCTION = `

## Language Instruction
Please respond in Simplified Chinese throughout this coaching session. Do not use English except for: AI technical terms (LLM, GPT, Claude, RAG, CoT, JSON, API, MCP, system prompt, temperature), tool names (ChatGPT, Midjourney, Cursor, n8n, Copilot), and fictional scenario names provided in the module. The mastery signal [[TASK_COMPLETE]] must always remain in English exactly as written.`;

const MASTERY_SIGNAL_INSTRUCTION = `

## Mastery Signal (System Use Only)
When you have determined that the task's learning objective is fully met and you are delivering your closing bridge statement, append the exact token [[TASK_COMPLETE]] on its own line at the very end of your response. This is a system signal to advance the learner to the next task. Do not explain it. Do not mention it to the learner.`;

/** Pillar IDs in display order for prior context injection. */
const PILLAR_ORDER: PillarId[] = ["p1", "p2", "p3", "p4", "p5", "p6"];

const PILLAR_NAMES: Record<PillarId | "capstone", string> = {
  p1: "P1 (AI Foundation)",
  p2: "P2 (Prompting)",
  p3: "P3 (Tool Fluency)",
  p4: "P4 (Configuration)",
  p5: "P5 (Workflow Design)",
  p6: "P6 (Agentic Systems)",
  capstone: "Capstone",
};

function buildPriorSummaries(learnerModel: LearnerModel | null): string {
  if (!learnerModel?.daily_summaries) return "(none — Day 1)";
  const entries = PILLAR_ORDER.map((pid) => {
    const summary = learnerModel.daily_summaries[pid];
    if (!summary) return null;
    return `- ${PILLAR_NAMES[pid]}: ${summary}`;
  }).filter(Boolean);
  return entries.length > 0 ? entries.join("\n") : "(none — Day 1)";
}

function buildPriorScores(learnerModel: LearnerModel | null): string {
  if (!learnerModel) return "(none — Day 1)";
  // LearnerModel doesn't store pillar_scores directly; those live in b2c_training_progress.
  // For now emit a placeholder — the assembler receives what the session/start route passes.
  return "(see daily summaries above)";
}

/**
 * Assembles the full system prompt for a coaching session.
 *
 * @param template   The raw `coach_system_prompt_template` from the pillar JSON.
 * @param profile    The learner's UserProfile (role, industry, daily work, lang).
 * @param learnerModel  The learner's current LearnerModel, or null on Day 1.
 */
export function assembleCoachPrompt(
  template: string,
  profile: Pick<
    UserProfile,
    "declared_role" | "declared_industry" | "daily_work_desc" | "lang"
  >,
  learnerModel: LearnerModel | null
): string {
  const role = profile.declared_role ?? "professional";
  const industry = profile.declared_industry ?? "your industry";
  const dailyWork = profile.daily_work_desc ?? "daily professional work";

  let prompt = template
    .replaceAll("{declared_role}", role)
    .replaceAll("{declared_industry}", industry)
    .replaceAll("{daily_work_desc}", dailyWork)
    .replaceAll("{prior_pillar_summaries}", buildPriorSummaries(learnerModel))
    .replaceAll("{prior_pillar_scores}", buildPriorScores(learnerModel));

  prompt += MASTERY_SIGNAL_INSTRUCTION;

  if (profile.lang === "zh") {
    prompt += ZH_LANGUAGE_INSTRUCTION;
  }

  return prompt;
}
