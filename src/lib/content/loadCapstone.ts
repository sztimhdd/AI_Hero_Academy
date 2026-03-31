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

const _cache: Partial<Record<"en" | "zh", CapstoneContent>> = {};

/**
 * Loads the capstone content for the given language.
 * Falls back to EN if the ZH file is not yet available.
 */
export function loadCapstoneContent(lang: "en" | "zh" = "en"): CapstoneContent {
  if (_cache[lang]) return _cache[lang]!;

  const enPath = path.join(process.cwd(), "content", "pillars", "capstone.json");
  if (!fs.existsSync(enPath)) {
    throw new Error("Capstone content not found");
  }

  if (lang === "zh") {
    const zhPath = path.join(
      process.cwd(),
      "content",
      "zh",
      "pillars",
      "capstone.json"
    );
    if (fs.existsSync(zhPath)) {
      _cache.zh = JSON.parse(fs.readFileSync(zhPath, "utf-8")) as CapstoneContent;
      return _cache.zh;
    }
    // ZH file not yet available — fall back to EN silently
  }

  _cache.en = JSON.parse(fs.readFileSync(enPath, "utf-8")) as CapstoneContent;
  return _cache.en;
}

// Note: fillScenario and fillSectionPrompt are in capstoneUtils.ts (no Node.js deps)
