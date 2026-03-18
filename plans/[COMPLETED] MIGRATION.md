# Migration: Databricks App → GCP Cloud Run

## Migration Status

| Phase | Description | Status | Commit |
|-------|-------------|--------|--------|
| A | LLM Layer — Gemini replaces Databricks Foundation Models | ✅ COMPLETE | (merged into Phase B commit) |
| B | Data Layer — Firestore replaces Unity Catalog Delta tables | ✅ COMPLETE | `4a00b68` (2026-03-18) |
| C | Cloud Run Packaging — Dockerfile, Cloud Build | ✅ COMPLETE | `8830512` (2026-03-18) |
| D | GitHub Remote + Cleanup — remove Databricks artifacts | ✅ COMPLETE | (this session, 2026-03-18) |

---

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

### Phase A — LLM Layer ✅ COMPLETE

**Goal**: replace `utils/ai.py` so all LLM calls go through Gemini instead of Databricks.

Files changed:
- `utils/ai.py` — replaced `WorkspaceClient` + `ChatMessage` with `google-genai` SDK; Gemini `gemini-2.0-flash` as default model
- `requirements.txt` — removed `databricks-sdk`; added `google-genai>=1.0.0`
- `.env` — replaced `DATABRICKS_TOKEN` / `DATABRICKS_WAREHOUSE_ID` / `SERVING_ENDPOINT_NAME` with `GEMINI_API_KEY`

The `call_llm()` function signature and return type remain identical — all callers (`score_diagnostic`, `coach_response`, `generate_gap_map`, `score_evaluation`, `generate_module_coach_note`) unchanged.

`_log_call()` writes to Firestore `ai_call_log` collection (Phase B completes the Firestore setup).

**Completed**: `streamlit run app.py` works locally with `GEMINI_API_KEY` set; all LLM calls route through Gemini.

---

### Phase B — Data Layer ✅ COMPLETE (2026-03-18, commit `4a00b68`)

**Goal**: replace `utils/db.py` so all learner reads/writes go to Firestore instead of Databricks SQL.

Files changed:
- `utils/db.py` — complete rewrite; replaced `WorkspaceClient` + `statement_execution` with `google-cloud-firestore`; domain-specific functions replace `execute()` / `query_one()`; `load_dotenv` self-loading added so env vars work regardless of app start method; relative `GOOGLE_APPLICATION_CREDENTIALS` path resolved to absolute at runtime; all `order_by` removed from compound Firestore queries (sorted in Python to avoid composite index requirement)
- `utils/auth.py` — added `GCP_USER_EMAIL` fallback before `DATABRICKS_USER_EMAIL`
- `requirements.txt` — added `google-cloud-firestore>=2.16.0`
- `app.py` — replaced `UC_CATALOG` env var; uses `get_profile()`, `get_latest_diagnostic()`, `get_any_progress()` from new db API
- `pages/00_Welcome.py` — uses `create_profile()`, `get_profile()`, `get_latest_diagnostic()`, `get_any_progress()`
- `pages/01_Diagnostic.py` — uses `get_profile()`, `get_latest_diagnostic()`, `save_diagnostic()`, `save_gap_map()`
- `pages/02_Skills_Profile.py` — uses `get_all_diagnostics()`, `get_latest_gap_map()`, `get_all_progress()`, `get_any_progress()`
- `pages/03_Home.py` — uses `get_profile()`, `get_latest_diagnostic()`, `get_all_progress()`
- `pages/04_Course_Module.py` — uses `get_progress()`, `get_all_progress()`, `get_progress_by_seq()`, `save_coach_session()`, `update_progress()`, `unlock_progress()`, `get_latest_diagnostic()`, `save_gap_map()`
- `utils/demo.py` — rewritten to use domain functions; `_wipe_demo_user()` deletes Firestore docs by querying `user_email`; `ensure_demo_seeded()` replaces all `_raw_execute()` calls with `create_profile()`, `save_diagnostic()`, `save_gap_map()`, `create_progress()`, `update_progress()`
- `scripts/reset_uat_user.py` — rewritten to use Firestore batch-delete and domain create functions
- `.env` — added `GCP_PROJECT_ID=banded-totality-485901`, `GOOGLE_APPLICATION_CREDENTIALS=.gcp/banded-totality-485901-eb494951ebf7.json`; removed all Databricks variables

Firestore collection layout (flat top-level, mirrors former Delta schema):

```
user_profiles/{user_email}               → {role_id, display_name, created_at}
diagnostic_sessions/{session_id}         → {user_email, started_at, completed_at, responses, item_scores, domain_scores, overall_score}
gap_maps/{gap_map_id}                    → {user_email, source_type, source_id, bullets, generated_at}
training_progress/{user_email}_{course_id} → {user_email, course_id, module_sequence_order, is_locked, reading_completed_at, practice_completed_at, evaluation_completed_at, evaluation_score, domain_score_after}
coach_sessions/{session_id}              → {user_email, course_id, started_at, completed_at, turn_count, conversation_json}
ai_call_log/{log_id}                     → {user_email, call_type, model_endpoint, latency_ms, success, error_message, prompt_tokens, completion_tokens}
```

GCP project: `banded-totality-485901`. Authentication via service account key in `.gcp/`.

**Key implementation decisions**:
- All compound Firestore queries use single `where("user_email", "==", ...)` + Python-side sort/filter to avoid composite index requirements
- `load_dotenv()` at the top of `utils/db.py` ensures `.env` is loaded regardless of how Streamlit is started
- `GOOGLE_APPLICATION_CREDENTIALS` relative path is resolved to absolute in `_get_db()` at first call
- `escape()` kept as a no-op shim for backward compatibility

**Completed**: full app flow verified locally (Welcome → Diagnostic → Skills Profile → Home → Module) against real GCP Firestore project; HTTP 200 on port 8502; Firestore reads/writes confirmed.

---

### Phase C — Cloud Run Packaging ✅ COMPLETE (2026-03-18, commit `8830512`)

**Goal**: containerise the app and deploy to Cloud Run.

Files created:
- `Dockerfile` — Python 3.11-slim, install requirements, run Streamlit on port 8080
- `.dockerignore` — excludes `.gcp/`, `.env`, `.venv/`, `__pycache__/`, tests, docs

Deployment:

- `.github/workflows/deploy.yml` — builds Docker image, pushes to Artifact Registry (`northamerica-northeast1`), deploys to Cloud Run service `ai-hero-academy` (1 GiB, 0–3 instances)
- Cloud Run env vars: `GEMINI_API_KEY`, `GCP_PROJECT_ID`

Previously removed: `app.yml` (Databricks App config)

---

### Phase D — GitHub Remote + Cleanup ✅ COMPLETE (2026-03-18)

- GitHub remote: `https://github.com/sztimhdd/AI_Hero_Academy.git` ✅
- Deleted: `databricks.yml`, `app.yml`, `notebooks/`, `.databricksignore`
- Updated `CLAUDE.md` to reflect GCP stack
- Tag `v1.0.0-gcp` applied

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
2. **`utils/db.py` domain functions are the new stable API** — pages call `get_profile()`, `get_latest_diagnostic()`, etc. directly; `execute()` and `query_one()` are gone.
3. **`content/*.json` files are read-only** — `utils/content.py` getters are unchanged.
4. **Demo mode** (`utils/demo.py`) uses domain functions from `utils/db.py` — `_raw_execute()` is removed; demo seeding uses `create_profile()`, `save_diagnostic()`, etc.
5. **Never break the main flow on logging failures** — `_log_call()` must always be wrapped in try/except.
