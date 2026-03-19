#!/usr/bin/env python3
"""
Convert 28 role-specific courses into role-agnostic atomic modules.

Reads:
    content/courses.json
    content/practice_scenarios.json
    content/reading_content_structured.json  (primary)
    content/reading_content.json             (fallback)

Writes:
    content/atomic_modules.json
    content/atomic_overlap_report.json

Run:
    python scripts/atomize_coursework.py                                    # all 28
    python scripts/atomize_coursework.py --dry-run                          # pretty-print, no write
    python scripts/atomize_coursework.py --course-id rm_c1_responsible_ai  # single test
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import urllib3
import requests as _requests

# Corporate SSL proxy workaround: the proxy re-signs TLS certs; Python SDK rejects them.
# This script uses direct HTTP calls (not the Databricks SDK) to avoid the SSL issue
# and to bypass the 5-minute host metadata resolution timeout in WorkspaceClient.
#
# Set DATABRICKS_INSECURE=1 to disable SSL verification (dev-only batch script).
_INSECURE = os.environ.get("DATABRICKS_INSECURE", "").lower() in ("1", "true", "yes")
if _INSECURE:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from tenacity import retry, wait_random_exponential, stop_after_attempt

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST", "https://adb-2717931942638877.17.azuredatabricks.net")
SONNET_ENDPOINT = os.environ.get("SONNET_ENDPOINT", "databricks-claude-sonnet-4-6")
CONTENT_DIR = Path(__file__).parent.parent / "content"
MAX_WORKERS = 4

# Capstone courses: included in atoms but excluded from overlap detection
# (integrative courses would produce false-positive clusters with *_c1_responsible_ai)
CAPSTONE_IDS = {"rm_c7_capstone", "uw_c7_capstone", "an_c7_capstone", "mk_c7_capstone"}

# ---------------------------------------------------------------------------
# Extraction prompts
# ---------------------------------------------------------------------------

TAG_EXTRACTION_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Extract 3–6 capability tags from the following course metadata. Tags identify the core AI
skill or framework taught in this module. They are used to detect which modules teach the
same underlying capability (even when framed for different professional roles).

<title>{title}</title>
<description>{description}</description>
<real_use_case>{real_use_case}</real_use_case>
<framework_acronym>{framework_acronym}</framework_acronym>

Output a single JSON array of lowercase, underscore-separated strings — no prose, no
markdown fences:
["tag_one", "tag_two", ...]

Rules:
- 3–6 tags per module
- FIRST tag MUST be the framework name: if framework_acronym is non-empty, use
  "{framework_acronym_lower}_framework" (e.g. "safe_framework", "craf_framework",
  "verify_framework"). This tag is required — it enables cross-role overlap detection.
- Remaining tags: (1) the key skill domain, (2) 1–3 specific capabilities
- Tag names must be ROLE-AGNOSTIC — describe the skill, not the job title context
- Do NOT include generic tags like "ai_usage" or "professional_development"
- Do NOT include role-specific tags like "rm_workflow" or "underwriting_process"
- Return only the JSON array
"""

SCENARIO_TEMPLATE_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Convert the following role-specific practice scenario into a role-agnostic template using
placeholder variables. The template must work for any professional role.

<scenario_text>
{scenario_text}
</scenario_text>

Available placeholders (use ONLY these):
- {{role}} — learner's job title
- {{org_type}} — type of organization
- {{case_type}} — type of work case
- {{data_types}} — what data is present
- {{sensitivity_level}} — data classification
- {{workflow_goal}} — the task objective
- {{programme_name}} — name of the project or programme
- {{audience}} — target audience for a deliverable

Output a single string — the de-roled scenario template — no JSON wrapping, no markdown fences.

Rules:
- Replace ALL role-specific references (job titles, org names, programme names) with
  the appropriate placeholder
- Fictional org names (Meridian, Aurora, Cascade, Crestview) → replace with {{org_type}}
  or {{organisation}}; do NOT keep hardcoded fictional org names
- Preserve the scenario's instructional intent exactly — de-role the framing only
- The output MUST contain at least {{role}} and {{org_type}}
- Return only the template string
"""

TASK_GENERALIZATION_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Convert 4 role-specific practice tasks into role-agnostic task templates using placeholder
variables. Each task asks a learner to perform an AI-assisted work activity.

<task_1>{task_1_text}</task_1>
<task_2>{task_2_text}</task_2>
<task_3>{task_3_text}</task_3>
<task_4>{task_4_text}</task_4>

Available placeholders:
{{role}}, {{org_type}}, {{case_type}}, {{data_types}}, {{sensitivity_level}},
{{workflow_goal}}, {{programme_name}}, {{audience}}

Output a single JSON array with exactly 4 objects — no prose, no markdown fences:
[
  {{"task_id": 1, "text_template": "<de-roled task>", "skill_focus": "<3-8 word description>"}},
  {{"task_id": 2, "text_template": "...", "skill_focus": "..."}},
  {{"task_id": 3, "text_template": "...", "skill_focus": "..."}},
  {{"task_id": 4, "text_template": "...", "skill_focus": "..."}}
]

Rules:
- Preserve step numbers, headings (e.g. "Step 1:", "Task:"), and structure exactly
- Replace programme names, client names, and job-title-specific references with placeholders
- skill_focus: 3-8 words naming the specific AI skill practiced
- Do NOT paraphrase or simplify the task — de-role only
- Return only the JSON array
"""

COACH_GENERALIZATION_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Convert a role-specific AI coach system prompt into a role-agnostic template. The coach is
an AI assistant that guides learners through practice tasks — it must serve any role.

<coach_system_prompt>
{coach_system_prompt}
</coach_system_prompt>

Available placeholders:
- {{role}} — learner's job title
- {{organisation}} — the learner's fictional organization name
- {{scenario_name}} — the name of the practice programme or project
- {{domain}} — the AI skill domain being practiced

Output a single string — the de-roled coach system prompt template — no JSON wrapping, no
markdown fences.

Rules:
- Replace ALL hardcoded job titles (e.g. "Relationship Manager", "analyst", "underwriter")
  with {{role}}
- Replace ALL hardcoded organization names (EDC, Meridian Corp, etc.) with {{organisation}}
- Replace ALL hardcoded programme/project names (Meridian Infrastructure Briefing, Aurora
  Initiative, Cascade Portfolio, Enterprise Intelligence Program) with {{scenario_name}}
- Replace explicit domain references with {{domain}} ONLY if domain-general
- Preserve ALL coaching logic, rubric guidance, and instructional tone exactly
- Return only the template string
"""

ROLE_HINT_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Write a brief role variants hint for this AI capability module. The hint guides the runtime
scenario generator on how to adapt the module's context for different professional roles.

<scenario_text>
{scenario_text}
</scenario_text>

<concept_text>
{concept_text}
</concept_text>

Output a single string of 1–2 sentences — no JSON wrapping, no markdown fences.

Rules:
- Identify the 2–3 most role-sensitive elements (data types, stakeholders, workflows)
- For each, give a brief adaptation note for 2–3 different role contexts
- Format: "For [role type 1]: [adaptation note]. For [role type 2]: [adaptation note]."
- Mention which {{}} placeholders are most important to fill accurately for this module
- Return only the hint string
"""

INTRO_DEROLE_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

The following intro sentence(s) may begin with role-specific framing ("As an analyst...",
"As a Relationship Manager..."). Rewrite only the role-specific opening to be role-agnostic
while keeping all meaning and context intact.

<intro>
{intro}
</intro>

Output a single string — the updated intro — no JSON wrapping, no markdown fences.

Rules:
- Replace role-specific openings: "As an analyst" → "As a professional";
  "As a Relationship Manager" → "In your professional work"; etc.
- Do NOT change any framework explanation or examples
- If the intro is already role-agnostic, return it unchanged
- Return only the updated string
"""

# ---------------------------------------------------------------------------
# AI extraction helpers
# ---------------------------------------------------------------------------

def _get_token() -> str:
    """Get a fresh OAuth token via the Databricks CLI."""
    import subprocess
    result = subprocess.run(
        ["databricks", "auth", "token", "--host", DATABRICKS_HOST, "--profile", "dev"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        # Fall back to DATABRICKS_TOKEN env var
        token = os.environ.get("DATABRICKS_TOKEN", "")
        if not token:
            raise RuntimeError(f"Could not get Databricks token: {result.stderr}")
        return token
    return json.loads(result.stdout)["access_token"]


# Module-level token cache (refreshed once per run)
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
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return text


def _extract_json(prompt: str):
    """Call LLM and parse JSON response."""
    text = _call_llm(prompt)
    return json.loads(text)


def _extract_text(prompt: str) -> str:
    """Call LLM and return plain text response."""
    return _call_llm(prompt)


# ---------------------------------------------------------------------------
# Atom assembly
# ---------------------------------------------------------------------------

def _assemble_atom(
    course_id: str,
    course: dict,
    scenario: dict,
    reading_s: dict | None,
    reading_f: dict,
    tags,
    scenario_template: str | None,
    task_templates,
    coach_template: str | None,
    role_hint: str | None,
    intro_derolled: str | None,
) -> dict:
    """Assemble a complete atom dict from the 6 LLM call outputs."""

    # reading.concept: prefer structured, fall back to flat
    if reading_s and reading_s.get("concept_text_structured"):
        cs = reading_s["concept_text_structured"]
        concept = {
            "framework_acronym": cs.get("framework_acronym"),
            "intro": intro_derolled,
            "cards": cs.get("cards", []),
            "guardrails": cs.get("guardrails", []),
        }
    else:
        concept = {"intro": intro_derolled}

    # Build task_templates with mcq_options merged in
    mcq_opts_raw = scenario.get("task_mcq_options") or [None, None, None, None]
    if task_templates:
        merged_tasks = []
        for i, task in enumerate(task_templates):
            mcq_options = mcq_opts_raw[i] if i < len(mcq_opts_raw) else None
            merged_tasks.append({
                "task_id": task.get("task_id", i + 1),
                "task_mode": (scenario.get("task_modes") or ["open", "mcq", "mcq", "mcq"])[i]
                    if i < len(scenario.get("task_modes") or []) else ("open" if i == 0 else "mcq"),
                "text_template": task.get("text_template"),
                "skill_focus": task.get("skill_focus"),
                "mcq_options": mcq_options,
            })
    else:
        merged_tasks = None

    return {
        "atom_id": f"{course['primary_domain']}__{course_id}",
        "title": course.get("title"),
        "domain": course.get("primary_domain"),
        "capability_tags": tags,
        "estimated_minutes": 30,
        "role_variants_hint": role_hint,
        "reading": {
            "concept": concept,
            "good_example": reading_f.get("good_example"),
            "anti_pattern": reading_f.get("anti_pattern"),
            "takeaway": reading_f.get("takeaway"),
        },
        "practice": {
            "scenario_template": scenario_template,
            "task_modes": scenario.get("task_modes", ["open", "mcq", "mcq", "mcq"]),
            "task_templates": merged_tasks,
            "task_mcq_options": scenario.get("task_mcq_options"),
            "coach_system_prompt_template": coach_template,
        },
        "eval": {
            "items_ref": "evaluation_items.json",
            "source_course_ids": [course_id],
        },
        "source_course_ids": [course_id],
        "atomized_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "status": "draft",
    }


# ---------------------------------------------------------------------------
# Per-course atomization
# ---------------------------------------------------------------------------

def atomize_course(
    course_id: str,
    course: dict,
    scenario: dict,
    reading_s: dict | None,
    reading_f: dict,
) -> tuple[str, dict]:
    """Run 6 sequential LLM calls for one course and return (course_id, atom)."""

    def safe_call(label: str, fn):
        try:
            result = fn()
            print(f"  ✓ [{course_id}] {label}")
            return result
        except Exception as exc:
            print(f"  WARN [{course_id}] {label}: {exc}", file=sys.stderr)
            return None

    # Prepare concept_text for prompts that need it
    if reading_s and reading_s.get("concept_text_structured"):
        concept_text = reading_s["concept_text_structured"].get("intro", "")
    else:
        concept_text = reading_f.get("concept_text", "")

    # Get framework_acronym from structured reading if available
    framework_acronym = ""
    if reading_s and reading_s.get("concept_text_structured"):
        framework_acronym = reading_s["concept_text_structured"].get("framework_acronym") or ""

    # Call 1 — TAG_EXTRACTION
    tags = safe_call("TAG_EXTRACTION", lambda: _extract_json(TAG_EXTRACTION_PROMPT.format(
        title=course.get("title", ""),
        description=course.get("description", ""),
        real_use_case=course.get("real_use_case", ""),
        framework_acronym=framework_acronym,
        framework_acronym_lower=framework_acronym.lower(),
    )))

    # Call 2 — SCENARIO_TEMPLATE
    scenario_template = safe_call("SCENARIO_TEMPLATE", lambda: _extract_text(SCENARIO_TEMPLATE_PROMPT.format(
        scenario_text=scenario.get("scenario_text", ""),
    )))

    # Call 3 — TASK_GENERALIZATION
    task_templates = safe_call("TASK_GENERALIZATION", lambda: _extract_json(TASK_GENERALIZATION_PROMPT.format(
        task_1_text=scenario.get("task_1_text", ""),
        task_2_text=scenario.get("task_2_text", ""),
        task_3_text=scenario.get("task_3_text", ""),
        task_4_text=scenario.get("task_4_text", ""),
    )))

    # Call 4 — COACH_GENERALIZATION
    coach_template = safe_call("COACH_GENERALIZATION", lambda: _extract_text(COACH_GENERALIZATION_PROMPT.format(
        coach_system_prompt=scenario.get("coach_system_prompt", ""),
    )))

    # Call 5 — ROLE_HINT
    role_hint = safe_call("ROLE_HINT", lambda: _extract_text(ROLE_HINT_PROMPT.format(
        scenario_text=scenario.get("scenario_text", ""),
        concept_text=concept_text,
    )))

    # Call 6 — INTRO_DEROLE
    # Source: structured intro if available, else first 2 sentences of flat concept_text
    if reading_s and reading_s.get("concept_text_structured"):
        raw_intro = reading_s["concept_text_structured"].get("intro", concept_text)
    else:
        sentences = concept_text.split(". ")
        raw_intro = ". ".join(sentences[:2]) + ("." if len(sentences) > 2 else "")

    intro_derolled = safe_call("INTRO_DEROLE", lambda: _extract_text(INTRO_DEROLE_PROMPT.format(
        intro=raw_intro,
    )))

    atom = _assemble_atom(
        course_id, course, scenario, reading_s, reading_f,
        tags, scenario_template, task_templates, coach_template,
        role_hint, intro_derolled,
    )
    return course_id, atom


# ---------------------------------------------------------------------------
# Overlap detection
# ---------------------------------------------------------------------------

def _detect_overlap(atoms: list[dict]) -> dict:
    """Complete-link agglomerative clustering on capability_tags (domain-scoped)."""

    def jaccard(a, b):
        sa, sb = set(a or []), set(b or [])
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)

    # Build pairwise similarity for same-domain pairs
    pairs = []
    for a, b in combinations(atoms, 2):
        if a["domain"] != b["domain"]:
            continue
        score = jaccard(a.get("capability_tags"), b.get("capability_tags"))
        if score >= 0.05:
            pairs.append((a["atom_id"], b["atom_id"], score))

    def complete_link_groups(pairs, threshold):
        candidates = {}
        for a, b, s in pairs:
            if s >= threshold:
                key = (min(a, b), max(a, b))
                candidates[key] = s

        atom_ids = list({aid for a, b, _ in pairs for aid in (a, b)})

        groups = []
        visited = set()
        for atom_id in atom_ids:
            if atom_id in visited:
                continue
            group = {atom_id}
            changed = True
            while changed:
                changed = False
                for (a, b), score in list(candidates.items()):
                    if a in group or b in group:
                        candidate = b if a in group else a
                        if candidate in group or candidate in visited:
                            continue
                        # Complete-link: candidate must exceed threshold with ALL in group
                        if all(
                            candidates.get((min(m, candidate), max(m, candidate)), 0) >= threshold
                            for m in group
                        ):
                            group.add(candidate)
                            changed = True
            if len(group) > 1:
                group_sorted = sorted(group)
                groups.append(group_sorted)
            # Mark all atoms in group as visited (even singletons) to prevent
            # them from appearing in later groups
            visited.update(group)

        return groups

    # Empirically, same-framework atoms share ~1 tag out of 11 possible (Jaccard ≈ 0.09).
    # The 0.70 threshold assumed tag convergence that doesn't happen across role-specific
    # generative runs. 0.08 captures any pair sharing at least the framework tag (the
    # only guaranteed cross-role invariant when all 4 variants teach the same framework).
    merge_groups = complete_link_groups(pairs, threshold=0.08)
    review_pairs = [(a, b, s) for a, b, s in pairs if 0.05 <= s < 0.08]

    atom_map = {a["atom_id"]: a for a in atoms}

    merge_candidates = []
    for group in merge_groups:
        domain = atom_map[group[0]]["domain"]
        source_ids = [sid for aid in group for sid in atom_map[aid].get("source_course_ids", [])]
        pairwise = [
            jaccard(atom_map[a].get("capability_tags"), atom_map[b].get("capability_tags"))
            for a, b in combinations(group, 2)
        ]
        merge_candidates.append({
            "domain": domain,
            "atom_ids": group,
            "source_course_ids": source_ids,
            "min_pairwise_score": round(min(pairwise), 2),
            "avg_pairwise_score": round(sum(pairwise) / len(pairwise), 2),
        })

    review_flags = [
        {"atom_a": a, "atom_b": b, "jaccard_score": round(s, 2)}
        for a, b, s in review_pairs
    ]

    return {
        "merge_candidates": merge_candidates,
        "review_flags": review_flags,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Dry-run pretty-print
# ---------------------------------------------------------------------------

def _print_atom_summary(course_id: str, atom: dict) -> None:
    """Print human-readable summary of one atom."""
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"─── {course_id} {'─' * max(0, 50 - len(course_id))}")
    print(f"{sep}")

    print(f"atom_id         : {atom.get('atom_id')}")
    print(f"domain          : {atom.get('domain')}")

    tags = atom.get("capability_tags") or []
    print(f"capability_tags : {json.dumps(tags)}")

    concept = (atom.get("reading") or {}).get("concept") or {}
    intro = concept.get("intro", "")
    intro_preview = intro[:80] + ("..." if len(intro) > 80 else "")
    print(f"intro (derolled): {intro_preview}")

    cards = concept.get("cards") or []
    letters = [c.get("letter", "?") for c in cards]
    print(f"cards           : {len(cards)} items ({', '.join(letters)})")

    guardrails = concept.get("guardrails") or []
    print(f"guardrails      : {len(guardrails)} items")

    scenario_tmpl = (atom.get("practice") or {}).get("scenario_template") or ""
    tmpl_preview = scenario_tmpl[:80] + ("..." if len(scenario_tmpl) > 80 else "")
    print(f"scenario_tmpl   : {tmpl_preview}")

    task_modes = (atom.get("practice") or {}).get("task_modes") or []
    print(f"task_modes      : {json.dumps(task_modes)}")

    task_templates = (atom.get("practice") or {}).get("task_templates") or []
    skill_focuses = [t.get("skill_focus", "?") for t in task_templates]
    print(f"tasks           : {len(task_templates)} items — skill_focus: {skill_focuses}")

    mcq_opts = (atom.get("practice") or {}).get("task_mcq_options") or []
    for i, opts in enumerate(mcq_opts):
        if opts:
            best = next((o.get("label", "?") for o in opts if o.get("is_best")), "none")
            print(f"mcq_options     : T{i + 1}: {len(opts)} options (best: \"{best[:60]}\")")

    coach_tmpl = (atom.get("practice") or {}).get("coach_system_prompt_template") or ""
    bad_words = ["analyst", "Relationship Manager", "underwriter",
                 "Meridian Infrastructure Briefing", "Aurora Initiative",
                 "Cascade Portfolio", "Enterprise Intelligence Program"]
    found_bad = [w for w in bad_words if w.lower() in coach_tmpl.lower()]
    checks = " ".join(
        [f"(no \"{w}\" ✓)" for w in ["analyst", "Meridian Infrastructure Briefing", "Aurora Initiative"]
         if w.lower() not in coach_tmpl.lower()]
    )
    if found_bad:
        checks += f" WARN: found {found_bad}"
    print(f"coach_tmpl      : {checks or '(template present)'}")

    role_hint = atom.get("role_variants_hint") or ""
    hint_preview = role_hint[:80] + ("..." if len(role_hint) > 80 else "")
    print(f"role_hint       : {hint_preview}")

    null_fields = [k for k in ["capability_tags", "role_variants_hint"] if not atom.get(k)]
    print(f"null_fields     : {null_fields}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Pretty-print to stdout; do not write files")
    parser.add_argument("--course-id", help="Process only this course_id")
    args = parser.parse_args()

    # Load source data
    def load(name: str) -> dict:
        path = CONTENT_DIR / name
        if not path.exists():
            sys.exit(f"ERROR: {path} not found")
        return json.loads(path.read_text(encoding="utf-8"))

    courses = load("courses.json")
    practice_scenarios = load("practice_scenarios.json")
    reading_flat = load("reading_content.json")

    structured_path = CONTENT_DIR / "reading_content_structured.json"
    reading_structured: dict = {}
    if structured_path.exists():
        reading_structured = json.loads(structured_path.read_text(encoding="utf-8"))

    # Filter to single course if requested
    if args.course_id:
        if args.course_id not in courses:
            sys.exit(f"ERROR: course_id '{args.course_id}' not in courses.json")
        courses = {args.course_id: courses[args.course_id]}

    print(f"Processing {len(courses)} course(s) with up to {MAX_WORKERS} workers...")

    # Warm up token cache before spawning threads (avoids races on first fetch)
    try:
        _token()
        print(f"  Auth: OK (token cached)")
    except Exception as exc:
        sys.exit(f"ERROR: Could not authenticate with Databricks: {exc}")

    results: dict[str, dict] = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(
                atomize_course,
                cid,
                course,
                practice_scenarios.get(cid, {}),
                reading_structured.get(cid),
                reading_flat.get(cid, {}),
            ): cid
            for cid, course in courses.items()
        }
        for future in as_completed(futures):
            course_id = futures[future]
            try:
                cid, atom = future.result()
                results[cid] = atom
                print(f"  Done: {cid}")
            except Exception as exc:
                print(f"  ERROR [{course_id}]: {exc}", file=sys.stderr)

    # Sort atoms by course_id for deterministic output
    atoms = [results[cid] for cid in sorted(results.keys())]

    if args.dry_run:
        print("\n=== DRY RUN — per-atom summary ===")
        for cid in sorted(results.keys()):
            _print_atom_summary(cid, results[cid])
        print(f"\nTotal atoms: {len(atoms)}")
        return

    # Write atomic_modules.json
    modules_path = CONTENT_DIR / "atomic_modules.json"
    modules_path.write_text(json.dumps(atoms, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(atoms)} atoms to {modules_path}")

    # Detect overlap (domain atoms only; capstones excluded)
    if not args.course_id:
        domain_atoms = [a for a in atoms if a.get("source_course_ids", [""])[0] not in CAPSTONE_IDS]
        overlap_report = _detect_overlap(domain_atoms)

        report_path = CONTENT_DIR / "atomic_overlap_report.json"
        report_path.write_text(json.dumps(overlap_report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote overlap report to {report_path}")
        print(f"  {len(overlap_report['merge_candidates'])} merge candidate groups")
        print(f"  {len(overlap_report['review_flags'])} review flags")
    else:
        print("(Overlap detection skipped for single-course runs)")


if __name__ == "__main__":
    main()
