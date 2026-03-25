# Phase 7 Kickstarter — ZH Translations

> Read `plans/phase7-zh-translations-plan.md` for full context before starting.

---

## Context

Phase 4 added 6 new inline atoms + 2 PM role-variant atoms. Phase 6 redesigned the Welcome page (8 sections). All new content is EN-only. ZH users currently see EN for:

1. Welcome page marketing sections (77 keys missing from `content/i18n/zh.json`)
2. Atom reading and practice content (`atomic_modules_v2.json` has no `_zh` fields)
3. `utils/welcome_zh.py` exists but is incomplete/uncommitted

Diagnostic BYOW prompts are **already bilingual** — do not touch `diagnostic_prompts.json`.

---

## Pre-flight checks (run these first)

```bash
# 1. Confirm working tree state
git status

# 2. Confirm exact missing i18n keys
python -c "
import json
en = json.load(open('content/i18n/en.json', encoding='utf-8'))
zh = json.load(open('content/i18n/zh.json', encoding='utf-8'))
missing = [k for k in en if k not in zh]
print(f'Missing: {len(missing)} keys')
for k in missing: print(f'  {k}')
"

# 3. Confirm PM course entries in ZH reading_content
python -c "
import json
d = json.load(open('content/zh/reading_content.json', encoding='utf-8'))
pm = [k for k in d if 'pm_' in k]
print('PM entries in ZH reading_content:', pm)
"

# 4. Confirm welcome_zh.py section coverage vs 00_Welcome.py ZH routing
grep -n "_wzh\." pages/00_Welcome.py
grep -n "^def render_" utils/welcome_zh.py
```

---

## Task sequence

### Task 1 — Commit existing WIP

Review `utils/welcome_zh.py` — it must have a `render_*_zh()` function for every `_wzh.render_*_zh()` call in `pages/00_Welcome.py`. Add any missing stubs (copy EN HTML, translate inline). Then:

```bash
git add utils/welcome_zh.py pages/00_Welcome.py content/i18n/en.json
git commit -m "feat(phase7): welcome page ZH renderers + i18n keys"
```

### Task 2 — Translate 77 zh.json keys

Add all 77 `welcome.*` keys to `content/i18n/zh.json`. These are short UI strings (labels, headings, stat copy, roadmap bullets). Use the Andrew Ng reflect-improve workflow (one call to translate, one to reflect/improve). Maintain the existing glossary in `scripts/translate_content.py`.

Commit: `feat(phase7): translate 77 welcome.* keys to ZH`

### Task 3 — Add _zh fields to 6 inline atoms

Edit `content/atomic_modules_v2.json`. For each of these 6 atoms, add `_zh` suffix variants for all user-visible fields:

**Target atoms:**
- `relationship_intel__meeting_intelligence`
- `augmented_comm__email_message_drafting`
- `strategic_prompting__iterative_refinement`
- `critical_eval__hallucination_patterns`
- `responsible_ai__ai_tool_governance`
- `data_decision__universal_analysis`

**Fields to add per atom:**
```
reading.concept_text_zh
reading.good_example_zh
reading.anti_pattern_zh
reading.takeaway_zh
practice.scenario_template_zh
practice.task_templates[*].text_template_zh   ← add _zh key inside each task template dict
title_zh
```

**Do not translate:** `scoring_rubric`, `coach_system_prompt_template`, `capability_tags`, `atom_id`, `domain`, `source_course_ids`.

Use the Gemini API (or databricks-claude-sonnet-4-6 endpoint) in batches of 2 atoms per LLM call. Apply the domain glossary from `scripts/translate_content.py`.

Commit: `feat(phase7): add _zh translation fields to 6 inline atoms`

### Task 4 — Wire ZH in 04_Course_Module.py

In the atom reading branch (around line 157–180), update to pick `_zh` fields when `_lang == "zh"`:

```python
# reading dict — atom["reading"] uses same keys with optional _zh suffix
_sfx = "_zh" if _lang == "zh" else ""
_r = _atom.get("reading") or {}
reading = {
    "concept_text": _r.get(f"concept_text{_sfx}") or _r.get("concept_text", ""),
    "good_example":  _r.get(f"good_example{_sfx}")  or _r.get("good_example", ""),
    "anti_pattern":  _r.get(f"anti_pattern{_sfx}")  or _r.get("anti_pattern", ""),
    "takeaway":      _r.get(f"takeaway{_sfx}")       or _r.get("takeaway", ""),
}
```

For `scenario_template`, update `fill_scenario()` in `utils/path_assembler.py` to accept `lang` and pick `scenario_template_zh` when `lang == "zh"`. (It already receives `_lang` — just pass it through.)

For task templates: in the scenario dict construction, pick `text_template_zh` when `_lang == "zh"`.

Atom `title`: `_atom.get("title_zh") if _lang == "zh" else _atom.get("title")` — apply wherever atom title is displayed.

Commit: `feat(phase7): wire _zh fields in Course Module for lang=="zh"`

### Task 5 — Handle PM atoms (reading_content)

If PM entries are missing from `content/zh/reading_content.json`:

```bash
python scripts/translate_content.py --file reading_content --role pm
```

Commit if changes made: `feat(phase7): translate PM reading_content to ZH`

### Task 6 — Extend translate_content.py

Add `translate_atomic_modules()` to `scripts/translate_content.py` and register it as `"atomic_modules"` in `FILE_MAP`. This function should:
- Load `content/atomic_modules_v2.json`
- For each atom in scope (all by default, filterable by domain), translate the fields listed above using the existing `_call_llm()` pattern
- Write `_zh` variants back in-place (same file, no separate output)
- Use `--dry-run` to preview

Commit: `feat(phase7): add translate_atomic_modules to translate_content.py`

### Task 7 — UAT G9

Run the app and verify end-to-end ZH path:

```bash
bash run_uat.sh
```

Reset to clean state:
```bash
python scripts/reset_uat_user.py --profile all-done
```

**G9 UAT checklist:**
- [ ] Welcome page: language toggle to ZH → all 8 sections render in ZH (no EN strings)
- [ ] Welcome page: stat labels, roadmap section, differentiators in ZH
- [ ] Diagnostic: BYOW prompts in ZH (already works — verify unchanged)
- [ ] Skills Profile: gap map bullets in ZH (already works)
- [ ] Home page: module titles in ZH
- [ ] Module reading (Phase 4 atom): `concept_text_zh` shown, not EN fallback
- [ ] Module practice (Phase 4 atom): scenario and tasks in ZH
- [ ] Module evaluation: inline eval items in ZH (if translated)
- [ ] Switch lang back to EN mid-session: EN content resumes

---

## Constraints

- Do NOT touch `diagnostic_prompts.json` — BYOW ZH is already live
- Do NOT translate `scoring_rubric` fields (AI-internal, never rendered)
- Do NOT translate `coach_system_prompt_template` (used as system prompt, EN is correct)
- Do NOT create `content/zh/atomic_modules_v2.json` — use in-place `_zh` suffix pattern
- All pytest must pass (42/42) before marking done

---

## Commit sequence summary

```
feat(phase7): welcome page ZH renderers + i18n keys        ← Task 1
feat(phase7): translate 77 welcome.* keys to ZH            ← Task 2
feat(phase7): add _zh translation fields to 6 inline atoms ← Task 3
feat(phase7): wire _zh fields in Course Module + assembler  ← Task 4
feat(phase7): translate PM reading_content to ZH            ← Task 5 (if needed)
feat(phase7): add translate_atomic_modules to script        ← Task 6
docs(phase7): mark COMPLETE — pytest green, G9 UAT pass    ← final
```
