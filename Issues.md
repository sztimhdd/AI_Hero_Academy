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

## Open Issues

### NX10 — `data-testid` CSS selectors are Streamlit-version-fragile

**File**: [utils/styles.py](utils/styles.py) (throughout)

**Severity**: 🟢 LOW

**What's wrong**: At least 12 CSS rules target `data-testid` attributes (e.g., `section[data-testid="stSidebar"]`, `div[data-testid="stInfo"]`, `[data-testid="stMetric"]`, `[data-testid="stButton"]`). These are Streamlit internal test IDs, not a public API, and can be renamed in any Streamlit release.

**Expected**: Where possible, replace `data-testid` selectors with Streamlit's public class names or use CSS custom properties via `config.toml [theme]`. For the sidebar specifically, use `st.sidebar` context and rely on theme colours — not CSS overrides on internal test IDs.

---

## Closed Issues

| ID | Severity | Description | Resolution |
| --- | --- | --- | --- |
| H1 | 🔴 HIGH | Domain scores: average-of-averages not equal-weight per item | Fixed — `compute_current_domain_scores()` now called in both Skills Profile and Home pages |
| H2 | 🔴 HIGH | MCQ items sent to LLM; `score_mcq()` never called | Fixed — `_score_batch()` now scores MCQ locally via `score_mcq()`; LLM only receives open-ended items |
| H3 | 🔴 HIGH | `score_evaluation` asked LLM for aggregates; inconsistent with `score_diagnostic` | Fixed — `score_evaluation()` now mirrors `score_diagnostic()`: uses `_score_batch()` per domain, aggregates computed in Python |
| NX1 | 🔴 HIGH | Practice chat used custom HTML divs instead of `st.chat_message()` + `st.chat_input()` | Fixed (Phase 7.2) — replaced with `st.chat_message("user")` / `st.chat_message("assistant")` context managers and `st.chat_input()`; native ARIA, auto-scroll, theme-consistent |
| NX2 | 🔴 HIGH | Global `.stButton > button` CSS override destroyed `type="primary"` vs `type="secondary"` affordance | Fixed (Phase 7.1) — removed `background-color` from `.stButton > button` in `utils/styles.py`; `primaryColor` in `config.toml` now drives primary button colour correctly |
| CX1 | 🔴 HIGH | No exit navigation during Diagnostic — user trapped until all 12 questions answered | Fixed — added `← Exit` button to orientation screen (returning users only) and to quiz header; both clear session state and navigate to `pages/03_Home.py` |
| M1 | 🟡 MEDIUM | Token counts never populated in `ai_call_log` | Fixed — `call_llm()` extracts `resp.usage.prompt_tokens` / `resp.usage.completion_tokens` and passes to `_log_call()` |
| M2 | 🟡 MEDIUM | `training_progress` UPDATE used inline float interpolation for `evaluation_score` and `domain_score_after` | Fixed — both values moved to parameterised placeholders `?`; parameter list updated to `[eval_score, domain_score_after, progress_id]` |
| M3 | 🟡 MEDIUM | `started_at` = `completed_at` in sessions; duration data lost | Fixed — `coach_sessions` and `diagnostic_sessions` both use session-state timestamps for `started_at` and `current_timestamp()` for `completed_at` |
| M4 | 🟡 MEDIUM | Results fallback: `result_domain_score = result_score` (wrong column) | Fixed — fallback now reads `progress.get("domain_score_after")` from the already-loaded `progress` variable |
| M5 | 🟡 MEDIUM | Gap map after evaluation uses partial domain scores (diagnostic baseline only) | Fixed — `complete_evaluation()` now calls `load_all_progress()` + `compute_current_domain_scores()` to build fully merged scores before generating the gap map |
| NX3 | 🟡 MEDIUM | Assessment History used raw HTML `<table>` instead of `st.dataframe()` | Fixed (Phase 7.3) — `pages/02_Skills_Profile.py` now builds a `pandas.DataFrame` and renders with `st.dataframe(use_container_width=True, hide_index=True)` |
| NX4 | 🟡 MEDIUM | Score/metric displays used custom HTML instead of `st.metric()` | Fixed (Phase 7.4) — Results sub-view score hero now uses `st.metric()`; `[data-testid="stMetric"]` CSS in `styles.py` provides card styling |
| NX5 | 🟡 MEDIUM | Domain score bars used custom HTML instead of `st.progress()` | Fixed (Phase 7.5) — `score_bar()` replaced with `st.columns` + `st.progress(value / 4.0, text=label)`; native `role="progressbar"` ARIA semantics |
| NX6 | 🟡 MEDIUM | 30–96 "Invalid color" console warnings per page load for `widgetBackgroundColor`, `widgetBorderColor`, `skeletonBackgroundColor` | Fixed (Phase 7.6) — root cause: Streamlit JS emits warnings when these deprecated internal tokens are absent (GitHub #13831). Added all three to `.streamlit/config.toml` with design-system hex values (`#1E2330`, `#2A2F3E`); visual no-ops since CSS overrides take precedence |
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
| NX11 | 🟢 LOW | Module card `:has()` + adjacent sibling CSS was structurally fragile | Fixed (Phase 7.10) — module cards refactored as `st.container(border=True)` with `st.button()` inside; cross-element CSS dependency eliminated |
| U0 | 🟢 LOW | `.block-container max-width: 900px` — initially flagged as whitespace issue | Accepted — 900px readable-content width is Streamlit's intentional default for `layout="wide"`; design system colors moved to `.streamlit/config.toml [theme]`; CSS injection now limited to custom components only |
| U2 | 🟢 LOW | Home module card layout unverified (no training_progress rows for UAT user) | Verified Feb 2026 via Playwright — Module 1 active (cyan border, sub-badges, CTA); Modules 2-5 locked (greyed, lock icon, no CTA). 12px gap between card HTML and Streamlit button is framework's native element spacing — structural constraint, accepted as-is |
