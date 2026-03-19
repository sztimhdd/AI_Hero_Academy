#!/usr/bin/env python3
"""
Convert 72 role-specific diagnostic items into role-agnostic atomic templates.

Reads:  content/diagnostic_items.json
Writes: content/atomic_diagnostic_items.json

Run:
    python scripts/atomize_diagnostics.py                           # all 72
    python scripts/atomize_diagnostics.py --dry-run                 # pretty-print, no write
    python scripts/atomize_diagnostics.py --item-id rm_diag_ra1_mcq  # single test
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import urllib3
import requests as _requests

# Corporate SSL proxy workaround: same pattern as atomize_coursework.py.
# Set DATABRICKS_INSECURE=1 to disable SSL verification (dev-only batch script).
_INSECURE = os.environ.get("DATABRICKS_INSECURE", "").lower() in ("1", "true", "yes")
if _INSECURE:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from tenacity import retry, wait_random_exponential, stop_after_attempt

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATABRICKS_HOST = os.environ.get(
    "DATABRICKS_HOST", "https://adb-2717931942638877.17.azuredatabricks.net"
)
SONNET_ENDPOINT = os.environ.get("SONNET_ENDPOINT", "databricks-claude-sonnet-4-6")
CONTENT_DIR = Path(__file__).parent.parent / "content"
MAX_WORKERS = 4

# ---------------------------------------------------------------------------
# Extraction prompts
# ---------------------------------------------------------------------------

# Unified de-role prompt for MCQ items.
# Handles: question_text + scenario_text + all 4 MCQ option texts.
MCQ_DEROLE_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

De-role the following multiple-choice diagnostic assessment item by replacing all
role-specific and organisation-specific language with template placeholders. The
result must be usable for any professional role without modification.

<domain>{domain_id}</domain>
<question_text>
{question_text}
</question_text>
<scenario_text>
{scenario_text}
</scenario_text>
<options>
{options_text}
</options>

Available placeholders (use ONLY these):
- {{role}} — learner's job title
  (replaces "RM", "Relationship Manager", "Underwriter", "analyst", "marketing manager",
   "underwriter", "account manager", and similar job titles)
- {{org_type}} — type of organization
  (replaces "bank", "trade finance firm", "EDC", "credit union", "the organization",
   "your organization's", "Apex Trade Finance", "the company")
- {{client_name}} — fictional client company name
  (replaces "Crestwood Logistics", "Vantara Foods", "Thornfield Agri-Export",
   "Driftwood Packaging", "Irongate Civil", "Northern Fabrication", and any other
   named fictional client)
- {{industry}} — client's industry sector
  (replaces "freight logistics", "food manufacturing", "construction", "retail",
   "manufacturing and logistics", and similar sector references)
- {{document_type}} — type of professional document
  (replaces "credit memo", "briefing note", "risk summary", "covenant analysis section",
   "facility report", and similar document types)
- {{meeting_type}} — type of meeting or review
  (replaces "annual review meeting", "facility renewal meeting", "credit committee",
   and similar meeting or review process references)
- {{workflow_action}} — the professional workflow activity being performed
  (replaces "portfolio outreach", "deal structuring", "client briefing preparation",
   and similar work tasks)

Output a single JSON object — no prose, no markdown fences:
{{
  "question_template": "<de-roled question text>",
  "scenario_template": "<de-roled scenario text>",
  "options": [
    {{"label": "A", "text_template": "<de-roled option A text>"}},
    {{"label": "B", "text_template": "<de-roled option B text>"}},
    {{"label": "C", "text_template": "<de-roled option C text>"}},
    {{"label": "D", "text_template": "<de-roled option D text>"}}
  ]
}}

Rules:
- Replace ALL job titles with {{role}} (including possessives: "an RM's" → "a {{role}}'s")
- Replace ALL named fictional organisations (client companies and employer firms) with the
  appropriate placeholder: client companies → {{client_name}},
  the learner's employer → {{org_type}}
- Preserve EVERY option's meaning and correctness — de-role the framing only;
  the correct answer must remain correct after de-roling
- The question_template and scenario_template MUST each contain at least {{role}}
- Do NOT paraphrase or simplify content — de-role identifiers only
- Return only the JSON object\
"""

# Unified de-role prompt for micro-task items.
# Handles: question_text + scenario_text + rubric criteria descriptions.
TASK_DEROLE_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

De-role the following micro-task diagnostic assessment item by replacing all
role-specific and organisation-specific language with template placeholders. The
result must be usable for any professional role without modification.

<domain>{domain_id}</domain>
<question_text>
{question_text}
</question_text>
<scenario_text>
{scenario_text}
</scenario_text>
<rubric_criteria>
{rubric_criteria_text}
</rubric_criteria>

Available placeholders (use ONLY these):
- {{role}} — learner's job title
  (replaces "RM", "Relationship Manager", "Underwriter", "analyst", "marketing manager",
   "underwriter", "account manager", and similar job titles)
- {{org_type}} — type of organization
  (replaces "bank", "trade finance firm", "EDC", "credit union", "the organization",
   "your organization's", "Apex Trade Finance", "the company")
- {{client_name}} — fictional client company name
  (replaces any named fictional client)
- {{industry}} — client's industry sector
- {{document_type}} — type of professional document
- {{meeting_type}} — type of meeting or review

Output a single JSON object — no prose, no markdown fences:
{{
  "question_template": "<de-roled question text>",
  "scenario_template": "<de-roled scenario text>",
  "rubric_criteria": [
    {{"name": "<criterion name>", "description_template": "<de-roled description>", "max": <integer>}},
    ...one object per criterion...
  ]
}}

Rules:
- Replace ALL job titles with {{role}} (including possessives)
- Replace ALL named fictional organisations with the appropriate placeholder
- Preserve rubric grading logic and scoring intent exactly — de-role identifiers only
- The question_template and scenario_template MUST each contain at least {{role}}
- Do NOT paraphrase or simplify content — de-role identifiers only
- Return only the JSON object\
"""

# ---------------------------------------------------------------------------
# HTTP / LLM helpers (identical pattern to atomize_coursework.py)
# ---------------------------------------------------------------------------

def _get_token() -> str:
    """Get a fresh OAuth token via the Databricks CLI."""
    import subprocess
    result = subprocess.run(
        ["databricks", "auth", "token", "--host", DATABRICKS_HOST, "--profile", "dev"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        token = os.environ.get("DATABRICKS_TOKEN", "")
        if not token:
            raise RuntimeError(f"Could not get Databricks token: {result.stderr}")
        return token
    return json.loads(result.stdout)["access_token"]


_TOKEN: str | None = None


def _token() -> str:
    global _TOKEN
    if _TOKEN is None:
        _TOKEN = os.environ.get("DATABRICKS_TOKEN") or _get_token()
    return _TOKEN


@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
def _call_llm(prompt: str) -> str:
    """Call Sonnet via direct HTTP and return raw text content."""
    url = f"{DATABRICKS_HOST}/serving-endpoints/{SONNET_ENDPOINT}/invocations"
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 2048,
    }
    resp = _requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {_token()}"},
        verify=not _INSECURE,
        timeout=60,
    )
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"].strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return text


def _extract_json(prompt: str):
    return json.loads(_call_llm(prompt))


# ---------------------------------------------------------------------------
# Per-item de-roling
# ---------------------------------------------------------------------------

def _format_options(options: list[dict]) -> str:
    """Format MCQ options as readable text for the prompt."""
    lines = []
    for opt in options:
        lines.append(f"{opt['label']}. {opt['text']}")
    return "\n".join(lines)


def _format_rubric_criteria(criteria: list[dict]) -> str:
    """Format rubric criteria as readable text for the prompt."""
    lines = []
    for c in criteria:
        lines.append(f"[name: {c['name']} | max: {c['max']}]\n{c['description']}")
    return "\n\n".join(lines)


def derole_item(item: dict) -> tuple[str, dict]:
    """De-role a single diagnostic item. Returns (item_id, atomic_item_dict)."""
    item_id = item["item_id"]
    item_type = item["item_type"]
    domain_id = item["domain_id"]

    if item_type == "mcq":
        options_text = _format_options(item["options"])
        prompt = MCQ_DEROLE_PROMPT.format(
            domain_id=domain_id,
            question_text=item["question_text"],
            scenario_text=item["scenario_text"],
            options_text=options_text,
        )
        result = _extract_json(prompt)
        print(f"  ✓ [{item_id}] de-roled (mcq)")

        # Merge is_correct from original into de-roled options
        correct = item.get("correct_option", "")
        options_out = []
        for opt in result.get("options", []):
            options_out.append({
                "label": opt["label"],
                "text_template": opt["text_template"],
                "is_correct": opt["label"] == correct,
            })

        atomic = {
            "source_item_id": item_id,
            "domain_id": domain_id,
            "item_type": "mcq",
            "display_order": item["display_order"],
            "question_template": result["question_template"],
            "scenario_template": result["scenario_template"],
            "options": options_out,
            "correct_option": correct,
            "scoring_rubric": item["scoring_rubric"],
            "role_id_hint": item["role_id"],
            "atomized_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "status": "draft",
        }

    elif item_type in ("micro_task", "prompt_sandbox"):
        criteria = item["scoring_rubric"].get("criteria", [])
        rubric_text = _format_rubric_criteria(criteria)
        prompt = TASK_DEROLE_PROMPT.format(
            domain_id=domain_id,
            question_text=item["question_text"],
            scenario_text=item["scenario_text"],
            rubric_criteria_text=rubric_text,
        )
        result = _extract_json(prompt)
        print(f"  ✓ [{item_id}] de-roled ({item_type})")

        # Preserve max scores from original criteria
        rubric_out = []
        for i, crit in enumerate(result.get("rubric_criteria", [])):
            original_max = criteria[i]["max"] if i < len(criteria) else crit.get("max", 2)
            rubric_out.append({
                "name": crit["name"],
                "description_template": crit["description_template"],
                "max": original_max,
            })

        atomic = {
            "source_item_id": item_id,
            "domain_id": domain_id,
            "item_type": item_type,
            "display_order": item["display_order"],
            "question_template": result["question_template"],
            "scenario_template": result["scenario_template"],
            "rubric_criteria": rubric_out,
            "scoring_rubric": item["scoring_rubric"],  # original preserved for reference
            "role_id_hint": item["role_id"],
            "atomized_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "status": "draft",
        }

    else:
        raise ValueError(f"Unknown item_type: {item_type!r} for {item_id}")

    return item_id, atomic


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _validate_atomic_item(atomic: dict) -> list[str]:
    """Return list of validation error strings (empty = pass)."""
    errors = []
    item_id = atomic.get("source_item_id", "?")

    # At least one of question_template or scenario_template must contain {role}
    q = atomic.get("question_template", "") or ""
    s = atomic.get("scenario_template", "") or ""
    if "{role}" not in q and "{role}" not in s:
        errors.append(f"{item_id}: neither question_template nor scenario_template contains {{role}}")

    if atomic["item_type"] == "mcq":
        options = atomic.get("options", [])
        if len(options) != 4:
            errors.append(f"{item_id}: expected 4 options, got {len(options)}")
        correct_count = sum(1 for o in options if o.get("is_correct"))
        if correct_count != 1:
            errors.append(f"{item_id}: expected 1 correct option, got {correct_count}")

    if atomic["item_type"] == "micro_task":
        criteria = atomic.get("rubric_criteria", [])
        if not criteria:
            errors.append(f"{item_id}: micro_task has no rubric_criteria")

    return errors


# ---------------------------------------------------------------------------
# Dry-run pretty-printer
# ---------------------------------------------------------------------------

def _print_dry_run(item_id: str, atomic: dict) -> None:
    errors = _validate_atomic_item(atomic)
    status = "✓" if not errors else "✗"
    print(f"\n{'='*70}")
    print(f"  {status} {item_id}  [{atomic['item_type']}] domain={atomic['domain_id']}")
    print(f"  question_template: {atomic.get('question_template', '')[:120]}")
    print(f"  scenario_template: {(atomic.get('scenario_template') or '')[:120]}")
    if atomic["item_type"] == "mcq":
        for opt in atomic.get("options", []):
            marker = "✓" if opt.get("is_correct") else " "
            print(f"  [{marker}] {opt['label']}: {opt.get('text_template', '')[:80]}")
    elif atomic["item_type"] == "micro_task":
        for c in atomic.get("rubric_criteria", []):
            print(f"  rubric [{c['name']}]: {c.get('description_template', '')[:80]}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout; do not write file")
    parser.add_argument("--item-id", help="Process only this item_id")
    args = parser.parse_args()

    # Load source data
    items_path = CONTENT_DIR / "diagnostic_items.json"
    if not items_path.exists():
        sys.exit(f"ERROR: {items_path} not found")
    items: list[dict] = json.loads(items_path.read_text(encoding="utf-8"))

    # Filter to single item if requested
    if args.item_id:
        filtered = [i for i in items if i["item_id"] == args.item_id]
        if not filtered:
            sys.exit(f"ERROR: item_id '{args.item_id}' not in diagnostic_items.json")
        items = filtered

    print(f"Processing {len(items)} item(s) with up to {MAX_WORKERS} workers...")

    # Load existing output if merging single-item re-runs
    out_path = CONTENT_DIR / "atomic_diagnostic_items.json"
    existing: dict = {}
    if out_path.exists() and args.item_id:
        existing = json.loads(out_path.read_text(encoding="utf-8"))

    results: dict = dict(existing)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(derole_item, item): item["item_id"] for item in items}
        for future in as_completed(futures):
            item_id = futures[future]
            try:
                iid, atomic = future.result()
                results[iid] = atomic
                print(f"  Done: {iid}")
            except Exception as exc:
                print(f"  ERROR [{item_id}]: {exc}", file=sys.stderr)

    # Validation summary
    all_errors: list[str] = []
    for atomic in results.values():
        all_errors.extend(_validate_atomic_item(atomic))

    if args.dry_run:
        print("\n--- DRY RUN OUTPUT ---")
        for iid, atomic in sorted(results.items()):
            _print_dry_run(iid, atomic)
        print(f"\n--- SUMMARY: {len(results)} items, {len(all_errors)} validation errors ---")
    else:
        out_path.write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\nWrote {len(results)} items to {out_path}")
        if all_errors:
            print(f"VALIDATION WARNINGS ({len(all_errors)}):")
            for e in all_errors:
                print(f"  {e}")
        else:
            print("All validation checks passed.")


if __name__ == "__main__":
    main()
