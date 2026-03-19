# Plan: Atomic Coursework Conversion Pipeline (Phase 0.5)

**Status**: READY TO IMPLEMENT
**Branch**: `feature/atomize-coursework`
**Scope**: `scripts/atomize_coursework.py` (new) + output files `content/atomic_modules.json` + `content/atomic_overlap_report.json`
**ADR Reference**: `plans/master-architecture.md` (full architectural rationale)

---

## Product Vision

The end goal is a product that can serve **any professional role** given a LinkedIn profile
(or equivalent self-description), with no hardcoded role list. The six-domain hexagon model
is already profession-agnostic — it measures AI literacy, not finance skills. The only thing
tying it to specific roles was the content framing. Atomization strips that framing out.

**The full any-role pipeline (across phases):**

```text
LinkedIn profile
    → extract: job_title, industry, company_type, seniority
    → map to:  {role}, {org_type}, {case_type}, {sensitivity_level}
    → run diagnostic (templatized items, domain-scoped not role-scoped)
    → score 6 domains
    → sequence 28+ atoms by gap priority
    → instantiate atom templates at render time with profile values
    → AI coach addresses "Senior Credit Analyst at a regional bank"
       not a hardcoded "Relationship Manager at EDC"
```

A supply chain manager, HR business partner, product manager, or civil engineer all get a
fully personalised AI skills curriculum from the same atom library.

**Four gaps between Phase 0.5 and the any-role vision** (later phases, not this script):

| Gap | Phase | Work |
| --- | --- | --- |
| Diagnostic items are still role-hardcoded | 0.6 | Same templatization treatment as practice scenarios |
| Domain keys are role-scoped (`rm_prompting`) | 0.7 | Universal domain schema; instantiated with learner role |
| No runtime placeholder instantiation layer | 0.7 | `instantiate_atom(atom, profile)` ~50 lines |
| Role selection UI → LinkedIn onboarding | 1 | LinkedIn OAuth or manual title+industry entry |

Phase 0.5 (this script) closes none of those gaps directly, but makes all four tractable
by producing a clean, templatized content store.

---

## Purpose

Phase 0.5 converts the 28 existing RM/UW/AN/MK modules into role-agnostic **atomic** modules
stored in `content/atomic_modules.json`. The app DOES NOT change — it keeps reading from
the original JSON files throughout. The output is a parallel data store ready for Phase 0.6
(diagnostic templatization), Phase 1 (PM + Engineer atoms), and Phase 3 (path assembler
activation).

---

## Architecture Decision

**Why a separate atomization script, not modifying original content:**

- Original JSON files stay pristine — no regression risk
- Atomization is a one-time batch process, not a generation step
- `atomic_modules.json` is self-contained: no runtime dependency on original files
- The same script re-runs on PM + Engineer content in Phase 1 without modification

**Data flow:**

```text
content/courses.json                    ─┐
content/practice_scenarios.json         ─┤
content/reading_content_structured.json ─┤──→ scripts/atomize_coursework.py ──→ content/atomic_modules.json
content/reading_content.json (fallback) ─┘   (6 Sonnet calls per course)        content/atomic_overlap_report.json
                                              28 courses: 7 RM + 7 UW + 7 AN + 7 MK
```

**Capstone handling**: all 4 capstone courses (`rm_c7_capstone`, `uw_c7_capstone`, `an_c7_capstone`,
`mk_c7_capstone`) have `primary_domain = "responsible_ai"` in `courses.json`. They must be processed
by the pipeline but **excluded from overlap detection** — capstones are integrative courses, not
domain-specific, and will produce false-positive clusters with `*_c1_responsible_ai` domain courses.
The script must filter them out before computing Jaccard groups:

```python
CAPSTONE_IDS = {"rm_c7_capstone", "uw_c7_capstone", "an_c7_capstone", "mk_c7_capstone"}
domain_atoms = [a for a in atoms if a["source_course_ids"][0] not in CAPSTONE_IDS]
# overlap detection runs on domain_atoms only (24 atoms)
```

**Source file structure (all dicts keyed by `course_id`):**

```python
courses            = {course_id: {role_id, primary_domain, title, description, real_use_case, ...}}
practice_scenarios = {course_id: {scenario_text, task_1_text...task_4_text, coach_system_prompt,
                                   task_modes,          # ["open", "mcq", "mcq", "mcq"]
                                   task_mcq_options}}   # [null, [{label, is_best}, ...], ...]
reading_structured = {course_id: {concept_text_structured: {framework_acronym, intro, cards[], guardrails[]},
                                   good_example_structured: {...}, ...}}
reading_flat       = {course_id: {concept_text, good_example, anti_pattern, takeaway}}
```

Join is direct: `reading_structured.get(course_id)` — fall back to `reading_flat[course_id]` if absent.

**`task_mcq_options` is a 4-element list**: index 0 = `null` (Task 1 is open mode),
indices 1–3 = list of 3 `{label: str, is_best: bool}` objects. Copy as-is into atom — labels are
already role-agnostic action phrases (no job-title references).

---

## Atomic JSON Schema

Each atom is a COMPLETE, self-contained object — no lookups into original files at runtime.

```json
{
  "atom_id": "responsible_ai__rm_course_1",
  "title": "Safe AI Prompting: The SAFE Abstraction Method",
  "domain": "responsible_ai",
  "capability_tags": ["SAFE_framework", "data_classification", "prompt_abstraction", "data_privacy"],
  "estimated_minutes": 30,
  "role_variants_hint": "For financial services: emphasize client data (KYC, credit files, NPI). For engineering: emphasize code secrets and API credentials. Adjust {data_type} and {compliance_context} accordingly.",
  "reading": {
    "concept": {
      "framework_acronym": "SAFE",
      "intro": "...",          // de-roled by Call 6 (e.g. "As an analyst" → "As a professional")
      "cards": [               // copied as-is from structured; already role-agnostic at card level
        {"letter": "S", "title": "Scrutinize", "body": "..."},
        {"letter": "A", "title": "Abstract",   "body": "..."},
        {"letter": "F", "title": "Filter",     "body": "..."},
        {"letter": "E", "title": "Ensure",     "body": "..."}
      ],
      "guardrails": ["...", "..."]   // copied as-is from structured
    },
    "good_example": "...",     // flat, copied as-is — fictional orgs already generic
    "anti_pattern": "...",     // flat, copied as-is
    "takeaway": "..."          // flat, copied as-is
  },
  "practice": {
    "scenario_template": "You are a {role} at {org_type}. ...",
    "task_modes": ["open", "mcq", "mcq", "mcq"],
    "task_templates": [
      {
        "task_id": 1,
        "task_mode": "open",
        "text_template": "...",
        "skill_focus": "Apply SAFE Step 1: Scrutinize sensitive elements",
        "mcq_options": null
      },
      {
        "task_id": 2,
        "task_mode": "mcq",
        "text_template": "...",
        "skill_focus": "...",
        "mcq_options": [
          {"label": "...", "is_best": true},
          {"label": "...", "is_best": false},
          {"label": "...", "is_best": false}
        ]
      }
    ],
    "coach_system_prompt_template": "..."
  },
  "eval": {
    "items_ref": "evaluation_items.json",
    "source_course_ids": ["rm_course_1"]
  },
  "source_course_ids": ["rm_course_1"],
  "atomized_at": "2026-03-16",
  "status": "draft"
}
```

**Fallback for reading**: if `reading_content_structured.json` has no entry for a course,
store `reading.concept` as `{"intro": "<de-roled concept_text>"}` (flat fallback).

### Atom ID convention

**Phase 0.5** (this script): `{domain}__{course_id}` — full course_id preserves traceability.

**Phase 2** (post-merge): `{domain}__{framework_or_key_skill}` — canonical library names.

### Placeholder naming convention (consistent across ALL atoms)

| Placeholder | Meaning |
| --- | --- |
| `{role}` | Learner's job title |
| `{org_type}` | Organization type |
| `{case_type}` | Type of work case |
| `{data_types}` | Data present |
| `{sensitivity_level}` | Data classification |
| `{workflow_goal}` | Task objective |
| `{programme_name}` | Project/programme name |
| `{audience}` | Target audience |
| `{organisation}` | Learner's fictional org name (coach prompt only) |
| `{scenario_name}` | Name of the practice scenario (coach prompt only) |
| `{domain}` | AI skill domain (coach prompt only) |

---

## Extraction Prompts (6 calls per course, `databricks-claude-sonnet-4-6`, temperature=0)

### Call 1 — TAG_EXTRACTION

**Input**: `courses[course_id]` → `title`, `description`, `real_use_case`
**Output key**: `capability_tags` (JSON array, 3–6 strings)

```python
TAG_EXTRACTION_PROMPT = """\
You are a content structuring assistant for an AI skills learning platform.

Extract 3–6 capability tags from the following course metadata. Tags identify the core AI
skill or framework taught in this module. They are used to match learners to relevant
content based on their role and pain points.

<title>{title}</title>
<description>{description}</description>
<real_use_case>{real_use_case}</real_use_case>

Output a single JSON array of lowercase, underscore-separated strings — no prose, no
markdown fences:
["tag_one", "tag_two", ...]

Rules:
- 3–6 tags per module
- Include: (1) the named framework/method taught (e.g. "SAFE_framework", "CRAF_method"),
  (2) the key skill domain, (3) 1–2 specific capabilities
- Do NOT include generic tags like "ai_usage" or "professional_development"
- Return only the JSON array
"""
```

### Call 2 — SCENARIO_TEMPLATE

**Input**: `practice_scenarios[course_id]` → `scenario_text`
**Output key**: `practice.scenario_template` (plain string)

```python
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
```

### Call 3 — TASK_GENERALIZATION

**Input**: `practice_scenarios[course_id]` → `task_1_text` through `task_4_text`
**Output key**: `practice.task_templates` (JSON array of 4 objects)

```python
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
```

### Call 4 — COACH_GENERALIZATION

**Input**: `practice_scenarios[course_id]` → `coach_system_prompt`
**Output key**: `practice.coach_system_prompt_template` (plain string)

```python
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
```

### Call 5 — ROLE_HINT

**Input**: `practice_scenarios[course_id]` → `scenario_text`; structured or flat `concept_text`
**Output key**: `role_variants_hint` (plain string)

```python
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
```

### Call 6 — INTRO_DEROLE

**Input**: structured `intro` field from `reading_content_structured[course_id].concept_text_structured.intro`;
falls back to first 2 sentences of flat `concept_text` if structured absent.
**Output key**: `reading.concept.intro` (plain string; `cards[]` and `guardrails[]` copied as-is)

```python
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
```

---

## Script Design: `scripts/atomize_coursework.py`

**Scope**: dev-time batch script only — not deployed to Cloud Run. The app itself runs on
GCP/Gemini (post phase-d migration). This script runs locally against the Databricks serving
endpoints, exactly like `scripts/enrich_reading_content.py`, and writes static output files
that are committed and bundled with the app.

**SDK pattern**: same as `scripts/enrich_reading_content.py` — `WorkspaceClient`, `tenacity`
retries, `ThreadPoolExecutor`, temperature=0.0 on all calls.

**Model**: `SONNET_ENDPOINT = os.environ.get("SONNET_ENDPOINT", "databricks-claude-sonnet-4-6")`

**Why Sonnet, not Haiku**: `enrich_reading_content.py` uses Haiku for purely extractive
structured parsing (card/guardrail extraction from existing text). This script must perform
genuine de-roling and re-writing (Calls 2–6) — replacing implicit role framing, inferring
placeholder boundaries, generating role-adaptive hints. That requires stronger instruction
following. Sonnet is justified; Haiku would produce inconsistent placeholder coverage.

**Concurrency**: `ThreadPoolExecutor(max_workers=4)` — concurrent across courses;
6 calls sequential within each course.

**Error handling**: if any single call fails after 3 retries, log warning and set that key
to `null`. Never abort the whole run.

**Atom assembly** (after 6 calls):

```python
def _assemble_atom(course_id, course, scenario, reading_s, reading_f,
                   tags, scenario_template, task_templates, coach_template,
                   role_hint, intro_derolled):

    # reading.concept: prefer structured, fall back to flat
    if reading_s:
        concept = {
            "framework_acronym": reading_s["concept_text_structured"].get("framework_acronym"),
            "intro": intro_derolled,                                    # de-roled by Call 6
            "cards": reading_s["concept_text_structured"].get("cards", []),    # as-is
            "guardrails": reading_s["concept_text_structured"].get("guardrails", []),
        }
    else:
        concept = {"intro": intro_derolled}  # flat fallback

    return {
        "atom_id": f"{course['primary_domain']}__{course_id}",
        "title": course["title"],
        "domain": course["primary_domain"],
        "capability_tags": tags,
        "estimated_minutes": 30,
        "role_variants_hint": role_hint,
        "reading": {
            "concept": concept,
            "good_example": reading_f["good_example"],   # flat, as-is
            "anti_pattern": reading_f["anti_pattern"],   # flat, as-is
            "takeaway": reading_f["takeaway"],            # flat, as-is
        },
        "practice": {
            "scenario_template": scenario_template,
            "task_modes": scenario.get("task_modes", ["open", "mcq", "mcq", "mcq"]),
            "task_templates": task_templates,   # text_template + skill_focus per task (Call 3)
            "task_mcq_options": scenario.get("task_mcq_options"),  # copied as-is; labels are role-agnostic
            "coach_system_prompt_template": coach_template,
        },
        "eval": {
            "items_ref": "evaluation_items.json",
            "source_course_ids": [course_id],
        },
        "source_course_ids": [course_id],
        "atomized_at": datetime.utcnow().strftime("%Y-%m-%d"),
        "status": "draft",
    }
```

**CLI interface:**

```bash
python scripts/atomize_coursework.py                                # all 21 courses
python scripts/atomize_coursework.py --dry-run                      # pretty-print to stdout, no write
python scripts/atomize_coursework.py --course-id an_c1_responsible_ai  # single course test
```

**Dry-run output format** (human-readable, per atom):

```text
─── rm_c1_responsible_ai ──────────────────────────────────────────
atom_id         : responsible_ai__rm_c1_responsible_ai
domain          : responsible_ai
capability_tags : ["SAFE_framework", "data_classification", "prompt_abstraction", "data_privacy"]
intro (derolled): As a professional working with confidential client files...
cards           : 4 items (S, A, F, E)
guardrails      : 5 items
scenario_tmpl   : You are a {role} at {org_type}. A {case_type} has been opened...
task_modes      : ["open", "mcq", "mcq", "mcq"]
tasks           : 4 items — skill_focus: [Apply SAFE Step 1, ...]
mcq_options     : T2: 3 options (best: "Replace all client-specific figures with directional ranges")
                  T3: 3 options (best: "Rewrite using only sector-level descriptors...")
                  T4: 3 options (best: "Apply all four SAFE steps and add explicit output constraints")
coach_tmpl      : (no "analyst" ✓) (no "Meridian Infrastructure Briefing" ✓) (no "Aurora Initiative" ✓)
role_hint       : For financial services: ... For engineering: ...
null_fields     : []
```

---

## Overlap Detection

**Algorithm**: complete-link agglomerative clustering on `capability_tags`.
Every pair in a merge group must exceed the Jaccard threshold with each other —
no chaining (A~B + B~C does NOT imply A, B, C merge unless A~C also exceeds threshold).

**Why complete-link**: single-link (greedy transitive) produces chaining artifacts and is
considered harmful for content deduplication. Complete-link ensures merge groups are
semantically cohesive — all members teach the same underlying capability.

**Two tiers:**

| Tier | Jaccard threshold | Action |
| --- | --- | --- |
| Merge candidate | ≥ 0.70 | Flag for Phase 2 merge |
| Review flag | 0.40–0.69 | Flag for human review; may share sub-skills |
| Distinct | < 0.40 | No flag |

```python
def _detect_overlap(atoms: list[dict]) -> dict:
    """Complete-link agglomerative clustering on capability_tags."""
    from itertools import combinations

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
        if score >= 0.40:
            pairs.append((a["atom_id"], b["atom_id"], score))

    # Complete-link grouping: a group forms only if ALL pairs within it exceed threshold
    def complete_link_groups(pairs, threshold):
        candidates = {(a, b): s for a, b, s in pairs if s >= threshold}
        atom_ids = list({aid for a, b, _ in pairs for aid in (a, b)})

        groups = []
        visited = set()
        for atom_id in atom_ids:
            if atom_id in visited:
                continue
            # Start a new group with this atom
            group = {atom_id}
            changed = True
            while changed:
                changed = False
                for a, b in list(candidates.keys()):
                    if a in group or b in group:
                        candidate = b if a in group else a
                        # Complete-link check: candidate must exceed threshold with ALL in group
                        if all(
                            candidates.get((min(m, candidate), max(m, candidate)), 0) >= threshold
                            or candidates.get((min(candidate, m), max(candidate, m)), 0) >= threshold
                            for m in group
                        ):
                            if candidate not in group:
                                group.add(candidate)
                                changed = True
            if len(group) > 1:
                groups.append(sorted(group))
                visited.update(group)

        return groups

    merge_groups = complete_link_groups(pairs, threshold=0.70)
    review_pairs = [(a, b, s) for a, b, s in pairs if 0.40 <= s < 0.70]

    # Build output with domain and source_course_ids
    atom_map = {a["atom_id"]: a for a in atoms}

    merge_candidates = []
    for group in merge_groups:
        domain = atom_map[group[0]]["domain"]
        source_ids = [sid for aid in group for sid in atom_map[aid]["source_course_ids"]]
        scores = [
            jaccard(atom_map[a].get("capability_tags"), atom_map[b].get("capability_tags"))
            for a, b in combinations(group, 2)
        ]
        merge_candidates.append({
            "domain": domain,
            "atom_ids": group,
            "source_course_ids": source_ids,
            "min_pairwise_score": round(min(scores), 2),
            "avg_pairwise_score": round(sum(scores) / len(scores), 2),
        })

    review_flags = [
        {"atom_a": a, "atom_b": b, "jaccard_score": round(s, 2)}
        for a, b, s in review_pairs
    ]

    return {
        "merge_candidates": merge_candidates,
        "review_flags": review_flags,
        "generated_at": datetime.utcnow().isoformat(),
    }
```

**Expected output (28 modules: 24 domain atoms + 4 capstone atoms; capstones excluded from overlap):**

- 6 merge candidate groups (one per domain: RM + UW + AN + MK versions of same framework)
- Each group: 4 atoms, all pairwise Jaccard ≥ 0.70
- Capstone atoms present in `atomic_modules.json` but absent from overlap report (filtered by `CAPSTONE_IDS`)
- 0 chaining artifacts

---

## Validation

```bash
# Step 1: test single item (dry run) — use rm_c1 as canonical test case
python scripts/atomize_coursework.py --dry-run --course-id rm_c1_responsible_ai

# Spot-check dry-run output:
# - capability_tags: 3–6 items, includes framework name (e.g. "SAFE_framework")
# - intro (derolled): no "As an analyst" or "As a Relationship Manager"
# - cards: 4 items with letter/title/body
# - scenario_template: contains {role} and {org_type}
# - task_modes: ["open", "mcq", "mcq", "mcq"]
# - task_templates: 4 items with text_template + skill_focus
# - mcq_options: T2–T4 show 3 options each with exactly 1 is_best
# - coach_tmpl: no hardcoded "EDC", "analyst", "Meridian Infrastructure Briefing"
# - role_hint: mentions 2 role types

# Step 2: if single item looks good, run all 28
python scripts/atomize_coursework.py

# Step 3: verify atomic_modules.json
python -c "
import json
atoms = json.load(open('content/atomic_modules.json'))
print(f'{len(atoms)} atoms generated:')
for a in atoms:
    tags = len(a.get('capability_tags') or [])
    has_role = '{role}' in (a.get('practice', {}).get('scenario_template') or '')
    has_org = '{org_type}' in (a.get('practice', {}).get('scenario_template') or '')
    has_cards = len((a.get('reading', {}).get('concept') or {}).get('cards') or [])
    mcq_opts = a.get('practice', {}).get('task_mcq_options') or []
    mcq_ok = (len(mcq_opts) == 4 and mcq_opts[0] is None
              and all(len(o) == 3 and sum(x['is_best'] for x in o) == 1
                      for o in mcq_opts[1:] if o))
    null_fields = [k for k in ['capability_tags','role_variants_hint'] if not a.get(k)]
    ok = '✓' if (has_role and has_org and tags >= 3 and mcq_ok) else '✗'
    print(f'  {ok} {a[\"atom_id\"]}: {tags} tags, {has_cards} cards, mcq={mcq_ok}, nulls={null_fields}')
"

# Step 4: verify overlap report
python -c "
import json
report = json.load(open('content/atomic_overlap_report.json'))
print(f'{len(report[\"merge_candidates\"])} merge candidate groups:')
for g in report['merge_candidates']:
    print(f'  {g[\"domain\"]} | min={g[\"min_pairwise_score\"]} avg={g[\"avg_pairwise_score\"]} | {len(g[\"atom_ids\"])} atoms: {g[\"atom_ids\"]}')
print(f'{len(report[\"review_flags\"])} review flags (0.40-0.69 overlap)')
"
```

---

## Acceptance Criteria

- [ ] `content/atomic_modules.json` has exactly 28 entries (7 RM + 7 UW + 7 AN + 7 MK)
- [ ] Every atom has `capability_tags` (3–6 items, no nulls)
- [ ] Every atom's `practice.scenario_template` contains `{role}` and `{org_type}`
- [ ] Every atom's `practice.coach_system_prompt_template` has no hardcoded role titles ("analyst", "Relationship Manager", "underwriter") or fictional programme names ("Meridian Infrastructure Briefing", "Aurora Initiative", "Cascade Portfolio", "Enterprise Intelligence Program") — note: "EDC" was already sanitized from all source content (commit `99383c2`) so residual EDC references would indicate a prompt regression
- [ ] Every atom from a structured-reading course has `reading.concept.cards` with ≥ 2 items
- [ ] Every atom's `practice.task_modes` == `["open", "mcq", "mcq", "mcq"]`
- [ ] Every atom's `practice.task_mcq_options` is a 4-item list: `[null, [...], [...], [...]]`
- [ ] Every MCQ option set (T2–T4) has exactly 3 options, exactly 1 with `is_best: true`
- [ ] `content/atomic_overlap_report.json` has exactly 6 merge candidate groups (5 non-`responsible_ai` domains × 4 atoms + 1 `responsible_ai` domain × 4 non-capstone atoms)
- [ ] 4 capstone atoms are in `atomic_modules.json` but absent from `atomic_overlap_report.json`
- [ ] No chaining artifacts: every pair within a merge group has pairwise Jaccard ≥ 0.70
- [ ] Human spot-check: 3 atoms (`responsible_ai__rm_c1_responsible_ai`, `strategic_prompting__uw_c2_strategic_prompting`, `data_decision__an_c5_data_decision`) read as role-agnostic with no loss of instructional intent
- [ ] App still runs on original JSON files — no regression
- [ ] `bash run_uat.sh` passes

---

## Commit

```bash
git add scripts/atomize_coursework.py \
        content/atomic_modules.json \
        content/atomic_overlap_report.json
git commit -m "feat(atomic): atomization pipeline + 21 converted modules"
```
