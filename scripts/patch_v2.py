#!/usr/bin/env python3
"""
Patch content/atomic_modules_v2.json — two targeted fixes on canonical atoms only.

Fix A — Add task_mode + mcq_options to all 5 canonical atoms' task_templates
  Task 1: task_mode="open", mcq_options=null
  Tasks 2/3/4: task_mode="mcq", mcq_options=[3 options, exactly 1 is_best=true]
  MCQ options synthesised from the 4 role-specific source atoms (AN/MK/RM/UW);
  PM atoms are all-open so they contribute no MCQ content.
  1 Haiku call per canonical group → 5 calls total.

Fix B — Replace oversized compound tags in capstone__end_to_end_workflow
  Deterministic replacement, no LLM.

Does NOT touch role-variant atoms or any other canonical atom's tags.
Overwrites content/atomic_modules_v2.json in-place.

Run:
    python scripts/patch_v2.py
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import urllib3
import requests as _requests
from tenacity import retry, wait_random_exponential, stop_after_attempt

# ─── Config ───────────────────────────────────────────────────────────────────

DATABRICKS_HOST = os.environ.get(
    "DATABRICKS_HOST", "https://adb-2717931942638877.17.azuredatabricks.net"
)
HAIKU_ENDPOINT = "databricks-claude-haiku-4-5"
CONTENT_DIR = Path(__file__).parent.parent / "content"

_INSECURE = os.environ.get("DATABRICKS_INSECURE", "").lower() in ("1", "true", "yes")
if _INSECURE:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── Group A source mapping (same as merge_atoms.py, PM excluded for MCQ) ────

# PM atom IDs (all-open mode — skip for MCQ synthesis)
PM_ATOM_IDS = {
    "responsible_ai__pm_c1_responsible_ai",
    "strategic_prompting__pm_c2_strategic_prompting",
    "critical_eval__pm_c3_critical_eval",
    "augmented_comm__pm_c6_augmented_comm",
    "capstone__pm_c7_capstone",
}

GROUP_A: list[dict] = [
    {
        "canonical_id": "responsible_ai__safe_framework",
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
        "source_ids": [
            "augmented_comm__an_c6_augmented_comm",
            "augmented_comm__mk_c6_augmented_comm",
            "augmented_comm__rm_c6_augmented_comm",
            "augmented_comm__uw_c6_augmented_comm",
            "augmented_comm__pm_c6_augmented_comm",
        ],
    },
    {
        "canonical_id": "capstone__end_to_end_workflow",
        "source_ids": [
            "responsible_ai__an_c7_capstone",
            "responsible_ai__mk_c7_capstone",
            "responsible_ai__rm_c7_capstone",
            "responsible_ai__uw_c7_capstone",
            "capstone__pm_c7_capstone",
        ],
    },
]

# Fix B: exact old→new tag mapping for capstone only
CAPSTONE_TAG_MAP = {
    "safe_craf_verify_relate_signal_framework": "safe_craf_verify_framework",
    "strategic_prompting_and_critical_evaluation": "strategic_prompting",
    "responsible_data_handling_and_verification": "responsible_ai",
    "stakeholder_communication_and_relationship_intelligence": "relationship_intel",
    "multi_tool_orchestration_and_copilot_surface_selector": "augmented_comm",
}

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
def _call_llm(system: str, user: str, max_tokens: int = 1500) -> str:
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


def _call_json(system: str, user: str, max_tokens: int = 1500) -> dict:
    return json.loads(_call_llm(system, user, max_tokens))


# ─── Fix A: synthesise MCQ options for one canonical group ───────────────────


def _fmt_opts(opts: list[dict]) -> str:
    return " | ".join(
        f"{'[BEST] ' if o.get('is_best') else ''}{o['label']}" for o in opts
    )


def synthesise_mcq(group: dict, src_atoms: dict[str, dict]) -> dict:
    """
    Returns {canonical_id, task_2_opts, task_3_opts, task_4_opts}
    where each *_opts is a list[dict] with keys label + is_best.
    """
    canonical_id = group["canonical_id"]

    # Find the v2 canonical atom to get the task text_templates
    # (passed in as a separate arg below — we look them up from v2_by_id)
    # This function receives source atoms from atomic_modules.json
    mcq_source_ids = [s for s in group["source_ids"] if s not in PM_ATOM_IDS]

    # Build context: canonical task templates are extracted from the v2 atom
    # (injected via closure — see caller)
    canonical_tasks = group["canonical_tasks"]  # injected by caller

    task_texts = {}
    for t in canonical_tasks:
        tid = t["task_id"]
        if tid in (2, 3, 4):
            task_texts[tid] = t["text_template"][:500]  # truncate for context

    # Build source MCQ block
    source_block_lines = []
    for sid in mcq_source_ids:
        atom = src_atoms.get(sid)
        if not atom:
            continue
        role_label = sid.split("__")[1].split("_")[0].upper()  # e.g. AN, MK, RM, UW
        p = atom.get("practice", {})
        mcq_opts = p.get("task_mcq_options", [])
        modes = p.get("task_modes", [])
        source_block_lines.append(f"--- {role_label} ---")
        for task_idx in (1, 2, 3):  # 0-based index for tasks 2, 3, 4
            if task_idx < len(mcq_opts) and mcq_opts[task_idx]:
                source_block_lines.append(
                    f"  Task {task_idx + 1}: {_fmt_opts(mcq_opts[task_idx])}"
                )

    source_block = "\n".join(source_block_lines)

    system = (
        "You are building training content for a generic professional AI upskilling programme. "
        "Your job is to synthesise role-agnostic MCQ answer options from role-specific source options. "
        "Output valid JSON only. No markdown fences."
    )

    user = f"""Canonical atom: {canonical_id}

Canonical task templates (for context — understand what each task is asking):
Task 2: {task_texts.get(2, '')}
Task 3: {task_texts.get(3, '')}
Task 4: {task_texts.get(4, '')}

Source role-specific MCQ options (synthesise from these):
{source_block}

Synthesise the best generalizable MCQ options for tasks 2, 3, and 4.
Rules:
- Exactly 3 options per task.
- Exactly 1 option has is_best=true per task (the option that reflects the correct framework behaviour).
- Labels must be role-agnostic — do NOT mention specific roles (Relationship Manager, Underwriter, Analyst, etc.).
  Use neutral professional language. You may use {{role}} as a placeholder if helpful.
- Each label 40–80 characters.
- Draw on the best answer from the source options and adapt it to be universally applicable.

Return JSON in this exact shape:
{{
  "task_2": [{{"label": "...", "is_best": true}}, {{"label": "...", "is_best": false}}, {{"label": "...", "is_best": false}}],
  "task_3": [...],
  "task_4": [...]
}}"""

    result = _call_json(system, user)
    return {"canonical_id": canonical_id, "mcq": result}


# ─── Fix B: replace capstone tags ─────────────────────────────────────────────


def fix_capstone_tags(atom: dict) -> dict:
    new_tags = [CAPSTONE_TAG_MAP.get(tag, tag) for tag in atom["capability_tags"]]
    atom["capability_tags"] = new_tags
    return atom


# ─── Inject MCQ into canonical atom ──────────────────────────────────────────


def inject_mcq(canonical_atom: dict, mcq: dict) -> dict:
    new_tasks = []
    for t in canonical_atom["practice"]["task_templates"]:
        tid = t["task_id"]
        new_t = dict(t)
        if tid == 1:
            new_t["task_mode"] = "open"
            new_t["mcq_options"] = None
        else:
            task_key = f"task_{tid}"
            opts = mcq.get(task_key, [])
            new_t["task_mode"] = "mcq"
            new_t["mcq_options"] = opts
        new_tasks.append(new_t)
    canonical_atom["practice"]["task_templates"] = new_tasks
    return canonical_atom


# ─── Verification ─────────────────────────────────────────────────────────────


def verify(atoms: list[dict]) -> bool:
    canonicals = [a for a in atoms if a.get("status") == "canonical"]
    ok = True
    print(f"\n{'─'*60}")
    print("Verification")
    print(f"{'─'*60}")
    for a in sorted(canonicals, key=lambda x: x["atom_id"]):
        aid = a["atom_id"]
        tasks = a.get("practice", {}).get("task_templates", [])
        issues = []

        for t in tasks:
            tid = t["task_id"]
            if "task_mode" not in t:
                issues.append(f"task {tid} missing task_mode")
            if tid == 1:
                if t.get("task_mode") != "open":
                    issues.append(f"task 1 mode should be open, got {t.get('task_mode')}")
            else:
                if t.get("task_mode") != "mcq":
                    issues.append(f"task {tid} mode should be mcq, got {t.get('task_mode')}")
                opts = t.get("mcq_options", [])
                if not opts or len(opts) != 3:
                    issues.append(f"task {tid} needs 3 mcq_options, got {len(opts) if opts else 0}")
                else:
                    best_count = sum(1 for o in opts if o.get("is_best"))
                    if best_count != 1:
                        issues.append(f"task {tid} needs exactly 1 is_best, got {best_count}")

        tags = a.get("capability_tags", [])
        long_tags = [tag for tag in tags if len(tag) > 30]
        and_tags = [tag for tag in tags if "_and_" in tag]
        if long_tags:
            issues.append(f"long tags: {long_tags}")
        if and_tags:
            issues.append(f"compound _and_ tags: {and_tags}")

        if issues:
            print(f"[FAIL] {aid}")
            for iss in issues:
                print(f"       - {iss}")
            ok = False
        else:
            print(f"[OK]   {aid}  tasks={len(tasks)}  tags={len(tags)}")

    print(f"{'─'*60}")
    print("PASS" if ok else "FAIL — see issues above")
    return ok


# ─── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    v2_path = CONTENT_DIR / "atomic_modules_v2.json"
    src_path = CONTENT_DIR / "atomic_modules.json"

    print("Loading atoms...")
    with open(v2_path, encoding="utf-8") as f:
        v2_atoms: list[dict] = json.load(f)
    with open(src_path, encoding="utf-8") as f:
        src_atoms_list: list[dict] = json.load(f)

    v2_by_id = {a["atom_id"]: a for a in v2_atoms}
    src_by_id = {a["atom_id"]: a for a in src_atoms_list}

    # ── Fix B: capstone tags (no LLM) ─────────────────────────────────────────
    print("\nFix B — patching capstone tags...")
    capstone = v2_by_id.get("capstone__end_to_end_workflow")
    if capstone:
        old_tags = list(capstone["capability_tags"])
        fix_capstone_tags(capstone)
        print(f"  Before: {old_tags}")
        print(f"  After:  {capstone['capability_tags']}")
    else:
        print("  WARNING: capstone__end_to_end_workflow not found in v2")

    # ── Fix A: synthesise and inject MCQ options (5 parallel LLM calls) ───────
    print("\nFix A — synthesising MCQ options (5 Haiku calls)...")

    # Inject canonical_tasks into each group def for the LLM prompt
    groups_with_tasks = []
    for grp in GROUP_A:
        canonical = v2_by_id.get(grp["canonical_id"])
        if not canonical:
            print(f"  WARNING: {grp['canonical_id']} not found in v2 — skipping")
            continue
        grp_copy = dict(grp)
        grp_copy["canonical_tasks"] = canonical["practice"]["task_templates"]
        groups_with_tasks.append(grp_copy)

    results: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(synthesise_mcq, grp, src_by_id): grp["canonical_id"]
            for grp in groups_with_tasks
        }
        for future in as_completed(futures):
            cid = futures[future]
            try:
                res = future.result()
                results[cid] = res["mcq"]
                print(f"  [done] {cid}")
            except Exception as exc:
                print(f"  [ERROR] {cid}: {exc}")
                raise

    # Inject MCQ results into v2 canonical atoms
    for grp in groups_with_tasks:
        cid = grp["canonical_id"]
        if cid in results:
            inject_mcq(v2_by_id[cid], results[cid])

    # ── Write patched v2 ──────────────────────────────────────────────────────
    # Preserve original sort order (canonical first, then role-variant, alpha within each)
    canonicals = sorted(
        [a for a in v2_atoms if a.get("status") == "canonical"],
        key=lambda a: a["atom_id"],
    )
    variants = sorted(
        [a for a in v2_atoms if a.get("status") != "canonical"],
        key=lambda a: a["atom_id"],
    )
    patched = canonicals + variants

    with open(v2_path, "w", encoding="utf-8") as f:
        json.dump(patched, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {len(patched)} atoms → {v2_path}")

    # ── Verify ────────────────────────────────────────────────────────────────
    verify(patched)


if __name__ == "__main__":
    main()
