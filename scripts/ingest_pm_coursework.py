#!/usr/bin/env python3
"""
scripts/ingest_pm_coursework.py

Parses references/PM-coursework-design.md and appends PM content to:
  content/courses.json
  content/reading_content.json
  content/practice_scenarios.json
  content/evaluation_items.json
  content/diagnostic_items.json
  content/atomic_modules.json

No LLM calls — pure string/regex parsing.

Usage:
  python scripts/ingest_pm_coursework.py --dry-run   # print to stdout only
  python scripts/ingest_pm_coursework.py             # write files
"""

import json
import re
import argparse
import sys
from pathlib import Path

# Force UTF-8 on Windows stdout for dry-run output
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "references" / "PM-coursework-design.md"
CONTENT = ROOT / "content"
TODAY = "2026-03-20"

# ── Sanitization ──────────────────────────────────────────────────────────────

SUBS = [
    ("EDC's Gen AI policy", "the organization's Gen AI policy"),
    ("EDC's Initiative Lifecycle Framework", "the organization's project governance framework"),
    ("EDC Project and Program Managers", "Project and Program Managers"),
    ("EDC Project Manager", "Project Manager"),
    ("EDC project", "internal project"),
    ("EDC policy", "organizational policy"),
    ("EDC", "the organization"),
    ("Planview", "the project management system"),
    ("M365", "Microsoft 365"),
]
URL_RE = re.compile(r"\]\(https?://[^\)]+\)")


def sanitize(text: str) -> str:
    if not text:
        return text
    for find, replace in SUBS:
        text = text.replace(find, replace)
    text = URL_RE.sub("", text)
    # Clean up orphaned closing brackets left by URL removal
    text = re.sub(r"\]\s*$", "", text)
    return text.strip()


# ── Atomization templates ─────────────────────────────────────────────────────

PROG_NAMES = [
    "Atlas Delivery Renewal",
    "NorthBridge CRM Release 2",
    "Summit Portfolio Review",
    "Horizon Service Transition",
    "Beacon Capacity Dashboard",
    "Maple Program SteerCo",
    "Polaris Transformation Wave",
]


def templatize_scenario(text: str) -> str:
    for name in PROG_NAMES:
        text = text.replace(name, "{programme_name}")
    return text


def templatize_coach(text: str) -> str:
    text = text.replace("Project and Program Managers", "{role}")
    text = text.replace("Project Manager", "{role}")
    text = re.sub(r"\binternal (program|initiative)\b", "{org_type}", text)
    return text


# ── Parsing helpers ───────────────────────────────────────────────────────────


def extract_kv(line: str) -> tuple:
    """Extract (key, value) from 'key: value' line, or (None, None)."""
    m = re.match(r"^([A-Za-z][A-Za-z0-9 _]*?):\s*(.*)", line.rstrip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, None


def find_section_starts(lines: list) -> dict:
    """Return dict mapping section_name -> line_index."""
    secs = {}
    for i, line in enumerate(lines):
        for s in ("SECTION C", "SECTION D", "SECTION E", "SECTION F", "SECTION G"):
            if line.strip().startswith(s):
                secs[s] = i
    return secs


# ── Section C: courses ────────────────────────────────────────────────────────


def parse_section_c(lines: list) -> list:
    """Parse 7 PM course specs."""
    courses = []
    cur = {}

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if re.match(r"^Course \d+ —", stripped):
            if cur.get("course_id"):
                courses.append(cur)
            cur = {}
            continue

        k, v = extract_kv(line)
        if not k:
            continue
        if k == "sequence_order":
            cur[k] = int(v) if v.isdigit() else v
        elif k in ("course_id", "role_id", "primary_domain", "title", "tagline", "description", "real_use_case"):
            cur[k] = sanitize(v)

    if cur.get("course_id"):
        courses.append(cur)
    return courses


# ── Section D: practice scenarios ────────────────────────────────────────────


def parse_section_d(lines: list) -> list:
    """Parse 7 PM practice scenarios."""
    scenarios = []
    cur = {}

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if re.match(r"^Course \d+ Scenario$", stripped):
            if cur.get("scenario_text"):
                scenarios.append(cur)
            cur = {}
            continue

        k, v = extract_kv(line)
        if not k:
            continue
        if k in (
            "scenario_text",
            "task_1_text",
            "task_2_text",
            "task_3_text",
            "task_4_text",
            "coach_system_prompt",
            "role_variants_hint",
        ):
            cur[k] = sanitize(v)

    if cur.get("scenario_text"):
        scenarios.append(cur)
    return scenarios


# ── Section E: reading content ────────────────────────────────────────────────


def parse_section_e(lines: list) -> list:
    """Parse 7 PM reading specs."""
    readings = []
    cur = {}

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if re.match(r"^Course \d+ Reading$", stripped):
            if cur.get("concept_text"):
                readings.append(cur)
            cur = {}
            continue

        k, v = extract_kv(line)
        if not k:
            continue
        if k in ("framework_name", "concept_text", "good_example", "anti_pattern", "takeaway"):
            cur[k] = sanitize(v)

    if cur.get("concept_text"):
        readings.append(cur)
    return readings


# ── Section F: diagnostic items ───────────────────────────────────────────────


def parse_section_f(lines: list) -> list:
    """Parse 18 PM diagnostic items (3 per domain × 6 domains)."""
    items = []
    cur = {}
    domain = None
    options = []
    rubric_lines = []
    in_options = False
    in_rubric = False
    item_counters = {}
    global_order = [0]  # mutable counter for display_order

    def finalize():
        if not cur.get("question_text"):
            return
        entry = dict(cur)
        if options:
            entry["options"] = [{"label": o[0], "text": o[3:].strip()} for o in options]
        else:
            entry["options"] = None
        if rubric_lines:
            entry["scoring_rubric"] = {
                "criteria": [
                    {"name": f"Criterion {i+1}", "description": sanitize(c), "max": 1}
                    for i, c in enumerate(rubric_lines)
                ]
            }
        else:
            entry["scoring_rubric"] = None
        if entry.get("item_type") == "mcq":
            entry["scoring_rubric"] = None
        items.append(entry)

    for line in lines:
        stripped = line.strip()

        # Domain header — always reset state
        m = re.match(r"^Diagnostic:\s+(\w+)", stripped)
        if m:
            finalize()
            cur = {}
            options = []
            rubric_lines = []
            in_options = False
            in_rubric = False
            domain = m.group(1)
            item_counters[domain] = 0
            continue

        # Item header — reset state and start new item
        m = re.match(r"^Item \d+ — type:\s+(\w+)", stripped)
        if m:
            finalize()
            cur = {}
            options = []
            rubric_lines = []
            in_options = False
            in_rubric = False
            if domain:
                item_counters[domain] = item_counters.get(domain, 0) + 1
                n = item_counters[domain]
                global_order[0] += 1
                cur = {
                    "item_id": f"pm_{domain}_{n}",
                    "domain_id": domain,
                    "item_type": m.group(1),
                    "display_order": global_order[0],
                    "role_id": "pm",
                    "question_text": None,
                    "scenario_text": None,
                    "correct_option": None,
                }
            continue

        if not cur:
            continue

        # Options header
        if stripped == "options:":
            in_options = True
            in_rubric = False
            options = []
            continue

        # Rubric header
        if stripped.startswith("scoring rubric criteria:"):
            in_rubric = True
            in_options = False
            rubric_lines = []
            continue

        # Collect options
        if in_options:
            m = re.match(r"^([A-D])\)\s+(.+)", stripped)
            if m:
                options.append(f"{m.group(1)}) {sanitize(m.group(2))}")
                continue
            else:
                in_options = False
                # fall through to KV parsing

        # Collect rubric criteria
        if in_rubric:
            if stripped:
                rubric_lines.append(stripped)
            continue

        # KV parsing
        k, v = extract_kv(line)
        if k in ("question_text", "scenario_text", "correct_option"):
            cur[k] = sanitize(v)

    finalize()
    return items


# ── Section G: evaluation items ───────────────────────────────────────────────


def parse_section_g(lines: list, courses: list) -> dict:
    """Parse 28 PM evaluation items (4 per course × 7 courses)."""
    course_map = {c["sequence_order"]: c["course_id"] for c in courses}
    result = {}
    cur = {}
    course_id = None
    options = []
    rubric_kv = {}
    in_options = False
    in_rubric = False

    def finalize():
        if not cur.get("question_text") or not course_id:
            return
        entry = dict(cur)
        if options:
            entry["options"] = [{"label": o[0], "text": o[3:].strip()} for o in options]
        else:
            entry["options"] = None
        if rubric_kv:
            entry["scoring_rubric"] = dict(rubric_kv)
        else:
            entry["scoring_rubric"] = None
        result.setdefault(course_id, []).append(entry)

    for line in lines:
        stripped = line.strip()

        # Course header
        m = re.match(r"^Evaluation: Course (\d+)", stripped)
        if m:
            finalize()
            cur = {}
            options = []
            rubric_kv = {}
            in_options = False
            in_rubric = False
            n = int(m.group(1))
            course_id = course_map.get(n)
            continue

        # Item header
        m = re.match(r"^Item \d+ — type:\s+(\w+),\s*sequence:\s*(\d+)", stripped)
        if m:
            finalize()
            cur = {}
            options = []
            rubric_kv = {}
            in_options = False
            in_rubric = False
            if course_id:
                item_type = m.group(1)
                seq = int(m.group(2))
                cur = {
                    "item_id": f"ev_{course_id}_q{seq}",
                    "course_id": course_id,
                    "item_type": item_type,
                    "sequence": seq,
                    "question_text": None,
                    "scenario_text": None,
                    "correct_option": None,
                    "explanation": None,
                    "scoring_rubric": None,
                }
            continue

        if not cur:
            continue

        # Options header
        if stripped == "options:":
            in_options = True
            in_rubric = False
            options = []
            continue

        # Scoring rubric header (Section G uses key1-key4 format)
        if stripped == "scoring rubric:":
            in_rubric = True
            in_options = False
            rubric_kv = {}
            continue

        # Collect options
        if in_options:
            m = re.match(r"^([A-D])\)\s+(.+)", stripped)
            if m:
                options.append(f"{m.group(1)}) {sanitize(m.group(2))}")
                continue
            else:
                in_options = False
                # fall through to KV parsing

        # Collect rubric key-value pairs (key1: ..., key2: ..., etc.)
        if in_rubric:
            m = re.match(r"^(key\d+):\s+(.*)", stripped)
            if m:
                rubric_kv[m.group(1)] = sanitize(m.group(2))
                continue
            elif stripped:
                in_rubric = False
                # fall through
            else:
                continue  # blank line in rubric — skip

        # KV parsing
        k, v = extract_kv(line)
        if k in ("question_text", "scenario_text", "correct_option", "explanation"):
            cur[k] = sanitize(v)

    finalize()
    return result


# ── Capability tags ───────────────────────────────────────────────────────────


def parse_capability_tags(lines: list) -> dict:
    """Parse capability_tags from header into {course_1: [...], ...}."""
    for line in lines:
        if line.startswith("capability_tags:"):
            rest = line[len("capability_tags:"):].strip()
            parts = re.split(r"\s{2,}(course_\d+):\s*", rest)
            # parts: ['prefix', 'course_1', 'tags1 ...', 'course_2', 'tags2 ...', ...]
            result = {}
            i = 1
            while i < len(parts) - 1:
                key = parts[i]
                tags_str = parts[i + 1].strip()
                tags = [t.strip() for t in tags_str.split(",") if t.strip()]
                result[key] = tags
                i += 2
            return result
    return {}


# ── Output builders ───────────────────────────────────────────────────────────


def build_courses(courses: list) -> dict:
    return {c["course_id"]: c for c in courses}


def build_reading_content(courses: list, readings: list) -> dict:
    result = {}
    for course, reading in zip(courses, readings):
        cid = course["course_id"]
        result[cid] = {
            "content_id": cid,
            "course_id": cid,
            "concept_text": reading.get("concept_text", ""),
            "good_example": reading.get("good_example", ""),
            "anti_pattern": reading.get("anti_pattern", ""),
            "takeaway": reading.get("takeaway", ""),
        }
    return result


def build_practice_scenarios(courses: list, scenarios: list) -> dict:
    result = {}
    for course, scenario in zip(courses, scenarios):
        cid = course["course_id"]
        result[cid] = {
            "scenario_id": cid,
            "course_id": cid,
            "scenario_text": scenario.get("scenario_text", ""),
            "task_1_text": scenario.get("task_1_text", ""),
            "task_2_text": scenario.get("task_2_text", ""),
            "task_3_text": scenario.get("task_3_text", ""),
            "task_4_text": scenario.get("task_4_text", ""),
            "coach_system_prompt": scenario.get("coach_system_prompt", ""),
            "task_modes": ["open", "open", "open", "open"],
            "task_mcq_options": [None, None, None, None],
        }
    return result


def build_atomic_modules(courses: list, readings: list, scenarios: list, cap_tags: dict) -> list:
    atoms = []
    for i, (course, reading, scenario) in enumerate(zip(courses, readings, scenarios)):
        cid = course["course_id"]
        domain = course["primary_domain"]
        atom_id = f"{domain}__{cid}"
        course_key = f"course_{i + 1}"
        tags = cap_tags.get(course_key, [])

        task_templates = []
        for t in range(1, 5):
            task_text = scenario.get(f"task_{t}_text", "")
            task_templates.append({
                "task_id": t,
                "task_mode": "open",
                "text_template": templatize_scenario(task_text),
                "skill_focus": "",
                "mcq_options": None,
            })

        atoms.append({
            "atom_id": atom_id,
            "title": course["title"],
            "domain": domain,
            "capability_tags": tags,
            "estimated_minutes": 30,
            "role_variants_hint": sanitize(scenario.get("role_variants_hint", "")),
            "reading": {
                "concept_text": reading.get("concept_text", ""),
                "good_example": reading.get("good_example", ""),
                "anti_pattern": reading.get("anti_pattern", ""),
                "takeaway": reading.get("takeaway", ""),
            },
            "practice": {
                "scenario_template": templatize_scenario(scenario.get("scenario_text", "")),
                "task_modes": ["open", "open", "open", "open"],
                "task_templates": task_templates,
                "task_mcq_options": [None, None, None, None],
                "coach_system_prompt_template": templatize_coach(
                    scenario.get("coach_system_prompt", "")
                ),
            },
            "eval": {
                "items_ref": "evaluation_items.json",
                "source_course_ids": [cid],
            },
            "source_course_ids": [cid],
            "atomized_at": TODAY,
            "status": "draft",
        })
    return atoms


# ── JSON I/O ──────────────────────────────────────────────────────────────────


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data, dry_run: bool):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN: {path.name}  ({len(text)} bytes)")
        print(f"{'='*60}")
        print(text[:3000])
        if len(text) > 3000:
            print(f"  ... ({len(text) - 3000} more bytes) ...")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  Written: {path}")


# ── Verification ──────────────────────────────────────────────────────────────


def verify():
    print("\n--- Verification ---")
    courses = load_json(CONTENT / "courses.json")
    pm_courses = [c for c in courses.values() if c["role_id"] == "pm"]
    print(f"  Total courses: {len(courses)}  (expected 35)")
    print(f"  PM courses:    {len(pm_courses)}  (expected 7)")

    di = load_json(CONTENT / "diagnostic_items.json")
    pm_di = [x for x in di if x.get("role_id") == "pm"]
    print(f"  PM diag items: {len(pm_di)}  (expected 18)")

    ei = load_json(CONTENT / "evaluation_items.json")
    pm_ei = sum(len(v) for k, v in ei.items() if k.startswith("pm_"))
    print(f"  PM eval items: {pm_ei}  (expected 28)")

    atoms = load_json(CONTENT / "atomic_modules.json")
    pm_atoms = [a for a in atoms if "pm_" in a["atom_id"]]
    print(f"  PM atoms:      {len(pm_atoms)}  (expected 7)")

    all_text = (
        json.dumps(courses)
        + json.dumps(di)
        + json.dumps(ei)
        + json.dumps(atoms)
    )
    edc_hits = len(re.findall(r"\bEDC\b", all_text))
    print(f"  EDC hits:      {edc_hits}  (expected 0)")

    if edc_hits:
        print("\n  EDC occurrences found in:")
        for name, obj in [
            ("courses.json", courses),
            ("diagnostic_items.json", {"items": di}),
            ("evaluation_items.json", ei),
            ("atomic_modules.json", {"atoms": atoms}),
        ]:
            hits = len(re.findall(r"\bEDC\b", json.dumps(obj)))
            if hits:
                print(f"    {name}: {hits} hits")


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Ingest PM coursework design brief")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout only")
    args = parser.parse_args()

    if not SOURCE.exists():
        print(f"ERROR: Source file not found: {SOURCE}")
        return 1

    print(f"Reading: {SOURCE}")
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    secs = find_section_starts(lines)
    print(f"  Sections found: {list(secs.keys())}")

    cap_tags = parse_capability_tags(lines)
    print(f"  Capability tag groups: {len(cap_tags)}")

    # Slice sections
    sec_c = lines[secs["SECTION C"]: secs["SECTION D"]]
    sec_d = lines[secs["SECTION D"]: secs["SECTION E"]]
    sec_e = lines[secs["SECTION E"]: secs["SECTION F"]]
    sec_f = lines[secs["SECTION F"]: secs["SECTION G"]]
    sec_g = lines[secs["SECTION G"]:]

    courses = parse_section_c(sec_c)
    print(f"  Courses parsed: {len(courses)}")

    scenarios = parse_section_d(sec_d)
    print(f"  Scenarios parsed: {len(scenarios)}")

    readings = parse_section_e(sec_e)
    print(f"  Readings parsed: {len(readings)}")

    diag_items = parse_section_f(sec_f)
    print(f"  Diagnostic items parsed: {len(diag_items)}")

    eval_items = parse_section_g(sec_g, courses)
    total_eval = sum(len(v) for v in eval_items.values())
    print(f"  Evaluation items parsed: {total_eval} across {len(eval_items)} courses")

    # Validate counts before writing
    issues = []
    if len(courses) != 7:
        issues.append(f"Expected 7 courses, got {len(courses)}")
    if len(scenarios) != 7:
        issues.append(f"Expected 7 scenarios, got {len(scenarios)}")
    if len(readings) != 7:
        issues.append(f"Expected 7 readings, got {len(readings)}")
    if len(diag_items) != 18:
        issues.append(f"Expected 18 diag items, got {len(diag_items)}")
    if total_eval != 28:
        issues.append(f"Expected 28 eval items, got {total_eval}")

    if issues:
        print("\nWARNING — Count mismatches:")
        for issue in issues:
            print(f"  - {issue}")
        if not args.dry_run:
            print("Aborting write. Fix parser issues first (use --dry-run to inspect).")
            return 1

    # Build structured outputs
    new_courses = build_courses(courses)
    new_reading = build_reading_content(courses, readings)
    new_scenarios = build_practice_scenarios(courses, scenarios)
    new_atoms = build_atomic_modules(courses, readings, scenarios, cap_tags)

    # Merge with existing JSON
    existing_courses = load_json(CONTENT / "courses.json")
    existing_courses.update(new_courses)

    existing_reading = load_json(CONTENT / "reading_content.json")
    existing_reading.update(new_reading)

    existing_scenarios = load_json(CONTENT / "practice_scenarios.json")
    existing_scenarios.update(new_scenarios)

    existing_eval = load_json(CONTENT / "evaluation_items.json")
    existing_eval.update(eval_items)

    existing_diag = load_json(CONTENT / "diagnostic_items.json")
    # Remove any stale pm items before appending (idempotent re-runs)
    existing_diag = [x for x in existing_diag if x.get("role_id") != "pm"]
    existing_diag.extend(diag_items)

    existing_atoms = load_json(CONTENT / "atomic_modules.json")
    # Remove stale pm atoms before appending (idempotent re-runs)
    existing_atoms = [a for a in existing_atoms if not a["atom_id"].endswith("__" + a["atom_id"].split("__")[-1]) or "pm_" not in a["atom_id"]]
    existing_atoms.extend(new_atoms)

    print("\nWriting files...")
    save_json(CONTENT / "courses.json", existing_courses, args.dry_run)
    save_json(CONTENT / "reading_content.json", existing_reading, args.dry_run)
    save_json(CONTENT / "practice_scenarios.json", existing_scenarios, args.dry_run)
    save_json(CONTENT / "evaluation_items.json", existing_eval, args.dry_run)
    save_json(CONTENT / "diagnostic_items.json", existing_diag, args.dry_run)
    save_json(CONTENT / "atomic_modules.json", existing_atoms, args.dry_run)

    if not args.dry_run:
        verify()
    else:
        print("\n(run without --dry-run to write files and verify)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
