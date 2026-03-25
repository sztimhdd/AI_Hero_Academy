# Full-App UX Audit — Kickstarter Prompt

> Companion to: `plans/full-app-ux-audit-plan.md`
> Status: READY TO START
> Prerequisite: `plans/welcome-page-ux-refactor-plan.md` complete (Phase B depends on it)

---

## Context

AI Hero Academy is a 5-page Streamlit app (GCP Cloud Run, Python 3.11).
A full ui-ux-pro-max skill audit found 54 UX issues across all pages and shared components.

**Read `plans/full-app-ux-audit-plan.md` in full before starting.**
It contains the complete issue registry with severity, rule reference, and page location for every issue.

Implement in phase order. Each phase is a discrete commit block. Do not mix phases.

---

## Phase Order (with dependencies)

```
Phase A — Global CSS fixes (utils/styles.py)         ← start here
Phase B — Welcome page refactor                       ← see plans/welcome-page-ux-refactor-plan.md
Phase C — Diagnostic page
Phase D — Home page
Phase E — Skills Profile page
Phase F1 — Course Module: Overview + Reading
Phase F2 — Course Module: Practice
Phase F3 — Course Module: Evaluation + Results
```

---

## Phase A — Global Fixes (`utils/styles.py`)

These are CSS-only changes to `inject_global_css()`. Fix once, all pages inherit.

**SC1 — Add `prefers-reduced-motion`** (HIGH)
Append to the `<style>` block in `inject_global_css()`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**SC2 — Add `scroll-behavior: smooth`**
Add to the `html` selector in `inject_global_css()`:
```css
html { scroll-behavior: smooth; }
```

**SC3 — Step strip accessibility: colour not the only differentiator**
The `.step-dot` classes (`.done`, `.current`, `.pending`) currently use colour only.
Update the step strip CSS in `styles.py` so each state has a distinct shape signal:
- `.done`: filled circle + checkmark content (via `::after { content: '✓' }`)
- `.current`: filled circle + pulsing ring border
- `.pending`: hollow ring (border only, no fill)

**SC4 — Replace `⚡` brand icon with SVG**
In `inject_global_css()` and wherever `.aha-brand-icon` content is set, replace the emoji
with an inline SVG lightning bolt:
```html
<svg width="18" height="18" viewBox="0 0 24 24" fill="var(--cyan)"
     xmlns="http://www.w3.org/2000/svg">
  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
</svg>
```
Find all `⚡` references in `pages/01_Diagnostic.py` (brand header) and replace there too.

**SC6 — Font preconnect**
Add before the Google Fonts `<link>` in `inject_global_css()`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

Commit: `style(global): reduced-motion, smooth-scroll, step strip a11y, font preconnect`

---

## Phase C — Diagnostic Page (`pages/01_Diagnostic.py`)

**D1 + D2 — Per-field validation + disable Submit until valid**
After each `st.text_area`, compute `char_count = len((val or "").strip())`.
Already done for char counter display. Now:
- If `char_count < 20`, render the counter in `var(--accent_red)` instead of `var(--text-muted)`
- Compute `_all_valid = all(len(r["response_text"]) >= 20 for r in responses)`
- Pass `disabled=not _all_valid` to `st.form_submit_button`

**D3 — Progress counter**
Above the form, add a dynamic "N / 6 answered" counter:
```python
_answered = sum(1 for r in responses if len(r["response_text"]) >= 20)
st.markdown(
    f'<div style="font-family:\'IBM Plex Mono\',monospace; font-size:0.72rem; '
    f'color:#8990A8; margin-bottom:1.5rem">'
    f'{_answered} / 6 {t("diag.answered_label", _lang)}</div>',
    unsafe_allow_html=True,
)
```
Add `diag.answered_label` to `content/i18n/en.json` ("answered") and `zh.json`.

**D4 — Replace `⚡` emoji in brand header**
Use the same SVG from Phase A SC4.

**D5 — Replace hardcoded hex in inline styles**
Change `color:#8990A8` in inline `style=` strings to `color:var(--text-muted)` or
`color:var(--text-faint)` as appropriate. Applies to the intro paragraph and char counter.

**D6 — Domain label eyebrow per prompt**
Above each `st.text_area`, render a small domain label pill:
```python
_domain_display = get_domain_display_name(prompt["domain_id"], _lang)
st.markdown(
    f'<div style="font-family:\'IBM Plex Mono\',monospace; font-size:0.65rem; '
    f'color:var(--cyan); text-transform:uppercase; letter-spacing:0.1em; '
    f'margin-bottom:0.3rem">{_domain_display}</div>',
    unsafe_allow_html=True,
)
```

**D8 — Improve spinner message**
Change the generic spinner to include time estimate:
```python
with st.spinner(t("diag.spinner_analysing", _lang) + " (~5s)"):
```
Or add a more descriptive i18n key `diag.spinner_analysing_detail`.

Commit: `feat(diagnostic): per-field validation, progress counter, domain labels, token cleanup`

---

## Phase D — Home Page (`pages/03_Home.py`)

**H1 — Locked module unlock explanation**
In the locked card branch, add a caption below the title:
```python
st.markdown(
    f'<div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.25rem">'
    f'{t("home.locked_hint", _lang).format(n=seq-1)}</div>',
    unsafe_allow_html=True,
)
```
Add `home.locked_hint` to i18n: "Complete Module {n} to unlock".

**H2 — Atom-path sub-badge strip**
Atom-path cards currently have no Read/Practice/Quiz status display. Add the same
`sub-strip` / `sub-badge` pattern used in the legacy path:
```python
_r_state = "done" if _atom_reading_done else "current" if not _atom_reading_done else "pending"
_p_state = "done" if _atom_practice_done else ("current" if _atom_reading_done else "pending")
_q_state = "done" if _atom_eval_done else ("current" if _atom_practice_done else "pending")
st.markdown(
    f'<div class="sub-strip">'
    f'{_badge(_read_label, _r_state)}'
    f'{_badge(_practice_label, _p_state)}'
    f'{_badge(_quiz_label, _q_state)}'
    f'</div>',
    unsafe_allow_html=True,
)
```

**H3 — Token-driven progress bar**
Move the inline gradient `linear-gradient(90deg,#00D4E8,#0099AA)` to a CSS class:
```css
.home-progress-bar { background: linear-gradient(90deg, var(--cyan), #0099AA); }
```

**H5 — Greeting font size**
Reduce from `2rem` (same as hero) to `1.5rem` for proper hierarchy.

**H6 — Empty state for empty assembled path**
```python
if _assembled_path is not None and len(_assembled_path) == 0:
    st.info(t("home.empty_path_info", _lang))
    st.stop()
```

**H7 — Lock icon emoji → SVG**
Replace `"🔒 "` string prefix with inline SVG lock icon (Heroicons `lock-closed`).

Commit: `feat(home): locked hints, atom sub-badges, token cleanup, empty state, SVG lock icon`

---

## Phase E — Skills Profile (`pages/02_Skills_Profile.py`)

**S1 — Radar chart accessible alternative**
Below the `st.plotly_chart`, add a collapsed expander with the domain scores as a simple table:
```python
with st.expander(t("profile.chart_alt_label", _lang), expanded=False):
    _rows = [{"Domain": get_domain_display_name(d, _lang), "Score": f"{current_domain_scores.get(d,0):.1f} / 4.0"} for d in DOMAIN_IDS]
    st.dataframe(pd.DataFrame(_rows), hide_index=True, use_container_width=True)
```

**S2 — Overall score custom HTML**
Replace `st.metric(label=level_label, value=f"{overall:.1f} / 4.0")` with the same
IBM Plex Mono styled score block used in `03_Home.py`.

**S4 — Theme the assessment history dataframe**
Streamlit's `st.dataframe` renders a white table. Override with CSS:
```css
[data-testid="stDataFrame"] { background: var(--bg-surface) !important; }
[data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {
  color: var(--text) !important;
  border-color: var(--border) !important;
}
```
Inject via `inject_global_css()` addition in `styles.py`.

**S5 — Button visual hierarchy**
Change Retake button to `type="secondary"` and add `use_container_width=False` with
explicit `width` so it's visually smaller than the primary action.

**S7 — Radar fill opacity**
Change `fillcolor="rgba(0,212,232,0.12)"` to `"rgba(0,212,232,0.22)"`.

**S8 — History section conditional**
Wrap `section_header` + `st.dataframe` in `if len(all_diags) > 1:`.

Commit: `feat(profile): radar a11y table, custom score display, dataframe theme, button hierarchy`

---

## Phase F1 — Course Module: Overview + Reading

**M1 — About expander open on first visit**
```python
_about_expanded = not bool(progress.get("reading_completed_at"))
with st.expander(t("module.about_expander", _lang), expanded=_about_expanded):
```

**R1 — Balloons guard fix**
Change session key to `f"reading_takeaway_celebrated_{course_id}_{st.session_state.get('diag_session_started','')}"` so it resets per diagnostic session, not per course ID.

**R4 — Themed reading section cards**
Replace `st.success`/`st.warning`/`st.info` fallback rendering with themed `aha-card` divs:
```python
# Good example
st.markdown(f'<div class="aha-card" style="border-left:3px solid var(--accent_green)">'
            f'<div style="font-size:0.75rem;color:var(--accent_green);margin-bottom:0.4rem">GOOD EXAMPLE</div>'
            f'{reading["good_example"]}</div>', unsafe_allow_html=True)
# Anti-pattern
st.markdown(f'<div class="aha-card" style="border-left:3px solid var(--accent_amber)">'
            f'<div style="font-size:0.75rem;color:var(--accent_amber);margin-bottom:0.4rem">COMMON MISTAKE</div>'
            f'{reading["anti_pattern"]}</div>', unsafe_allow_html=True)
```

Commit: `feat(module): overview about-expander, reading themed cards, balloons guard fix`

---

## Phase F2 — Course Module: Practice

**P1 — Replace `avatar="🤖"` with CSS avatar**
Streamlit `st.chat_message` supports `avatar` as an image path or emoji. Replace with
a small inline SVG or a single-letter CSS avatar:
```python
# Use a small robot SVG saved as bytes or a data URI
# Simpler: use "assistant" as role and override the avatar CSS
st.chat_message("assistant", avatar=None)  # then CSS override for the generated avatar
```
Or inject CSS to override the default Streamlit avatar background:
```css
[data-testid="chatAvatarIcon-assistant"] {
  background: var(--bg-elevated) !important;
  color: var(--cyan) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 0.65rem !important;
}
[data-testid="chatAvatarIcon-assistant"]::after { content: "AI"; }
```

**P2 — Privacy warning: first-visit only**
```python
_practice_warn_key = f"practice_warn_seen_{course_id}"
if not st.session_state.get(_practice_warn_key):
    st.error(t("module.practice_warning", _lang))
    st.session_state[_practice_warn_key] = True
else:
    st.caption(t("module.practice_warning_short", _lang))  # shorter note
```
Add `module.practice_warning_short` to i18n.

**P4 — Soft turn counter before limit**
When `total_turns >= MAX_TOTAL_TURNS - 3`, show a warning:
```python
if MAX_TOTAL_TURNS - total_turns <= 3:
    st.caption(t("module.turns_remaining", _lang).format(n=MAX_TOTAL_TURNS - total_turns))
```

**P5 — Stack MCQ options vertically**
Replace `cols = st.columns(len(current_mcq_options))` with a single-column loop:
```python
for i, opt in enumerate(current_mcq_options):
    if st.button(opt["label"], key=f"mcq_{task_idx}_{i}", use_container_width=True):
        ...
```

Commit: `feat(module-practice): AI avatar CSS, first-visit warning, turn counter, vertical MCQ`

---

## Phase F3 — Course Module: Evaluation + Results

**E1 — Domain pin emoji → CSS pill**
Replace `st.caption(f"📍 {domain}")` with:
```python
st.markdown(f'<span class="module-domain-tag">{get_domain_display_name(primary_domain, _lang)}</span>',
            unsafe_allow_html=True)
```

**E3 + E4 — Restore input labels**
Performance task: add `st.markdown("**Your response:**")` before the `st.text_area`.
MCQ radio: change `label_visibility="collapsed"` to `label_visibility="visible"` with
a translated label string `t("module.eval_answer_label", _lang)`.

**E5 — Confirm on last question**
Add a session state flag for last-question confirmation:
```python
if is_last and not st.session_state.get(f"eval_confirm_{item_id}"):
    if st.button(t("module.eval_submit_quiz_btn", _lang), ...):
        st.session_state[f"eval_confirm_{item_id}"] = True
        st.rerun()
elif is_last and st.session_state.get(f"eval_confirm_{item_id}"):
    st.warning(t("module.eval_confirm_warning", _lang))
    col_c, col_s = st.columns(2)
    with col_c:
        if st.button(t("module.eval_cancel_btn", _lang)):
            st.session_state.pop(f"eval_confirm_{item_id}", None)
            st.rerun()
    with col_s:
        if st.button(t("module.eval_confirm_btn", _lang), type="primary"):
            # proceed with submission
```

**RE1 + RE2 — Custom score display + themed progress bar**
Replace `st.metric` with IBM Plex Mono HTML block (same pattern as Home/Profile).
Replace `st.progress` with:
```python
st.markdown(
    f'<div style="background:var(--bg-elevated);border-radius:4px;height:6px;overflow:hidden">'
    f'<div style="height:100%;width:{int(ds/4.0*100)}%;background:var(--cyan);border-radius:4px"></div>'
    f'</div>', unsafe_allow_html=True
)
```

**RE3 — Coach note card**
Replace `st.container(border=True)` with `st.markdown('<div class="aha-card-accent">...')`.

**RE4 — Success banner**
Replace `st.success(t("module.results_updated_success"))` with a styled card:
```python
st.markdown(
    f'<div class="aha-card" style="border-left:3px solid var(--accent_green);'
    f'color:var(--accent_green)">{t("module.results_updated_success", _lang)}</div>',
    unsafe_allow_html=True,
)
```

**RE5 — All-complete celebration**
```python
if all_complete:
    st.balloons()
    st.markdown('<div class="demo-cta-headline" style="text-align:center">🎉 Path Complete!</div>',
                unsafe_allow_html=True)
```

Commit: `feat(module-eval-results): domain pill, input labels, confirm dialog, themed score/progress/cards`

---

## Verification (after all phases)

```bash
.venv/Scripts/python -m pytest --tb=short -q   # must be 42/42
bash run_uat.sh
```

Playwright UAT — full journey:
```
Welcome (sticky CTA visible) → Get Started → Diagnostic (progress counter, disabled Submit)
→ Skills Profile (chart + table alt, custom metric) → Home (sub-badges, no emoji lock)
→ Module Overview (expander open) → Reading (themed cards, no balloons repeat)
→ Practice (CSS avatar, first-visit warning) → Evaluation (labels visible, confirm dialog)
→ Results (themed score, green banner) → Profile (updated hexagon)
```

Final commit per phase: `docs(ux-audit): Phase X complete — pytest green, UAT pass`

Final rename:
```
plans/full-app-ux-audit-plan.md      → [COMPLETED] full-app-ux-audit-plan.md
plans/full-app-ux-audit-kickstart.md → [COMPLETED] full-app-ux-audit-kickstart.md
```
