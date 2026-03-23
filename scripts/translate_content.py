#!/usr/bin/env python3
"""
Translate AI Hero Academy content files from English to Simplified Chinese.

Writes translated files to content/zh/{filename}.
For content/i18n/zh.json, overwrites in place (not in zh/ subdir).

Usage:
    python scripts/translate_content.py              # all files
    python scripts/translate_content.py --file courses      # single file
    python scripts/translate_content.py --dry-run           # print to stdout
    python scripts/translate_content.py --role rm           # filter to one role
"""

import argparse
import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from tenacity import retry, wait_random_exponential, stop_after_attempt

CONTENT_DIR = Path(__file__).parent.parent / "content"
ZH_DIR = CONTENT_DIR / "zh"
SONNET_ENDPOINT = "databricks-claude-sonnet-4-6"

SYSTEM_PROMPT = """\
You are a professional Simplified Chinese (简体中文) translator for corporate AI training
materials in financial services.

Translation rules:
1. Translate ONLY the user-visible text fields specified in the task. Return valid JSON.
2. Keep ALL JSON keys, IDs, booleans, numbers, scoring weights in English as-is.
3. Framework acronyms (SAFE, CRAF, VERIFY, TRACE, STAKE): keep in English;
   on first use within a document add Chinese meaning in parentheses,
   e.g. "SAFE抽象法（敏感数据处理框架）".
4. Fictional company names (Meridian, Aurora, Crestwood, Apex, Maple, Northern, etc.): keep in English.
5. {placeholder} variables (e.g. {role}, {n}, {name}): keep exactly as-is.
6. Professional financial services register. Formal writing style.
7. Return only valid JSON — no markdown code fences, no explanation text."""


# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

@retry(wait=wait_random_exponential(min=2, max=20), stop=stop_after_attempt(3))
def _call(w: WorkspaceClient, user_content: str) -> str:
    resp = w.serving_endpoints.query(
        name=SONNET_ENDPOINT,
        messages=[ChatMessage(role=ChatMessageRole.USER, content=user_content)],
        temperature=0.1,
        max_tokens=8192,
    )
    return resp.choices[0].message.content.strip()


def _strip_fences(raw: str) -> str:
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:]).strip()
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0].strip()
    return raw


def _translate_batch(w: WorkspaceClient, batch: list | dict, fields: list[str], task_desc: str) -> list | dict:
    """Translate a batch (list or dict) of entries. Returns translated batch of same type."""
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Task: {task_desc}\n"
        f"Fields to translate: {', '.join(fields)}\n\n"
        f"Input JSON:\n{json.dumps(batch, ensure_ascii=False, indent=2)}\n\n"
        "Return the translated JSON with the same structure."
    )
    raw = _call(w, prompt)
    raw = _strip_fences(raw)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# File-specific translators
# ---------------------------------------------------------------------------

def translate_roles(w: WorkspaceClient, dry_run: bool, role_filter: str | None):
    src = json.loads((CONTENT_DIR / "roles.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items() if not role_filter or k == role_filter}
    print(f"[roles] Translating {len(entries)} entries...")
    result = dict(src)  # copy all keys; overwrite translated entries
    translated = _translate_batch(w, entries, ["title", "description"], "Translate role titles and descriptions.")
    result.update(translated)
    _write_or_print(ZH_DIR / "roles.json", result, dry_run)
    print(f"  ✓ roles.json: {len(translated)} entries translated")


def translate_domains(w: WorkspaceClient, dry_run: bool, role_filter: str | None):
    src = json.loads((CONTENT_DIR / "domains.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or v.get("role_id") == role_filter}
    print(f"[domains] Translating {len(entries)} entries in batches of 6...")
    keys = list(entries.keys())
    result = dict(src)
    for i in range(0, len(keys), 6):
        batch_keys = keys[i:i + 6]
        batch = {k: entries[k] for k in batch_keys}
        translated = _translate_batch(
            w, batch,
            ["name", "description", "level_descriptors"],
            "Translate domain names, descriptions, and all level descriptor values."
        )
        result.update(translated)
        print(f"  ✓ domains batch {i // 6 + 1}: {len(batch_keys)} entries")
    _write_or_print(ZH_DIR / "domains.json", result, dry_run)
    print(f"  ✓ domains.json: {len(entries)} entries written")


def translate_courses(w: WorkspaceClient, dry_run: bool, role_filter: str | None):
    src = json.loads((CONTENT_DIR / "courses.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or v.get("role_id") == role_filter}
    print(f"[courses] Translating {len(entries)} entries in batches of 5...")
    keys = list(entries.keys())
    result = dict(src)
    for i in range(0, len(keys), 5):
        batch_keys = keys[i:i + 5]
        batch = {k: entries[k] for k in batch_keys}
        translated = _translate_batch(
            w, batch,
            ["title", "tagline", "description", "real_use_case"],
            "Translate course titles, taglines, descriptions, and real_use_case fields."
        )
        result.update(translated)
        print(f"  ✓ courses batch {i // 5 + 1}: {len(batch_keys)} entries")
    _write_or_print(ZH_DIR / "courses.json", result, dry_run)
    print(f"  ✓ courses.json: {len(entries)} entries written")


def translate_i18n(w: WorkspaceClient, dry_run: bool, _role_filter: str | None):
    src = json.loads((CONTENT_DIR / "i18n" / "zh.json").read_text(encoding="utf-8"))
    # Strip [ZH] placeholder suffixes from values before sending
    cleaned = {k: v.replace(" [ZH]", "").replace("[ZH]", "") for k, v in src.items()}
    print(f"[i18n/zh] Translating {len(cleaned)} UI string keys...")
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "Task: Translate all values in this UI strings dictionary from English to Simplified Chinese.\n"
        "Rules:\n"
        "- Keep all {placeholder} variables exactly as-is.\n"
        "- Keep all arrow/icon characters (→, ←, ✓, etc.) exactly as-is.\n"
        "- Button and nav labels should be concise (Chinese is more compact than English).\n\n"
        f"Input JSON:\n{json.dumps(cleaned, ensure_ascii=False, indent=2)}\n\n"
        "Return the translated JSON with the same keys."
    )
    raw = _call(w, prompt)
    raw = _strip_fences(raw)
    result = json.loads(raw)
    assert len(result) == len(src), f"Expected {len(src)} keys, got {len(result)}"
    out_path = CONTENT_DIR / "i18n" / "zh.json"
    _write_or_print(out_path, result, dry_run)
    print(f"  ✓ i18n/zh.json: {len(result)} keys written")


def translate_diagnostic_items(w: WorkspaceClient, dry_run: bool, role_filter: str | None):
    src = json.loads((CONTENT_DIR / "diagnostic_items.json").read_text(encoding="utf-8"))
    items = [i for i in src if not role_filter or i.get("role_id") == role_filter]
    print(f"[diagnostic_items] Translating {len(items)} items in batches of 5...")
    result = list(src)
    # Build a mapping from item_id to index in result for easy update
    id_to_idx = {item["item_id"]: idx for idx, item in enumerate(result)}
    for i in range(0, len(items), 5):
        batch = items[i:i + 5]
        translated = _translate_batch(
            w, batch,
            ["question_text", "scenario_text", "options[].text", "criteria[].name", "criteria[].description"],
            "Translate diagnostic question text, scenario text, MCQ option text, and rubric criterion names/descriptions. Keep item_id, role_id, domain_id, item_type, correct_option, display_order, and all numeric scoring values unchanged."
        )
        for t_item in translated:
            idx = id_to_idx.get(t_item["item_id"])
            if idx is not None:
                result[idx] = t_item
        print(f"  ✓ diagnostic_items batch {i // 5 + 1}: {len(batch)} items")
    _write_or_print(ZH_DIR / "diagnostic_items.json", result, dry_run)
    print(f"  ✓ diagnostic_items.json: {len(items)} items written")


def translate_reading_content(w: WorkspaceClient, dry_run: bool, role_filter: str | None):
    src = json.loads((CONTENT_DIR / "reading_content.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or k.startswith(role_filter + "_")}
    print(f"[reading_content] Translating {len(entries)} entries in batches of 3...")
    keys = list(entries.keys())
    result = dict(src)
    for i in range(0, len(keys), 3):
        batch_keys = keys[i:i + 3]
        batch = {k: entries[k] for k in batch_keys}
        translated = _translate_batch(
            w, batch,
            ["concept_text", "good_example", "anti_pattern", "takeaway"],
            "Translate reading content fields: concept_text, good_example, anti_pattern, takeaway."
        )
        result.update(translated)
        print(f"  ✓ reading_content batch {i // 3 + 1}: {len(batch_keys)} entries")
    _write_or_print(ZH_DIR / "reading_content.json", result, dry_run)
    print(f"  ✓ reading_content.json: {len(entries)} entries written")


def translate_evaluation_items(w: WorkspaceClient, dry_run: bool, role_filter: str | None):
    src = json.loads((CONTENT_DIR / "evaluation_items.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or k.startswith(role_filter + "_")}
    print(f"[evaluation_items] Translating {len(entries)} entries in batches of 3...")
    keys = list(entries.keys())
    result = dict(src)
    for i in range(0, len(keys), 3):
        batch_keys = keys[i:i + 3]
        batch = {k: entries[k] for k in batch_keys}
        translated = _translate_batch(
            w, batch,
            ["scenario_text", "question_text", "options[].label", "criteria[].name", "criteria[].description"],
            "Translate evaluation scenario text, question text, MCQ option labels, and rubric criterion names/descriptions. Keep item_id, item_type, correct_option, and all numeric scoring values unchanged."
        )
        result.update(translated)
        print(f"  ✓ evaluation_items batch {i // 3 + 1}: {len(batch_keys)} entries")
    _write_or_print(ZH_DIR / "evaluation_items.json", result, dry_run)
    print(f"  ✓ evaluation_items.json: {len(entries)} entries written")


def translate_practice_scenarios(w: WorkspaceClient, dry_run: bool, role_filter: str | None):
    src = json.loads((CONTENT_DIR / "practice_scenarios.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or k.startswith(role_filter + "_")}
    print(f"[practice_scenarios] Translating {len(entries)} entries in batches of 2...")
    keys = list(entries.keys())
    result = dict(src)
    for i in range(0, len(keys), 2):
        batch_keys = keys[i:i + 2]
        batch = {k: entries[k] for k in batch_keys}
        translated = _translate_batch(
            w, batch,
            ["scenario_text", "task_1_text", "task_2_text", "task_3_text", "task_4_text",
             "coach_system_prompt", "task_mcq_options[].label"],
            "Translate scenario text, task texts, coach system prompt, and MCQ option labels. Keep course_id, task_modes, and all structural fields unchanged."
        )
        result.update(translated)
        print(f"  ✓ practice_scenarios batch {i // 2 + 1}: {len(batch_keys)} entries")
    _write_or_print(ZH_DIR / "practice_scenarios.json", result, dry_run)
    print(f"  ✓ practice_scenarios.json: {len(entries)} entries written")


# ---------------------------------------------------------------------------
# Output helper
# ---------------------------------------------------------------------------

def _write_or_print(path: Path, data, dry_run: bool):
    if dry_run:
        print(f"\n--- DRY RUN: {path} ---")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
        print("...")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# File registry
# ---------------------------------------------------------------------------

FILE_MAP = {
    "roles": translate_roles,
    "domains": translate_domains,
    "courses": translate_courses,
    "i18n": translate_i18n,
    "diagnostic_items": translate_diagnostic_items,
    "reading_content": translate_reading_content,
    "evaluation_items": translate_evaluation_items,
    "practice_scenarios": translate_practice_scenarios,
}

FILE_ORDER = ["roles", "domains", "courses", "i18n", "diagnostic_items",
              "reading_content", "evaluation_items", "practice_scenarios"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Translate content files to Simplified Chinese")
    parser.add_argument("--file", choices=list(FILE_MAP.keys()), help="Translate only this file")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout, do not write")
    parser.add_argument("--role", help="Filter to one role (e.g. rm, uw, an, mk)")
    args = parser.parse_args()

    w = WorkspaceClient()
    files_to_run = [args.file] if args.file else FILE_ORDER

    for name in files_to_run:
        fn = FILE_MAP[name]
        try:
            fn(w, args.dry_run, args.role)
        except Exception as e:
            print(f"  [ERROR] {name}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            print(f"  Continuing with next file...")

    print("\nDone.")


if __name__ == "__main__":
    main()
