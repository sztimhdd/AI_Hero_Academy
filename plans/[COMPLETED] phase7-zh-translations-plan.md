# Phase 7 — ZH Translations for New Atoms + Welcome Page

> Status: **PLANNED** — 2026-03-25
> Prerequisite: Phase 6 COMPLETE ✅

---

## Problem Statement

Phase 4 added 6 new inline atoms and 2 PM role-variant atoms. Phase 6 added a fully redesigned Welcome page (8 sections, 77 new i18n keys). All new content is EN-only. ZH users get:

1. **Atom reading/practice content in EN** — `get_atomic_modules()` has no `lang` param; `04_Course_Module.py` reads `atom["reading"]` directly without ZH fallback
2. **Welcome page in EN regardless of toggle** — `welcome_zh.py` exists (started) but is incomplete and uncommitted
3. **77 missing zh.json keys** — all `welcome.*` keys added in Phase 6 are absent from `content/i18n/zh.json`

Diagnostic BYOW prompts are already bilingual (`prompt_text_zh`, `placeholder_text_zh` fields in `diagnostic_prompts.json`) — no action needed there.

---

## Scope

### Task 1 — Commit in-progress Welcome ZH work
The working tree has 3 uncommitted files from exploratory Phase 7 work:
- `utils/welcome_zh.py` (292 lines — Chinese renderers for marketing sections)
- `pages/00_Welcome.py` (wired to call `welcome_zh.py` when `lang == "zh"`)
- `content/i18n/en.json` (77 new `welcome.*` keys added)

**Action:** Review the 3 files, complete any missing sections in `welcome_zh.py`, then commit.

### Task 2 — Translate 77 missing zh.json keys
All 77 missing keys are `welcome.*` — the Welcome page marketing copy.

**Action:** Add all 77 keys to `content/i18n/zh.json` using the Andrew Ng reflection workflow (translate → reflect → improve). These are UI strings, not long-form content — batch in one pass.

### Task 3 — Translate 6 new inline atom fields
Six atoms have `source_course_ids: []` and store content inline in `atomic_modules_v2.json`. They are read directly from `atom["reading"]` in `04_Course_Module.py` with no ZH fallback.

**Atoms to translate:**
- `relationship_intel__meeting_intelligence`
- `augmented_comm__email_message_drafting`
- `strategic_prompting__iterative_refinement`
- `critical_eval__hallucination_patterns`
- `responsible_ai__ai_tool_governance`
- `data_decision__universal_analysis`

**Fields to translate per atom:**
- `reading.concept_text`
- `reading.good_example`
- `reading.anti_pattern`
- `reading.takeaway`
- `practice.scenario_template`
- `practice.task_templates[*].text_template`
- `title` (atom title shown in UI)

**Approach A — Bilingual fields in-place** (preferred for atoms):
Add `_zh` suffix variants directly into `atomic_modules_v2.json`:
```json
"reading": {
  "concept_text": "...[EN]...",
  "concept_text_zh": "...[ZH]...",
  ...
}
```
Then update `04_Course_Module.py` atom reading branch to pick `_zh` fields when `_lang == "zh"`.

**Approach B — Separate file** (`content/zh/atomic_modules_v2.json`):
Mirror the EN file; `get_atomic_modules(lang)` loads the ZH version.
Requires adding a `lang` param to `get_atomic_modules()`.

**Decision: Use Approach A** — consistent with how `diagnostic_prompts.json` handles bilingual content. Avoids duplicating the full 21-atom file.

### Task 4 — PM role-variant atoms (reading content)
`relationship_intel__pm_c4_relationship_intel` and `data_decision__pm_c5_data_decision` use `source_course_ids: ['pm_c4_relationship_intel', 'pm_c5_data_decision']` — they delegate reading content to `reading_content.json`. Check if PM course entries exist in `content/zh/reading_content.json`.

```bash
python -c "import json; d=json.load(open('content/zh/reading_content.json')); print([k for k in d if 'pm_' in k])"
```

If absent → add PM entries to `content/zh/reading_content.json` via `translate_content.py --file reading_content`.

### Task 5 — Extend translate_content.py
Add `translate_atomic_modules()` function to `scripts/translate_content.py`:
- Reads `content/atomic_modules_v2.json`
- For each atom in scope, translates the fields listed above
- Writes `_zh` suffix variants back in-place
- Registers as `"atomic_modules"` in `FILE_MAP`

This enables re-running translations if atoms are added in future phases.

### Task 6 — UAT ZH language toggle
Run the app with `lang = "zh"` through:
- Welcome page (all 8 marketing sections render in ZH)
- Diagnostic (BYOW prompts in ZH — already works)
- Skills Profile (existing ZH coverage)
- Module reading for a Phase 4 atom (concept_text_zh rendered)
- Module practice for a Phase 4 atom (scenario_template_zh rendered)

---

## What Does NOT Need Translation

| Item | Reason |
|------|--------|
| `diagnostic_prompts.json` | Already bilingual (Phase 5 added `_zh` fields) |
| `content/zh/reading_content.json` (original 35) | Fully translated (Phase 1.8) |
| `content/zh/practice_scenarios.json` | Fully translated |
| `content/zh/evaluation_items.json` | Fully translated |
| `content/zh/courses.json` | Fully translated |
| `scoring_rubric` in atoms | AI-internal only, never rendered to user |

---

## Acceptance Criteria

- [ ] `content/i18n/zh.json` has 261 keys (matches EN)
- [ ] Welcome page renders in ZH with no EN fallback strings visible
- [ ] `utils/welcome_zh.py` covers all 8 sections rendered in `00_Welcome.py`
- [ ] 6 inline atoms each have `_zh` variants for all user-visible fields
- [ ] `04_Course_Module.py` picks `_zh` fields when `_lang == "zh"`
- [ ] PM course entries present in `content/zh/reading_content.json`
- [ ] `scripts/translate_content.py --file atomic_modules` runs without error
- [ ] 42/42 pytest green
- [ ] ZH UAT G9 pass (Welcome → Diagnostic → Module with Phase 4 atom, all in ZH)

---

## Files Touched

| File | Change |
|------|--------|
| `content/i18n/zh.json` | +77 `welcome.*` keys |
| `utils/welcome_zh.py` | Complete all 8 sections (commit existing start) |
| `pages/00_Welcome.py` | Commit existing ZH routing (minor fix if needed) |
| `content/atomic_modules_v2.json` | +`_zh` fields on 6 inline atoms |
| `pages/04_Course_Module.py` | Atom reading/practice branch picks `_zh` when `lang=="zh"` |
| `content/zh/reading_content.json` | +PM entries if missing |
| `scripts/translate_content.py` | +`translate_atomic_modules()` + FILE_MAP entry |

No schema changes, no Firestore changes, no new pages.

---

## Estimated Token Budget

- Task 1 (commit WIP): trivial
- Task 2 (77 i18n keys): ~1 LLM call, ~3K tokens
- Task 3 (6 atoms × ~6 fields): ~6 LLM calls or 2 batched calls, ~8K tokens
- Task 4 (PM reading content check + translate if needed): ~2 LLM calls
- Task 5 (extend translate script): code only, no LLM
- Task 6 (UAT): Playwright MCP, no LLM

Total: low-risk, single-session sprint.
