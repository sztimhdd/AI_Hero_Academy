# Full-App UX Audit & Refactor Plan

> Generated: 2026-03-25 | Skill: ui-ux-pro-max
> Status: **PLANNED**
> Scope: All 5 pages + shared components (`utils/styles.py`)

---

## Audit Methodology

Skill queries run across all UX domains: `ux`, `style`, `chart`, `product`, `landing`, `typography`.
Each page read in full. 138 total UI component calls catalogued across 2,820 lines.
Findings grouped by page, then cross-cutting issues at the end.

**Product classification confirmed:** Dark Mode OLED + Enterprise Gateway pattern.
**Style match:** Existing design is well-aligned. Issues are structural and polish, not fundamental redesign.

---

## Issue Registry

Severity: 🔴 HIGH (blocks quality/conversion) | 🟡 MEDIUM (degrades experience) | 🟢 LOW (polish)

---

### PAGE 0 — Welcome (`pages/00_Welcome.py`)

> Already has a dedicated refactor plan: `plans/welcome-page-ux-refactor-plan.md`
> Do NOT duplicate. Treat as a dependency — implement Welcome refactor first.

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| W1 | 🔴 | Intake form above marketing content | `Funnel pattern` — see dedicated plan |
| W2 | 🟡 | `text_faint` has no distinct tier | `weight-hierarchy` — see dedicated plan |
| W3 | 🟡 | Emoji icons in 3 sections | `no-emoji-icons` — see dedicated plan |
| W4 | 🟡 | No sticky "Get Started" CTA | `smooth-scroll` — see dedicated plan |
| W5 | 🟢 | No card hover micro-interactions | `hover-states` — see dedicated plan |
| W6 | 🟢 | No glow on OLED accent elements | `Dark Mode OLED` — see dedicated plan |

---

### PAGE 1 — Diagnostic (`pages/01_Diagnostic.py`)

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| D1 | 🔴 | No per-field character count feedback until submission — users don't know the 20-char minimum until they hit Submit and get a blanket warning | `error-placement` — show inline per field, not blanket at top |
| D2 | 🔴 | Submit button is never disabled — it's always clickable even with all empty fields, making the 20-char warning a surprise | `loading-buttons` — disable submit until all 6 fields meet min length |
| D3 | 🟡 | No visible progress indicator for the 6 prompts (e.g. "3 / 6 answered") — users don't know how far through they are | `progress-indicators` — Step N of 6 counter |
| D4 | 🟡 | Brand header uses emoji `⚡` in `div.aha-brand-icon` — same cross-platform rendering risk as Welcome | `no-emoji-icons` |
| D5 | 🟡 | Inline hardcoded hex `#8990A8` for intro paragraph and char counter — bypasses the design token system, will diverge if tokens change | `color-semantic` — use `var(--text-muted)` |
| D6 | 🟡 | The 6 text areas are rendered with no visual separation or grouping — all 6 stack identically with only a label distinguishing them | `visual-hierarchy` — add domain label pill or section eyebrow per prompt |
| D7 | 🟢 | `st.balloons()` not called on diagnostic completion — it fires on reading section but not on completing the diagnostic itself, which is a bigger milestone | `success-feedback` |
| D8 | 🟢 | AI scoring spinner shows a single generic message — no sense of the 3–8 second wait | `loading-states` — show "Analysing your responses… this takes ~5s" |

---

### PAGE 2 — Skills Profile (`pages/02_Skills_Profile.py`)

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| S1 | 🔴 | Radar chart has no accessible alternative — `displayModeBar: False` disables the Plotly toolbar (including download), and there's no data table fallback | `data-table` + `screen-reader-summary` — radar chart is Accessibility Grade B; grouped bar or table required as alternative |
| S2 | 🔴 | `st.metric` for overall score uses Streamlit default styling — the score number is visually inconsistent with the IBM Plex Mono monospace system used everywhere else | `consistency` — wrap in custom HTML matching the Home page score display |
| S3 | 🟡 | Gap map bullets are built via `"".join(parts)` HTML — colour dots use hardcoded inline `style` with no token reference | `color-semantic` — use CSS classes + token vars |
| S4 | 🟡 | Assessment history `st.dataframe` has no styling override — renders Streamlit's default light table on a dark page, creating a jarring white island | `dark-mode-pairing` — apply `st.dataframe` with custom CSS or convert to themed HTML table |
| S5 | 🟡 | "Retake Diagnostic" and "Build My Path" buttons are equal weight (`use_container_width=True`) — primary action (Build/View) has `type="primary"` but same size as Retake | `primary-action` — Retake should be visually subordinate (secondary type + smaller) |
| S6 | 🟡 | Role title displayed as raw `role_id.upper()` fallback — if `ROLES` dict misses a key, user sees "UNIVERSAL" | `error-recovery` — friendly fallback: "Your Role" |
| S7 | 🟢 | Radar chart `fillcolor="rgba(0,212,232,0.12)"` is very faint on dark bg — barely visible polygon | `chart — color-guidance` — increase to 0.2 fill opacity |
| S8 | 🟢 | No empty state for assessment history when only 1 diagnostic exists — section header appears with a single-row table, which looks incomplete | `empty-states` — only show history section if `len(all_diags) > 1` |

---

### PAGE 3 — Home (`pages/03_Home.py`)

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| H1 | 🔴 | Module list has no locked-state visual beyond `opacity:0.5` — locked modules have no explanation of what unlocks them or when | `empty-nav-state` — "Complete Module N to unlock" tooltip or inline note |
| H2 | 🔴 | Atom-path cards have no sub-badge strip (Read / Practice / Quiz status) — legacy path shows `sub-badge` pills per module but atom path cards show nothing, making in-progress state invisible | `progress-indicators` — add same `sub-strip` badge pattern to atom-path cards |
| H3 | 🟡 | Summary card progress bar uses hardcoded inline `style` gradient — not a token-driven colour | `color-semantic` — use CSS class |
| H4 | 🟡 | `st.container(border=True)` for module cards uses Streamlit's default border — slightly inconsistent with the manually-styled `aha-card` used elsewhere | `consistency` — apply `aha-card` CSS class or match border token |
| H5 | 🟡 | Greeting uses `DM Serif Display` at `2rem` inline — same font/size as hero headings on Welcome, flattening hierarchy | `visual-hierarchy` — reduce to `1.5rem` or switch to Inter 600 for greeting |
| H6 | 🟡 | No empty state for the case where `_assembled_path` returns an empty list | `empty-states` — "No modules assigned yet — please complete the diagnostic" |
| H7 | 🟢 | Lock icon uses emoji `🔒` — same cross-platform risk | `no-emoji-icons` — replace with inline SVG lock icon |
| H8 | 🟢 | Done icon uses `"✓ "` string prefix — not themed, could be replaced with a green-tinted SVG checkmark | `icon-style-consistent` |

---

### PAGE 4 — Course Module (`pages/04_Course_Module.py`) — 5 sub-views

#### 4a. Overview sub-view

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| M1 | 🟡 | `About this module` expander is collapsed by default — key orientation info (domain, estimated time) is hidden on first visit | `progressive-disclosure` — expand by default on first visit |
| M2 | 🟡 | Single primary CTA determined by state but no context for why other states aren't available — e.g. user can't tell why "Take Quiz" appears without Practice being shown | `state-clarity` — show completed steps with checkmarks to explain CTA state |

#### 4b. Reading sub-view

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| R1 | 🔴 | `st.balloons()` fires on every return to Takeaway section (guarded by session key) but the guard key includes `course_id` — if the same course is re-entered, balloons fire again | `success-feedback` — guard should include a "session-permanent" flag, not just course_id |
| R2 | 🟡 | Reading nav uses `← Section Name` / `Section Name →` as button labels — works but the arrow direction convention is reversed for RTL and inconsistent with the `→` in other CTAs | `navigation-consistency` |
| R3 | 🟡 | `st.segmented_control` for section tabs is a newer Streamlit API — label is `label_visibility="collapsed"` with no accessible `aria-label` alternative | `aria-labels` — add title attribute or visible label |
| R4 | 🟡 | Fallback reading renders `st.success`/`st.warning`/`st.info` for good_example/anti_pattern/takeaway — these Streamlit alert widgets have coloured borders and icons that look jarring in the dark theme | `style-match` — custom styled cards consistent with `aha-card` theme |
| R5 | 🟢 | Content column uses `st.columns([1, 4, 1])` gutter — on narrow screens this 1-unit gutter may collapse too aggressively | `responsive-layout` |

#### 4c. Practice sub-view (AI Coach)

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| P1 | 🔴 | `st.chat_message` uses `avatar="🤖"` for assistant — emoji avatar, cross-platform rendering risk, and looks toy-like in an enterprise tool | `no-emoji-icons` — use a styled CSS avatar (initials "AI" or small SVG icon) |
| P2 | 🔴 | `st.error(t("module.practice_warning"))` — a red error-styled banner warns about real client data at the top of EVERY practice session, even after reading it many times | `progressive-disclosure` — show only on first visit to practice (session state flag); after that, show a subtle smaller note |
| P3 | 🟡 | Task counter ("Task 1 of 4") is visually present via `step_progress_strip` but the current task number within that step isn't visible in the chat UI itself | `progress-indicators` — show "Task 2 / 4" inline in chat header |
| P4 | 🟡 | Turn limit warning (`st.warning`) appears mid-conversation with buttons to continue/skip — abrupt interruption with no pre-warning | `multi-step-progress` — show a soft turn counter ("3 turns remaining") before hitting the wall |
| P5 | 🟡 | MCQ option buttons rendered as `st.columns(len(options))` — on mobile / narrow viewport, 3–4 column buttons collapse to very narrow targets | `touch-target-size` — stack MCQ options vertically (single column), not horizontally |
| P6 | 🟢 | Completed MCQ buttons use `disabled=True` — correct state but no visual differentiation for the selected answer vs unselected options | `disabled-states` — highlight the chosen answer with a border/background even when disabled |

#### 4d. Evaluation sub-view

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| E1 | 🟡 | `st.caption(f"📍 {domain}")` uses a pin emoji as a location icon | `no-emoji-icons` — use a CSS bullet or domain tag pill |
| E2 | 🟡 | `st.progress(eval_idx / EVAL_TOTAL)` bar shows raw fraction — no "Question N of 4" text label above it | `progress-indicators` — label is in `st.caption` above but visually disconnected from the progress bar |
| E3 | 🟡 | Performance task `text_area` has `label_visibility="collapsed"` with `"Response:"` as the label — fails the visible label rule | `input-labels` — use visible label or `st.markdown` heading before the textarea |
| E4 | 🟡 | MCQ `st.radio` uses `label_visibility="collapsed"` — no visible prompt label; question text is in a custom div above but semantically disconnected | `form-labels` — wire label to the widget or keep label visible |
| E5 | 🟢 | No confirmation before submitting the final evaluation answer — it's irreversible (triggers AI scoring) | `confirmation-dialogs` — "Submit your final answer?" confirm step on last question |

#### 4e. Results sub-view

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| RE1 | 🟡 | `st.metric` for module score — same inconsistency as Skills Profile (default Streamlit metric styling vs. custom monospace system) | `consistency` — custom HTML score display |
| RE2 | 🟡 | Domain score `st.progress` bar is unthemed — renders Streamlit default blue on dark background | `dark-mode-pairing` — custom CSS progress bar using `var(--cyan)` |
| RE3 | 🟡 | Coach note displayed in `st.container(border=True)` — default Streamlit border, not `aha-card` | `consistency` |
| RE4 | 🟡 | `st.success("Profile updated!")` for confirming gap map update — Streamlit success widget (green) inconsistent with custom success patterns elsewhere | `style-match` — custom success banner |
| RE5 | 🟢 | When all modules complete, only "View Profile" button shown — no celebration/milestone moment | `success-feedback` — `st.balloons()` or `st.snow()` + congratulatory copy |

---

### SHARED COMPONENTS (`utils/styles.py`)

| # | Sev | Issue | Rule |
|---|-----|-------|------|
| SC1 | 🔴 | `prefers-reduced-motion` media query is absent from `inject_global_css()` — all transitions/animations run regardless of OS accessibility setting | `reduced-motion` — add `@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }` |
| SC2 | 🔴 | No `scroll-behavior: smooth` on `html` element globally — anchor links jump, not scroll | `smooth-scroll` |
| SC3 | 🟡 | `render_sidebar` injects `step_progress_strip` — strips use coloured dots (`.done`, `.current`, `.pending`) but colour is the ONLY differentiator; no shape, icon, or text weight change | `color-not-only` — add a checkmark SVG for done, filled dot for current, hollow ring for pending |
| SC4 | 🟡 | Brand icon `⚡` used in `aha-brand-icon` div across pages — consistent emoji usage that should be replaced with a themed SVG lightning bolt | `no-emoji-icons` |
| SC5 | 🟡 | `section_header()` utility wraps in `<div class="section-header-text">` — no `id` attribute assigned, making it impossible to deep-link or smooth-scroll to sections | `deep-linking` |
| SC6 | 🟢 | Google Fonts loaded via `<link>` in every page's `inject_global_css()` — no `preconnect` hints, causing font FOIT | `font-loading` — add `<link rel="preconnect" href="https://fonts.googleapis.com">` |
| SC7 | 🟢 | Demo mode indicator uses `**🎭 Demo Mode**` — emoji in a bold Streamlit markdown widget | `no-emoji-icons` |

---

## Cross-Cutting Issues Summary

| Category | Count | Pages Affected |
|----------|-------|----------------|
| Emoji as structural icons | 9 instances | All 5 pages + styles.py |
| `prefers-reduced-motion` missing | 1 (global) | styles.py → all pages |
| Hardcoded hex in inline styles | 8+ instances | D1, S3, H3, H5 |
| Streamlit default widgets on dark theme | 6 instances | S4, RE2, RE3, RE4, P6 |
| Accessibility: label_visibility collapsed | 3 instances | E3, E4, R3 |
| Missing progress feedback | 4 instances | D3, H2, P3, E2 |

---

## Refactor Phases

Ordered by dependency and risk. Each phase is a standalone agent session.

### Phase A — Global fixes (prerequisite for all other phases)
**Files:** `utils/styles.py`
Tasks: SC1 (`prefers-reduced-motion`), SC2 (`scroll-behavior`), SC3 (step strip a11y), SC4 (brand icon SVG), SC6 (font preconnect)
**Why first:** These are global CSS changes that every page inherits. Fix once, benefit everywhere.

### Phase B — Welcome page refactor
**Files:** `pages/00_Welcome.py`, `utils/welcome_zh.py`
Tasks: W1–W6 (see `plans/welcome-page-ux-refactor-plan.md`)
**Dependency:** Phase A complete (inherits global CSS fixes)

### Phase C — Diagnostic page
**Files:** `pages/01_Diagnostic.py`
Tasks: D1 (per-field validation), D2 (disable submit until valid), D3 (progress counter), D4–D5 (token cleanup), D6 (domain grouping), D8 (spinner text)
**Risk:** Low — no logic changes. D2 requires reading form state but no AI/DB changes.

### Phase D — Home page
**Files:** `pages/03_Home.py`
Tasks: H1 (locked module explanation), H2 (atom-path sub-badges), H3–H5 (token/styling), H6 (empty state), H7–H8 (emoji → SVG)
**Risk:** Low-Medium. H2 requires reading atom progress state but no DB changes.

### Phase E — Skills Profile page
**Files:** `pages/02_Skills_Profile.py`
Tasks: S1 (radar chart a11y table), S2 (metric custom HTML), S3–S4 (themed gap map + dataframe), S5 (button hierarchy), S7 (chart fill opacity), S8 (history empty state)
**Risk:** Medium. S1 adds a new UI component (bar chart or table). S4 requires CSS override for `st.dataframe`.

### Phase F — Course Module page (all 5 sub-views)
**Files:** `pages/04_Course_Module.py`
Tasks: M1–M2, R1–R5, P1–P6, E1–E5, RE1–RE5
**Risk:** Medium-High. Most complex page (1,131 lines, 5 sub-views). Run in sub-phases if needed.
Sub-phase F1: Overview + Reading (M1, M2, R1–R5)
Sub-phase F2: Practice (P1–P6)
Sub-phase F3: Evaluation + Results (E1–E5, RE1–RE5)

---

## Total Issue Count

| Severity | Count |
|----------|-------|
| 🔴 HIGH | 11 |
| 🟡 MEDIUM | 29 |
| 🟢 LOW | 14 |
| **Total** | **54** |

---

## Acceptance Criteria (full audit complete)

- [ ] Zero emoji in structural icon positions across all pages
- [ ] `prefers-reduced-motion` respected globally
- [ ] All hardcoded hex colours replaced with CSS token vars
- [ ] Streamlit default widgets (metric, dataframe, progress, success) themed to dark palette
- [ ] All `label_visibility="collapsed"` inputs have accessible alternative label
- [ ] Radar chart has accessible data table alternative on Skills Profile
- [ ] Atom-path module cards show Read/Practice/Quiz sub-badge strip
- [ ] Locked modules explain unlock condition
- [ ] AI Coach emoji avatar replaced with CSS/SVG alternative
- [ ] Practice privacy warning shown only on first visit
- [ ] 42/42 pytest green after each phase
- [ ] Playwright UAT pass for full user journey: Welcome → Diagnostic → Profile → Home → Module (read → practice → eval → results)
