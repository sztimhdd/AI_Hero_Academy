# PLAN.md — AI Hero Academy MVP
**Next Steps Implementation Plan**
Based on: PRD.md, TDD.md, Issues.md
Date: February 2026

---

## Part 1 — Feature Implementation Status

Complete inventory of every PRD/TDD requirement and its current implementation state.

### Legend
| Symbol | Meaning |
|--------|---------|
| ✅ | Implemented and correct |
| ⚠️ | Implemented but has known bug (see Issues.md) |
| ❌ | Not implemented |

---

### App Shell & Routing

| Requirement | PRD Ref | Status | Notes |
|-------------|---------|--------|-------|
| Multi-page Streamlit app | §4.2 | ✅ | 5 pages + app.py entry point |
| SSO auth via `DATABRICKS_USER_EMAIL` | §13.4, TDD §5.2 | ✅ | `utils/auth.py` correct |
| State-based routing on every page load | §6.1 | ✅ | `app.py` routes new_user / needs_diagnostic / needs_course / in_training |
| Page guards on each page | §6.3 | ✅ | All pages guard-redirect to correct prior state |
| Welcome guard routes to correct state | §6.3 | ✅ | Fixed L6: full state detection (needs_diagnostic / needs_course / in_training) |
| Dark theme design system | §7 | ✅ | `utils/styles.py` — full CSS system |
| Responsive layout (desktop-first) | §5.2 | ✅ | `max-width: 900px` block container |

---

### Welcome Screen (00_Welcome.py)

| Requirement | PRD §7.1 | Status | Notes |
|-------------|----------|--------|-------|
| App logo and brand mark | §7.1 | ✅ | |
| Tagline and value proposition text | §7.1 | ✅ | |
| Role selector dropdown (single: RM) | §7.1 | ✅ | |
| CTA disabled until role selected | §7.1 | ✅ | |
| Profile creation on CTA click | §7.1 | ✅ | Uses inline SQL + `escape()` (M2 issue) |
| Navigate to Diagnostic after profile creation | §7.1 | ✅ | |
| Guard: redirect if profile already exists | §7.1 | ✅ | Fixed L6: routes to correct state based on user journey |

---

### Diagnostic Screen (01_Diagnostic.py)

| Requirement | PRD §7.2 | Status | Notes |
|-------------|----------|--------|-------|
| Question counter "X of 12" | §7.2 | ✅ | |
| Domain label per question | §7.2 | ✅ | |
| Progress bar | §7.2 | ✅ | |
| MCQ item rendering with radio buttons | §7.2 | ✅ | |
| Prompt sandbox item rendering | §7.2 | ✅ | |
| Micro-task item rendering | §7.2 | ✅ | |
| No back navigation | §7.2 | ✅ | |
| No partial saves; restart from Q1 on refresh | §7.2, TDD §9 | ✅ | |
| AI scoring after Q12 with loading state | §7.2 | ✅ | Fixed H2: MCQ scored locally; only open-ended items sent to LLM |
| Gap map generation after scoring | §7.2 | ✅ | `generate_gap_map()` called with correct params |
| Results written to `diagnostic_sessions` | TDD §3.3 | ✅ | Fixed M2: parameterized INSERT; Fixed M3: `started_at` captured at session init |
| Gap map written to `gap_maps` | TDD §3.3 | ✅ | |
| Redirect to Skills Profile after completion | §7.2 | ✅ | |
| Graceful error on AI failure | TDD §9 | ✅ | |

---

### Skills Profile Screen (02_Skills_Profile.py)

| Requirement | PRD §7.3 | Status | Notes |
|-------------|----------|--------|-------|
| Overall score and level label | §7.3 | ✅ | Fixed H1: equal-weight domain score computation |
| 4 domain score bars with color coding | §7.3 | ✅ | danger/warning/success thresholds correct |
| Gap map narrative bullets (priority ordered) | §7.3 | ✅ | |
| Gap map dot colors (red/yellow/green) | §7.3 | ✅ | |
| Assessment history table | §7.3 | ✅ | All diagnostic sessions shown |
| "Last assessed" date | §7.3 | ✅ | |
| "Retake Diagnostic" button | §7.3 | ✅ | Clears diagnostic session state |
| "Build My Training Course" (if no course) | §7.3 | ✅ | Calls `compute_module_sequence()` |
| "View My Course" (if course exists) | §7.3 | ✅ | Navigates to Home |
| Domain scores incorporate evaluation scores | §7.3 | ✅ | Fixed H1: `compute_current_domain_scores()` in `utils/scoring.py` |
| Uses `domain_score_after` per module | TDD §3.3 | ✅ | Fixed H1: equal-weight per-item aggregation |

---

### Home Screen (03_Home.py)

| Requirement | PRD §7.4 | Status | Notes |
|-------------|----------|--------|-------|
| "Welcome back, [display_name]" greeting | §7.4 | ✅ | |
| Overall score summary card | §7.4 | ✅ | Fixed H1: uses `compute_current_domain_scores()` |
| Trend indicator (up/right/down arrow) | §7.4 | ✅ | Fixed 4.1: ↑/→/↓ vs diagnostic baseline, shown inline with score |
| Last updated date in summary card | §7.4 | ✅ | Fixed 4.2: max(diagnostic completed_at, evaluation_completed_at) |
| "View Full Profile" link | §7.4 | ✅ | Fixed L5: dead HTML anchor removed; uses Streamlit button only |
| 5 module cards | §7.4 | ✅ | |
| Completed module: checkmarks + score | §7.4 | ✅ | |
| In-progress module: sub-badges + CTA | §7.4 | ✅ | |
| Locked module: lock icon + greyed styling | §7.4 | ✅ | |
| "Continue" button resumes correct sub-module | §7.4 | ✅ | reading → practice → evaluation state machine |
| "Review Module" button for completed modules | §7.4 | ✅ | Sets `active_submodule = "overview"` |

---

### Course Module Screen (04_Course_Module.py)

#### Overview Sub-view

| Requirement | PRD §7.5.1 | Status | Notes |
|-------------|------------|--------|-------|
| Module number and title | §7.5.1 | ✅ | |
| Module tagline | §7.5.1 | ✅ | |
| 3-step progress strip (Read/Practice/Quiz) | §7.5.1 | ✅ | |
| Context-aware CTA | §7.5.1 | ✅ | Start Reading / Continue Practice / Take Quiz / Review Results |

#### Reading Sub-view

| Requirement | PRD §7.5.2 | Status | Notes |
|-------------|------------|--------|-------|
| Concept section | §7.5.2 | ✅ | |
| Good Example box | §7.5.2 | ✅ | |
| Common Mistake (anti-pattern) box | §7.5.2 | ✅ | |
| Key Takeaway box | §7.5.2 | ✅ | |
| "I've read this — Start Practice" CTA | §7.5.2 | ✅ | |
| `reading_completed_at` written on CTA click | §7.5.2, TDD §3.3 | ✅ | Fixed L2: UPDATE guarded by `WHERE reading_completed_at IS NULL` |

#### Practice Sub-view (AI Coach)

| Requirement | PRD §7.5.3 | Status | Notes |
|-------------|------------|--------|-------|
| Scenario panel (always visible) | §7.5.3 | ✅ | |
| Task indicator "Task X of 4" | §7.5.3 | ✅ | |
| Task instruction text | §7.5.3 | ✅ | |
| Text input + "Send to Coach" button | §7.5.3 | ✅ | |
| AI Coach response display | §7.5.3 | ✅ | Chat bubble styling |
| Turn counter "Turn X of 15" | §7.5.3 | ✅ | |
| Max 3 turns per task → "Next Task" | §7.5.3, TDD §6.4 | ✅ | `MAX_TASK_TURNS = 3` |
| Max 15 total turns → "Go to Quiz" | §7.5.3, TDD §6.4 | ✅ | `MAX_TOTAL_TURNS = 15` |
| "Next Task" after coach reply | §7.5.3 | ✅ | |
| "Complete Practice" after all 4 tasks | §7.5.3 | ✅ | |
| "Skip" task option | §7.5.3 | ✅ | |
| "Complete Practice Early" option | §7.5.3 | ✅ | |
| Coach session written to `coach_sessions` | TDD §3.3 | ✅ | Fixed M2: parameterized INSERT; Fixed M3: `practice_started_at` stored in session state |
| `practice_completed_at` written on complete | TDD §3.3 | ✅ | Uses parameterized UPDATE |
| Conversation lost on refresh (acceptable) | TDD §9 | ✅ | In-memory only; no partial saves |
| Coach system prompt from `practice_scenarios` | TDD §6.4 | ✅ | |
| Graceful error on AI failure | TDD §9 | ✅ | |

#### Evaluation Sub-view

| Requirement | PRD §7.5.4 | Status | Notes |
|-------------|------------|--------|-------|
| Question counter "X of 4" | §7.5.4 | ✅ | |
| Progress bar | §7.5.4 | ✅ | |
| MCQ rendering (questions 1–3) | §7.5.4 | ✅ | |
| Performance task rendering (question 4) | §7.5.4 | ✅ | |
| No back navigation | §7.5.4 | ✅ | |
| "Scoring your responses..." loading state | §7.5.4 | ✅ | |
| AI evaluation scoring | §7.5.4 | ✅ | Fixed H2+H3: MCQ scored locally; Python computes aggregates (not LLM) |
| `evaluation_score` written to `training_progress` | TDD §3.3 | ✅ | Fixed M2: parameterized write |
| `domain_score_after` written | TDD §3.3 | ✅ | Fixed H3: computed in Python, not by LLM |
| `evaluation_completed_at` written | TDD §3.3 | ✅ | |
| Next module unlocked | TDD §6.5 | ✅ | `UPDATE ... SET is_locked = false WHERE module_sequence_order = N+1` |
| Gap map updated after evaluation | TDD §6.5 | ✅ | Fixed M5: uses full merged domain scores via `compute_current_domain_scores()` |
| Graceful error; no progress loss on retry | TDD §9 | ✅ | |

#### Results Sub-view

| Requirement | PRD §7.5.5 | Status | Notes |
|-------------|------------|--------|-------|
| Module score "X.X / 4.0" display | §7.5.5 | ✅ | |
| Per-domain score breakdown | §7.5.5 | ✅ | Shows primary domain score bar |
| AI-generated coach note | §7.5.5 | ✅ | `generate_module_coach_note()` |
| "Your skills profile has been updated" text | §7.5.5 | ✅ | |
| "View Updated Skills Profile" CTA | §7.5.5 | ✅ | |
| "Start Module N+1" CTA | §7.5.5 | ✅ | |
| "View Final Skills Profile" when all complete | §7.5.5 | ✅ | |
| Results fallback when session state lost | TDD §9 | ✅ | Fixed M4+L4: reads `domain_score_after` from cached `progress` (no extra DB call) |

---

### Scoring Engine (utils/)

| Requirement | TDD §8 | Status | Notes |
|-------------|--------|--------|-------|
| MCQ: deterministic score from rubric | §8 | ✅ | Fixed H2: `score_mcq()` called in `_score_batch()`; MCQ never sent to LLM |
| Open-ended: AI scores each criterion, scales to 0–4 | §8 | ✅ | Correct rubric format |
| Domain score: equal-weight average of all items | §8 | ✅ | Fixed H1: `compute_current_domain_scores()` in `utils/scoring.py` |
| Overall score: average of 4 domain scores | §8 | ✅ | `calculate_overall_score()` correct |
| Level labels (5 tiers) | §8 | ✅ | Fixed L3: Unaware threshold extended to cover 0.0–0.49 |
| `get_score_color()` thresholds | §8 | ✅ | |

---

### Module Sequencing (utils/sequencing.py)

| Requirement | PRD §10, TDD §7 | Status | Notes |
|-------------|-----------------|--------|-------|
| Quick-win first (1.5–2.5, closest to 2.0) | §10 | ✅ | |
| Gaps next (below 1.5, ascending) | §10 | ✅ | |
| Remaining domains | §10 | ✅ | |
| Strong last (above 2.5, ascending) | §10 | ✅ | |
| Capstone always module 5 | §10 | ✅ | `sequence.append(CAPSTONE_COURSE_ID)` |
| 5 rows inserted in `training_progress` | TDD §3.3 | ✅ | Module 1 unlocked; 2–5 locked |

---

### Content Seeding (notebooks/)

| Notebook | Status | Notes |
|----------|--------|-------|
| `00_create_schemas.py` | ✅ Complete | Registered as `seed_00_create_schemas`; targets `mdlg_ai_shared`; fixed `# MAGIC %md ##` silent execution bug |
| `01_seed_roles_domains.py` | ✅ Complete → Retiring | Fixed `# MAGIC %md ##` bug (roles and domains were silently skipped); now seeds correctly to `mdlg_ai_shared` |
| `02_seed_courses.py` | ✅ Complete → Retiring | Targets `mdlg_ai_shared`; courses=5, reading=5, practice=5, eval_items=20 confirmed |
| `03_seed_diagnostic_items.py` | ✅ Complete → Retiring | Targets `mdlg_ai_shared`; diagnostic_items=12 confirmed |

**Catalog migration completed (Feb 2026):** All content seeded to `mdlg_ai_shared`. Old `mdlg_ai.content`, `mdlg_ai.learner`, `mdlg_ai.system` schemas dropped. App service principal (`9f2c56cc-8b4a-4904-8729-0698a7c67b01`) granted all required UC privileges on `mdlg_ai_shared`.

---

### PRD Requirements Status — All Implemented ✅

All PRD requirements are now implemented. Previously pending items were resolved in Phases 4 and 5:

| Feature | PRD Ref | Fixed In |
|---------|---------|----------|
| Trend indicator (↑/→/↓) on Home summary card | §7.4 | Phase 4 Task 4.1 |
| "Last updated date" on Home summary card | §7.4 | Phase 4 Task 4.2 |
| Functional "View Full Profile" link (not dead anchor) | §7.4 | Phase 5 Task L5 |

---

## Part 2 — Implementation Plan

---

### Phase 0 — Infrastructure & Catalog Migration ✅ COMPLETE

All tasks below were completed across Sessions 1 and 2.

**Session 1 — Bug Fixes**
- ✅ H1: Equal-weight domain score computation (`compute_current_domain_scores()` in `utils/scoring.py`)
- ✅ H2: MCQ local scoring — `score_mcq()` called in `_score_batch()`; MCQ items never sent to LLM
- ✅ H3: Evaluation aggregates computed in Python, not by LLM
- ✅ L2: `reading_completed_at` overwrite prevented (`WHERE reading_completed_at IS NULL`)
- ✅ L3: Level label gap fixed — Unaware threshold covers 0.0–0.49
- ✅ L5: Dead "View Full Profile" HTML anchor removed; Streamlit button used
- ✅ L6: Welcome guard routing fixed — detects full user state (needs_diagnostic / needs_course / in_training)
- ✅ L7: (additional fix applied in session 1)
- ✅ M2: Learner writes parameterized (evaluation_score, domain_score_after)
- ✅ M5: Gap map after evaluation uses full merged domain scores

**Session 2 — Catalog Migration**
- ✅ All 12 source files migrated from `mdlg_ai` to `mdlg_ai_shared` default
- ✅ Fixed `# MAGIC %md ##` silent execution bug in `00_create_schemas.py` and `01_seed_roles_domains.py`
- ✅ Schemas and 12 tables created in `mdlg_ai_shared`
- ✅ All 4 seeding jobs run against `mdlg_ai_shared`: roles=1, domains=4, courses=5, reading=5, practice=5, eval_items=20, diag_items=12
- ✅ Old `mdlg_ai.content/learner/system` schemas dropped (CASCADE)
- ✅ App redeployed to Databricks Apps (status: SUCCEEDED)
- ✅ App service principal (`9f2c56cc-8b4a-4904-8729-0698a7c67b01`) granted all UC privileges on `mdlg_ai_shared`: `USE CATALOG`, `USE SCHEMA` × 3, `SELECT` × 7 content tables, `SELECT+MODIFY` × 6 write tables
- ✅ `databricks.yml` updated: seed_01/02/03 jobs removed (only `seed_00_create_schemas` remains)

---

### Phase 1 — Content DB → JSON Refactor

Move all 7 `content` schema tables to JSON files bundled with the app. The app never writes to these tables; this eliminates warehouse round-trips for static data, removes the seeding pipeline for content updates, and simplifies future edits to file changes only.

---

#### Code Review: Full Implication Analysis

The following were identified by reading every affected file before planning.

##### Implication 1 — CRITICAL: `json.loads()` on fields that become native Python types

**File**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

In the DB, `options` and `scoring_rubric` are stored as JSON *strings*, so the app calls `json.loads()`. After moving to JSON files, these fields are native Python dict/list — `json.loads()` on a dict raises `TypeError`.

Two locations in `01_Diagnostic.py` use raw `json.loads()` directly:

| Location | Current code | Problem |
|----------|-------------|---------|
| ~line 113 | `rubric = json.loads(item["scoring_rubric"]) if item["scoring_rubric"] else {}` | Breaks when already a dict |
| ~line 226 | `options = json.loads(item["options"]) if item["options"] else []` | Breaks when already a list |

**Fix**: Replace with `parse_rubric()` and `parse_options()` from `utils/scoring.py` — these already handle both string and dict/list inputs. `04_Course_Module.py` already uses these helpers throughout and needs no change.

##### Implication 2 — Three JOIN queries must become Python dict enrichment

**Files**: [pages/03_Home.py](pages/03_Home.py), [pages/04_Course_Module.py](pages/04_Course_Module.py)

Three functions JOIN `learner.training_progress` with `content.courses`. Each becomes: query `training_progress` from Delta only, then enrich rows via `get_course(row["course_id"])`.

| Function | Location | Change |
|----------|----------|--------|
| Home dashboard query | `03_Home.py:~49` | Remove JOIN; add Python enrichment loop |
| `load_all_progress()` | `04_Course_Module.py:120` | Remove JOIN; add Python enrichment loop |
| `load_next_module_title()` | `04_Course_Module.py:131` | Remove JOIN; look up `course["title"]` from dict |

**`primary_domain` downstream impact**: Every consumer reads `row["primary_domain"]` which currently comes from the JOIN. After refactor, the enrichment loop must explicitly set `row["primary_domain"] = course.get("primary_domain", "")`. Affected:
- `03_Home.py` `eval_domain_scores_home` loop
- `04_Course_Module.py` Results sub-view (`load_all_progress()` rows)

##### Implication 3 — `load_eval_domain_scores()` in 02_Skills_Profile.py: unparameterized IN clause removed

**File**: [pages/02_Skills_Profile.py](pages/02_Skills_Profile.py)

Currently builds SQL with inline string-interpolation of `course_id` values — a latent SQL injection risk. After refactor this entire query disappears; replaced by `get_course(cid)["primary_domain"]` dict lookup.

##### Implication 4 — `domain_descriptions` for `generate_gap_map()` must come from JSON module

**Files**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py), [pages/04_Course_Module.py](pages/04_Course_Module.py)

Both pages pass `domain_descriptions=domain_descs` to `generate_gap_map()`. This dict (`{domain_id: description}`) currently comes from `SELECT domain_id, description FROM content.domains WHERE role_id = 'rm'`.

After refactor, `utils/content.py` must export:
```python
DOMAIN_DESCRIPTIONS: dict[str, str]  # built from DOMAINS at module load
```
Both pages replace their DB call with `from utils.content import DOMAIN_DESCRIPTIONS`.

##### Implication 5 — `@st.cache_data` decorators on content loaders become misleading

**Files**: [pages/04_Course_Module.py](pages/04_Course_Module.py), [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

Five loaders in `04_Course_Module.py` and two in `01_Diagnostic.py` use `@st.cache_data(ttl=300/600)`. After refactor these functions return from module-level Python dicts with zero I/O. The decorator is harmless but implies a DB call that no longer exists — remove it.

Python's `sys.modules` cache ensures `utils.content` is loaded once per container process and shared across all sessions. No explicit caching needed.

##### Implication 6 — `options` and `scoring_rubric` stored as native JSON in files

In the DB these fields are JSON-encoded strings. In JSON files they will be native arrays/objects — directly human-readable and editable, which is the point of moving to files.

Fields that are `null` in some DB rows (`scenario_text`, `options`, `correct_option`, `explanation` on performance tasks) must be `null` in JSON files. App code already handles them with `item.get("field") or default` — no change needed.

##### Implication 7 — `content_id` and `scenario_id` are unused DB PKs

`reading_content.content_id` (format: `rc_{course_id}`) and `practice_scenarios.scenario_id` (format: `ps_{course_id}`) are never read by the app — all queries filter by `course_id`. These can be omitted from JSON files.

##### Implication 8 — `00_create_schemas.py` content DDL must be removed

**File**: [notebooks/00_create_schemas.py](notebooks/00_create_schemas.py)

Lines 22–150 create the `content` schema and 7 tables. After refactor:
- Change `["content", "learner", "system"]` → `["learner", "system"]` in the schema loop
- Delete all 7 content `CREATE TABLE` blocks

Do **not** DROP the `content` schema — it still exists in the DB from the catalog migration and is harmless.

##### Implication 9 — Content load failure changes from runtime to startup

Currently a missing or broken DB query shows `st.error(...)` at page render time. After refactor, a missing JSON file raises an exception at Python module import time — the Streamlit app fails to start.

`utils/content.py` must wrap file loading in a `try/except` that raises a descriptive `RuntimeError` (e.g., `"Missing content/courses.json"`). This surfaces cleanly in app startup logs and is easier to diagnose than a silent runtime failure.

##### Implication 10 — Course 3 title has SQL-escaped apostrophe

In the seeding notebook: `'The C3 Line: What Goes Into AI and What Doesn''t'` (double-apostrophe for SQL). In the JSON file this is simply `"The C3 Line: What Goes Into AI and What Doesn't"`. Extract carefully when writing JSON files.

##### Implication 11 — Phase 2 Task 2.3 depends on Phase 1 being complete

Task 2.3 (H1 equal-weight domain scores) reads `row["primary_domain"]` from `progress_rows`. This field only exists after Phase 1's enrichment loop is in place. Do not attempt Task 2.3 before Phase 1 is deployed.

---

#### Task 1.1 — Create `utils/content.py`

**New file**: `utils/content.py`

Loads all 7 JSON files at module import time. Exposes module-level dicts and typed getters.

Interface:
```python
ROLES: dict[str, dict]               # keyed by role_id
DOMAINS: dict[str, dict]             # keyed by domain_id
DIAGNOSTIC_ITEMS: list[dict]         # ordered by display_order
COURSES: dict[str, dict]             # keyed by course_id
READING: dict[str, dict]             # keyed by course_id
SCENARIOS: dict[str, dict]           # keyed by course_id
EVAL_ITEMS: dict[str, list[dict]]    # keyed by course_id, sorted by sequence
DOMAIN_DESCRIPTIONS: dict[str, str]  # {domain_id: description} for generate_gap_map()

def get_course(course_id: str) -> dict | None
def get_domain(domain_id: str) -> dict | None
def get_diagnostic_items() -> list[dict]
def get_reading(course_id: str) -> dict | None
def get_scenario(course_id: str) -> dict | None
def get_eval_items(course_id: str) -> list[dict]
```

JSON files are at `content/` in the project root. Load relative to `utils/content.py` using `pathlib.Path(__file__).parent.parent / "content"`.

---

#### Task 1.2 — Create 7 JSON files in `content/`

Extract data verbatim from seeding notebooks. Store `options` and `scoring_rubric` as native JSON (arrays/objects), not as strings.

| File | Source | Key | Count |
|------|--------|-----|-------|
| `content/roles.json` | `01_seed_roles_domains.py` | `role_id` | 1 |
| `content/domains.json` | `01_seed_roles_domains.py` | `domain_id` | 4 |
| `content/diagnostic_items.json` | `03_seed_diagnostic_items.py` | list (by `display_order`) | 12 |
| `content/courses.json` | `02_seed_courses.py` | `course_id` | 5 |
| `content/reading_content.json` | `02_seed_courses.py` | `course_id` | 5; omit `content_id` |
| `content/practice_scenarios.json` | `02_seed_courses.py` | `course_id` | 5; omit `scenario_id`; keep `task_1_text`..`task_4_text` as flat fields |
| `content/evaluation_items.json` | `02_seed_courses.py` | `course_id` → list | 5 × 4; `null` for N/A fields on performance tasks |

`diagnostic_items.json` is a list (not a keyed dict) because the diagnostic page iterates items in `display_order` and accesses them by index.

---

#### Task 1.3 — Update pages/01_Diagnostic.py

**File**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

1. Add `from utils.content import get_diagnostic_items, DOMAIN_DESCRIPTIONS`
2. Remove `load_items()` and `load_domain_descriptions()` (both DB query functions with `@st.cache_data`)
3. Replace calls: `items = load_items()` → `items = get_diagnostic_items()`, `domain_descriptions = load_domain_descriptions()` → `domain_descriptions = DOMAIN_DESCRIPTIONS`
4. **Patch (Implication 1)**: Replace `json.loads(item["scoring_rubric"])` → `parse_rubric(item.get("scoring_rubric") or "{}")`
5. **Patch (Implication 1)**: Replace `json.loads(item["options"])` → `parse_options(item.get("options") or "[]")`

---

#### Task 1.4 — Update pages/02_Skills_Profile.py

**File**: [pages/02_Skills_Profile.py](pages/02_Skills_Profile.py)

1. Add `from utils.content import get_course`
2. Remove `load_eval_domain_scores()` (the unparameterized IN-clause query)
3. Replace its usage with Python dict lookups over already-loaded `progress_rows`:
   ```python
   for row in progress_rows:
       if row.get("evaluation_completed_at") and row.get("domain_score_after") is not None:
           course = get_course(row["course_id"])
           domain = course["primary_domain"] if course else None
   ```

---

#### Task 1.5 — Update pages/03_Home.py

**File**: [pages/03_Home.py](pages/03_Home.py)

1. Add `from utils.content import get_course`
2. Replace the JOIN query with a `training_progress`-only query, then enrich rows:
   ```python
   rows = execute(f"SELECT * FROM {CATALOG}.learner.training_progress WHERE user_email = ? ORDER BY module_sequence_order", [user_email])
   for row in rows:
       course = get_course(row["course_id"]) or {}
       row["course_title"] = course.get("title", "")
       row["primary_domain"] = course.get("primary_domain", "")
   ```
3. Verify `eval_domain_scores_home` loop reads `row.get("primary_domain")` correctly after enrichment

---

#### Task 1.6 — Update pages/04_Course_Module.py

**File**: [pages/04_Course_Module.py](pages/04_Course_Module.py)

1. Add `from utils.content import get_course, get_reading, get_scenario, get_eval_items, DOMAIN_DESCRIPTIONS`
2. Remove `@st.cache_data` from `load_course`, `load_reading`, `load_scenario`, `load_eval_items`, `load_domain_descriptions`; rewrite each to delegate to content getters
3. Rewrite `load_all_progress()` — remove JOIN, enrich rows:
   ```python
   def load_all_progress() -> list:
       rows = execute(
           f"SELECT course_id, module_sequence_order, is_locked, evaluation_completed_at "
           f"FROM {CATALOG}.learner.training_progress WHERE user_email = ? ORDER BY module_sequence_order",
           [user_email],
       )
       for row in rows:
           course = get_course(row["course_id"]) or {}
           row["primary_domain"] = course.get("primary_domain", "")
           row["title"] = course.get("title", "")
       return rows
   ```
4. Rewrite `load_next_module_title()` — remove JOIN:
   ```python
   def load_next_module_title(current_seq: int):
       nxt = query_one(
           f"SELECT course_id FROM {CATALOG}.learner.training_progress "
           f"WHERE user_email = ? AND module_sequence_order = ?",
           [user_email, current_seq + 1],
       )
       if not nxt:
           return None
       course = get_course(nxt["course_id"])
       return course["title"] if course else None
   ```
5. Replace `domain_descs` (DB query) with `DOMAIN_DESCRIPTIONS` from content module

---

#### Task 1.7 — Update notebooks/00_create_schemas.py

**File**: [notebooks/00_create_schemas.py](notebooks/00_create_schemas.py)

1. Line 22: `["content", "learner", "system"]` → `["learner", "system"]`
2. Delete lines 27–150 (all 7 content `CREATE TABLE` blocks)
3. Learner and system DDL unchanged

Do not DROP `content` schema — tables remain in DB as harmless orphans.

---

#### Task 1.8 — Update databricks.yml ✅ DONE

**File**: [databricks.yml](databricks.yml)

Removed 3 job entries: `seed_01_roles_domains`, `seed_02_courses`, `seed_03_diagnostic_items`.
Kept: `seed_00_create_schemas`. Comment updated: "Content is now served from JSON files in content/ (no seeding required)."

---

#### Task 1.9 — Archive seeding notebooks

Review notebooks one final time to confirm all content is captured in JSON files, then move to `_archive/` or delete:
- `notebooks/01_seed_roles_domains.py`
- `notebooks/02_seed_courses.py`
- `notebooks/03_seed_diagnostic_items.py`

---

#### Phase 1 Execution Order

```
1.1  Create utils/content.py (loader + getters)
1.2  Create all 7 JSON files in content/
     → Verify: import utils.content succeeds; counts match
1.3  Update pages/01_Diagnostic.py (+ json.loads patches)
1.4  Update pages/02_Skills_Profile.py
1.5  Update pages/03_Home.py   ← highest structural risk; test JOIN replacement
1.6  Update pages/04_Course_Module.py  ← largest file; test all 5 sub-views
1.7  Update notebooks/00_create_schemas.py
1.8  Update databricks.yml
1.9  Archive seeding notebooks
     → Deploy and run Phase 1 acceptance tests
```

---

#### Phase 1 Acceptance Checks

- [ ] `from utils.content import get_course, get_diagnostic_items` succeeds
- [ ] `len(DIAGNOSTIC_ITEMS) == 12`, `len(COURSES) == 5`, `len(EVAL_ITEMS["rm_c1_prompting"]) == 4`
- [ ] Diagnostic page renders all 12 questions; MCQ options display correctly (list input to `parse_options()`)
- [ ] MCQ `scoring_rubric` is passed as dict to `_score_batch()` without `json.loads()` error
- [ ] Home page shows correct course titles and domain labels (JOIN replacement verified)
- [ ] Course Module sidebar shows correct titles for all 5 modules
- [ ] Next module CTA on Results page shows correct next module title
- [ ] `generate_gap_map()` receives correct `domain_descriptions` dict from content module
- [ ] `load_all_progress()` rows have `primary_domain` populated from JSON enrichment

---

### Phase 2 — High Priority Bug Fixes

#### Task 2.1 — Fix H2: MCQ local scoring (bypass LLM for MCQ items)

**Files to change**: [utils/ai.py](utils/ai.py)

**Note**: `_score_batch()` already has MCQ local scoring implemented. Verify it is wired correctly in `score_diagnostic()` and `score_evaluation()`. If already working, mark done after verification.

**Approach**: In `_score_batch()`, pre-filter MCQ items, score them locally with `score_mcq()`, and only send open-ended items to the LLM:

```python
from utils.scoring import score_mcq

local_scores = {}
llm_items = []
for item in items:
    if item.get("item_type") == "mcq":
        rubric = item.get("scoring_rubric") or {"correct": 4, "incorrect": 0}
        local_scores[item["item_id"]] = score_mcq(
            item.get("response", ""),
            item.get("correct_option"),
            rubric,
        )
    else:
        llm_items.append(item)

if not llm_items:
    return local_scores

llm_scores = _call_llm_for_batch(llm_items, ...)
return {**local_scores, **llm_scores}
```

---

#### Task 2.2 — Fix H3: Move aggregate computation out of LLM in `score_evaluation`

**File**: [utils/ai.py](utils/ai.py)

**Note**: `score_evaluation()` already mirrors `score_diagnostic()` with Python aggregation. Verify the prompt returns only `item_scores` and that aggregation happens in Python. If already correct, mark done after verification.

The evaluation prompt must return only:
```json
{"item_scores": {"item_id": score_float, ...}}
```
Python then computes domain and overall scores — not the LLM.

---

#### Task 2.3 — Fix H1: Equal-weight domain score computation

**Files**: [pages/02_Skills_Profile.py](pages/02_Skills_Profile.py), [pages/03_Home.py](pages/03_Home.py)

**Prerequisite**: Phase 1 complete (needs `primary_domain` from JSON enrichment in `progress_rows`).

Replace the "average of averages" logic with equal-weight per-item computation. Extract into `utils/scoring.py`:

```python
def compute_current_domain_scores(diag_domain_scores: dict, progress_rows: list) -> dict:
    DIAG_ITEMS_PER_DOMAIN = 3
    EVAL_ITEMS_PER_MODULE = 4
    domain_buckets = {d: {"sum": 0.0, "count": 0} for d in DOMAIN_IDS}

    for domain_id, score in diag_domain_scores.items():
        if domain_id in domain_buckets:
            domain_buckets[domain_id]["sum"] += score * DIAG_ITEMS_PER_DOMAIN
            domain_buckets[domain_id]["count"] += DIAG_ITEMS_PER_DOMAIN

    for row in progress_rows:
        if row.get("evaluation_completed_at") and row.get("domain_score_after") is not None:
            domain = row.get("primary_domain")  # from Phase 1 JSON enrichment
            if domain and domain in domain_buckets:
                domain_buckets[domain]["sum"] += float(row["domain_score_after"]) * EVAL_ITEMS_PER_MODULE
                domain_buckets[domain]["count"] += EVAL_ITEMS_PER_MODULE

    return {
        d: round(v["sum"] / v["count"], 2) if v["count"] > 0 else 0.0
        for d, v in domain_buckets.items()
    }
```

Call this from both Skills Profile and Home in place of the current inline computation.

---

### Phase 3 — Medium Priority Fixes

#### Task 3.1 — Fix M2: Parameterize all learner writes

**Files**: [pages/01_Diagnostic.py:142-156](pages/01_Diagnostic.py#L142-L156), [pages/04_Course_Module.py:148-161](pages/04_Course_Module.py#L148-L161), [pages/04_Course_Module.py:555-562](pages/04_Course_Module.py#L555-L562), [pages/04_Course_Module.py:593-602](pages/04_Course_Module.py#L593-L602)

Convert all f-string SQL writes to parameterized queries. The `execute()` helper supports `?` parameters. Note: large text payloads (JSON strings) may exceed parameter value length limits — test with realistic practice session JSON sizes.

#### Task 3.2 — Fix M3: Capture `started_at` at session creation

**Files**: [pages/04_Course_Module.py:142](pages/04_Course_Module.py#L142), [pages/01_Diagnostic.py:77](pages/01_Diagnostic.py#L77)

- For `diagnostic_sessions`: store `started_at` in session state when the session UUID is created (`diag_session_started`), pass it to the INSERT
- For `coach_sessions`: store a session start timestamp in session state when practice begins (at Reading → Practice transition), pass it to the INSERT in `do_complete_practice()`

#### Task 3.3 — Fix M4: Results fallback reads `domain_score_after`

**File**: [pages/04_Course_Module.py:724](pages/04_Course_Module.py#L724)

Change:
```python
result_domain_score = result_score
```
To:
```python
try:
    result_domain_score = float(prog_fresh.get("domain_score_after") or result_score)
except (TypeError, ValueError):
    result_domain_score = result_score
```

#### Task 3.4 — Fix M5: Gap map after evaluation uses full merged domain scores

**File**: [pages/04_Course_Module.py:575-591](pages/04_Course_Module.py#L575-L591)

After evaluation, compute the full merged domain scores (using `compute_current_domain_scores()` from Task 2.3) before calling `generate_gap_map()`. This ensures the gap map reflects all training progress, not just the diagnostic baseline.

#### Task 3.5 — Fix M1: Populate token counts in `ai_call_log`

**File**: [utils/ai.py:43-45](utils/ai.py#L43-L45)

After a successful LLM call, extract and pass token counts to `_log_call()`:
```python
usage = getattr(resp, "usage", None)
prompt_tokens = getattr(usage, "prompt_tokens", None)
completion_tokens = getattr(usage, "completion_tokens", None)
_log_call(..., prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
```
Update `_log_call()` signature and the INSERT statement accordingly.

---

### Phase 4 — PRD Feature Gaps

#### Task 4.1 — Add trend indicator to Home summary card

**File**: [pages/03_Home.py](pages/03_Home.py)

**PRD §7.4**: "Trend indicator compared to previous assessment: up arrow if improved, right arrow if same, down arrow if declined"

Query the two most recent `diagnostic_sessions.overall_score` values and compare. Display `↑` (green), `→` (grey), or `↓` (red) next to the overall score.

#### Task 4.2 — Add "Last updated" date to Home summary card

**File**: [pages/03_Home.py](pages/03_Home.py)

**PRD §7.4**: Show "Last updated" date in the summary card.

Use `max(completed_at)` from the most recent `diagnostic_sessions` or `evaluation_completed_at` from `training_progress`, whichever is more recent.

#### Task 4.3 — Fix dead "View Full Profile" link in Home

**File**: [pages/03_Home.py:140-147](pages/03_Home.py#L140-L147)

Remove the dead HTML anchor. Use only the Streamlit button (`view_profile_btn`) for navigation.

---

### Phase 5 — Low Priority Fixes

#### Task 5.1 — Fix L3: Level label gap (0.41–0.49)
**File**: [utils/scoring.py:8-14](utils/scoring.py#L8-L14)
Change `(0.0, 0.4, "Unaware")` to `(0.0, 0.49, "Unaware")` — or refactor to use `<`/`<=` comparisons.

#### Task 5.2 — Fix L6: Welcome guard uses correct routing
**File**: [pages/00_Welcome.py:26-33](pages/00_Welcome.py#L26-L33)
Import and call `get_user_state(user_email)` from `app.py` logic; route to the correct page based on actual state.

#### Task 5.3 — Fix L2: Prevent `reading_completed_at` overwrite
**File**: [pages/04_Course_Module.py:332-341](pages/04_Course_Module.py#L332-L341)
Add `WHERE reading_completed_at IS NULL` to the UPDATE condition. (Already present — verify this is deployed.)

#### Task 5.4 — Fix L4: Cache `load_progress()` or use the cached value ✅ DONE
**File**: [pages/04_Course_Module.py:109-117](pages/04_Course_Module.py#L109-L117)
Fixed: Results fallback now uses the `progress` dict already loaded at page start instead of calling `load_progress()` again — eliminates redundant DB round-trip.

---

## Execution Order

```
Phase 0 ✅ DONE    Phase 1 ✅ DONE               Phase 2 ✅ DONE             Phase 3 ✅ DONE        Phase 4 ✅ DONE          Phase 5 ✅ DONE
Catalog migration   Content DB → JSON refactor    2.1 H2 MCQ local            3.1 M2 Parameterize    4.1 Trend indicator     5.1 L3 Score gap
Bug fixes (H1-H3,   All 7 JSON files created      2.2 H3 Aggregates           3.2 M3 started_at      4.2 Last updated        5.2 L6 guard
L2/L3/L5/L6/L7,    utils/content.py loader        2.3 H1 Domain scores        3.3 M4 Results fix     4.3 Dead link           5.3 L2 stamp
M2/M5)              pages/01-04 updated                                        3.4 M5 Gap map fix                             5.4 L4 Cache
                                                                               3.5 M1 Token counts
```

**All phases complete. Ready for UAT.**

---

## Acceptance Test Checklist (post-Phase 2)

After completing Phases 1 and 2, verify all TDD acceptance criteria:

- [ ] AC-01: New user completes full journey (welcome → diagnostic → skills profile → course → module 1) without errors
- [ ] AC-02: Returning user lands on Home with accurate progress and correct course titles
- [ ] AC-03: Browser close + return on different device → all progress preserved
- [ ] AC-04: Diagnostic scores 12 items and produces gap map within 45 seconds
- [ ] AC-05: AI coach responds within 10 seconds per turn
- [ ] AC-06: Completing module evaluation updates domain scores and unlocks next module
- [ ] AC-07: Module sequence is personalized (verify with different diagnostic score profiles)
- [ ] AC-08: Retake diagnostic updates scores without losing completed module progress
- [ ] AC-09: AI call failures display graceful error and preserve user progress
- [ ] AC-10: No real client names in any content
- [ ] AC-11 (Phase 1): MCQ `options` render correctly from JSON-native list input to `parse_options()`
- [ ] AC-12 (Phase 1): `scoring_rubric` dict passed to scoring functions without `json.loads()` error
- [ ] AC-13 (Phase 1): All 5 module titles and domain labels correct on Home dashboard and sidebar
