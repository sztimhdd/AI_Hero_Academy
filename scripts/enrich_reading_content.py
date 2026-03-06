#!/usr/bin/env python3
"""
Enrich content/reading_content.json with structured sub-fields for template rendering.

Reads:  content/reading_content.json
Writes: content/reading_content_structured.json

Run:
    python scripts/enrich_reading_content.py              # enrich all items
    python scripts/enrich_reading_content.py --dry-run    # print to stdout, no write
    python scripts/enrich_reading_content.py --course-id rm_c1_responsible_ai  # single item
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Ensure UTF-8 output on Windows (console may default to cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from tenacity import retry, wait_random_exponential, stop_after_attempt

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HAIKU_ENDPOINT = os.environ.get("HAIKU_ENDPOINT", "databricks-claude-haiku-4-5")
CONTENT_DIR = Path(__file__).parent.parent / "content"
MAX_WORKERS = 4

# ---------------------------------------------------------------------------
# Extraction prompts (module-level constants)
# ---------------------------------------------------------------------------

CONCEPT_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following concept_text field. The text describes a
named acronym framework (e.g. CRAF, SAFE, VERIFY) used in a professional AI workflow.

<concept_text>
{concept_text}
</concept_text>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "framework_acronym": "<the acronym letters, e.g. CRAF>",
  "intro": "<1-2 sentences introducing the framework and why it matters>",
  "cards": [
    {{"letter": "<single uppercase letter>", "title": "<one word>", "body": "<1-2 sentence description>"}},
    ...one card per acronym letter...
  ],
  "guardrails": ["<constraint 1>", ...]
}}

Rules:
- Extract one card per letter in the acronym, in order
- Preserve the source text closely; do not paraphrase beyond minor cleanup
- guardrails: extract any listed rules/constraints; use [] if none exist
- Return only the JSON object\
"""

GOOD_EXAMPLE_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following good_example field. The text describes a
before/after scenario comparing an unsafe AI prompt with a corrected version.

<good_example>
{good_example}
</good_example>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "scenario": "<1 sentence: what task the practitioner is trying to accomplish>",
  "before_prompt": "<the unsafe/incorrect prompt or action, as a direct quote or close paraphrase>",
  "before_issue": "<1 sentence: what specific problem makes this unsafe or incorrect>",
  "after_prompt": "<the safe/correct prompt or action, as a direct quote or close paraphrase>",
  "after_benefit": "<1 sentence: what specific quality makes this version correct>",
  "outcome": "<1 sentence: what the corrected approach produces or achieves>"
}}

Rules:
- before_prompt and after_prompt should read as actual prompt text (monospace-renderable)
- Keep before_issue and after_benefit short — they appear as captions under the prompt
- Return only the JSON object\
"""

ANTI_PATTERN_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following anti_pattern field. The text describes a
failure scenario and its consequences.

<anti_pattern>
{anti_pattern}
</anti_pattern>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "headline": "<3-6 word name for this failure pattern>",
  "failure_scenario": "<2-3 sentences: what the practitioner did wrong and the immediate error>",
  "chain": ["<consequence 1>", "<consequence 2>", "<final impact (most damaging outcome)>"],
  "root_lesson": "<1-2 sentences: the specific rule or check that was skipped>"
}}

Rules:
- chain: 2-4 items; each is a single step in the domino effect; final item is the most damaging outcome
- root_lesson must be actionable — what the learner should always do instead
- Return only the JSON object\
"""

TAKEAWAY_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Given the reading item below, produce a structured takeaway with two action cards.

<concept_text>
{concept_text}
</concept_text>

<takeaway>
{takeaway}
</takeaway>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "statement": "<the takeaway sentence — preserve exactly as written>",
  "action_1": {{"title": "<3-5 word imperative>", "body": "<1-2 sentence elaboration>"}},
  "action_2": {{"title": "<3-5 word imperative>", "body": "<1-2 sentence elaboration>"}}
}}

Rules:
- statement: copy the takeaway text exactly; do not paraphrase
- action_1 and action_2: synthesise two complementary action points from the concept_text
  and takeaway; they should answer "what do I actually do differently on the job?"
- Return only the JSON object\
"""

# ---------------------------------------------------------------------------
# AI extraction helpers
# ---------------------------------------------------------------------------

@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
def _extract(w: WorkspaceClient, prompt: str) -> dict:
    """Call Haiku and return parsed JSON dict."""
    resp = w.serving_endpoints.query(
        name=HAIKU_ENDPOINT,
        messages=[ChatMessage(role=ChatMessageRole.USER, content=prompt)],
        temperature=0.0,
        max_tokens=1024,
    )
    text = resp.choices[0].message.content.strip()
    # Strip possible markdown fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def enrich_item(w: WorkspaceClient, course_id: str, item: dict) -> tuple[str, dict]:
    """Extract all 4 structured sub-fields for one reading item sequentially."""
    structured = {}
    extractions = [
        ("concept_text_structured",  lambda: CONCEPT_PROMPT.format(**item)),
        ("good_example_structured",  lambda: GOOD_EXAMPLE_PROMPT.format(**item)),
        ("anti_pattern_structured",  lambda: ANTI_PATTERN_PROMPT.format(**item)),
        ("takeaway_structured",      lambda: TAKEAWAY_PROMPT.format(**item)),
    ]
    for field, prompt_fn in extractions:
        try:
            structured[field] = _extract(w, prompt_fn())
            print(f"  ✓ [{course_id}] {field}")
        except Exception as exc:
            print(f"  WARN [{course_id}] {field}: {exc}", file=sys.stderr)
    return course_id, structured


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout; do not write file")
    parser.add_argument("--course-id", help="Process only this course_id")
    args = parser.parse_args()

    # Load source data
    reading_path = CONTENT_DIR / "reading_content.json"
    if not reading_path.exists():
        sys.exit(f"ERROR: {reading_path} not found")
    reading: dict = json.loads(reading_path.read_text(encoding="utf-8"))

    # Filter to single item if requested
    if args.course_id:
        if args.course_id not in reading:
            sys.exit(f"ERROR: course_id '{args.course_id}' not in reading_content.json")
        reading = {args.course_id: reading[args.course_id]}

    print(f"Processing {len(reading)} item(s) with up to {MAX_WORKERS} workers...")

    # Load existing structured file if it exists (so we can merge)
    out_path = CONTENT_DIR / "reading_content_structured.json"
    existing: dict = {}
    if out_path.exists() and not args.course_id:
        existing = json.loads(out_path.read_text(encoding="utf-8"))

    w = WorkspaceClient()
    results: dict = dict(existing)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(enrich_item, w, cid, item): cid
            for cid, item in reading.items()
        }
        for future in as_completed(futures):
            course_id = futures[future]
            try:
                cid, structured = future.result()
                results[cid] = structured
                print(f"  Done: {cid}")
            except Exception as exc:
                print(f"  ERROR [{course_id}]: {exc}", file=sys.stderr)

    if args.dry_run:
        print("\n--- DRY RUN OUTPUT ---")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        out_path.write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\nWrote {len(results)} courses to {out_path}")


if __name__ == "__main__":
    main()
