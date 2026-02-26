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

## CX / UX Journey Audit

> Findings from a full customer-journey review (February 2026) covering first-visit and return-visit flows, sidebar navigation consistency, breadcrumbs, and page-level affordances across all 5 pages.

---

### CX1 — No exit navigation during Diagnostic

**Files**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

**Severity**: 🔴 HIGH

**What's wrong**: Once a user clicks "Start Assessment →" the entire Diagnostic page renders with `initial_sidebar_state="collapsed"` and zero navigation links. There is no "Home", no "← Back", and no "Save & exit" option for the full 12-question flow. A returning user who lands here by accident (bookmark, browser back, stale redirect) is trapped until all questions are answered or the tab is closed.

**Expected**: Add a discreet "← Exit assessment" link in the orientation screen and an equally discreet "← Home" link in the header during the quiz. Wire it to `st.switch_page("pages/03_Home.py")` with a Streamlit `st.warning` confirmation. Session state is already discarded on re-entry, so data loss is minimal and by design.

---

### CX2 — Sidebar navigation is different on every page (no persistent chrome)

**Files**: all pages

**Severity**: 🟡 MEDIUM

**What's wrong**: There is no stable set of navigation destinations that appears on all pages. Each page defines its own arbitrary subset:

| Page | Sidebar buttons |
| ---- | --------------- |
| Welcome (00) | None (collapsed) |
| Diagnostic (01) | None (collapsed) |
| Skills Profile (02) | 🏠 Home · 📚 My Course |
| Home (03) | 🏅 Skills Profile |
| Course Module (04) | ← Back to Course List · 🏅 Skills Profile |

Users cannot predict where to find navigation. A user on the Home page has no sidebar path to Diagnostic. A user on Skills Profile has no breadcrumb trail. Users who learn navigation on one page must re-learn it on the next.

**Expected**: Standardise the sidebar for all post-onboarding pages (02–04) to always include: Home, Skills Profile, and (within Course Module) the module context block. Welcome and Diagnostic may remain collapsed.

---

### CX3 — "📚 My Course" sidebar button on Skills Profile bounces silently to Home

**File**: [pages/02_Skills_Profile.py:139-140](pages/02_Skills_Profile.py#L139-L140)

**Severity**: 🟡 MEDIUM

**What's wrong**: The sidebar button labelled "📚  My Course" calls `st.switch_page("pages/04_Course_Module.py")`. Course Module guards on `active_course_id` in session state — if absent, it immediately redirects to Home. Since Skills Profile never sets `active_course_id`, clicking "My Course" from the sidebar navigates to Course Module, which silently redirects to Home. The user ends up on Home with no feedback.

**Expected**: Either (a) fix the button to navigate to Home directly (`st.switch_page("pages/03_Home.py")`) and relabel it "🏠  Home", or (b) look up the user's current in-progress module, set `st.session_state["active_course_id"]` and `st.session_state["active_submodule"] = "overview"`, then switch to Course Module.

---

### CX4 — No breadcrumbs or wayfinding trail anywhere

**Files**: [pages/03_Home.py](pages/03_Home.py), [pages/04_Course_Module.py](pages/04_Course_Module.py)

**Severity**: 🟡 MEDIUM

**What's wrong**: The deepest reachable state in the app is Home → Module 3 → Practice → Task 2. None of these levels is surfaced as a breadcrumb or persistent path indicator. Course Module shows a "Module X of 5" counter and a Read/Practice/Quiz step strip, but these appear inside the content area and do not show the user's position relative to the whole app. There is no "where am I?" affordance.

**Expected**: Add a breadcrumb row at the top of Course Module:
`Home / Module {N}: {title} / {sub-view}` — each segment a button link. Home and the module title are already available in session state.

---

### CX5 — Results page: two equal-weight CTAs, one is a duplicate when all modules complete

**File**: [pages/04_Course_Module.py:750-757](pages/04_Course_Module.py#L750-L757)

**Severity**: 🟢 LOW

**What's wrong**: The Results page places two buttons side by side with equal visual weight:

- `col_a`: "View Updated Skills Profile →" (always shown)
- `col_b`: "🏆 View Final Skills Profile →" OR "Start Module N →"

When all modules are complete, both buttons navigate to Skills Profile — the user sees two buttons with near-identical labels going to the same page. When modules remain, the two buttons have different destinations but equal styling, making the primary action (next module) indistinguishable from the secondary action (check profile).

**Expected**: Make the next-module / completion CTA `type="primary"` and the Skills Profile link `type="secondary"`, or move the Skills Profile link to the sidebar.

---

### CX6 — Skills Profile is under-signposted from the Home page

**File**: [pages/03_Home.py:192-193](pages/03_Home.py#L192-L193)

**Severity**: 🟢 LOW

**What's wrong**: Skills Profile is the primary analysis view (scores, gap map, full history), but from Home it is only accessible via: (a) a small secondary-style button "→ View Full Skills Profile" placed below the summary score card, and (b) a sidebar button labelled "🏅 Skills Profile". Neither is prominent. A user focused on the module cards will miss both.

**Expected**: Elevate the "View Full Skills Profile" button to `type="primary"` or reposition it alongside the score hero number in the summary card as a clear call-to-action.

---

### CX7 — Display name is derived from email and never confirmed by the user

**Files**: [pages/00_Welcome.py:153](pages/00_Welcome.py#L153), [pages/03_Home.py:91](pages/03_Home.py#L91)

**Severity**: 🟢 LOW

**What's wrong**: On first login, `display_name` is set to `user_email.split("@")[0].replace(".", " ").title()`. A user with email `hhu@edc.ca` is stored as "Hhu"; `j.smith@edc.ca` becomes "J Smith". The user is never shown what name was captured, and there is no way to correct it. Home page greets the user with this derived name ("Welcome back, Hhu.").

**Expected**: Show the derived name on the Welcome page below the role selector ("You'll be shown as: Hhu — [Edit]") with an optional text input, or add a profile name field on the Skills Profile page.

---

### CX8 — Role selector is a single-option dropdown

**File**: [pages/00_Welcome.py:133-140](pages/00_Welcome.py#L133-L140)

**Severity**: 🟢 LOW

**What's wrong**: The Welcome page presents a `st.selectbox` with options `["— Select your role —", "Relationship Manager"]`. A single real option in a dropdown signals an unfinished UI. Users may click the dropdown, see one choice, and wonder if the app is broken.

**Expected**: For MVP with one role, replace the dropdown with a pre-selected role card (non-interactive but visually styled): `"Your role: Relationship Manager"`. Keep the selectbox pattern in code for future role expansion but wrap it in a condition so it only renders as a dropdown when more than one role exists.

---

### CX9 — No navigation warning before leaving an in-progress practice session

**File**: [pages/04_Course_Module.py:161-175](pages/04_Course_Module.py#L161-L175)

**Severity**: 🟢 LOW

**What's wrong**: During Practice (coach conversation), the sidebar shows "← Back to Course List" and "🏅 Skills Profile" with no warning. Clicking either button navigates away immediately, discarding the entire in-memory conversation. The session is not saved until "Complete Practice →" is clicked. A user who accidentally clicks the sidebar loses all their coach turns with no warning.

**Expected**: The sidebar back/profile buttons in the `practice` sub-view should set a warning flag and show a `st.warning` banner: "Leaving now will end your practice session. Your turns are not saved mid-session." Alternatively, auto-save partial practice turns to `coach_sessions` with a `completed=false` flag (larger scope change).

---

### CX10 — "Home" page label is counterintuitive for new users

**File**: [pages/03_Home.py](pages/03_Home.py)

**Severity**: 🟢 LOW

**What's wrong**: The page named "Home" is a course progress dashboard — it shows module cards, a score summary, and a trend indicator. It is not a traditional entry/landing page. New users who complete the diagnostic and build a course are dropped here without explicit context that this is the app's ongoing dashboard. The Welcome page (the true entry page) is never seen again after onboarding.

**Expected**: Consider renaming the page to "Dashboard" or "My Training" in `st.set_page_config(page_title=...)` and updating sidebar labels accordingly. This is a low-effort clarity improvement.

---

## Native Component Audit

> Findings from a systematic review (February 2026) of all pages against Streamlit best practices:
> use native components instead of custom HTML/CSS; use `type="primary"` / `type="secondary"` for affordance hierarchy; prefer `st.metric()`, `st.dataframe()`, `st.chat_message()`, `st.progress()` over hand-rolled equivalents.
> NX1–NX9, NX11 resolved in Phase 7 (February 2026). NX10 remains as acknowledged technical debt.

---

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
| M1 | 🟡 MEDIUM | Token counts never populated in `ai_call_log` | Fixed — `call_llm()` extracts `resp.usage.prompt_tokens` / `resp.usage.completion_tokens` and passes to `_log_call()` |
| M3 | 🟡 MEDIUM | `started_at` = `completed_at` in sessions; duration data lost | Fixed — `coach_sessions` and `diagnostic_sessions` both use session-state timestamps for `started_at` and `current_timestamp()` for `completed_at` |
| M4 | 🟡 MEDIUM | Results fallback: `result_domain_score = result_score` (wrong column) | Fixed — fallback now reads `progress.get("domain_score_after")` from the already-loaded `progress` variable |
| M5 | 🟡 MEDIUM | Gap map after evaluation uses partial domain scores (diagnostic baseline only) | Fixed — `complete_evaluation()` now calls `load_all_progress()` + `compute_current_domain_scores()` to build fully merged scores before generating the gap map |
| NX3 | 🟡 MEDIUM | Assessment History used raw HTML `<table>` instead of `st.dataframe()` | Fixed (Phase 7.3) — `pages/02_Skills_Profile.py` now builds a `pandas.DataFrame` and renders with `st.dataframe(use_container_width=True, hide_index=True)` |
| NX4 | 🟡 MEDIUM | Score/metric displays used custom HTML instead of `st.metric()` | Fixed (Phase 7.4) — Results sub-view score hero now uses `st.metric()`; `[data-testid="stMetric"]` CSS in `styles.py` provides card styling |
| NX5 | 🟡 MEDIUM | Domain score bars used custom HTML instead of `st.progress()` | Fixed (Phase 7.5) — `score_bar()` replaced with `st.columns` + `st.progress(value / 4.0, text=label)`; native `role="progressbar"` ARIA semantics |
| NX6 | 🟡 MEDIUM | 30–96 "Invalid color" console warnings per page load for `widgetBackgroundColor`, `widgetBorderColor`, `skeletonBackgroundColor` | Fixed (Phase 7.6) — root cause: Streamlit JS emits warnings when these deprecated internal tokens are absent (GitHub #13831). Added all three to `.streamlit/config.toml` with design-system hex values (`#1E2330`, `#2A2F3E`); visual no-ops since CSS overrides take precedence |
| U1 | 🟡 MEDIUM | Pre-diagnostic orientation screen missing — users saw Q1 with no context | Fixed — orientation card added to `pages/01_Diagnostic.py` guarded by `st.session_state["diag_started"]`; retake path in `02_Skills_Profile.py` also clears the flag |
| U3 | 🟡 MEDIUM | UX audit pending for Home and Course Module pages | Closed (Phase 6.4 + 6.5, Feb 2026) — full Playwright audit of both pages complete; all PRD §7.4/§7.5 checks passed; one new bug extracted as U5 |
| U4 | 🟡 MEDIUM | MCQ `st.radio()` defaulted to Option A; `disabled` guard on "Next →" never fired | Fixed — added `index=None` to `st.radio()` in `pages/01_Diagnostic.py`; user must now make an explicit selection before "Next →" enables |
| U5 | 🟡 MEDIUM | Evaluation MCQ `st.radio()` missing `index=None`; submit button guard never fired | Fixed (Phase 6.5 audit, Feb 2026) — added `index=None` to `st.radio()` in `pages/04_Course_Module.py:595`; mirrors the U4 fix in `01_Diagnostic.py` |
| L2 | 🟢 LOW | `reading_completed_at` overwritten on re-read | Fixed — UPDATE now uses `WHERE progress_id = ? AND reading_completed_at IS NULL` |
| L3 | 🟢 LOW | Level label gap at score 0.41–0.49 | Fixed — `LEVEL_LABELS` range changed to `(0.0, 0.49, "Unaware")` |
| L4 | 🟢 LOW | `load_progress()` uncached; extra DB call in Results fallback | Fixed — Results fallback uses the `progress` variable loaded at page start; no extra DB call |
| L5 | 🟢 LOW | Dead `<a href="#">` link in Home summary card | Fixed — replaced with a Streamlit button (`st.button("→  View Full Skills Profile", ...)`) |
| L6 | 🟢 LOW | Welcome guard routes all existing users to Diagnostic | Fixed — guard now checks for completed diagnostic session and training_progress, routing to Diagnostic / Skills Profile / Home as appropriate |
| L7 | 🟢 LOW | Missing `seed_03_diagnostic_items` job in `databricks.yml` | Resolved by architecture change — all content is now served from JSON files in `content/`; no Delta seeding required for content tables |
| NX7 | 🟢 LOW | Reading content boxes used custom HTML instead of Streamlit callout components | Fixed (Phase 7.9) — "Good Example", "Common Mistake", and "Key Takeaway" boxes replaced with `st.success()`, `st.error()`, and `st.info()`; confirmed as native `alert` elements in Playwright accessibility tree |
| NX8 | 🟢 LOW | HTML spacer divs (`height:Xrem`) used throughout all pages | Fixed (Phase 7.7) — all `st.markdown("<div style='height:Xrem'>")` spacers removed; grep confirms zero instances remain |
| NX9 | 🟢 LOW | Page headers used `st.markdown('<h1>')` instead of `st.title()` | Fixed (Phase 7.8) — `st.title()` used in `pages/02_Skills_Profile.py` and all sub-views of `pages/04_Course_Module.py` |
| NX11 | 🟢 LOW | Module card `:has()` + adjacent sibling CSS was structurally fragile | Fixed (Phase 7.10) — module cards refactored as `st.container(border=True)` with `st.button()` inside; cross-element CSS dependency eliminated |
| U0 | 🟢 LOW | `.block-container max-width: 900px` — initially flagged as whitespace issue | Accepted — 900px readable-content width is Streamlit's intentional default for `layout="wide"`; design system colors moved to `.streamlit/config.toml [theme]`; CSS injection now limited to custom components only |
| U2 | 🟢 LOW | Home module card layout unverified (no training_progress rows for UAT user) | Verified Feb 2026 via Playwright — Module 1 active (cyan border, sub-badges, CTA); Modules 2-5 locked (greyed, lock icon, no CTA). 12px gap between card HTML and Streamlit button is framework's native element spacing — structural constraint, accepted as-is |
