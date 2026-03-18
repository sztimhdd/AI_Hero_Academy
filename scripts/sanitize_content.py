"""
sanitize_content.py - Remove EDC-specific branding from all content JSON files.

Usage:
  python scripts/sanitize_content.py --dry-run        # Audit only, no writes (Phase 0)
  python scripts/sanitize_content.py --apply           # Apply replacement dictionary (Phase 1)
  python scripts/sanitize_content.py --apply --llm     # Apply replacements + LLM rewrite (Phase 2)
  python scripts/sanitize_content.py --validate-only   # Structural validation CI gate (Phase 3)
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

TARGET_FILES = [
    "roles.json",
    "courses.json",
    "diagnostic_items.json",
    "evaluation_items.json",
    "practice_scenarios.json",
    "reading_content.json",
    "reading_content_structured.json",
]

# Fields in reading_content_structured.json that may hold nested JSON objects
# or JSON-serialised strings requiring recursive substitution
STRUCTURED_FIELDS = {
    "concept_text_structured",
    "good_example_structured",
    "anti_pattern_structured",
    "takeaway_structured",
}

# ---------------------------------------------------------------------------
# Replacement dictionary - applied in priority order (longest match first)
# ---------------------------------------------------------------------------
REPLACEMENT_DICT: list[tuple[str, str]] = [
    ("EDC's Responsible AI policy",          "your organization's AI use policy"),
    ("EDC-approved AI tool",                 "your organization's approved AI tool"),
    ("non-public EDC information",           "non-public organizational data"),
    ("Impact team (FinDev Canada)",          "the development finance team"),
    ("Meridian Infrastructure Briefing",     "Meridian Infrastructure Programme"),
    ("Company Information Management team",  "the client data management team"),
    ("CIS buyer-file note",                  "client file note"),
    ("FinDev Canada",                        "the development finance division"),
    ("EDC-approved",                         "organization-approved"),
    ("within EDC's",                         "within the organization's"),
    ("EDC tenant",                           "organization's tenant"),
    ("EDC data",                             "organizational data"),
    ("at EDC",                               "at Apex Trade Finance"),
    ("EDC's",                                "Apex Trade Finance's"),
    ("the EDC",                              "Apex Trade Finance"),
    ("EDC",                                  "Apex Trade Finance"),   # word-boundary applied below
]

# Patterns compiled once - highest-priority entries first, word-boundary on bare EDC
_COMPILED_PATTERNS: list[tuple[re.Pattern, str]] = []
for _original, _replacement in REPLACEMENT_DICT:
    if _original == "EDC":
        _pattern = re.compile(r"\bEDC\b", re.IGNORECASE)
    else:
        _pattern = re.compile(re.escape(_original), re.IGNORECASE)
    _COMPILED_PATTERNS.append((_pattern, _replacement))


# ---------------------------------------------------------------------------
# EDC detection regex (for audit / validation)
# ---------------------------------------------------------------------------
EDC_DETECT = re.compile(r"\bEDC\b", re.IGNORECASE)


def _safe_ascii(text: str) -> str:
    """Return text with non-ASCII chars replaced by '?' for safe terminal output."""
    return text.encode("ascii", errors="replace").decode("ascii")


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------
def load_content_files() -> dict[str, Any]:
    """Return {filename: parsed_json} for every target file."""
    data: dict[str, Any] = {}
    for fname in TARGET_FILES:
        path = CONTENT_DIR / fname
        with open(path, encoding="utf-8") as fh:
            data[fname] = json.load(fh)
    return data


def write_content_files(data: dict[str, Any]) -> None:
    """Write each file back to disk, then verify it re-parses cleanly."""
    for fname, content in data.items():
        path = CONTENT_DIR / fname
        serialized = json.dumps(content, indent=2, ensure_ascii=False)
        path.write_text(serialized, encoding="utf-8")
        try:
            json.loads(serialized)
        except json.JSONDecodeError as exc:
            print(f"CRITICAL: {fname} failed JSON validation after write: {exc}", file=sys.stderr)
            sys.exit(1)
        print(f"  wrote {fname}")


# ---------------------------------------------------------------------------
# ID snapshot
# ---------------------------------------------------------------------------
def snapshot_ids(data: dict[str, Any]) -> dict[str, set]:
    """Capture top-level keys (IDs) from every file for stability check."""
    return {fname: set(content.keys()) for fname, content in data.items()}


# ---------------------------------------------------------------------------
# String substitution
# ---------------------------------------------------------------------------
def _apply_replacements_to_string(text: str, log_entry: dict | None = None) -> str:
    """Apply all replacement patterns to a single string, in priority order."""
    for pattern, replacement in _COMPILED_PATTERNS:
        new_text = pattern.sub(replacement, text)
        if new_text != text and log_entry is not None:
            log_entry["changes"].append({
                "pattern": pattern.pattern,
                "before_snippet": _safe_ascii(text[:80]),
                "after_snippet":  _safe_ascii(new_text[:80]),
            })
        text = new_text
    return text


def _walk_and_apply(obj: Any, path: str, log: list, count: list) -> Any:
    """
    Recursively walk obj.  For every string leaf, apply the replacement dict.
    Returns a new object (no mutation of the original).
    """
    if isinstance(obj, str):
        entry: dict = {"path": path, "changes": []}
        new_val = _apply_replacements_to_string(obj, log_entry=entry)
        if new_val != obj:
            count[0] += len(entry["changes"])
            log.append(entry)
        return new_val

    if isinstance(obj, dict):
        return {k: _walk_and_apply(v, f"{path}.{k}", log, count) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_walk_and_apply(item, f"{path}[{i}]", log, count) for i, item in enumerate(obj)]

    return obj  # int, float, bool, None - unchanged


def apply_replacement_dict(data: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """
    Apply the replacement dictionary to all target files.
    Returns (mutated_data, total_substitution_count).
    """
    total = 0
    mutated: dict[str, Any] = {}
    for fname, content in data.items():
        log: list = []
        count = [0]
        mutated_content = _walk_and_apply(content, fname, log, count)
        mutated[fname] = mutated_content
        if log:
            print(f"\n  [{fname}] - {count[0]} substitutions")
            for entry in log:
                for change in entry["changes"]:
                    before = entry["before_snippet"][:60]
                    after  = change["after_snippet"][:60]
                    print(f"    {entry['path']}: {before!r} -> {after!r}")
        total += count[0]
    return mutated, total


# ---------------------------------------------------------------------------
# EDC audit
# ---------------------------------------------------------------------------
def _count_edc_in_string(text: str) -> int:
    return len(EDC_DETECT.findall(text))


def _walk_and_count(obj: Any, path: str, hits: list) -> None:
    """Walk obj recursively, recording every string that contains EDC."""
    if isinstance(obj, str):
        n = _count_edc_in_string(obj)
        if n:
            hits.append((path, n, obj[:80]))
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            _walk_and_count(v, f"{path}.{k}", hits)
        return
    if isinstance(obj, list):
        for i, item in enumerate(obj):
            _walk_and_count(item, f"{path}[{i}]", hits)


def audit_edc_occurrences(data: dict[str, Any]) -> dict[str, list]:
    """Return {filename: [(field_path, count, snippet), ...]} for all EDC hits."""
    result: dict[str, list] = {}
    for fname, content in data.items():
        hits: list = []
        _walk_and_count(content, fname, hits)
        result[fname] = hits
    return result


def print_audit_report(hits: dict[str, list]) -> int:
    """Print the audit report table. Returns total count."""
    total = 0
    for fname, file_hits in hits.items():
        file_count = sum(h[1] for h in file_hits)
        if file_count:
            print(f"\n  {fname} - {file_count} occurrences")
            for path, n, snippet in file_hits:
                print(f"    {path} ({n}x): {_safe_ascii(snippet)!r}")
        total += file_count
    return total


# ---------------------------------------------------------------------------
# LLM rewrite
# ---------------------------------------------------------------------------
LLM_SYSTEM_PROMPT = (
    'You are rewriting training content for a generic financial services organization\n'
    'called "Apex Trade Finance". Rewrite the following passage so that:\n'
    '- All references to "EDC", its policies, programmes, and internal systems are\n'
    '  replaced with generic equivalents referencing "Apex Trade Finance".\n'
    '- Do NOT change fictional client company names (Crestwood, Bluewave, Westport,\n'
    '  Meridian Trade Finance Bank, Northern Fabrication, Maple Industries, Vantara Foods,\n'
    '  Irongate Civil).\n'
    '- Do NOT change Microsoft product names (M365, Copilot, Teams, SharePoint).\n'
    '- Do NOT change the SAFE Abstraction Method name.\n'
    '- Do NOT change the meaning, scenario structure, difficulty, or answer keys.\n'
    '- Return ONLY the rewritten text, no commentary.\n'
)


def _call_llm(passage: str) -> str:
    """Call Gemini 2.0 Flash to rewrite a passage via utils/ai.py."""
    sys.path.insert(0, str(ROOT))
    try:
        from utils.ai import call_llm as _api_call  # type: ignore
        response = _api_call(
            messages=[
                {"role": "system", "content": LLM_SYSTEM_PROMPT},
                {"role": "user",   "content": f"Original:\n{passage}"},
            ],
            temperature=0.1,
            call_type="sanitize_rewrite",
        )
        return response.strip()
    except Exception as exc:
        print(f"    LLM call failed: {exc}", file=sys.stderr)
        return passage  # leave unchanged on failure


def _walk_and_rewrite(obj: Any, path: str, log: list) -> Any:
    """Walk obj; for any string still containing EDC, send to LLM."""
    if isinstance(obj, str):
        if EDC_DETECT.search(obj):
            print(f"    LLM rewriting: {path}")
            rewritten = _call_llm(obj)
            log.append({
                "path": path,
                "original_snippet":  _safe_ascii(obj[:80]),
                "rewritten_snippet": _safe_ascii(rewritten[:80]),
            })
            return rewritten
        return obj
    if isinstance(obj, dict):
        return {k: _walk_and_rewrite(v, f"{path}.{k}", log) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_and_rewrite(item, f"{path}[{i}]", log) for i, item in enumerate(obj)]
    return obj


def rewrite_residuals_with_llm(data: dict[str, Any]) -> dict[str, Any]:
    """Send any string still containing EDC through Gemini for rewriting."""
    mutated: dict[str, Any] = {}
    for fname, content in data.items():
        log: list = []
        new_content = _walk_and_rewrite(content, fname, log)
        mutated[fname] = new_content
        if log:
            print(f"\n  [{fname}] - {len(log)} LLM rewrites")
            for entry in log:
                print(f"    {entry['path']}: {entry['original_snippet']!r} -> {entry['rewritten_snippet']!r}")
    return mutated


# ---------------------------------------------------------------------------
# Structural validation
# ---------------------------------------------------------------------------
def validate_structure(data_before: dict[str, Any] | None, data_after: dict[str, Any]) -> bool:
    """
    Run all structural checks.  Returns True if all pass, False otherwise.
    Prints details on any failure.
    """
    ok = True

    # --- 1. EDC residual check ---
    hits = audit_edc_occurrences(data_after)
    total_edc = sum(sum(h[1] for h in v) for v in hits.values())
    if total_edc == 0:
        print("  [OK] 0 EDC occurrences found")
    else:
        print(f"  [FAIL] {total_edc} EDC occurrences remain:")
        print_audit_report(hits)
        ok = False

    # --- 2. JSON validity (double-check on-disk files after writes) ---
    for fname in TARGET_FILES:
        path = CONTENT_DIR / fname
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
                print(f"  [OK] {fname} - valid JSON")
            except json.JSONDecodeError as exc:
                print(f"  [FAIL] {fname} - JSON parse error: {exc}")
                ok = False

    # --- 3. Field completeness ---
    courses = data_after.get("courses.json", {})
    for course_id, course in courses.items():
        for field in ("tagline", "description"):
            if not course.get(field):
                print(f"  [FAIL] courses.json: {course_id}.{field} is empty")
                ok = False

    scenarios = data_after.get("practice_scenarios.json", {})
    for sid, scenario in scenarios.items():
        if not scenario.get("scenario_text"):
            print(f"  [FAIL] practice_scenarios.json: {sid}.scenario_text is empty")
            ok = False

    for fname in ("diagnostic_items.json", "evaluation_items.json"):
        items = data_after.get(fname, {})
        for iid, item in items.items():
            if not item.get("question_text"):
                print(f"  [FAIL] {fname}: {iid}.question_text is empty")
                ok = False

    if ok:
        print("  [OK] All required fields are non-empty")

    # --- 4. ID stability ---
    if data_before is not None:
        ids_before = snapshot_ids(data_before)
        ids_after  = snapshot_ids(data_after)
        for fname in TARGET_FILES:
            before_set = ids_before.get(fname, set())
            after_set  = ids_after.get(fname, set())
            added   = after_set - before_set
            removed = before_set - after_set
            if added or removed:
                print(f"  [FAIL] {fname}: ID mismatch - added={added} removed={removed}")
                ok = False
        if ok:
            print("  [OK] All IDs stable")

    # --- 5. Nested JSON integrity for reading_content_structured.json ---
    structured = data_after.get("reading_content_structured.json", {})
    struct_errors = 0
    for course_id, entry in structured.items():
        for field in STRUCTURED_FIELDS:
            val = entry.get(field)
            if val is None:
                continue
            if isinstance(val, str):
                try:
                    json.loads(val)
                except json.JSONDecodeError as exc:
                    print(f"  [FAIL] reading_content_structured.json: {course_id}.{field} invalid JSON string: {exc}")
                    ok = False
                    struct_errors += 1
    if struct_errors == 0:
        print("  [OK] reading_content_structured.json nested integrity OK")

    return ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Sanitize EDC references from content JSON files")
    parser.add_argument("--dry-run",       action="store_true", help="Audit only, no writes")
    parser.add_argument("--apply",         action="store_true", help="Apply replacement dictionary")
    parser.add_argument("--llm",           action="store_true", help="Also run LLM rewrite on residuals (requires --apply)")
    parser.add_argument("--validate-only", action="store_true", help="Structural validation CI gate")
    args = parser.parse_args()

    if not any([args.dry_run, args.apply, args.validate_only]):
        parser.print_help()
        sys.exit(1)

    if args.llm and not args.apply:
        print("Error: --llm requires --apply", file=sys.stderr)
        sys.exit(1)

    print("Loading content files...")
    data = load_content_files()
    data_before = copy.deepcopy(data)

    # -----------------------------------------------------------------------
    # --dry-run
    # -----------------------------------------------------------------------
    if args.dry_run:
        print("\n=== DRY-RUN AUDIT ===")
        hits = audit_edc_occurrences(data)
        total = print_audit_report(hits)
        print(f"\nTotal EDC occurrences: {total}")
        if total > 0:
            sys.exit(1)
        sys.exit(0)

    # -----------------------------------------------------------------------
    # --validate-only
    # -----------------------------------------------------------------------
    if args.validate_only:
        print("\n=== STRUCTURAL VALIDATION ===")
        clean = validate_structure(None, data)
        sys.exit(0 if clean else 1)

    # -----------------------------------------------------------------------
    # --apply [--llm]
    # -----------------------------------------------------------------------
    if args.apply:
        print("\n=== APPLYING REPLACEMENT DICTIONARY ===")
        data, sub_count = apply_replacement_dict(data)
        print(f"\nTotal substitutions made: {sub_count}")

        if args.llm:
            print("\n=== LLM REWRITE FOR RESIDUALS ===")
            hits = audit_edc_occurrences(data)
            residual_count = sum(sum(h[1] for h in v) for v in hits.values())
            if residual_count == 0:
                print("  No residuals found - LLM rewrite skipped.")
            else:
                print(f"  {residual_count} residual EDC occurrences - sending to Gemini...")
                data = rewrite_residuals_with_llm(data)

        print("\nWriting files...")
        write_content_files(data)

        print("\n=== POST-APPLY VALIDATION ===")
        hits = audit_edc_occurrences(data)
        remaining = sum(sum(h[1] for h in v) for v in hits.values())
        if remaining == 0:
            print("  [OK] 0 EDC occurrences found after apply")
        else:
            print(f"  [FAIL] {remaining} EDC occurrences remain - run --validate-only to see details")

        sys.exit(0)


if __name__ == "__main__":
    main()
