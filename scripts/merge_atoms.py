#!/usr/bin/env python3
"""
Merge 35 role-specific atoms → 15 canonical/role-variant atoms.

Reads:  content/atomic_modules.json
Writes: content/atomic_modules_v2.json

Run:
    python scripts/merge_atoms.py --dry-run             # print merge plan, no LLM
    python scripts/merge_atoms.py --group responsible_ai  # test one domain group
    python scripts/merge_atoms.py                       # full run
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import urllib3
import requests as _requests
from tenacity import retry, wait_random_exponential, stop_after_attempt

# ─── Config ──────────────────────────────────────────────────────────────────

DATABRICKS_HOST = os.environ.get(
    "DATABRICKS_HOST", "https://adb-2717931942638877.17.azuredatabricks.net"
)
HAIKU_ENDPOINT = "databricks-claude-haiku-4-5"
CONTENT_DIR = Path(__file__).parent.parent / "content"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

_INSECURE = os.environ.get("DATABRICKS_INSECURE", "").lower() in ("1", "true", "yes")
if _INSECURE:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── Merge group definitions (hardcoded from decision table) ──────────────────

GROUP_A: list[dict] = [
    {
        "canonical_id": "responsible_ai__safe_framework",
        "domain": "responsible_ai",
        "source_ids": [
            "responsible_ai__an_c1_responsible_ai",
            "responsible_ai__mk_c1_responsible_ai",
            "responsible_ai__rm_c1_responsible_ai",
            "responsible_ai__uw_c1_responsible_ai",
            "responsible_ai__pm_c1_responsible_ai",
        ],
    },
    {
        "canonical_id": "strategic_prompting__craf_framework",
        "domain": "strategic_prompting",
        "source_ids": [
            "strategic_prompting__an_c2_strategic_prompting",
            "strategic_prompting__mk_c2_strategic_prompting",
            "strategic_prompting__rm_c2_strategic_prompting",
            "strategic_prompting__uw_c2_strategic_prompting",
            "strategic_prompting__pm_c2_strategic_prompting",
        ],
    },
    {
        "canonical_id": "critical_eval__verify_framework",
        "domain": "critical_eval",
        "source_ids": [
            "critical_eval__an_c3_critical_eval",
            "critical_eval__mk_c3_critical_eval",
            "critical_eval__rm_c3_critical_eval",
            "critical_eval__uw_c3_critical_eval",
            "critical_eval__pm_c3_critical_eval",
        ],
    },
    {
        "canonical_id": "augmented_comm__surface_workflow",
        "domain": "augmented_comm",
        "source_ids": [
            "augmented_comm__an_c6_augmented_comm",
            "augmented_comm__mk_c6_augmented_comm",
            "augmented_comm__rm_c6_augmented_comm",
            "augmented_comm__uw_c6_augmented_comm",
            "augmented_comm__pm_c6_augmented_comm",
        ],
    },
    {
        # NOTE: an/mk/rm/uw capstones are stored with domain="responsible_ai" due to a
        # Phase 0.5 schema issue; pm capstone correctly has domain="capstone".
        # All 5 are treated as capstones for merge purposes.
        "canonical_id": "capstone__end_to_end_workflow",
        "domain": "capstone",
        "source_ids": [
            "responsible_ai__an_c7_capstone",
            "responsible_ai__mk_c7_capstone",
            "responsible_ai__rm_c7_capstone",
            "responsible_ai__uw_c7_capstone",
            "capstone__pm_c7_capstone",
        ],
    },
]

GROUP_B: list[str] = [
    "data_decision__an_c5_data_decision",
    "data_decision__mk_c5_data_decision",
    "data_decision__rm_c5_data_decision",
    "data_decision__uw_c5_data_decision",
    "data_decision__pm_c5_data_decision",
    "relationship_intel__an_c4_relationship_intel",
    "relationship_intel__mk_c4_relationship_intel",
    "relationship_intel__rm_c4_relationship_intel",
    "relationship_intel__uw_c4_relationship_intel",
    "relationship_intel__pm_c4_relationship_intel",
]

# ─── Auth + HTTP ──────────────────────────────────────────────────────────────

_TOKEN: str | None = None


def _get_token() -> str:
    import subprocess

    result = subprocess.run(
        ["databricks", "auth", "token", "--host", DATABRICKS_HOST, "--profile", "dev"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        token = os.environ.get("DATABRICKS_TOKEN", "")
        if not token:
            raise RuntimeError(f"Could not get Databricks token: {result.stderr}")
        return token
    return json.loads(result.stdout)["access_token"]


def _token() -> str:
    global _TOKEN
    if _TOKEN is None:
        _TOKEN = os.environ.get("DATABRICKS_TOKEN") or _get_token()
    return _TOKEN


@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
def _call_llm(system: str, user: str, max_tokens: int = 4000) -> str:
    """Call Haiku via direct HTTP and return raw text content."""
    url = f"{DATABRICKS_HOST}/serving-endpoints/{HAIKU_ENDPOINT}/invocations"
    payload = {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }
    resp = _requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {_token()}"},
        verify=not _INSECURE,
        timeout=90,
    )
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"].strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return text


def _call_json(system: str, user: str, max_tokens: int = 4000) -> dict:
    return json.loads(_call_llm(system, user, max_tokens))


# ─── Reading content helpers ──────────────────────────────────────────────────


def _reading_text(atom: dict) -> str:
    """Serialize an atom's concept content as readable text (handles both schemas)."""
    r = atom.get("reading", {})
    concept = r.get("concept", {})
    if concept:
        lines = []
        fa = concept.get("framework_acronym")
        if fa:
            lines.append(f"Framework acronym: {fa}")
        intro = concept.get("intro", "")
        if intro:
            lines.append(f"Intro: {intro}")
        for card in concept.get("cards", []):
            lines.append(
                f"  {card.get('letter')} — {card.get('title')}: {card.get('body', '')}"
            )
        for g in concept.get("guardrails", []):
            lines.append(f"  Guardrail: {g}")
        return "\n".join(lines)
    return r.get("concept_text", "")


def _role_label(atom: dict) -> str:
    """Derive short role label (AN/MK/RM/UW/PM) from source_course_ids."""
    cids = atom.get("source_course_ids", [])
    if cids:
        return cids[0].split("_")[0].upper()
    return atom["atom_id"].split("__")[1].split("_")[0].upper()


# ─── Merge canonical (Group A) — 4 LLM calls ────────────────────────────────


def merge_canonical(group: dict, atoms_by_id: dict[str, dict]) -> dict:
    source_atoms = [atoms_by_id[sid] for sid in group["source_ids"]]
    n = len(source_atoms)
    canonical_id = group["canonical_id"]

    # ── Call 1: reading synthesis ─────────────────────────────────────────────
    print(f"  [{canonical_id}] Call 1: reading synthesis")
    reading_blocks = []
    for atom in source_atoms:
        role = _role_label(atom)
        r = atom.get("reading", {})
        reading_blocks.append(
            f"=== {role} version ===\n"
            f"Concept:\n{_reading_text(atom)}\n\n"
            f"Good example:\n{r.get('good_example', '')}\n\n"
            f"Anti-pattern:\n{r.get('anti_pattern', '')}\n\n"
            f"Takeaway: {r.get('takeaway', '')}"
        )

    reading_sys = (
        f"You are merging {n} role-specific AI training modules into one canonical "
        "role-agnostic atom. Synthesize the best reading content that works for any "
        "professional role. Rules: "
        "(1) No 'As an RM/analyst/PM/underwriter/marketer/project manager' framing "
        "— use 'As a professional' or 'In your work'. "
        "(2) The concept_text MUST answer 'what is in this for me personally?' within "
        "2 sentences, then explain the full framework with all letter cards and guardrails "
        "preserved in the same text. "
        "(3) good_example shows a concrete time-saving or quality win, not compliance. "
        "(4) Keep all framework explanation intact — do not omit or shorten the framework cards. "
        "(5) takeaway names a concrete personal benefit. "
        "(6) title should be role-agnostic and reference the framework acronym."
    )
    reading_user = (
        f"Here are {n} role-specific versions of a training module's reading content.\n"
        "Synthesize one canonical version of each field plus a canonical title.\n\n"
        + "\n\n".join(reading_blocks)
        + "\n\nOutput JSON only (no markdown fences, no explanation):\n"
        '{"title": "...", "concept_text": "...", "good_example": "...", '
        '"anti_pattern": "...", "takeaway": "..."}'
    )
    reading_result = _call_json(reading_sys, reading_user)

    # ── Call 2: scenario template synthesis ───────────────────────────────────
    print(f"  [{canonical_id}] Call 2: scenario template")
    scenario_blocks = "\n\n".join(
        f"[{_role_label(a)}]: {a.get('practice', {}).get('scenario_template', '')}"
        for a in source_atoms
    )
    scenario_sys = (
        "Synthesize the most generic, placeholder-rich scenario_template from "
        f"{n} role-specific versions. "
        "Use ONLY these placeholders: {role}, {org_type}, {case_type}, {data_types}, "
        "{sensitivity_level}, {workflow_goal}, {programme_name}, {audience}. "
        "No hardcoded role names, no fictional org names in the template itself — "
        "those are filled at runtime. The template MUST contain {role} and {org_type}."
    )
    scenario_user = (
        f"Here are {n} role-specific scenario_templates. "
        "Produce one canonical scenario_template.\n\n"
        + scenario_blocks
        + '\n\nOutput JSON only: {"scenario_template": "..."}'
    )
    scenario_result = _call_json(scenario_sys, scenario_user)

    # ── Call 3: task templates synthesis ──────────────────────────────────────
    print(f"  [{canonical_id}] Call 3: task templates")
    task_blocks = []
    for atom in source_atoms:
        role = _role_label(atom)
        tasks = atom.get("practice", {}).get("task_templates") or []
        task_lines = []
        for t in tasks:
            text = str(t.get("text_template", ""))[:600]
            task_lines.append(
                f"  Task {t.get('task_id')}: {text}{'...' if len(str(t.get('text_template',''))) > 600 else ''}"
            )
        task_blocks.append(f"[{role}]:\n" + "\n".join(task_lines))

    task_sys = (
        "Synthesize one set of 4 canonical task_templates from N role-specific versions. "
        "Keep skill_focus precise (3-8 words naming the specific AI skill practiced). "
        "text_template must use placeholders for role-specific nouns: {role}, {org_type}, "
        "{case_type}, {data_types}, {sensitivity_level}, {workflow_goal}, {programme_name}, {audience}. "
        "Preserve step numbers and task structure. "
        "Output JSON array only."
    )
    task_user = (
        f"Here are {n} sets of 4 task templates. "
        "Produce one canonical set of 4 task_templates.\n\n"
        + "\n\n".join(task_blocks)
        + "\n\nOutput JSON only:\n"
        '{"task_templates": [{"task_id": 1, "text_template": "...", "skill_focus": "..."}, '
        '{"task_id": 2, "text_template": "...", "skill_focus": "..."}, '
        '{"task_id": 3, "text_template": "...", "skill_focus": "..."}, '
        '{"task_id": 4, "text_template": "...", "skill_focus": "..."}]}'
    )
    task_result = _call_json(task_sys, task_user)

    # ── Call 4: coach + tags + hint synthesis ─────────────────────────────────
    print(f"  [{canonical_id}] Call 4: coach + tags + hint")
    coach_blocks = []
    for atom in source_atoms:
        role = _role_label(atom)
        coach = (atom.get("practice", {}).get("coach_system_prompt_template") or "")[:500]
        tags = atom.get("capability_tags", [])
        hint = atom.get("role_variants_hint", "")[:200]
        coach_blocks.append(
            f"[{role}]:\n"
            f"Coach (first 500 chars): {coach}...\n"
            f"Tags: {json.dumps(tags)}\n"
            f"Role hint: {hint}"
        )

    coach_sys = (
        "Synthesize three fields from N role-specific atoms into canonical versions:\n"
        "(1) coach_system_prompt_template — use {role}, {organisation}, {scenario_name} "
        "placeholders; remove any hardcoded job titles or org names; preserve ALL coaching "
        "logic, rubric guidance, task-by-task instructions, and conversation discipline rules. "
        "Expand to a full coach prompt (not just the first 500 chars — infer the full structure). "
        "(2) capability_tags — union of all tags, deduplicated, keep 3-6 items; "
        "first tag MUST be the framework-name tag (safe_framework, craf_framework, etc.); "
        "prioritize universally applicable skill tags. "
        "(3) role_variants_hint — 2-3 sentences covering ALL roles: what context changes per role, "
        "which {placeholder} values matter most, and what the runtime LLM should inject."
    )
    coach_user = (
        f"Here are {n} atoms' coach prompts (first 500 chars), tag lists, and role hints.\n\n"
        + "\n\n".join(coach_blocks)
        + "\n\nOutput JSON only:\n"
        '{"coach_system_prompt_template": "...", "capability_tags": [...], "role_variants_hint": "..."}'
    )
    coach_result = _call_json(coach_sys, coach_user)

    # ── Assemble ──────────────────────────────────────────────────────────────
    source_course_ids = [
        cid for a in source_atoms for cid in a.get("source_course_ids", [])
    ]
    return {
        "atom_id": canonical_id,
        "title": reading_result.get("title", canonical_id.replace("__", ": ").replace("_", " ")),
        "domain": group["domain"],
        "capability_tags": coach_result.get("capability_tags", []),
        "estimated_minutes": 30,
        "role_variants_hint": coach_result.get("role_variants_hint", ""),
        "reading": {
            "concept_text": reading_result.get("concept_text", ""),
            "good_example": reading_result.get("good_example", ""),
            "anti_pattern": reading_result.get("anti_pattern", ""),
            "takeaway": reading_result.get("takeaway", ""),
        },
        "practice": {
            "scenario_template": scenario_result.get("scenario_template", ""),
            "task_templates": task_result.get("task_templates", []),
            "coach_system_prompt_template": coach_result.get(
                "coach_system_prompt_template", ""
            ),
        },
        "eval": {
            "items_ref": "evaluation_items.json",
            "source_course_ids": source_course_ids,
        },
        "source_course_ids": source_course_ids,
        "merged_from": group["source_ids"],
        "atomized_at": TODAY,
        "status": "canonical",
    }


# ─── Improve variant (Group B) — 1 LLM call ─────────────────────────────────


def improve_variant(atom: dict) -> dict:
    atom_id = atom["atom_id"]
    print(f"  [{atom_id}] improving variant")

    improve_sys = (
        "Improve this role-variant atom's template fields. "
        "Do NOT change the role-specific framing — this atom is intentionally role-specific. "
        "Goals:\n"
        "(1) scenario_template: use {programme_name} and {case_type} placeholders for any "
        "fictional programme names or case labels currently hardcoded, while keeping the "
        "role context intact. Must still contain {role} and {org_type}.\n"
        "(2) coach_system_prompt_template: replace hardcoded job titles with {role} and "
        "hardcoded org names with {organisation} where they appear.\n"
        "(3) role_variants_hint: write 2-3 sentences naming concrete differences this "
        "specific role has compared with other roles in the same domain — what data types, "
        "workflows, or stakeholders differ, and which {placeholder} values matter most."
    )
    improve_user = (
        f"Full atom JSON:\n{json.dumps(atom, indent=2, ensure_ascii=False)}\n\n"
        "Output JSON only (no markdown fences, no explanation):\n"
        '{"scenario_template": "...", "coach_system_prompt_template": "...", "role_variants_hint": "..."}'
    )
    result = _call_json(improve_sys, improve_user, max_tokens=4000)

    # Return improved atom (immutable update pattern)
    improved_practice = {**atom.get("practice", {})}
    if "scenario_template" in result:
        improved_practice["scenario_template"] = result["scenario_template"]
    if "coach_system_prompt_template" in result:
        improved_practice["coach_system_prompt_template"] = result[
            "coach_system_prompt_template"
        ]

    return {
        **atom,
        "role_variants_hint": result.get(
            "role_variants_hint", atom.get("role_variants_hint", "")
        ),
        "practice": improved_practice,
        "atomized_at": TODAY,
        "status": "role-variant",
    }


# ─── Load ─────────────────────────────────────────────────────────────────────


def load_atoms() -> dict[str, dict]:
    path = CONTENT_DIR / "atomic_modules.json"
    atoms = json.loads(path.read_text(encoding="utf-8"))
    return {a["atom_id"]: a for a in atoms}


# ─── Dry-run ──────────────────────────────────────────────────────────────────


def print_merge_plan(atoms_by_id: dict[str, dict]) -> None:
    print("=" * 70)
    print("GROUP A — Canonical merges (5 → 1 each)")
    print("=" * 70)
    for g in GROUP_A:
        missing = [sid for sid in g["source_ids"] if sid not in atoms_by_id]
        status = "OK" if not missing else f"MISSING: {missing}"
        print(f"\n  canonical_id : {g['canonical_id']}")
        print(f"  domain       : {g['domain']}")
        print(f"  sources      : {status}")
        for sid in g["source_ids"]:
            mark = "✓" if sid in atoms_by_id else "✗"
            print(f"    {mark} {sid}")

    print()
    print("=" * 70)
    print("GROUP B — Role-variant improvements (10 atoms)")
    print("=" * 70)
    for atom_id in GROUP_B:
        mark = "✓" if atom_id in atoms_by_id else "✗ MISSING"
        print(f"  {mark}  {atom_id}")

    total_a = len(GROUP_A) * 4
    total_b = len(GROUP_B) * 1
    print(f"\nTotal LLM calls  : {total_a} (Group A) + {total_b} (Group B) = {total_a + total_b}")
    print(
        f"Expected v2 atoms: {len(GROUP_A)} canonical + {len(GROUP_B)} role-variant "
        f"= {len(GROUP_A) + len(GROUP_B)} total"
    )


# ─── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print merge plan only, no LLM calls"
    )
    parser.add_argument(
        "--group",
        help=(
            "Process only the Group A group matching this string "
            "(matches canonical_id prefix or domain, e.g. 'responsible_ai')"
        ),
    )
    args = parser.parse_args()

    atoms_by_id = load_atoms()
    print(f"Loaded {len(atoms_by_id)} atoms from atomic_modules.json")

    if args.dry_run:
        print_merge_plan(atoms_by_id)
        return

    # Warm up token cache before spawning threads
    try:
        _token()
        print("Auth: OK")
    except Exception as exc:
        sys.exit(f"ERROR: Could not authenticate with Databricks: {exc}")

    # Filter Group A if --group is specified
    group_a_to_run = GROUP_A
    if args.group:
        group_a_to_run = [
            g
            for g in GROUP_A
            if args.group in g["canonical_id"] or args.group == g["domain"]
        ]
        if not group_a_to_run:
            sys.exit(
                f"ERROR: No Group A group matches '{args.group}'. "
                f"Valid domains: {[g['domain'] for g in GROUP_A]}"
            )
        print(f"Scoped to: {[g['canonical_id'] for g in group_a_to_run]}")

    results: list[dict] = []

    # Group A: parallel canonical merges (max 3 concurrent threads)
    print(
        f"\nGroup A: merging {len(group_a_to_run)} group(s) "
        "with ThreadPoolExecutor(max_workers=3)..."
    )
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(merge_canonical, g, atoms_by_id): g["canonical_id"]
            for g in group_a_to_run
        }
        for future in as_completed(futures):
            cid = futures[future]
            try:
                atom = future.result()
                results.append(atom)
                print(f"  Done canonical: {cid}")
            except Exception as exc:
                print(f"  ERROR [{cid}]: {exc}", file=sys.stderr)
                raise

    # Group B: sequential variant improvements (skipped when --group is used)
    if not args.group:
        print(f"\nGroup B: improving {len(GROUP_B)} role-variant atoms sequentially...")
        for atom_id in GROUP_B:
            atom = atoms_by_id.get(atom_id)
            if not atom:
                print(
                    f"  WARN: {atom_id} not found in source atoms",
                    file=sys.stderr,
                )
                continue
            try:
                improved = improve_variant(atom)
                results.append(improved)
            except Exception as exc:
                print(f"  ERROR [{atom_id}]: {exc}", file=sys.stderr)
                raise

    # Sort: canonical first, then role-variant, each group alphabetically
    results.sort(
        key=lambda a: (0 if a.get("status") == "canonical" else 1, a["atom_id"])
    )

    out_path = CONTENT_DIR / "atomic_modules_v2.json"
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    n_canonical = sum(1 for a in results if a.get("status") == "canonical")
    n_variant = sum(1 for a in results if a.get("status") == "role-variant")
    print(f"\nWrote {len(results)} atoms to {out_path}")
    print(f"  canonical   : {n_canonical}")
    print(f"  role-variant: {n_variant}")


if __name__ == "__main__":
    main()
