# Plan: Executive Demo Page (Welcome Page Redesign)

**Status**: READY TO IMPLEMENT
**Branch**: `feature/demo-page`
**Scope**: `pages/00_Welcome.py` (full rewrite of content section) + `assets/screenshots/` (Playwright-captured)
**ADR Reference**: `plans/master-architecture.md`

---

## Purpose

Replace the minimal Welcome page with a self-contained **Executive Demo Page** — a scrollable, interactive-feel showcase that lets leaders (CIO/SVP/Board) understand the solution's design, methodology, coursework structure, and business value in a single sitting. This is the app's "front door" and primary selling document.

**Audience**: Two audiences in one scroll.

- **CIO / SVP / Board**: arrive having been told this product exists; want to understand the methodology, see the actual UI, and judge whether it's worth rolling out to 3,000 employees. They leave either approving a pilot or asking for a follow-up meeting.
- **Individual contributor (new user)**: arrives to register. They scroll briefly, see relevance, and click "Start My Diagnostic."

The page must convert both audiences in a single pass.

**Constraints**:
- The routing guard at the top of `00_Welcome.py` **must be preserved** — returning users are immediately redirected to their state; only new/unregistered users see this page.
- Pure Streamlit (no React, no external server, no websockets). All interactivity via `st.tabs()`, `st.expander()`, `st.columns()`, CSS.
- Screenshots of actual app pages are captured by Playwright during implementation and embedded as `st.image()` calls.
- Must load in < 2 seconds (no external API calls on this page).

---

## Reference Sites Studied

| Site | Key Pattern Borrowed |
| --- | --- |
| LeanIX Enterprise Architecture | Browser-mockup product screenshot as hero centerpiece |
| ServiceNow AI Platform | Dark hero + tabbed capability tour + bold metric bar |
| Databricks Genie Code | Eyebrow label + punchy single-line headline + two-CTA structure |
| OpenAI Codex | Feature-card grid with headings and short descriptions |
| Claude Code | Minimal cream hero, "built for X" dynamic framing, logo social proof |

**Common structural patterns across all 5**:

1. Eyebrow label (product category) → punchy headline → 1-line sub-headline → 1-2 CTAs
2. Product screenshot in a device/browser frame below the fold
3. 3–6 value-prop cards with icon + title + 2-line description
4. Tabbed or sectioned capability tour
5. Social proof (metrics or logos)
6. Scrollable narrative — each section answers the next executive question

---

## Page Architecture (8 Sections)

```text
┌─────────────────────────────────────────────────────────┐
│  Section 1 — HERO                                       │
│  Brand mark · Bold headline · Sub-headline · CTAs       │
├─────────────────────────────────────────────────────────┤
│  Section 2 — THE CHALLENGE (why this exists)            │
│  3 external stat cards + EDC internal use-case callout  │
├─────────────────────────────────────────────────────────┤
│  Section 3 — THE LEARNING LOOP (our answer)             │
│  4-stage horizontal flow: Diagnose→Map→Train→Score      │
├─────────────────────────────────────────────────────────┤
│  Section 4 — INSIDE THE PLATFORM (tabbed screenshots)   │
│  st.tabs(): Diagnostic / Skills Profile / Course /      │
│             AI Coach / Results                          │
├─────────────────────────────────────────────────────────┤
│  Section 5 — WHAT MAKES IT DIFFERENT (4 differentiators)│
│  Role scenarios · AI coach · Personalized path ·        │
│  Built on your Databricks workspace                     │
├─────────────────────────────────────────────────────────┤
│  Section 6 — THE SKILL MODEL (6 domains + progression)  │
│  6-domain hexagon model · 5-level mastery scale         │
├─────────────────────────────────────────────────────────┤
│  Section 7 — GET STARTED (role selector + CTA)          │
│  Preserved onboarding form + pilot/team framing note    │
├─────────────────────────────────────────────────────────┤
│  Section 8 — WHAT'S COMING (Future Features)            │
│  Honest roadmap: more roles, org dashboard, Copilot     │
└─────────────────────────────────────────────────────────┘
```

---

## Section Specifications

### Section 1 — Hero

**Visual target**: ServiceNow / Databricks dark-hero pattern.

```text
⚡ AI Hero Academy                     [Databricks Internal · AI Skills Platform]

Turn every employee into an
AI-powered professional.

Not another e-learning course.
A diagnostic engine + personalized path + live AI coaching,
built specifically for each role — and ready for your entire team.

[Start My Diagnostic →]   [See How It Works ↓]
```

- Background: `var(--bg-primary)` (#0D0F14) — existing design system
- Headline: DM Serif Display, ~2.8rem, `var(--text)` white
- Sub-headline: Inter 400, 1rem, `var(--text-muted)` grey
- Primary CTA: existing `.stButton` primary style (cyan)
- Secondary CTA: text link with arrow (anchor link to Section 4)
- **Do not** add a background product screenshot here — the platform screenshots live in Section 4 as the "product reveal"

### Section 2 — The Challenge

Three metric cards arranged in `st.columns(3)`, styled as the existing `.aha-card` but with a large stat number.

| Stat | Source | Framing |
| --- | --- | --- |
| **68%** of employees want AI training more than job security | Predictive Index 2025 | "Your people are asking for this" |
| **3×** more AI usage than leaders expect — shadow AI is rampant | McKinsey Superagency 2025 | "It's already happening" |
| **48%** cite lack of training as the #1 adoption blocker | McKinsey Superagency 2025 | "Training unlocks ROI" |

Card structure: large stat number in `var(--cyan)`, bold label, 1-line context sentence, tiny source citation in muted text.

**EDC internal callout** — rendered as a full-width highlighted box below the 3 stat cards:

```text
At EDC, over 100 employees have already submitted AI use case requests.
Meeting support, document summarization, and email drafting rank as the top three needs.
This platform builds the skills to do them right — securely, consistently, at scale.
```

Style: `var(--bg-elevated)` background, left border `var(--cyan)` 3px, italic body text, `var(--text-muted)`. No external source citation — this is internal data framed as organizational context, not a published stat. This callout bridges the external research above with the CIO's direct knowledge of their workforce.

### Section 3 — The Learning Loop

Four-stage horizontal flow diagram built with `st.columns(4)`. Each column = one stage card.

| Stage | Icon | Label | What happens |
| --- | --- | --- | --- |
| 1 | 🎯 | **Diagnose** | 12-item adaptive assessment reveals exact skill gaps across 6 domains in ~5 minutes |
| 2 | 🗺️ | **Map Gaps** | AI generates a personalized narrative gap map and sequences your training path |
| 3 | 🤖 | **Train** | Role-specific scenarios + live AI coach. You practice; the coach responds to YOUR answers |
| 4 | 📊 | **Score & Track** | Hexagon skill radar updates after each module. Watch your gaps close over time |

Between each column: a `→` arrow rendered via CSS (`::after` pseudo-element or inline HTML `›`).

At the bottom of section 3: a subtle callout box:
```text
The path is yours. Module 1 unlocks immediately based on your biggest gap —
not a fixed curriculum everyone follows in the same order.
```

### Section 4 — Inside the Platform

This is the centrepiece — a tabbed screenshot gallery showing the actual app.

```python
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Diagnostic",
    "🗺️ Skills Profile",
    "📚 Course Module",
    "🤖 AI Coach",
    "📊 Results"
])
```

Each tab contains:
- A Playwright screenshot of the actual app page (taken during implementation, saved to `assets/screenshots/`)
- A 2-sentence caption below the screenshot explaining what the user is seeing
- Image rendered via `st.image(path, use_container_width=True)`

**Screenshots to capture during implementation** (Playwright + seeded profiles):

| Tab | Screenshot target | Seed command |
| --- | --- | --- |
| Diagnostic | Question 4 of 12 visible | `--role rm` → navigate to Diagnostic page |
| Skills Profile | Hexagon radar + gap bullets visible | `--role rm --diag` |
| Course Module | Reading view of Module 1 | `--profile course-built` → open module |
| AI Coach | Practice view with 2 coach turns visible | `--profile course-built` → Practice sub-view |
| Results | Score breakdown + coach note | `--profile m1-done` → Module 1 Results |

Screenshot save path: `assets/screenshots/demo_01_diagnostic.png`, `demo_02_skills_profile.png`, etc.

**Caption copy**:

| Tab | Caption |
| --- | --- |
| Diagnostic | "A 12-item adaptive assessment. Questions mix multiple choice, prompt sandbox tasks, and micro-scenarios. Takes ~5 minutes. Scores all 6 AI skill domains simultaneously." |
| Skills Profile | "Your hexagon radar shows exactly where you stand. The AI-generated gap map turns raw scores into plain-language priorities you can act on today." |
| Course Module | "Each module opens with a reading section that explains the core framework — then immediately asks you to apply it to a realistic work scenario." |
| AI Coach | "The AI coach responds to what you actually wrote — not a scripted flow. It asks follow-up questions, flags weak reasoning, and models better approaches in real time." |
| Results | "After each module, you get a score breakdown by rubric criterion and a personalized coach note. Your hexagon radar updates immediately." |

### Section 5 — What Makes It Different

Four-column card grid (`.aha-card` style), each with a strong differentiator headline. Use `st.columns(4, gap="medium")` — 4 cards fit at 1440px; the 4th card (infrastructure) speaks directly to the CIO's trust and data-residency question.

| Card | Headline | Body |
| --- | --- | --- |
| 1 | **Your role. Your scenarios.** | Every practice task is built around real work situations for your specific role — RM, Underwriter, Analyst. No generic "write a prompt about dogs" exercises. |
| 2 | **An AI coach that actually reads your answer.** | The coach sees exactly what you wrote and responds with contextual feedback. It can't be fooled by a vague answer — it will push back. |
| 3 | **Your gaps drive the sequence.** | The diagnostic scores 6 domains. Module 1 is the domain where you need the most help — not the one that comes first alphabetically. |
| 4 | **Your data never leaves your workspace.** | Built as a Databricks App and served from your EDC environment. No data sent to third-party training platforms. No external user accounts. |

Card 4 is a **built** architectural fact — the app runs as a Databricks App on the EDC workspace with SSO. It is not a roadmap item.

### Section 6 — The Skill Model

Six-domain grid (`st.columns(3)` × 2 rows), each domain rendered as a pill/card.

| Domain ID | Display label | Employee reframe | Emoji |
| --- | --- | --- | --- |
| `responsible_ai` | Responsible AI | Protect your professional reputation | 🛡️ |
| `strategic_prompting` | Strategic Prompting | Your personal productivity superpower | ⚡ |
| `critical_eval` | Critical Evaluation | Never be caught out by an AI error | 🔍 |
| `data_decision` | Data & Decision | Generate insights in minutes, not hours | 📊 |
| `relationship_intel` | Relationship Intelligence | Know every stakeholder better than anyone | 🤝 |
| `augmented_comm` | Augmented Communication | Deliver polished outputs 3× faster | ✍️ |

Below the domain grid, two callouts stacked:

**Industry alignment note** (one line):

```text
Aligned with the Alan Turing Institute's AI Skills Framework for Knowledge Workers (2024).
```

**5-level mastery progression** (rendered as a horizontal pill row, amber accent on the middle level):

```text
Unaware  →  Explorer  →  Practitioner  →  Proficient  →  Champion
```

Style: 5 pills in a flex row, center-aligned. All pills `var(--bg-elevated)` + `var(--border)` border, grey text. The middle pill ("Practitioner") uses `var(--amber)` border and `var(--text)` white — signals the "target state" without a caption. A one-line note below in muted text:

```text
Every domain is scored independently. The diagnostic tells you exactly where you sit on each axis.
```

This progression is a **built** feature — the level labels (Unaware → Champion) are calculated from domain scores in the existing scoring logic and displayed on the Skills Profile page.

### Section 7 — Get Started

**Preserved exactly from the original Welcome page** — role selector, display name input, "Start My Diagnostic →" button, routing logic, and privacy footer note. This section is the conversion point.

Section header copy:
```text
Choose your role and begin.

Your 5-minute diagnostic is waiting.
Results are visible only to you — no manager dashboard, no rankings.
```

**Pilot note** — rendered below the role selector as a muted callout (not a form element):

```text
Piloting with a team? Every employee takes the same diagnostic independently
and gets their own personalized path. No shared account. No group score.
```

This note is **accurate** — each user creates their own profile via Databricks SSO and all data is filtered by `user_email`. No new functionality is implied. It reframes the existing individual-user architecture as a CIO-friendly deployment model.

### Section 8 — What's Coming

A forward-looking section that sets honest expectations without overpromising. Rendered as an `st.expander("Roadmap →", expanded=False)` to keep it from dominating the page.

Inside the expander: a 2-column grid of feature cards styled as `.demo-diff-card` with `var(--border)` border and a `🔜` badge.

| Feature | Description | Phase |
| --- | --- | --- |
| 🔜 **More roles** | PM, Engineer, Legal, Finance — same methodology, role-specific scenarios | Phase 1 |
| 🔜 **Org-level dashboard** | Admin view: completion rates, average scores by department, skill gap heatmap | Phase 3+ |
| 🔜 **Board-ready metrics** | % workforce at Practitioner+ per domain; exportable for quarterly reporting | Phase 3+ |
| 🔜 **Microsoft Copilot track** | A dedicated module covering M365 Copilot — the tool most frequently requested by employees | Phase 1+ |

**Implementation note**: use `st.expander()` so the section collapses by default — it rewards curiosity without distracting the main CTA flow. The table above should be rendered as 4 cards in `st.columns(2)`, not a raw HTML table, to maintain visual consistency.

**Copy above expander** (always visible):

```text
This is version 1. Three roles are live today.
The roadmap below reflects what's already being built.
```

---

## Demo Assets

Three tiers of media are needed. Static screenshots are **required** (embedded in Section 4). GIFs and video are **optional** but significantly increase executive impact.

---

### Tier 1 — Static Screenshots (Required, 5 PNGs)

Embedded via `st.image()` in Section 4 tabs. Captured with Playwright at 1440 × 900.

| # | Save path | Tab | What must be visible |
| --- | --- | --- | --- |
| 1 | `assets/screenshots/demo_01_diagnostic.png` | 🎯 Diagnostic | Question 4 of 12; question text + answer options clearly readable; progress indicator at top |
| 2 | `assets/screenshots/demo_02_skills_profile.png` | 🗺️ Skills Profile | Full hexagon radar + at least 2 gap bullets; domain labels legible |
| 3 | `assets/screenshots/demo_03_course_module.png` | 📚 Course Module | Reading view; concept heading + first 3–4 paragraphs visible; sidebar collapsed |
| 4 | `assets/screenshots/demo_04_ai_coach.png` | 🤖 AI Coach | Practice view; task prompt visible + at least 1 completed coach exchange (user turn + coach reply) |
| 5 | `assets/screenshots/demo_05_results.png` | 📊 Results | Score breakdown table + coach note text; hexagon radar if it fits in viewport |

**Recommended persona for each screenshot** (demo mode preferred — DML writes are suppressed, personas are stable, no risk of polluting prod data):

| Screenshot | Persona | Seed method | URL |
| --- | --- | --- | --- |
| 1 — Diagnostic | **3b** Alex Chen (RM) | demo mode auto-seeds | `localhost:8501?demo=true` → select 3b → navigates to Diagnostic → answer Q1–Q3 manually to reach Q4 |
| 2 — Skills Profile | **3c** Jordan Lee (UW) | demo mode auto-seeds | `localhost:8501?demo=true` → select 3c → auto-routes to Skills Profile |
| 3 — Course Module | **3c** Jordan Lee (UW) | same session | Home → click Module 1 → Reading sub-view |
| 4 — AI Coach | **3c** Jordan Lee (UW) | same session | Home → Module 1 → Practice → type a response to Task 1 → send → wait for coach reply → screenshot |
| 5 — Results | **3c** Jordan Lee (UW) | same session | Home → Module 1 → Results sub-view (Module 1 is already complete for 3c) |

**Alternative using UAT reset** (if demo mode is unavailable or you prefer your own dev account):

```bash
# Screenshot 1 — Diagnostic
python scripts/reset_uat_user.py --role rm
# Open localhost:8501 → auto-routes to Diagnostic → answer Q1–Q3 → screenshot at Q4

# Screenshot 2 — Skills Profile
python scripts/reset_uat_user.py --role rm --diag
# Open localhost:8501 → auto-routes to Skills Profile → screenshot

# Screenshots 3, 4 — Course reading + AI coach
python scripts/reset_uat_user.py --profile course-built
# Open localhost:8501 → Home → Module 1 → Reading → screenshot
# Then → Practice → send one message → wait for reply → screenshot

# Screenshot 5 — Results
python scripts/reset_uat_user.py --profile m1-done
# Open localhost:8501 → Home → Module 1 → Results → screenshot
```

---

### Tier 2 — Animated GIFs (Optional, 2 GIFs)

Swap in place of the static PNG for Section 4's two highest-impact tabs: **AI Coach** and **Skills Profile**. Dramatically more convincing than a still for an async executive audience.

| # | Save path | Tab | What to record | Target duration | Persona |
| --- | --- | --- | --- | --- | --- |
| A | `assets/screenshots/demo_04_coach_animated.gif` | 🤖 AI Coach | Task 1 prompt visible → user types a response → clicks Send → coach reply streams in → reply fully rendered | 8–12 s | **3c** Jordan Lee (UW) |
| B | `assets/screenshots/demo_02_skills_animated.gif` | 🗺️ Skills Profile | Page loads → hexagon radar draws → gap bullets fade in one by one | 4–6 s | **3c** Jordan Lee (UW) |

**How to record on Windows (ScreenToGif)**:

```text
Tool: ScreenToGif — free, no install required
      Download: https://www.screentogif.com/

Steps:
  1. Start app: bash run_uat.sh
  2. Navigate to localhost:8501?demo=true → select persona 3c (Jordan Lee, UW)
  3. Open ScreenToGif → Recorder → select region
     — Capture only the Streamlit main content area (exclude the browser chrome + sidebar)
     — Recommended capture size: ~1100 × 800 px
  4. Set frame rate: 10 fps (sufficient); 15 fps for the coach typing animation
  5. Record the target interaction
  6. In the ScreenToGif editor:
     — Trim 0.5 s dead frames from start and end
     — Add a 1.5 s hold on the final frame so the last state is readable
     — Reduce colors to 128 if file size > 2 MB (Optimize tab)
  7. File → Save As → GIF → save to assets/screenshots/
  8. Target file size: < 2 MB per GIF (Streamlit loads GIFs synchronously)
```

**Implementation note**: In Section 4, check at runtime whether the animated GIF exists and prefer it:

```python
import os
coach_asset = "assets/screenshots/demo_04_coach_animated.gif"
if not os.path.exists(coach_asset):
    coach_asset = "assets/screenshots/demo_04_ai_coach.png"
st.image(coach_asset, use_container_width=True)
```

---

### Tier 3 — Video Walkthrough (Optional, 1 MP4)

Not embedded in the page. Used for async stakeholder sharing (Slack, email, Board pack).

| # | Save path | Duration | Personas used | Narrative arc |
| --- | --- | --- | --- | --- |
| V1 | `assets/demo_walkthrough.mp4` | 2–3 min | 3b → 3c → 3d | Employee arrives → takes diagnostic (3b) → sees their gap map (3c) → coaches through a module → views full results (3d) |

**How to record (OBS Studio)**:

```text
Tool: OBS Studio — free
      Download: https://obsproject.com/

Suggested scene config:
  — Source: Window Capture → select the browser window
  — Resolution: 1440 × 900 (or match your monitor)
  — Bitrate: 2500 kbps (sufficient for screen capture)
  — Output: MP4, H.264

Suggested script (3 acts, ~45 s each):
  Act 1 (Diagnose): persona 3b → Diagnostic page →
    show Q1, Q4, Q12 → submit → scoring spinner
  Act 2 (Profile + Course): persona 3c → Skills Profile →
    hexagon + gap bullets → Home → Module 1 → Reading →
    Practice (type + send + coach reply)
  Act 3 (Results): persona 3d → Home (all modules complete) →
    any completed module → Results → full hexagon
```

**Demo mode for video recording**: always use `?demo=true` personas. DML suppression ensures no accidental data writes during the recording. Switching personas is instant (sidebar dropdown) — no DB reset required between acts.

---

### Demo Personas Quick Reference

| Persona | Name | Role | State | Best for |
| --- | --- | --- | --- | --- |
| **3a** | Demo User | — | Fresh (Welcome page) | Recording the Welcome/demo page itself |
| **3b** | Alex Chen | RM | Profile only; Diagnostic not started | Diagnostic screenshots/recording |
| **3c** | Jordan Lee | UW | Diagnostic complete; Module 1 complete | Skills Profile, Course, Coach, Results |
| **3d** | Taylor Kim | AN | All 7 modules complete | Full results, completed hexagon, Board-ready view |

**Activating demo mode**: append `?demo=true` to any `localhost:8501` URL. A persona selector appears in the sidebar. Selecting a persona auto-seeds that user's fixture data and suppresses all DML writes for the session — the app behaves exactly as a real user's session but nothing is persisted to Delta tables.

---

## CSS Strategy

All new CSS lives in a `DEMO_CSS` constant at the top of `00_Welcome.py`, injected via `st.markdown(DEMO_CSS, unsafe_allow_html=True)` after `inject_global_css()`. Never modify `utils/styles.py` for page-specific styles.

**Typography scale:**
- Hero headline: DM Serif Display 2.8rem, `var(--text)`
- Stat numbers: IBM Plex Mono 3rem, `var(--cyan)`
- Section headings: Inter 600 1.6rem, `var(--text)`
- Body / cards: Inter 400 0.82–0.9rem, `var(--text-muted)`
- Eyebrow / mono labels: IBM Plex Mono 0.68–0.72rem, uppercase, `var(--cyan)`

### DEMO_CSS constant

```python
DEMO_CSS = """
<style>
/* ─── LAYOUT & TYPOGRAPHY ───────────────────────────────── */
.demo-hero {
  padding: 5rem 0 4rem;
  text-align: center;
}
.demo-eyebrow {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--cyan);
  margin-bottom: 1.2rem;
}
.demo-headline {
  font-family: 'DM Serif Display', serif;
  font-size: 2.8rem;
  line-height: 1.15;
  color: var(--text);
  margin-bottom: 1rem;
}
.demo-headline em {
  color: var(--cyan);
  font-style: normal;
}
.demo-subhead {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-muted);
  max-width: 560px;
  margin: 0 auto 2.4rem;
}
.demo-section-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.68rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--cyan);
  margin-bottom: 0.5rem;
}
.demo-section-heading {
  font-family: 'DM Serif Display', serif;
  font-size: 1.6rem;
  color: var(--text);
  margin-bottom: 0.4rem;
}
.demo-section-sub {
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 2rem;
  max-width: 540px;
}
.demo-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 3.5rem 0;
}
/* ─── STAT CARDS (Section 2) ────────────────────────────── */
.demo-stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.8rem 1.4rem;
  height: 100%;
}
.demo-stat-number {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 3rem;
  font-weight: 500;
  color: var(--cyan);
  line-height: 1;
  margin-bottom: 0.4rem;
}
.demo-stat-label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text);
  margin-bottom: 0.5rem;
}
.demo-stat-context {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.6;
}
.demo-stat-source {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-faint);
  margin-top: 0.8rem;
}
/* ─── EDC CALLOUT (Section 2) ───────────────────────────── */
.demo-edc-callout {
  background: var(--bg-elevated);
  border-left: 3px solid var(--cyan);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.4rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-style: italic;
  color: var(--text-muted);
  line-height: 1.7;
  margin-top: 1.4rem;
}
/* ─── LEARNING LOOP (Section 3) ─────────────────────────── */
.demo-stage-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.6rem 1.2rem;
  text-align: center;
  height: 100%;
}
.demo-stage-icon  { font-size: 1.8rem; margin-bottom: 0.7rem; }
.demo-stage-num   { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: var(--cyan); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.demo-stage-label { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.95rem; color: var(--text); margin-bottom: 0.5rem; }
.demo-stage-body  { font-family: 'Inter', sans-serif; font-size: 0.8rem; color: var(--text-muted); line-height: 1.6; }
.demo-loop-callout {
  background: var(--bg-elevated);
  border-left: 3px solid var(--cyan);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 1.6rem;
  max-width: 640px;
}
/* ─── SCREENSHOT TABS (Section 4) ───────────────────────── */
.demo-screenshot-caption {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
  padding: 0.7rem 0 0;
  max-width: 680px;
  margin: 0 auto;
}
/* ─── DIFFERENTIATOR CARDS (Section 5) ──────────────────── */
.demo-diff-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.6rem 1.4rem;
  height: 100%;
}
.demo-diff-icon     { font-size: 1.4rem; margin-bottom: 0.6rem; }
.demo-diff-headline { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.95rem; color: var(--text); margin-bottom: 0.5rem; }
.demo-diff-body     { font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-muted); line-height: 1.65; }
/* ─── DOMAIN PILLS (Section 6) ──────────────────────────── */
.demo-domain-pill {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.1rem 1rem;
  height: 100%;
}
.demo-domain-emoji  { font-size: 1.3rem; margin-bottom: 0.4rem; }
.demo-domain-label  { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.85rem; color: var(--text); margin-bottom: 0.25rem; }
.demo-domain-reframe { font-family: 'Inter', sans-serif; font-size: 0.78rem; color: var(--cyan); line-height: 1.5; }
.demo-attribution   { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: var(--text-faint); text-align: center; margin-top: 1rem; }
/* ─── MASTERY PROGRESSION (Section 6) ──────────────────── */
.demo-mastery-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 1.4rem 0 0.6rem;
}
.demo-mastery-pill {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-muted);
  white-space: nowrap;
}
.demo-mastery-pill.active {
  border-color: var(--amber);
  color: var(--text);
  background: var(--bg-surface);
}
.demo-mastery-arrow { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: var(--border); }
.demo-mastery-note  { font-family: 'Inter', sans-serif; font-size: 0.78rem; color: var(--text-faint); text-align: center; margin-top: 0.4rem; }
/* ─── GET STARTED (Section 7) ───────────────────────────── */
.demo-cta-header   { text-align: center; padding: 1rem 0 2rem; }
.demo-cta-headline { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: var(--text); margin-bottom: 0.5rem; }
.demo-cta-sub      { font-family: 'Inter', sans-serif; font-size: 0.88rem; color: var(--text-muted); line-height: 1.7; }
/* ─── PILOT NOTE (Section 7) ────────────────────────────── */
.demo-pilot-note {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-style: italic;
  color: var(--text-muted);
  border-left: 2px solid var(--border);
  padding: 0.5rem 0.8rem;
  margin-top: 1rem;
  line-height: 1.6;
}
/* ─── ROADMAP CARDS (Section 8) ─────────────────────────── */
.demo-roadmap-card  { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem; height: 100%; }
.demo-roadmap-badge { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: var(--amber); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
.demo-roadmap-title { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.88rem; color: var(--text); margin-bottom: 0.35rem; }
.demo-roadmap-body  { font-family: 'Inter', sans-serif; font-size: 0.78rem; color: var(--text-muted); line-height: 1.6; }
</style>
"""
```

---

## Implementation Patterns

### Section 2 — 3 stat cards + EDC callout

```python
sc1, sc2, sc3 = st.columns(3, gap="medium")
with sc1:
    st.markdown('<div class="demo-stat-card"><div class="demo-stat-number">68%</div><div class="demo-stat-label">want AI training more than job security</div>...</div>', unsafe_allow_html=True)
# ... sc2 (3×), sc3 (48%) follow same pattern
st.markdown('<div class="demo-edc-callout">At EDC, over 100 employees...</div>', unsafe_allow_html=True)
```

### Section 3 — 4-stage learning loop

```python
lc1, lc2, lc3, lc4 = st.columns(4, gap="medium")
# Each col: demo-stage-card with demo-stage-icon, demo-stage-num, demo-stage-label, demo-stage-body
st.markdown('<div class="demo-loop-callout"><strong>The path is yours.</strong> Module 1 unlocks...</div>', unsafe_allow_html=True)
```

### Section 4 — Tabbed screenshots with GIF-over-PNG fallback

```python
import os as _os

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Diagnostic", "🗺️ Skills Profile", "📚 Course Module", "🤖 AI Coach", "📊 Results",
])

_BASE = _os.path.join(_os.path.dirname(__file__), "..", "assets", "screenshots")

_screenshots = {
    tab1: ("demo_01_diagnostic.png",    None,                            "A 12-item adaptive assessment..."),
    tab2: ("demo_02_skills_profile.png","demo_02_skills_animated.gif",   "Your hexagon radar shows..."),
    tab3: ("demo_03_course_module.png", None,                            "Each module opens with a reading section..."),
    tab4: ("demo_04_ai_coach.png",      "demo_04_coach_animated.gif",    "The AI coach responds to what you actually wrote..."),
    tab5: ("demo_05_results.png",       None,                            "After each module, you get a score breakdown..."),
}

for tab, (png_name, gif_name, caption) in _screenshots.items():
    with tab:
        asset_path = None
        if gif_name:
            gif_path = _os.path.join(_BASE, gif_name)
            if _os.path.exists(gif_path):
                asset_path = gif_path
        if asset_path is None:
            png_path = _os.path.join(_BASE, png_name)
            if _os.path.exists(png_path):
                asset_path = png_path
        if asset_path:
            st.image(asset_path, use_container_width=True)
        else:
            st.info(f"Screenshot not yet captured: `{png_name}`")
        st.markdown(f'<div class="demo-screenshot-caption">{caption}</div>', unsafe_allow_html=True)
```

### Section 5 — 4-column differentiator cards

```python
dc1, dc2, dc3, dc4 = st.columns(4, gap="medium")
# Each col: demo-diff-card with demo-diff-icon, demo-diff-headline, demo-diff-body
# Icons: 🎯 🤖 🗺️ 🔒
```

### Section 6 — Domain grid + mastery pills

```python
_DOMAINS = [
    ("🛡️", "Responsible AI",          "Protect your professional reputation"),
    ("⚡",  "Strategic Prompting",     "Your personal productivity superpower"),
    ("🔍", "Critical Evaluation",     "Never be caught out by an AI error"),
    ("📊", "Data & Decision",         "Generate insights in minutes, not hours"),
    ("🤝", "Relationship Intelligence","Know every stakeholder better than anyone"),
    ("✍️", "Augmented Communication", "Deliver polished outputs 3× faster"),
]
row1 = st.columns(3, gap="medium")
row2 = st.columns(3, gap="medium")
for i, (emoji, label, reframe) in enumerate(_DOMAINS):
    col = row1[i] if i < 3 else row2[i - 3]
    with col:
        st.markdown(f'<div class="demo-domain-pill">...</div>', unsafe_allow_html=True)

# Mastery progression pills (after domain grid)
st.markdown("""
<div class="demo-mastery-row">
  <span class="demo-mastery-pill">Unaware</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">Explorer</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill active">Practitioner</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">Proficient</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">Champion</span>
</div>
<div class="demo-mastery-note">Every domain is scored independently...</div>
""", unsafe_allow_html=True)
```

### Section 8 — Collapsed roadmap expander

```python
with st.expander("Roadmap →", expanded=False):
    rc1, rc2 = st.columns(2, gap="medium")
    # rc1: "More roles" (Phase 1) + "Board-ready metrics" (Phase 3+)
    # rc2: "Org-level dashboard" (Phase 3+) + "Microsoft Copilot track" (Phase 1+)
    # Each: demo-roadmap-card with demo-roadmap-badge, demo-roadmap-title, demo-roadmap-body
```

---

## File Changes

**Required** (must exist before `00_Welcome.py` is deployed):

| File | Change | How produced |
| --- | --- | --- |
| `pages/00_Welcome.py` | Full rewrite of content section; routing guard preserved verbatim | Implementation |
| `assets/screenshots/demo_01_diagnostic.png` | NEW | Playwright + persona 3b |
| `assets/screenshots/demo_02_skills_profile.png` | NEW | Playwright + persona 3c |
| `assets/screenshots/demo_03_course_module.png` | NEW | Playwright + persona 3c |
| `assets/screenshots/demo_04_ai_coach.png` | NEW | Playwright + persona 3c (requires live coach call) |
| `assets/screenshots/demo_05_results.png` | NEW | Playwright + persona 3c |

**Optional** (enrich Section 4 if present; gracefully falls back to PNG if absent):

| File | Change | How produced |
| --- | --- | --- |
| `assets/screenshots/demo_04_coach_animated.gif` | OPTIONAL — replaces static PNG in AI Coach tab | ScreenToGif + persona 3c |
| `assets/screenshots/demo_02_skills_animated.gif` | OPTIONAL — replaces static PNG in Skills Profile tab | ScreenToGif + persona 3c |
| `assets/demo_walkthrough.mp4` | OPTIONAL — not embedded; used for async sharing | OBS Studio + personas 3b→3c→3d |

`utils/styles.py` is read but not written to. No other files are modified.

---

## Streamlit Constraints

- `st.tabs()` — use for Section 4 screenshot gallery; do NOT nest inside `st.expander()`
- `st.image()` — use `use_container_width=True` for all demo screenshots
- `st.columns()` — use `gap="medium"` for value prop / domain grids
- `st.button()` with `type="primary"` — use for the "Start My Diagnostic" CTA
- Anchor links (`[See How It Works ↓](#section-4)`) do NOT work in Streamlit (no fragment routing); replace with a plain `↓` as visual decoration
- `st.markdown(..., unsafe_allow_html=True)` — use for all custom HTML blocks
- Before any Streamlit API use: verify current SDK via `mcp__context7__resolve-library-id` (library: "streamlit") then `mcp__context7__query-docs`

---

## Acceptance Criteria

- [ ] Page loads for a new user (no profile) and displays all 8 sections
- [ ] Returning user is immediately redirected (routing guard works, no flash of demo content)
- [ ] All 5 required PNGs exist in `assets/screenshots/` before deployment
- [ ] All 5 screenshot tabs display correctly on a 1440px wide viewport
- [ ] Where animated GIF exists, it renders in place of the static PNG (AI Coach and Skills Profile tabs)
- [ ] Section 5 renders 4 cards in a single row at 1440px (no wrapping)
- [ ] EDC internal callout renders below the 3 stat cards in Section 2
- [ ] Mastery progression pills render correctly in Section 6 with amber highlight on "Practitioner"
- [ ] Section 8 expander is collapsed by default; expands to show 4 roadmap cards in 2 columns
- [ ] Role selector + CTA at Section 7 functions as before (profile created, redirects to Diagnostic)
- [ ] `bash run_uat.sh` passes (no regressions on any UAT scenario)
- [ ] Visual check with Playwright: `browser_navigate` to `localhost:8501`, screenshot confirms all sections render
- [ ] No inline styles hardcoding colour values — all colours use CSS custom properties from `inject_global_css()`

---

## Commit

```bash
# Required assets only:
git add pages/00_Welcome.py assets/screenshots/demo_0*.png

# If optional GIFs were recorded, include them:
# git add assets/screenshots/demo_04_coach_animated.gif
# git add assets/screenshots/demo_02_skills_animated.gif

# If video walkthrough was recorded, include it:
# git add assets/demo_walkthrough.mp4

git commit -m "feat(demo): executive demo page — 8 sections, CIO-ready with EDC context and roadmap"
```
