# Issues.md — AI Hero Academy MVP
**Code Review Against TDD.md and PRD.md**
Date: February 2026 | Reviewer: Claude Code
Last validated: February 2026

---

## Severity Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 HIGH | Incorrect behaviour, wrong scores, broken TDD contract |
| 🟡 MEDIUM | Deviates from TDD spec, missing data, suboptimal but not wrong |
| 🟢 LOW | Minor UX gap, cosmetic, or TDD wording mismatch |

---

## Open Issues

### M2 — `training_progress` UPDATE still uses inline float interpolation

**File**: [pages/04_Course_Module.py:510-517](pages/04_Course_Module.py#L510-L517)

**TDD reference**: §5.5 — "Use parameterised queries for all learner writes"

**What's wrong**: The evaluation score UPDATE interpolates `{eval_score}` and `{domain_score_after}` directly into the SQL string:

```python
execute(
    f"UPDATE {CATALOG}.learner.training_progress "
    f"SET evaluation_score = {eval_score}, "
    f"    evaluation_completed_at = current_timestamp(), "
    f"    domain_score_after = {domain_score_after} "
    f"WHERE progress_id = ?",
    [progress_id],
)
```

Both values are Python `float()` casts from LLM output, so the SQL injection risk is negligible. However, TDD §5.5 requires parameterised queries for **all** learner writes. The other three affected statements (coach_sessions INSERT, gap_maps INSERT, diagnostic_sessions INSERT) have all been fixed.

---

### L1 — `call_type="coach_note"` not in TDD §3.4 allowed values

**File**: [utils/ai.py:351](utils/ai.py#L351)

**TDD reference**: §3.4 — `call_type` values: `'diagnostic_scoring' | 'gap_map' | 'coach_response' | 'evaluation_scoring'`

`generate_module_coach_note()` uses `call_type="coach_note"`. Not a runtime error, but monitoring queries in TDD §3.4 won't catch this type. Either add `'coach_note'` to the TDD allowed list or change to `'coach_response'`.

---

### U1 — Pre-diagnostic orientation screen missing

**File**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

**PRD reference**: §7.2 — Diagnostic user flow

**Severity**: 🟡 MEDIUM

**What's wrong**: Users are immediately presented with Question 1 of 12 with zero context. There is no time estimate, no question count, no format overview (MCQ + open-text + micro-task mix), and no "Start Assessment" CTA for mental preparation. Users see the first question cold.

**Expected**: An orientation screen before Q1 showing — estimated time (~5 min), total questions (12), format description (mix of multiple choice and written responses), and a "Start Assessment" button. Use `st.session_state["diag_started"]` flag so the screen shows on first load and is skipped on rerun.

---

### U2 — Home module card layout (P0-3) unverified

**File**: [pages/03_Home.py](pages/03_Home.py)

**Severity**: 🟢 LOW

**What's wrong**: The module card button-attachment fix applied in a prior session cannot be visually confirmed because the UAT user (`uat-test@edc.ca`) has no `training_progress` rows — the Home page shows no module cards at all.

**Blocked by**: UAT user must have a training course. Click "🗺️ Build My Training Course" on the Skills Profile page to unblock, then verify cards render with button attached to card bottom.

---

### U3 — No UX audit performed on Diagnostic, Home, or Course Module pages

**Files**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py), [pages/03_Home.py](pages/03_Home.py), [pages/04_Course_Module.py](pages/04_Course_Module.py)

**Severity**: 🟡 MEDIUM

**What's wrong**: The skills profile UX audit (contrast, layout, legend, column cleanup, max-width fix) covered only `02_Skills_Profile.py`. Three major pages have not yet been reviewed for contrast failures, spacing issues, empty columns, missing feedback, or PRD compliance gaps.

**Expected**: Full per-page audit of all three remaining pages against PRD §7.2, §7.4, §7.5 and the WCAG AA contrast minimum (`#8990A8` on `#0D0F14`).

---

## Closed Issues

| ID | Severity | Description | Resolution |
| --- | --- | --- | --- |
| H1 | 🔴 HIGH | Domain scores: average-of-averages not equal-weight per item | Fixed — `compute_current_domain_scores()` now called in both Skills Profile and Home pages |
| H2 | 🔴 HIGH | MCQ items sent to LLM; `score_mcq()` never called | Fixed — `_score_batch()` now scores MCQ locally via `score_mcq()`; LLM only receives open-ended items |
| H3 | 🔴 HIGH | `score_evaluation` asked LLM for aggregates; inconsistent with `score_diagnostic` | Fixed — `score_evaluation()` now mirrors `score_diagnostic()`: uses `_score_batch()` per domain, aggregates computed in Python |
| M1 | 🟡 MEDIUM | Token counts never populated in `ai_call_log` | Fixed — `call_llm()` extracts `resp.usage.prompt_tokens` / `resp.usage.completion_tokens` and passes to `_log_call()` |
| M3 | 🟡 MEDIUM | `started_at` = `completed_at` in sessions; duration data lost | Fixed — `coach_sessions` and `diagnostic_sessions` both use session-state timestamps for `started_at` and `current_timestamp()` for `completed_at` |
| M4 | 🟡 MEDIUM | Results fallback: `result_domain_score = result_score` (wrong column) | Fixed — fallback now reads `progress.get("domain_score_after")` from the already-loaded `progress` variable |
| M5 | 🟡 MEDIUM | Gap map after evaluation uses partial domain scores (diagnostic baseline only) | Fixed — `complete_evaluation()` now calls `load_all_progress()` + `compute_current_domain_scores()` to build fully merged scores before generating the gap map |
| L2 | 🟢 LOW | `reading_completed_at` overwritten on re-read | Fixed — UPDATE now uses `WHERE progress_id = ? AND reading_completed_at IS NULL` |
| L3 | 🟢 LOW | Level label gap at score 0.41–0.49 | Fixed — `LEVEL_LABELS` range changed to `(0.0, 0.49, "Unaware")` |
| L4 | 🟢 LOW | `load_progress()` uncached; extra DB call in Results fallback | Fixed — Results fallback uses the `progress` variable loaded at page start; no extra DB call |
| L5 | 🟢 LOW | Dead `<a href="#">` link in Home summary card | Fixed — replaced with a Streamlit button (`st.button("→  View Full Skills Profile", ...)`) |
| L6 | 🟢 LOW | Welcome guard routes all existing users to Diagnostic | Fixed — guard now checks for completed diagnostic session and training_progress, routing to Diagnostic / Skills Profile / Home as appropriate |
| L7 | 🟢 LOW | Missing `seed_03_diagnostic_items` job in `databricks.yml` | Resolved by architecture change — all content is now served from JSON files in `content/`; no Delta seeding required for content tables |
| U0 | 🟢 LOW | `.block-container max-width: 900px` caused blank whitespace on wide screens | Fixed — changed to `max-width: none !important` in `utils/styles.py`; `layout="wide"` now fills viewport correctly |
