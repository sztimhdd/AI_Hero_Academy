# Technical Design Document (TDD)
## AI Hero Academy MVP

**Version**: 1.1
**Date**: February 2026
**Status**: In Development

---

## 1. Overview

AI Hero Academy is a Streamlit-based Databricks App that delivers personalized AI skills training to employees. It implements a four-stage learning loop: **Diagnose → Map Gaps → Train → Score & Track**.

The MVP launched with Relationship Manager (RM) and expanded to include Underwriter (UW), Analyst (AN), and Marketing/Comms Advisor (MK). All four roles are fully live. Each role has 18 diagnostic questions across 6 skill domains and 7 training courses (6 domain + 1 capstone).

UAT v2.0 (2026-03-06): 16 scenarios across 4 independent groups (A–D). Groups B/C/D can run standalone via `python scripts/reset_uat_user.py --profile {course-built|m1-done|all-done}` without running prior groups. Phase 12 (March 2026) extended the platform to a 6-domain architecture for future role content generation. All AI scoring, coaching, and gap analysis is powered by **Google Gemini API** (`gemini-2.0-flash`). All learner state is persisted in **Google Cloud Firestore** (GCP project `banded-totality-485901`). Static content (courses, diagnostic items, reading, scenarios, evaluations) is served from JSON files bundled with the app — no database queries needed for content.

---

## 2. Architecture

### 2.1 Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Frontend** | Streamlit (multi-page) | Local: port 8502; Phase C target: GCP Cloud Run |
| **Database** | Google Cloud Firestore | GCP project `banded-totality-485901`; flat top-level collections; credentials via service account key |
| **AI** | Google Gemini API (`gemini-2.0-flash`) | `google-genai` SDK; `GEMINI_API_KEY` env var; `call_llm()` signature unchanged |
| **State** | Firestore collections (flat, top-level) | `user_profiles`, `diagnostic_sessions`, `gap_maps`, `training_progress`, `coach_sessions`, `ai_call_log` |
| **Auth** | `GCP_USER_EMAIL` / `DEV_USER_EMAIL` env var | Phase C: GCP Identity-Aware Proxy header injection |
| **Hosting** | Local Streamlit / Phase C: GCP Cloud Run | `Dockerfile` + `cloudbuild.yaml` pending (Phase C) |

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
 │ Firestore    │ │ Gemini API      │ │ JSON file loader  │
 │ domain fns   │ │ google-genai    │ │                   │
 └──────┬──────┘ └──────┬──────────┘ └────┬──────────────┘
        │               │                  │
 ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼────────────┐
 │  Firestore  │  │ Gemini API  │  │  content/*.json   │
 │  GCP project│  │ gemini-2.0  │  │  (bundled with    │
 │  user_prof  │  │ -flash      │  │  app) roles,      │
 │  diag_sess  │  │             │  │  domains, courses │
 │  gap_maps   │  └─────────────┘  │  diagnostic items │
 │  train_prog │                   │  reading,         │
 │  coach_sess │                   │  scenarios,       │
 │  ai_call_log│                   │  eval items       │
 └─────────────┘                   └───────────────────┘
```

### 2.3 AI Model

All LLM calls go through `utils/ai.py`:`call_llm()`. The active model is Google Gemini via the `google-genai` SDK. The API key is injected via the `GEMINI_API_KEY` environment variable.

| Model | Use case |
|-------|----------|
| `gemini-2.0-flash` | **Default** — scoring, gap maps, coach responses, evaluation |

The `call_llm(messages, temperature, user_email, call_type) → str` signature is frozen — all callers (`score_diagnostic`, `coach_response`, `generate_gap_map`, `score_evaluation`, `generate_module_coach_note`) depend on it unchanged.

---

## 3. Data Schema

### 3.1 Design Principles

- **JSON strings over complex types**: Structured data (options, rubrics, responses, scores) is stored as plain JSON strings and parsed in Python. This keeps Firestore documents simple and avoids serialisation friction.
- **`user_email` as identity key**: `user_email` is used directly as the Firestore document ID in `user_profiles` and as the primary filter in all learner queries. No UUID layer needed for MVP.
- **Flat top-level collections**: All Firestore collections are top-level (not nested). `training_progress` docs use a composite key `{user_email}_{course_id}`. All compound queries use a single `where("user_email", "==", ...)` filter; additional filtering and sorting done in Python to avoid composite index requirements.

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
real_use_case    STRING,   -- source use case(s) from internal use case library
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
user_email      STRING NOT NULL PRIMARY KEY,   -- from GCP IAP / DEV_USER_EMAIL
display_name    STRING,
role_id         STRING NOT NULL,               -- legacy role selection; retained for existing users
lang            STRING DEFAULT 'en',           -- 'en' | 'zh'; Phase 15 (i18n)
intake_profile  STRING,                        -- JSON: {role_text, magic_wish, daily_tasks, ai_tools[]}; Phase 3
assembled_path  STRING,                        -- JSON: [atom_id, ...] ordered path; Phase 3
created_at      TIMESTAMP NOT NULL DEFAULT current_timestamp()
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

Seven rows created per user when they click "Build My Training Course" (6 domain courses + 1 capstone). Module 1 is immediately unlocked (`is_locked = false`). Modules 2–7 are unlocked sequentially as the prior module's evaluation is completed.

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
| `content/roles.json` | `{role_id: {...}}` | 5 roles (rm, uw, an, mk, pm) |
| `content/domains.json` | `{rm_responsible_ai: {...}, ...}` | 30 entries (6 per role × 5 roles); role-scoped top-level keys |
| `content/domains_universal.json` | `{responsible_ai: {an: {...}, mk: {...}, rm: {...}, uw: {...}}, ...}` | 6 domains × 4 role variants; Phase 0.7 |
| `content/diagnostic_items.json` | `[{item_id, role_id, domain_id, ...}]` | 90 items (18 per role × 5 roles); 3 per domain per role |
| `content/atomic_diagnostic_items.json` | `[{item_id, role_id, domain_id, ...}]` | 36 items; role-agnostic subset for Phase 3 diagnostic |
| `content/courses.json` | `{course_id: {...}}` | 35 courses (7 per role × 5 roles); keyed by `course_id` |
| `content/reading_content.json` | `{course_id: {...}}` | 35 entries (1 per course) |
| `content/reading_content_structured.json` | `{course_id: {concept_text_structured, ...}}` | 35 entries; generated by `scripts/enrich_reading_content.py`; optional fallback |
| `content/practice_scenarios.json` | `{course_id: {...}}` | 35 entries; includes `task_1_text`–`task_4_text` + `coach_system_prompt` + `task_modes` + `task_mcq_options` |
| `content/evaluation_items.json` | `{course_id: [{...}]}` | 35 × 4 = 140 items |
| `content/atomic_modules.json` | `[{atom_id, domain, capability_tags, reading, practice, ...}]` | 35 draft atoms (Phase 0.5); 1:1 with source courses; status="draft" |
| `content/atomic_modules_v2.json` | `[{atom_id, domain, capability_tags, reading, practice, merged_from, status, ...}]` | 15 canonical atoms (Phase 2); 5 universal + 10 role-variant; status="canonical"\|"role-variant" |
| `content/atomic_overlap_report.json` | `{merge_candidates: [{domain, source_course_ids, ...}]}` | 6 merge groups from Phase 0.5 overlap detection |
| `content/i18n/en.json` | `{key: string}` | UI strings (English); ~140 flat keys |
| `content/i18n/zh.json` | `{key: string}` | UI strings (Chinese); matching keys |

**`domains.json` key format**: top-level keys are role-scoped (`rm_responsible_ai`, `uw_responsible_ai`, `an_responsible_ai`, etc.); each entry has a `domain_id` field with the flat key (`responsible_ai`). `utils/content.py` exposes `get_domain(domain_id, role_id)` and `get_domain_descriptions(role_id)` that filter by `role_id` field value.

> **Phase 12 (March 2026):** All three roles (RM, UW, AN) use the 6-domain hexagon architecture: `responsible_ai`, `strategic_prompting`, `critical_eval`, `relationship_intel`, `data_decision`, `augmented_comm`. The legacy 4-domain model (`prompting`, `verification`, `data_safety`, `tool_fluency`) is no longer in active use.

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
def get_reading_structured(course_id: str) -> dict | None  # returns None if structured file absent
```

### 4.3 Content Generation Pipeline

UW content (and future role content) is generated by `scripts/generate_course_content.py` — an 8-stage multi-agent LLM pipeline that converts a Course Design Brief markdown document into all content JSON files. The pipeline does not require running notebooks or writing to Delta.

**Reading enrichment pipeline** (March 2026): `scripts/enrich_reading_content.py` is a post-generation enrichment step that calls Claude Haiku to extract structured sub-fields from the flat reading content. It reads `content/reading_content.json` and writes `content/reading_content_structured.json`. Run once after content generation (or any time reading content is updated):

```bash
# Enrich all items (4 concurrent workers)
python scripts/enrich_reading_content.py

# Single item / dry run
python scripts/enrich_reading_content.py --course-id rm_c1_responsible_ai --dry-run
```

The structured file is optional — the Reading sub-view falls back to flat-text rendering automatically if it is absent. The 4 extracted sub-fields per course are:

| Sub-field | Schema |
| --------- | ------ |
| `concept_text_structured` | `{framework_acronym, intro, cards: [{letter, title, body}], guardrails}` |
| `good_example_structured` | `{scenario, before_prompt, before_issue, after_prompt, after_benefit, outcome}` |
| `anti_pattern_structured` | `{headline, failure_scenario, chain: [str], root_lesson}` |
| `takeaway_structured` | `{statement, action_1: {title, body}, action_2: {title, body}}` |

### 4.4 Remaining Seeding (learner + system schemas only)

`notebooks/00_create_schemas.py` is still used to create `learner.*` and `system.*` Delta schemas on first deploy. It no longer creates `content.*` tables.

### 4.5 Verification (post-startup)

After deploying the app, verify content loaded correctly by checking:

```python
from utils.content import DIAGNOSTIC_ITEMS, COURSES, EVAL_ITEMS, ROLES
assert len(ROLES) == 4                             # rm + uw + an + mk
assert len(DIAGNOSTIC_ITEMS) == 72                 # 18 RM + 18 UW + 18 AN + 18 MK
assert len(COURSES) == 28                          # 7 RM + 7 UW + 7 AN + 7 MK
assert len(EVAL_ITEMS["rm_c1_responsible_ai"]) == 4  # 4 items per course
```

---

## 5. Application Architecture

### 5.1 File Structure

```
app.py                        # entry point; handles routing based on user state
pages/
  00_Welcome.py               # new user onboarding + role selection (Phase 3: intake form replaces role dropdown)
  01_Diagnostic.py            # 12-question diagnostic assessment (multi-role)
  02_Skills_Profile.py        # domain scores, gap map, assessment history
  03_Home.py                  # course progress dashboard (Phase 3: shows assembled atom path)
  04_Course_Module.py         # reading / practice / evaluation sub-views
utils/
  db.py                       # Firestore data layer; domain-specific functions (get_profile, save_diagnostic, update_profile_lang, etc.)
  ai.py                       # Gemini API calls via google-genai; writes to ai_call_log Firestore collection
  auth.py                     # extracts user_email from GCP_USER_EMAIL / DEV_USER_EMAIL env var
  content.py                  # JSON file loader; typed getters for all content + atomic loaders
  i18n.py                     # i18n module; t(key, lang) translation fn; SUPPORTED_LANGS; detect_browser_lang()
  scoring.py                  # MCQ scoring; rubric parsing; domain score calculation
  sequencing.py               # role-based module sequence algorithm (legacy; superseded by path_assembler in Phase 3)
  styles.py                   # inject_global_css(); render_sidebar() (lang toggle); section_header()
  path_assembler.py           # [Phase 3] atom path assembly: filter by tags → rank by gap → sequence
content/
  roles.json                  # {role_id: {...}} — rm + uw + an + mk + pm
  domains.json                # role-scoped keys (rm_responsible_ai, ...)
  domains_universal.json      # {domain_id: {role_id: {...}}} — 6 domains × 4 role variants (Phase 0.7)
  diagnostic_items.json       # list of 90 items (18 per role × 5 roles)
  atomic_diagnostic_items.json # list of 36 items for Phase 3 role-agnostic diagnostic
  courses.json                # {course_id: {...}} — 35 courses (7 per role × 5 roles)
  reading_content.json        # {course_id: {...}} — 35 entries
  reading_content_structured.json  # {course_id: {structured sub-fields}} — optional enrichment
  practice_scenarios.json     # {course_id: {...}} — 35 entries with task_modes + mcq_options
  evaluation_items.json       # {course_id: [{...}]} — 140 items (35 courses × 4)
  atomic_modules.json         # list of 35 draft atoms (Phase 0.5); status="draft"
  atomic_modules_v2.json      # list of 15 canonical atoms (Phase 2); status="canonical"|"role-variant"
  atomic_overlap_report.json  # 6 merge groups from overlap detection
  i18n/
    en.json                   # ~140 flat key-value UI string pairs (English)
    zh.json                   # matching keys with Chinese translations
scripts/
  generate_course_content.py  # multi-agent LLM pipeline for new role content
  atomize_coursework.py       # Phase 0.5: converts role-specific courses → draft atoms
  merge_atoms.py              # Phase 2: merges draft atoms → canonical v2 library
  ingest_pm_coursework.py     # Phase 1: ingests PM design doc → content JSON files
  enrich_reading_content.py   # enriches reading_content.json → structured sub-fields
  reset_uat_user.py           # reset UAT user; --profile {course-built|m1-done|all-done}
requirements.txt              # streamlit, google-genai, google-cloud-firestore, plotly, tenacity, ...
```

### 5.2 Auth: Extracting `user_email`

The user email is resolved from environment variables in priority order:

```python
# utils/auth.py
import os

def get_user_email() -> str:
    email = (
        os.environ.get("GCP_USER_EMAIL")           # Phase C: injected by Cloud Run / IAP
        or os.environ.get("DATABRICKS_USER_EMAIL") # legacy path (unused post-migration)
        or os.environ.get("DEV_USER_EMAIL", "dev@example.com")  # local development
    )
    return email
```

Never use hardcoded emails or require the user to type their email.

### 5.3 Router Logic (`app.py`)

On every page load, the app reads user state from Firestore and routes:

```python
import streamlit as st
from utils.auth import get_user_email
from utils.db import get_profile, get_latest_diagnostic, get_any_progress

def get_user_state(user_email: str) -> str:
    profile = get_profile(user_email)
    if not profile:
        return "new_user"

    session = get_latest_diagnostic(user_email)
    if not session:
        return "needs_diagnostic"

    progress = get_any_progress(user_email)
    if not progress:
        return "needs_course"
    return "in_training"
```

> **Note**: `get_latest_diagnostic()` returns only completed sessions (where `completed_at IS NOT NULL`). `get_any_progress()` is an existence check — returns the first `training_progress` doc for the user.
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
st.session_state["coach_messages_by_task"]  # dict {task_idx: [{role, content}]}; one list per task
st.session_state["mcq_answered_by_task"]    # dict {task_idx: chosen_label | None}; MCQ tasks only
st.session_state["practice_task_idx"]       # int: 0-3
st.session_state["practice_turns"]          # int: total turns used in this session
st.session_state["task_extra_{task_idx}"]   # int: number of 3-turn extensions granted (open tasks)

# i18n (Phase 15, March 2026)
st.session_state["lang"]                # str: "en" | "zh"; default "en"
st.session_state["_lang_from_profile"]  # bool sentinel: True once profile lang has been applied (avoids redundant Firestore reads)
```

### 5.5 Database Helper (`utils/db.py`)

All learner reads/writes go through domain-specific Firestore functions. There is no generic `execute()` / `query_one()` — each operation is a named function:

```python
# User profiles
get_profile(user_email) -> dict | None
create_profile(user_email, display_name, role_id, lang: str = "en") -> None  # lang written to Firestore profile
update_profile_lang(user_email, lang) -> None                                  # updates lang field; no-op for demo profiles

# Diagnostic sessions
get_latest_diagnostic(user_email) -> dict | None   # completed only, newest first
get_all_diagnostics(user_email) -> list[dict]
save_diagnostic(session_id, user_email, started_at, responses_json,
                item_scores_json, domain_scores_json, overall_score) -> None

# Gap maps
get_latest_gap_map(user_email) -> dict | None
save_gap_map(gap_map_id, user_email, source_type, source_id, bullets_json) -> None

# Training progress
get_all_progress(user_email) -> list[dict]          # sorted by module_sequence_order
get_progress(user_email, course_id) -> dict | None
get_progress_by_seq(user_email, seq) -> dict | None
get_any_progress(user_email) -> dict | None         # existence check
create_progress(user_email, course_id, seq, is_locked) -> None
update_progress(user_email, course_id, **fields) -> None
unlock_progress(user_email, seq) -> None

# Coach sessions
save_coach_session(session_id, user_email, course_id,
                   started_at, turn_count, conv_json) -> None
```

The module self-loads `.env` via `load_dotenv()` at import time and resolves `GOOGLE_APPLICATION_CREDENTIALS` from relative to absolute path on first call to `_get_db()`.

---

## 6. AI Call Workflows

### 6.1 LLM Helper (`utils/ai.py`)

```python
import os, time, uuid
from google import genai
from google.genai import types

_MODEL = "gemini-2.0-flash"

def call_llm(messages: list[dict], temperature: float = 0.1, user_email: str = None,
             call_type: str = "unknown") -> str:
    """
    messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
    Returns the assistant reply as a string.
    Writes one row to the Firestore ai_call_log collection.
    """
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    # Convert messages to google-genai Contents format
    # system message extracted separately; user/assistant messages form the history
    t0 = time.time()
    try:
        response = client.models.generate_content(
            model=_MODEL,
            contents=_to_contents(messages),
            config=types.GenerateContentConfig(temperature=temperature),
        )
        content = response.text
        latency = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, _MODEL, latency, success=True)
        return content
    except Exception as e:
        latency = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, _MODEL, latency, success=False, error=str(e))
        raise

def _log_call(user_email, call_type, model, latency_ms, success, error=None):
    try:
        from utils.db import _get_db
        from google.cloud.firestore import SERVER_TIMESTAMP
        _get_db().collection("ai_call_log").document(str(uuid.uuid4())).set({
            "user_email": user_email or "",
            "call_type": call_type,
            "model_endpoint": model,
            "latency_ms": latency_ms,
            "success": success,
            "error_message": str(error)[:500] if error else None,
            "called_at": SERVER_TIMESTAMP,
        })
    except Exception:
        pass  # never break the main flow on logging failures
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

**Message structure** (open tasks):
```python
task_msgs = st.session_state["coach_messages_by_task"].get(task_idx, [])
messages = [
    {"role": "system", "content": coach_system_prompt},
    *task_msgs,                            # prior turns for this task
    {"role": "user", "content": user_input},
]
```

**MCQ tasks** use the same `coach_response()` helper but the system prompt is extended at call time with an MCQ FEEDBACK MODE addendum. The learner's chosen label is passed as `user_input`. Response is capped at 2 sentences; no follow-up question is asked.

**Hard limits enforced in code (not in Delta)**:
- Open tasks: max 3 turns per task (extendable by 3 with "Continue" button); auto-advance at limit
- MCQ tasks: exactly 1 exchange; no turn limit needed
- Max 15 total turns across open tasks in the session; show "Go to Quiz" at limit

**Output**: Store reply in `st.session_state["coach_messages_by_task"][task_idx]`; increment `practice_turns`.

### 6.5 Evaluation Scoring

Same pattern as diagnostic scoring (§6.2). Uses `content.evaluation_items` rubrics. On completion:
1. Write `evaluation_score` and `evaluation_completed_at` to `learner.training_progress`
2. Write `domain_score_after` to `learner.training_progress`
3. Unlock next module (`UPDATE ... SET is_locked = false WHERE module_sequence_order = N+1`)
4. Trigger gap map generation (§6.3) with `source_type = 'evaluation'`

---

## 7. Module Sequencing Algorithm

Run once after the user clicks "Build My Training Course". Creates 7 rows in `learner.training_progress` (6 domain courses + 1 capstone).

```python
DOMAIN_TO_COURSE = {
    # All roles use the 6-domain hexagon model (Phase 12, March 2026).
    # Course IDs follow the pattern {role}_c{N}_{domain_slug}.
    "rm": {
        "responsible_ai":      "rm_c1_responsible_ai",
        "strategic_prompting": "rm_c2_strategic_prompting",
        "critical_eval":       "rm_c3_critical_eval",
        "relationship_intel":  "rm_c4_relationship_intel",
        "data_decision":       "rm_c5_data_decision",
        "augmented_comm":      "rm_c6_augmented_comm",
    },
    "uw": {
        "responsible_ai":      "uw_c1_responsible_ai",
        "strategic_prompting": "uw_c2_strategic_prompting",
        "critical_eval":       "uw_c3_critical_eval",
        "relationship_intel":  "uw_c4_relationship_intel",
        "data_decision":       "uw_c5_data_decision",
        "augmented_comm":      "uw_c6_augmented_comm",
    },
    "an": {
        "responsible_ai":      "an_c1_responsible_ai",
        "strategic_prompting": "an_c2_strategic_prompting",
        "critical_eval":       "an_c3_critical_eval",
        "relationship_intel":  "an_c4_relationship_intel",
        "data_decision":       "an_c5_data_decision",
        "augmented_comm":      "an_c6_augmented_comm",
    },
    "mk": {
        "responsible_ai":      "mk_c1_responsible_ai",
        "strategic_prompting": "mk_c2_strategic_prompting",
        "critical_eval":       "mk_c3_critical_eval",
        "relationship_intel":  "mk_c4_relationship_intel",
        "data_decision":       "mk_c5_data_decision",
        "augmented_comm":      "mk_c6_augmented_comm",
    },
}
CAPSTONE_COURSE_ID = {
    "rm": "rm_c7_capstone",
    "uw": "uw_c7_capstone",
    "an": "an_c7_capstone",
    "mk": "mk_c7_capstone",
}

def compute_module_sequence(domain_scores: dict, role_id: str = "rm") -> list[str]:
    """
    domain_scores: {"responsible_ai": 2.0, "strategic_prompting": 0.8, ...}
    role_id: "rm", "uw", "an", or "mk"
    Returns: list of course_ids in personalised order (index 0 = module 1).
    """
    domain_to_course = DOMAIN_TO_COURSE.get(role_id, DOMAIN_TO_COURSE["rm"])
    capstone = CAPSTONE_COURSE_ID.get(role_id, CAPSTONE_COURSE_ID["rm"])

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
    return sequence[:7]
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

### 10.1 Local development (current)

```bash
.venv/Scripts/pip install -r requirements.txt
# .env must contain GEMINI_API_KEY, GCP_PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS, DEV_USER_EMAIL
.venv/Scripts/streamlit run app.py --server.port 8502
```

Or via the UAT helper:

```bash
bash run_uat.sh   # sources .env, starts on port 8502 with LOCAL_UAT=true
```

### 10.2 Environment variables (`.env`)

```bash
GEMINI_API_KEY=<your-key>
GCP_PROJECT_ID=banded-totality-485901
GOOGLE_APPLICATION_CREDENTIALS=.gcp/banded-totality-485901-eb494951ebf7.json
LOCAL_UAT=true
DEV_USER_EMAIL=you@example.com
```

### 10.3 Cloud Run packaging (Phase C — pending)

Files to create:
- `Dockerfile` — Python 3.11-slim, install requirements, run Streamlit on port 8080
- `.dockerignore` — exclude `.venv/`, `__pycache__/`, `.env`, `*.pyc`
- `cloudbuild.yaml` — for automated GCP deployment

Files to remove: `app.yml`, `databricks.yml` (Databricks-specific — no longer needed).

Cloud Run environment variables:
- `GEMINI_API_KEY`
- `GCP_PROJECT_ID`
- `GCP_USER_EMAIL` (or rely on IAP header injection)

### 10.4 CI/CD (Phase D — pending)

Will use `gcloud run deploy` via GitHub Actions with `GEMINI_API_KEY` and GCP service account key stored as GitHub secrets.

---

## 11. Security & Access Control

| Concern | Approach |
|---------|---------|
| Authentication | `GCP_USER_EMAIL` env var (Phase C: IAP header); `DEV_USER_EMAIL` for local dev |
| Learner data isolation | Every Firestore query includes `where("user_email", "==", user_email)` |
| Content safety | All seeded content uses fictional companies and data only (per PRD §13.2) |
| AI logs | `ai_call_log` Firestore collection; write-only path in `_log_call()`; always wrapped in try/except |
| No secrets in code | `GEMINI_API_KEY`, `GCP_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS` injected via `.env` or Cloud Run env vars; `.env` in `.gitignore` |
| GCP credentials (local) | Service account key at `.gcp/` (gitignored); resolved to absolute path at runtime |
| GCP credentials (Phase C) | Workload Identity or service account key injected as Cloud Run secret |

---

## 12. Performance Targets

| Metric | Target | Measured via |
|--------|--------|-------------|
| Diagnostic scoring + gap map | < 45s end-to-end | `ai_call_log.latency_ms` |
| Coach response per turn | < 10s | `ai_call_log.latency_ms` |
| Evaluation scoring + gap map | < 30s | `ai_call_log.latency_ms` |
| Page load (Firestore reads) | < 3s | `ai_call_log.latency_ms` / browser timing |
| Firestore reads per page load | ≤ 3 | Code review |

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

**Multi-role status (updated March 2026):** Four roles are complete — Relationship Manager (RM), Underwriter (UW), Analyst (AN), and Marketing/Comms Advisor (MK). All four roles are fully live with content generated, loaded, and Welcome page role selection wired. UAT smoke tests (UAT-17) passed for MK in March 2026.
