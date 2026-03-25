# UX Revamp 2026 — Kickstarter Prompt

> Companion to: `plans/ux-revamp-2026-plan.md`
> Streamlit version: **1.55.0** (confirmed)
> Status: READY TO START
> Prerequisite: `plans/welcome-page-ux-refactor-plan.md` complete first

---

## Your Mission

Implement a cohesive UX revamp across all 5 pages of AI Hero Academy.

**Read `plans/ux-revamp-2026-plan.md` in full before writing a line.**
It contains the exact CSS, HTML, Python code, and Streamlit 1.55.0 API calls for every task.
Do not improvise implementations — follow the plan precisely.

The single north-star concept: **the AI stops being a feature and becomes the interface.**
Every design decision either reinforces that or gets removed.

---

## Pre-flight Checks

```bash
# Confirm Streamlit version
.venv/Scripts/python -c "import streamlit; print(streamlit.__version__)"
# Expected: 1.55.0

# Confirm tests baseline
.venv/Scripts/python -m pytest --tb=short -q
# Expected: 42 passed

# Check current config.toml
cat .streamlit/config.toml
```

---

## Phase 1 — Foundation

### 1A — Font upgrade via config.toml

Edit `.streamlit/config.toml`. Replace `font = "sans serif"` with:

```toml
[theme]
primaryColor             = "#00D4E8"
backgroundColor          = "#0D0F14"
secondaryBackgroundColor = "#161A22"
textColor                = "#EDF0F7"
font        = "Inter:https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600&display=swap"
headingFont = "'DM Serif Display':https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&display=swap"
codeFont    = "'JetBrains Mono':https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap"
widgetBackgroundColor    = "#1E2330"
widgetBorderColor        = "#2A2F3E"
skeletonBackgroundColor  = "#1E2330"
```

Then remove the manual Google Fonts `<link>` tags from `inject_global_css()` in
`utils/styles.py` — they are now handled natively by Streamlit 1.55.

### 1B — New design tokens

Add to `COLORS` dict in `utils/styles.py`:
```python
"accent_indigo":        "#6366F1",
"accent_indigo_glow":   "rgba(99,102,241,0.12)",
"accent_indigo_border": "rgba(99,102,241,0.30)",
"text_faint":           "#4B5268",
```

Update the CSS variable injection block:
```css
--indigo:        {COLORS['accent_indigo']};
--indigo-glow:   {COLORS['accent_indigo_glow']};
--indigo-border: {COLORS['accent_indigo_border']};
--text-faint:    {COLORS['text_faint']};
```

### 1C — Inject all new CSS classes

Append the full CSS block from the plan (signal grammar, reading cards, chat bubbles,
MCQ option cards, eval progress rail, score card, themed progress bar, domain tag pill,
global a11y rules) to `inject_global_css()`.

### 1D — Step strip accessibility

In `utils/styles.py` step strip CSS, update dot states:
```css
.step-dot.done::after  { content: '✓'; font-size: 0.6rem; }
.step-dot.done         { background: var(--cyan); color: #0D0F14; }
.step-dot.current      { background: var(--cyan); box-shadow: 0 0 0 3px rgba(0,212,232,0.25); }
.step-dot.pending      { background: transparent; border: 2px solid var(--border); }
```

**Verify:** Run the app and check that the step strip uses shape + colour (not colour alone).

Commit: `style(foundation): JetBrains Mono via config.toml, indigo tokens, new CSS classes, a11y step strip`

---

## Phase 2 — Diagnostic Page

**File:** `pages/01_Diagnostic.py`

### Per-field validation (D1 + D2)
In the `st.form` loop, after each `st.text_area`:
1. Replace hardcoded `color:#8990A8` with `var(--text-muted)` / `var(--text-faint)`
2. Colour the char counter red (`var(--accent_red)`) when `char_count < 20`
3. Compute `_all_valid = all(len(r["response_text"]) >= 20 for r in responses)` **before** the submit button (note: in `st.form`, responses are built inside the loop — ensure you read `st.session_state` key values, not the responses list which may still be empty at widget-render time)
4. Pass `disabled=not _all_valid` to `st.form_submit_button`

### Progress counter (D3)
Above the `st.form(...)`, add:
```python
_answered = sum(
    1 for p in byow_prompts
    if len((st.session_state.get(f"byow_{p['item_id']}", "") or "").strip()) >= 20
)
st.markdown(
    f'<div class="domain-tag-pill">{_answered} / 6 {t("diag.answered_label", _lang)}</div>',
    unsafe_allow_html=True,
)
```

### Domain eyebrow per prompt (D6)
Inside the loop, before `st.text_area`:
```python
_domain_display = get_domain_display_name(prompt["domain_id"], _lang)
st.markdown(f'<div class="domain-tag-pill">{_domain_display}</div>', unsafe_allow_html=True)
```

### Replace ⚡ emoji (D4)
Replace the brand header HTML `<div class="aha-brand-icon">⚡</div>` with:
```html
<div class="aha-brand-icon">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="var(--cyan)">
    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
  </svg>
</div>
```
Apply same replacement in `utils/styles.py` if `⚡` appears there.

### i18n additions
Add to `content/i18n/en.json`:
```json
"diag.answered_label": "answered"
```
Add to `content/i18n/zh.json`:
```json
"diag.answered_label": "已回答"
```

Commit: `feat(diagnostic): per-field validation, progress counter, domain labels, SVG brand icon`

---

## Phase 3 — Home Page

**File:** `pages/03_Home.py`

### Atom-path sub-badges (H2)
This is the highest priority in Phase 3. Inside the atom-path card loop, after the
`_col_body` markdown, add:
```python
_r_state = "done" if _atom_reading_done else "current"
_p_state = "done" if _atom_practice_done else ("current" if _atom_reading_done else "pending")
_q_state = "done" if _atom_eval_done else ("current" if _atom_practice_done else "pending")
st.markdown(
    f'<div class="sub-strip">'
    f'{_badge(t("home.badge_read", _lang), _r_state)}'
    f'{_badge(t("home.badge_practice", _lang), _p_state)}'
    f'{_badge(t("home.badge_quiz", _lang), _q_state)}'
    f'</div>',
    unsafe_allow_html=True,
)
```

### Locked hint (H1)
In the locked card branch (legacy path), add below the title:
```python
if seq > 1:
    st.markdown(
        f'<div style="font-size:0.75rem;color:var(--text-faint);margin-top:0.2rem">'
        f'{t("home.locked_hint", _lang).format(n=seq-1)}</div>',
        unsafe_allow_html=True,
    )
```

### SVG icons for lock/checkmark (H7, H8)
Define at top of file:
```python
_SVG_LOCK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>'
_SVG_CHECK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--accent_green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'
```
Replace `"🔒 "` with `f'{_SVG_LOCK} '` and `"✓ "` with `f'{_SVG_CHECK} '` in markdown strings.

### Token-driven progress bar + greeting (H3, H5)
Replace inline `linear-gradient(90deg,#00D4E8,#0099AA)` with `.themed-progress-fill` class.
Change greeting `font-size:2rem` → `1.5rem`.

### i18n additions
```json
"home.locked_hint": "Complete Module {n} to unlock"
```
```json
"home.locked_hint": "完成模块 {n} 后解锁"
```

Commit: `feat(home): atom sub-badges, locked hints, SVG icons, token progress bar`

---

## Phase 4 — Skills Profile

**File:** `pages/02_Skills_Profile.py`

### Custom score HTML (S2)
Replace `st.metric(label=level_label, value=f"{overall:.1f} / 4.0")` with the
`score-card` HTML block from the plan.

### Radar fill opacity (S7) + accessible table (S1)
Change `fillcolor` to `"rgba(0,212,232,0.22)"`.

Add below `st.plotly_chart`:
```python
with st.expander(t("profile.chart_alt_label", _lang), expanded=False):
    import pandas as pd
    _alt_rows = [{"Domain": get_domain_display_name(d, _lang), "Score": f"{current_domain_scores.get(d,0.0):.1f}"} for d in DOMAIN_IDS]
    st.dataframe(pd.DataFrame(_alt_rows), hide_index=True, use_container_width=True)
```

### Dataframe theme (S4)
The global CSS from Phase 1C already handles this. Verify it applies.

### Button hierarchy (S5)
Change Retake to `type="secondary"`, remove `use_container_width=True`.

### History conditional (S8)
Wrap in `if len(all_diags) > 1:`.

### Gap map signal grammar (S3)
Update gap map card to use `ai-card` class — change the opening `parts = ['<div class="aha-card">']` to `parts = ['<div class="ai-card">']`.

Add i18n key:
```json
"profile.chart_alt_label": "View as table"
"profile.chart_alt_label": "以表格查看"
```

Commit: `feat(profile): custom score card, radar opacity, a11y table, dataframe theme, gap map signal grammar`

---

## Phase 5 — Module: Overview + Reading

**File:** `pages/04_Course_Module.py`

### Overview — What You'll Learn block (M1, M2)
Replace the collapsed `st.expander("About...")` with:
1. An always-visible capability tags block (first 4 tags from `_atom.get("capability_tags", [])`)
2. A `st.popover("ℹ Module info")` for domain + time metadata

```python
# Always-visible capability tags
_tags = (_atom.get("capability_tags", []) if active_atom_id else [])[:4]
if _tags:
    _tag_html = "".join(f'<div style="padding:0.25rem 0;font-size:0.88rem;color:var(--text);border-bottom:1px solid var(--border)">· {tag}</div>' for tag in _tags)
    st.markdown(
        f'<div class="read-concept-card" style="margin-bottom:1.2rem">'
        f'<div class="ai-card-label">What You\'ll Learn</div>{_tag_html}</div>',
        unsafe_allow_html=True,
    )

# Floating info popover
with st.popover(t("module.about_popover_label", _lang)):
    st.caption(f"Domain: {get_domain_display_name(primary_domain, _lang)}")
    if active_atom_id and _atom:
        st.caption(f"Est. {_atom.get('estimated_minutes', '?')} min")
```

### Reading — Structured cards (R4)
Replace the `if section_idx == 0/1/2/3` content rendering blocks with the
themed card HTML from the plan. Parse `good_example` for a split panel if
the text contains `" → "` or `"vs "` — otherwise render in the green panel only.

### Reading — st.pills navigation (R3)
Replace `st.segmented_control` with:
```python
_pill_selected = st.pills(
    label="Section",
    options=_SECTION_DISPLAY,
    default=_SECTION_DISPLAY[section_idx],
    label_visibility="collapsed",
    key=f"reading_pills_{course_id}",
)
if _pill_selected and _pill_selected in _SECTION_DISPLAY:
    _new_idx = _SECTION_DISPLAY.index(_pill_selected)
    if _new_idx != section_idx:
        st.session_state["reading_section_ctrl"] = _SECTION_LABELS[_new_idx]
        st.rerun()
```

### Balloons guard fix (R1)
Update guard key to `f"reading_takeaway_celebrated_{course_id}_{st.session_state.get('diag_session_started', 'default')}"`.

Commit: `feat(module-overview-reading): what-you-learn block, structured cards, pills nav, balloons fix`

---

## Phase 6 — Module: Practice

**File:** `pages/04_Course_Module.py`, `utils/ai.py`

### @st.fragment for chat (6A)
Extract the practice sub-view rendering into a fragment function.
The fragment should contain: scenario expander, all message rendering, chat input.
**Important:** Fragment functions cannot use `st.switch_page` or `st.stop` — move any
navigation logic outside the fragment.

### Chat bubble redesign (6B)
Inside the message rendering loop, replace `st.chat_message` with custom HTML bubbles
using `.chat-coach-bubble` and `.chat-user-bubble` CSS classes from Phase 1C.

### call_llm_stream in utils/ai.py (6C)
Add the streaming generator. Check if `WorkspaceClient().serving_endpoints.query`
supports `stream=True` — if the endpoint raises `TypeError` on `stream=True`, catch and
fall back to non-streaming. Log the fallback to stderr.

### First-visit privacy warning (P2)
Use session state key `f"practice_warn_seen_{course_id}"`.
First visit: `st.error(...)`. Subsequent visits: small `st.caption`.

### MCQ vertical stack (P5)
Replace `st.columns(len(options))` layout with single-column `st.button` calls
using `use_container_width=True`.

### Quiet turn counter (P4)
Replace the `st.warning` turn limit wall with `st.caption` showing remaining turns
when ≤ 3 remain.

Commit: `feat(module-practice): @fragment, chat bubbles, write_stream, MCQ stack, quiet turn counter`

---

## Phase 7 — Module: Evaluation + Results

**File:** `pages/04_Course_Module.py`

### Evaluation (7A–7D)
- Top progress rail (fixed position CSS div)
- Domain tag pill + question counter replacing `st.caption(f"📍 ...")`
- Full-width MCQ buttons replacing `st.radio`
- Visible label above performance task textarea + char counter

### Results (7E–7I)
- Custom score card HTML (centered, JetBrains Mono, level label, delta)
- Themed progress bar for domain score
- Coach note wrapped in `ai-card` div with "Coach Note" label
- Themed green banner replacing `st.success`
- All-complete celebration: `st.balloons()` + custom congratulations copy

Commit: `feat(module-eval-results): top rail, MCQ cards, custom score, themed progress, ai-card note, celebration`

---

## Verification (after all phases)

```bash
# Tests
.venv/Scripts/python -m pytest --tb=short -q

# Run app
bash run_uat.sh
```

### Playwright UAT checklist

**Foundation:**
- [ ] JetBrains Mono visible on module numbers, score displays, domain labels
- [ ] No IBM Plex Mono remaining (verify via DevTools Computed Styles)
- [ ] `prefers-reduced-motion: reduce` in DevTools → all transitions disabled

**Diagnostic:**
- [ ] Empty submit → button disabled
- [ ] Type ≥ 20 chars in all 6 → button enables
- [ ] Counter turns red on short answers, grey on valid

**Home:**
- [ ] Atom-path cards show Read / Practice / Quiz badges
- [ ] Locked module shows "Complete Module N to unlock"
- [ ] No 🔒 emoji — SVG lock icon

**Skills Profile:**
- [ ] Score displays as large JetBrains Mono number, not st.metric widget
- [ ] Radar polygon fill visibly brighter
- [ ] Gap map has indigo left border (ai-card class)
- [ ] "View as table" expander shows domain scores table

**Module Reading:**
- [ ] Concept section uses card layout (not plain text)
- [ ] Good example shows split panel (Without/With columns)
- [ ] Pitfall uses red-accent card (not yellow st.warning)
- [ ] Takeaway uses full-width cyan card
- [ ] Navigation uses st.pills (pill buttons), not segmented control

**Module Practice:**
- [ ] Coach messages have indigo left border
- [ ] User messages are right-aligned with dark background
- [ ] MCQ options stack vertically (not horizontal columns)
- [ ] Privacy warning shows only once per course
- [ ] Chat input does NOT trigger full-page rerender (@st.fragment working)

**Module Evaluation:**
- [ ] 3px cyan progress rail at top of page
- [ ] Domain pill replaces "📍 domain" caption
- [ ] MCQ options are full-width card buttons
- [ ] Performance task has visible "Your response" label

**Module Results:**
- [ ] Score is large centered number (not st.metric)
- [ ] Coach note has "COACH NOTE" label + indigo left border
- [ ] Domain progress bar is cyan (not Streamlit default blue)
- [ ] Success banner is green themed card (not st.success widget)

---

## Constraints

- DO NOT change any Firestore schema, LLM prompt content, or scoring logic
- DO use `t()` for ALL user-facing text — no hardcoded English strings
- DO NOT use `st.rerun()` inside `@st.fragment` — use `st.rerun(scope="fragment")`
- If `st.write_stream` fails at runtime, fall back gracefully to non-streaming
- All 42 pytest tests must pass after EVERY phase commit
- Rename files after completion:
  `plans/ux-revamp-2026-plan.md` → `[COMPLETED] ux-revamp-2026-plan.md`
  `plans/ux-revamp-2026-kickstart.md` → `[COMPLETED] ux-revamp-2026-kickstart.md`
