# Welcome Page UX Refactor — Kickstarter Prompt

> Companion to: `plans/welcome-page-ux-refactor-plan.md`
> Status: READY TO START

---

## Context

AI Hero Academy is a Streamlit multi-page app (GCP Cloud Run, Python 3.11).
`pages/00_Welcome.py` is the marketing/onboarding landing shown to first-time users
(no Firestore profile yet). It has 8 marketing sections + an intake form.

A full UX audit using the ui-ux-pro-max skill produced 6 prioritised findings.
All 6 are CSS/structural — no form logic, no Firestore, no LLM call changes.

**Read `plans/welcome-page-ux-refactor-plan.md` in full before writing a single line.**
It contains exact CSS, SVG strings, hex values, and before/after structure for every task.

---

## Your Mission

Implement all 6 tasks in order. Do not skip ahead — each task is a discrete commit.

---

## Task Sequence

### Task 1 — Move intake form to page bottom  🔴 HIGH
**Files:** `pages/00_Welcome.py`, `utils/welcome_zh.py`

The intake form (LinkedIn URL → file upload → text_area → multiselect → Advanced Options
→ CTA button) currently renders immediately after the Hero, before all 8 marketing
sections. Move the entire block to after Section 8 (Roadmap).

- Add `<div id="cta-section"></div>` anchor immediately before the form
- Prepend a CTA header block (headline + sub — see plan for exact copy)
- Update `utils/welcome_zh.py` to add a ZH CTA section header function and match order
- **DO NOT touch** form submit handler, session state, LLM calls, or `st.switch_page`

Commit: `refactor(welcome): move intake form to terminal CTA position`

---

### Task 2 — Split text_faint color tier  🟡 MEDIUM
**File:** `utils/styles.py`

`text_secondary` and `text_muted` are currently the same hex (`#8990A8`).
Split into three distinct tiers:

```python
"text_secondary": "#8990A8",   # body copy, card text
"text_muted":     "#6B7280",   # secondary labels, helper text  (was #8990A8)
"text_faint":     "#4B5268",   # citations, source labels, footnotes
```

Check contrast: `#4B5268` on `#161A22` (bg_surface) = ~3.8:1, acceptable for 0.65rem
citation text. If you want full AA, use `#5A6178` (4.5:1).

Commit: `refactor(styles): split text_faint into distinct third color tier`

---

### Task 3 — Replace emoji icons with inline SVG  🟡 MEDIUM
**File:** `pages/00_Welcome.py`

Three sections use emoji as structural icons. Replace with Heroicons outline SVGs
(24×24, stroke-width 1.5, `color: var(--cyan)`). Define as Python string constants
at the top of the file (after imports), then embed in the HTML templates.

Sections to update:
- **Section 3 (Learning Loop)** — `.demo-stage-icon`: 🔍📊🎯🏆 → magnifying-glass, bar-chart, target/crosshairs, trending-up SVGs
- **Section 5 (Differentiators)** — `.demo-diff-icon`: 🎭🤖🧭🔒 → user-circle, cpu-chip, compass, lock-closed SVGs
- **Section 6 (Skill Model)** — `.demo-domain-emoji`: 🛡️✨🔎📈🤝💬 → shield-check, sparkles, magnifying-glass-circle, chart-bar, users, chat-bubble SVGs

See plan doc for exact SVG path strings for each icon.

Update `.demo-stage-icon`, `.demo-diff-icon`, `.demo-domain-emoji` CSS:
```css
.demo-stage-icon svg,
.demo-diff-icon svg,
.demo-domain-emoji svg { display: block; margin: 0 auto 0.7rem; }
```

Commit: `refactor(welcome): replace emoji icons with inline SVG (Heroicons outline)`

---

### Task 4 — Add sticky "Get Started" anchor CTA  🟡 MEDIUM
**File:** `pages/00_Welcome.py`

Add to `DEMO_CSS`:
```css
.demo-sticky-cta {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 100;
  background: var(--cyan);
  color: #0D0F14;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  text-decoration: none;
  letter-spacing: 0.03em;
  box-shadow: 0 0 16px rgba(0, 212, 232, 0.35);
  transition: transform 150ms ease-out, box-shadow 150ms ease-out;
}
.demo-sticky-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 24px rgba(0, 212, 232, 0.5);
}
html { scroll-behavior: smooth; }
```

Inject anchor tag immediately after `st.markdown(DEMO_CSS, ...)` at the top of the
page render (before the Hero section):
```python
st.markdown(
    '<a class="demo-sticky-cta" href="#cta-section">Get Started &rarr;</a>',
    unsafe_allow_html=True
)
```

Commit: `feat(welcome): add sticky Get Started CTA with smooth scroll to form`

---

### Task 5 — Card hover micro-interactions  🟢 LOW
**File:** `pages/00_Welcome.py` — `DEMO_CSS` block

Add to `DEMO_CSS`:
```css
.demo-stat-card,
.demo-stage-card,
.demo-diff-card,
.demo-roadmap-card {
  transition: border-color 200ms ease-out, transform 200ms ease-out;
}
.demo-stat-card:hover,
.demo-stage-card:hover,
.demo-diff-card:hover,
.demo-roadmap-card:hover {
  border-color: rgba(0, 212, 232, 0.3);
  transform: translateY(-2px);
}
.demo-domain-pill {
  transition: border-color 200ms ease-out, background 200ms ease-out;
}
.demo-domain-pill:hover {
  border-color: rgba(0, 212, 232, 0.25);
  background: var(--bg-surface);
}
```

Commit: `style(welcome): add card hover micro-interactions (200ms ease-out)`

---

### Task 6 — Subtle glow on accent elements  🟢 LOW
**File:** `pages/00_Welcome.py` — `DEMO_CSS` block

Dark OLED style calls for `text-shadow: 0 0 10px` on accent elements only.
Apply sparingly — section eyebrows, section labels, and stat numbers only.

Add to existing `.demo-eyebrow`, `.demo-section-label`, `.demo-stat-number` rules:
```css
.demo-eyebrow,
.demo-section-label {
  text-shadow: 0 0 12px rgba(0, 212, 232, 0.4);
}
.demo-stat-number {
  text-shadow: 0 0 16px rgba(0, 212, 232, 0.35);
}
.demo-roadmap-badge {
  text-shadow: 0 0 10px rgba(245, 166, 35, 0.35);
}
```

Do NOT add glow to body copy, card text, subheads, or muted text.

Commit: `style(welcome): add subtle cyan/amber glow to OLED accent elements`

---

## Verification

After all 6 tasks:

```bash
# 1. Run pytest
.venv/Scripts/python -m pytest --tb=short -q

# 2. Start app
bash run_uat.sh
```

Then use Playwright MCP (`mcp__playwright__browser_*`) to verify:
- [ ] Welcome page loads — form is NOT visible above the fold
- [ ] Scrolling to bottom shows the intake form with CTA header
- [ ] Sticky "Get Started" button visible in bottom-right corner
- [ ] Clicking sticky CTA smooth-scrolls to form
- [ ] 3 stat cards, 4 stage cards, 4 diff cards all show hover effect
- [ ] Section eyebrows have visible cyan glow (subtle, not neon)
- [ ] No emoji visible in Section 3, 5, or 6 — SVG icons present
- [ ] Language toggle to ZH — all 8 sections render in ZH, form at bottom

Final commit: `docs(welcome-ux-refactor): mark COMPLETE — pytest green, UAT pass`

---

## Constraints

- Streamlit renders `unsafe_allow_html=True` markdown — use it for all CSS/HTML injection
- Do NOT use `st.dialog` or modal components anywhere in this page
- Do NOT change any Python logic — only HTML structure and CSS
- Do NOT remove the `[COMPLETED]` prefix convention from plans/ filenames after finishing;
  rename `welcome-page-ux-refactor-plan.md` → `[COMPLETED] welcome-page-ux-refactor-plan.md`
  and this file → `[COMPLETED] welcome-page-ux-refactor-kickstart.md`
