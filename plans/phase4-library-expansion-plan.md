# Phase 4 — Atomic Library Expansion

> Status: **PLANNED** — ready to start after Phase 3 ZH UAT closes
> Last updated: March 2026

---

## Context & What's Already Done

**Phase 3 complete (2026-03-23):** Dynamic path assembler live. 34/34 UAT checks pass.
The atomic library (`content/atomic_modules_v2.json`) has 15 canonical atoms:

| Type | Count | Description |
|------|-------|-------------|
| Universal canonical | 5 | `responsible_ai__safe_framework`, `strategic_prompting__craf_framework`, `critical_eval__verify_framework`, `augmented_comm__surface_workflow`, `capstone__end_to_end_workflow` |
| Role-variant | 10 | 5 × `data_decision` + 5 × `relationship_intel` (one per role) |

**The problem Phase 4 solves:**
The library is thin on universal atoms. A user with weak `augmented_comm` can only receive
`surface_workflow` — there is no second choice. McKinsey data flags meeting intelligence,
email drafting, iterative prompting, and hallucination detection as the top 4 high-demand
AI skills not yet covered. These are also the 4 gaps against the Turing Institute and WEF
frameworks documented in `plans/master-architecture.md`.

---

## What Phase 4 Builds

5 new universal canonical atoms, authored directly in atomic-ready JSON format.
No atomization pipeline needed — these are original atoms, not converted from legacy courses.

| Priority | Atom ID | Domain | Employee Hook |
|----------|---------|--------|---------------|
| P1 | `relationship_intel__meeting_intelligence` | `relationship_intel` | "Walk into every meeting knowing more context than the person who called it." |
| P2 | `augmented_comm__email_message_drafting` | `augmented_comm` | "Email drafting is the #1 daily time sink AI eliminates — reclaim it today." |
| P3 | `strategic_prompting__iterative_refinement` | `strategic_prompting` | "One more prompt turn converts a mediocre draft into something you'd actually send." |
| P4 | `critical_eval__hallucination_patterns` | `critical_eval` | "One unchecked AI error forwarded to leadership can undo months of credibility." |
| P5 | `responsible_ai__ai_tool_governance` | `responsible_ai` | "Knowing which AI tool to use — and which to avoid — is a career skill, not a policy box to check." |

---

## Schema Change: Inline Eval Items

New atoms have no `source_course_ids`, so eval items must be self-contained.
Adds `inline_items` to the `eval` section. Existing atoms are unchanged.

```json
"eval": {
  "items_ref": "inline",
  "inline_items": [
    {
      "item_id": "ev_<atom_id>_q1",
      "item_type": "mcq",
      "sequence": 1,
      "question_text": "...",
      "scenario_text": "...",
      "options": [
        {"label": "A", "text": "..."},
        {"label": "B", "text": "..."},
        {"label": "C", "text": "..."},
        {"label": "D", "text": "..."}
      ],
      "correct_answer": "B",
      "score_value": 1
    },
    {
      "item_id": "ev_<atom_id>_q4",
      "item_type": "performance_task",
      "sequence": 4,
      "question_text": "...",
      "scenario_text": "...",
      "rubric": [
        {"criterion": "...", "weight": 0.25},
        {"criterion": "...", "weight": 0.25},
        {"criterion": "...", "weight": 0.25},
        {"criterion": "...", "weight": 0.25}
      ]
    }
  ],
  "source_course_ids": []
}
```

**Backward compat:** Existing atoms use `items_ref: "evaluation_items.json"`. The eval
loader in `pages/04_Course_Module.py` checks `items_ref` first:

```python
eval_section = atom.get("eval", {})
if eval_section.get("items_ref") == "inline":
    eval_items = eval_section["inline_items"]
else:
    course_id = eval_section["source_course_ids"][0]
    eval_items = get_eval_items(course_id)   # unchanged
```

---

## Implementation Tasks

### 4.1 — Create `scripts/generate_atom.py`

New CLI script. Pattern from `scripts/enrich_reading_content.py` (SDK auth, retry, CLI flags).

```bash
python scripts/generate_atom.py --atom-id relationship_intel__meeting_intelligence
python scripts/generate_atom.py --atom-id <id> --dry-run   # prints prompt, exits
```

- Hardcoded `ATOM_SPECS` dict with all 5 atoms' metadata (title, domain, tags, hook, framework)
- LLM: `gemini-2.0-flash`, temperature 0.3
- Output: valid JSON printed to stdout — human reviews, then appends to `atomic_modules_v2.json`
- Content rules:
  - Employee benefit within first 2 sentences of `reading.concept_text`
  - All placeholders from `fill_scenario()`: `{role}`, `{org_type}`, `{case_type}`,
    `{data_types}`, `{workflow_goal}`, `{programme_name}`, `{audience}`, `{sensitivity_level}`
  - Never hardcode "EDC", "analyst", or role-specific org names
  - 4 task_templates with `task_id`, `text_template`, `skill_focus`, `task_mode`, `mcq_options`
  - 3 MCQ + 1 performance_task eval items in `eval.inline_items`

### 4.2 — Generate all 5 atoms (in priority order)

Run `generate_atom.py` for each, review output quality, append to `atomic_modules_v2.json`.

Validation after each append:

```python
python -c "
import json, re
atoms = json.load(open('content/atomic_modules_v2.json', encoding='utf-8'))
a = [x for x in atoms if x['atom_id'] == '<atom_id>'][0]
print('tags:', len(a['capability_tags']))
print('inline:', a['eval']['items_ref'] == 'inline')
print('items:', len(a['eval']['inline_items']))
# Check no unfilled placeholders
filled = a['practice']['scenario_template'].format(
    role='X', org_type='X', case_type='X', data_types='X', workflow_goal='X',
    programme_name='X', audience='X', sensitivity_level='X',
    scenario_name='X', organisation='X', domain='X'
)
print('unfilled placeholders:', re.findall(r'\{[a-z_]+\}', filled))
"
```

### 4.3 — Update eval loader (`pages/04_Course_Module.py`)

**Hold until Phase 3 ZH UAT closes** (risk: merge conflict in 53 KB file).

Add inline eval branch before the existing `source_course_ids` lookup.
2-line change, backward compat preserved.

### 4.4 — Run regression tests

```bash
.venv/Scripts/pytest tests/test_path_assembler.py -v
```

Path assembler requires no changes — new atoms flow through `assemble_path()` automatically.

### 4.5 — Smoke test

```bash
bash run_uat.sh
```

Use Playwright MCP tools to verify:

1. A demo persona (3a–3f) loads Home without errors
2. Click Module 1 → Reading tab loads
3. Navigate to Evaluation tab → questions render
4. No Python exceptions in terminal

---

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `atomic_modules_v2.json` has 20 atoms (15 existing + 5 new) | 🔜 |
| 2 | All 5 new atoms: `eval.items_ref == "inline"`, 4 items (3 MCQ + 1 perf task) | 🔜 |
| 3 | All 5 new atoms: `fill_scenario()` produces zero unfilled `{placeholder}` tokens | 🔜 |
| 4 | All 5 new atoms: `status: "canonical"`, 3–6 `capability_tags` | 🔜 |
| 5 | `pages/04_Course_Module.py` loads eval from `inline_items` when `items_ref == "inline"` | 🔜 |
| 6 | Path assembler unchanged — new atoms selected automatically by `assemble_path()` | 🔜 |
| 7 | A user with weak `augmented_comm` can receive either `surface_workflow` or `email_message_drafting` | 🔜 |
| 8 | Regression: all Phase 3 UAT personas (3a–3f) still load correctly | 🔜 |

---

## New Files

- `scripts/generate_atom.py` — atom generation CLI

## Modified Files

- `content/atomic_modules_v2.json` — append 5 new atoms
- `pages/04_Course_Module.py` — eval loader inline branch (Step 4.3, after ZH UAT)

## Non-Goals for Phase 4

- Engineer role content (Phase 5)
- Reusable Prompt Templates atom (`strategic_prompting`) — deferred
- Shadow AI Risk Management atom — deferred
- ZH translations of new atoms — deferred (translate_content.py handles it when ready)

---

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LLM generates new `{placeholder}` not in `fill_scenario()` | Medium | Validation script checks for unfilled tokens; add placeholder to `fill_scenario()` if needed |
| Eval quality is low for new atoms (no source rubric to draw from) | Medium | Human review before appending; re-run with higher temperature if output is generic |
| Merge conflict in `04_Course_Module.py` with ZH UAT fixes | Low (if Step 4.3 is held) | Hold Step 4.3 until ZH UAT closes |
