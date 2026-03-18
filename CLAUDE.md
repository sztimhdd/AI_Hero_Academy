# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment

**Python**: 3.11 via `.venv/`

### Install dependencies

```bash
.venv/Scripts/pip install -r requirements.txt
```

### Run locally (UAT / Playwright testing)

```bash
bash run_uat.sh
```

Sources `.env` (copy from `.env.example`, fill in `GEMINI_API_KEY`, `GCP_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`), starts Streamlit on port 8501 with `LOCAL_UAT=true`. The Playwright Chromium browser connects to `localhost:8501`.

To reset the test user's data between runs:

```bash
python scripts/reset_uat_user.py                          # full wipe → Welcome page
python scripts/reset_uat_user.py --role rm                # seed RM profile → Diagnostic
python scripts/reset_uat_user.py --role rm --diag         # + diagnostic + gap map → Skills Profile
python scripts/reset_uat_user.py --profile course-built   # RM + module 1 unlocked → Home (UAT Group C)
python scripts/reset_uat_user.py --profile m1-done        # RM + module 1 complete → Home (UAT-16)
python scripts/reset_uat_user.py --profile all-done       # RM + all 7 modules done → Home (UAT-15)
```

### Deploy to Cloud Run

Deployment is automated via GitHub Actions (`.github/workflows/deploy.yml`). Push to `main` → builds Docker image → pushes to Artifact Registry → deploys to Cloud Run service `ai-hero-academy`.

Required GitHub secrets: `GCP_SA_KEY` (service account JSON), `GEMINI_API_KEY`, `GCP_PROJECT_ID`.

---

## Project Overview

**AI Hero Academy** is an internal Streamlit app (GCP Cloud Run) that evaluates, trains, and benchmarks employees on AI skills through real-life, job-specific scenarios and AI coaching powered by Google Gemini API.

The app implements a four-stage learning loop: Diagnose → Map Gaps → Train → Score & Track. Three roles are fully generated and live: **Relationship Manager (RM)**, **Underwriter (UW)**, and **Analyst (AN)**. All three use the **6-domain hexagon model** (`responsible_ai`, `strategic_prompting`, `critical_eval`, `relationship_intel`, `data_decision`, `augmented_comm`) with 7 courses and 18 diagnostic items per role (3 per domain).

## Technology Stack

- **Frontend/App**: Streamlit (deployed on GCP Cloud Run)
- **AI models**: Google Gemini API (`gemini-2.0-flash`) via `google-genai` SDK
- **Persistence**: Google Cloud Firestore (GCP project `banded-totality-485901`)
- **Authentication**: `GCP_USER_EMAIL` env var (Cloud Run) or `DEV_USER_EMAIL` (local dev)
- **Language**: Python 3.11

## Remote Environment

| Resource | Value |
| --- | --- |
| GCP Project | `banded-totality-485901` |
| Cloud Run service | `ai-hero-academy` (region: `northamerica-northeast1`) |
| Firestore database | default (same GCP project) |
| Gemini model | `gemini-2.0-flash` |
| GitHub repo | `https://github.com/sztimhdd/AI_Hero_Academy` |

### Local GCP credentials

```bash
# One-time setup for local dev
gcloud auth application-default login
```

Or place service account key at `.gcp/banded-totality-485901-eb494951ebf7.json` and set `GOOGLE_APPLICATION_CREDENTIALS` in `.env`.

## Data Architecture

**Static content** — all served from `content/*.json` files bundled with the app (no database queries at runtime):

- `content/roles.json` — role definitions (rm, uw, an, mk)
- `content/domains.json` — skill domains with level descriptors; top-level keys are role-scoped (e.g. `rm_prompting`, `uw_prompting`)
- `content/diagnostic_items.json` — 72 items (18 per role × 4 roles); 3 per domain per role
- `content/courses.json` — 28 courses (7 per role × 4 roles); mapped to domains via `primary_domain`
- `content/reading_content.json` — reading material per course
- `content/reading_content_structured.json` — AI-extracted structured sub-fields (optional fallback)
- `content/practice_scenarios.json` — scenario text, 4 tasks, and coach system prompt per course
- `content/evaluation_items.json` — 4 questions per course (3 MCQ + 1 performance task) with scoring rubrics

Access content via `utils/content.py` typed getters. Never query Firestore for static content.

**Firestore collections** (top-level, all filtered by `user_email`):

- `user_profiles/{user_email}` — role, display_name, created_at
- `diagnostic_sessions/{session_id}` — responses, item_scores, domain_scores, overall_score
- `gap_maps/{gap_map_id}` — bullets, source_type, generated_at
- `training_progress/{user_email}_{course_id}` — reading/practice/evaluation completion, scores, lock status
- `coach_sessions/{session_id}` — full conversation transcript, turn count
- `ai_call_log/{log_id}` — every AI API call with latency, token counts, error status

## Application Architecture

The app is a multi-page Streamlit application. Pages map directly to user journey states:

| Page | Trigger condition |
| ---- | ----------------- |
| Welcome | No doc in Firestore `user_profiles/{email}` |
| Diagnostic | Profile exists, no completed diagnostic |
| Skills Profile | Diagnostic complete |
| Home | Course created; default landing for returning users |
| Course Module | User navigates into a module |

On every page load, the app reads `user_email` from `GCP_USER_EMAIL` (Cloud Run) or `DEV_USER_EMAIL` (local), queries Firestore `user_profiles` and `training_progress`, then routes to the appropriate page.

**Module sub-views** (within the Course Module page):

1. **Overview** — entry point; context-aware CTA based on sub-module completion state
2. **Reading** — static content rendered from `content.reading_content`; writes `reading_completed_at` on completion
3. **Practice** (AI Coach) — 4 sequential tasks; max 15 total coach turns; conversation is in-memory only (not persisted mid-session); writes `coach_sessions` + `practice_completed_at` on completion
4. **Evaluation** (Quiz) — 4 questions; triggers AI scoring + gap map update + module unlock on submission
5. **Results** — shows AI-generated coach note and score breakdown

## AI Call Patterns

There are four distinct AI call types:

1. **Diagnostic scoring** — batch call after question 12; scores all 12 responses against rubrics; use temperature 0.1
2. **Gap map generation** — called after diagnostic scoring and after each module evaluation; generates 3-6 personalized narrative bullets ordered by priority
3. **AI Coach responses** — called per user turn during practice; constrained by a per-course system prompt; temperature 0.4; must flag if user appears to input real client data
4. **Evaluation scoring** — same pattern as diagnostic scoring; temperature 0.1

All AI calls write to Firestore `ai_call_log` collection and display a graceful error message on failure without losing user progress.

## Module Sequencing Algorithm

After diagnostic, courses are ordered per user:

1. **Quick win first**: domain scoring 1.5–2.5, closest to 2.0
2. **Gaps next**: domains below 1.5, ascending (lowest first)
3. **Remaining**: domains not in above categories
4. **Strong last**: domains above 2.5

Courses are mapped to domains via `primary_domain`; Module 1 unlocks immediately, Modules 2–7 unlock sequentially.

## Scoring Rules

- **MCQ**: fixed score per answer choice (0–4 scale)
- **Prompt sandbox / micro-task / performance task**: AI-scored against a weighted rubric (criteria scored 0–1, total scaled to 0–4)
- **Domain score**: average of all scored items for that domain across diagnostic and completed evaluations (equal weight per item)
- **Overall score**: average of 4 domain scores
- **Level labels**: 0.0–0.4 Unaware, 0.5–1.4 Explorer, 1.5–2.4 Practitioner, 2.5–3.4 Proficient, 3.5–4.0 Champion

## Key Constraints

- **No partial saves during diagnostic or evaluation** — if user refreshes mid-assessment, they restart from question 1 (acceptable for a 5-minute assessment)
- **Practice conversation is in-memory only** — refresh loses the coach conversation; user restarts from Task 1
- **All queries filtered by `user_email`** — no user can access another user's data
- **Content uses only fictional data** — no real client names, financials, or non-public information anywhere in seeded content (use entities like "Northern Fabrication Ltd.", "Maple Industries Ltd.")
- **No admin UI in MVP** — content is updated by editing `content/*.json` and redeploying

## Content Architecture

Static app content lives in `content/*.json` (committed to the repo, loaded at startup by `utils/content.py`). Any content changes require editing the JSON files directly and redeploying the app.

## Out of Scope

Do not build toward: manager dashboards, admin UI, MLflow prompt versioning, SQL Warehouse analytics, materialized views, mobile layout, multilingual content, badges/HR integration, email notifications, or leaderboards.

**Note**: Multi-role support (UW) and the agent content generation pipeline are no longer out of scope — both are in progress.

## UI/UX Development Rules

**Always consult the latest Streamlit SDK documentation via Context7 before attempting any UI/UX fix.**

Use `mcp__context7__resolve-library-id` (library: "streamlit") then `mcp__context7__query-docs` to look up the current API for any Streamlit feature you are about to touch (layout, sidebar, navigation, theming, CSS injection, etc.). Do this before reading or modifying any code. This prevents wasted effort fighting internal `data-testid` selectors or CSS specificity battles that are already solved by the official SDK.

Example: hiding auto-generated sidebar navigation is done via `.streamlit/config.toml` (`showSidebarNavigation = false`), not via CSS.

---

## Project Verification Checklist

> General engineering standards (plan before acting, subagents, elegance, autonomy) are in `~/.claude/CLAUDE.md`. Below are the **project-specific** verification steps for "Verify before marking done":

- Run the app locally (`bash run_uat.sh`) and exercise the changed flow
- For data changes: check Firestore console (GCP project `banded-totality-485901`) to confirm writes
- For AI call changes: check Firestore `ai_call_log` collection for correct entries
- For scoring changes: run `pytest` and confirm expected scores
- Ask: would a senior engineer approve this diff?

---

## Lessons Learned

> Append new entries here after any correction or unexpected failure. Format: `date — what went wrong — rule to prevent recurrence.`

- **2026-02** — Attempted to query `mdlg_ai_shared.content.*` tables after they were retired; app errored at runtime. **Rule**: always use `utils/content.py` getters for static content; never query any database for static content.
- **2026-02** — UI/UX fixes fought internal `data-testid` CSS selectors that broke across Streamlit versions. **Rule**: always look up the current Streamlit API via Context7 before any UI change.
- **2026-03** — UW design doc (85KB) caused Stage 1 JSON parse failure in `generate_course_content.py` due to 19KB of embedded Copilot/SharePoint URLs that produced malformed LLM-generated JSON. **Rule**: always strip URLs from design docs before running the pipeline. Use `re.sub(r'\]\(https?://[^)]+\)', ']', text)` — strips the URL while keeping the display text. Target size is ~60–65KB.
- **2026-03** — Adding `max-width` to `.block-container` without `align-self` caused a large centering gap on wide displays. Root cause: `[data-testid="stMain"]` is a column-flex with `align-items: center`; a max-width cap creates a narrower child that the parent centers, producing a 430px+ gap between the sidebar and content. **Rule**: whenever setting `max-width` on `.block-container`, always pair it with `width: 100% !important` and `align-self: flex-start !important` to prevent centering.
- **2026-03** — Claude invoked `Skill({skill: "compact"})` which failed with a red dot because no "compact" skill file exists. **Rule**: `/compact`, `/clear`, and `/help` are built-in CLI commands — never invoke them via the `Skill` tool. Only use the `Skill` tool for skills explicitly listed in the available skills section of the system reminder.
