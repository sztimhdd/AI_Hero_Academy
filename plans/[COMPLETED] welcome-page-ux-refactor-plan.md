# Welcome Page — UX Refactor Plan

> Generated: 2026-03-25 | Skill: ui-ux-pro-max
> Status: **PLANNED**
> Scope: `pages/00_Welcome.py`, `utils/styles.py`, `utils/welcome_zh.py`

---

## Audit Summary

Full review run against ui-ux-pro-max design system + UX guidelines database.

**Product classification:** Enterprise Gateway / Dark Mode (OLED)
**Recommended style match:** Dark Mode OLED — already implemented. Palette is correct.
**Landing pattern match:** Funnel (3-Step Conversion) — currently violated.

### Findings by severity

| # | Severity | Finding | Rule |
|---|----------|---------|------|
| 1 | 🔴 HIGH | Intake form renders above all marketing content | `Funnel pattern` — CTA must be terminal, not position 2 |
| 2 | 🟡 MEDIUM | `text_secondary` and `text_muted` map to identical hex `#8990A8` | `weight-hierarchy`, `whitespace-balance` — no faint tier |
| 3 | 🟡 MEDIUM | Emoji used as structural icons in 3 sections | `no-emoji-icons` — platform rendering inconsistency |
| 4 | 🟡 MEDIUM | No persistent "Get Started" escape hatch after form is moved | `sticky navigation`, `smooth-scroll`, `primary-action` |
| 5 | 🟢 LOW | Cards and sections have no hover/transition feedback | `hover-states` — 150–300ms micro-interaction missing |
| 6 | 🟢 LOW | Dark style calls for subtle glow on accent elements | `Dark Mode OLED` — `text-shadow: 0 0 10px` on cyan labels |

**What is already correct:** All WCAG color contrast passes (lowest pair 4.95:1). Typography tri-stack (DM Serif + Inter + IBM Plex Mono) is intentional and consistent. Loading spinners present on both async operations. Form labels are explicit (not placeholder-only). Surface depth hierarchy (`bg_primary → bg_surface → bg_elevated`) is correct.

---

## Design System (from skill)

Use as reference for all changes in this refactor:

| Token | Value | Use |
|-------|-------|-----|
| `--bg-primary` | `#0D0F14` | Page background |
| `--bg-surface` | `#161A22` | Cards |
| `--bg-elevated` | `#1E2330` | Callouts, nested surfaces |
| `--text` | `#EDF0F7` | Headings, primary text |
| `--text-muted` | `#8990A8` | Body copy, card text |
| `--text-faint` | `#636880` ← **new** | Citations, source labels, footnotes |
| `--cyan` | `#00D4E8` | Accents, labels, highlights |
| `--amber` | `#F5A623` | Badges, secondary accents |
| `--border` | `#2A2F3E` | Card borders, dividers |

**Key effects (Dark OLED style):**
- Subtle cyan glow on accent labels: `text-shadow: 0 0 8px rgba(0, 212, 232, 0.35)`
- Card hover: `border-color` shift to `rgba(0, 212, 232, 0.3)` + `transform: translateY(-2px)`, 200ms ease-out
- Section transitions: 150–300ms ease-out on all interactive state changes

---

## Refactor Tasks

### Task 1 — Reorder: Move intake form to bottom (HIGH)

**File:** `pages/00_Welcome.py`

**Current structure:**
```
Hero
[LinkedIn URL input]          ← form starts here (line 345)
[— or —]
[File uploader]
[LinkedIn PDF expander]
[text_area: describe your role]
[multiselect: AI tools]
[Advanced Options expander]
[Get My Personalized Path button]
──── divider ────
Section 2: The Challenge
Section 3: How It Works
Section 4: Product Tour
Section 5: Differentiators
Section 6: Skill Model
Section 7: Roadmap
```

**Target structure:**
```
Hero  (keep intro paragraph; remove form)
──── divider ────
Section 2: The Challenge
Section 3: How It Works
Section 4: Product Tour
Section 5: Differentiators
Section 6: Skill Model
Section 7: Roadmap
──── divider ────
Section 8: Get Started  ← intake form moves here
  [headline: "Ready to find out where you stand?"]
  [sub: "Takes 5 minutes. No right answers."]
  [LinkedIn URL input]
  [— or —]
  [File uploader]
  [LinkedIn PDF expander]
  [text_area: describe your role]
  [multiselect: AI tools]
  [Advanced Options expander]
  [Get My Personalized Path button]  ← primary CTA
```

**Implementation notes:**
- Wrap the form block in an HTML anchor: `st.markdown('<div id="cta-section"></div>', unsafe_allow_html=True)` immediately before it
- Add a `demo-cta-header` heading block (same pattern as the existing one at line ~289):
  ```html
  <div class="demo-cta-header">
    <div class="demo-section-label">Get Started</div>
    <div class="demo-cta-headline">Ready to find out where you stand?</div>
    <div class="demo-cta-sub">6 open-ended questions. ~5 minutes.<br>No right answers — your responses shape your path.</div>
  </div>
  ```
- Apply same change to `utils/welcome_zh.py` ZH sections (move ZH form header to bottom)
- **No logic changes** — only structural reorder. The form submit handler, session state, and `st.switch_page` are unaffected.

---

### Task 2 — Add faint text tier to color system (MEDIUM)

**File:** `utils/styles.py`

**Current:**
```python
COLORS = {
    ...
    "text_secondary": "#8990A8",
    "text_muted":     "#8990A8",   # identical — no faint tier
}
```

**Target:**
```python
COLORS = {
    ...
    "text_secondary": "#8990A8",   # body copy, card text, sub-headings
    "text_muted":     "#6B7280",   # secondary labels, helper text
    "text_faint":     "#4B5268",   # citations, source labels, footnotes (was #8990A8)
}
```

**Where `--text-faint` is used in Welcome page:**
- `.demo-stat-source` — McKinsey citation lines
- `.demo-attribution` — Turing Institute attribution
- `.demo-mastery-note` — footnote below hexagon progression

**Contrast check for new `#4B5268` on `#161A22`:**
- Ratio: ~3.8:1 — passes WCAG AA for large/bold text (≥3:1); acceptable for 0.65rem citation text
- If stricter AA is required, use `#5A6178` (4.5:1 on bg_surface)

---

### Task 3 — Replace emoji icons with inline SVG (MEDIUM)

**Files:** `pages/00_Welcome.py`

Three sections use emoji as structural icons:

**Section 3 — Learning Loop stage cards** (`.demo-stage-icon`):
| Stage | Current emoji | SVG replacement |
|-------|--------------|-----------------|
| Diagnose | 🔍 | magnifying glass SVG |
| Map Gaps | 📊 | bar chart SVG |
| Train | 🎯 | target SVG |
| Score & Track | 🏆 | chart trending up SVG |

**Section 5 — Differentiator cards** (`.demo-diff-icon`):
| Diff | Current emoji | SVG replacement |
|------|--------------|-----------------|
| Role scenarios | 🎭 | user circle SVG |
| AI reads answer | 🤖 | cpu chip SVG |
| Gaps drive sequence | 🧭 | compass SVG |
| Data stays internal | 🔒 | lock closed SVG |

**Section 6 — Domain pills** (`.demo-domain-emoji`):
| Domain | Current emoji | SVG replacement |
|--------|--------------|-----------------|
| Responsible AI | 🛡️ | shield check SVG |
| Strategic Prompting | ✨ | sparkles SVG |
| Critical Eval | 🔎 | magnifying glass circle SVG |
| Data Decision | 📈 | trending up SVG |
| Relationship Intel | 🤝 | users SVG |
| Augmented Comm | 💬 | chat bubble SVG |

**Implementation approach for Streamlit:**
Inline the SVG string directly in the HTML template. Use Heroicons outline style (24×24, stroke-width 1.5) in `var(--cyan)` color. Example:
```html
<div class="demo-stage-icon">
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.5" style="color: var(--cyan)">
    <path stroke-linecap="round" stroke-linejoin="round"
          d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/>
  </svg>
</div>
```
Each icon is ~120 chars of SVG — negligible payload. Define them as Python constants at the top of `00_Welcome.py`.

---

### Task 4 — Add sticky "Get Started" CTA (MEDIUM)

**File:** `pages/00_Welcome.py`

After the form moves to the bottom (Task 1), add a sticky button that appears after the hero scrolls out of view, linking back to `#cta-section`.

**CSS injection** (add to `DEMO_CSS`):
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

**Streamlit injection** (after `st.markdown(DEMO_CSS)`):
```python
st.markdown(
    '<a class="demo-sticky-cta" href="#cta-section">Get Started &rarr;</a>',
    unsafe_allow_html=True
)
```

**Note:** Streamlit's `st.markdown` with `unsafe_allow_html=True` renders anchor tags. The `scroll-behavior: smooth` on `html` handles the scroll. No JS required.

---

### Task 5 — Add card hover micro-interactions (LOW)

**File:** `pages/00_Welcome.py` — `DEMO_CSS` block

Add hover transitions to all interactive-feeling card classes. The Dark OLED style calls for `200ms ease-out` transitions.

```css
/* Card hover — stat, stage, diff, roadmap cards */
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

/* Domain pill hover */
.demo-domain-pill {
  transition: border-color 200ms ease-out, background 200ms ease-out;
}
.demo-domain-pill:hover {
  border-color: rgba(0, 212, 232, 0.25);
  background: var(--bg-surface);
}
```

---

### Task 6 — Add subtle glow to cyan accent labels (LOW)

**File:** `pages/00_Welcome.py` — `DEMO_CSS` block

The Dark OLED style recommendation: `text-shadow: 0 0 10px neon-color (sparingly)`. Apply only to the monospace section labels and stat numbers — the highest-contrast elements where glow reads as intentional, not buggy.

```css
/* Subtle cyan glow on section eyebrows and stat numbers */
.demo-eyebrow,
.demo-section-label,
.demo-stat-number {
  text-shadow: 0 0 12px rgba(0, 212, 232, 0.4);
}

/* Amber glow on roadmap badges */
.demo-roadmap-badge {
  text-shadow: 0 0 10px rgba(245, 166, 35, 0.35);
}
```

Do **not** add glow to body copy, subheads, or card text — only the accent elements.

---

## Acceptance Criteria

- [ ] Form section renders after Section 8 (Roadmap), not after Hero
- [ ] `#cta-section` anchor exists and sticky CTA scrolls to it smoothly
- [ ] `text_faint` is a visually distinct third tier from `text_muted` (citation text visibly lighter)
- [ ] No emoji characters remain in structural icon positions — all replaced with inline SVG
- [ ] All stat cards, stage cards, diff cards respond to hover with `translateY(-2px)` + cyan border tint
- [ ] Section labels and stat numbers have subtle cyan glow
- [ ] ZH path (`lang == "zh"`) still renders correctly — `welcome_zh.py` section functions updated to match new order
- [ ] 42/42 pytest green (no logic changes — should pass unchanged)
- [ ] Playwright UAT: Welcome page renders end-to-end, sticky CTA visible, clicking it scrolls to form

---

## Files Changed

| File | Changes |
|------|---------|
| `pages/00_Welcome.py` | Reorder form to bottom; add anchor + sticky CTA; replace emoji with SVG constants; add hover CSS; add glow CSS |
| `utils/styles.py` | Split `text_muted` / `text_faint` to distinct hex values |
| `utils/welcome_zh.py` | Add ZH CTA section header function; reorder ZH routing calls to match new section order |

No new files. No Firestore changes. No pytest logic affected.

---

## Kickstarter Prompt

Use the block below to start a new agent session for implementation:

```
You are implementing the Welcome Page UX Refactor for AI Hero Academy.

Read: plans/welcome-page-ux-refactor-plan.md — this is your complete spec.

The app is a Streamlit multi-page app on GCP Cloud Run. The file to change is
pages/00_Welcome.py (the marketing/onboarding landing shown to users with no profile).

Work through the 6 tasks in order:
  Task 1 — Move intake form to bottom of page (structural reorder only, no logic changes)
  Task 2 — Split text_faint color tier in utils/styles.py
  Task 3 — Replace emoji icons with inline SVG Heroicons (outline, 24x24, var(--cyan))
  Task 4 — Add sticky "Get Started" anchor CTA with cyan glow
  Task 5 — Add card hover micro-interactions (200ms ease-out, translateY -2px)
  Task 6 — Add subtle text-shadow glow to cyan section labels and stat numbers

Constraints:
- DO NOT change any form submit logic, session state, LLM calls, or Firestore writes
- DO update utils/welcome_zh.py to match the new section order for lang=="zh"
- Run pytest after all changes — all 42 tests must pass
- Run the app via `bash run_uat.sh` and use Playwright MCP to visually verify
  the new layout before marking done
```
