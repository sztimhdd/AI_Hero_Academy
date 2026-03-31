/**
 * Server-side pillar content loader.
 * Reads from content/pillars/*.json — never from Firestore.
 * Must only be called in server components or API routes.
 */

import fs from "fs";
import path from "path";
import type { PillarId } from "@/lib/firestore/types";

// ── Typed schemas for pillar JSON ─────────────────────────────────────────────

export interface PillarReadingContent {
  concept_text: string;
  good_example: string;
  anti_pattern: string;
  takeaway: string;
}

export interface PracticeTask {
  task_id: string;
  task_number: number;
  title: string;
  mode: string;
  learning_objective: string;
  prompt_template: string;
  rubric: Record<string, string>;
}

export interface QuizItem {
  item_id: string;
  type: "mcq" | "open_rubric";
  question: string;
  // MCQ only
  options?: Record<string, string>;
  correct_answer?: string;
  explanation?: string;
  // Open rubric only
  rubric?: Record<string, string>;
  max_score?: number;
  score_weight: number;
}

export interface PillarQuiz {
  items: QuizItem[];
  pass_threshold: number;
  max_score: number;
  fail_guidance: string;
}

export interface BuildArtifactConfig {
  artifact_type: string;
  artifact_name: string;
  artifact_description: string;
  prompt: string;
  coach_closing_prompt: string;
}

export interface PillarContent {
  pillar_id: PillarId;
  pillar_name: string;
  day_number: number;
  framework?: string;
  coaching_vocabulary?: Record<string, string>;
  estimated_minutes: number;
  reading: PillarReadingContent;
  practice: {
    scenario_template: string;
    tasks: PracticeTask[];
    coach_system_prompt_template: string;
  };
  quiz: PillarQuiz;
  build_artifact: BuildArtifactConfig;
}

/** Map from pillar_id to the filename slug. */
const PILLAR_FILE_MAP: Partial<Record<PillarId, string>> = {
  p1: "p1_foundation",
  p2: "p2_prompting",
  p3: "p3_tool_fluency",
  p4: "p4_configuration",
  p5: "p5_workflow",
  p6: "p6_agentic",
};

/**
 * Loads and returns the content for a given pillar.
 * When lang is "zh", loads from content/zh/pillars/ with silent EN fallback.
 * Throws if the EN pillar JSON does not exist.
 */
export function loadPillarContent(
  pillarId: string,
  lang: "en" | "zh" = "en"
): PillarContent {
  const slug = PILLAR_FILE_MAP[pillarId as PillarId];
  if (!slug) {
    throw new Error(`Unknown pillar: ${pillarId}`);
  }

  const enPath = path.join(process.cwd(), "content", "pillars", `${slug}.json`);

  if (!fs.existsSync(enPath)) {
    throw new Error(`Pillar content not yet available: ${pillarId}`);
  }

  if (lang === "zh") {
    const zhPath = path.join(
      process.cwd(),
      "content",
      "zh",
      "pillars",
      `${slug}.json`
    );
    if (fs.existsSync(zhPath)) {
      return JSON.parse(fs.readFileSync(zhPath, "utf-8")) as PillarContent;
    }
    // ZH file not yet available — fall back to EN silently
  }

  return JSON.parse(fs.readFileSync(enPath, "utf-8")) as PillarContent;
}
