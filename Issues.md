# Issues.md — AI Hero Academy MVP

**Code Review Against TDD.md and PRD.md**
Date: February 2026 | Reviewer: Claude Code
Last validated: February 2026

---

## Severity Legend

| Symbol | Meaning |
| ------ | ------- |
| 🔴 HIGH | Incorrect behaviour, wrong scores, broken TDD contract |
| 🟡 MEDIUM | Deviates from TDD spec, missing data, suboptimal but not wrong |
| 🟢 LOW | Minor UX gap, cosmetic, or TDD wording mismatch |

---

## MCQ Quality Standard (applies to PR-RM through PR-MK)

Trainer review (2026-03-17) of three sampled RM scenarios surfaced two defect categories beyond word length. **All four role rewrites (Phases 2–5) must satisfy all three checks before a scenario is considered fixed:**

**Check 1 — Label length**: every option label ≤ 10 words. Verifiable by script.

**Check 2 — Distractor realism**: each wrong option must represent a shortcut or misconception a busy, well-intentioned professional would genuinely consider under time pressure. "Plausible-but-sloppy" is the target, not "obviously wrong." The coach must be able to name the distractor's flaw in one sentence.

**Check 3 — Task alignment (most commonly violated)**: the best answer must directly address the specific situation described in *that task's text* — not re-state a general framework principle that belongs to an earlier task. Re-read the task text before writing any option. Ask: "Does selecting the best answer here prove the learner understood *this* task's objective?" If no, the options must be rewritten from scratch.

**Confirmed broken instance (already corrected in RM rewrite)**: `rm_c4_relationship_intel` Task 2 — the task asks the learner to add a source-citation verification requirement after an unverifiable hallucination appeared in the AI draft brief. The auto-generated best answer was "Structure prompt with relationship context and clear deliverable" — a general Task 1 principle that teaches nothing about catching hallucinations. Corrected to "Add a citation requirement: every claim must name its source." The same drift pattern may exist in UW/AN/MK and must be actively caught during those phases.

---

## Open Issues

| ID | Severity | Description |
| --- | --- | --- |
| LG-1b | 🟡 MEDIUM | Practice — Logic: `[ADVANCE]` sentinel never emitted in practice. The `_OPEN_TASK_MASTERY_ADDENDUM` instructs the coach to append `[ADVANCE]` when mastery is demonstrated, but the coach's "always probe deeper" discipline (added in BUG-3 fix) overrides this — it keeps finding new dimensions to probe rather than recognising task-objective completion. **Root cause**: the BUG-3 addendum ("Do not wrap up… always end with a probing follow-up question until the turn limit") explicitly contradicts the mastery signal instruction. Fix: add a mastery-recognition exception to the BUG-3 addendum, or restructure so the mastery addendum takes precedence. Strip code is confirmed working; only the emit path is broken. |

---

## UAT Execution Log

| Date | Commit | Tester | Result |
| ---- | ------ | ------ | ------ |
| 2026-03-04 | `a311052` | `uat-test@edc.ca` | ✅ PASS — 13/13 scenarios |
| 2026-03-17 | `6780c91` | `uat-test@edc.ca` | ✅ PASS — Practice sub-view BUG-3, UX-P1, UX-P2, UI-1, LG-2 all verified via Playwright |
| 2026-03-17 | pending | `uat-test@edc.ca` | ✅ PASS — PR-SYS/PR-RM/PR-UW/PR-AN/PR-MK MCQ rework verified: 252 labels ≤10 words (0 failures); ✅/❌ correctness signal renders on Task 2; navigation warning is red `st.error()`; "Next Task →" CTA appears after MCQ feedback |
| 2026-03-17 | `6780c91` | `uat-test@edc.ca` | ⚠️ PARTIAL — LG-1 `[ADVANCE]` sentinel UAT (persona 3e, mk_c3_critical_eval, Task 1): **Strip confirmed** — `[ADVANCE]` text never visible in any displayed coach message across 9 turns. **Auto-advance NOT confirmed** — coach never emitted `[ADVANCE]` despite exemplary answers across all VERIFY dimensions; turn-limit fallback fired correctly at 3 turns per extension. Root cause: `_OPEN_TASK_MASTERY_ADDENDUM` not reliably followed by coach model — coach's "always probe deeper" discipline (from BUG-3 fix) appears to override mastery recognition. New issue logged as **LG-1b**. |

**Scenarios covered (2026-03-04):**
UAT-01 Welcome (RM) · UAT-02 Diagnostic (RM, 12q) · UAT-03 Skills Profile + gap map · UAT-04 Home Dashboard + 5 modules · UAT-05 Module Overview · UAT-06 Reading sub-view · UAT-07 AI Coach practice (4 turns) · UAT-08 Evaluation quiz (3 MCQ + 1 text) · UAT-09 Module Results + Delta writes · UAT-10 Module 2 unlock + Home refresh · UAT-11 Skills Profile post-evaluation · UAT-12 Retake Diagnostic (progress preserved) · UAT-13 UW role selector + UW Diagnostic Q1/Q2

**Scenarios covered (2026-03-17):**
Practice-01 Coach discipline (BUG-3): Task 1 open mode — coach reply ends with probing question, no wrap-up · Practice-02 Per-task isolation (UX-P1): Task 2 starts with clean empty chat after Task 1 skip · Practice-03 Turn-limit CTA position (UX-P2): CTA renders above chat history (code-verified) · Practice-04 Turn-limit label (UI-1): Task 4 turn-limit block shows "Complete Practice →" (code-verified) · Practice-05 MCQ mode (LG-2): Tasks 2–4 render 3 `st.button()` MCQ choices with no chat input; coach feedback appears after selection; "Next Task →" shown on Tasks 2–3; "Complete Practice →" shown on Task 4

---

## Closed Issues

| ID | Severity | Description | Resolution |
| --- | --- | --- | --- |
| PR-SYS | 🟡 MEDIUM | Practice — Prompt / UX (Systemic) | Fixed (2026-03-17) — **(1)** Anti-hallucination addendum ("Do NOT cite specific numbers … unless verbatim in scenario text") appended to MCQ FEEDBACK MODE addenda in `pages/04_Course_Module.py`. **(2)** MCQ correctness signal: post-answer buttons re-rendered as disabled `st.button()` with ✅ prefix on best answer and ❌ prefix on selected wrong answer. **(3)** Navigation warning: `st.warning()` replaced with `st.error()` (red banner). Playwright-verified (2026-03-17): ✅/❌ labels render correctly; `st.error()` confirmed in page code. |
| PR-RM | 🟡 MEDIUM | Practice — Content (RM, 7 scenarios) | Fixed (2026-03-17) — Full pedagogical review of all 21 RM MCQs. 11 Check 3 alignment failures corrected; all 63 labels trimmed to ≤10 words (0 failures). Key fixes: `rm_c1 T2` best = "Use abstracted ranges and sector context in the prompt"; `rm_c4 T2` best = "Require AI to label each item Confirmed or Needs Confirmation"; `rm_c4 T3` best = "Add guardrail: include only verified prior interactions for CFO". Verified via word-count script (0/63 labels >10 words) and Playwright live smoke test. |
| PR-UW | 🟡 MEDIUM | Practice — Content (UW, 7 scenarios) | Fixed (2026-03-17) — Full pedagogical review of all 21 UW MCQs. 16 Check 1 + 16 Check 3 failures corrected; all 63 labels ≤10 words. Key fixes: `uw_c2 T3` best = "Add constraints focusing AI on liquidity and working capital"; `uw_c4 T2` best = "Apply RELATE: acknowledge frustration without conceding an error"; `uw_c5 T2` best = "Structure the prompt to request a four-part SIFT analysis". Verified via word-count script (0/63 labels >10 words). |
| PR-AN | 🟡 MEDIUM | Practice — Content (AN, 7 scenarios) | Fixed (2026-03-17) — Full pedagogical review of all 21 AN MCQs. 20/21 MCQs had at least one failure; all corrected. All 63 labels ≤10 words. Key fixes: `an_c4 T3` best = "Write a CRAF prompt for BD Leadership analytical priorities"; `an_c5 T4` best = "Replace the client name and exact figure with abstracted values"; `an_c7 T3` best = "Apply STAKE to draft the summary for the risk subcommittee". Verified via word-count script (0/63 labels >10 words). |
| PR-MK | 🟡 MEDIUM | Practice — Content (MK, 7 scenarios) | Fixed (2026-03-17) — Full pedagogical review of all 21 MK MCQs (worst affected: 54/63 labels >10 words pre-fix). All corrected; all 63 labels ≤10 words. Key fixes: `mk_c2 T4` best = "Add tone constraints prohibiting capitals, emojis, and superlatives"; `mk_c5 T3` best = "Override the AI interpretation using the CEO viral moment context"; `mk_c7 T4` best = "Draft bilingually with Copilot; apply full human review before presenting". Verified via word-count script (0/63 labels >10 words). |
| LG-1 | 🟡 MEDIUM | Practice — Logic: no mastery signal from coach | Fixed (2026-03-17) — added `_OPEN_TASK_MASTERY_ADDENDUM` to open-task system prompt in `pages/04_Course_Module.py`; instructs coach to append `[ADVANCE]` when the learner clearly demonstrates mastery. After each open-task reply, `[ADVANCE]` is stripped before display; if detected, `_advance_task()` (Tasks 1–3) or `do_complete_practice()` (Task 4) fires automatically without a manual click. Turn-limit path unchanged as fallback. ⚠️ UAT 2026-03-17: strip confirmed; `[ADVANCE]` never emitted — see open issue LG-1b. |
| BUG-3 | 🔴 HIGH | Coach declares session complete before turn limit fires | Fixed (2026-03-17) — appended "Do not wrap up, summarize, or offer to end the session. Always end your response with a probing follow-up question until the turn limit is reached." to CONVERSATION DISCIPLINE block in all 28 `coach_system_prompt` fields in `content/practice_scenarios.json`. Playwright-verified: coach ends Task 1 turn with a probing question. |
| UX-P1 | 🔴 HIGH | All task chat histories accumulate on screen — no per-task isolation | Fixed (2026-03-17) — replaced flat `coach_messages` list with `coach_messages_by_task` dict keyed by `task_idx`; per-task sub-list fetched on each render; `mcq_answered_by_task` dict added in parallel. Playwright-verified: Task 2 starts with empty chat after Task 1 skip. |
| UX-P2 | 🔴 HIGH | Turn-limit CTA buried below full accumulated chat history | Fixed (2026-03-17) — turn-limit warning + Continue/Next buttons now rendered **before** the chat history loop in the open-task branch of `pages/04_Course_Module.py`. Code-verified. |
| UI-1 | 🟢 LOW | "Next Task →" shown on Task 4 turn-limit block instead of "Complete Practice →" | Fixed (2026-03-17) — turn-limit block now checks `task_idx >= 3` and uses correct label; mirrors the post-reply CTA logic. Code-verified. |
| LG-2 | 🔴 HIGH | All 4 practice tasks required open-ended typing — no MCQ option | Fixed (2026-03-17) — `task_modes` and `task_mcq_options` fields added to all 28 scenario entries via `scripts/add_mcq_options.py`; `pages/04_Course_Module.py` branches on `current_task_mode == "mcq"` to render 3 `st.button()` choices instead of `st.chat_input()` for Tasks 2–4; MCQ feedback mode addendum injected into coach system prompt at call time. Playwright-verified: Task 1 open, Tasks 2–4 MCQ buttons; coach feedback appears; correct CTA labels on all tasks. |
| H1 | 🔴 HIGH | Domain scores: average-of-averages not equal-weight per item | Fixed — `compute_current_domain_scores()` now called in both Skills Profile and Home pages |
| H2 | 🔴 HIGH | MCQ items sent to LLM; `score_mcq()` never called | Fixed — `_score_batch()` now scores MCQ locally via `score_mcq()`; LLM only receives open-ended items |
| H3 | 🔴 HIGH | `score_evaluation` asked LLM for aggregates; inconsistent with `score_diagnostic` | Fixed — `score_evaluation()` now mirrors `score_diagnostic()`: uses `_score_batch()` per domain, aggregates computed in Python |
| NX1 | 🔴 HIGH | Practice chat used custom HTML divs instead of `st.chat_message()` + `st.chat_input()` | Fixed (Phase 7.2) — replaced with `st.chat_message("user")` / `st.chat_message("assistant")` context managers and `st.chat_input()`; native ARIA, auto-scroll, theme-consistent |
| NX2 | 🔴 HIGH | Global `.stButton > button` CSS override destroyed `type="primary"` vs `type="secondary"` affordance | Fixed (Phase 8.1) — added `[data-testid="stBaseButton-secondary"] button` CSS block in `utils/styles.py` with `transparent` background, muted border, and hover state; secondary buttons now visually distinct from primary cyan CTA |
| CX1 | 🔴 HIGH | No exit navigation during Diagnostic — user trapped until all 12 questions answered | Fixed — added `← Exit` button to orientation screen (returning users only) and to quiz header; both clear session state and navigate to `pages/03_Home.py` |
| M1 | 🟡 MEDIUM | Token counts never populated in `ai_call_log` | Fixed — `call_llm()` extracts `resp.usage.prompt_tokens` / `resp.usage.completion_tokens` and passes to `_log_call()` |
| M2 | 🟡 MEDIUM | `training_progress` UPDATE used inline float interpolation for `evaluation_score` and `domain_score_after` | Fixed — both values moved to parameterised placeholders `?`; parameter list updated to `[eval_score, domain_score_after, progress_id]` |
| M3 | 🟡 MEDIUM | `started_at` = `completed_at` in sessions; duration data lost | Fixed — `coach_sessions` and `diagnostic_sessions` both use session-state timestamps for `started_at` and `current_timestamp()` for `completed_at` |
| M4 | 🟡 MEDIUM | Results fallback: `result_domain_score = result_score` (wrong column) | Fixed — fallback now reads `progress.get("domain_score_after")` from the already-loaded `progress` variable |
| M5 | 🟡 MEDIUM | Gap map after evaluation uses partial domain scores (diagnostic baseline only) | Fixed — `complete_evaluation()` now calls `load_all_progress()` + `compute_current_domain_scores()` to build fully merged scores before generating the gap map |
| NX3 | 🟡 MEDIUM | Assessment History used raw HTML `<table>` instead of `st.dataframe()` | Fixed (Phase 7.3) — `pages/02_Skills_Profile.py` now builds a `pandas.DataFrame` and renders with `st.dataframe(use_container_width=True, hide_index=True)` |
| NX4 | 🟡 MEDIUM | Score/metric displays used custom HTML instead of `st.metric()` | Fixed (Phase 7.4) — Results sub-view score hero now uses `st.metric()`; `[data-testid="stMetric"]` CSS in `styles.py` provides card styling |
| NX5 | 🟡 MEDIUM | Domain score bars used custom HTML instead of `st.progress()` | Fixed (Phase 7.5) — `score_bar()` replaced with `st.columns` + `st.progress(value / 4.0, text=label)`; native `role="progressbar"` ARIA semantics |
| NX6 | 🟡 MEDIUM | 30–96 "Invalid color" console warnings per page load for `widgetBackgroundColor`, `widgetBorderColor`, `skeletonBackgroundColor` | Upstream limitation (Phase 8.2) — root cause confirmed as Streamlit issue #13831: JS sidebar theme doesn't inherit these deprecated tokens from `config.toml`. Tokens are already set in config.toml (best-effort); 3 warnings per page persist, are non-blocking, and cannot be suppressed without patching Streamlit's JS bundle. Accepted. |
| BUG-1 | 🟡 MEDIUM | `gap_maps` table not written after diagnostic completion — AI call succeeds but gap map not persisted | Fixed (Phase 8.3) — root cause: `generate_gap_map()` did a hard `result["gap_bullets"]` that raised `KeyError` when the LLM returned a key variant (e.g. `"bullets"`); silently swallowed by `except Exception: pass`. Fixed in `utils/ai.py`: resilient `.get("gap_bullets") or .get("bullets") or []`. Fixed in `pages/01_Diagnostic.py`: `except` now logs to stderr instead of silently passing. |
| CX2 | 🟡 MEDIUM | Sidebar navigation different on every page — no persistent chrome | Fixed — pages 02–04 now consistently show `🏠 My Training` + `🏅 Skills Profile`; Course Module additionally shows module context block |
| CX3 | 🟡 MEDIUM | "📚 My Course" button on Skills Profile silently bounced to Home (active_course_id not set) | Fixed — button now looks up the active (unlocked, incomplete) module from `progress_rows`, sets `st.session_state["active_course_id"]` and `active_submodule = "overview"` before navigating |
| CX4 | 🟡 MEDIUM | No breadcrumbs or wayfinding trail in Course Module | Fixed — breadcrumb row added at top of `pages/04_Course_Module.py` before all sub-views: `← My Training` button + `Module N: {title} / {sub-view}` text |
| U1 | 🟡 MEDIUM | Pre-diagnostic orientation screen missing — users saw Q1 with no context | Fixed — orientation card added to `pages/01_Diagnostic.py` guarded by `st.session_state["diag_started"]`; retake path in `02_Skills_Profile.py` also clears the flag |
| U3 | 🟡 MEDIUM | UX audit pending for Home and Course Module pages | Closed (Phase 6.4 + 6.5, Feb 2026) — full Playwright audit of both pages complete; all PRD §7.4/§7.5 checks passed; one new bug extracted as U5 |
| U4 | 🟡 MEDIUM | MCQ `st.radio()` defaulted to Option A; `disabled` guard on "Next →" never fired | Fixed — added `index=None` to `st.radio()` in `pages/01_Diagnostic.py`; user must now make an explicit selection before "Next →" enables |
| U5 | 🟡 MEDIUM | Evaluation MCQ `st.radio()` missing `index=None`; submit button guard never fired | Fixed (Phase 6.5 audit, Feb 2026) — added `index=None` to `st.radio()` in `pages/04_Course_Module.py:595`; mirrors the U4 fix in `01_Diagnostic.py` |
| L1 | 🟢 LOW | `call_type="coach_note"` not in TDD §3.4 allowed values | Fixed — `generate_module_coach_note()` in `utils/ai.py` now uses `call_type="coach_response"` |
| L2 | 🟢 LOW | `reading_completed_at` overwritten on re-read | Fixed — UPDATE now uses `WHERE progress_id = ? AND reading_completed_at IS NULL` |
| L3 | 🟢 LOW | Level label gap at score 0.41–0.49 | Fixed — `LEVEL_LABELS` range changed to `(0.0, 0.49, "Unaware")` |
| L4 | 🟢 LOW | `load_progress()` uncached; extra DB call in Results fallback | Fixed — Results fallback uses the `progress` variable loaded at page start; no extra DB call |
| L5 | 🟢 LOW | Dead `<a href="#">` link in Home summary card | Fixed — replaced with a Streamlit button (`st.button("→  View Full Skills Profile", ...)`) |
| L6 | 🟢 LOW | Welcome guard routes all existing users to Diagnostic | Fixed — guard now checks for completed diagnostic session and training_progress, routing to Diagnostic / Skills Profile / Home as appropriate |
| L7 | 🟢 LOW | Missing `seed_03_diagnostic_items` job in `databricks.yml` | Resolved by architecture change — all content is now served from JSON files in `content/`; no Delta seeding required for content tables |
| CX5 | 🟢 LOW | Results page: two equal-weight CTAs, one duplicate when all modules complete | Fixed — `col_a` "View Updated Skills Profile →" is hidden when `all_complete=True`; `col_b` remains as the single primary CTA |
| CX6 | 🟢 LOW | Skills Profile under-signposted from Home page | Fixed — "→ View Full Skills Profile" button elevated to `type="primary"` in `pages/03_Home.py` |
| CX7 | 🟢 LOW | Display name derived from email and never confirmed by user | Fixed — `pages/00_Welcome.py` now shows an editable `st.text_input` pre-filled with the derived name; user can correct before creating profile |
| CX8 | 🟢 LOW | Role selector was a single-option dropdown signalling an unfinished UI | Fixed — when `_available_roles` has one entry, a static `st.info()` card replaces the selectbox; `selected_role` is pre-set, enabling the CTA immediately |
| CX9 | 🟢 LOW | No navigation warning before leaving an in-progress practice session | Fixed — `st.warning()` banner added at top of Practice sub-view in `pages/04_Course_Module.py` advising that navigating away discards the session |
| CX10 | 🟢 LOW | "Home" page label counterintuitive — page is a course dashboard, not a landing page | Fixed — `page_title` in `pages/03_Home.py` updated to `"My Training \| AI Hero Academy"`; sidebar labels across pages 02 and 04 updated to `"🏠 My Training"` |
| NX7 | 🟢 LOW | Reading content boxes used custom HTML instead of Streamlit callout components | Fixed (Phase 7.9) — "Good Example", "Common Mistake", and "Key Takeaway" boxes replaced with `st.success()`, `st.error()`, and `st.info()`; confirmed as native `alert` elements in Playwright accessibility tree |
| NX8 | 🟢 LOW | HTML spacer divs (`height:Xrem`) used throughout all pages | Fixed (Phase 7.7) — all `st.markdown("<div style='height:Xrem'>")` spacers removed; grep confirms zero instances remain |
| NX9 | 🟢 LOW | Page headers used `st.markdown('<h1>')` instead of `st.title()` | Fixed (Phase 7.8) — `st.title()` used in `pages/02_Skills_Profile.py` and all sub-views of `pages/04_Course_Module.py` |
| NX10 | 🟢 LOW | `data-testid` CSS selectors are Streamlit-version-fragile (12 rules) | Fixed — 7 selectors migrated to stable class names: `section.stSidebar` (3 rules), `.stMetric`, `.stMetricLabel`, `.stMetricValue`; 5 `data-testid` rules retained for `stHeader` + alert variants (`stInfo`/`stSuccess`/`stWarning`/`stError`) — no stable public class exists for these; all retained rules have explanatory comments |
| NX11 | 🟢 LOW | Module card `:has()` + adjacent sibling CSS was structurally fragile | Fixed (Phase 7.10) — module cards refactored as `st.container(border=True)` with `st.button()` inside; cross-element CSS dependency eliminated |
| U0 | 🟢 LOW | `.block-container max-width: 900px` — initially flagged as whitespace issue | Accepted — 900px readable-content width is Streamlit's intentional default for `layout="wide"`; design system colors moved to `.streamlit/config.toml [theme]`; CSS injection now limited to custom components only |
| U2 | 🟢 LOW | Home module card layout unverified (no training_progress rows for UAT user) | Verified Feb 2026 via Playwright — Module 1 active (cyan border, sub-badges, CTA); Modules 2-5 locked (greyed, lock icon, no CTA). 12px gap between card HTML and Streamlit button is framework's native element spacing — structural constraint, accepted as-is |
| P1 | 🟡 MEDIUM | Per-task turn limit offers no "continue" option — forced skip only | Fixed (Phase 11) — replaced forced "Next Task →" at the turn limit with a two-button prompt: "Continue (3 more turns) →" increments `task_extra_{task_idx}` session state to extend the effective limit by 3; "Next Task →" (primary) advances `practice_task_idx`. `MAX_TASK_TURNS` constant unchanged. |
| P2 | 🟡 MEDIUM | "Complete Practice →" banner reference misleads at session start | Fixed (Phase 11) — banner copy updated to remove the button reference; new wording: "⚠️ Navigating away via the sidebar or breadcrumb will end your session without saving your practice conversation." |
| NAV1 | 🟡 MEDIUM | Inconsistent sidebar navigation — different buttons on every page | Fixed (Phase 11) — extracted `render_sidebar(active_page, has_course, progress_rows, active_course_id, module_context)` utility in `utils/styles.py`; all 3 pages (Home, Skills Profile, Course Module) now render the same 3 nav buttons (My Training · Skills Profile · My Course); active-page button is disabled; CX3 look-up logic consolidated into the utility. |
| NAV2 | 🟢 LOW | Streamlit sidebar collapse button bleeds through as text | Fixed (Phase 11, corrected in UAT) — added `[data-testid="stSidebarCollapseButton"] { display: none !important; }` to `inject_global_css()` in `utils/styles.py`; sidebar is always expanded so hiding the toggle is safe. Note: original fix incorrectly targeted `collapsedControl` (testid does not exist in this Streamlit version); UAT confirmed the actual wrapper testid is `stSidebarCollapseButton`. |
| UI1 | 🟢 LOW | Zero-pixel gap between sub-badges and action button on course cards | Fixed (Phase 11) — added `margin-bottom: 0.75rem` to the `.sub-strip` CSS rule in `utils/styles.py`, creating visible separation between the Read/Practice/Quiz badge strip and the action button below. |
| UI2 | 🟢 LOW | "Review Module" requires two clicks to reach results | Fixed (Phase 11) — "Review Module" button handler in `pages/03_Home.py` now checks all three completion timestamps (`reading_completed_at`, `practice_completed_at`, `evaluation_completed_at`); sets `active_submodule = "results"` when all three are set, otherwise `"overview"`. |
| BUG-2 | 🟡 MEDIUM | `gap_maps.bullets` column may contain plain strings — `AttributeError: 'str' object has no attribute 'get'` on Skills Profile | Fixed (UAT) — root cause: early gap map generations (pre-BUG-1 fix) stored strings `["Domain (score): text", ...]` instead of dicts. Fixed in `pages/02_Skills_Profile.py`: added `isinstance(b, dict)` filter on the bullets list before sorting and rendering. No data migration needed — stale records are overwritten after the next evaluation. |
| Phase9.5 | 🟡 MEDIUM | Full UW learner journey acceptance tests — blocked on Task 9.4 | Closed (UAT-13, March 2026) — UW welcome → diagnostic → skills profile → build course → module 1 all confirmed; UW-specific questions and content verified end-to-end. |
| HEX-1 | 🟡 MEDIUM | Platform domain taxonomy expansion — 4-domain/5-course → 6-domain/7-course architecture required for new role content generation | Closed (Phase 12, March 2026) — all 11 hexagon refactor tasks complete; platform constants, content pipeline, prompt files, skills profile hexagon viz, and copilot-course-design-brief.md all updated; backward compatible with existing RM/UW 4-domain content; 33/33 tests passing. |
