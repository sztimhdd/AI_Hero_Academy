# Technical Design Document (TDD)
## AI Hero Academy MVP

**Version**: 2.0
**Date**: February 2026 (GCP Migration)
**Status**: In Development

---

## 1. Overview

AI Hero Academy is a Streamlit-based application hosted on GCP Cloud Run that delivers personalized AI skills training to employees. It implements a four-stage learning loop: **Diagnose → Map Gaps → Train → Score & Track**.

The MVP covers the Relationship Manager (RM) role. The Underwriter (UW) role content is fully generated and in-app — welcome page wiring is the remaining step before UW users can onboard. Each role has 12 diagnostic questions across 4 skill domains and 5 training courses. All AI scoring, coaching, and gap analysis is powered by the **Google Gemini API** (`google-genai` SDK). All learner state is persisted in **Google Cloud Firestore** (NoSQL document store) under the project `banded-totality-485901`. Static content (courses, diagnostic items, reading, scenarios, evaluations) is served from JSON files bundled with the app — no database queries needed for content.

---

## 2. Architecture

### 2.1 Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Frontend** | Streamlit (multi-page) | Hosted on GCP Cloud Run (port 8080) |
| **Database** | Google Cloud Firestore | NoSQL document store; `google-cloud-firestore` SDK; project `banded-totality-485901` |
| **AI** | Google Gemini API | `google-genai` SDK (GA since May 2025); `GOOGLE_API_KEY` env var |
| **State** | Firestore collections | User profiles, learner subcollections, `ai_call_log` top-level collection |
| **Auth** | `USER_EMAIL` env var | Set by Cloud Run env for prod; `.env` file for local dev. Future: Firebase Auth |
| **Hosting** | GCP Cloud Run | Containerized; auto-scaling; `min-instances=1` to preserve Streamlit session state |
| **CI/CD** | GitHub Actions + `gcloud` | `google-github-actions/deploy-cloudrun@v2` action |
| **Secrets** | GCP Secret Manager | `GOOGLE_API_KEY` stored as secret; exposed to Cloud Run as env var at instance start |

### 2.2 Component Diagram

```
┌────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│  (Welcome / Diagnostic / Skills Profile / Home / Module)   │
└──────────────────────┬─────────────────────────────────────┘
                       │ st.session_state (in-memory)
        ┌──────────────┼───────────────────┐
        │              │                   │
 ┌──────▼──────┐ ┌──────▼──────────┐ ┌────▼──────────────┐
 │ utils/db.py  │ │  utils/ai.py    │ │ utils/content.py  │
 │ SQL via SDK  │ │ serving_endpts  │ │ JSON file loader  │
 └──────┬──────┘ └──────┬──────────┘ └────┬──────────────┘
        │               │                  │
 ┌──────▼───────────────▼──┐    ┌──────────▼────────────┐
 │  Unity Catalog           │    │  content/*.json       │
 │  mdlg_ai_shared          │    │  (bundled with app)   │
 │  ├─ learner.* (rw)       │    │  roles, domains,      │
 │  └─ system.*  (wo)       │    │  courses, diagnostic  │
 └──────────────────────────┘    │  items, reading,      │
                                 │  scenarios, eval items│
                                 └───────────────────────┘
```

### 2.3 Gemini Model Endpoints

All calls use the `google-genai` Python SDK authenticated via `GOOGLE_API_KEY`. Model is selected based on call type.

| Model | Use Case | Temperature |
|-------|----------|-------------|
| `gemini-3.1-pro-preview` | **Default** — diagnostic scoring, gap map generation, evaluation scoring, module coach note | 0.1 (scoring) / 0.4 (generation) |
| `gemini-3-flash-preview` | AI coach responses during practice (low-latency) | 0.4 |

> **SDK Note:** Use `google-genai` (unified GA SDK, May 2025). The older `google-generativeai` package is deprecated as of November 2025. For structured JSON output, always set `response_mime_type="application/json"` and provide a `response_schema`.

---

## 3. Data Schema

### 3.1 Design Principles

- **Document-oriented over relational**: Firestore stores structured data as native Python dicts (not JSON strings). Options, rubrics, and responses are stored as native types and serialized only when needed.
- **`user_email` as identity key**: `user_email` from the `USER_EMAIL` env var is used as the document path key in `users/{email}` and as a filter in all learner queries. No UUID layer needed for MVP.
- **Subcollections for user data**: User-owned data lives in subcollections under `users/{email}/` for natural hierarchy and query efficiency. `ai_call_log` is a top-level collection (operational, not user-owned).
- **UUID document IDs**: All subcollection documents use `uuid4()` IDs to avoid Firestore hotspotting on write-heavy paths.
- **Content from JSON files**: All static content is bundled as `content/*.json` and loaded at startup by `utils/content.py`. No Firestore queries needed for content.

### 3.2 Content Schema

> **Architecture note:** All content is served from `content/*.json` files bundled with the app. No database queries are needed for content. The data shapes below document the JSON structure loaded by `utils/content.py`.

All content that was previously in `content.*` Delta tables is now served from `content/*.json` files.

#### `content.roles`
```sql
role_id       STRING NOT NULL PRIMARY KEY,
title         STRING NOT NULL,
description   STRING,
department    STRING
```

#### `content.domains`
```sql
domain_id           STRING NOT NULL PRIMARY KEY,
role_id             STRING NOT NULL,
title               STRING NOT NULL,
description         STRING,
level_0_label       STRING,
level_0_descriptor  STRING,
level_1_label       STRING,
level_1_descriptor  STRING,
level_2_label       STRING,
level_2_descriptor  STRING,
level_3_label       STRING,
level_3_descriptor  STRING,
level_4_label       STRING,
level_4_descriptor  STRING
```

The four domains seeded for the RM role: `prompting`, `verification`, `data_safety`, `tool_fluency`.

#### `content.diagnostic_items`
```sql
item_id         STRING NOT NULL PRIMARY KEY,
domain_id       STRING NOT NULL,
item_type       STRING NOT NULL,   -- 'mcq' | 'prompt_sandbox' | 'micro_task'
question_text   STRING NOT NULL,
scenario_text   STRING,
options         STRING,            -- JSON: [{"label":"A","text":"..."},...] for MCQ
correct_option  STRING,            -- label of correct MCQ option (e.g. "A")
scoring_rubric  STRING,            -- JSON: {"criterion_name": max_points, ...}
display_order   INT
```

**MCQ options format**: `[{"label":"A","text":"..."},{"label":"B","text":"..."},{"label":"C","text":"..."},{"label":"D","text":"..."}]`

**Rubric format (open-ended)**: `{"context_present":1,"role_present":1,"action_specific":1,"format_specified":1}` (each criterion max 1 point; total = 0–4 domain scale)

**MCQ rubric format**: `{"correct":4,"incorrect":0}`

#### `content.courses`
```sql
course_id        STRING NOT NULL PRIMARY KEY,
role_id          STRING NOT NULL,
primary_domain   STRING NOT NULL,
title            STRING NOT NULL,
tagline          STRING,
description      STRING,
real_use_case    STRING,   -- source use case(s) from EDC use case library
sequence_order   INT
```

The 5 RM courses:

| `course_id` | `primary_domain` | `sequence_order` | Title |
|-------------|-----------------|-----------------|-------|
| `rm_c1_prompting` | `prompting` | 1 | Brief Like a Pro |
| `rm_c2_verification` | `verification` | 2 | Recap, Review, Then Log |
| `rm_c3_data_safety` | `data_safety` | 3 | The C3 Line |
| `rm_c4_tool_fluency` | `tool_fluency` | 4 | Your Monday Morning Copilot Reset |
| `rm_c5_capstone` | `prompting` | 5 | Win-Back and Portfolio Intelligence |

#### `content.reading_content`
```sql
content_id    STRING NOT NULL PRIMARY KEY,
course_id     STRING NOT NULL,
concept_text  STRING NOT NULL,   -- core concept explanation (2-4 paragraphs)
good_example  STRING NOT NULL,   -- annotated positive example
anti_pattern  STRING NOT NULL,   -- annotated negative example with explanation
takeaway      STRING NOT NULL    -- one-sentence practical rule
```

One row per course (1:1 with `courses`).

#### `content.practice_scenarios`
```sql
scenario_id          STRING NOT NULL PRIMARY KEY,
course_id            STRING NOT NULL,
scenario_text        STRING NOT NULL,   -- scene-setting context given to learner
task_1_text          STRING NOT NULL,
task_2_text          STRING NOT NULL,
task_3_text          STRING NOT NULL,
task_4_text          STRING NOT NULL,
coach_system_prompt  STRING NOT NULL    -- system prompt for the AI coach for this course
```

One row per course (1:1 with `courses`). Max turns per task (3) and total max turns (15) are constants in app code, not stored in the table.

#### `content.evaluation_items`
```sql
item_id        STRING NOT NULL PRIMARY KEY,
course_id      STRING NOT NULL,
item_type      STRING NOT NULL,   -- 'mcq' | 'performance_task'
sequence       INT NOT NULL,      -- 1-3 = MCQ, 4 = performance_task
question_text  STRING NOT NULL,
scenario_text  STRING,            -- additional context for performance tasks
options        STRING,            -- JSON array (MCQ only)
correct_option STRING,            -- label of correct MCQ answer
explanation    STRING,            -- explanation of correct MCQ answer
scoring_rubric STRING NOT NULL    -- JSON: criteria -> max_points
```

Four rows per course (3 MCQ + 1 performance task). Total: 20 rows across all 5 courses.

### 3.3 Learner Schema (Firestore)

All learner data is stored in Firestore under `users/{user_email}/` subcollections. Every read is scoped to the authenticated user's email. The `google-cloud-firestore` Admin SDK is used server-side.

#### Collection: `users/{user_email}` (document)
```python
{
    "user_email":   str,   # document ID / identity key
    "display_name": str,   # optional
    "role_id":      str,   # e.g. "rm"
    "created_at":   datetime
}
```

#### Subcollection: `users/{user_email}/diagnostic_sessions/{session_id}`
```python
{
    "session_id":    str,   # uuid4()
    "user_email":    str,
    "started_at":    datetime,
    "completed_at":  datetime | None,
    "responses":     dict,  # {"item_id": "response_text", ...}
    "item_scores":   dict,  # {"item_id": score_float, ...}
    "domain_scores": dict,  # {"domain_id": score_float, ...}
    "overall_score": float | None
}
```
Multiple documents per user (retakes). App always reads most recent completed (`ORDER BY completed_at DESC LIMIT 1`).

#### Subcollection: `users/{user_email}/gap_maps/{gap_map_id}`
```python
{
    "gap_map_id":   str,   # uuid4()
    "user_email":   str,
    "source_type":  str,   # 'diagnostic' | 'evaluation'
    "source_id":    str,   # session_id or progress_id
    "bullets":      list,  # [{"priority": 1, "domain_id": "...", "bullet": "..."}, ...]
    "generated_at": datetime
}
```
Inserted after each diagnostic completion and each evaluation completion. App always shows the most recent.

#### Subcollection: `users/{user_email}/training_progress/{progress_id}`
```python
{
    "progress_id":             str,   # uuid4()
    "user_email":              str,
    "course_id":               str,
    "module_sequence_order":   int,   # 1-5; personalized per user
    "is_locked":               bool,  # True by default; Module 1 unlocked immediately
    "reading_completed_at":    datetime | None,
    "practice_completed_at":   datetime | None,
    "evaluation_score":        float | None,
    "evaluation_completed_at": datetime | None,
    "domain_score_after":      float | None  # domain score after this module's evaluation
}
```
Five documents created per user when they click "Build My Training Course". Module 1 is immediately unlocked (`is_locked = False`). Modules 2–5 are unlocked sequentially.

**Lock state derivation**: A module is complete when `evaluation_completed_at is not None`. Reading is complete when `reading_completed_at is not None`.

#### Subcollection: `users/{user_email}/coach_sessions/{session_id}`
```python
{
    "session_id":       str,   # uuid4()
    "user_email":       str,
    "course_id":        str,
    "started_at":       datetime,
    "completed_at":     datetime | None,
    "turn_count":       int,
    "conversation_json": list  # [{"role": "user"|"model", "content": "..."}, ...]
}
```
Written when the user clicks "Complete Practice". `conversation_json` uses the Gemini content format (`role: "user"` / `role: "model"`).

### 3.4 System Schema (Firestore)

#### Top-level collection: `ai_call_log/{log_id}`
```python
{
    "log_id":            str,   # uuid4()
    "user_email":        str | None,
    "call_type":         str,   # 'diagnostic_scoring' | 'gap_map' | 'coach_response' | 'evaluation_scoring'
    "model_name":        str,   # e.g. 'gemini-3.1-pro-preview'
    "prompt_tokens":     int | None,
    "completion_tokens": int | None,
    "latency_ms":        int | None,
    "success":           bool,
    "error_message":     str | None,
    "called_at":         datetime
}
```

Every Gemini API call writes one document. Used for monitoring, debugging, and token cost tracking. Not user-scoped (top-level collection, not a subcollection).

---

## 4. Content Architecture

> **Architecture change (Feb 2026):** All static content was migrated from Delta tables to JSON files bundled with the app. The `content.*` Delta schema is retired. `notebooks/01_seed_roles_domains.py`, `02_seed_courses.py`, and `03_seed_diagnostic_items.py` are no longer used.

### 4.1 JSON File Layout

All content lives in `content/` at the project root and is loaded by `utils/content.py` at module import time (once per container process).

| File | Key structure | Counts |
|------|---------------|--------|
| `content/roles.json` | `{role_id: {...}}` | 2 roles (rm, uw) |
| `content/domains.json` | `{rm_prompting: {...}, uw_prompting: {...}, ...}` | 8 entries (4 per role); role-scoped top-level keys |
| `content/diagnostic_items.json` | `[{item_id, role_id, domain_id, ...}]` | 24 items (12 RM + 12 UW); ordered by `display_order` |
| `content/courses.json` | `{course_id: {...}}` | 10 courses (5 RM + 5 UW); keyed by `course_id` |
| `content/reading_content.json` | `{course_id: {...}}` | 10 entries (1 per course) |
| `content/practice_scenarios.json` | `{course_id: {...}}` | 10 entries; includes `task_1_text`–`task_4_text` + `coach_system_prompt` |
| `content/evaluation_items.json` | `{course_id: [{...}]}` | 10 × 4 = 40 items |

**`domains.json` key format**: top-level keys are role-scoped (`rm_prompting`, `uw_prompting`, etc.); each entry has a `domain_id` field with the flat key (`prompting`). `utils/content.py` exposes `get_domain(domain_id, role_id)` and `get_domain_descriptions(role_id)` that filter by `role_id` field value.

### 4.2 Content Loader (`utils/content.py`)

```python
# Module-level constants — loaded once at startup
ROLES: dict           # {role_id: {...}}
DOMAINS: dict         # role-scoped keys; use get_domain()/get_domain_descriptions()
DIAGNOSTIC_ITEMS: list  # all items; filter by role_id via get_diagnostic_items(role_id)
COURSES: dict         # {course_id: {...}}
READING: dict         # {course_id: {...}}
SCENARIOS: dict       # {course_id: {...}}
EVAL_ITEMS: dict      # {course_id: [{...}, ...]}
DOMAIN_DESCRIPTIONS: dict  # {domain_id: description} for default role (rm)

# Typed getters
def get_role(role_id: str) -> dict
def get_domain(domain_id: str, role_id: str = "rm") -> dict
def get_domain_descriptions(role_id: str = "rm") -> dict[str, str]
def get_diagnostic_items(role_id: str = "rm") -> list[dict]
def get_course(course_id: str) -> dict
def get_reading(course_id: str) -> dict
def get_scenario(course_id: str) -> dict
def get_eval_items(course_id: str) -> list[dict]
```

### 4.3 Content Generation Pipeline

UW content (and future role content) is generated by `scripts/generate_course_content.py` — an 8-stage multi-agent LLM pipeline that converts a Course Design Brief markdown document into all content JSON files. The pipeline does not require running notebooks or writing to Delta.

### 4.4 Remaining Seeding (Firestore)

Firestore auto-creates collections and documents on first write — no DDL or schema creation notebooks are needed. `utils/db.py` initialises the Firestore client on first call. All learner documents are created by the app at runtime (welcome page, diagnostic completion, course creation, etc.).

### 4.5 Verification (post-startup)

After deploying the app, verify content loaded correctly by checking:

```python
from utils.content import DIAGNOSTIC_ITEMS, COURSES, EVAL_ITEMS, ROLES
assert len(ROLES) == 2                             # rm + uw
assert len(DIAGNOSTIC_ITEMS) == 24                 # 12 RM + 12 UW
assert len(COURSES) == 10                          # 5 RM + 5 UW
assert len(EVAL_ITEMS["rm_c1_prompting"]) == 4     # 4 items per course
```

---

## 5. Application Architecture

### 5.1 File Structure

```
app.py                        # entry point; handles routing based on user state
Dockerfile                    # Cloud Run container (python:3.11-slim-bookworm; port 8080)
.env.example                  # env var template for local dev
pages/
  00_Welcome.py               # new user onboarding + role selection
  01_Diagnostic.py            # 12-question diagnostic assessment (multi-role)
  02_Skills_Profile.py        # domain scores, gap map, assessment history
  03_Home.py                  # course progress dashboard
  04_Course_Module.py         # reading / practice / evaluation sub-views
utils/
  db.py                       # Firestore helper; Admin SDK; execute/query_one/escape API
  ai.py                       # Gemini API calls via google-genai; writes to ai_call_log
  auth.py                     # extracts user_email from USER_EMAIL env var
  content.py                  # JSON file loader; typed getters for all content
  scoring.py                  # MCQ scoring; rubric parsing; domain score calculation
  sequencing.py               # module sequence algorithm
  styles.py                   # inject_global_css(); section_header()
content/
  roles.json                  # {role_id: {...}} — rm + uw
  domains.json                # role-scoped keys (rm_prompting, uw_prompting, ...)
  diagnostic_items.json       # list of 24 items (12 RM + 12 UW)
  courses.json                # {course_id: {...}} — 10 courses
  reading_content.json        # {course_id: {...}} — 10 entries
  practice_scenarios.json     # {course_id: {...}} — 10 entries
  evaluation_items.json       # {course_id: [{...}]} — 40 items
scripts/
  generate_course_content.py  # multi-agent LLM pipeline for new role content
  reset_uat_user.py           # clears UAT test user data for re-testing
.github/
  workflows/
    deploy.yml                # GitHub Actions: build + push to Artifact Registry + deploy to Cloud Run
requirements.txt              # streamlit, google-genai, google-cloud-firestore, plotly, tenacity, ...
```

### 5.2 Auth: Extracting `user_email`

On GCP Cloud Run, the authenticated user's email is provided via the `USER_EMAIL` environment variable. For local development, set `USER_EMAIL` in a `.env` file:

```python
# utils/auth.py
import os

def get_user_email() -> str:
    email = os.environ.get("USER_EMAIL")
    if not email:
        raise RuntimeError(
            "USER_EMAIL environment variable is not set. "
            "For local dev, add USER_EMAIL=your@email.com to your .env file."
        )
    return email
```

Never use hardcoded emails. Do not prompt users to type their email.

### 5.3 Router Logic (`app.py`)

On every page load, the app reads user state from Firestore and routes:

```python
import streamlit as st
from utils.auth import get_user_email
from utils.db import query_one

def get_user_state(user_email: str) -> str:
    profile = query_one(
        "SELECT role_id FROM users WHERE user_email = ?",
        [user_email]
    )
    if not profile:
        return "new_user"

    session = query_one(
        "SELECT session_id FROM diagnostic_sessions "
        "WHERE user_email = ? AND completed_at IS NOT NULL "
        "ORDER BY completed_at DESC LIMIT 1",
        [user_email]
    )
    if not session:
        return "needs_diagnostic"

    progress = query_one(
        "SELECT progress_id FROM training_progress "
        "WHERE user_email = ? LIMIT 1",
        [user_email]
    )
    if not progress:
        return "needs_course"

    return "in_training"

user_email = get_user_email()
state = get_user_state(user_email)
st.session_state["user_email"] = user_email
st.session_state["user_state"] = state

PAGE_MAP = {
    "new_user":        "pages/00_Welcome.py",
    "needs_diagnostic":"pages/01_Diagnostic.py",
    "needs_course":    "pages/02_Skills_Profile.py",
    "in_training":     "pages/03_Home.py",
}
if state in PAGE_MAP:
    st.switch_page(PAGE_MAP[state])
```

### 5.4 Session State Keys

Only the keys below are persisted in `st.session_state`. Everything else is read from Firestore on page load.

```python
# Identity (set once on app load)
st.session_state["user_email"]   # str
st.session_state["user_state"]   # str: new_user | needs_diagnostic | needs_course | in_training

# Diagnostic flow (cleared on completion; never written to Delta mid-flow)
st.session_state["diag_responses"]    # list[dict]: [{"item_id":"...","response":"..."}]
st.session_state["diag_item_index"]   # int: 0-11

# Course module navigation
st.session_state["active_course_id"]  # str
st.session_state["active_submodule"]  # str: overview | reading | practice | evaluation | results

# Practice (in-memory only; lost on refresh — acceptable)
st.session_state["coach_messages"]    # list[dict]: [{"role":"user"|"assistant","content":"..."}]
st.session_state["practice_task_idx"] # int: 0-3
st.session_state["practice_turns"]    # int: total turns used in this session
```

### 5.5 Database Helper (`utils/db.py`)

All Firestore operations run through this helper. The `execute()` and `query_one()` functions maintain a backward-compatible API that the page files use. Internally they translate simplified SQL-like patterns into Firestore Admin SDK calls:

```python
from google.cloud import firestore
import os

_db = None

def _get_db() -> firestore.Client:
    global _db
    if _db is None:
        project = os.environ.get("GCP_PROJECT_ID", "banded-totality-485901")
        _db = firestore.Client(project=project)
    return _db

def execute(statement: str, parameters: list = None) -> list[dict]:
    """Translates simplified SQL statements to Firestore operations.
    Supports: SELECT, INSERT, UPDATE (with user_email scoping).
    Returns list of dicts for SELECT; empty list for INSERT/UPDATE."""
    # ... routes to _execute_select, _execute_insert, _execute_update

def query_one(statement: str, parameters: list = None) -> dict | None:
    """Returns first result from execute(), or None."""
    rows = execute(statement, parameters)
    return rows[0] if rows else None

def escape(value: str) -> str:
    """Escapes a string value (no-op for Firestore; kept for API compatibility)."""
    return str(value).replace("'", "\\'") if value else ""
```

> **Firestore collection mapping**: The helper maps collection names from query strings to Firestore paths under `users/{user_email}/` for learner collections (`diagnostic_sessions`, `gap_maps`, `training_progress`, `coach_sessions`) and `users/{user_email}` for `user_profiles`. The `ai_call_log` collection is top-level.

---

## 6. AI Call Workflows

### 6.1 Gemini API Helper (`utils/ai.py`)

```python
import os, time, uuid
from google import genai
from google.genai import types

# Model routing
PRO_MODEL = os.environ.get("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")
FLASH_MODEL = os.environ.get("GEMINI_FLASH_MODEL", "gemini-3-flash-preview")

_client = None

def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client

def call_llm(
    messages: list[dict],
    system_instruction: str = None,
    temperature: float = 0.1,
    use_flash: bool = False,
    response_schema: dict = None,
    user_email: str = None,
    call_type: str = "unknown"
) -> str:
    """
    messages: [{"role": "user"|"model", "content": "..."}]
    Returns the model reply as a string (JSON string if response_schema set).
    Writes one document to ai_call_log Firestore collection.
    """
    client = _get_client()
    model = FLASH_MODEL if use_flash else PRO_MODEL
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    if response_schema:
        config.response_mime_type = "application/json"
        config.response_schema = response_schema

    contents = [
        types.Content(role=m["role"], parts=[types.Part(text=m["content"])])
        for m in messages
    ]
    t0 = time.time()
    try:
        resp = client.models.generate_content(
            model=model, contents=contents, config=config
        )
        content = resp.text
        latency = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, model, latency, success=True)
        return content
    except Exception as e:
        latency = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, model, latency, success=False, error=str(e))
        raise

def _log_call(user_email, call_type, model_name, latency_ms, success, error=None):
    from utils.db import execute
    log_id = str(uuid.uuid4())
    execute(
        "INSERT INTO ai_call_log "
        "(log_id, user_email, call_type, model_name, latency_ms, success, error_message) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [log_id, user_email or "", call_type, model_name, latency_ms,
         str(success).lower(), error[:500] if error else None]
    )
```

### 6.2 Diagnostic Scoring

**Trigger**: User submits question 12.
**Model**: `gemini-3.1-pro-preview` (Pro).
**Temperature**: 0.1 (deterministic scoring).
**Output**: Set `response_schema` to enforce structured JSON — no "return only JSON" prompting needed.

**System instruction** (PTCF pattern):
```
You are a scoring engine for an AI skills assessment. Your task is to score
learner responses against the provided rubrics. Be precise and consistent.
Return scores exactly on the 0.0–4.0 scale as specified.
```

**User prompt template**:
```
Score the following learner responses against the rubrics provided.

<responses_and_rubrics>
{json_payload}
</responses_and_rubrics>

Rules:
- Each score is on a 0.0–4.0 scale.
- For MCQ items: apply the rubric's "correct" or "incorrect" value.
- For open-ended items: score each rubric criterion (0 to its max), sum, and scale to 4.0.
- domain_score = mean of all item scores for that domain.
- overall_score = mean of 4 domain scores.
```

**`response_schema`** (passed to `call_llm`):
```python
{
  "type": "object",
  "properties": {
    "item_scores":   {"type": "object"},
    "domain_scores": {"type": "object"},
    "overall_score": {"type": "number"}
  },
  "required": ["item_scores", "domain_scores", "overall_score"]
}
```

**Output**: Parse JSON response, write one Firestore document to `diagnostic_sessions`, then call gap map generation.

### 6.3 Gap Map Generation

**Trigger**: After diagnostic scoring; after each module evaluation.
**Model**: `gemini-3.1-pro-preview` (Pro).
**Temperature**: 0.4.

**System instruction**:
```
You are a supportive learning coach. Your task is to generate a personalized
gap analysis for a learner. Be specific, actionable, and encouraging.
```

**User prompt template**:
```
Generate a personalized gap analysis for this learner.

<domain_scores>
{domain_scores_json}
</domain_scores>

<domain_descriptions>
{domain_descriptions}
</domain_descriptions>

Write 3–6 gap bullets ordered by priority (biggest gap = priority 1).
Be specific to their scores and encouraging — not punitive.
```

**`response_schema`**:
```python
{
  "type": "object",
  "properties": {
    "gap_bullets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "priority":  {"type": "integer"},
          "domain_id": {"type": "string"},
          "bullet":    {"type": "string"}
        }
      }
    }
  }
}
```

**Output**: Write one Firestore document to `gap_maps` subcollection.

### 6.4 AI Coach (Practice)

**Trigger**: Each user turn during practice (max 15 total turns per session).
**Model**: `gemini-3-flash-preview` (Flash — low latency for conversational turns).
**Temperature**: 0.4.

The system instruction is loaded from `content.practice_scenarios.coach_system_prompt` for the active course. It contains course-specific coaching rules, task context, and instructions to flag if the user inputs real (non-fictional) client data. Passed via `system_instruction` param in `call_llm()`.

**Message structure** (pass `use_flash=True`):
```python
messages = [
    *st.session_state["coach_messages"],   # prior turns (role: "user"|"model")
    {"role": "user", "content": user_input},
]
call_llm(messages, system_instruction=coach_system_prompt,
          temperature=0.4, use_flash=True, call_type="coach_response")
```

**Hard limits enforced in code**:
- Max 3 turns per task; auto-advance to next task at turn 3
- Max 15 total turns across the session; show "Go to Quiz" at limit

**Output**: Append coach reply to `st.session_state["coach_messages"]`; increment `practice_turns`.

### 6.5 Evaluation Scoring

Same pattern as diagnostic scoring (§6.2). Uses `content.evaluation_items` rubrics. On completion:
1. Write `evaluation_score` and `evaluation_completed_at` to Firestore `training_progress` document
2. Write `domain_score_after` to same document
3. Unlock next module (update Firestore document: `is_locked = False` for `module_sequence_order = N+1`)
4. Trigger gap map generation (§6.3) with `source_type = 'evaluation'`

---

## 7. Module Sequencing Algorithm

Run once after the user clicks "Build My Training Course". Creates 5 documents in Firestore `training_progress` subcollection.

```python
def compute_module_sequence(domain_scores: dict) -> list[str]:
    """
    domain_scores: {"prompting": 2.0, "verification": 0.8, ...}
    Returns: list of course_ids in personalised order (index 0 = module 1).
    """
    # Map primary_domain -> course_id (from content.courses)
    domain_to_course = {
        "prompting":    "rm_c1_prompting",
        "verification": "rm_c2_verification",
        "data_safety":  "rm_c3_data_safety",
        "tool_fluency": "rm_c4_tool_fluency",
    }
    capstone = "rm_c5_capstone"  # always last

    quick_wins = sorted(
        [(d, s) for d, s in domain_scores.items() if 1.5 <= s <= 2.5],
        key=lambda x: abs(x[1] - 2.0)
    )
    gaps = sorted(
        [(d, s) for d, s in domain_scores.items() if s < 1.5],
        key=lambda x: x[1]
    )
    strong = sorted(
        [(d, s) for d, s in domain_scores.items() if s > 2.5],
        key=lambda x: x[1]
    )
    remaining = [
        (d, s) for d, s in domain_scores.items()
        if d not in {x[0] for x in quick_wins + gaps + strong}
    ]

    ordered_domains = [d for d, _ in quick_wins + gaps + remaining + strong]
    sequence = [domain_to_course[d] for d in ordered_domains if d in domain_to_course]
    sequence.append(capstone)
    return sequence[:5]
```

---

## 8. Scoring Rules

### Item scoring
| Item type | Method |
|-----------|--------|
| MCQ | `rubric["correct"]` (typically 4) if answer matches `correct_option`; else `rubric["incorrect"]` (typically 0) |
| `prompt_sandbox`, `micro_task`, `performance_task` | AI scores each rubric criterion (0–max); sum scaled to 0–4 |

### Domain score
Average of all scored items for that domain (diagnostic items + any completed evaluation items; equal weight per item).

### Overall score
Average of 4 domain scores.

### Level label
| Score range | Label |
|-------------|-------|
| 0.0–0.4 | Unaware |
| 0.5–1.4 | Explorer |
| 1.5–2.4 | Practitioner |
| 2.5–3.4 | Proficient |
| 3.5–4.0 | Champion |

---

## 9. Error Handling & Resilience

### AI call failures
```python
try:
    response = call_llm(messages, temperature=0.1, call_type="diagnostic_scoring")
except Exception:
    st.error("We encountered an issue scoring your responses. Your answers are saved. Please try again.")
    st.stop()
    # session_state["diag_responses"] is preserved; user can retry
```

### Database failures
```python
try:
    rows = execute(statement)
except RuntimeError as e:
    st.error("Unable to load your data. Please refresh the page.")
    st.stop()
```

### Session recovery rules
| Phase | Refresh behaviour |
|-------|------------------|
| Diagnostic (mid-flow) | Restart from Q1; `diag_responses` cleared (acceptable for 5-min assessment) |
| Practice (mid-session) | Restart from Task 1; coach conversation lost (acceptable; practice is exploratory) |
| Reading | Re-read; completion flag only written on CTA click |
| Evaluation (mid-flow) | Restart from Q1; no partial saves |

---

## 10. Deployment & CI/CD

### 10.1 Local Development

```bash
# Set up virtual environment
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in: GOOGLE_API_KEY, GCP_PROJECT_ID, USER_EMAIL

# Run locally
streamlit run app.py
```

### 10.2 Dockerfile

```dockerfile
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8080
CMD ["streamlit", "run", "app.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

> **Cloud Run session state note**: Set `min-instances=1` to keep at least one container warm and prevent Streamlit session state from being lost on cold starts.

### 10.3 Environment Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `GOOGLE_API_KEY` | GCP Secret Manager | Gemini API key; injected as env var by Cloud Run |
| `GCP_PROJECT_ID` | Cloud Run env | GCP project: `banded-totality-485901` |
| `USER_EMAIL` | Cloud Run env | Authenticated user's email (set per-deployment for MVP) |
| `GEMINI_PRO_MODEL` | Cloud Run env (optional) | Overrides default Pro model name |
| `GEMINI_FLASH_MODEL` | Cloud Run env (optional) | Overrides default Flash model name |

### 10.4 Deploy to Cloud Run

```bash
# Build and push container
gcloud builds submit --tag gcr.io/banded-totality-485901/ai-hero-academy

# Deploy to Cloud Run
gcloud run deploy ai-hero-academy \
  --image gcr.io/banded-totality-485901/ai-hero-academy \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances=1 \
  --set-secrets="GOOGLE_API_KEY=GOOGLE_API_KEY:latest" \
  --set-env-vars="GCP_PROJECT_ID=banded-totality-485901,USER_EMAIL=user@example.com"
```

### 10.5 CI/CD (GitHub Actions)

```yaml
- name: Deploy to Cloud Run
  uses: google-github-actions/deploy-cloudrun@v2
  with:
    service: ai-hero-academy
    region: us-central1
    image: gcr.io/banded-totality-485901/ai-hero-academy:${{ github.sha }}
    env_vars: |
      GCP_PROJECT_ID=banded-totality-485901
    secrets: |
      GOOGLE_API_KEY=GOOGLE_API_KEY:latest
```

---

## 11. Security & Access Control

| Concern | Approach |
|---------|---------|
| Authentication | `USER_EMAIL` environment variable (MVP); future: Firebase Auth |
| Learner data isolation | Every Firestore query is scoped to `users/{user_email}/` subcollections |
| Content write protection | Content is served from bundled JSON files; no database writes for content |
| AI logs | `ai_call_log` Firestore collection is write-only for the app; readable by GCP admins |
| Secrets | `GOOGLE_API_KEY` stored in GCP Secret Manager; exposed to Cloud Run as env var via native integration |
| Content safety | All seeded content uses fictional companies and data only (per PRD §13.2) |
| Cloud Run service account | Principle of Least Privilege: only `secretmanager.secretAccessor` + Firestore read/write roles granted |
| No ADC credentials needed | Running on Cloud Run, the service account is automatically used for GCP APIs (Firestore, Secret Manager) |

---

## 12. Performance Targets

| Metric | Target | Measured via |
|--------|--------|-------------|
| Diagnostic scoring + gap map | < 45s end-to-end | `ai_call_log.latency_ms` in Firestore |
| Coach response per turn | < 10s | `ai_call_log.latency_ms` in Firestore |
| Evaluation scoring + gap map | < 30s | `ai_call_log.latency_ms` in Firestore |
| Page load (Firestore reads) | < 2s | Cloud Run request logs |
| Firestore reads per page load | ≤ 3 | Code review |

---

## 13. Out of Scope for MVP

Do not build toward:

- Manager or leadership dashboards
- Admin content management UI
- Proficient/advanced training tier
- Firebase Authentication SSO (future v1)
- Advanced analytics or admin dashboards
- Badge export or HR integration
- Mobile-optimised layout
- Multilingual content (English only)
- Email notifications or leaderboards
- Peer comparison features
- Vertex AI or model fine-tuning

**Multi-role status (updated Feb 2026):** The Underwriter (UW) role is in progress — content fully generated and loaded; Welcome page wiring (Task 9.4 in PLAN.md) is the only remaining step. Additional roles beyond UW remain out of scope for MVP.
