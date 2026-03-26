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

## Your Active Design Tool: ui-ux-pro-max

The skill is installed and working at:
```
~/.claude/skills/ui-ux-pro-max/scripts/search.py
```

**You must use it throughout this sprint — not just at the start.**
The plan covers the major design decisions upfront. For everything else — every
button, every spacing value, every animation, every new state — query the skill first.

### The rule: query before you guess

If the plan does not specify a detail, do NOT default to your own judgement.
Run the skill, read the output, then implement.

```bash
# Any UX decision not covered by the plan
python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<what you're designing>" --domain ux

# Choosing a style or visual treatment
python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<description>" --domain style

# Chart or data display
python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<data type>" --domain chart

# Full design system for a new component type
python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<component> dark enterprise" --design-system -p "AI Hero Academy" -f markdown
```

### Mandatory query triggers

You MUST run the skill before implementing any of these:

| Trigger | Domain flag |
| ------- | ----------- |
| New button style (not already in plan) | `--domain ux` |
| New spacing / padding value | `--domain ux` |
| Hover, focus, or disabled state for any element | `--domain ux` |
| Any animation or transition | `--domain ux` |
| Any icon (choosing stroke, size, style) | `--domain ux` |
| Any form element (label, input, textarea) | `--domain ux` |
| Any loading, skeleton, or empty state | `--domain ux` |
| Any card border-radius, shadow, or border | `--domain style` |
| Any colour not in the existing token set | `--domain ux` + `--domain style` |
| Any chart or data visualisation change | `--domain chart` |
| Any component with no spec in this plan | `--design-system` |

### Decisions already settled — do NOT re-query

These were resolved in planning. Apply directly:

| Decision | Answer |
| -------- | ------ |
| Micro-interaction duration | 150–300ms ease-out |
| Progress rail transition | 400ms ease |
| Minimum touch target | 44×44px |
| Card border-radius (small) | 8–12px |
| Card border-radius (large content) | 12–16px |
| Reading body line-height | 1.7 |
| Reading max-width | 65ch |
| Icon style | Heroicons outline, 24×24, stroke-width 1.5 |
| Disabled opacity | 0.38–0.5 |
| Error colour | `var(--accent_red)` #E8455A |
| Success colour | `var(--accent_green)` #29CC6A |
| AI content accent | `var(--indigo)` #6366F1, left border 3px |
| User action accent | `var(--cyan)` #00D4E8 |

### How to apply skill output

1. Run the query
2. Apply the **Do** guidance; avoid the **Don't** examples
3. If output conflicts with this plan, **the plan wins** — it already incorporates the skill audit
4. If output reveals something the plan missed, apply it and note it in the commit message body

---

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

## Phase 2 — Diagnostic Page (Hybrid Redesign)

**Files:** `pages/01_Diagnostic.py`, `utils/ai.py`, `content/i18n/en.json`, `content/i18n/zh.json`

> **This is a full architecture replacement of the diagnostic.** Read
> `plans/ux-revamp-2026-plan.md` Phase 2 in full before writing a line.
> The existing `st.form` with 6 stacked text areas is removed entirely.

### Before you start — run the skill

```bash
python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "progressive disclosure one question wizard step" --domain ux
python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "MCQ option card button selection auto advance" --domain ux
```

Apply the Do/Don't guidance to every screen you build.

---

### Step 2A — Session state schema

Add at the top of `pages/01_Diagnostic.py` after existing session state inits:

```python
# Hybrid diagnostic state machine
_DIAG_SCREENS = ["entry", "q1", "q2", "generating", "mcq_0", "mcq_1", "mcq_2", "mcq_3", "scoring"]

if "diag_screen" not in st.session_state:
    st.session_state["diag_screen"] = "entry"
if "diag_q1_text" not in st.session_state:
    st.session_state["diag_q1_text"] = ""
if "diag_q2_text" not in st.session_state:
    st.session_state["diag_q2_text"] = ""
if "diag_mcqs" not in st.session_state:
    st.session_state["diag_mcqs"] = []       # list of 4 generated MCQ dicts
if "diag_mcq_idx" not in st.session_state:
    st.session_state["diag_mcq_idx"] = 0     # current MCQ index (0-3)
if "diag_mcq_answers" not in st.session_state:
    st.session_state["diag_mcq_answers"] = {} # {domain_id: score_float}
```

Remove the existing `st.form("byow_diagnostic_form")` block and the `responses` list construction.

---

### Step 2B — Progress pill helper

```python
def _progress_pill(n: int, total: int = 6) -> str:
    return (
        f'<div class="domain-tag-pill" style="margin-bottom:1.2rem">'
        f'{n} of {total}</div>'
    )
```

---

### Step 2C — Screen router

Replace the entire render body with a dispatch on `diag_screen`:

```python
screen = st.session_state["diag_screen"]

if screen == "entry":
    _render_entry()
elif screen == "q1":
    _render_text_question(q_num=1)
elif screen == "q2":
    _render_text_question(q_num=2)
elif screen == "generating":
    _render_generating()
elif screen.startswith("mcq_"):
    idx = int(screen.split("_")[1])
    _render_mcq(idx)
elif screen == "scoring":
    _render_scoring()
```

---

### Step 2D — Entry screen

```python
def _render_entry():
    st.markdown(_progress_pill(0), unsafe_allow_html=True)
    st.markdown(
        f'<div class="score-card" style="padding:3rem 0 2rem">'
        f'<div style="font-family:\'DM Serif Display\',serif;font-size:2rem;color:var(--text)">'
        f'{t("diag.entry_headline", _lang)}</div>'
        f'<div style="font-size:0.9rem;color:var(--text-muted);margin-top:0.6rem">'
        f'{t("diag.entry_sub", _lang)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if st.button(t("diag.begin_btn", _lang), type="primary", use_container_width=False):
        st.session_state["diag_screen"] = "q1"
        st.rerun()
```

---

### Step 2E — Text question screens (Q1 and Q2)

```python
def _render_text_question(q_num: int):
    key = f"diag_q{q_num}_text"
    label_key = f"diag.q{q_num}_label"
    screen_next = "q2" if q_num == 1 else "generating"

    st.markdown(_progress_pill(q_num), unsafe_allow_html=True)

    # Domain tag pill
    domain = "strategic_prompting" if q_num == 1 else "critical_eval"
    st.markdown(
        f'<div class="domain-tag-pill">{get_domain_display_name(domain, _lang)}</div>',
        unsafe_allow_html=True,
    )

    val = st.text_area(
        t(label_key, _lang),
        value=st.session_state.get(key, ""),
        max_chars=300,
        height=120,
        key=f"diag_ta_q{q_num}",
    )
    # Persist on every keystroke
    st.session_state[key] = val or ""

    # Live char counter — JetBrains Mono, right-aligned
    char_count = len((val or "").strip())
    counter_color = "var(--accent_green)" if char_count >= 30 else "var(--text-faint)"
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;'
        f'color:{counter_color};text-align:right;margin-top:-0.5rem">'
        f'{char_count} / 300 · {t("diag.char_hint_short", _lang)}</div>',
        unsafe_allow_html=True,
    )

    _valid = char_count >= 30
    col_back, col_next = st.columns([1, 3])
    with col_back:
        if q_num == 2 and st.button(t("diag.back_btn", _lang), use_container_width=True):
            st.session_state["diag_screen"] = "q1"
            st.rerun()
    with col_next:
        if st.button(t("diag.next_btn", _lang), disabled=not _valid,
                     type="primary", use_container_width=True):
            st.session_state["diag_screen"] = screen_next
            st.rerun()
```

---

### Step 2F — Transition / generation screen

This screen triggers the LLM call and waits. Do NOT use `st.spinner` (it blocks render).
Instead render the custom screen first, then call the LLM, then advance.

```python
def _render_generating():
    st.markdown(_progress_pill(3), unsafe_allow_html=True)
    st.markdown(
        f'<div class="ai-card" style="text-align:center;padding:2.5rem 1.5rem">'
        f'<div class="ai-card-label" style="text-align:center">'
        f'{t("diag.generating_headline", _lang)}</div>'
        f'<div style="font-size:0.88rem;color:var(--text-muted);margin-top:0.8rem;line-height:1.7">'
        f'{t("diag.generating_sub", _lang)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Only generate if not already done
    if not st.session_state.get("diag_mcqs"):
        with st.spinner(""):
            intake_raw = profile.get("intake_profile") if profile else None
            intake = json.loads(intake_raw) if intake_raw else {}
            mcqs = generate_diagnostic_mcqs(
                q1_text=st.session_state["diag_q1_text"],
                q2_text=st.session_state["diag_q2_text"],
                intake_profile=intake,
                user_email=user_email,
                lang=_lang,
            )
            st.session_state["diag_mcqs"] = mcqs

    st.session_state["diag_screen"] = "mcq_0"
    st.rerun()
```

---

### Step 2G — MCQ screens

```python
def _render_mcq(idx: int):
    mcqs = st.session_state.get("diag_mcqs", [])
    if idx >= len(mcqs):
        st.session_state["diag_screen"] = "scoring"
        st.rerun()
        return

    mcq = mcqs[idx]
    screen_num = idx + 3  # screens 3-6 in overall flow (0-indexed)
    st.markdown(_progress_pill(screen_num), unsafe_allow_html=True)

    # Domain tag
    st.markdown(
        f'<div class="domain-tag-pill">{get_domain_display_name(mcq["domain_id"], _lang)}</div>',
        unsafe_allow_html=True,
    )

    # Question text
    st.markdown(
        f'<div style="font-family:\'Inter\',sans-serif;font-size:1.05rem;font-weight:600;'
        f'color:var(--text);line-height:1.6;margin-bottom:1.2rem">'
        f'{mcq["question_text"]}</div>',
        unsafe_allow_html=True,
    )

    # Options — full-width buttons, auto-advance on click (NO Next button)
    for option in mcq["options"]:
        if st.button(
            f'{option["label"]}.  {option["text"]}',
            key=f'mcq_{mcq["domain_id"]}_{option["label"]}',
            use_container_width=True,
        ):
            st.session_state["diag_mcq_answers"][mcq["domain_id"]] = option["score"]
            next_idx = idx + 1
            if next_idx < len(mcqs):
                st.session_state["diag_screen"] = f"mcq_{next_idx}"
            else:
                st.session_state["diag_screen"] = "scoring"
            st.rerun()
```

---

### Step 2H — Scoring screen

```python
def _render_scoring():
    st.markdown(_progress_pill(6, 6), unsafe_allow_html=True)
    st.markdown(
        f'<div class="score-card" style="padding:2rem 0">'
        f'<div style="font-size:1.8rem;color:var(--accent_green)">✓</div>'
        f'<div style="font-family:\'Inter\',sans-serif;font-size:1rem;'
        f'color:var(--text);margin-top:0.6rem">{t("diag.all_done", _lang)}</div>'
        f'<div style="font-size:0.88rem;color:var(--text-muted);margin-top:0.3rem">'
        f'{t("diag.scoring_headline", _lang)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        intake_raw = profile.get("intake_profile") if profile else None
        intake = json.loads(intake_raw) if intake_raw else {}
        result = score_hybrid_diagnostic(
            q1_text=st.session_state["diag_q1_text"],
            q2_text=st.session_state["diag_q2_text"],
            mcq_answers=st.session_state["diag_mcq_answers"],
            intake_profile=intake,
            user_email=user_email,
            lang=_lang,
        )
    # Save to Firestore (same path as before)
    # ... existing save_diagnostic / save_gap_map / assemble_path logic here ...
    # Clear diagnostic session state
    for k in ["diag_screen", "diag_q1_text", "diag_q2_text", "diag_mcqs",
              "diag_mcq_idx", "diag_mcq_answers"]:
        st.session_state.pop(k, None)
    st.switch_page("pages/02_Skills_Profile.py")
```

---

### Step 2I — `generate_diagnostic_mcqs()` in `utils/ai.py`

Add after existing AI functions. Full spec in the plan doc (Phase 2F).

Key implementation details:
- Use `call_llm()` with `temperature=0.4`, `call_type="mcq_generation"`
- Strip markdown fences from response before `json.loads()`
- Validate: exactly 4 items, each with `domain_id` in the 4 MCQ domains, exactly 4 options, scores in `[0.0, 4.0]`
- On any validation failure → load fallback from `content/diagnostic_prompts.json` key `"fallback_mcqs"` → never raise to caller

---

### Step 2J — `score_hybrid_diagnostic()` in `utils/ai.py`

**Scoring: holistic LLM — all 6 domains in one batch call.**

The scorer receives the full picture: both text answers AND the selected MCQ option
text (not a pre-scored weight). This lets the LLM contextualise a naive MCQ pick
against a sophisticated text answer, or reward consistent behaviour across all inputs.

`mcq_selections` shape:
```python
{
  "responsible_ai": {"question": "...", "selected_text": "..."},
  "data_decision":  {"question": "...", "selected_text": "..."},
  ...
}
```

Store this in session state during MCQ auto-advance:
```python
# In _render_mcq(), on button click:
st.session_state["diag_mcq_answers"][mcq["domain_id"]] = {
    "question": mcq["question_text"],
    "selected_text": option["text"],   # full text of chosen option, not a score
}
```

Build the scoring prompt (one call, all 6 domains):
```python
_DOMAIN_ORDER = [
    "strategic_prompting", "critical_eval",
    "responsible_ai", "data_decision", "relationship_intel", "augmented_comm",
]

def score_hybrid_diagnostic(q1_text, q2_text, mcq_selections, intake_profile, user_email, lang):
    role = intake_profile.get("role_text", "professional")
    seniority = intake_profile.get("seniority", "mid")
    org_type = intake_profile.get("org_type", "organisation")

    # Load rubrics from diagnostic_prompts.json for the 2 text domains
    prompts_data = json.loads(Path("content/diagnostic_prompts.json").read_text(encoding="utf-8"))
    rubric_map = {p["domain_id"]: p["scoring_rubric"] for p in prompts_data
                  if isinstance(p, dict) and "domain_id" in p}

    sections = []
    sections.append(f"DOMAIN: strategic_prompting\nAnswer: {q1_text}\nRubric: {rubric_map.get('strategic_prompting','')}")
    sections.append(f"DOMAIN: critical_eval\nAnswer: {q2_text}\nRubric: {rubric_map.get('critical_eval','')}")
    for domain_id, sel in mcq_selections.items():
        sections.append(
            f"DOMAIN: {domain_id}\n"
            f"Question: {sel['question']}\n"
            f"Selected answer: {sel['selected_text']}\n"
            f"Rubric: {rubric_map.get(domain_id,'Score based on depth and accuracy.')}"
        )

    scoring_prompt = (
        f"Score this AI skills diagnostic for a {seniority} {role} at a {org_type}.\n"
        f"Scale: 0.0–4.0 (0.0–0.4 Unaware, 0.5–1.4 Explorer, 1.5–2.4 Practitioner, "
        f"2.5–3.4 Proficient, 3.5–4.0 Champion).\n\n"
        + "\n\n".join(sections)
        + '\n\nReturn ONLY valid JSON with exactly these keys: '
        + '{"strategic_prompting": X.X, "critical_eval": X.X, "responsible_ai": X.X, '
        + '"data_decision": X.X, "relationship_intel": X.X, "augmented_comm": X.X}'
    )

    raw = call_llm(
        messages=[{"role": "user", "content": scoring_prompt}],
        temperature=0.1,
        user_email=user_email,
        call_type="hybrid_diagnostic_scoring",
    )
    raw_clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    domain_scores = json.loads(raw_clean)
    overall_score = sum(domain_scores.values()) / len(domain_scores)

    return {
        "item_scores": {},        # no per-item breakdown needed for MCQ in holistic mode
        "domain_scores": domain_scores,
        "overall_score": overall_score,
    }
```

**Also update `generate_diagnostic_mcqs()`** — remove `score` from the options schema.
Options only need `label` and `text`:
```json
{"label": "A", "text": "Paste the full transcript into Copilot"}
```
Update the generation prompt accordingly: instruct the LLM to write options spanning
Unaware → Proficient naturally but do NOT include numeric scores.

---

### Step 2K — Fallback MCQs in `content/diagnostic_prompts.json`

Add a `"fallback_mcqs"` key at the root with 4 generic (but role-aware where possible)
MCQs covering the same 4 domains. These activate only if LLM generation fails.

---

### Step 2L — i18n additions

Add all keys listed in the plan Phase 2I to both `content/i18n/en.json` and
`content/i18n/zh.json`.

---

### Step 2M — Replace ⚡ emoji

```html
<div class="aha-brand-icon">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="var(--cyan)">
    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
  </svg>
</div>
```

---

### Commit sequence

```
feat(ai): generate_diagnostic_mcqs() with validation + fallback
feat(ai): score_hybrid_diagnostic() merging text + MCQ scores
feat(diagnostic): hybrid 2-text + 4-MCQ one-at-a-time flow
feat(diagnostic): entry screen, text questions, MCQ auto-advance, scoring screen
content(diagnostic): fallback_mcqs in diagnostic_prompts.json + i18n keys
```

### UAT checklist for Phase 2

- [ ] Entry screen shows, Begin → Q1
- [ ] Q1 Next button disabled until 30+ chars; counter turns green on threshold
- [ ] Q1 → Q2 → transition screen appears (not blank)
- [ ] Transition generates MCQs and advances (or falls back silently)
- [ ] MCQ screens show domain pill + question + 4 full-width option buttons
- [ ] Clicking any MCQ option immediately advances — NO Next button
- [ ] After MCQ 4, scoring screen shows, then navigates to Skills Profile
- [ ] Full journey ZH works: all labels translated
- [ ] If LLM returns invalid JSON → fallback MCQs appear, no error shown to user
- [ ] Skills Profile shows all 6 domain scores (2 from text, 4 from MCQ)

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
