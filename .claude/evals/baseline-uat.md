# Baseline UAT Eval — AI Hero Academy
<!-- eval-type: baseline | version: 1.0 | updated: 2026-03-23 -->

## Overview

Covers all 4 roles × 2 languages across every major flow state.
9 personas chosen for minimal redundancy: full flow tested on RM, smoke-tested on UW/AN/MK.

---

## Persona Matrix

| ID | Role | Lang | Reset Command | Entry State | Purpose |
|----|------|------|---------------|-------------|---------|
| P1 | — | en→zh | `(full wipe)` | Welcome | Welcome page + lang toggle |
| P2 | rm | en | `--role rm` | Diagnostic | Full RM diagnostic en |
| P3 | rm | zh | `--role rm` (then toggle zh) | Diagnostic | RM diagnostic zh strings |
| P4 | uw | en | `--role uw` | Diagnostic | UW role smoke |
| P5 | an | en | `--role an` | Diagnostic | AN role smoke |
| P6 | mk | en | `--role mk` | Diagnostic | MK role smoke |
| P7 | rm | en | `--role rm --diag` | Skills Profile | Skills Profile render |
| P8 | rm | en | `--profile course-built` | Home + Module | Module full flow en |
| P9 | rm | zh | `--profile course-built` (then toggle zh) | Home + Module | Module flow zh strings |

> **Note**: `--profile` fixtures are RM-only. UW/AN/MK Home-state testing deferred until
> `--profile` is extended to support multi-role in a future sprint.

---

## Pre-Run Checklist

```bash
# 1. App running?
curl -s -o /dev/null -w "%{http_code}" http://localhost:8501/  # expect 200

# If not, start it:
bash run_uat.sh &
sleep 5

# 2. Browser connected?
# Navigate to http://localhost:8501 with mcp__playwright__browser_navigate
```

---

## Test Groups

### G1: Welcome Page — P1 (full wipe)

**Reset**: `python scripts/reset_uat_user.py`

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 1.1 | Page renders without JS error | code | `browser_console_messages` shows no `[error]` entries |
| 1.2 | Role selector shows 4 options | snapshot | RM, UW, AN, MK all visible |
| 1.3 | Language toggle present in sidebar | snapshot | zh / 中文 option visible |
| 1.4 | Switch to zh | snapshot | Heading text changes to Chinese |
| 1.5 | Switch back to en | snapshot | Heading text reverts to English |
| 1.6 | Select RM + submit | snapshot | Redirects to Diagnostic page |

**Pass**: 6/6
**Acceptable**: 5/6 (non-blocking cosmetic only)

---

### G2: Diagnostic — P2 (full flow, RM en), P3 (zh smoke), P4/P5/P6 (role smoke)

#### G2a: Full flow — P2 (RM en)

**Reset**: `python scripts/reset_uat_user.py --role rm`

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 2.1 | Diagnostic page loads | snapshot | Progress indicator visible, Question 1 rendered |
| 2.2 | Question text is English | snapshot | English text in question body |
| 2.3 | Answer all 12 questions | manual | Navigate through all 12 using radio selections |
| 2.4 | Submit diagnostic | snapshot | Loading indicator appears, then redirects to Skills Profile |
| 2.5 | Skills Profile shows hexagon | snapshot | 6-domain hexagon with numeric scores visible |
| 2.6 | Gap map has 3 bullets | snapshot | 3 priority bullet points rendered |

**Pass**: 6/6

#### G2b: Lang smoke — P3 (RM zh)

**Reset**: `python scripts/reset_uat_user.py --role rm` → toggle to zh in sidebar

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 2.7 | Question text renders in Chinese | snapshot | Chinese characters visible in question body |
| 2.8 | Answer options render in Chinese | snapshot | Radio option labels are Chinese |
| 2.9 | No console errors after toggle | code | `browser_console_messages` clean |

**Pass**: 3/3

#### G2c: Role smoke — P4 (UW), P5 (AN), P6 (MK)

For each role run: `python scripts/reset_uat_user.py --role <role>`

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 2.10 | UW Diagnostic renders | snapshot | Question 1 loads, no error banner |
| 2.11 | AN Diagnostic renders | snapshot | Question 1 loads, no error banner |
| 2.12 | MK Diagnostic renders | snapshot | Question 1 loads, no error banner |

**Pass**: 3/3

---

### G3: Skills Profile — P7 (RM, post-diag)

**Reset**: `python scripts/reset_uat_user.py --role rm --diag`

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 3.1 | Hexagon renders with 6 scores | snapshot | All 6 domain scores visible |
| 3.2 | Domain score labels match domains | snapshot | responsible_ai, strategic_prompting, etc. present |
| 3.3 | Gap map section present | snapshot | Bullet list with ≥3 items |
| 3.4 | "Start Learning" / CTA button present | snapshot | Navigation to Home available |

**Pass**: 4/4

---

### G4: Home + Module Full Flow — P8 (RM en)

**Reset**: `python scripts/reset_uat_user.py --profile course-built`

#### G4a: Home Page

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 4.1 | Home loads with 7 module cards | snapshot | 7 cards visible |
| 4.2 | Module 1 is unlocked | snapshot | Module 1 CTA is clickable (not greyed) |
| 4.3 | Modules 2–7 show locked state | snapshot | Lock icon or greyed CTA on modules 2–7 |

#### G4b: Module Overview

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 4.4 | Click Module 1 → Overview tab | snapshot | Module title and "Start Reading" CTA visible |

#### G4c: Reading Sub-module

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 4.5 | Navigate to Reading tab | snapshot | Reading content renders (text or sections visible) |
| 4.6 | Complete Reading → mark complete | snapshot | Reading completion confirmed, Practice unlocked |

#### G4d: Practice (AI Coach)

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 4.7 | Practice tab loads Task 1 | snapshot | Task prompt visible, chat input present |
| 4.8 | Submit a coach message | snapshot | AI response appears within 30s |
| 4.9 | No `[error]` console entries | code | `browser_console_messages` clean |

#### G4e: Evaluation (Quiz)

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 4.10 | Evaluation tab loads 4 questions | snapshot | 3 MCQ + 1 open-ended question visible |
| 4.11 | Answer all 4 + submit | snapshot | Scoring spinner appears, then Results page |

#### G4f: Results

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 4.12 | Coach note rendered | snapshot | AI-generated coach note text visible |
| 4.13 | Score breakdown visible | snapshot | Numeric score and domain delta shown |
| 4.14 | Module 2 unlocked on Home | snapshot | Return to Home shows Module 2 unlocked |

**Pass**: 14/14
**Acceptable**: 12/14 (AI latency timeouts not counted as failures if retry succeeds)

---

### G5: Module Flow zh Strings — P9 (RM zh)

**Reset**: `python scripts/reset_uat_user.py --profile course-built` → toggle to zh

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| 5.1 | Module card labels in zh | snapshot | Chinese text on module cards |
| 5.2 | Module 1 Overview renders zh heading | snapshot | Chinese heading in module detail |
| 5.3 | Reading content renders (en fallback OK) | snapshot | No error; content visible (may be English fallback) |
| 5.4 | Practice task prompt in zh | snapshot | Chinese task description in coach area |
| 5.5 | No console errors throughout | code | `browser_console_messages` clean |

**Pass**: 5/5

---

## Execution Order

Run groups in this order for maximum dependency safety:

```
G1 (Welcome) → G2c (role smokes, parallel) → G2a (RM full diag) → G2b (zh diag)
→ G3 (Skills Profile) → G4 (Module full flow) → G5 (Module zh)
```

G2c (P4/P5/P6) can run in parallel using 3 separate browser tabs since each starts from a fresh reset.

---

## Metrics

| Group | Tests | Required Pass | Notes |
|-------|-------|---------------|-------|
| G1 | 6 | 5 | 1 cosmetic fail OK |
| G2a | 6 | 6 | Full flow — must pass |
| G2b | 3 | 3 | i18n regression |
| G2c | 3 | 3 | Role smoke |
| G3 | 4 | 4 | — |
| G4 | 14 | 12 | AI latency tolerance |
| G5 | 5 | 5 | i18n regression |
| **Total** | **41** | **38** | **pass@1 ≥ 93%** |

Release gate: **38/41** (pass@1). Any failure in G2a or G4 blocks release regardless of total score.

---

## Regression Eval Baseline

Run after every PR merge to `main`:

```bash
# Code graders (deterministic)
python -m pytest tests/ -q                                    # 40/40 expected
grep -r "calculate_domain_scores" utils/ tests/               # 0 hits expected (ARCH-1)
grep -n "call_type" utils/ai.py | grep -v "module_coach_note\|coach_response\|diagnostic_score\|evaluation_score\|gap_map"  # 0 unexpected types

# i18n completeness (NEW-4 — not yet implemented)
# python -m pytest tests/test_i18n_keys.py
```

---

---

## Group G: BYOW Diagnostic (Phase 5)

**Reset for all G7 tests:**
```bash
python scripts/reset_uat_user.py   # full wipe → Welcome page
```

**Run the app:**
```bash
bash run_uat.sh
```

**Playwright entry point:**
```python
mcp__playwright__browser_navigate(url="http://localhost:8501")
```

### G7 Test Cases

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| G7.1 | Diagnostic page shows 6 text_area prompts, no MCQ radio buttons | snapshot | 6 open text boxes visible, no radio elements |
| G7.2 | Submit button disabled when all responses are empty | snapshot | Button has `disabled` attribute |
| G7.3 | Submit button enabled after filling all 6 (≥20 chars each) | snapshot | Button is active/clickable |
| G7.4 | Scoring spinner appears on submit | snapshot | Spinner text visible after click |
| G7.5 | Skills Profile hexagon renders with 6 valid domain scores | snapshot | No zero or None scores in hexagon |
| G7.6 | Path assembles 7 modules on Home page | snapshot | 7 module cards visible |
| G7.7 | RM shortcut (Advanced Options) still works end-to-end | manual | Select RM → complete BYOW → valid path assembled |
| G7.8 | Unknown role text pasted → valid path, no errors | manual | Paste Sr. Technical Advisor JD → complete diagnostic → Home |
| G7.9 | No console errors throughout G7 flow | code | `browser_console_messages()` returns empty or non-error logs |

### G7 Score Summary

| Group | Total | Passing | Gate |
|-------|-------|---------|------|
| G7 (BYOW) | 9 | — | ≥ 8/9 to pass |

---

## Known Gaps (Deferred)

| Gap | Reason | Linked Issue |
|-----|---------|--------------|
| `--profile` for UW/AN/MK | Reset script only seeds RM courses | Extend in future sprint |
| zh scoring correctness | `lang` not threaded into `_score_batch` | NEW-2 (HIGH) |
| Evaluation input truncation | `MAX_USER_INPUT_CHARS` missing on eval `text_area` | NEW-5 (MEDIUM) |
| i18n key completeness test | No pytest coverage yet | NEW-4 (LOW) |
