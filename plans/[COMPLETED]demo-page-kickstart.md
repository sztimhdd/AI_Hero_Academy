# Kickstart: Executive Demo Page

Paste this prompt into a new Claude Code session to implement the executive demo page.

---

## Your Task

Rewrite `pages/00_Welcome.py` as an 8-section executive demo page for AI Hero Academy.

The full design spec — including section content, copy, CSS constant, and Python patterns — is in `plans/demo-page-plan.md`. Read it thoroughly before writing a single line of code.

**Only two things change:** `pages/00_Welcome.py` and new files added under `assets/screenshots/`.

---

## Read First

In this order:

1. `plans/demo-page-plan.md` — full spec, section content, DEMO_CSS constant, Python patterns
2. `pages/00_Welcome.py` — existing file; routing guard (lines 1–51) and registration form (lines 120–193) are copied verbatim into the new file
3. `utils/styles.py` — design system: `inject_global_css()` and CSS custom properties (`--cyan`, `--amber`, `--text`, `--bg-surface`, etc.)

---

## Pre-flight

```bash
# Confirm seeding script exists
ls scripts/reset_uat_user.py
```

Consult Streamlit SDK before using any layout API:

- `mcp__context7__resolve-library-id` → library: "streamlit"
- `mcp__context7__query-docs` → query: "st.tabs st.columns st.image layout"

---

## Branch Setup

```bash
git checkout -b feature/demo-page
mkdir -p assets/screenshots
```

---

## Task DP-1 — Capture App Screenshots

Start the server, seed each profile, navigate with Playwright, save each PNG.

```bash
bash run_uat.sh &
# Wait ~8s, then verify: curl -s -o /dev/null -w "%{http_code}" http://localhost:8501
```

| # | Seed command | Navigate to | Save as |
| --- | --- | --- | --- |
| 1 | `python scripts/reset_uat_user.py --role rm` | `localhost:8501` → auto-routes to Diagnostic | `assets/screenshots/demo_01_diagnostic.png` |
| 2 | `python scripts/reset_uat_user.py --role rm --diag` | `localhost:8501` → auto-routes to Skills Profile | `assets/screenshots/demo_02_skills_profile.png` |
| 3 | `python scripts/reset_uat_user.py --profile course-built` | Home → Module 1 → Reading sub-view | `assets/screenshots/demo_03_course_module.png` |
| 4 | (same session, no reseed) | Module 1 → Practice → type 1 response → wait for coach reply | `assets/screenshots/demo_04_ai_coach.png` |
| 5 | `python scripts/reset_uat_user.py --profile m1-done` | Home → Module 1 → Results sub-view | `assets/screenshots/demo_05_results.png` |

Verify all 5 files exist and are > 50 KB before proceeding:

```bash
ls -la assets/screenshots/demo_*.png
```

**Alternative (demo mode):** Use `localhost:8501?demo=true` and the persona selector. Persona 3b → screenshot 1; persona 3c → screenshots 2–5. Demo mode suppresses all DB writes.

---

## Task DP-2 — Rewrite `pages/00_Welcome.py`

### File structure

```
[Lines 1–51 from existing file — routing guard, VERBATIM]

DEMO_CSS constant                ← full CSS from plans/demo-page-plan.md
inject_global_css()
st.markdown(DEMO_CSS, unsafe_allow_html=True)

Section 1  — Hero
Section 2  — The Challenge (3 stat cards + EDC callout)
Section 3  — The Learning Loop (4-stage flow + path callout)
Section 4  — Inside the Platform (st.tabs, 5 tabs, GIF-over-PNG fallback)
Section 5  — What Makes It Different (4-column card grid)
Section 6  — The Skill Model (6-domain grid + mastery pills)
Section 7  — Get Started
    [Lines 120–193 from existing file — registration form, VERBATIM]
    + pilot note below form
Section 8  — What's Coming (st.expander, collapsed by default)
```

### Critical constraints

- Routing guard must be character-for-character identical to the original (lines 1–51)
- All colours via CSS custom properties only — no hex literals in inline `style=` attributes
- `st.tabs()` must NOT be nested inside `st.expander()`
- Page must make zero external API calls — loads in < 2s
- Section 4 must check for `.gif` before `.png` (see GIF-over-PNG pattern in plan)

### Where to find the implementation details

Everything you need is in `plans/demo-page-plan.md`:

- **Section headings + body copy** → Section Specifications
- **DEMO_CSS constant** → CSS Strategy section (full `<style>` block)
- **Python pattern for each section** → Implementation Patterns section
- **Screenshot captions** → Section 4 spec
- **Domain pills + mastery progression** → Section 6 spec

---

## Task DP-3 — Verify

```bash
# Reset to fresh state (no profile) so the demo page shows
python scripts/reset_uat_user.py

# Ensure server is running
bash run_uat.sh &

# Playwright: navigate and take a full-page screenshot
# browser_navigate → http://localhost:8501
# browser_take_screenshot → demo-page-check.png (full page)
# Scroll through all 8 sections — confirm nothing is broken

# Verify routing guard: returning user must NOT see the demo page
python scripts/reset_uat_user.py --role rm --diag
# Reload http://localhost:8501 — must redirect straight to Skills Profile
```

---

## Acceptance Checklist

- [ ] All 5 required PNGs exist in `assets/screenshots/` before deployment
- [ ] Demo page loads for a new user (no profile) and shows all 8 sections
- [ ] Returning user (any state) is immediately redirected — no demo page flash
- [ ] All 5 screenshot tabs display correctly (images load, captions appear)
- [ ] Where a GIF exists (`demo_02_skills_animated.gif` / `demo_04_coach_animated.gif`), it renders instead of the PNG
- [ ] Section 2 EDC callout renders below the 3 stat cards
- [ ] Section 5 renders 4 cards in a single row at 1440px (no wrapping)
- [ ] Section 6 mastery pills visible; "Practitioner" pill has amber border
- [ ] Section 8 expander is collapsed by default; expands to 4 roadmap cards in 2 columns
- [ ] Section 7 registration form creates a profile and routes to Diagnostic
- [ ] No hex literals in inline `style=` attributes — all colours use CSS custom properties
- [ ] Full-page Playwright screenshot looks correct at 1440px
- [ ] `bash run_uat.sh` passes all UAT scenarios without regression

---

## Commit

```bash
git add pages/00_Welcome.py assets/screenshots/demo_*.png
git commit -m "feat(demo): executive demo page — 8 sections, CIO-ready with EDC context and roadmap"
```

Then deploy:

```bash
bash scripts/sync_deploy.sh
```
