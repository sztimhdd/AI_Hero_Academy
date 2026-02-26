# Technical Design Document (TDD)
## AI Hero Academy MVP

**Version**: 1.1
**Date**: February 2026
**Status**: In Development

---

## 1. Overview

AI Hero Academy is a Streamlit-based Databricks App that delivers personalized AI skills training to employees. It implements a four-stage learning loop: **Diagnose → Map Gaps → Train → Score & Track**.

The MVP covers the Relationship Manager (RM) role. The Underwriter (UW) role content is fully generated and in-app — welcome page wiring is the remaining step before UW users can onboard. Each role has 12 diagnostic questions across 4 skill domains and 5 training courses. All AI scoring, coaching, and gap analysis is powered by Databricks Foundation Model serving endpoints. All learner state is persisted in Delta tables via Unity Catalog (`mdlg_ai_shared`). Static content (courses, diagnostic items, reading, scenarios, evaluations) is served from JSON files bundled with the app — no Delta queries needed for content.

---

## 2. Architecture

### 2.1 Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Frontend** | Streamlit (multi-page) | Hosted as a Databricks App |
| **SQL** | Databricks Serverless SQL Warehouse | `eaa098820703bf5f`; all queries via `WorkspaceClient` |
| **AI** | Databricks Foundation Model APIs | Accessed via `w.serving_endpoints.query()`; endpoint name injected via env var |
| **State** | Delta tables in Unity Catalog `mdlg_ai_shared` | Three schemas: `content`, `learner`, `system` |
| **Auth** | Databricks workspace SSO | `user_email` extracted from `SparkContext` or `dbutils` context in App runtime |
| **Hosting** | Databricks Apps (container-based) | `app.yml` declares command and env vars |

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

### 2.3 Foundation Model Endpoints

All endpoints support the OpenAI-compatible `llm/v1/chat` interface. The active endpoint is injected via the `SERVING_ENDPOINT_NAME` environment variable.

| Endpoint | Use case |
|----------|----------|
| `databricks-claude-sonnet-4-6` | **Default** — scoring, gap maps, coach responses |
| `databricks-claude-haiku-4-5` | Low-latency coach turns (optional optimisation) |
| `databricks-claude-opus-4-6` | Complex capstone evaluation scoring |
| `databricks-gemini-3-1-pro` | Alternative; same interface |

---

## 3. Data Schema

### 3.1 Design Principles

- **JSON strings over complex types**: Delta `MAP<>` and `ARRAY<STRUCT<>>` columns are avoided for MVP. Structured data (options, rubrics, responses, scores) is stored as plain JSON strings and parsed in Python. This keeps SQL simple and avoids SDK serialisation friction.
- **`user_email` as identity key**: `user_email` from Databricks SSO is used directly as the primary key in `learner.user_profiles` and as a filter in all learner queries. No UUID layer needed for MVP.
- **Idempotent seeding**: Content tables are populated via `DELETE + INSERT` from Databricks notebooks (not the app). The app has read-only access to `content.*`.

### 3.2 Content Schema

> **Architecture note (Feb 2026):** All `content.*` Delta tables have been retired. Static content is now served from `content/*.json` files bundled with the app and loaded at startup by `utils/content.py`. The Delta DDL below is preserved as reference for the data shape; the app no longer queries these tables.

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

### 3.3 Learner Schema

All tables in `learner` are read-write for the app. Every query is filtered by `user_email`.

#### `learner.user_profiles`
```sql
user_email    STRING NOT NULL PRIMARY KEY,   -- from Databricks SSO
display_name  STRING,
role_id       STRING NOT NULL,
created_at    TIMESTAMP NOT NULL DEFAULT current_timestamp()
```

`user_email` is the identity key throughout the system. No UUID layer is used in MVP.

#### `learner.diagnostic_sessions`
```sql
session_id     STRING NOT NULL PRIMARY KEY,
user_email     STRING NOT NULL,
started_at     TIMESTAMP NOT NULL DEFAULT current_timestamp(),
completed_at   TIMESTAMP,
responses      STRING,   -- JSON: {"item_id": "response_text", ...}
item_scores    STRING,   -- JSON: {"item_id": score_float, ...}
domain_scores  STRING,   -- JSON: {"domain_id": score_float, ...}
overall_score  DOUBLE
```

Multiple sessions per user are allowed (retakes). The app always uses the most recent completed session (`ORDER BY completed_at DESC LIMIT 1`).

#### `learner.gap_maps`
```sql
gap_map_id    STRING NOT NULL PRIMARY KEY,
user_email    STRING NOT NULL,
source_type   STRING NOT NULL,   -- 'diagnostic' | 'evaluation'
source_id     STRING NOT NULL,   -- session_id or progress_id
bullets       STRING NOT NULL,   -- JSON: [{"priority":1,"domain_id":"...","bullet":"..."}, ...]
generated_at  TIMESTAMP NOT NULL DEFAULT current_timestamp()
```

A new row is inserted after each diagnostic completion and after each module evaluation completion. The app always shows the most recent (`ORDER BY generated_at DESC LIMIT 1`).

#### `learner.training_progress`
```sql
progress_id              STRING NOT NULL PRIMARY KEY,
user_email               STRING NOT NULL,
course_id                STRING NOT NULL,
module_sequence_order    INT NOT NULL,       -- 1-5; personalized per user
is_locked                BOOLEAN NOT NULL DEFAULT true,
reading_completed_at     TIMESTAMP,
practice_completed_at    TIMESTAMP,
evaluation_score         DOUBLE,
evaluation_completed_at  TIMESTAMP,
domain_score_after       DOUBLE             -- domain score after this module's evaluation
```

Five rows created per user when they click "Build My Training Course". Module 1 is immediately unlocked (`is_locked = false`). Modules 2–5 are unlocked sequentially as the prior module's evaluation is completed.

**Lock state derivation**: A module is considered complete when `evaluation_completed_at IS NOT NULL`. Reading is complete when `reading_completed_at IS NOT NULL`. Practice is complete when `practice_completed_at IS NOT NULL`.

#### `learner.coach_sessions`
```sql
session_id         STRING NOT NULL PRIMARY KEY,
user_email         STRING NOT NULL,
course_id          STRING NOT NULL,
started_at         TIMESTAMP NOT NULL DEFAULT current_timestamp(),
completed_at       TIMESTAMP,
turn_count         INT NOT NULL DEFAULT 0,
conversation_json  STRING NOT NULL   -- JSON: [{"role":"user"|"assistant","content":"..."}, ...]
```

Written once when the user clicks "Complete Practice". The `conversation_json` format is the standard OpenAI messages array format, compatible with the serving endpoint API.

### 3.4 System Schema

#### `system.ai_call_log`
```sql
log_id            STRING NOT NULL PRIMARY KEY,
user_email        STRING,
call_type         STRING NOT NULL,   -- 'diagnostic_scoring' | 'gap_map' | 'coach_response' | 'evaluation_scoring'
model_endpoint    STRING NOT NULL,
prompt_tokens     INT,
completion_tokens INT,
latency_ms        INT,
success           BOOLEAN NOT NULL,
error_message     STRING,
called_at         TIMESTAMP NOT NULL DEFAULT current_timestamp()
```

Every AI call writes one row. Used for monitoring, debugging, and token cost tracking. Not exposed to end users.

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

### 4.4 Remaining Seeding (learner + system schemas only)

`notebooks/00_create_schemas.py` is still used to create `learner.*` and `system.*` Delta schemas on first deploy. It no longer creates `content.*` tables.

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
app.yml                       # Databricks App command + env vars
pages/
  00_Welcome.py               # new user onboarding + role selection
  01_Diagnostic.py            # 12-question diagnostic assessment (multi-role)
  02_Skills_Profile.py        # domain scores, gap map, assessment history
  03_Home.py                  # course progress dashboard
  04_Course_Module.py         # reading / practice / evaluation sub-views
utils/
  db.py                       # SQL execution helper; wraps WorkspaceClient
  ai.py                       # serving endpoint calls; writes to ai_call_log
  auth.py                     # extracts user_email from Databricks App context
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
notebooks/
  00_create_schemas.py        # creates learner.* + system.* Delta schemas
requirements.txt              # streamlit, databricks-sdk, plotly, tenacity, ...
```

### 5.2 Auth: Extracting `user_email`

In Databricks Apps, the authenticated user's email is available via the `DATABRICKS_USER_EMAIL` environment variable injected by the App runtime:

```python
# utils/auth.py
import os

def get_user_email() -> str:
    email = os.environ.get("DATABRICKS_USER_EMAIL")
    if not email:
        # Fallback for local development
        email = os.environ.get("DEV_USER_EMAIL", "dev@example.com")
    return email
```

Never use hardcoded emails or require the user to type their email.

### 5.3 Router Logic (`app.py`)

On every page load, the app reads user state from Delta and routes:

```python
import streamlit as st
from utils.auth import get_user_email
from utils.db import query_one

def get_user_state(user_email: str) -> str:
    profile = query_one(
        "SELECT role_id FROM mdlg_ai_shared.learner.user_profiles WHERE user_email = ?",
        [user_email]
    )
    if not profile:
        return "new_user"

    session = query_one(
        "SELECT session_id FROM mdlg_ai_shared.learner.diagnostic_sessions "
        "WHERE user_email = ? AND completed_at IS NOT NULL "
        "ORDER BY completed_at DESC LIMIT 1",
        [user_email]
    )
    if not session:
        return "needs_diagnostic"

    progress = query_one(
        "SELECT progress_id FROM mdlg_ai_shared.learner.training_progress "
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

Only the keys below are persisted in `st.session_state`. Everything else is read from Delta on page load.

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

All SQL runs through this helper. Parameterised queries use `?` placeholders via `disposition` and `parameters` args:

```python
from databricks.sdk import WorkspaceClient
import os, json

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = WorkspaceClient()
    return _client

def execute(statement: str, parameters: list = None) -> dict:
    """Returns {"columns": [...], "rows": [...]}"""
    w = _get_client()
    kwargs = dict(
        warehouse_id=os.environ["DATABRICKS_WAREHOUSE_ID"],
        statement=statement,
        wait_timeout="30s",
    )
    if parameters:
        kwargs["parameters"] = [
            {"name": str(i+1), "value": str(p)} for i, p in enumerate(parameters)
        ]
        statement = statement  # placeholders must be ?1, ?2, ... or use named params
    result = w.statement_execution.execute_statement(**kwargs)
    if result.status.error:
        raise RuntimeError(result.status.error.message)
    cols = [c.name for c in (result.manifest.schema.columns or [])]
    rows = [dict(zip(cols, r.values)) for r in (result.result.data_array or [])]
    return rows

def query_one(statement: str, parameters: list = None):
    rows = execute(statement, parameters)
    return rows[0] if rows else None
```

> **Note on parameters**: The Databricks Statement Execution API supports named parameters (`?` with `StatementParameterListItem`). For MVP simplicity, string interpolation with an `escape()` function is acceptable for read-only content queries. Use parameterised queries for all learner writes.

---

## 6. AI Call Workflows

### 6.1 Serving Endpoint Helper (`utils/ai.py`)

```python
import os, time, json, uuid
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

def call_llm(messages: list[dict], temperature: float = 0.1, user_email: str = None,
             call_type: str = "unknown") -> str:
    """
    messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
    Returns the assistant reply as a string.
    Writes one row to system.ai_call_log.
    """
    w = WorkspaceClient()
    endpoint = os.environ["SERVING_ENDPOINT_NAME"]
    sdk_messages = [
        ChatMessage(
            role=ChatMessageRole[m["role"].upper()],
            content=m["content"]
        )
        for m in messages
    ]
    t0 = time.time()
    try:
        resp = w.serving_endpoints.query(name=endpoint, messages=sdk_messages,
                                         temperature=temperature)
        content = resp.choices[0].message.content
        latency = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, endpoint, latency, success=True)
        return content
    except Exception as e:
        latency = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, endpoint, latency, success=False, error=str(e))
        raise

def _log_call(user_email, call_type, endpoint, latency_ms, success, error=None):
    from utils.db import execute
    log_id = str(uuid.uuid4())
    execute(f"""
        INSERT INTO mdlg_ai_shared.system.ai_call_log
          (log_id, user_email, call_type, model_endpoint, latency_ms, success, error_message)
        VALUES ('{log_id}', '{user_email or ""}', '{call_type}', '{endpoint}',
                {latency_ms}, {str(success).upper()}, {'NULL' if not error else f"'{error[:500]}'"})
    """)
```

### 6.2 Diagnostic Scoring

**Trigger**: User submits question 12.
**Temperature**: 0.1 (deterministic scoring).

**Prompt template**:
```
You are a scoring engine. Score the learner responses below against the rubrics provided.
Return ONLY valid JSON — no explanation, no markdown fences.

RESPONSES AND RUBRICS:
{json_payload}

Return:
{
  "item_scores": {"item_id": score_float, ...},
  "domain_scores": {"domain_id": score_float, ...},
  "overall_score": float
}

Rules:
- Each score is on a 0.0–4.0 scale.
- For MCQ items: apply the rubric's "correct" or "incorrect" value.
- For open-ended items: score each rubric criterion (0 to its max), sum, and scale to 4.0.
- domain_score = mean of all item scores for that domain.
- overall_score = mean of 4 domain scores.
```

**Output**: Parse JSON, write one row to `learner.diagnostic_sessions`, then call gap map generation.

### 6.3 Gap Map Generation

**Trigger**: After diagnostic scoring; after each module evaluation.
**Temperature**: 0.4.

**Prompt template**:
```
You are a learning coach generating a personalized gap analysis for an RM learner.

Domain scores (0–4 scale):
{domain_scores_json}

Domain descriptions:
{domain_descriptions}

Write 3–6 gap bullets. Order by priority (biggest gap = priority 1).
Each bullet should be specific, actionable, and encouraging — not punitive.
Return ONLY valid JSON:
{
  "gap_bullets": [
    {"priority": 1, "domain_id": "...", "bullet": "..."},
    ...
  ]
}
```

**Output**: Insert one row into `learner.gap_maps` with `bullets` as JSON string.

### 6.4 AI Coach (Practice)

**Trigger**: Each user turn during practice (max 15 total turns per session).
**Temperature**: 0.4.

The system prompt is loaded from `content.practice_scenarios.coach_system_prompt` for the active course. It contains course-specific coaching rules, task context, and the instruction to flag if the user appears to input real (non-fictional) client data.

**Message structure**:
```python
messages = [
    {"role": "system", "content": coach_system_prompt},
    *st.session_state["coach_messages"],   # prior turns
    {"role": "user", "content": user_input},
]
```

**Hard limits enforced in code (not in Delta)**:
- Max 3 turns per task; auto-advance to next task at turn 3
- Max 15 total turns across the session; show "Go to Quiz" at limit

**Output**: Append coach reply to `st.session_state["coach_messages"]`; increment `practice_turns`.

### 6.5 Evaluation Scoring

Same pattern as diagnostic scoring (§6.2). Uses `content.evaluation_items` rubrics. On completion:
1. Write `evaluation_score` and `evaluation_completed_at` to `learner.training_progress`
2. Write `domain_score_after` to `learner.training_progress`
3. Unlock next module (`UPDATE ... SET is_locked = false WHERE module_sequence_order = N+1`)
4. Trigger gap map generation (§6.3) with `source_type = 'evaluation'`

---

## 7. Module Sequencing Algorithm

Run once after the user clicks "Build My Training Course". Creates 5 rows in `learner.training_progress`.

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

### 10.1 Local development

```bash
.venv/Scripts/pip install -r requirements.txt
DEV_USER_EMAIL=you@example.com .venv/Scripts/streamlit run app.py
```

Auth is handled by the Databricks VS Code extension metadata service. No token setup needed when running inside VS Code.

### 10.2 `app.yml`

```yaml
command: [".venv/bin/streamlit", "run", "app.py", "--server.port", "8080"]
env:
  - name: DATABRICKS_WAREHOUSE_ID
    value: "eaa098820703bf5f"
  - name: SERVING_ENDPOINT_NAME
    value: "databricks-claude-sonnet-4-6"
  - name: UC_CATALOG
    value: "mdlg_ai_shared"
```

### 10.3 Deploy

```bash
# Sync files to workspace (live iteration)
databricks sync --watch . /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp

# Deploy the app
databricks apps deploy my-ai-hero-academy-mvp \
  --source-code-path /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp
```

### 10.4 CI/CD (GitHub Actions)

```yaml
- uses: databricks/setup-cli@main
- name: Deploy app
  run: |
    databricks apps deploy my-ai-hero-academy-mvp \
      --source-code-path /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp
  env:
    DATABRICKS_HOST: https://adb-2717931942638877.17.azuredatabricks.net
    DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
```

---

## 11. Security & Access Control

| Concern | Approach |
|---------|---------|
| Authentication | Databricks workspace SSO; `user_email` from App runtime env var |
| Learner data isolation | Every `learner.*` query includes `WHERE user_email = '<current_user>'` |
| Content write protection | App service principal has `SELECT` on `content.*` only |
| AI logs | `system.ai_call_log` is write-only for the app; read by workspace admins |
| No secrets in code | Warehouse ID, endpoint name, catalog injected via `app.yml` env vars |
| Content safety | All seeded content uses fictional companies and data only (per PRD §13.2) |
| App service principal UC grants | The deployed App runs as its own SP — **distinct from the deploying user's identity**. Group membership (e.g. `ai-mlengineer-mdlg`) does not propagate to the App SP. Required grants on `mdlg_ai_shared`: `USE CATALOG`; `USE SCHEMA` on `content`, `learner`, `system`; `SELECT` on all 7 `content.*` tables; `SELECT + MODIFY` on all 5 `learner.*` tables and `system.ai_call_log`. Grant syntax: `` GRANT USE CATALOG ON CATALOG mdlg_ai_shared TO `<app-sp-client-uuid>` `` (SP referenced by its application UUID in backticks, not by display name) |

---

## 12. Performance Targets

| Metric | Target | Measured via |
|--------|--------|-------------|
| Diagnostic scoring + gap map | < 45s end-to-end | `ai_call_log.latency_ms` |
| Coach response per turn | < 10s | `ai_call_log.latency_ms` |
| Evaluation scoring + gap map | < 30s | `ai_call_log.latency_ms` |
| Page load (Delta reads) | < 3s | Warehouse query history |
| SQL queries per page load | ≤ 3 | Code review |

---

## 13. Out of Scope for MVP

Do not build toward:

- Manager or leadership dashboards
- Admin content management UI
- Proficient/advanced training tier
- MLflow prompt versioning
- Materialized views or SQL Warehouse analytics
- Badge export or HR integration
- Mobile-optimised layout
- Multilingual content (English only)
- Email notifications or leaderboards
- Peer comparison features

**Multi-role status (updated Feb 2026):** The Underwriter (UW) role is in progress — content fully generated and loaded; Welcome page wiring (Task 9.4 in PLAN.md) is the only remaining step. Additional roles beyond UW remain out of scope for MVP.
