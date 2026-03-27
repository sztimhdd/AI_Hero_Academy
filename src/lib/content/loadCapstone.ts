/**
 * Loads the capstone challenge content (content/pillars/capstone.json).
 * Server-side only.
 */

import fs from "fs";
import path from "path";

export interface CapstoneMcqItem {
  item_id: string;
  pillar: string;
  question: string;
  options: Record<string, string>;
  correct_answer: string;
}

export interface CapstoneSection {
  section_id: string;
  section_number: number;
  title: string;
  pillars_tested: string[];
  type: "text_input" | "mcq_cluster" | "open_design";
  estimated_minutes: number;
  prompt_template?: string;
  coach_rubric?: Record<string, Record<string, string>>;
  items?: CapstoneMcqItem[];
  pass_threshold_within_section?: number;
  coach_closing_prompt?: string;
}

export interface CapstoneContent {
  capstone_id: string;
  title: string;
  day_number: number;
  estimated_minutes: number;
  description: string;
  pass_criteria: string;
  scenario_template: string;
  sections: CapstoneSection[];
}

let _cached: CapstoneContent | null = null;

export function loadCapstoneContent(): CapstoneContent {
  if (_cached) return _cached;
  const filePath = path.join(
    process.cwd(),
    "content",
    "pillars",
    "capstone.json"
  );
  if (!fs.existsSync(filePath)) {
    throw new Error("Capstone content not found");
  }
  _cached = JSON.parse(fs.readFileSync(filePath, "utf-8")) as CapstoneContent;
  return _cached;
}

// Note: fillScenario and fillSectionPrompt are in capstoneUtils.ts (no Node.js deps)
