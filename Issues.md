# Issues.md — AI Hero Academy MVP
**Code Review Against TDD.md and PRD.md**
Date: February 2026 | Reviewer: Claude Code

---

## Severity Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 HIGH | Incorrect behaviour, wrong scores, broken TDD contract |
| 🟡 MEDIUM | Deviates from TDD spec, missing data, suboptimal but not wrong |
| 🟢 LOW | Minor UX gap, cosmetic, or TDD wording mismatch |

---

## 🔴 HIGH Issues

### H1 — Domain scores use "average of averages" instead of equal-weight per item

**Files**: [pages/02_Skills_Profile.py:128-133](pages/02_Skills_Profile.py#L128-L133), [pages/03_Home.py:71-81](pages/03_Home.py#L71-L81)

**TDD reference**: §8 — "Domain score = average of all scored items for that domain across diagnostic and completed evaluations (equal weight per item)"

**What's wrong**: Both pages compute domain scores by averaging `domain_score_after` values from `learner.training_progress` — one scalar per completed module. This produces an "average of averages" not a per-item average.

Concrete example:
- Diagnostic: 3 prompting items scored 1.0, 1.0, 1.0 → avg = 1.0
- C1 evaluation (4 items, primary_domain=prompting): overall_score = 3.0 → stored as `domain_score_after = 3.0`
- C5 evaluation (4 items, primary_domain=prompting): overall_score = 3.5 → stored as `domain_score_after = 3.5`

Correct (TDD §8): average of 11 item scores = (3×1.0 + 4×3.0 + 4×3.5) / 11 = 2.36
Implemented: `(((1.0 + 3.0) / 2) + 3.5) / 2 = 2.125` — wrong weighting

**Root cause**: `calculate_domain_scores()` in `utils/scoring.py` has the correct algorithm but is never called from any page. Both pages use inline "running average" logic instead.

---

### H2 — MCQ items sent to LLM; `score_mcq()` is dead code

**Files**: [utils/ai.py:89-112](utils/ai.py#L89-L112), [utils/scoring.py:45-54](utils/scoring.py#L45-L54)

**TDD reference**: §8 — "MCQ items: rubric['correct'] (typically 4) if answer matches correct_option; else rubric['incorrect'] (typically 0)" — deterministic, no LLM needed

**What's wrong**: `_score_batch()` sends all item types including MCQ to the LLM. The LLM is asked to apply the rubric deterministically, but this (a) wastes tokens/latency, (b) risks non-deterministic results if the LLM interprets the rubric differently, and (c) means `score_mcq()` in `scoring.py` is unused dead code.

Same issue applies in `score_evaluation()` called from `complete_evaluation()` in `pages/04_Course_Module.py`.

---

### H3 — `score_evaluation` asks LLM to compute aggregates; inconsistent with `score_diagnostic`

**Files**: [utils/ai.py:239-273](utils/ai.py#L239-L273) vs [utils/ai.py:128-171](utils/ai.py#L128-L171)

**TDD reference**: §6.5 — "Same pattern as diagnostic scoring (§6.2)"

**What's wrong**: `score_diagnostic` sends items batched by domain and computes `domain_scores`/`overall_score` in Python. `score_evaluation` sends all 4 items in a single call and asks the LLM to compute the aggregates too. Two inconsistencies:
1. Architecture inconsistency: LLM computes aggregates in evaluation, Python computes them in diagnostic
2. The evaluation LLM prompt returns `overall_score = mean of domain_scores present`, but only one domain is ever present (all 4 eval items share `primary_domain`), so this `overall_score` is effectively the domain score — not a meaningful "overall"
3. `domain_score_after` in `complete_evaluation()` falls back to `eval_score` if `primary_domain` is not in the returned `domain_scores` dict — risky

---

## 🟡 MEDIUM Issues

### M1 — `prompt_tokens` and `completion_tokens` always NULL in `ai_call_log`

**File**: [utils/ai.py:52-74](utils/ai.py#L52-L74)

**TDD reference**: §3.4 `system.ai_call_log` defines `prompt_tokens INT` and `completion_tokens INT`

**What's wrong**: `_log_call()` never extracts token counts from the SDK response. The `resp` object from `w.serving_endpoints.query()` includes token usage in `resp.usage.prompt_tokens` and `resp.usage.completion_tokens`, but these are never read. Both columns will always be NULL, making cost/token monitoring impossible.

---

### M2 — Learner writes use inline SQL + `escape()` instead of parameterized queries

**Files**: [pages/04_Course_Module.py:148-161](pages/04_Course_Module.py#L148-L161), [pages/04_Course_Module.py:555-562](pages/04_Course_Module.py#L555-L562), [pages/04_Course_Module.py:593-602](pages/04_Course_Module.py#L593-L602), [pages/01_Diagnostic.py:142-156](pages/01_Diagnostic.py#L142-L156)

**TDD reference**: §5.5 — "Use parameterised queries for all learner writes"

**What's wrong**: Multiple INSERT/UPDATE statements for learner tables use f-string interpolation with `escape()` rather than parameterized `?` placeholders. The `execute()` helper fully supports parameterized writes. Using `escape()` is fragile and a SQL injection risk for any future path where input may not pass through `escape()`.

Affected statements:
- `coach_sessions` INSERT in `do_complete_practice()`
- `training_progress` UPDATE for evaluation score (mixes inline float `{eval_score}` with `?` param for `progress_id`)
- `gap_maps` INSERT in `complete_evaluation()`
- `diagnostic_sessions` INSERT in `complete_diagnostic()`

---

### M3 — `started_at` equals `completed_at` in both `coach_sessions` and `diagnostic_sessions`

**Files**: [pages/04_Course_Module.py:148-161](pages/04_Course_Module.py#L148-L161), [pages/01_Diagnostic.py:142-156](pages/01_Diagnostic.py#L142-L156)

**TDD reference**: §3.3 `learner.coach_sessions` and `learner.diagnostic_sessions` both define `started_at` as the session start time, `completed_at` as the end time.

**What's wrong**: Both use `current_timestamp()` for both `started_at` and `completed_at`. The `diagnostic_sessions.started_at` is set at the time `diag_session_started` UUID is created (session state on first question), but the actual INSERT doesn't use that stored timestamp — both columns receive `current_timestamp()` at save time. Session duration data is permanently lost.

---

### M4 — Results sub-view fallback uses `evaluation_score` for `result_domain_score`

**File**: [pages/04_Course_Module.py:717-724](pages/04_Course_Module.py#L717-L724)

**TDD reference**: §3.3 `learner.training_progress.domain_score_after` — the per-domain score after this module's evaluation

**What's wrong**: When `module_result_score` is not in session state (e.g. user navigated directly to results view), the fallback reads `evaluation_score` and assigns it to both `result_score` and `result_domain_score`:
```python
result_domain_score = result_score  # should be prog_fresh.get("domain_score_after")
```
The domain score bar on the Results page will show the overall eval score instead of the domain-specific score.

---

### M5 — Gap map `domain_scores` passed to `generate_gap_map` after evaluation is partial

**File**: [pages/04_Course_Module.py:575-591](pages/04_Course_Module.py#L575-L591)

**What's wrong**: After evaluation, the gap map is generated using:
```python
ds = json.loads(diag_row.get("domain_scores") or "{}")  # diagnostic-only baseline
ds[primary_domain] = domain_score_after                  # overwrite one domain
```
This uses the diagnostic baseline (not the post-training scores) for all non-primary domains. If the user has completed multiple modules, those improvements are not reflected in the gap map. The Skills Profile page already computes a more accurate merged score but that logic isn't reused here.

---

## 🟢 LOW Issues

### L1 — `call_type="coach_note"` not in TDD §3.4 allowed values

**File**: [utils/ai.py:305](utils/ai.py#L305)

**TDD reference**: §3.4 — `call_type` values: `'diagnostic_scoring' | 'gap_map' | 'coach_response' | 'evaluation_scoring'`

`generate_module_coach_note()` uses `call_type="coach_note"`. Not a runtime error, but the monitoring queries in TDD §3.4 won't catch this type. Should be `"coach_note"` or added to the allowed list in the TDD.

---

### L2 — `reading_completed_at` is overwritten on re-read

**File**: [pages/04_Course_Module.py:332-341](pages/04_Course_Module.py#L332-L341)

The `UPDATE ... SET reading_completed_at = current_timestamp()` fires every time the user clicks "I've read this." If a user re-reads after completing, the timestamp resets. Low impact but `WHERE reading_completed_at IS NULL` would be more defensive.

---

### L3 — Level label gap: score 0.45 maps to neither range

**File**: [utils/scoring.py:8-14](utils/scoring.py#L8-L14)

```python
(0.0, 0.4, "Unaware"),
(0.5, 1.4, "Explorer"),
```
A score of exactly 0.41–0.49 falls through all ranges and returns `"Unaware"` by the final fallback. PRD §8.2 says "0.5–1.4 = Explorer" and "0.0–0.4 = Unaware" — there is a gap at 0.41–0.49. Fix: change `(0.0, 0.4, ...)` to `(0.0, 0.49, ...)` or use `<` comparisons instead of range tuples.

---

### L4 — `load_progress()` called uncached in Results fallback

**File**: [pages/04_Course_Module.py:718](pages/04_Course_Module.py#L718)

`load_progress()` is defined without `@st.cache_data` (unlike `load_course`, `load_reading`, etc.) and is called in the Results fallback path. On a page that shows the module score, this fires a fresh DB query on every rerun. Minor performance issue — consistent with the other data loaders using cache.

---

### L5 — Dead `<a href="#">` link in Home page summary card

**File**: [pages/03_Home.py:140-141](pages/03_Home.py#L140-L141)

The "View Full Profile →" text link uses `href="#" onclick="return false;"` — it is a non-functional anchor. The functional navigation button on line 146 (`view_profile_btn`) achieves the same purpose but is visually separate. The HTML anchor should either be removed or replaced with a Streamlit button using the correct styling.

---

### L6 — Welcome page guard always redirects to Diagnostic, ignoring actual user state

**File**: [pages/00_Welcome.py:26-33](pages/00_Welcome.py#L26-L33)

```python
if existing:
    st.session_state["user_state"] = "needs_diagnostic"
    st.switch_page("pages/01_Diagnostic.py")
```
If a user with an existing profile (who has completed the diagnostic and is in training) navigates directly to the Welcome URL, they are routed to the Diagnostic page instead of Home. The guard should call `get_user_state()` and route accordingly (as `app.py` does). In practice, `app.py` handles routing on the main entry point, so this only matters for direct URL access to `00_Welcome.py`.

---

### L7 — `databricks.yml` missing `seed_03_diagnostic_items` job

**File**: [databricks.yml](databricks.yml)

`notebooks/03_seed_diagnostic_items.py` exists but is not registered as a bundle job. Must be added before the diagnostic flow can be tested end-to-end.

---

## Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| H1 | 🔴 HIGH | Skills Profile, Home | Domain scores: average-of-averages not equal-weight per item |
| H2 | 🔴 HIGH | utils/ai.py | MCQ items sent to LLM; `score_mcq()` never called |
| H3 | 🔴 HIGH | utils/ai.py | `score_evaluation` asks LLM for aggregates; inconsistent with `score_diagnostic` |
| M1 | 🟡 MEDIUM | utils/ai.py | Token counts never populated in `ai_call_log` |
| M2 | 🟡 MEDIUM | pages/01, 04 | Learner writes use inline SQL + escape() not parameterized queries |
| M3 | 🟡 MEDIUM | pages/01, 04 | `started_at` = `completed_at` in sessions; duration data lost |
| M4 | 🟡 MEDIUM | pages/04 | Results fallback: `result_domain_score = result_score` (wrong column) |
| M5 | 🟡 MEDIUM | pages/04 | Gap map after evaluation uses partial domain scores (diagnostic baseline only) |
| L1 | 🟢 LOW | utils/ai.py | `call_type="coach_note"` not in TDD allowed values |
| L2 | 🟢 LOW | pages/04 | `reading_completed_at` overwritten on re-read |
| L3 | 🟢 LOW | utils/scoring.py | Level label gap at score 0.41–0.49 |
| L4 | 🟢 LOW | pages/04 | `load_progress()` uncached; extra DB call in Results fallback |
| L5 | 🟢 LOW | pages/03 | Dead `<a href="#">` link in Home summary card |
| L6 | 🟢 LOW | pages/00 | Welcome guard routes all existing users to Diagnostic |
| L7 | 🟢 LOW | databricks.yml | Missing `seed_03_diagnostic_items` job definition |
