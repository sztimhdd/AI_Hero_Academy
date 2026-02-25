# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment

**Python**: 3.11 via `.venv/` (created by the Databricks VS Code extension)

### Install dependencies

```bash
.venv/Scripts/pip install -r requirements.txt
```

### Run locally (UAT / Playwright testing)

```bash
bash run_uat.sh
```

Sources `.env` (copy from `.env.example`, add `DATABRICKS_TOKEN`), starts Streamlit on port 8501 with `LOCAL_UAT=true`. The Playwright Chromium browser only connects to `localhost:8501` — it has no direct Databricks dependency; all auth is handled by the Python process.

To reset the test user's data between runs:

```bash
python scripts/reset_uat_user.py
```

### Sync + deploy to remote (one command)

```bash
bash scripts/sync_deploy.sh
```

Syncs local files to the Databricks workspace and redeploys the app using the `dev` CLI profile. This is the standard post-commit deploy step. The `/commit` skill runs this automatically.

**Manual equivalents** (if running CLI directly from Git Bash, prefix with `MSYS_NO_PATHCONV=1`):

```bash
MSYS_NO_PATHCONV=1 databricks sync . /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp --profile dev
MSYS_NO_PATHCONV=1 databricks apps deploy my-ai-hero-academy-mvp --source-code-path /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp --profile dev
```

### Databricks CLI profile

The `dev` profile (`~/.databrickscfg`) uses OAuth via `auth_type = databricks-cli`. It is pre-configured for `https://adb-2717931942638877.17.azuredatabricks.net`. If the token expires, refresh with:

```bash
databricks auth login --profile dev
```

---

## Project Overview

**AI Hero Academy** is an internal Databricks App that evaluates, trains, and benchmarks employees on AI skills through real-life, job-specific scenarios and AI coaching powered by Mosaic AI Foundation Models.

The MVP targets a single role — **Relationship Manager (RM)** — and implements a four-stage learning loop: Diagnose → Map Gaps → Train → Score & Track.

## Technology Stack

- **Frontend/App**: Streamlit (hosted as a Databricks App)
- **AI models**: Databricks Foundation Model APIs via serving endpoints (OpenAI-compatible, accessed through `databricks-sdk`)
- **Persistence**: Delta tables in Unity Catalog (`mdlg_ai` catalog)
- **Authentication**: Databricks workspace SSO (no custom auth layer)
- **Language**: Python 3.11

## Remote Environment

| Resource | Value |
| --- | --- |
| Workspace | `https://adb-2717931942638877.17.azuredatabricks.net` |
| Unity Catalog | `mdlg_ai_shared` |
| SQL Warehouse | `eaa098820703bf5f` (Serverless Starter Warehouse) |
| App serving endpoint | `databricks-claude-sonnet-4-5` |
| App name | `my-ai-hero-academy-mvp` |
| Workspace source path | `/Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp` |

Other available Foundation Model endpoints (all support `llm/v1/chat`): `databricks-claude-sonnet-4-5`, `databricks-claude-opus-4-5`, `databricks-claude-haiku-4-5`.

## Unity Catalog Schema Layout

All tables live under `mdlg_ai_shared`. The three schemas for this app are:

- `mdlg_ai_shared.content` — read-only; pre-seeded static content (now served from `content/*.json` in the app bundle — no SQL queries needed)
- `mdlg_ai_shared.learner` — read-write; per-user data, always filtered by `user_email`
- `mdlg_ai_shared.system` — write by app, read by admins; AI call logs

### Accessing Delta tables from app code

```python
from databricks.sdk import WorkspaceClient
import os

w = WorkspaceClient()  # auto-authenticates in both local VS Code and deployed App contexts
result = w.statement_execution.execute_statement(
    warehouse_id=os.environ["DATABRICKS_WAREHOUSE_ID"],
    statement="SELECT * FROM mdlg_ai_shared.learner.user_profiles WHERE user_email = :p1",
    wait_timeout="30s",
)
```

### Calling AI serving endpoints

```python
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

response = w.serving_endpoints.query(
    name=os.environ["SERVING_ENDPOINT_NAME"],
    messages=[ChatMessage(role=ChatMessageRole.USER, content="Hello")],
)
```

## Data Architecture

Two Unity Catalog schemas:

**`content` schema** (read-only for app, pre-seeded via notebooks):

- `roles` — role definitions (RM only in MVP)
- `domains` — 4 skill domains with level descriptors
- `diagnostic_items` — 12 questions (3 per domain; types: MCQ, prompt_sandbox, micro_task)
- `courses` — 5 training courses mapped to RM use cases
- `reading_content` — reading material per course
- `practice_scenarios` — scenario text, 4 tasks, and coach system prompt per course
- `evaluation_items` — 4 questions per course (3 MCQ + 1 performance task) with scoring rubrics

**`learner` schema** (read-write, all queries filtered by `user_email`):

- `user_profiles` — one row per user; stores role, display_name, created_at
- `diagnostic_sessions` — each diagnostic attempt; stores all 12 responses and item scores
- `gap_maps` — AI-generated narrative bullets per session; references diagnostic or evaluation
- `training_progress` — one row per user per course; tracks reading/practice/evaluation completion, scores, module sequence order, lock status
- `coach_sessions` — full conversation transcript per practice session; stores turn count

**`system` schema** (app writes, admins read):

- `ai_call_log` — every AI API call with prompt, response, latency, and error status

## Application Architecture

The app is a multi-page Streamlit application. Pages map directly to user journey states:

| Page | Trigger condition |
| ---- | ----------------- |
| Welcome | No row in `learner.user_profiles` |
| Diagnostic | Profile exists, no completed diagnostic |
| Skills Profile | Diagnostic complete |
| Home | Course created; default landing for returning users |
| Course Module | User navigates into a module |

On every page load, the app reads `user_email` from Databricks SSO context, queries `learner.user_profiles` and `learner.training_progress`, then routes to the appropriate page.

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

All AI calls must write to `system.ai_call_log` and display a graceful error message on failure without losing user progress.

## Module Sequencing Algorithm

After diagnostic, courses are ordered per user:

1. **Quick win first**: domain scoring 1.5–2.5, closest to 2.0
2. **Gaps next**: domains below 1.5, ascending (lowest first)
3. **Remaining**: domains not in above categories
4. **Strong last**: domains above 2.5

Courses are mapped to domains via `primary_domain`; Module 1 unlocks immediately, Modules 2–5 unlock sequentially.

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
- **No admin UI in MVP** — content is seeded and updated via notebooks

## Content Seeding

All `content` schema tables are populated via Databricks notebooks (not the app). The app service principal has read-only access to `content`. Any content changes require running the seeding notebook.

## Out of Scope for MVP

Do not build toward: manager dashboards, multi-role support, admin UI, agent pipelines for content generation, MLflow prompt versioning, SQL Warehouse analytics, materialized views, mobile layout, multilingual content, badges/HR integration, email notifications, or leaderboards.

## UI/UX Development Rules

**Always consult the latest Streamlit SDK documentation via Context7 before attempting any UI/UX fix.**

Use `mcp__context7__resolve-library-id` (library: "streamlit") then `mcp__context7__query-docs` to look up the current API for any Streamlit feature you are about to touch (layout, sidebar, navigation, theming, CSS injection, etc.). Do this before reading or modifying any code. This prevents wasted effort fighting internal `data-testid` selectors or CSS specificity battles that are already solved by the official SDK.

Example: hiding auto-generated sidebar navigation is done via `.streamlit/config.toml` (`showSidebarNavigation = false`), not via CSS.
