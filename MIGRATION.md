# Migration: Databricks App → GCP Cloud Run

## Target Architecture

| Layer | From | To |
|-------|------|----|
| Deployment | Databricks App (`app.yml`) | GCP Cloud Run (Docker container) |
| LLM API | Databricks Foundation Model endpoints (`databricks-sdk`) | Google Gemini API (`google-genai`) |
| Learner data store | Unity Catalog Delta tables (`mdlg_ai_shared.learner.*`) | Firestore (GCP NoSQL) |
| Authentication | Databricks SSO (`DATABRICKS_USER_EMAIL` env) | Google Identity-Aware Proxy (IAP) or manual email env |
| AI call logging | Unity Catalog `system.ai_call_log` Delta table | Firestore `ai_call_log` collection |
| Static content | `content/*.json` (unchanged) | `content/*.json` (unchanged — no migration needed) |

---

## What Does NOT Change

- All `content/*.json` files — roles, domains, courses, diagnostics, reading, practice scenarios, evaluation items
- All `pages/*.py` page logic (except auth header calls)
- All `utils/scoring.py`, `utils/sequencing.py`, `utils/content.py`, `utils/styles.py`, `utils/demo.py`
- Streamlit as the frontend framework
- The scoring algorithm and domain model
- The 4-stage learning loop (Diagnose → Map Gaps → Train → Score)

---

## Phased Migration Plan

### Phase A — LLM Layer (do first, testable locally)

**Goal**: replace `utils/ai.py` so all LLM calls go through Gemini instead of Databricks.

Files to change:
- `utils/ai.py` — replace `WorkspaceClient` + `ChatMessage` with `google-genai` SDK
- `requirements.txt` — remove `databricks-sdk`; add `google-genai`
- `.env.example` — replace `DATABRICKS_TOKEN` / `DATABRICKS_WAREHOUSE_ID` / `SERVING_ENDPOINT_NAME` with `GEMINI_API_KEY`

Gemini model to use: `gemini-2.0-flash` (fast, cheap, production-grade).

The `call_llm()` function signature and return type must remain identical — all callers (`score_diagnostic`, `coach_response`, `generate_gap_map`, `score_evaluation`, `generate_module_coach_note`) must not need changes.

For `_log_call()`: in Phase A, write to Firestore `ai_call_log` collection instead of Delta SQL. If Firestore is not yet set up, write to a local JSON file as a temporary fallback (never break the main flow — match the existing try/except pattern).

**Done when**: `streamlit run app.py` works locally with `GEMINI_API_KEY` set; all LLM calls succeed.

---

### Phase B — Data Layer (Firestore replaces Delta tables)

**Goal**: replace `utils/db.py` so all learner reads/writes go to Firestore instead of Databricks SQL.

Files to change:
- `utils/db.py` — replace `WorkspaceClient` + `statement_execution` with `google-cloud-firestore`
- `utils/auth.py` — replace `DATABRICKS_USER_EMAIL` with `GCP_USER_EMAIL` (or Cloud Run IAP header `X-Goog-Authenticated-User-Email`)
- `requirements.txt` — add `google-cloud-firestore`
- `app.py` — replace `UC_CATALOG` env var with nothing (Firestore collection paths are hardcoded by schema name)

Firestore collection layout (mirrors Delta schema exactly):

```
learner/
  user_profiles/{user_email}           → {role_id, display_name, created_at}
  diagnostic_sessions/{session_id}     → {user_email, completed_at, responses, item_scores, domain_scores, overall_score}
  gap_maps/{gap_map_id}                → {user_email, session_id, source_type, bullets, created_at}
  training_progress/{user_email}_{course_id} → {user_email, course_id, ...all progress fields}
  coach_sessions/{session_id}          → {user_email, course_id, transcript, turn_count, created_at}

system/
  ai_call_log/{log_id}                 → {user_email, call_type, model_endpoint, latency_ms, success, ...}
```

The `execute()` and `query_one()` function signatures must remain identical where used by pages — or pages must be updated consistently.

**Done when**: full app flow works locally (Welcome → Diagnostic → Skills Profile → Home → Module) against Firestore emulator or real Firestore project.

---

### Phase C — Cloud Run Packaging

**Goal**: containerise the app and deploy to Cloud Run.

Files to create:
- `Dockerfile` — Python 3.11-slim, install requirements, run Streamlit on port 8080
- `.dockerignore` — exclude `.venv/`, `__pycache__/`, `.env`, `*.pyc`
- `cloudbuild.yaml` (optional) — for automated GCP deployment

Files to remove:
- `app.yml` (Databricks App config — no longer needed)
- `databricks.yml` (bundle config — no longer needed)

Environment variables for Cloud Run:
- `GEMINI_API_KEY`
- `GCP_PROJECT_ID` (for Firestore)
- `GCP_USER_EMAIL` (or rely on IAP header — TBD)

**Done when**: `docker build` succeeds locally; `docker run -p 8501:8080` serves the app; `gcloud run deploy` succeeds.

---

### Phase D — GitHub Remote + Cleanup

- Point repo remote to new GitHub repo
- Delete Databricks-specific files: `databricks.yml`, `app.yml`, `notebooks/`, `.databricks/`
- Update `CLAUDE.md` to reflect GCP stack
- Tag `v1.0.0-gcp`

---

## TODO Markers (leave in code during migration, remove at Phase D)

```python
# TODO: DATABRICKS_REMOVED — this block replaced by Firestore/Gemini equivalent
# TODO: AUTH_GCP — confirm IAP header injection in Cloud Run
# TODO: CLOUD_RUN — test this path in container (env var may differ)
```

---

## Key Constraints

1. **`utils/ai.py` `call_llm()` signature is frozen** — `(messages, temperature, user_email, call_type) → str`. All callers depend on it.
2. **`utils/db.py` `query_one()` and `execute()` signatures are frozen** — pages call these directly.
3. **`content/*.json` files are read-only** — `utils/content.py` getters are unchanged.
4. **Demo mode** (`utils/demo.py`) depends on `utils/db.py` `_raw_execute()` — must be preserved or re-implemented alongside the db layer.
5. **Never break the main flow on logging failures** — `_log_call()` must always be wrapped in try/except.
