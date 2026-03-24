#!/usr/bin/env python3
"""
Generate a single canonical atom JSON for the AI Hero Academy atomic library.

Calls Gemini gemini-2.0-flash to produce a complete atom object matching the
atomic_modules_v2.json schema. Output is printed to stdout — review it, then
manually append it to content/atomic_modules_v2.json.

Run:
    python scripts/generate_atom.py --atom-id relationship_intel__meeting_intelligence
    python scripts/generate_atom.py --atom-id <id> --dry-run   # print prompt, exit
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows (console may default to cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()

# ---------------------------------------------------------------------------
# Atom specifications — all 5 Phase 4 atoms
# ---------------------------------------------------------------------------

ATOM_SPECS: dict[str, dict] = {
    "relationship_intel__meeting_intelligence": {
        "title": "Meeting Intelligence: Know Every Room Before You Walk In",
        "domain": "relationship_intel",
        "capability_tags": [
            "meeting_prep",
            "stakeholder_research",
            "action_item_extraction",
            "pre_meeting_synthesis",
            "meeting_follow_up",
        ],
        "employee_hook": "Walk into every meeting knowing more context than the person who called it.",
        "framework": "3-phase loop: Pre-meeting research → In-meeting synthesis → Post-meeting action capture",
        "priority": 1,
    },
    "augmented_comm__email_message_drafting": {
        "title": "Email Intelligence: Draft, Tone, and Send in Minutes",
        "domain": "augmented_comm",
        "capability_tags": [
            "email_drafting",
            "tone_calibration",
            "async_communication",
            "stakeholder_messaging",
            "follow_up_sequencing",
        ],
        "employee_hook": "Email drafting is the #1 daily time sink AI eliminates — reclaim it today.",
        "framework": "TONE framework: Target audience → Objective → Nuance → Edit loop",
        "priority": 2,
    },
    "strategic_prompting__iterative_refinement": {
        "title": "Iterative Prompting: From Good Output to Great Output",
        "domain": "strategic_prompting",
        "capability_tags": [
            "multi_turn_prompting",
            "output_refinement",
            "prompt_iteration",
            "critique_prompting",
            "constraint_narrowing",
        ],
        "employee_hook": "One more prompt turn converts a mediocre draft into something you'd actually send.",
        "framework": "REFINE loop: Review → Evaluate gap → Feed back constraint → Iterate → Next",
        "priority": 3,
    },
    "critical_eval__hallucination_patterns": {
        "title": "Hallucination Patterns: The 5 Most Dangerous AI Errors",
        "domain": "critical_eval",
        "capability_tags": [
            "hallucination_detection",
            "fact_verification",
            "ai_error_patterns",
            "source_checking",
            "credibility_protection",
        ],
        "employee_hook": "One unchecked AI error forwarded to leadership can undo months of credibility.",
        "framework": (
            "5 error types: False facts, Fabricated citations, Plausible-but-wrong numbers, "
            "Confident confabulation, Outdated information"
        ),
        "priority": 4,
    },
    "responsible_ai__ai_tool_governance": {
        "title": "AI Tool Governance: Choose the Right Tool, Every Time",
        "domain": "responsible_ai",
        "capability_tags": [
            "tool_selection",
            "ai_literacy",
            "policy_compliance",
            "tool_risk_assessment",
            "approved_tools",
        ],
        "employee_hook": (
            "Knowing which AI tool to use — and which to avoid — is a career skill, "
            "not a policy box to check."
        ),
        "framework": (
            "SELECT framework: Sensitivity check → Evaluate alternatives → Legal/policy check → "
            "Evaluate data residency → Compare output quality → Track and document"
        ),
        "priority": 5,
    },
}

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an instructional designer authoring atomic AI skills modules for a corporate training app.

Output a single JSON object — no markdown fences, no explanation.

The atom must follow this exact schema:
{
  "atom_id": "<atom_id>",
  "title": "<title>",
  "domain": "<domain>",
  "capability_tags": [...],
  "estimated_minutes": 30,
  "role_variants_hint": "...",
  "reading": {
    "concept_text": "...",
    "good_example": "...",
    "anti_pattern": "...",
    "takeaway": "..."
  },
  "practice": {
    "scenario_template": "...",
    "task_templates": [
      {
        "task_id": 1,
        "text_template": "...",
        "skill_focus": "...",
        "task_mode": "open",
        "mcq_options": null
      }
    ],
    "coach_system_prompt_template": "..."
  },
  "eval": {
    "items_ref": "inline",
    "inline_items": [
      {
        "item_id": "ev_<atom_id>_q1",
        "item_type": "mcq",
        "sequence": 1,
        "question_text": "...",
        "scenario_text": "...",
        "options": [
          {"label": "A", "text": "..."},
          {"label": "B", "text": "..."},
          {"label": "C", "text": "..."},
          {"label": "D", "text": "..."}
        ],
        "correct_answer": "B",
        "score_value": 1
      },
      {
        "item_id": "ev_<atom_id>_q4",
        "item_type": "performance_task",
        "sequence": 4,
        "question_text": "...",
        "scenario_text": "...",
        "rubric": [
          {"criterion": "...", "weight": 0.25},
          {"criterion": "...", "weight": 0.25},
          {"criterion": "...", "weight": 0.25},
          {"criterion": "...", "weight": 0.25}
        ]
      }
    ],
    "source_course_ids": []
  },
  "source_course_ids": [],
  "merged_from": [],
  "atomized_at": "2026-03-24",
  "status": "canonical"
}

Content rules:
1. reading.concept_text must be 150-250 words. First 2 sentences must answer: what is in this for ME personally as an employee — a concrete time saving, quality improvement, or career protection benefit.
2. reading.good_example must show a concrete time-saving or quality-improvement win — not just policy compliance. Use fictional company names (Meridian, Aurora, Crestwood, Northfield, Lakewood) for any scenarios.
3. reading.anti_pattern must describe the costly mistake this skill prevents and its professional consequences.
4. reading.takeaway: one sentence with a specific personal benefit.
5. practice.scenario_template MUST contain {role} and {org_type}. Use ONLY these placeholders — no others: {role}, {org_type}, {case_type}, {data_types}, {workflow_goal}, {programme_name}, {audience}, {sensitivity_level}, {scenario_name}, {organisation}, {domain}
6. practice.task_templates must have exactly 4 tasks. At least 1 task must use task_mode "mcq". For mcq tasks, mcq_options is a list of exactly 3 JSON objects: [{"label": "<full option sentence — this is the button text shown to the learner>", "is_best": true}, {"label": "...", "is_best": false}, {"label": "...", "is_best": false}]. Exactly one has is_best: true. The "label" value MUST be a full descriptive sentence (10–15 words), NOT single letters like "A", "B", "C". For open tasks, mcq_options is null.
7. practice.coach_system_prompt_template must use {role}, {organisation}, {scenario_name}, {domain} — no hardcoded org or role names.
8. eval.inline_items must have exactly 4 items: sequences 1, 2, 3 are item_type "mcq"; sequence 4 is item_type "performance_task".
9. Eval questions must test the specific named framework in this atom — not generic AI knowledge.
10. Never hardcode "EDC", "analyst", or any real organization name in content.
11. Output only valid JSON — no prose, no markdown fences.\
"""


# ---------------------------------------------------------------------------
# Gemini call
# ---------------------------------------------------------------------------

@retry(wait=wait_random_exponential(min=1, max=15), stop=stop_after_attempt(3))
def _call_gemini(prompt: str) -> dict:
    """Call Gemini and return parsed JSON dict."""
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=genai_types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=4096,
        ),
    )
    text = response.text.strip()
    # Strip possible markdown fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def build_prompt(atom_id: str) -> str:
    spec = ATOM_SPECS[atom_id]
    lines = [
        f"Generate a complete canonical atom JSON for atom_id: {atom_id}",
        "",
        f"Title: {spec['title']}",
        f"Domain: {spec['domain']}",
        f"Capability tags: {', '.join(spec['capability_tags'])}",
        f"Employee hook: {spec['employee_hook']}",
        f"Framework to teach: {spec['framework']}",
        "",
        "Follow the schema and all content rules from the system prompt exactly.",
        "Output only the JSON object — nothing else.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--atom-id",
        required=True,
        choices=list(ATOM_SPECS.keys()),
        help="Atom ID to generate",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the LLM prompt and exit — no API call",
    )
    args = parser.parse_args()

    prompt = build_prompt(args.atom_id)

    if args.dry_run:
        print("=== SYSTEM PROMPT ===")
        print(SYSTEM_PROMPT)
        print("\n=== USER PROMPT ===")
        print(prompt)
        return

    print(f"Generating atom: {args.atom_id} ...", file=sys.stderr)
    try:
        atom = _call_gemini(prompt)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Gemini returned invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    # Ensure atom_id matches (LLM occasionally substitutes)
    atom["atom_id"] = args.atom_id

    print(json.dumps(atom, indent=2, ensure_ascii=False))
    print(f"\nDone. Review output above, then append to content/atomic_modules_v2.json.", file=sys.stderr)


if __name__ == "__main__":
    main()
