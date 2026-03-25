# UX Revamp 2026 — Merged Plan

> Generated: 2026-03-25
> Sources: full-app-ux-audit-plan.md + module-ux-vision-2026.md + Streamlit 1.55.0 SDK
> Status: **PLANNED**
> Scope: All pages + shared components. Welcome page (separate plan) is a dependency.

---

## Framing: What This Plan Is

This is not an incremental bug-fix list. It is a cohesive redesign of the user
experience using two inputs:

1. **54 audit findings** (what's broken or weak — fix floor)
2. **The Terminal vision** (what's possible — raise ceiling)

The merge rule: include everything from the audit that is HIGH/MEDIUM severity, and
layer the vision on top where it amplifies the same surfaces. Drop audit LOW issues
and vision HIGH-effort items that don't justify their complexity in a single sprint.

The result is one plan that makes the app noticeably better — not just cleaner.

---

## Mandatory: ui-ux-pro-max Skill Usage During Implementation

The skill was used upfront to generate this plan. It must also be used **throughout
implementation** — not just at the planning stage.

The agent working this sprint has access to the skill at:
```
~/.claude/skills/ui-ux-pro-max/scripts/search.py
```

### When to query during implementation

The agent MUST run the skill before making any design decision not already specified
by this plan. This includes:

| Situation | Command to run |
|-----------|---------------|
| Choosing padding / spacing for a new element | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "spacing padding touch target" --domain ux` |
| Deciding hover / focus state behaviour | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "hover state transition interactive" --domain ux` |
| Picking a colour for a new state (error, disabled, selected) | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<state> colour dark mode" --domain ux` |
| Choosing border-radius for a new card or button | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "border radius card button dark" --domain style` |
| Designing any icon or replacing any emoji | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "icon SVG stroke consistency" --domain ux` |
| Deciding animation duration or easing curve | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "animation duration easing micro-interaction" --domain ux` |
| Adding any form element (input, radio, checkbox, textarea) | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "form label input feedback" --domain ux` |
| Adding a loading or empty state | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "loading skeleton empty state" --domain ux` |
| Choosing a chart type or data display | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<data type>" --domain chart` |
| Any component not covered by this plan | `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<component description>" --design-system -p "AI Hero Academy"` |

### How to apply skill output

1. Run the query and read the result
2. Apply the **Do** guidance; avoid the **Don't** patterns
3. If the result conflicts with this plan, **this plan takes precedence** — the plan
   already incorporates the skill's audit findings
4. If the result reveals a consideration not in this plan, apply it and note it in
   the commit message

### Quick reference — decisions already settled by the skill

These were resolved during planning. Do not re-query, just apply:

| Decision | Resolved answer |
|----------|----------------|
| Animation duration | 150–300ms ease-out (micro), 400ms ease (progress rail) |
| Touch target minimum | 44×44px — all interactive elements |
| Card border-radius | 8–12px (smaller cards), 12–16px (larger content cards) |
| Body text line-height | 1.7 for reading content, 1.5 for UI labels |
| Body text max-width | 65ch for reading; unrestricted for UI |
| Icon style | Heroicons outline, 24×24, stroke-width 1.5 |
| Disabled opacity | 0.38–0.5 + `cursor: not-allowed` |
| Error colour | `var(--accent_red)` (#E8455A) |
| Success colour | `var(--accent_green)` (#29CC6A) |
| AI-generated content accent | `var(--indigo)` (#6366F1) — left border 3px |
| User-action accent | `var(--cyan)` (#00D4E8) |

---

## Streamlit 1.55.0 SDK — What's Available

The app is already on 1.55.0. These features are confirmed available:

| Feature | API | Use in this plan |
|---------|-----|-----------------|
| Streaming text | `st.write_stream(generator)` | Coach responses, results coach note |
| Partial reruns | `@st.fragment` | Chat input loop — no full-page rerender |
| Pill navigation | `st.pills(options, selection_mode)` | Reading section nav, eval domain tag |
| Floating overlay | `st.popover("label")` | Module info overlay (replaces expander) |
| Dynamic containers | `st.expander(on_change=fn)` (1.55) | Scenario expander collapse after read |
| Native font theming | `config.toml headingFont / codeFont` | JetBrains Mono via config (no CSS hack) |
| Container alignment | `st.container(horizontal=True, horizontal_alignment="center")` | Score card centering |
| Spacing primitive | `st.space("large")` | Cleaner vertical rhythm |
| Theme detection | `st.context.theme` | Future-proof dark/light conditional |

---

## Design System Additions (apply globally)

### New CSS tokens — add to `utils/styles.py` COLORS dict

```python
# Signal grammar: indigo = AI-generated content
"accent_indigo":        "#6366F1",
"accent_indigo_glow":   "rgba(99,102,241,0.12)",
"accent_indigo_border": "rgba(99,102,241,0.30)",

# Faint text tier (citations, footnotes — distinct from text_muted)
"text_faint":           "#4B5268",
```

### Font upgrade — `.streamlit/config.toml`

Replace the current `font = "sans serif"` with native Google Fonts via config:

```toml
[theme]
primaryColor             = "#00D4E8"
backgroundColor          = "#0D0F14"
secondaryBackgroundColor = "#161A22"
textColor                = "#EDF0F7"
font        = "Inter:https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
headingFont = "'DM Serif Display':https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&display=swap"
codeFont    = "'JetBrains Mono':https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap"
```

This replaces the manual `<link>` injection in `inject_global_css()` for all three
fonts. IBM Plex Mono → JetBrains Mono for the mono stack (tighter, more premium).

### New global CSS classes — add to `inject_global_css()` in `utils/styles.py`

```css
/* ── Signal grammar ─────────────────────────────── */
.ai-card {
  background: var(--indigo-glow);
  border-left: 3px solid var(--indigo-border);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
}
.ai-card-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--accent_indigo);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}

/* ── Reading content cards ───────────────────────── */
.read-concept-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.6rem; }
.read-principle-callout { background: var(--bg-elevated); border-left: 3px solid var(--accent_indigo); border-radius: 0 6px 6px 0; padding: 0.9rem 1.1rem; margin-top: 1rem; font-size: 0.88rem; color: var(--text); }
.read-split { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.8rem; }
.read-split-bad  { background: rgba(232,69,90,0.08); border: 1px solid rgba(232,69,90,0.25); border-radius: 8px; padding: 1rem; }
.read-split-good { background: rgba(41,204,106,0.08); border: 1px solid rgba(41,204,106,0.25); border-radius: 8px; padding: 1rem; }
.read-split-label { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.read-pitfall-card { background: rgba(232,69,90,0.06); border-left: 3px solid var(--accent_red); border-radius: 0 8px 8px 0; padding: 1.2rem 1.4rem; }
.read-takeaway-card { background: rgba(0,212,232,0.07); border: 1px solid rgba(0,212,232,0.25); border-radius: 12px; padding: 1.4rem; text-align: center; }

/* ── Chat bubbles ────────────────────────────────── */
.chat-user-bubble {
  margin-left: auto; max-width: 78%;
  background: var(--bg-elevated); border: 1px solid var(--border);
  border-radius: 16px 16px 4px 16px; padding: 0.75rem 1rem;
  font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text);
}
.chat-coach-bubble {
  max-width: 88%;
  background: var(--indigo-glow); border-left: 3px solid var(--indigo-border);
  border-radius: 4px 16px 16px 16px; padding: 0.75rem 1rem;
  font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text);
}
.chat-coach-label {
  font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
  color: var(--accent_indigo); text-transform: uppercase;
  letter-spacing: 0.1em; margin-bottom: 0.4rem;
}

/* ── MCQ option cards ────────────────────────────── */
.mcq-option {
  border: 1px solid var(--border); border-radius: 8px;
  padding: 0.85rem 1.1rem; margin-bottom: 0.5rem;
  cursor: pointer; transition: border-color 150ms ease-out, background 150ms ease-out;
  font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text);
}
.mcq-option:hover { border-color: var(--cyan); background: rgba(0,212,232,0.06); }
.mcq-option.selected { border-color: var(--cyan); background: rgba(0,212,232,0.10); }

/* ── Eval top progress rail ──────────────────────── */
.eval-progress-rail-track {
  position: fixed; top: 0; left: 0; right: 0; height: 3px;
  background: var(--border); z-index: 999;
}
.eval-progress-rail-fill {
  height: 100%; background: var(--cyan);
  transition: width 400ms ease;
  box-shadow: 0 0 8px rgba(0,212,232,0.5);
}

/* ── Score card ──────────────────────────────────── */
.score-card { text-align: center; padding: 2rem 0 1.5rem; }
.score-number { font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; font-weight: 500; color: var(--cyan); line-height: 1; }
.score-level { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--cyan); margin-top: 0.4rem; }
.score-delta-pos { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent_green); margin-top: 0.3rem; }
.score-delta-neg { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent_red); margin-top: 0.3rem; }

/* ── Themed progress bar ─────────────────────────── */
.themed-progress-track { background: var(--bg-elevated); border-radius: 4px; height: 6px; overflow: hidden; margin: 0.4rem 0; }
.themed-progress-fill  { height: 100%; background: linear-gradient(90deg, var(--cyan), #0099AA); border-radius: 4px; transition: width 0.5s ease; }

/* ── Domain tag pill ─────────────────────────────── */
.domain-tag-pill {
  display: inline-block; font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--cyan); background: rgba(0,212,232,0.08);
  border: 1px solid rgba(0,212,232,0.2); border-radius: 4px;
  padding: 0.2rem 0.6rem; margin-bottom: 1rem;
}

/* ── Global accessibility ────────────────────────── */
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Phase 1 — Foundation (prerequisite)

**Files:** `utils/styles.py`, `.streamlit/config.toml`
**Risk:** Zero — CSS and config only

### 1A — Font upgrade via config.toml
Replace `font = "sans serif"` with the three native font declarations above.
Remove the Google Fonts `<link>` tags from `inject_global_css()` — they are now
redundant (Streamlit 1.55 handles them natively via config).

### 1B — New tokens + global CSS
Add `accent_indigo`, `accent_indigo_glow`, `accent_indigo_border`, `text_faint`
to `COLORS` dict in `utils/styles.py`.

Inject all new CSS classes from the block above into `inject_global_css()`.

### 1C — Step strip accessibility
Update step strip dots in `render_sidebar` / `step_progress_strip`:
- `.done`: filled cyan + checkmark via `::after { content: '✓' }`
- `.current`: filled cyan + pulse ring
- `.pending`: hollow ring (border only)
Colour is no longer the only differentiator.

Commit: `style(foundation): JetBrains Mono, indigo tokens, a11y step strip, reduced-motion`

---

## Phase 2 — Diagnostic Page (Hybrid Redesign)

**Files:** `pages/01_Diagnostic.py`, `utils/ai.py`, `content/i18n/en.json`, `content/i18n/zh.json`
**Risk:** HIGH — full architecture replacement. No existing diagnostic logic survives unchanged.

### Background: Why the current BYOW-6 design fails

The audit identified the stacked-6-textarea layout as the single biggest completion risk:
all 6 open-ended questions visible at once creates blank-page anxiety, no progress signal,
and submit-only validation. The learning advisor's analysis confirms this and proposes a
fundamentally better approach.

### The Hybrid 2-Text + 4-MCQ Architecture

**Core insight:** the Welcome page intake already captured `role_text`, `daily_tasks`,
`industry`, `seniority`, `org_type`, and `ai_tools`. That context is enough for an LLM
to generate fully personalized MCQs after just 2 text answers — something no static
diagnostic can achieve.

**Domain assignment:**

| Domain | Mode | Rationale |
|--------|------|-----------|
| `strategic_prompting` | Text (Q1) | MCQ cannot measure prompt craft — we need to see how they construct it |
| `critical_eval` | Text (Q2) | Open-ended verification behaviour is rich signal, hard to fake with MCQ |
| `responsible_ai` | LLM-generated MCQ | Attitude/policy questions are naturally multiple-choice |
| `data_decision` | LLM-generated MCQ | "Given this data situation..." — classic MCQ |
| `relationship_intel` | LLM-generated MCQ | Preference/approach patterns map cleanly to 4 options |
| `augmented_comm` | LLM-generated MCQ | "Pick the better output" style works well |

**Total user effort:** ~4 sentences of typing + 4 clicks. Under 3 minutes.

---

### Screen Flow (7 states, all in session state)

```
diag_screen: "entry" → "q1" → "q2" → "generating" → "mcq_3" → "mcq_4" → "mcq_5" → "mcq_6" → "scoring"
```

**State management — key session keys:**
```python
st.session_state["diag_screen"]        # current screen name
st.session_state["diag_q1_text"]       # strategic_prompting text answer
st.session_state["diag_q2_text"]       # critical_eval text answer
st.session_state["diag_mcqs"]          # list of 4 generated MCQ dicts
st.session_state["diag_mcq_answers"]   # {domain_id: selected_option_score}
```

---

### 2A — Screen 0: Entry

```
┌──────────────────────────────────────────────┐
│  AI Skills Diagnostic                        │
│  6 questions · ~3 minutes · no right answers │
│                                              │
│  ████░░░░░░░░░░░░░  0 of 6                   │
│                                              │
│              [ Begin → ]                     │
└──────────────────────────────────────────────┘
```

Render a full-screen entry card with headline, sub-copy, and a single Begin button.
No form, no inputs. Sets `diag_screen = "q1"` on click.

---

### 2B — Screens 1–2: Text Questions (one at a time)

One `st.text_area` per screen. **No `st.form` wrapper** — we need live char counting
without form submission semantics.

**Q1 (strategic_prompting):**
> "Pick one task from your work you wish took half the time. Walk me through exactly
> how you'd ask AI to help — be as specific as you can."

**Q2 (critical_eval):**
> "You used AI to draft something important — a proposal, email, or summary.
> Before you send it, what specifically do you check?"

**Per-question UX:**
- `max_chars=300` with visible counter `0 / 300` in JetBrains Mono, bottom-right
- "2–3 sentences is plenty" as persistent sub-label (not placeholder)
- Next button **disabled** until `len(answer.strip()) >= 30`
- Next button enables with `transition: background-color 200ms` — no jarring instant change
- Progress pill: `<div class="domain-tag-pill">1 of 6</div>`

```python
_q1 = st.text_area(
    t("diag.q1_label", _lang),
    value=st.session_state.get("diag_q1_text", ""),
    max_chars=300,
    height=120,
    key="diag_q1_input",
    help=t("diag.char_hint_short", _lang),
)
_q1_valid = len((_q1 or "").strip()) >= 30
st.button(t("diag.next_btn", _lang), disabled=not _q1_valid, on_click=_advance_to_q2)
```

---

### 2C — Screen 3: Transition (LLM generation)

Triggered immediately when user clicks Next on Q2. Render before the LLM call completes.

```
┌──────────────────────────────────────────────┐
│                                              │
│   ⟳  Building your next 4 questions         │
│                                              │
│   Using your answers + role profile to       │
│   tailor the rest of the assessment          │
│   to your specific work.                     │
│                                              │
│   ████████████░░░░░  generating...           │
└──────────────────────────────────────────────┘
```

This screen is a **feature, not a bug**. The 5-8 second wait signals personalisation.
Use `st.spinner` hidden (replaced by custom HTML) + call `generate_diagnostic_mcqs()`.

**Pre-generation while typing:** Start the LLM call in the background as soon as
`diag_q2_text` reaches 30 chars using `@st.fragment` — by the time the user clicks
Next, generation may already be complete.

---

### 2D — Screens 4–7: MCQ (one at a time, auto-advance)

**No Next button.** Selecting an option immediately advances to the next screen.
This creates a rhythm — click, click, click, done.

```python
for i, option in enumerate(current_mcq["options"]):
    if st.button(
        option["text"],
        key=f"mcq_opt_{current_mcq['domain_id']}_{i}",
        use_container_width=True,
    ):
        st.session_state["diag_mcq_answers"][current_mcq["domain_id"]] = option["score"]
        _advance_mcq_screen()
        st.rerun()
```

MCQ option cards use `.mcq-option` CSS from Phase 1C. Full-width stacked buttons.
No radio widget — pure `st.button` so auto-advance is trivial.

Domain label pill shown above each MCQ question. Progress counter updates: `3 of 6`, `4 of 6`, etc.

---

### 2E — Screen 8: Scoring / Completion

```
┌──────────────────────────────────────────────┐
│  ████████████████████  6 of 6                │
│                                              │
│       ✓  All done.                           │
│       Scoring your responses...              │
│                                              │
│       [ animated hexagon building... ]       │
└──────────────────────────────────────────────┘
```

Call `score_hybrid_diagnostic()` (new function) which combines:
- Text answer scoring for Q1 (strategic_prompting) and Q2 (critical_eval) via LLM
- Direct MCQ scores for the 4 generated questions (pre-scored by the LLM during generation)

Then navigate to Skills Profile.

---

### 2F — New function: `generate_diagnostic_mcqs()` in `utils/ai.py`

```python
def generate_diagnostic_mcqs(
    q1_text: str,
    q2_text: str,
    intake_profile: dict,
    user_email: str,
    lang: str = "en",
) -> list[dict]:
    """
    Generate 4 personalised MCQs (responsible_ai, data_decision,
    relationship_intel, augmented_comm) calibrated to the user's
    role, seniority, and org_type.

    Returns list of dicts:
    [
      {
        "domain_id": "responsible_ai",
        "question_text": "...",
        "options": [
          {"label": "A", "text": "...", "score": 0.5},
          {"label": "B", "text": "...", "score": 2.5},
          {"label": "C", "text": "...", "score": 1.5},
          {"label": "D", "text": "...", "score": 3.0},
        ]
      },
      ...
    ]
    """
```

**LLM generation prompt (concept):**
```
You are generating a personalised AI skills diagnostic.

User profile:
  role: {role_text}
  daily_tasks: {daily_tasks}
  industry: {industry}
  seniority: {seniority}
  org_type: {org_type}
  ai_tools: {ai_tools}

Their answers so far:
  Q1 (Strategic Prompting): {q1_text}
  Q2 (Critical Evaluation): {q2_text}

Generate exactly 4 MCQs, one per domain:
- responsible_ai
- data_decision
- relationship_intel
- augmented_comm

Each MCQ must:
- Feature a realistic scenario from their specific role and industry
- Have exactly 4 options (A/B/C/D) spanning Unaware(0.5) → Explorer(1.5) →
  Practitioner(2.5) → Proficient(3.5) naturally (shuffle order, no obvious "correct" answer)
- Include a pre-scored float per option (0.5 / 1.5 / 2.5 / 3.5)
- Be calibrated to {seniority} level at a {org_type}

Return valid JSON only. No explanation. Schema: [{"domain_id": ..., "question_text": ...,
"options": [{"label": ..., "text": ..., "score": ...}]}]
```

**Temperature:** 0.4 (some creativity for option diversity, not too wild)
**Validation:** parse JSON, verify 4 domains, verify 4 options each, verify scores in
`[0.0, 4.0]`. If validation fails → use **fallback preset MCQs** per role from
`content/diagnostic_prompts.json` (add a `fallback_mcqs` section per role).

---

### 2G — New function: `score_hybrid_diagnostic()` in `utils/ai.py`

**Scoring decision: holistic LLM scoring across all 6 inputs.**

The LLM sees the complete picture — both text answers AND the selected MCQ option texts
(not just the score value) — and scores all 6 domains in a single batch call. This means:
- MCQ options are **not pre-scored** with fixed weights; `generate_diagnostic_mcqs()` does
  not need a `score` field per option
- The scorer receives the question + the selected answer text for each MCQ domain
- The LLM can weigh the MCQ choice in context of the user's text answers (e.g. a user who
  demonstrated sophisticated prompting in Q1 but picked a naive MCQ option may get a
  nuanced domain score, not a mechanical 0.5)

```python
def score_hybrid_diagnostic(
    q1_text: str,               # strategic_prompting
    q2_text: str,               # critical_eval
    mcq_selections: dict,       # {domain_id: {"question": str, "selected_text": str}}
    intake_profile: dict,
    user_email: str,
    lang: str = "en",
) -> dict:
    """
    Holistic LLM scoring of all 6 domains in one batch call.

    Builds a combined prompt containing:
      - intake profile context (role, industry, seniority)
      - Q1 text answer + strategic_prompting rubric
      - Q2 text answer + critical_eval rubric
      - 4 MCQ questions + selected option text + domain rubric

    LLM returns scores for all 6 domains simultaneously.
    Returns: {item_scores, domain_scores, overall_score}
    """
```

**Scoring prompt structure (concept):**
```
You are scoring an AI skills diagnostic for a {seniority} {role_text} at a {org_type}.

Score each domain on a 0.0–4.0 scale using these level anchors:
  0.0–0.4 Unaware | 0.5–1.4 Explorer | 1.5–2.4 Practitioner | 2.5–3.4 Proficient | 3.5–4.0 Champion

DOMAIN: strategic_prompting
Question: [Q1 prompt text]
Answer: {q1_text}
Rubric: [rubric from diagnostic_prompts.json]

DOMAIN: critical_eval
Question: [Q2 prompt text]
Answer: {q2_text}
Rubric: [rubric from diagnostic_prompts.json]

DOMAIN: responsible_ai
Question: [generated MCQ question text]
Selected answer: {selected_option_text}
Rubric: [rubric]

[...repeat for data_decision, relationship_intel, augmented_comm]

Return ONLY valid JSON: {"strategic_prompting": X.X, "critical_eval": X.X,
"responsible_ai": X.X, "data_decision": X.X, "relationship_intel": X.X,
"augmented_comm": X.X}
```

**Temperature:** 0.1 (same as existing `score_byow_diagnostic`)
**Token estimate:** ~1200 input tokens, ~60 output — comparable to the existing 6-question scorer

**`generate_diagnostic_mcqs()` change:** Remove `score` from the options schema.
Options only need `label` and `text`. The generation prompt instructs the LLM to write
options that span the skill range naturally — the scorer will evaluate the choice in
context, not by a preset weight.

---

### 2H — Fallback strategy

If `generate_diagnostic_mcqs()` fails (LLM error, JSON parse failure, timeout):
1. Log the error to `ai_call_log`
2. Fall back to 4 preset MCQs from `content/diagnostic_prompts.json` (add `fallback_mcqs` array per domain)
3. Show no error to user — transition screen just takes a moment longer
4. The fallback MCQs should be role-aware (use `intake_profile.role_id` to pick from
   RM/UW/AN/universal presets)

Never block the user. Degraded personalisation > broken flow.

---

### 2I — Replace ⚡ brand header emoji

Use inline SVG lightning bolt in `aha-brand-icon` everywhere `⚡` appears.

---

### i18n additions (new keys needed)

```json
"diag.entry_headline": "AI Skills Diagnostic",
"diag.entry_sub": "6 questions · ~3 minutes · no right answers",
"diag.begin_btn": "Begin →",
"diag.q1_label": "Pick one task from your work you wish took half the time. Walk me through exactly how you'd ask AI to help — be as specific as you can.",
"diag.q2_label": "You used AI to draft something important. Before you send it, what specifically do you check?",
"diag.char_hint_short": "2–3 sentences is plenty",
"diag.next_btn": "Next →",
"diag.generating_headline": "Building your next 4 questions",
"diag.generating_sub": "Using your answers + role profile to tailor the rest of the assessment to your specific work.",
"diag.n_of_6": "{n} of 6",
"diag.scoring_headline": "Scoring your responses...",
"diag.all_done": "All done."
```

Add ZH equivalents to `content/i18n/zh.json`.

---

### Acceptance criteria for Phase 2

- [ ] Entry screen shows with Begin button (no form visible)
- [ ] Q1 screen: Next disabled until 30+ chars; char counter updates live
- [ ] Q2 screen: same behaviour
- [ ] Transition screen appears and calls `generate_diagnostic_mcqs()`
- [ ] 4 MCQ screens render, each with domain pill + question + 4 full-width option cards
- [ ] Clicking an MCQ option auto-advances (no Next button needed)
- [ ] Fallback MCQs activate silently if LLM generation fails
- [ ] `score_hybrid_diagnostic()` produces valid `domain_scores` for all 6 domains
- [ ] Firestore write schema unchanged (existing tests pass)
- [ ] ZH language toggle works throughout all 8 screens
- [ ] 42/42 pytest green (update test fixtures for new diagnostic format)

Commit sequence:
```
feat(diagnostic): hybrid 2-text + 4-MCQ architecture, one-at-a-time screens
feat(ai): generate_diagnostic_mcqs() + score_hybrid_diagnostic()
feat(diagnostic): MCQ auto-advance, transition screen, fallback strategy
```

---

## Phase 3 — Home Page

**File:** `pages/03_Home.py`
**Risk:** Low

### 3A — Atom-path sub-badge strip
Add Read/Practice/Quiz `sub-badge` strip to atom-path cards (currently missing; legacy
path already has it). Derive states from `_atom_reading_done`, `_atom_practice_done`, `_atom_eval_done`.

### 3B — Locked module unlock hint
In locked card branch, add below the title:
```python
st.markdown(
    f'<div style="font-size:0.75rem;color:var(--text-faint);margin-top:0.2rem">'
    f'{t("home.locked_hint", _lang).format(n=seq-1)}</div>',
    unsafe_allow_html=True,
)
```
Add `home.locked_hint` = "Complete Module {n} to unlock" to i18n.

### 3C — Token-driven progress bar + greeting size
Move inline gradient to `.themed-progress-fill` CSS class.
Reduce greeting from `font-size:2rem` to `1.5rem`.

### 3D — SVG icons for lock and checkmark
Replace `"🔒 "` and `"✓ "` string prefixes with inline SVG constants defined at top of file.

### 3E — Empty state for empty assembled path
```python
if _assembled_path is not None and len(_assembled_path) == 0:
    st.info(t("home.empty_path_info", _lang))
    st.stop()
```

Commit: `feat(home): atom sub-badges, locked hints, token progress bar, SVG icons, empty state`

---

## Phase 4 — Skills Profile

**File:** `pages/02_Skills_Profile.py`
**Risk:** Medium (new components)

### 4A — Custom score display
Replace `st.metric(label=level_label, value=f"{overall:.1f} / 4.0")` with:
```python
st.markdown(
    f'<div class="score-card">'
    f'<div class="score-number">{overall:.1f}</div>'
    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;color:var(--text-muted);margin-top:0.2rem">/ 4.0</div>'
    f'<div class="score-level">{level_label}</div>'
    f'</div>',
    unsafe_allow_html=True,
)
```

### 4B — Radar fill opacity
Change `fillcolor="rgba(0,212,232,0.12)"` → `"rgba(0,212,232,0.22)"`.

### 4C — Accessible chart alternative
Below `st.plotly_chart`, add:
```python
with st.expander(t("profile.chart_alt_label", _lang), expanded=False):
    _table_rows = [{"Domain": get_domain_display_name(d, _lang), "Score": f"{current_domain_scores.get(d,0.0):.1f} / 4.0"} for d in DOMAIN_IDS]
    st.dataframe(pd.DataFrame(_table_rows), hide_index=True, use_container_width=True)
```

### 4D — Themed dataframe (assessment history)
Add to global CSS in `utils/styles.py`:
```css
[data-testid="stDataFrame"] thead th,
[data-testid="stDataFrame"] tbody td {
  background: var(--bg-surface) !important;
  color: var(--text) !important;
  border-color: var(--border) !important;
}
```

### 4E — Button hierarchy
Change Retake to `type="secondary"` with `use_container_width=False`.

### 4F — History section conditional
Wrap section in `if len(all_diags) > 1:`.

Commit: `feat(profile): custom score display, radar opacity, a11y table, dataframe theme, button hierarchy`

---

## Phase 5 — Module: Signal Grammar + Overview + Reading

**File:** `pages/04_Course_Module.py`
**Risk:** Medium — largest page, isolated to sub-view sections

### 5A — Signal grammar on all AI-generated content
Wrap all AI-generated content blocks (coach messages, gap map bullets, coach notes,
generated summaries) in `<div class="ai-card">`. This is the single highest visual
impact change in the entire plan.

Pages affected:
- `02_Skills_Profile.py` gap map section → wrap `aha-card` → `ai-card`
- `04_Course_Module.py` practice coach messages → new bubble CSS
- `04_Course_Module.py` results coach note → `ai-card` + label

### 5B — Overview: "What You'll Learn" block
Replace `st.expander("About this module", expanded=False)` with a always-visible
"What You'll Learn" block derived from `capability_tags`:
```python
_tags = _atom.get("capability_tags", []) if active_atom_id else []
if _tags:
    st.markdown(
        '<div class="read-concept-card" style="margin-bottom:1.2rem">'
        '<div class="ai-card-label">What You\'ll Learn</div>'
        + "".join(f'<div style="padding:0.2rem 0;font-size:0.88rem;color:var(--text)">· {tag}</div>' for tag in _tags[:4])
        + '</div>',
        unsafe_allow_html=True,
    )
```
Keep `st.popover("Module info")` for domain/time metadata — uses new 1.55 API:
```python
with st.popover("ℹ Module info"):
    st.caption(f"Domain: {domain_display}")
    st.caption(f"Est. {_atom.get('estimated_minutes','?')} min")
```

### 5C — Reading: structured cards
Replace fallback `st.success` / `st.warning` / `st.info` rendering with themed cards:

**Concept section:**
```python
st.markdown(
    f'<div class="read-concept-card">'
    f'<div class="ai-card-label">Concept</div>'
    f'<div style="font-size:0.95rem;line-height:1.75;color:var(--text);max-width:65ch">{concept_text}</div>'
    + (f'<div class="read-principle-callout"><strong>Key principle</strong><br>{key_principle}</div>' if key_principle else '')
    + '</div>',
    unsafe_allow_html=True,
)
```

**Good example section — split panel:**
```python
st.markdown(
    f'<div class="read-concept-card">'
    f'<div class="ai-card-label">Good Example</div>'
    f'<div class="read-split">'
    f'<div class="read-split-bad"><div class="read-split-label" style="color:var(--accent_red)">Without</div>{bad_text}</div>'
    f'<div class="read-split-good"><div class="read-split-label" style="color:var(--accent_green)">With</div>{good_text}</div>'
    f'</div></div>',
    unsafe_allow_html=True,
)
```
Parse `good_example` text — split on separator (e.g. `" → "` or `"vs "`) if present,
otherwise render full text in the green panel only.

**Anti-pattern section:**
```python
st.markdown(f'<div class="read-pitfall-card"><div class="ai-card-label" style="color:var(--accent_red)">Common Mistake</div>{anti_pattern}</div>', unsafe_allow_html=True)
```

**Takeaway section:**
```python
st.markdown(f'<div class="read-takeaway-card"><div class="ai-card-label">Key Takeaway</div><div style="font-size:1rem;line-height:1.7;color:var(--text)">{takeaway}</div></div>', unsafe_allow_html=True)
```

### 5D — Reading: st.pills navigation
Replace `st.segmented_control` with `st.pills`:
```python
_section_pill = st.pills(
    "Section",
    options=_SECTION_DISPLAY,
    default=_SECTION_DISPLAY[section_idx],
    label_visibility="collapsed",
    key="reading_section_pills",
)
```
`st.pills` is cleaner visually and has confirmed stable API in 1.55.

### 5E — Balloons guard fix
Change guard key to use session start timestamp:
```python
_celebrate_key = f"reading_takeaway_celebrated_{course_id}_{st.session_state.get('diag_session_started','')}"
```

Commit: `feat(module-overview-reading): signal grammar, what-you-learn, structured cards, pills nav`

---

## Phase 6 — Module: Practice (The Coach)

**File:** `pages/04_Course_Module.py`
**Risk:** Medium-High — chat loop is complex; use @st.fragment

### 6A — @st.fragment for chat loop
Wrap the practice chat rendering in `@st.fragment` to avoid full-page reruns:
```python
@st.fragment
def render_practice_chat(task_idx, messages, ...):
    # all chat message rendering + chat_input goes here
    if user_input := st.chat_input(...):
        ...
        st.rerun(scope="fragment")
```
This is the most impactful performance change in the entire plan.

### 6B — Chat bubble redesign
Replace `st.chat_message` default rendering with custom HTML bubbles:
```python
# Coach message
st.markdown(
    f'<div class="chat-coach-bubble">'
    f'<div class="chat-coach-label">Coach</div>'
    f'{msg["content"]}</div>',
    unsafe_allow_html=True,
)
# User message
st.markdown(
    f'<div class="chat-user-bubble">{msg["content"]}</div>',
    unsafe_allow_html=True,
)
```

### 6C — st.write_stream for coach responses
Upgrade the coach LLM call to use streaming. In `utils/ai.py`, add a streaming
variant of `call_llm` that yields tokens:
```python
def call_llm_stream(messages, temperature, user_email, call_type):
    """Yields text chunks from the serving endpoint stream."""
    w = WorkspaceClient()
    for chunk in w.serving_endpoints.query(
        name=os.environ["SERVING_ENDPOINT_NAME"],
        messages=[ChatMessage(role=m["role"], content=m["content"]) for m in messages],
        stream=True,
    ):
        if chunk.choices:
            yield chunk.choices[0].delta.content or ""
```
In the practice view:
```python
with st.container():
    st.markdown('<div class="chat-coach-label">Coach</div>', unsafe_allow_html=True)
    response = st.write_stream(
        call_llm_stream(coach_messages, temperature=0.4, user_email=user_email, call_type="coach")
    )
```
**Fallback:** If the Databricks serving endpoint does not support streaming, fall back
to the existing `call_llm()` call and render the full response at once. Detect at
runtime with a try/except on the first chunk.

### 6D — Privacy warning: first visit only
```python
_warn_key = f"practice_warn_seen_{course_id}"
if not st.session_state.get(_warn_key):
    st.error(t("module.practice_warning", _lang))
    st.session_state[_warn_key] = True
else:
    st.caption(f"⚠ {t('module.practice_warning_short', _lang)}")
```

### 6E — MCQ vertical stack
Replace `cols = st.columns(len(options))` with a single-column loop.
Each option rendered as a full-width `st.button(use_container_width=True)`.

### 6F — Quiet turn counter
Replace the mid-conversation `st.warning` turn limit wall with a caption:
```python
remaining = MAX_TOTAL_TURNS - total_turns
if remaining <= 3:
    st.caption(f"{remaining} {t('module.turns_remaining', _lang)}")
```

Commit: `feat(module-practice): @fragment, chat bubbles, write_stream, MCQ stack, turn counter`

---

## Phase 7 — Module: Evaluation + Results

**File:** `pages/04_Course_Module.py`

### 7A — 3px top progress rail
Inject at the top of the evaluation sub-view:
```python
_pct = int(eval_idx / EVAL_TOTAL * 100)
st.markdown(
    f'<div class="eval-progress-rail-track">'
    f'<div class="eval-progress-rail-fill" style="width:{_pct}%"></div></div>',
    unsafe_allow_html=True,
)
```

### 7B — Domain tag pill + question counter
Replace `st.caption(f"📍 {domain}")` and the disconnected counter with:
```python
st.markdown(
    f'<div style="margin-bottom:0.5rem">'
    f'<span class="domain-tag-pill">{domain_display}</span>'
    f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;color:var(--text-muted);margin-left:0.8rem">'
    f'Q {eval_idx+1} / {EVAL_TOTAL}</span></div>',
    unsafe_allow_html=True,
)
```

### 7C — Full-width MCQ option cards
Replace `st.radio(label_visibility="collapsed")` with stacked `st.button` cards
using the `.mcq-option` CSS class and a session state selection flag:
```python
for i, opt_label in enumerate(opt_labels):
    if st.button(opt_label, key=f"eq_{item_id}_{i}", use_container_width=True):
        st.session_state[f"eq_selected_{item_id}"] = opt_keys[i]
        st.rerun()
```

### 7D — Performance task: visible label + char count
Add `st.markdown("**Your response**")` above the text area.
Add JetBrains Mono char counter below: `f'{len(response_text)} / {MAX_USER_INPUT_CHARS}'`.

### 7E — Results: custom score card
Replace `st.metric` with:
```python
delta_class = "score-delta-pos" if delta_val >= 0 else "score-delta-neg"
st.markdown(
    f'<div class="score-card">'
    f'<div class="score-number">{rs:.1f}</div>'
    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;color:var(--text-muted);margin-top:0.2rem">/ 4.0</div>'
    f'<div class="score-level">{level_label}</div>'
    + (f'<div class="{delta_class}">▲ {delta_str}</div>' if delta_str else '')
    + '</div>',
    unsafe_allow_html=True,
)
```

### 7F — Themed domain progress bar
Replace `st.progress(ds/4.0)` with:
```python
st.markdown(
    f'<div class="themed-progress-track">'
    f'<div class="themed-progress-fill" style="width:{int(ds/4.0*100)}%"></div></div>',
    unsafe_allow_html=True,
)
```

### 7G — Coach note as ai-card
Replace `st.container(border=True)` with:
```python
st.markdown(
    f'<div class="ai-card" style="margin-top:1.2rem">'
    f'<div class="ai-card-label">Coach Note</div>'
    f'{coach_note}</div>',
    unsafe_allow_html=True,
)
```
If streaming is available (6C succeeds): stream the coach note via `st.write_stream`
inside the ai-card container with a 600ms initial delay.

### 7H — All-complete celebration
```python
if all_complete:
    st.balloons()
    st.markdown(
        '<div class="score-card" style="padding:1rem 0">'
        '<div style="font-family:\'DM Serif Display\',serif;font-size:1.8rem;color:var(--text)">Path Complete</div>'
        '<div style="font-size:0.9rem;color:var(--text-muted);margin-top:0.5rem">All 7 modules done. Your hexagon is updated.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
```

### 7I — Results success banner
Replace `st.success(...)` with themed card:
```python
st.markdown(
    f'<div style="border-left:3px solid var(--accent_green);background:rgba(41,204,106,0.06);'
    f'padding:0.6rem 1rem;border-radius:0 6px 6px 0;font-size:0.85rem;color:var(--accent_green)">'
    f'{t("module.results_updated_success", _lang)}</div>',
    unsafe_allow_html=True,
)
```

Commit: `feat(module-eval-results): top rail, MCQ cards, custom score, themed progress, ai-card coach note`

---

## Acceptance Criteria

### Functional
- [ ] 42/42 pytest green after every phase commit
- [ ] `@st.fragment` chat loop renders without full-page flicker
- [ ] `st.write_stream` coach responses stream or gracefully fall back
- [ ] All form submissions still navigate correctly (`st.switch_page`)
- [ ] ZH language toggle works — all new HTML uses `t()` for text content

### Visual (Playwright UAT)
- [ ] JetBrains Mono renders for module numbers, labels, score display (not IBM Plex Mono)
- [ ] Coach messages have indigo left border; user messages are right-aligned with dark bg
- [ ] Reading section uses structured cards — no `st.success`/`st.warning` yellow/green
- [ ] Evaluation page shows 3px cyan progress rail at top
- [ ] MCQ options are full-width vertical stack, not horizontal columns
- [ ] Results score is centered monospace, not `st.metric` widget
- [ ] Results coach note has indigo ai-card styling
- [ ] Atom-path module cards show Read/Practice/Quiz badge strip on Home
- [ ] Locked modules show unlock hint text
- [ ] Skills Profile score uses custom HTML (not `st.metric`)
- [ ] Radar polygon fill is visibly brighter
- [ ] No emoji in structural icon positions across all pages
- [ ] `prefers-reduced-motion` disables transitions (verify in DevTools)

### Accessibility
- [ ] Step strip dots use shape + colour (checkmark for done, hollow for pending)
- [ ] Eval MCQ buttons are keyboard-navigable
- [ ] Radar chart has accessible data table in expander
- [ ] All input labels visible (no `label_visibility="collapsed"` without alternative)

---

## What Is Explicitly Deferred

These are in the vision doc but excluded from this plan:

| Item | Reason |
|------|--------|
| Animated radar polygon on Results | Plotly frames are complex; risk not justified in one sprint |
| Ambient gradient blobs | Decorative only; add after core is stable |
| Full sidebar removal from module | Streamlit sidebar CSS removal is fragile across versions |
| Eval confirm dialog on last question | Low priority; adds friction for power users |
| Welcome page (W1–W6) | Has its own plan; implement first as dependency |

---

## File Change Summary

| File | Phase | Type of change |
|------|-------|---------------|
| `.streamlit/config.toml` | 1A | Font upgrade (3 lines) |
| `utils/styles.py` | 1B–1C | New tokens + CSS classes (~80 lines) |
| `pages/01_Diagnostic.py` | 2 | Per-field validation, domain labels, SVG icon |
| `pages/03_Home.py` | 3 | Sub-badges, locked hints, SVG icons |
| `pages/02_Skills_Profile.py` | 4 | Custom score, radar, dataframe theme |
| `pages/04_Course_Module.py` | 5–7 | Signal grammar, cards, chat, eval, results |
| `utils/ai.py` | 6C | `call_llm_stream()` generator function |
| `content/i18n/en.json` + `zh.json` | 2–3 | 3–4 new keys |
