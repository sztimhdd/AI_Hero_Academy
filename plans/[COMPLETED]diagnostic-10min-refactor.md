# Plan: Diagnostic Redesign — 10-Minute Sequence (All Roles)

**Status**: DEFERRED — blocked on UW 6-domain content regeneration
**Ready to execute when**: UW coursework pipeline has been run and `content/diagnostic_items.json`
contains 18 UW items following the 6-domain model

---

## Background

### Problem
The current diagnostic is 18 questions per role (3 per domain × 6 domains), including
prompt_sandbox and micro_task items. Estimated completion time: **35–45 minutes**.

### Industry standard
8–12 questions, 5–10 minutes (SurveySparrow, Shift eLearning, Elucidat research).
Average cognitive attention window before drop-off: 10–15 minutes.

### Design principle
- **MCQ** for conceptual/evaluative domains — fast, sufficient to place the learner
- **micro_task** for hands-on domains — required to demonstrate actual skill; sandbox belongs
  in practice modules, not at the pre-training gate

---

## Proposed 6-Item, ~10-Minute Sequence

### Domain classification (applies to all roles)

| Domain | Hands-on? | Reasoning | Item type |
|--------|-----------|-----------|-----------|
| `responsible_ai` | No | Pattern recognition / judgment call | MCQ |
| `strategic_prompting` | **Yes** | Writing and improving prompts IS the skill | micro_task |
| `critical_eval` | No | Analytical / cognitive evaluation | MCQ |
| `data_decision` | **Yes** | Interpreting data and deciding on action | micro_task |
| `relationship_intel` | No | AI-assisted prep; decision-making | MCQ |
| `augmented_comm` | No | Tool selection, record governance, judgment | MCQ |

### Sequence order and timing

| # | Domain | Type | Est. time |
|---|--------|------|-----------|
| 1 | `responsible_ai` | MCQ | ~1 min |
| 2 | `strategic_prompting` | micro_task | ~3 min |
| 3 | `critical_eval` | MCQ | ~1 min |
| 4 | `data_decision` | micro_task | ~3 min |
| 5 | `relationship_intel` | MCQ | ~1 min |
| 6 | `augmented_comm` | MCQ | ~1 min |
| **Total** | | 4 MCQ + 2 micro_task | **~10 min** |

**Sequencing rationale**: Opens with a fast conceptual question (low friction entry),
front-loads the two demanding tasks while attention is highest (positions 2 & 4), and
ends with two quick MCQs for a light finish.

---

## Per-Role Item Keepers

### RM — Confirmed ✓

| display_order | item_id | domain | type |
|---|---------|--------|------|
| 1 | `rm_diag_ra1_mcq` | responsible_ai | MCQ |
| 2 | `rm_diag_sp6_task` | strategic_prompting | micro_task |
| 3 | `rm_diag_ce7_mcq` | critical_eval | MCQ |
| 4 | `rm_diag_dd15_task` | data_decision | micro_task |
| 5 | `rm_diag_ri10_mcq` | relationship_intel | MCQ |
| 6 | `rm_diag_ac16_mcq` | augmented_comm | MCQ |

### AN — Confirmed ✓

| display_order | item_id | domain | type |
|---|---------|--------|------|
| 1 | `an_diag_ra1_mcq` | responsible_ai | MCQ |
| 2 | `an_diag_sp6_task` | strategic_prompting | micro_task |
| 3 | `an_diag_ce7_mcq` | critical_eval | MCQ |
| 4 | `an_diag_dd15_task` | data_decision | micro_task |
| 5 | `an_diag_ri10_mcq` | relationship_intel | MCQ |
| 6 | `an_diag_ac16_mcq` | augmented_comm | MCQ |

### UW — PENDING (blocked on UW content regeneration)

Current UW items use a different numbering scheme (sp1/sp2/sp3 not sp4/sp5/sp6).
After UW is regenerated on the 6-domain model, the UW keepers will be:

| display_order | Expected item_id | domain | type |
|---|---------|--------|------|
| 1 | `uw_diag_ra1_mcq` | responsible_ai | MCQ |
| 2 | `uw_diag_sp?_task` | strategic_prompting | micro_task |
| 3 | `uw_diag_ce?_mcq` | critical_eval | MCQ |
| 4 | `uw_diag_dd?_task` | data_decision | micro_task |
| 5 | `uw_diag_ri?_mcq` | relationship_intel | MCQ |
| 6 | `uw_diag_ac?_mcq` | augmented_comm | MCQ |

**On execution day**: list all UW items by domain and pick the correct item_id for each
of the 6 keeper slots (1 MCQ per non-hands-on domain, 1 micro_task per hands-on domain).

---

## Items Dropped (12 per role, 36 total)

For each domain, drop:
- All `prompt_sandbox` items — sandbox belongs in practice modules, not pre-training gate
- `micro_task` from non-hands-on domains (responsible_ai, critical_eval, relationship_intel,
  augmented_comm)
- `mcq` from hands-on domains (strategic_prompting, data_decision)

---

## Implementation Steps

### Step 1 — Confirm UW content is ready

```bash
python -c "
import json
items = json.load(open('content/diagnostic_items.json'))
uw = [i for i in items if i.get('role_id') == 'uw']
print(f'UW items: {len(uw)}')
for i in uw: print(f'  {i[\"item_id\"]:30s}  {i[\"domain_id\"]:20s}  {i[\"item_type\"]}')
"
```

Expected: 18 UW items covering all 6 domains with MCQ/sandbox/task types.
If UW has < 18 items or missing domains → **stop, regenerate UW content first**.

### Step 2 — Identify UW keepers and update the plan

From the listing above, fill in the `uw_diag_sp?_task`, `uw_diag_ce?_mcq`, etc. item IDs
in the KEEP dict below, then proceed.

### Step 3 — Apply filter + add display_order

Run inline Python (update UW IDs first):

```python
import json
from pathlib import Path

KEEP = {
    "rm": [
        "rm_diag_ra1_mcq",
        "rm_diag_sp6_task",
        "rm_diag_ce7_mcq",
        "rm_diag_dd15_task",
        "rm_diag_ri10_mcq",
        "rm_diag_ac16_mcq",
    ],
    "an": [
        "an_diag_ra1_mcq",
        "an_diag_sp6_task",
        "an_diag_ce7_mcq",
        "an_diag_dd15_task",
        "an_diag_ri10_mcq",
        "an_diag_ac16_mcq",
    ],
    "uw": [
        "uw_diag_ra1_mcq",    # fill in after Step 2
        "uw_diag_sp?_task",   # TODO: fill in
        "uw_diag_ce?_mcq",    # TODO: fill in
        "uw_diag_dd?_task",   # TODO: fill in
        "uw_diag_ri?_mcq",    # TODO: fill in
        "uw_diag_ac?_mcq",    # TODO: fill in
    ],
}

# display_order key: suffix pattern → order position
ORDER_MAP = {
    "responsible_ai":    1,
    "strategic_prompting": 2,
    "critical_eval":     3,
    "data_decision":     4,
    "relationship_intel": 5,
    "augmented_comm":    6,
}

p = Path("content/diagnostic_items.json")
items = json.loads(p.read_text())
result = []
for item in items:
    role = item.get("role_id")
    if item["item_id"] in KEEP.get(role, []):
        item["display_order"] = ORDER_MAP[item["domain_id"]]
        result.append(item)

p.write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(f"Done: {len(result)} items kept (expected 18)")
for role in ["rm", "uw", "an"]:
    n = sum(1 for i in result if i.get("role_id") == role)
    print(f"  {role}: {n}")
```

Expected output: 18 items total, 6 per role.

### Step 4 — Audit app code for hardcoded question counts

Search for hardcoded `18` or similar:
```bash
grep -rn "18\|num_questions\|total_questions" app.py pages/ utils/ --include="*.py"
```

Key files to check:
- `app.py` or the diagnostic page file — progress bar / "Question X of N" display
- `utils/content.py` — `get_diagnostic_items()` — confirm returns full list dynamically
- `utils/scoring.py` (if exists) — confirm domain averaging uses `len(items)` not a constant

Fix any hardcoded counts. All question counts must derive from `len(items)`.

### Step 5 — Reset test user and run UAT

```bash
python scripts/reset_uat_user.py
bash run_uat.sh
```

Walk the full diagnostic as `dev@example.com`. Verify:
- 6 questions appear in order: MCQ → micro_task → MCQ → micro_task → MCQ → MCQ
- Progress indicator shows X/6 (not X/18)
- All 6 domain scores populated after submission
- Gap map generates correctly
- No regression on UW / AN flows (run a quick UW diagnostic pass too)

### Step 6 — Commit and deploy

```bash
git add content/diagnostic_items.json
# + any modified app/utils files from Step 4
git commit -m "feat(diagnostic): reduce to 6-item 10-min sequence (4 MCQ + 2 micro_task per role)"
bash scripts/sync_deploy.sh
```

---

## Files Modified

| File | Change |
|------|--------|
| `content/diagnostic_items.json` | 54 → 18 items; `display_order` field added |
| `app.py` / diagnostic page | Remove hardcoded question-count references (if any) |
| `utils/scoring.py` | Confirm dynamic item count in domain averaging |

## Verification Checklist

- [ ] `len(items) == 18` and exactly 6 per role in `diagnostic_items.json`
- [ ] Each item has a `display_order` field (1–6)
- [ ] UI shows 6 questions in the correct sequence
- [ ] Progress indicator is dynamic (X/6, not X/18)
- [ ] All 6 domain scores populated after diagnostic submission
- [ ] Gap map generates and persists correctly
- [ ] No regression for UW or AN diagnostic flows
