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
| Dark theme design system | §7 | ✅ | Colors/font moved to `.streamlit/config.toml [theme]`; CSS injection now only for custom HTML components |
| Responsive layout (desktop-first) | §5.2 | ✅ | Streamlit's native 900px readable-content width accepted; CSS `max-width` override removed |

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
| `01_seed_roles_domains.py` | ✅ Retired | Content now served from `content/roles.json` + `content/domains.json` (RM + UW) — no Delta seeding required |
| `02_seed_courses.py` | ✅ Retired | Content now served from `content/courses.json` + related JSON files (RM + UW) — no Delta seeding required |
| `03_seed_diagnostic_items.py` | ✅ Retired | Content now served from `content/diagnostic_items.json` (RM 12 + UW 12 = 24 items) — no Delta seeding required |

**Catalog migration completed (Feb 2026):** All content seeded to `mdlg_ai_shared`. Old `mdlg_ai.content`, `mdlg_ai.learner`, `mdlg_ai.system` schemas dropped. App service principal (`9f2c56cc-8b4a-4904-8729-0698a7c67b01`) granted all required UC privileges on `mdlg_ai_shared`.

**Content → JSON architecture (Feb 2026):** All 7 `content.*` Delta tables retired. Static content now served from `content/*.json` files bundled with the app (`utils/content.py` loads them at startup). Multi-role support enabled: `roles.json` has both `rm` and `uw`; `diagnostic_items.json` has 24 items (12 RM + 12 UW); `courses.json` has 10 courses (`rm_c1_*`–`rm_c5_*`, `uw_c1_*`–`uw_c5_*`); `domains.json` uses role-scoped top-level keys (`rm_prompting`, `uw_prompting`, etc.).

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

### Phase 6 — UI/UX Polish Wave 2

Goal: Implement the missing pre-diagnostic orientation screen and conduct a systematic UX audit of every page not yet reviewed. Issues U1–U3 from `Issues.md` are resolved here.

---

#### Task 6.1 — Add pre-diagnostic orientation screen ✅ DONE

**File**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

**Issues.md**: U1 → closed

Orientation screen added before Q1: ~5 min estimate, 12 questions, 4 skill domains, format description, "Start Assessment →" CTA. Guarded by `st.session_state["diag_started"]`; retake path in `02_Skills_Profile.py` clears the flag. Verified via Playwright — card wraps stats correctly, button advances to Q1.

---

#### Task 6.2 — Verify Home module card layout (P0-3) ✅ DONE

**File**: [pages/03_Home.py](pages/03_Home.py)

**Issues.md**: U2 → closed

Verified Feb 2026 via Playwright (1440×900). Module 1 active: cyan border, sub-badges (Read=current, Practice/Quiz=pending), "Start Module 1 →" CTA. Modules 2-5 locked: greyed number, lock icon, no CTA. Summary card: score 0.7, EXPLORER, → trend, "0 of 5 modules complete". 12px gap between card HTML and Streamlit button is framework's native element spacing — structural constraint, accepted.

---

#### Task 6.3 — UX audit: Diagnostic page ✅ DONE

**File**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

**Issues.md**: U3 (partial) | U4 → closed

Audit results (Feb 2026, Playwright):

| Check | Result |
| ----- | ------ |
| All secondary text ≥ `#8990A8` | ✅ Pass — no `#545B70` found anywhere |
| "X of 12" counter + domain tag | ✅ Visible, styled correctly (top-right, cyan pill) |
| Progress bar | ✅ Advances correctly (8% at Q2) |
| MCQ radio: no default selection | ✅ Fixed — `index=None` added (U4) |
| Open-text Submit: disabled when empty | ✅ Pass — prompt_sandbox and micro_task both correct |
| Character guidance hint | ✅ "Aim for 3–8 sentences" visible for prompt_sandbox |
| No orphaned columns | ✅ Pass |

---

#### Task 6.4 — UX audit: Home page ✅ DONE

**File**: [pages/03_Home.py](pages/03_Home.py)

**Issues.md**: U3 (partial) → closed

Audit results (Feb 2026, Playwright 1440×900, Streamlit 1.54.0):

| Check | Result |
| ----- | ------ |
| Summary card: score, trend arrow, level label | ✅ Score 1.5, → (grey), PRACTITIONER |
| "Last updated" date in summary card | ✅ "Last updated: Feb 26, 2026" |
| Module progress counter | ✅ "0 of 5 modules complete" with inline progress bar |
| Module 1 active state: sub-badges + CTA | ✅ Read=current, Practice/Quiz=pending; "Start Module 1 →" `type="primary"` |
| Modules 2-5 locked: 🔒 icon + greyed number | ✅ Lock icon, no CTA, greyed |
| No `color:#545B70` in source | ✅ grep confirmed zero matches |
| "→ View Full Skills Profile" navigates | ✅ Navigates to Skills Profile page |
| Sidebar "🏅 Skills Profile" button | ✅ Present and navigates correctly |

---

#### Task 6.5 — UX audit: Course Module page ✅ DONE

**File**: [pages/04_Course_Module.py](pages/04_Course_Module.py)

**Issues.md**: U3 (partial) → closed | U5 (new bug) → fixed

Audit results (Feb 2026, Playwright + code review):

| Sub-view | Key checks | Result |
| -------- | ---------- | ------ |
| Overview | Progress strip labels; context-aware CTA | ✅ All states correct (`type="primary"`) |
| Reading | Breadcrumb; `st.title()`; step strip; CONCEPT section; callout boxes | ✅ `st.success/error/info()` confirmed in a11y tree |
| Practice | Scenario panel; task counter; `st.chat_message()`; `st.chat_input()` | ✅ Native chat components verified |
| Evaluation | Question counter; `st.progress()`; MCQ radio; performance textarea | ⚠️ Bug found + fixed: MCQ `index=None` added (U5) |
| Results | `st.metric()` score; `st.progress()` domain bar; coach note; next-module CTA | ✅ Native components verified |

No `color:#545B70` found (grep confirmed). No raw `<h1>` HTML injections found.

**Bug fixed during audit**: Evaluation MCQ `st.radio()` was missing `index=None` — same issue as U4 (Diagnostic) but in the Evaluation sub-view. Submit button guard `disabled=(selected is None)` never fired since radio defaulted to first option. Fix: added `index=None` at [pages/04_Course_Module.py:595](pages/04_Course_Module.py#L595).

---

#### Phase 6 Execution Order

```text
6.1  ✅ Pre-diagnostic orientation screen
6.2  ✅ Verify Home module card layout
6.3  ✅ Diagnostic page UX audit  (U4 fixed: MCQ index=None)
6.4  ✅ Home page full UX audit   (all checks pass)
6.5  ✅ Course Module UX audit    (U5 fixed: Evaluation MCQ index=None)
```

---

### Phase 7 — Native UX Modernisation

Goal: Replace custom HTML/CSS hacks with Streamlit-native components throughout the app. Resolve all NX-series issues from `Issues.md`. The priority order addresses HIGH-severity items (broken affordances) first, then MEDIUM (missing semantics), then LOW (cosmetic / fragility). Each task is independently deployable.

---

#### Task 7.1 — Remove global CSS button override; restore `type=` affordance hierarchy

**File**: [utils/styles.py](utils/styles.py) (~line 117)

**Issues.md**: NX2 → close

Remove the global `.stButton > button { background: var(--cyan) !important; ... }` block and its `:hover`, `:active`, `:focus`, `:disabled` variants. Streamlit's `primaryColor = "#00D4E8"` in `config.toml` already sets the correct cyan for `type="primary"` buttons. After removal:

1. Audit each page for buttons that should be `type="primary"` (main CTA per view) and ensure they have `type="primary"`.
2. Secondary/back buttons get no `type=` argument (default grey).
3. The disabled state is handled natively by `disabled=True` on the button.
4. Test all 5 pages to verify no button styling regressions.

| Page | Primary button | Secondary buttons |
|------|---------------|------------------|
| 00_Welcome | "Start My Diagnostic →" | — |
| 01_Diagnostic | "Start Assessment →", "Next →", "Submit →" | — |
| 02_Skills_Profile | "Build My Training Course" / "View My Course" | "↩ Retake Diagnostic" |
| 03_Home | Module CTAs ("Start", "Continue", "Review") | "→ View Full Skills Profile" |
| 04_Course_Module | Per-sub-view CTA | "← Overview", "← Back" |

---

#### Task 7.2 — Replace Practice chat with `st.chat_message()` + `st.chat_input()`

**File**: [pages/04_Course_Module.py](pages/04_Course_Module.py) (Practice sub-view, render_practice function)

**Issues.md**: NX1 → close

Replace the custom HTML chat loop with native Streamlit chat components:

```python
# Render conversation history
for msg in st.session_state["coach_messages"]:
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

# Input
if user_input := st.chat_input("Your response...", disabled=turn_limit_reached):
    # handle send
```

Remove `div.chat-bubble-user`, `div.chat-bubble-coach`, and `div.coach-header` CSS blocks from `styles.py`. The task instruction panel above the chat remains as a custom card (no native equivalent).

---

#### Task 7.3 — Replace Assessment History HTML table with `st.dataframe()`

**File**: [pages/02_Skills_Profile.py:232-262](pages/02_Skills_Profile.py#L232-L262)

**Issues.md**: NX3 → close

Build a `pandas.DataFrame` from `all_diags` and render natively:

```python
import pandas as pd

rows = []
for diag in all_diags:
    ds = json.loads(diag.get("domain_scores") or "{}")
    rows.append({
        "Date": str(diag.get("completed_at", ""))[:10],
        "Overall": round(float(diag.get("overall_score") or 0), 1),
        "Prompting": round(float(ds.get("prompting", 0)), 1),
        "Verification": round(float(ds.get("verification", 0)), 1),
        "Data Safety": round(float(ds.get("data_safety", 0)), 1),
        "Tool Fluency": round(float(ds.get("tool_fluency", 0)), 1),
    })
df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)
```

Remove the `<table>` HTML block and the raw `header_row` / `rows_html` string construction.

---

#### Task 7.4 — Replace score hero with `st.metric()`

**Files**: [pages/02_Skills_Profile.py:161-167](pages/02_Skills_Profile.py#L161-L167), [pages/04_Course_Module.py](pages/04_Course_Module.py) (Results sub-view)

**Issues.md**: NX4 → close

The `[data-testid="stMetric"]` CSS block in `styles.py` already styles the metric card — it just needs to be used. Replace:

```python
st.markdown(f"""
<div class="result-score-box">
  <div class="score-hero-number">{overall:.1f}<span class="score-hero-denom"> / 4.0</span></div>
  <div class="score-hero-label">{level_label}</div>
</div>
""", unsafe_allow_html=True)
```

With:

```python
st.metric(label=level_label, value=f"{overall:.1f} / 4.0")
```

Remove `div.result-score-box`, `.score-hero-number`, `.score-hero-denom`, `.score-hero-label` CSS from `styles.py`.

---

#### Task 7.5 — Replace domain score bars with `st.progress()` + columns

**Files**: [utils/styles.py](utils/styles.py) (`score_bar()` function), [pages/02_Skills_Profile.py:169-180](pages/02_Skills_Profile.py#L169-L180), [pages/04_Course_Module.py](pages/04_Course_Module.py) (Results sub-view)

**Issues.md**: NX5 → close

Replace the `score_bar()` utility function with a native pattern. In each call site:

```python
col_label, col_val = st.columns([4, 1])
with col_label:
    st.caption(DOMAIN_DISPLAY_NAMES.get(domain_id, domain_id))
    st.progress(max(0.0, min(1.0, score / 4.0)))
with col_val:
    st.caption(f"{score:.1f} / 4.0")
```

Remove `score_bar()` from `utils/styles.py` and the associated CSS for `.score-bar-*`. Adjust the `score_bar` import in Skills Profile and Course Module pages.

---

#### Task 7.6 — Investigate and fix console "Invalid color" warnings ✅ DONE

**Files**: [utils/styles.py](utils/styles.py), [.streamlit/config.toml](.streamlit/config.toml)

**Issues.md**: NX6 → closed

**Root cause (Feb 2026)**: Streamlit 1.54.0 JS widget theme code emits warnings when the deprecated internal tokens `widgetBackgroundColor`, `widgetBorderColor`, `skeletonBackgroundColor` have empty string values (Streamlit GitHub issue #13831). These tokens were deprecated in PR #10332 but not yet removed — the JS renderer validates them and warns on empty string.

Our `inject_global_css()` is **not** the cause: all CSS rules already use resolved hex values (not `var()`). The warnings originate purely from Streamlit's own JS theme initialisation.

**Fix applied**: Added the 3 deprecated tokens to `.streamlit/config.toml [theme]` with resolved hex values matching the design system:

```toml
widgetBackgroundColor   = "#1E2330"   # bg_elevated
widgetBorderColor       = "#2A2F3E"   # border
skeletonBackgroundColor = "#1E2330"   # bg_elevated
```

These are visual no-ops (our CSS overrides all widget styling) but provide valid hex values to the JS validator, suppressing the warnings. Requires server restart to take effect.

---

#### Task 7.7 — Replace HTML spacers with `st.divider()` or removal

**Files**: all pages

**Issues.md**: NX8 → close

Grep for `height:` in `st.markdown()` calls. Remove all `<div style='height:Xrem'>` spacer injections. Where a visual section break is needed, use `st.divider()`. Where only padding was needed, remove entirely and let Streamlit's default spacing apply.

```bash
grep -n "height:" pages/*.py
```

---

#### Task 7.8 — Replace `st.markdown('<h1>')` page titles with `st.title()`

**Files**: [pages/02_Skills_Profile.py:146](pages/02_Skills_Profile.py#L146), [pages/04_Course_Module.py](pages/04_Course_Module.py)

**Issues.md**: NX9 → close

Replace raw HTML heading injections with native heading calls. For the two-column layout on Skills Profile (title + date), keep the `st.columns` split and call `st.title()` / `st.caption()` inside columns.

---

#### Task 7.9 — Replace reading content boxes with `st.success()` / `st.error()` / `st.info()`

**File**: [pages/04_Course_Module.py](pages/04_Course_Module.py) (Reading sub-view)

**Issues.md**: NX7 → close

Replace the three reading box types:

| Current div class | Replacement |
|-------------------|-------------|
| `reading-example-box` (Good Example) | `st.success()` |
| `reading-mistake-box` (Common Mistake) | `st.error()` |
| `reading-takeaway-box` (Key Takeaway) | `st.info()` |

Render the box label as `**Good Example**` bold text at the top of the callout content.

---

#### Task 7.10 — Refactor module cards as `st.container(border=True)` with button inside ✅ DONE

**Files**: [pages/03_Home.py](pages/03_Home.py), [utils/styles.py](utils/styles.py)

**Issues.md**: NX10 (partial), NX11 → closed

Replace the HTML card + `:has()` CSS fusion pattern with a native pattern:

```python
with st.container(border=True):
    st.markdown(f"**{title}**")
    st.caption(domain_label)
    # sub-badges as st.columns with st.caption()
    if not is_locked:
        if st.button("Start Module →", key=f"mod_{seq}", type="primary"):
            # navigate
```

This eliminates the fragile `:has()` + adjacent sibling CSS and the `data-testid` button overrides. Remove the entire module card CSS block from `styles.py` (`.module-card`, `.module-card.active`, `.module-card.locked`, the `:has()` rules).

---

#### Phase 7 Execution Order

All tasks complete (Feb 2026):

```text
7.1  ✅ Remove global button CSS override; restore type= system      (NX2 — HIGH)
7.2  ✅ Practice chat → st.chat_message() + st.chat_input()          (NX1 — HIGH)
7.3  ✅ Assessment History → st.dataframe()                          (NX3 — MEDIUM)
7.4  ✅ Score hero → st.metric()                                     (NX4 — MEDIUM)
7.5  ✅ Domain score bars → st.progress()                            (NX5 — MEDIUM)
7.6  ✅ Fix console "Invalid color" warnings                         (NX6 — MEDIUM)
7.7  ✅ Remove HTML spacers                                          (NX8 — LOW)
7.8  ✅ Page titles → st.title()                                     (NX9 — LOW)
7.9  ✅ Reading boxes → st.success/error/info()                      (NX7 — LOW)
7.10 ✅ Module cards → st.container(border=True)                     (NX10/11 — LOW)
```

---

### Phase 8 — UAT Regression Fixes ✅ COMPLETE

Resolved by full end-to-end Playwright UAT (Feb 2026) — 25/27 checks passed. Three issues resolved (Feb 2026). Radar chart added to Skills Profile in this phase as a final UX improvement.

---

#### Task 8.1 ✅ — Fix NX2: Secondary button colour differentiation

**File**: [utils/styles.py](utils/styles.py)

**Issue**: Phase 7.1 removed the global `.stButton > button` background-color override, but UAT confirms both `stBaseButton-primary` and `stBaseButton-secondary` still render identical `rgb(0, 212, 232)`. Streamlit applies `primaryColor` to all interactive elements; there is no built-in separate `secondaryButtonColor`.

**Fix**: Add an explicit CSS rule targeting `[data-testid="stBaseButton-secondary"]` to give secondary buttons a neutral appearance:

```css
/* Secondary buttons — neutral grey to distinguish from primary CTA */
[data-testid="stBaseButton-secondary"] > button {
    background-color: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stBaseButton-secondary"] > button:hover {
    background-color: var(--bg-elevated) !important;
}
```

**Applied**: Added `[data-testid="stBaseButton-secondary"] button` CSS block in `utils/styles.py` with `transparent` background, `border: 1px solid {border}`, and hover state. Uses resolved hex values (not `var()`) consistent with project CSS patterns.

Verify all pages: secondary/back buttons should be grey/outlined; primary CTAs should remain cyan.

---

#### Task 8.2 ✅ — Fix NX6: Console colour warnings persist after config.toml fix (upstream limitation, accepted)

**File**: [.streamlit/config.toml](.streamlit/config.toml), [utils/styles.py](utils/styles.py)

**Issue**: Three `Invalid color` warnings for `widgetBackgroundColor`, `widgetBorderColor`, `skeletonBackgroundColor` still fire per page interaction despite Phase 7.6 adding them to config.toml.

**Resolution**: Root cause confirmed as upstream Streamlit issue #13831 — Streamlit's JS sidebar theme doesn't propagate `widgetBackgroundColor`, `widgetBorderColor`, `skeletonBackgroundColor` from `config.toml`. These are deprecated internal tokens only settable via the JS theme object; no path exists from `config.toml` to suppress the sidebar warnings. Updated `config.toml` comment to document this. 3 warnings per page persist; they are non-blocking and invisible to users. **Accepted as upstream limitation.**

---

#### Task 8.3 ✅ — Fix BUG-1: `gap_maps` table not written after diagnostic

**Files**: [pages/01_Diagnostic.py](pages/01_Diagnostic.py), [utils/ai.py](utils/ai.py)

**Issue**: After diagnostic completion, `ai_call_log` records a successful `generate_gap_map` call but the gap map content is not persisted to `mdlg_ai_shared.learner.gap_maps`. Post-evaluation gap maps work correctly.

**Resolution**: Root cause — `generate_gap_map()` (`utils/ai.py:253`) did a hard `result["gap_bullets"]` that raised `KeyError` when the LLM returned the key as `"bullets"` (or another variant). The exception was silently swallowed by `except Exception: pass`. Two fixes applied:

1. `utils/ai.py`: `generate_gap_map()` now uses `.get("gap_bullets") or .get("bullets") or []` with a list type guard — resilient to LLM key variation.
2. `pages/01_Diagnostic.py`: `except Exception: pass` replaced with `except Exception as _gap_err: print(...)` to stderr — future failures are visible in app logs.

---

#### Phase 8 Execution Order

```text
8.1  Fix NX2: secondary button CSS rule
8.2  Fix NX6: investigate + suppress console colour warnings
8.3  Fix BUG-1: diagnose + fix gap_maps INSERT after diagnostic
     → Deploy and re-run UAT smoke test (Welcome → Diagnostic → Skills Profile gap map visible)
```

---

### Phase 9 — Multi-Role Content Generation: Underwriter (UW)

Extend the app to support a second role — **Underwriter** — using all content authored in `references/underwriter-course-design.md`. The pipeline is a multi-agent LLM script that converts the structured design document into production-ready JSON content files.

The UW role shares the same 4 domain IDs (`prompting`, `verification`, `data_safety`, `tool_fluency`) and the same app shell. Content delivery is through the same JSON module used for the RM role.

---

#### Task 9.1 — Extend app to support multiple roles 🔧 PARTIAL

**Files**: [utils/content.py](utils/content.py), [pages/00_Welcome.py](pages/00_Welcome.py), [pages/01_Diagnostic.py](pages/01_Diagnostic.py)

**Completed sub-tasks:**
- ✅ `content/roles.json` — now has both `rm` and `uw` top-level entries
- ✅ `content/domains.json` — role-scoped top-level keys (`rm_prompting`, `uw_prompting`, etc.); `utils/content.py` builds `DOMAIN_DESCRIPTIONS` from `d["domain_id"]` field values
- ✅ `utils/content.py` — `get_diagnostic_items(role_id)` and `get_domain_descriptions(role_id)` both accept a `role_id` parameter
- ✅ `pages/01_Diagnostic.py` — reads `role_id` from user profile, calls `get_diagnostic_items(role_id)` and `get_domain_descriptions(role_id)`; UW diagnostic flow works end-to-end

**Remaining (blocked on Task 9.4):**
- ❌ `pages/00_Welcome.py` — still hardcodes `role_id = 'rm'` in the INSERT and `_available_roles = ["Relationship Manager"]`; UW users cannot onboard

---

#### Task 9.2 — Multi-agent content generation pipeline ✅ COMPLETE

**File**: `scripts/generate_course_content.py` (1771 lines)

An 8-stage LLM pipeline (not a notebook) that converts a Course Design Brief markdown into all 7 content JSON files. Stages:

1. Parse & Extract — reads design doc, extracts sections
2. Structural Generator — builds course/domain skeletons
3. QA Gap Check — validates coverage
4. Parallel Content Agents — `CourseAgent`, `ReadingAgent`, `ScenarioAgent`, `DiagnosticAgent`, `EvalAgent`
5. Final QA — schema validation
6. Atomic merge — writes UW entries into `content/*.json` alongside existing RM entries

All UW content generated and merged into the shared JSON files.

---

#### Task 9.3 — Validate generated UW content ✅ COMPLETE

Verified counts as of Feb 2026:
- [x] `len(get_diagnostic_items("uw")) == 12` — confirmed (24 total items in `diagnostic_items.json`)
- [x] `len(COURSES)` includes 5 UW courses — `uw_c1_*` through `uw_c5_*` in `courses.json`
- [x] All 5 UW reading entries present in `reading_content.json`
- [x] All 5 UW scenarios with 4 tasks + `coach_system_prompt` in `practice_scenarios.json`
- [x] All 20 UW eval items in `evaluation_items.json` (15 MCQ + 5 performance tasks per course)
- [ ] Welcome page shows role selector with RM + UW options — **blocked on Task 9.4**
- [ ] Full UW learner journey smoke test — **blocked on Task 9.4**

---

#### Task 9.4 — Wire Welcome page for UW role selection ❌ PENDING

**File**: [pages/00_Welcome.py](pages/00_Welcome.py)

Two changes needed:

1. **Role selector**: replace hardcoded `_available_roles = ["Relationship Manager"]` with dynamic lookup from `ROLES` content:
   ```python
   from utils.content import ROLES
   _available_roles = [(v["role_id"], v["title"]) for v in ROLES.values()]
   # then display titles in selectbox; map back to role_id on submit
   ```

2. **INSERT statement**: replace hardcoded `'rm'` with the selected `role_id`:
   ```python
   execute(f"""
       INSERT INTO {CATALOG}.learner.user_profiles
         (user_email, display_name, role_id, created_at)
       VALUES ('{e_email}', '{e_name}', '{escape(selected_role_id)}', current_timestamp())
   """)
   ```

Note: `CX8` fix (closed) replaced the single-option selectbox with a static `st.info()` card to avoid showing an unfinished UI. Now that UW content is complete, this guard should be relaxed: if `len(ROLES) > 1`, show the selectbox; if exactly 1 role exists, keep the static card.

---

#### Task 9.5 — Full UW journey acceptance test ❌ PENDING

Prerequisite: Task 9.4 complete and deployed.

- [ ] New UW user can complete Welcome → Diagnostic → Skills Profile → Build Course → Module 1
- [ ] Diagnostic shows 12 UW-specific questions with correct domain labels
- [ ] Module sequencing uses `uw_c1_*`–`uw_c5_*` course IDs
- [ ] All reading content, practice scenarios, and evaluation items load correctly
- [ ] Gap map generates with UW-specific domain descriptions
- [ ] Retake diagnostic works for UW user without losing module progress

---

#### Phase 9 Execution Order

```text
9.1  🔧 PARTIAL  Multi-role app support (content.py + diagnostic done; Welcome pending)
9.2  ✅ DONE     Multi-agent content generation pipeline (scripts/generate_course_content.py)
9.3  ✅ DONE     UW content validation (24 diag items, 10 courses, 10 eval courses confirmed)
9.4  ❌ PENDING  Wire Welcome page for UW role selection (dynamic ROLES lookup + role_id INSERT)
9.5  ❌ PENDING  Full UW learner journey acceptance tests
     → Deploy and smoke-test full UW learner journey after 9.4
```

---

## Execution Order

```text
Phase 0 ✅ DONE    Phase 1 ✅ DONE               Phase 2 ✅ DONE             Phase 3 ✅ DONE        Phase 4 ✅ DONE          Phase 5 ✅ DONE      Phase 6 ✅ DONE          Phase 7 ✅ DONE
Catalog migration   Content DB → JSON refactor    2.1 H2 MCQ local            3.1 M2 Parameterize    4.1 Trend indicator     5.1 L3 Score gap     6.1 ✅ Orientation       7.1 ✅ Button override
Bug fixes (H1-H3,   All 7 JSON files created      2.2 H3 Aggregates           3.2 M3 started_at      4.2 Last updated        5.2 L6 guard         6.2 ✅ Module cards      7.2 ✅ Chat components
L2/L3/L5/L6/L7,    utils/content.py loader        2.3 H1 Domain scores        3.3 M4 Results fix     4.3 Dead link           5.3 L2 stamp         6.3 ✅ Diagnostic        7.3 ✅ st.dataframe()
M2/M5)              pages/01-04 updated                                        3.4 M5 Gap map fix                             5.4 L4 Cache         6.4 ✅ Home audit        7.4 ✅ st.metric()
                                                                               3.5 M1 Token counts                                                 6.5 ✅ Course audit      7.5 ✅ st.progress()
                                                                                                                                                                           7.6 ✅ Color warnings
                                                                                                                                                                           7.7 ✅ Spacers
                                                                                                                                                                           7.8 ✅ st.title()
                                                                                                                                                                           7.9 ✅ Callout boxes
                                                                                                                                                                           7.10 ✅ Module cards

Phase 8 ✅ DONE             Phase 9 — Underwriter Role (in progress)
UAT Regression Fixes       9.1 🔧 Multi-role app support (partial — Welcome page pending)
8.1 NX2 secondary button   9.2 ✅ Content generation pipeline (scripts/generate_course_content.py)
8.2 NX6 console warnings   9.3 ✅ UW content validation (24 diag, 10 courses, domains role-scoped)
8.3 BUG-1 gap_maps fix     9.4 ❌ Wire Welcome page for UW role selection
                           9.5 ❌ Full UW journey acceptance tests
```

**Phases 0–8 complete. Phase 9 in progress: UW content generated and validated; Welcome page wiring (Task 9.4) is the only remaining blocker before UW goes live.**

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

---

### Phase 10 — UAT Persona Switching ❌ PENDING

**Problem:** The UAT environment uses a single hardcoded test user (`DEV_USER_EMAIL` = `uat-test@edc.ca`). Once the profile is seeded with a completed RM diagnostic and module progress, it is impossible to test:

- The Welcome → profile creation flow
- The newly added UW (Underwriter) role
- The Diagnostic flow from scratch

**Solution:** Enhance `scripts/reset_uat_user.py` with two optional CLI flags. No new files, no new emails, no changes to `.env` or `run_uat.sh`.

---

#### Task 10.1 — Enhance `scripts/reset_uat_user.py` ❌ PENDING

**File**: [`scripts/reset_uat_user.py`](scripts/reset_uat_user.py)

**Scope**: Single-file change only. Add `argparse` with two optional flags:

| Flag | Type | Effect |
| --- | --- | --- |
| `--role rm/uw` | optional str | After full wipe, inserts one `user_profiles` row → app lands on Diagnostic |
| `--diag` | optional flag | Requires `--role`; also inserts `diagnostic_sessions` + `gap_maps` → Skills Profile |

**Resulting test states:**

| Command | App landing page | Tables seeded |
| --- | --- | --- |
| `python scripts/reset_uat_user.py` | Welcome | nothing (full wipe — existing behaviour) |
| `python scripts/reset_uat_user.py --role rm` | Diagnostic | `user_profiles` (role_id=rm) |
| `python scripts/reset_uat_user.py --role uw` | Diagnostic | `user_profiles` (role_id=uw) |
| `python scripts/reset_uat_user.py --role rm --diag` | Skills Profile | `user_profiles` + `diagnostic_sessions` + `gap_maps` |
| `python scripts/reset_uat_user.py --role uw --diag` | Skills Profile | `user_profiles` + `diagnostic_sessions` + `gap_maps` |

**Implementation notes:**

1. **argparse block** — add after `load_dotenv` and before the `TABLES` loop:

   ```python
   import argparse, uuid, json
   from datetime import datetime, timezone

   parser = argparse.ArgumentParser(description="Reset UAT user data")
   parser.add_argument("--role", choices=["rm", "uw"], help="Seed a user_profiles row for this role")
   parser.add_argument("--diag", action="store_true", help="Also seed a completed diagnostic_sessions + gap_maps row (requires --role)")
   args = parser.parse_args()

   if args.diag and not args.role:
       parser.error("--diag requires --role")
   ```

2. **`--role` seed** — insert a `user_profiles` row using parameterised execute():

   ```python
   display_name = "RM Tester" if args.role == "rm" else "UW Tester"
   execute(
       f"INSERT INTO {CATALOG}.learner.user_profiles (user_email, display_name, role_id, created_at) "
       f"VALUES (?, ?, ?, current_timestamp())",
       [EMAIL, display_name, args.role],
   )
   ```

3. **`--diag` seed** — insert canned `diagnostic_sessions` and `gap_maps` rows:
   - Use realistic but artificial domain scores: all 4 domains at `1.5` (Practitioner boundary — exercises the full gap map display)
   - Use the same `DOMAIN_IDS = ["prompting", "verification", "data_safety", "tool_fluency"]` keys for both roles (role-agnostic per `utils/scoring.py`)
   - Canned `domain_scores_json`: `{"prompting": 1.5, "verification": 1.0, "data_safety": 2.0, "tool_fluency": 1.5}`
   - `overall_score`: `1.5`
   - Canned `gap_maps.bullets`: 3 bullets, one per low-scoring domain
   - `session_id` and `gap_map_id`: generate fresh `uuid.uuid4()` at runtime

4. **Validation** — guard `--diag` with `if args.diag and not args.role: parser.error(...)` (already listed above)

**No changes to:**

- `.env` / `.env.example`
- `run_uat.sh`
- `utils/auth.py`
- Any page or content file

---

#### Phase 10 Acceptance Checks

- [ ] `python scripts/reset_uat_user.py` — app opens on Welcome page (existing behaviour unchanged)
- [ ] `python scripts/reset_uat_user.py --role rm` — app opens on Diagnostic page with RM role
- [ ] `python scripts/reset_uat_user.py --role uw` — app opens on Diagnostic page with UW role
- [ ] `python scripts/reset_uat_user.py --role rm --diag` — app opens on Skills Profile; domain scores visible; gap map bullets visible
- [ ] `python scripts/reset_uat_user.py --role uw --diag` — same as above for UW role
- [ ] `python scripts/reset_uat_user.py --diag` (without `--role`) — prints error and exits non-zero
- [ ] Existing full-wipe path produces no errors after this change

---

### Phase 11 — UI/UX Bug Fixes (Open Issues) ✅ COMPLETE

Fix all 6 open issues currently tracked in `Issues.md`. Ordered by severity then ID.

---

#### Task 11.1 — Fix P1: Add "Continue" option at per-task turn limit

**File**: [pages/04_Course_Module.py](pages/04_Course_Module.py)

**Issues.md**: P1 (MEDIUM)

The turn-limit block at lines 388–396 shows "Next Task →" then calls `st.stop()`, forcing advancement. Learner has no option to extend.

**Fix**:

1. Add `task_extra_turns` to session state (keyed per task index, default 0).
2. Compute effective turn limit: `effective_limit = MAX_TASK_TURNS + st.session_state.get(f"task_extra_{task_idx}", 0) * 3`.
3. Replace the existing turn-limit block with a two-button prompt:

```python
if turns_this_task >= effective_limit:
    st.info("You've reached the turn limit for this task.")
    col_cont, col_next = st.columns(2)
    with col_cont:
        if st.button("Continue (3 more turns) →", key=f"cont_{task_idx}"):
            st.session_state[f"task_extra_{task_idx}"] = st.session_state.get(f"task_extra_{task_idx}", 0) + 1
            st.rerun()
    with col_next:
        if st.button("Next Task →", key=f"next_{task_idx}", type="primary"):
            _advance_task()
    st.stop()
```

No changes to `MAX_TASK_TURNS` constant or overall turn counter.

---

#### Task 11.2 — Fix P2: Update practice navigation warning banner copy

**File**: [pages/04_Course_Module.py](pages/04_Course_Module.py)

**Issues.md**: P2 (MEDIUM)

The `st.warning()` at line 344 says "Use **Complete Practice →** to save your work" but that button is not visible at Turn 0 of Task 1. Misleads users.

**Fix**: Change the banner text to remove the button reference:

```python
st.warning(
    "⚠️ Navigating away via the sidebar or breadcrumb will end your session "
    "without saving your practice conversation."
)
```

Single-line change. No logic changes.

---

#### Task 11.3 — Fix NAV1: Consistent sidebar navigation across all pages

**Files**: [utils/styles.py](utils/styles.py), [pages/03_Home.py](pages/03_Home.py), [pages/02_Skills_Profile.py](pages/02_Skills_Profile.py), [pages/04_Course_Module.py](pages/04_Course_Module.py)

**Issues.md**: NAV1 (MEDIUM)

Each page independently renders its own sidebar, causing inconsistent navigation:

- Home: only "🏅 Skills Profile"
- Skills Profile: "🏠 My Training" + "📚 My Course"
- Course Module: "🏠 My Training" + "🏅 Skills Profile" + context block

**Fix**: Extract a `render_sidebar(active_page, has_course, progress_rows, active_course_id)` utility into `utils/styles.py`. The utility always renders all 3 nav buttons (disabled when active), and conditionally shows the module context block on Course Module only.

```python
def render_sidebar(
    active_page: str,           # "home" | "skills_profile" | "course_module"
    has_course: bool = False,
    progress_rows: list = None,
    active_course_id: str = None,
):
    with st.sidebar:
        # ... brand block ...
        st.markdown("---")
        if st.button("🏠  My Training", ..., disabled=(active_page == "home")):
            st.switch_page("pages/03_Home.py")
        if st.button("🏅  Skills Profile", ..., disabled=(active_page == "skills_profile")):
            st.switch_page("pages/02_Skills_Profile.py")
        if has_course:
            if st.button("📚  My Course", ..., disabled=(active_page == "course_module")):
                # CX3 logic: set active_course_id then navigate
                ...
        # Module context block — Course Module only
        if active_page == "course_module" and active_course_id:
            ...
```

Replace each page's `with st.sidebar:` block with a single `render_sidebar(...)` call.

**Execution order**: implement utility first, then update each page.

---

#### Task 11.4 — Fix NAV2: Hide Streamlit sidebar collapse button

**File**: [utils/styles.py](utils/styles.py)

**Issues.md**: NAV2 (LOW)

The built-in Streamlit sidebar collapse toggle renders its Material Icon font code as plain text on hover. Causes accidental mis-clicks. The sidebar is always expanded; collapse is not a use case for this app.

**Fix**: Add one CSS rule to `inject_global_css()`:

```css
/* Hide Streamlit's built-in sidebar collapse toggle — sidebar is always expanded
   and the Material Icons font is not loaded, causing icon text to bleed through. */
[data-testid="collapsedControl"] {{ display: none !important; }}
```

One-line CSS addition.

---

#### Task 11.5 — Fix UI1: Add gap between sub-badges and action button on module cards

**File**: [pages/03_Home.py](pages/03_Home.py)

**Issues.md**: UI1 (LOW)

Playwright DOM measurement confirmed: `.sub-strip` bottom = 470px, button top = 470px — zero-pixel gap. The Read/Practice/Quiz badge strip is flush against the CTA button with no visual separation.

**Fix**: Add `margin-top: 0.75rem` to the `.sub-strip` CSS rule in `utils/styles.py`:

```css
.sub-strip {{
    ...existing rules...
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;   /* ← new: separates strip from button below */
}}
```

Alternatively (if `.sub-strip` bottom margin is insufficient due to Streamlit element spacing): add a small spacer `st.markdown('<div style="margin-top:0.5rem"></div>', unsafe_allow_html=True)` before the `st.button()` call for the active module in `pages/03_Home.py`. CSS approach preferred.

---

#### Task 11.6 — Fix UI2: "Review Module" button jumps directly to Results sub-view

**File**: [pages/03_Home.py](pages/03_Home.py)

**Issues.md**: UI2 (LOW)

Clicking "Review Module N" on the Home page lands on the Overview sub-view (all 3 steps checked ✓, only CTA is "Review Results →"). A second click is required to reach Results. The Overview sub-view adds no value for a fully-completed module.

**Fix**: In the "Review Module" button handler, set `active_submodule = "results"` when all three sub-steps (reading, practice, evaluation) are complete:

```python
if st.button(f"Review Module {seq} →", key=f"review_{seq}"):
    st.session_state["active_course_id"] = row["course_id"]
    # Jump directly to results if fully complete; overview otherwise
    all_done = (
        row.get("reading_completed_at")
        and row.get("practice_completed_at")
        and row.get("evaluation_completed_at")
    )
    st.session_state["active_submodule"] = "results" if all_done else "overview"
    st.switch_page("pages/04_Course_Module.py")
```

---

#### Phase 11 Execution Order

Tasks are roughly independent except 11.3 (NAV1) which touches 3 files and should be done last to avoid merge conflicts with 11.1/11.2 which edit the same `04_Course_Module.py`.

```text
11.4  Hide sidebar collapse button (1 CSS line — lowest risk)
11.5  Sub-badge gap (1 CSS rule change)
11.6  Review Module → results shortcut (1 button handler change)
11.2  Practice banner copy (1 string change)
11.1  Per-task turn limit: Continue option (logic change in practice sub-view)
11.3  Consistent sidebar: extract render_sidebar() utility (multi-file refactor)
      → Run Playwright UAT after 11.3 to verify all pages
```

---

#### Phase 11 Acceptance Checks

- [x] P1: After 3 turns on a task, page shows "Continue (3 more turns) →" and "Next Task →" side-by-side; clicking Continue allows 3 more turns; clicking Next Task advances to next task
- [x] P2: Practice sub-view navigation banner at Turn 0 no longer references "Complete Practice →"; new wording confirms navigating away ends the session
- [x] NAV1: All 3 pages (Home, Skills Profile, Course Module) show the same 3 sidebar buttons; active page button is disabled; "📚 My Course" appears on Home if a course exists
- [x] NAV2: Sidebar collapse toggle is no longer visible (no text bleed-through on hover)
- [x] UI1: Visible gap between Read/Practice/Quiz badge strip and the action button on module cards
- [x] UI2: Clicking "Review Module N" on a fully-completed module lands directly on the Results sub-view; clicking on an incomplete module still lands on Overview
