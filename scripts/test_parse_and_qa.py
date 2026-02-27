#!/usr/bin/env python3
"""
Quick test: Stage 1 (parse_brief) + Stage 3 (qa_gap_check) only.

Usage:
    python scripts/test_parse_and_qa.py <brief_filepath>

Runs only parsing and QA gap check — no content generation, no file writes.
Use this to validate a Course Design Brief before committing to a full pipeline run.
"""
import argparse
import io
import json
import sys
from pathlib import Path

# Add parent dir to path so we can import from generate_course_content
sys.path.insert(0, str(Path(__file__).parent))

from generate_course_content import (
    parse_brief,
    qa_gap_check,
    generate_followup_prompt,
)


def main() -> None:
    # Ensure UTF-8 output on Windows
    if hasattr(sys.stdout, "buffer") and getattr(sys.stdout, "encoding", "utf-8").lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    cli = argparse.ArgumentParser(
        description="Test Stage 1 + Stage 3 of the content generation pipeline (no writes)."
    )
    cli.add_argument("brief_filepath", help="Path to the Course Design Brief markdown file")
    cli.add_argument(
        "--skip-llm-quality-check",
        action="store_true",
        help="Skip the Sonnet LLM quality check in Stage 3 (structural checks only)",
    )
    args = cli.parse_args()

    brief_path = args.brief_filepath

    print()
    print("=" * 60)
    print("Stage 1 + Stage 3 Test Runner")
    print("=" * 60)
    print(f"  Brief: {brief_path}")
    print()

    # ── Stage 1: Parse brief ──────────────────────────────────────────────
    print("[Stage 1] Parsing brief...")
    spec = parse_brief(brief_path)

    print()
    print("  Extracted spec fields:")
    print(f"    role_prefix        : {spec.get('role_prefix')}")
    print(f"    role_display_name  : {spec.get('role_display_name')}")
    company_map = spec.get("company_map") or {}
    print(f"    company_map        : {company_map}")
    real_use_cases = spec.get("real_use_cases") or {}
    print(f"    real_use_cases     : {len(real_use_cases)} courses found ({list(real_use_cases.keys())})")
    framework_names = spec.get("framework_names") or []
    print(f"    framework_names    : {framework_names}")
    domain_seeds = spec.get("domain_seeds") or {}
    print(f"    domain_seeds       : {list(domain_seeds.keys())} found")
    course_seeds = spec.get("course_seeds") or {}
    print(f"    course_seeds       : {list(course_seeds.keys())} found")
    scenario_seeds = spec.get("scenario_seeds") or {}
    print(f"    scenario_seeds     : {list(scenario_seeds.keys())} found")
    reading_seeds = spec.get("reading_seeds") or {}
    print(f"    reading_seeds      : {list(reading_seeds.keys())} found")
    diag_seeds = spec.get("diagnostic_seeds") or {}
    print(f"    diagnostic_seeds   : {list(diag_seeds.keys())} domains found")
    eval_seeds = spec.get("evaluation_seeds") or {}
    print(f"    evaluation_seeds   : {list(eval_seeds.keys())} courses found")
    print()

    # ── Stage 3: QA gap check ─────────────────────────────────────────────
    if args.skip_llm_quality_check:
        print("[Stage 3] Running structural QA checks only (--skip-llm-quality-check)...")
        # Monkey-patch _llm_quality_check to skip the Sonnet call
        import generate_course_content as _mod
        _mod._llm_quality_check = lambda spec: []

    print("[Stage 3] Running QA gap check...")
    passed, flags = qa_gap_check(spec, {})

    if passed:
        print("  ✓ QA gap check PASSED — brief is complete and meets quality standards")
        print()
        print("  This brief is ready for a full pipeline run:")
        print(f"    python scripts/generate_course_content.py {brief_path}")
    else:
        followup = generate_followup_prompt(flags, brief_path)
        print(followup)

    print()


if __name__ == "__main__":
    main()
