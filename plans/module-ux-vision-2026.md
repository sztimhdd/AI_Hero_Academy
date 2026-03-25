# Module Experience — UX Vision 2026

> Generated: 2026-03-25 | Skill: ui-ux-pro-max | Type: VISION / ART OF POSSIBLE
> Status: **EXPLORATORY** — not a task list; a north star for future sprints
> Scope: `pages/04_Course_Module.py` — all 5 sub-views

---

## The Honest Starting Point

The current module is functional and coherent. The dark OLED palette is correct for the
product type. But it was built sub-view by sub-view, not as a unified experience. The
result is a page that *works* but doesn't *feel* like anything.

The skill's design system query for this product returns a single verdict:

> **AI-Native UI** — Minimal chrome, streaming text, context cards, smooth reveals.
> Best for: AI products, copilots, AI-powered tools, conversational interfaces.

That's exactly what this is. An AI coach living inside a learning module. The current UI
treats it like a form. The 2026 opportunity is to make it feel like a conversation.

---

## The Concept: "The Terminal"

**One metaphor, five views.**

A professional sits down at their workstation. The interface feels like a focused
workspace — not a course platform, not a chatbot, not a quiz app. Something between
a code editor, a Bloomberg terminal, and a personal tutor.

Dark. Dense with meaning. Zero decoration. Every element earns its place.

The module number in the top-left. The skill domain glowing in cyan. The content
occupies the full available space. No sidebars fighting for attention. No Streamlit
chrome bleeding through.

The key shift: **the AI stops being a feature and becomes the interface itself.**

---

## Design System for This Vision

Synthesised from skill outputs across style, color, animation, and product domains.

### Style: AI-Native Dark OLED + Swiss Grid discipline
The current palette (`#0D0F14` base, cyan `#00D4E8`) is the right foundation.
Upgrade with:
- **Swiss 12-column grid discipline** — content zones are mathematically fixed, not
  Streamlit's fluid reflow. Use CSS Grid injected via `st.markdown`.
- **Cinematic Cinema Dark refinements** — ambient gradient blobs (very subtle,
  `opacity: 0.06–0.08`) behind the active content zone to give it depth without noise
- **AI-Native minimal chrome** — strip all visible Streamlit UI chrome from the module
  page (sidebar, top header, padding) so the module content is the entire viewport

### Typography: Upgrade the tri-stack
Current: DM Serif Display / Inter / IBM Plex Mono
Upgrade:

| Role | Current | Proposed | Why |
|------|---------|----------|-----|
| Display / score | IBM Plex Mono | **JetBrains Mono** | Tighter letter-spacing, designed for code + data, more premium |
| Content headings | DM Serif Display | **Keep** | Distinctive, warm serif contrast works on dark |
| Body | Inter | **Keep** | Perfect for body — don't change what works |
| Module number / label | IBM Plex Mono | **JetBrains Mono** | Consistent mono stack |

### Color: Add an indigo layer
The current palette is cyan-only for accents. In 2026 AI product design,
the dominant accent language is **indigo + cyan** — indigo for AI-generated content,
cyan for interactive/user actions.

```
Current:
  --cyan: #00D4E8      ← user actions, CTAs, labels

Proposed addition:
  --indigo: #6366F1    ← AI-generated content borders, coach bubbles, generated summaries
  --indigo-glow: rgba(99, 102, 241, 0.15)   ← ambient fill behind AI content zones
  --indigo-border: rgba(99, 102, 241, 0.3)  ← left-border on coach messages
```

This gives the interface a clear **signal grammar**: cyan = you, indigo = the AI.
Users learn it unconsciously within the first session.

---

## The Five Sub-Views Reimagined

### 1. OVERVIEW — "Mission Briefing"

**Current:** Title + step strip + About expander + single CTA button

**2026 vision:**
```
┌─────────────────────────────────────────────────────────────┐
│  MODULE 03                              STRATEGIC PROMPTING │  ← JetBrains Mono, right-aligned
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CSS: The Copilot Surface Selector Framework         │  │  ← DM Serif 2rem
│  │                                                      │  │
│  │  ○ ── ○ ── ○   Read · Practice · Evaluate           │  │  ← step dots, minimal
│  │  ●                                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─── WHAT YOU'LL LEARN ──────────────────────────────┐  │
│  │  By the end of this module you will be able to:    │  │  ← Inter, warm intro
│  │  • Choose the right Copilot surface for each task  │  │
│  │  • Avoid the 3 most common Copilot routing errors  │  │
│  │  • Apply the CSS framework to your daily workflow  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                             │
│  [  Begin Reading  →  ]           Est. 12 min              │
└─────────────────────────────────────────────────────────────┘
```

Key changes:
- Domain label top-right (not buried in an expander)
- "What you'll learn" bullets derived from `capability_tags` — always visible, never hidden
- Time estimate prominent but subordinate
- Full-bleed card, no Streamlit container chrome

---

### 2. READING — "The Briefing Room"

**Current:** 4-section segmented control + card content + Prev/Next buttons

**2026 vision — Focus Mode:**

Strip everything except the content. Full-width reading zone. IBM Plex Mono section
label in the top-left. Content fills `max-width: 65ch` centered. Prev/Next are ghost
buttons that appear on hover at the edges. The section indicator is a minimal dot
trail at the bottom, not a segmented control widget.

```
[Concept]  ●  ○  ○  ○          ← bottom dot trail, not top segmented control
```

**The key 2026 upgrade — structured reading cards:**

Replace the current flat `concept_text` wall of text with a **structured insight card** pattern:

```
┌─────────────────────────────────────────────────────────────┐
│  CONCEPT                                                    │  ← JetBrains Mono label
│                                                             │
│  The CSS framework maps every Copilot capability to one of  │  ← Inter, max 65ch
│  three surfaces: Compose, Summarise, and Search. Each       │
│  surface has a different input expectation and output       │
│  contract.                                                  │
│                                                             │
│  ┌─ KEY PRINCIPLE ─────────────────────────────────────┐  │
│  │  Surface mismatch is the #1 reason Copilot responses │  │  ← indigo left-border callout
│  │  feel generic. Choose the surface before writing     │  │
│  │  the prompt.                                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

The **Good Example** section becomes a split-panel:
```
┌──────────────────────┬───────────────────────────────────┐
│  WITHOUT CSS         │  WITH CSS                         │
│  ──────────────────  │  ─────────────────────────────── │
│  "Summarise my       │  "I'm in Outlook. Summarise this │
│  email thread."      │  email thread into 3 bullets,    │
│                      │  flagging any action items."     │
│  Generic response.   │  Surface-aware. Much better.     │
└──────────────────────┴───────────────────────────────────┘
```

The **Pitfall** section uses a red-accent warning card (not `st.warning` yellow).

The **Takeaway** section uses a full-bleed cyan-accent card — the most visually
prominent card on the page — because this is the durable memory anchor.

Animation: each section fades in with `opacity: 0 → 1` + `translateY(8px → 0)` over
`300ms ease-out`. Respects `prefers-reduced-motion`.

---

### 3. PRACTICE — "The Coach"

This is the biggest opportunity. The current chat UI looks like a Streamlit default.
The 2026 vision makes the AI feel like a genuine expert colleague.

**Current:** `st.chat_message` bubbles + `st.chat_input` at bottom

**2026 vision — The Coach Interface:**

**Signal grammar in action:**
- **User messages**: right-aligned, `bg: var(--bg-elevated)`, `border: 1px solid var(--border)`, `border-radius: 16px 16px 4px 16px`
- **Coach messages**: left-aligned, `bg: var(--indigo-glow)`, `border-left: 3px solid var(--indigo)`, `border-radius: 4px 16px 16px 16px` — unmistakably AI-generated

```
┌─────────────────────────────────────────────────────────────┐
│  TASK 2 / 4  ·  CSS: SURFACE SELECTOR                       │  ← JetBrains Mono
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ SCENARIO ──────────────────────────────────────────┐  │
│  │  You need to prepare for a client call at Northern  │  │  ← collapsed after first read
│  │  Fabrication Ltd. You have an email thread...       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─── Coach ─────────────────────────────────────────────┐ │  ← indigo left border
│  │  Good start. You identified the Summarise surface     │ │
│  │  correctly. Now — which Copilot tool in M365 would   │ │
│  │  you actually open first, and why?                   │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│                    ┌─── You ──────────────────────────┐   │  ← right-aligned
│                    │  I'd use Copilot in Outlook to   │   │
│                    │  summarise the thread first...   │   │
│                    └──────────────────────────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Your response...                           Send → │   │  ← sticky input
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Streaming text:** Coach responses render character-by-character with a blinking
cursor — not instant. This is the single highest-impact UI change possible. It makes
the AI feel alive. Implementation: render coach text progressively using
`st.session_state` to track streamed characters + `st.rerun()` on each chunk.
(Or, on upgrade to Streamlit ≥ 1.33, use `st.write_stream`.)

**Turn counter:** Not a warning. A quiet progress indicator:
`3 exchanges · 2 remaining before next task`
IBM Plex Mono, `var(--text-faint)`, no colour change until 1 remaining.

**MCQ options:** Full-width stacked buttons, not horizontal columns. Each option is a
card with `border: 1px solid var(--border)` that changes to `border-color: var(--cyan)`
on hover and `background: rgba(0,212,232,0.08)` on selection.

---

### 4. EVALUATION — "The Assessment"

**Current:** Radio buttons + text area + progress bar

**2026 vision — The Exam Room:**

One question fills the viewport. No distractions. The progress is communicated by a
thin progress rail at the very top of the page (like a reading progress indicator in
a news article) — `height: 3px`, `background: var(--cyan)`, `transition: width 400ms ease`.

```
┌─────────────────────────────────────────────────────────────┐
│ ████████████████████░░░░░░░░░  ← 3px top rail, 75% done   │
│                                                             │
│  QUESTION 3 / 4  ·  STRATEGIC PROMPTING                    │  ← JetBrains Mono
│                                                             │
│  ┌─ SCENARIO ──────────────────────────────────────────┐  │
│  │  Your colleague sends you a 40-page policy update.  │  │
│  │  You need to find the section on data handling...   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Which Copilot surface best fits this task?                │  ← Inter 1.1rem
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  A.  Compose — generate a summary from scratch       │  │  ← full-width option card
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  B.  Search — ask it to find the section             │  │  ← hover: cyan border
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  C.  Summarise — ask for a structured overview       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│                              [ Confirm Answer → ]          │
└─────────────────────────────────────────────────────────────┘
```

**Performance task (open-ended):** The text area is full-width, minimal border,
monospaced font — feels like writing in a code editor, not a Google Form. Character
count displayed as `143 / 600` in JetBrains Mono, bottom-right of the textarea.

---

### 5. RESULTS — "The Debrief"

**Current:** `st.metric` + `st.progress` bar + coach note container + success banner

**2026 vision — The Score Card:**

This is a cinematic moment. The score should feel earned. The UI should acknowledge it.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                          3.2 / 4.0                         │  ← JetBrains Mono 4rem, centered
│                       PRACTITIONER                         │  ← Inter 600, var(--cyan)
│                     ▲ +0.8 from baseline                   │  ← green delta
│                                                             │
│  ████████████████████████████░░░░░░░  80%                 │  ← domain progress, cyan gradient
│  Strategic Prompting                                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  COACH NOTE                                          │  │  ← indigo left border
│  │                                                      │  │
│  │  You clearly understand surface selection. Where     │  │  ← streaming text reveal
│  │  you can go deeper: your Task 3 response treated     │  │
│  │  Search and Summarise as interchangeable. They're    │  │
│  │  not — Search retrieves, Summarise synthesises.      │  │
│  │  That distinction will matter for complex queries.   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  [ View Profile ]              [ Module 4: Next Topic → ]  │
└─────────────────────────────────────────────────────────────┘
```

Key upgrade: **the coach note streams in** after the score renders, with a 600ms delay.
It feels like the coach is reading your work and composing their thoughts. Same
indigo grammar as the Practice sub-view — the AI voice is always indigo.

**All-complete state:** The hexagon radar chart appears here — a mini version, showing
the user's full skill polygon updated in real time. This replaces `st.balloons()` with
something that actually means something. The polygon edges animate from the previous
values to the new values over 1.2 seconds (SVG `stroke-dashoffset` animation or
Plotly `frame` animation).

---

## Implementation Reality Check

| Vision Element | Streamlit Feasibility | Effort |
|---------------|----------------------|--------|
| CSS Grid zone layout | ✅ `st.markdown(unsafe_allow_html=True)` | Low |
| Indigo AI signal grammar | ✅ CSS custom properties | Low |
| JetBrains Mono font swap | ✅ Google Fonts `<link>` | Trivial |
| Structured reading cards | ✅ Custom HTML in `st.markdown` | Medium |
| Good/Bad split panel | ✅ CSS Grid in HTML block | Medium |
| Cyan top progress rail | ✅ CSS + session state fraction | Low |
| Full-width MCQ cards | ✅ Replace `st.radio` with `st.button` columns | Medium |
| Streaming coach text | ⚠️ `st.write_stream` (Streamlit ≥ 1.33) OR `st.rerun()` loop | High |
| Score card centered layout | ✅ Custom HTML | Low |
| Radar on Results page | ✅ Plotly (already imported) | Medium |
| Animated radar polygon | ⚠️ Plotly frames — complex but possible | High |
| Ambient gradient blobs | ✅ CSS `radial-gradient` + `position:fixed` | Low |
| 65ch max-width reading | ✅ CSS on content container | Trivial |

**The one transformative change with lowest effort:** indigo AI grammar + structured
reading cards. Both are CSS + HTML changes. No new libraries. No Streamlit API risk.
Combined, they make the module feel like a different product.

**The one transformative change with highest impact per effort:** streaming coach text.
`st.write_stream` in Streamlit ≥ 1.33 makes this a 3-line change in `utils/ai.py`.
Check the current Streamlit version first.

---

## Aesthetic Reference Points

These are the products this vision is deliberately positioned between:

| Reference | What we borrow |
|-----------|---------------|
| **Linear** (project management) | Dark palette, JetBrains Mono data density, cyan accent language |
| **Cursor** (AI code editor) | Indigo for AI-generated content, streaming text, minimal chrome |
| **Brilliant** (learning app) | One question per screen, focus mode, reward on completion |
| **Vercel dashboard** | Swiss grid discipline, monospace numbers, surface depth system |
| **Perplexity** | AI voice always distinct from UI chrome, context cards |

None of these are learning platforms. That's the point. The people who will use
AI Hero Academy are professionals who use Linear, Cursor, and Vercel. The bar they
carry in their heads is set by those products. A Streamlit-default quiz page next to
those references feels like a downgrade. The Terminal concept meets them where they are.

---

## Recommended Sprint Structure

This vision is too large for one sprint. Suggested phasing:

**Sprint 1 — Signal Grammar** (low effort, high impact)
- Indigo CSS tokens + left-border on all AI-generated content
- JetBrains Mono font swap for mono stack
- Structured reading cards (concept, good/bad split panel, cyan takeaway)
- Full-width MCQ buttons (replace radio)
- Cyan top progress rail on evaluation

**Sprint 2 — The Coach Interface** (medium effort)
- User/coach message bubble redesign (right/left alignment, signal grammar borders)
- Turn counter redesign (quiet, not warning)
- Streaming text for coach responses (if Streamlit ≥ 1.33)

**Sprint 3 — Cinematic Moments** (high effort)
- Score card centered layout with animated delta
- Coach note streaming on results page
- Mini radar chart on results (animated polygon)
- Ambient gradient blobs on module background

---

## What This Does NOT Change

- Firestore schema — no data changes
- Scoring logic — no AI changes
- Module sequence — no path changes
- pytest suite — all 42 tests remain valid
- ZH language support — all HTML changes use `t()` for text content

The Terminal is a skin, not a rebuild. The product underneath is already right.
The job is to make the surface worthy of the content inside it.
