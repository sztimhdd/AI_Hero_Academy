
# Technical Design Document (TDD)
## AI Hero Academy MVP

**Version**: 1.0  
**Date**: June 2025  
**Status**: In Development

---

## 1. Overview

This document describes the technical architecture, data schema, API patterns, and implementation strategy for the AI Hero Academy MVP—a Streamlit-based Databricks App that delivers personalized AI skills training to Relationship Managers through diagnostic assessment, gap mapping, and scenario-based practice with AI coaching.

---

## 2. Architecture

### 2.1 High-Level Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Multi-page app with session state management |
| **Compute** | Databricks Serverless SQL Warehouse | Query execution (`eaa098820703bf5f`) |
| **AI Models** | Foundation Model serving endpoints | Diagnostic scoring, gap mapping, coaching, evaluation |
| **Persistence** | Delta tables (Unity Catalog `mdlg_ai`) | User profiles, assessments, progress, AI logs |
| **Auth** | Databricks workspace SSO | Identity via `user_email` |
| **Hosting** | Databricks App runtime | Container-based, auto-scaling |

### 2.2 Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  (Welcome / Diagnostic / Skills Profile / Home / Module)    │
└──────────────┬──────────────────────────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
   ┌────▼────┐   ┌───▼────┐
   │ Session │   │ Queries │
   │ State   │   │ to DW   │
   └─────────┘   └───┬────┘
                     │
        ┌────────────┴──────────────┐
        │                           │
   ┌────▼──────────────────────┐  ┌▼───────────────────┐
   │  Unity Catalog (mdlg_ai)  │  │ Foundation Model   │
   │  ├─ content.*             │  │ Serving Endpoints  │
   │  ├─ learner.*             │  │ ├─ gemini-3-1-pro  │
   │  └─ system.*              │  │ ├─ claude-sonnet   │
   └─────────────────────────┘  │ └─ etc.            │
                                 └───────────────────┘
```

---

## 3. Data Schema

### 3.1 Schema Organization

All tables live in `mdlg_ai` catalog across three schemas:

- **`content`** — read-only; pre-seeded via notebooks
- **`learner`** — read-write; per-user data (all queries filtered by `user_email`)
- **`system`** — app logs; read-only for end users

### 3.2 Content Schema (Static)

#### `content.roles`
```sql
role_id STRING PRIMARY KEY
role_name STRING
description STRING
created_at TIMESTAMP
```

#### `content.domains`
```sql
domain_id STRING PRIMARY KEY
domain_name STRING
description STRING
level_descriptors MAP<INT, STRING>  -- 0→Unaware, 1→Explorer, 2→Practitioner, 3→Proficient, 4→Champion
created_at TIMESTAMP
```

#### `content.diagnostic_items`
```sql
item_id STRING PRIMARY KEY
domain_id STRING FOREIGN KEY → domains.domain_id
question_number INT              -- 1-12
item_type STRING ENUM(mcq, prompt_sandbox, micro_task)
scenario_text STRING
question_text STRING
options MAP<STRING, FLOAT>        -- {A: 2.0, B: 1.5, C: 0.0, ...} for MCQ
rubric MAP<STRING, FLOAT>         -- {criterion_1: 0.25, criterion_2: 0.75} for perf tasks
created_at TIMESTAMP
```

#### `content.courses`
```sql
course_id STRING PRIMARY KEY
course_name STRING
primary_domain_id STRING FOREIGN KEY → domains.domain_id
use_case_summary STRING
created_at TIMESTAMP
```

#### `content.reading_content`
```sql
reading_id STRING PRIMARY KEY
course_id STRING FOREIGN KEY → courses.course_id
module_number INT                -- 1-5
title STRING
body STRING (markdown)
created_at TIMESTAMP
```

#### `content.practice_scenarios`
```sql
scenario_id STRING PRIMARY KEY
course_id STRING FOREIGN KEY → courses.course_id
module_number INT
scenario_text STRING
task_1_prompt STRING
task_2_prompt STRING
task_3_prompt STRING
task_4_prompt STRING
coach_system_prompt STRING        -- instructions for AI coach
max_turns_per_task INT DEFAULT 3
total_max_turns INT DEFAULT 15
created_at TIMESTAMP
```

#### `content.evaluation_items`
```sql
eval_item_id STRING PRIMARY KEY
course_id STRING FOREIGN KEY → courses.course_id
module_number INT
question_number INT              -- 1-4
item_type STRING ENUM(mcq, performance_task)
scenario_text STRING
question_text STRING
options MAP<STRING, FLOAT>        -- for MCQ
rubric MAP<STRING, FLOAT>         -- for performance task
created_at TIMESTAMP
```

### 3.3 Learner Schema (Dynamic)

#### `learner.user_profiles`
```sql
user_id STRING PRIMARY KEY (generated as UUID)
user_email STRING UNIQUE          -- from SSO context
display_name STRING
role_id STRING FOREIGN KEY → content.roles.role_id
created_at TIMESTAMP
updated_at TIMESTAMP
```

#### `learner.diagnostic_sessions`
```sql
session_id STRING PRIMARY KEY
user_id STRING FOREIGN KEY → user_profiles.user_id
user_email STRING                -- denormalized for easy filtering
started_at TIMESTAMP
completed_at TIMESTAMP
responses ARRAY<STRUCT<
  item_id STRING,
  user_response STRING,
  item_score FLOAT,
  domain_id STRING
>>
domain_scores MAP<STRING, FLOAT>  -- {domain_id: overall_score, ...}
overall_score FLOAT
is_latest BOOLEAN DEFAULT TRUE
created_at TIMESTAMP
```

#### `learner.gap_maps`
```sql
gap_map_id STRING PRIMARY KEY
user_id STRING FOREIGN KEY → user_profiles.user_id
user_email STRING
session_id STRING FOREIGN KEY → diagnostic_sessions.session_id
generated_by STRING ENUM(diagnostic, evaluation)
gap_bullets ARRAY<STRUCT<
  priority INT,
  domain_id STRING,
  bullet_text STRING
>>
created_at TIMESTAMP
```

#### `learner.training_progress`
```sql
progress_id STRING PRIMARY KEY
user_id STRING FOREIGN KEY → user_profiles.user_id
user_email STRING
course_id STRING FOREIGN KEY → content.courses.course_id
module_sequence_order INT         -- 1-5 (personalized per user)
status STRING ENUM(locked, available, in_progress, completed)
reading_started_at TIMESTAMP
reading_completed_at TIMESTAMP
practice_started_at TIMESTAMP
practice_completed_at TIMESTAMP
eval_started_at TIMESTAMP
eval_completed_at TIMESTAMP
eval_score FLOAT
practice_turn_count INT DEFAULT 0
created_at TIMESTAMP
updated_at TIMESTAMP
```

#### `learner.coach_sessions`
```sql
session_id STRING PRIMARY KEY
user_id STRING FOREIGN KEY → user_profiles.user_id
user_email STRING
course_id STRING FOREIGN KEY → content.courses.course_id
module_number INT
started_at TIMESTAMP
completed_at TIMESTAMP
conversation ARRAY<STRUCT<
  turn_number INT,
  role STRING ENUM(user, coach),
  content STRING,
  timestamp TIMESTAMP
>>
total_turns INT
task_sequence ARRAY<INT>          -- which tasks completed in which order
created_at TIMESTAMP
```

### 3.4 System Schema (Logs)

#### `system.ai_call_log`
```sql
call_id STRING PRIMARY KEY
user_email STRING
call_type STRING ENUM(diagnostic_scoring, gap_mapping, coaching, eval_scoring)
model_name STRING
prompt STRING(large)
response STRING(large)
latency_ms INT
http_status INT
error_message STRING
created_at TIMESTAMP
```

---

## 4. Page Architecture & State Management

### 4.1 Multi-Page Structure

```
app/
├── pages/
│   ├── 00_Welcome.py
│   ├── 01_Diagnostic.py
│   ├── 02_Skills_Profile.py
│   ├── 03_Home.py
│   └── 04_Course_Module.py
├── utils/
│   ├── auth.py             # SSO context, user_email extraction
│   ├── db.py               # SQL execution via WorkspaceClient
│   ├── ai.py               # Serving endpoint calls
│   ├── scoring.py          # Diagnostic/eval scoring logic
│   └── sequencing.py       # Module sequence algorithm
└── app.py                  # Router & session init
```

### 4.2 Session State Keys

```python
st.session_state = {
    "user_email": "...",           # from SSO
    "user_id": "...",              # from user_profiles
    "user_state": "new_user|needs_diagnostic|needs_course|in_training|completed",
    
    # Diagnostic flow
    "diagnostic_responses": [
        {"item_id": "...", "response": "...", "domain_id": "..."},
        ...
    ],
    "current_question_index": 0,
    
    # Course flow
    "current_course_id": "...",
    "current_module_number": 1,
    "current_submodule": "overview|reading|practice|evaluation|results",
    
    # Practice flow (in-memory only)
    "coach_conversation": [
        {"role": "user", "content": "..."},
        {"role": "coach", "content": "..."},
    ],
    "current_task_index": 0,
    "current_task_turns": 0,
}
```

### 4.3 Router Logic (app.py)

```python
def determine_user_state(user_email):
    # Query learner.user_profiles
    # Query learner.diagnostic_sessions (latest)
    # Query learner.training_progress (any row for this user)
    # Return: new_user|needs_diagnostic|needs_course|in_training|completed

def route_to_page(user_state):
    if user_state == "new_user":
        st.switch_page("pages/00_Welcome.py")
    elif user_state == "needs_diagnostic":
        st.switch_page("pages/01_Diagnostic.py")
    # ... etc.
```

---

## 5. AI Call Workflows

### 5.1 Diagnostic Scoring

**Trigger**: User submits question 12

**Input**:
- All 12 responses (from `st.session_state["diagnostic_responses"]`)
- Rubrics (fetched from `content.diagnostic_items`)

**Prompt template** (temperature 0.1):
```
Score the following responses against the rubric. Return JSON.
{
  "item_scores": [
    {"item_id": "...", "score": 3.2},
    ...
  ],
  "domain_scores": {
    "domain_id_1": 2.5,
    "domain_id_2": 1.8,
    ...
  }
}
```

**Output**:
- Write to `learner.diagnostic_sessions` (all 12 item scores + domain scores)
- Trigger gap map generation

### 5.2 Gap Map Generation

**Trigger**: After diagnostic scoring OR after evaluation submission

**Input**:
- User's domain scores
- User's responses (context)
- Domain definitions

**Prompt template** (temperature 0.4):
```
Generate 3-6 personalized gap bullets for this learner. Order by priority (biggest gap first).
Return JSON:
{
  "gap_bullets": [
    {"priority": 1, "domain_id": "...", "bullet": "..."},
    ...
  ]
}
```

**Output**:
- Write to `learner.gap_maps`

### 5.3 AI Coach Response

**Trigger**: User submits task input during practice

**Input**:
- Task prompt (from `content.practice_scenarios`)
- User's input text
- Coach system prompt (course-specific)
- Prior conversation (if any)
- Turn count (must not exceed `max_turns_per_task`)

**Prompt template** (temperature 0.4):
```
You are an AI coach for [RM role]. Current task: [task_prompt]

User input: "[user_text]"

Prior conversation:
[conversation history]

Rules:
- Keep responses concise (<200 words)
- Ask clarifying questions
- Flag if user shares real non-public client data
- Do NOT provide the answer

Respond as the coach:
```

**Output** (in-memory, not persisted until practice complete):
- Add turn to `st.session_state["coach_conversation"]`
- Increment turn counter

### 5.4 Evaluation Scoring

**Trigger**: User submits question 4 of evaluation quiz

**Input**:
- All 4 responses
- Rubrics (from `content.evaluation_items`)

**Process**: Same pattern as diagnostic scoring

**Output**:
- Write to `learner.training_progress` (eval score, eval_completed_at)
- Trigger gap map update (with generated_by = "evaluation")
- Unlock next module

---

## 6. Error Handling & Resilience

### 6.1 AI Call Failures

```python
try:
    response = call_serving_endpoint(...)
except Exception as e:
    log_ai_call(call_type, prompt, None, http_status=500, error=str(e))
    st.error("We encountered an issue processing your response. Your progress has been saved. Please try again.")
    # Do NOT lose session state; user can retry
```

### 6.2 Database Query Failures

```python
try:
    result = execute_sql(statement, warehouse_id)
except Exception as e:
    log_system_event("db_query_failed", str(e))
    st.error("Unable to load your data. Please refresh the page.")
```

### 6.3 Session Timeout & Recovery

- **Diagnostic**: No partial saves. If user refreshes mid-diagnostic, session resets (restart from Q1).
- **Practice**: In-memory only. Refresh = restart task 1.
- **Reading**: Completion flag written on CTA. Refresh before CTA = stay in reading.
- **Evaluation**: No partial saves. If user refreshes mid-evaluation, restart from Q1.

---

## 7. Deployment & CI/CD

### 7.1 Local Development

```bash
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/streamlit run app.py
```

### 7.2 Sync to Workspace

```bash
databricks sync --watch . /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp
```

### 7.3 App Deployment

**File**: `app.yml`
```yaml
command: [".venv/bin/streamlit", "run", "app.py", "--server.port", "8080"]
env:
  - name: DATABRICKS_WAREHOUSE_ID
    value: "eaa098820703bf5f"
  - name: SERVING_ENDPOINT_NAME
    value: "databricks-gemini-3-1-pro"
```

**Deploy**:
```bash
databricks apps deploy my-ai-hero-academy-mvp --source-code-path /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp
```

### 7.4 CI/CD (GitHub Actions)

```yaml
- uses: databricks/setup-cli@main
- run: databricks apps deploy my-ai-hero-academy-mvp --source-code-path /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp
  env:
    DATABRICKS_HOST: https://adb-2717931942638877.17.azuredatabricks.net
    DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
```

---

## 8. Security & Access Control

- **Authentication**: Databricks workspace SSO; `user_email` extracted from context
- **Data filtering**: All learner schema queries `WHERE user_email = :current_user`
- **Content access**: Read-only; no user can modify; pre-seeded via admin notebooks
- **AI logs**: `system.ai_call_log` written by app, read by admins only
- **No secrets in code**: Use environment variables (`DATABRICKS_WAREHOUSE_ID`, `SERVING_ENDPOINT_NAME`)

---

## 9. Performance & Monitoring

| Metric | Target | Monitoring |
|--------|--------|-----------|
| Diagnostic solve time | <45s | Track in `ai_call_log.latency_ms` |
| Coach response latency | <10s | Track in `ai_call_log.latency_ms` |
| Page load time | <3s | Streamlit profiler |
| Database query time | <2s | Warehouse query logs |

---

## 10. Out of Scope

- Manager dashboards
- Multi-role support beyond RM
- Real-time collaboration
- Offline mode
- Mobile optimization
- Custom admin UI
