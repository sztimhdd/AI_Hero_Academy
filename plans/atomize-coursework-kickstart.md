# Atomic Coursework Pipeline — Agent Kickstart Prompt

Copy the section below into a new Claude Code session to implement Phase 0.5.

---

## Kickstart Prompt

You are implementing **Phase 0.5 of the AI Hero Academy atomic architecture**: building
`scripts/atomize_coursework.py`, running it against all 21 existing courses, and producing
`content/atomic_modules.json` + `content/atomic_overlap_report.json`.

**The app DOES NOT change.** It keeps running from its original JSON files throughout.
These output files are a parallel data store for Phase 1 (PM + Engineer content) and
Phase 3 (path assembler activation). No page, route, or utility reads from these files yet.

---

### Read these files first (in order)

1. `plans/atomize-coursework-plan.md` — full spec: schema, extraction prompts, overlap algorithm, validation
2. `scripts/enrich_reading_content.py` — reuse its SDK and concurrency pattern exactly
3. `content/courses.json` (first 60 lines)
4. `content/practice_scenarios.json` (first 40 lines)
5. `content/reading_content_structured.json` (first 50 lines) — primary reading source
6. `content/reading_content.json` (first 20 lines) — fallback for courses with no structured entry

---

### Branch setup

```bash
git checkout main && git pull
git checkout -b feature/atomize-coursework
```

---

### What to build (3 tasks, in order)

---

#### AC-1 — Build `scripts/atomize_coursework.py`

The full spec is in `plans/atomize-coursework-plan.md`. Key points:

- Source files are all **dicts keyed by `course_id`** — join is direct
- `practice_scenarios.json` already contains `task_modes` and `task_mcq_options` — **copy both
  fields as-is** into the atom's `practice` block (no LLM call needed; labels are already role-agnostic)
- For each of 21 courses: run 6 sequential LLM calls (`databricks-claude-sonnet-4-6`, `temperature=0`)
  to produce one complete atom dict
- Reading source: `reading_content_structured.json` (primary) → `reading_content.json` (fallback)
- Overlap detection: complete-link Jaccard clustering — see plan for the full algorithm
  (single-link / greedy transitive is explicitly NOT correct here)
- Dry-run must pretty-print a per-atom structured summary (not raw JSON) — see plan for format
- Write `content/atomic_modules.json` (list of 21 atoms) and `content/atomic_overlap_report.json`

CLI:

```bash
python scripts/atomize_coursework.py                                   # all 21
python scripts/atomize_coursework.py --dry-run                         # pretty-print, no write
python scripts/atomize_coursework.py --course-id an_c1_responsible_ai  # single test
```

Constraints:

- Only create new files — do NOT modify any existing `content/*.json`, `pages/`, `utils/`, or `app.py`
- `temperature=0.0` on all 6 calls — deterministic output is critical

---

#### AC-2 — Run enrichment and produce output files

```bash
# Test one item first
python scripts/atomize_coursework.py --dry-run --course-id an_c1_responsible_ai
```

Spot-check the pretty-printed output:

- `capability_tags`: 3–6 items, includes a named framework (e.g. `"SAFE_framework"`)
- `intro (derolled)`: no "As an analyst" or "As a Relationship Manager"
- `cards`: 4 items with letter / title / body
- `scenario_template`: contains `{role}` and `{org_type}`
- `task_modes`: `["open", "mcq", "mcq", "mcq"]`
- `task_templates`: 4 items, each with `text_template` + `skill_focus`
- `mcq_options`: T2–T4 each show 3 options; exactly 1 `is_best: true` per set
- `coach_tmpl`: no hardcoded "EDC", "analyst", or programme names
- `role_hint`: mentions 2 role types

If the single item looks correct, run all 21:

```bash
python scripts/atomize_coursework.py
```

Then verify the outputs using the validation commands in `plans/atomize-coursework-plan.md`
(Section "Validation"). Pretty-print the results and show them to the user.

If any item has null fields or fails the spot-check, re-run `--course-id <id>` to regenerate.
Fix systematic prompt issues before re-running the full batch.

Expected results:

- 21 atoms, all ✓
- 6 merge candidate groups (one per domain, each containing the RM + UW + AN version)
- All pairwise Jaccard scores within each group ≥ 0.70 (no chaining artifacts)

---

#### AC-3 — Verify no app regression

```bash
bash run_uat.sh
```

The app does not read `atomic_modules.json` — regression is impossible unless a shared file
was accidentally modified. Confirm no shared files were changed.

---

### Commit when done

```bash
git add scripts/atomize_coursework.py \
        content/atomic_modules.json \
        content/atomic_overlap_report.json
git commit -m "feat(atomic): atomization pipeline + 21 converted modules"
```

Then ask the user whether to merge to main or keep the branch for review.

---

### Acceptance checklist

- [ ] `python scripts/atomize_coursework.py --dry-run --course-id an_c1_responsible_ai` runs without errors
- [ ] `content/atomic_modules.json` has exactly 21 entries
- [ ] All 21 atoms have non-null `capability_tags` (3–6 items)
- [ ] All 21 atoms' `practice.scenario_template` contains `{role}` and `{org_type}`
- [ ] All 21 atoms' `practice.coach_system_prompt_template` has no hardcoded org/role/programme names
- [ ] All 21 atoms' `practice.task_modes` == `["open", "mcq", "mcq", "mcq"]`
- [ ] All 21 atoms' `practice.task_mcq_options` is `[null, [3 opts], [3 opts], [3 opts]]` with exactly 1 `is_best: true` per set
- [ ] Atoms from structured-reading courses have `reading.concept.cards` with ≥ 2 items
- [ ] `content/atomic_overlap_report.json` has exactly 6 merge candidate groups
- [ ] All pairwise scores within each merge group ≥ 0.70 (shown in validation output)
- [ ] `bash run_uat.sh` passes — no regressions
