# Hexagon Domain Refactor Implementation Plan

> **Status:** APPROVED

---

## Specification

**Problem:** The app's AI skill model has 4 domains (`prompting`, `verification`, `data_safety`,
`tool_fluency`). The public companion version introduced 6 richer, more business-outcome-focused
domains. The corp version needs to adopt this expanded model while preserving its unique
Responsible AI dimension and staying M365/Copilot grounded.

**Goal:** The app uses a 6-domain "hexagon" skill model. Every affected layer — code constants,
scoring, sequencing, prompts, content JSON files, and UI — reflects the new model consistently.
After code changes, the content team can re-run the 3-prompt → generation pipeline to produce
new RM and UW courseware.

**New Domain Model (both roles, role-adapted descriptors):**

| New ID | New Title | Origin |
|---|---|---|
| `responsible_ai` | Responsible AI | Renamed from `data_safety` |
| `strategic_prompting` | Strategic Prompting | Evolved from `prompting` |
| `critical_eval` | Critical Evaluation | Evolved from `verification` |
| `relationship_intel` | Relationship Intelligence | NEW (from public version) |
| `data_decision` | Data-Driven Decision Making | NEW (from public version) |
| `augmented_comm` | Augmented Communication | NEW (from public version) |

**New Course Structure (per role):**
- 7 courses total: 6 domain courses (one per domain) + 1 capstone (always last)
- RM course IDs: `rm_c1_responsible_ai` … `rm_c6_augmented_comm` + `rm_c7_capstone`
- UW course IDs: `uw_c1_responsible_ai` … `uw_c6_augmented_comm` + `uw_c7_capstone`

**New Assessment Counts (per role):**
- Diagnostic: 18 items (3 per domain × 6 domains)
- Evaluation: 28 items (4 per course × 7 courses)
- Reading modules: 7 | Practice scenarios: 7

**Scope IN:**
- All code constants referencing the 4 old domain IDs
- Scoring and sequencing logic updated for 6 domains + 7 courses
- All 3 prompt files updated for the new model (the course design pipeline)
- Placeholder stub content JSON files (correct structure, minimal text) so the app boots
- Hexagon visualization on the Skills Profile page
- Page-level updates for item counts (18 diagnostic, 7 courses)

**Scope OUT:**
- Actual content regeneration (human-in-the-loop: run Prompt A→B→C→script after plan is done)
- Growth hacking, registration, email campaigns (never in corp version)
- Tool Integration domain from public version (intentionally excluded)
- Admin UI, manager dashboards, leaderboards
- Data migration for existing learner rows (dev/MVP: reset is acceptable; see Task 6.1)

**Success Criteria:**
- [ ] `utils/scoring.py` `DOMAIN_IDS` has exactly 6 new IDs; all scoring functions pass pytest
- [ ] `utils/sequencing.py` returns a 7-course sequence (6 domain + capstone) for both roles
- [ ] `scripts/generate_course_content.py` `DOMAIN_IDS` constant matches `utils/scoring.py`
- [ ] All 3 prompt files updated: 6 domains, 7 courses, correct parser-critical section headers
- [ ] Stub content JSON files load without error in `utils/content.py`
- [ ] Skills Profile page renders a hexagon (6 vertices) from domain scores
- [ ] App boots locally (`bash run_uat.sh`) without import errors or missing key errors
- [ ] `pytest` passes (update any test that hardcodes 4 domains or 5 courses)

---

## Context Loading

_Read before starting any task:_

```
read utils/scoring.py
read utils/sequencing.py
read scripts/generate_course_content.py   (lines 1–100)
read prompts/copilot-course-design-brief.md
read prompts/copilot-role-intelligence.md
read prompts/copilot-use-case-mapping.md
read content/domains.json
read content/courses.json
read pages/02_Skills_Profile.py
read pages/01_Diagnostic.py
read pages/03_Home.py
read pages/04_Course_Module.py
read utils/content.py
```

---

## Code Constants Tasks

### Task 1: Update `utils/scoring.py` — domain constants

**Context:** `utils/scoring.py`

**Steps:**

1. [ ] Replace `DOMAIN_IDS` list:
   ```python
   DOMAIN_IDS = [
       "responsible_ai",
       "strategic_prompting",
       "critical_eval",
       "relationship_intel",
       "data_decision",
       "augmented_comm",
   ]
   ```
2. [ ] Replace `DOMAIN_DISPLAY_NAMES` dict:
   ```python
   DOMAIN_DISPLAY_NAMES = {
       "responsible_ai":      "Responsible AI",
       "strategic_prompting": "Strategic Prompting",
       "critical_eval":       "Critical Evaluation",
       "relationship_intel":  "Relationship Intelligence",
       "data_decision":       "Data-Driven Decision Making",
       "augmented_comm":      "Augmented Communication",
   }
   ```
3. [ ] Verify `compute_current_domain_scores` and `calculate_domain_scores` both initialize
   buckets from `DOMAIN_IDS` — no inline domain strings; fix any that exist.
4. [ ] `calculate_overall_score` already averages N values dynamically — no change needed;
   confirm by reading it.

**Verify:** `python -c "from utils.scoring import DOMAIN_IDS, DOMAIN_DISPLAY_NAMES; print(DOMAIN_IDS)"`
outputs 6 new IDs without error.

---

### Task 2: Update `utils/sequencing.py` — course mapping + sequence length

**Context:** `utils/sequencing.py`

**Steps:**

1. [ ] Replace `DOMAIN_TO_COURSE` with the 6-domain mapping for both roles:
   ```python
   DOMAIN_TO_COURSE: dict[str, dict[str, str]] = {
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
   }
   ```
2. [ ] Update `CAPSTONE_COURSE_ID`:
   ```python
   CAPSTONE_COURSE_ID: dict[str, str] = {
       "rm": "rm_c7_capstone",
       "uw": "uw_c7_capstone",
   }
   ```
3. [ ] Change `return sequence[:5]` → `return sequence[:7]` in `compute_module_sequence`.
4. [ ] Update the docstring: "Returns: list of 7 course_ids in personalised order
   (index 0 = Module 1, index 6 = Capstone always last)."

**Verify:** Run the following and confirm 7-element list ending in capstone:
```python
python -c "
from utils.sequencing import compute_module_sequence
scores = {d: 1.5 for d in ['responsible_ai','strategic_prompting','critical_eval','relationship_intel','data_decision','augmented_comm']}
print(compute_module_sequence(scores, 'rm'))
"
```

---

### Task 3: Update `scripts/generate_course_content.py` — constants + token budgets

**Context:** `scripts/generate_course_content.py` (full file)

**Steps:**

1. [ ] Replace `DOMAIN_IDS` on line 56:
   ```python
   DOMAIN_IDS = [
       "responsible_ai",
       "strategic_prompting",
       "critical_eval",
       "relationship_intel",
       "data_decision",
       "augmented_comm",
   ]
   ```
2. [ ] Update `MAX_TOKENS` budgets for 6 domains / 7 courses:
   ```python
   MAX_TOKENS = {
       "parser":         6_000,   # unchanged
       "structural":     9_000,   # 6 domains × 11 level fields + 7 courses
       "qa":             2_000,   # unchanged
       "course_content": 6_000,   # unchanged per course
       "assessment":    12_000,   # 18 items × ~500 tokens/item
       "evaluation":    14_000,   # 28 items × ~400 tokens/item
       "final_qa":       2_000,   # unchanged
   }
   ```
3. [ ] Search the file for any other hardcoded references to the 4 old domain IDs or numbers
   like "4 domains", "5 courses", "12 items", "20 items" — update them to 6/7/18/28.
4. [ ] In the Stage 2 (Structural Generator) system prompt string, update the domain count
   description if it is hardcoded.
5. [ ] In the Stage 5 (Assessment Designer) system prompt, update "12 items (3 per domain)"
   → "18 items (3 per domain × 6 domains)".
6. [ ] In the Stage 6 (Evaluation Designer) system prompt, update "20 items (4 per course)"
   → "28 items (4 per course × 7 courses)".

**Verify:** `python scripts/generate_course_content.py --help` (or import check):
```python
python -c "import scripts.generate_course_content as g; print(g.DOMAIN_IDS)"
```

---

## Prompt Files Tasks

### Task 4: Redesign `prompts/copilot-course-design-brief.md`

**Context:** `prompts/copilot-course-design-brief.md`, `prompts/copilot-use-case-mapping.md`
(read both before editing)

This is the most significant prompt change. The brief is the quality gate for content
generation — get the structure right before content is regenerated.

**Steps:**

1. [ ] In the **PROGRAM STRUCTURE** block, change:
   - "4 AI skill domains (always the same 4 titles)" → "6 AI skill domains (always the same 6 titles)"
   - "5 courses (1 per domain for courses 1–4; course 5 is a capstone)" →
     "7 courses (1 per domain for courses 1–6; course 7 is a capstone integrating all 6 domains)"
   - "1 diagnostic: 12 questions total (3 per domain)" → "18 questions total (3 per domain)"

2. [ ] Replace the 4 fixed domain titles list with the 6 new titles:
   ```
   Domain 1: Responsible AI
   Domain 2: Strategic Prompting
   Domain 3: Critical Evaluation
   Domain 4: Relationship Intelligence
   Domain 5: Data-Driven Decision Making
   Domain 6: Augmented Communication
   ```

3. [ ] In the **FEW-SHOT EXAMPLES** block — SECTION B domain examples:
   Replace all 4 RM domain specs with 6 new specs using the public version's level
   descriptors as a base but adapted to corp/EDC context:
   - `### Domain: responsible_ai` — use corp `data_safety` RM descriptors, rename title
   - `### Domain: strategic_prompting` — use public `strategic_prompting` descriptors,
     adapt corp M365 context (CRAF framework stays)
   - `### Domain: critical_eval` — use public `critical_eval` descriptors, keep VERIFY
     checklist references from corp `verification`
   - `### Domain: relationship_intel` — use public `relationship_intel` descriptors verbatim
     (already RM-appropriate); note UW adaptation needed (portfolio intelligence vs prospect)
   - `### Domain: data_decision` — use public `data_decision` descriptors; adapt to EDC context
     (credit analysis, sector briefings, pipeline forecasting)
   - `### Domain: augmented_comm` — use public `augmented_comm` descriptors; adapt to
     EDC communication channels (client emails, credit memos, proposals)

4. [ ] In **SECTION B output format** (parser-critical sub-headers), replace:
   ```
   ### Domain: prompting
   ### Domain: verification
   ### Domain: data_safety
   ### Domain: tool_fluency
   ```
   with:
   ```
   ### Domain: responsible_ai
   ### Domain: strategic_prompting
   ### Domain: critical_eval
   ### Domain: relationship_intel
   ### Domain: data_decision
   ### Domain: augmented_comm
   ```

5. [ ] Update the **SECTION C** course structure examples: add courses 6 and 7 (augmented_comm
   and capstone) following the same pattern as courses 1–5 in the RM example.

6. [ ] Update the **MACHINE-READABLE HEADER** block:
   - `company_map`: add `course_6` and `course_7` fields
   - `framework_names`: add entries for the 3 new domains:
     - Domain 4 (relationship_intel): standardized name "Prospect Intelligence Framework"
     - Domain 5 (data_decision): standardized name "AI Data Analysis Workflow"
     - Domain 6 (augmented_comm): standardized name "Voice-First Drafting Method"
   - Keep existing 3 framework names (CRAF, VERIFY, SAFE Abstraction); drop "Copilot Surface
     Selector" and "End-to-End AI Workflow" (capstone now synthesizes all 6)

7. [ ] In **SECTION F** (Diagnostic) sub-headers, replace the 4 old domain headers with 6:
   ```
   ### Diagnostic: responsible_ai
   ### Diagnostic: strategic_prompting
   ### Diagnostic: critical_eval
   ### Diagnostic: relationship_intel
   ### Diagnostic: data_decision
   ### Diagnostic: augmented_comm
   ```

8. [ ] In **SECTION G** (Evaluation), extend from 5 courses to 7:
   ```
   ### Evaluation: Course 1
   ...
   ### Evaluation: Course 7
   ```

9. [ ] Update **QUALITY RULES**: change "4 domains" references to "6 domains" and
   "5 courses" to "7 courses".

**Verify:** Read the saved file. Confirm: (a) exactly 6 domain sub-headers in SECTION B,
(b) exactly 7 course entries referenced in SECTION C/D/E/G, (c) MACHINE-READABLE HEADER
lists all 6 framework names.

---

### Task 5: Update `prompts/copilot-role-intelligence.md` and `copilot-use-case-mapping.md`

**Context:** `prompts/copilot-role-intelligence.md`, `prompts/copilot-use-case-mapping.md`

**Steps — `copilot-role-intelligence.md`:**

1. [ ] Read the full file to locate Section 13 "AI Training Design Seeds".
2. [ ] In the domain-to-workflow map sub-section (Section 13C or equivalent), replace:
   `prompting | verification | data_safety | tool_fluency`
   with:
   `responsible_ai | strategic_prompting | critical_eval | relationship_intel | data_decision | augmented_comm`
3. [ ] In the scenario seeds sub-section, update the `Domain` field enum to use new IDs.
4. [ ] If Section 13 has an explicit "4 domains" count, change to "6 domains".

**Steps — `copilot-use-case-mapping.md`:**

1. [ ] Read the full file.
2. [ ] In Task 2 (domain mapping), replace the domain enum:
   `prompting | verification | data_safety | tool_fluency | capstone`
   with:
   `responsible_ai | strategic_prompting | critical_eval | relationship_intel | data_decision | augmented_comm | capstone`
3. [ ] In Task 3 (course anchor proposals), extend from 5 courses to 7:
   - Course 1: `responsible_ai` domain
   - Course 2: `strategic_prompting` domain
   - Course 3: `critical_eval` domain
   - Course 4: `relationship_intel` domain
   - Course 5: `data_decision` domain
   - Course 6: `augmented_comm` domain
   - Course 7: Capstone (integrates 3+ domains)
4. [ ] Update Task 4 gap check: 6 domains to check vs 4.

**Verify:** Grep for old domain IDs in both files — none should remain:
```bash
grep -n "prompting\|verification\|data_safety\|tool_fluency" prompts/copilot-role-intelligence.md prompts/copilot-use-case-mapping.md
```
(Only the old copilot-course-design-brief.md few-shot examples may contain old IDs as
historical reference — acceptable.)

---

## Content Stub Tasks

### Task 6: Create placeholder stub content JSON files

**Context:** `content/domains.json`, `content/courses.json`, `content/diagnostic_items.json`,
`content/evaluation_items.json`, `content/reading_content.json`,
`content/practice_scenarios.json`, `utils/content.py`

The stubs let the app boot and be tested before full content regeneration. They must have
the correct structure and new IDs but may have "[PLACEHOLDER]" text for titles/descriptions.

**Steps:**

1. [ ] **`content/domains.json`** — Replace with 12 stub entries (6 new domain IDs × 2 roles).
   Each entry must have all required keys (`domain_id`, `role_id`, `title`, `description`,
   `level_0_label` through `level_4_label`, `level_0_descriptor` through `level_4_descriptor`).
   Use the public version's domain descriptors as a starting point for RM;
   adapt for UW (e.g., `relationship_intel` for UW = "Portfolio Intelligence" — understanding
   client portfolios rather than prospect research).

2. [ ] **`content/courses.json`** — Replace with 14 stub entries (7 course IDs × 2 roles).
   Use new course IDs (`rm_c1_responsible_ai` … `rm_c7_capstone`, same for `uw_`).
   Each entry must have: `course_id`, `role_id`, `primary_domain`, `title`, `tagline`,
   `description`, `real_use_case`, `sequence_order`.

3. [ ] **`content/diagnostic_items.json`** — Replace with 36 stub items (3 per domain × 6 × 2 roles).
   Each item must have all required keys. For MCQ items: `options` array + `correct_option`.
   For sandbox/micro items: `scoring_rubric` with 4 criteria.
   Use `[PLACEHOLDER - regenerate after Prompt C]` for question text.

4. [ ] **`content/evaluation_items.json`** — Replace with 56 stub items (4 per course × 7 × 2 roles).
   Same structure rules as diagnostic items.

5. [ ] **`content/reading_content.json`** — Replace with 14 stub entries (7 courses × 2 roles).
   Each must have: `content_id`, `course_id`, `concept_text`, `good_example`, `anti_pattern`,
   `takeaway`.

6. [ ] **`content/practice_scenarios.json`** — Replace with 14 stub entries (7 courses × 2 roles).
   Each must have: `scenario_id`, `course_id`, `scenario_text`, `task_1_text` through
   `task_4_text`, `coach_system_prompt`.

7. [ ] Verify `utils/content.py` typed getters work with new IDs. Read the file — if any getter
   filters by domain ID using hardcoded old IDs, update to new IDs.

**Verify:** Boot the app dry-run:
```python
python -c "
from utils.content import get_diagnostic_items, get_courses, get_domain_descriptions
print('RM diag:', len(get_diagnostic_items('rm')), 'items')
print('RM courses:', len(get_courses('rm')), 'courses')
"
```
Expect: 18 diagnostic items, 7 courses for RM (and same for UW).

---

## Data Reset Task

### Task 7: Learner data migration note + reset script update

**Context:** `scripts/reset_uat_user.py`, `notebooks/00_create_schemas.py`

**Steps:**

1. [ ] Read `scripts/reset_uat_user.py`. After the domain refactor, any existing
   `diagnostic_sessions.domain_scores` rows contain 4 old domain keys.
   Update the reset script with a comment block:
   ```python
   # DOMAIN REFACTOR NOTE (2026-03):
   # After the hexagon domain refactor, domain_scores JSON columns store 6 new domain IDs.
   # Any rows created before this refactor have 4 old keys and will produce incorrect
   # scores on the Skills Profile page.
   # For dev/UAT: use this script to reset the test user (already handles full row deletion).
   # For production: a data migration is out of scope for MVP.
   ```
2. [ ] Verify the reset script deletes rows from all affected tables:
   `user_profiles`, `diagnostic_sessions`, `gap_maps`, `training_progress`, `coach_sessions`.
   If `training_progress` still references old course IDs, the delete-by-email already
   handles it (row is dropped, not updated).

**Verify:** Script runs without error against the test database:
```bash
python scripts/reset_uat_user.py
```

---

## UI Tasks

### Task 8: Skills Profile — hexagon visualization

**Context:** `pages/02_Skills_Profile.py`, `utils/scoring.py`

**Steps:**

1. [ ] Read the full `pages/02_Skills_Profile.py` to understand the current chart
   implementation (likely a radar chart via matplotlib or plotly).
2. [ ] Fetch Streamlit + plotly documentation via context7 before making any changes
   (`mcp__context7__resolve-library-id` with "plotly" or "streamlit").
3. [ ] Replace the current domain chart with a proper 6-vertex hexagon using
   **Plotly `go.Scatterpolar`** (same library if already present; add plotly to
   `requirements.txt` if not). The hexagon must:
   - Show 6 vertices labeled with domain display names (from `DOMAIN_DISPLAY_NAMES`)
   - Scale each axis 0–4
   - Fill the polygon area
   - Display the learner's score at each vertex
   - Show level labels (Unaware → Champion) alongside or in tooltip
   - Match existing page color scheme / dark/light theme
4. [ ] If plotly is not already in `requirements.txt`, add it.

**Verify:** App loads Skills Profile page locally without error. Screenshot or visual
confirm that 6 vertices are displayed.

---

### Task 9: Page-level item count updates

**Context:** `pages/01_Diagnostic.py`, `pages/03_Home.py`, `pages/04_Course_Module.py`

**Steps:**

1. [ ] **`pages/01_Diagnostic.py`**: Search for any hardcoded `12` (item count),
   `range(12)`, `question 12 of 12`, progress bar fractions (e.g. `i/12`),
   or domain count `4`. Replace with `18` / `6` as appropriate, or make dynamic
   by computing from `len(get_diagnostic_items(role_id))`.

2. [ ] **`pages/03_Home.py`**: Search for hardcoded `5` (module count), "5 modules",
   progress fractions like `completed/5`. Replace with `7` or make dynamic via
   `len(get_courses(role_id))`.

3. [ ] **`pages/04_Course_Module.py`**: Search for hardcoded module count (`5`) or
   any capstone detection logic that checks `course_id.endswith('_capstone')` or
   `sequence_order == 5`. Update capstone detection to `sequence_order == 7`.

4. [ ] Search all page files for remaining references to old domain IDs
   (`"prompting"`, `"verification"`, `"data_safety"`, `"tool_fluency"`):
   ```bash
   grep -rn "prompting\|verification\|data_safety\|tool_fluency" pages/
   ```
   Replace each with the new domain ID.

**Verify:**
```bash
python -c "import ast, sys; [ast.parse(open(f).read()) for f in ['pages/01_Diagnostic.py','pages/03_Home.py','pages/04_Course_Module.py']]; print('Syntax OK')"
```

---

## Test Update Tasks

### Task 10: Update pytest tests for new domain model

**Context:** `tests/` directory (glob `tests/**/*.py`)

**Steps:**

1. [ ] Glob `tests/**/*.py` to discover all test files.
2. [ ] In each test file, replace all hardcoded old domain IDs
   (`"prompting"`, `"verification"`, `"data_safety"`, `"tool_fluency"`) with
   new IDs from `utils.scoring.DOMAIN_IDS`.
3. [ ] Update any test that constructs `domain_scores` dicts with 4 keys — change to 6 keys.
4. [ ] Update any test that asserts sequence length `== 5` → `== 7`.
5. [ ] Update any test that asserts diagnostic item count `== 12` → `== 18`, or
   evaluation item count `== 20` → `== 28`.
6. [ ] Run the full test suite and fix any remaining failures (do not skip tests).

**Verify:**
```bash
.venv/Scripts/python -m pytest -x -q
```
All tests pass (no skipped domain-related tests).

---

## Final Verification

### Task 11: End-to-end boot check

**Context:** All modified files.

**Steps:**

1. [ ] Confirm `requirements.txt` is up to date (plotly added if needed).
2. [ ] Run `bash run_uat.sh` — app must start on port 8501 without error.
3. [ ] Navigate the full diagnostic flow (Welcome → Diagnostic → Skills Profile) using
   the stub content to verify no runtime key errors.
4. [ ] Check that the Skills Profile hexagon renders for all 6 domains.
5. [ ] Check that the Home page shows 7 module cards.
6. [ ] Run `python scripts/reset_uat_user.py` to confirm reset still works.
7. [ ] Grep for any remaining old domain IDs across the entire codebase:
   ```bash
   grep -rn '"prompting"\|"verification"\|"data_safety"\|"tool_fluency"' \
     utils/ scripts/ pages/ notebooks/ content/ \
     --include="*.py" --include="*.json"
   ```
   Zero matches expected (prompts/ folder is excluded — old IDs may appear in RM few-shot
   examples within the brief).

**Verify:** Successful local app boot + zero grep matches = plan complete.

---

## Post-Plan: Content Regeneration (Human-in-the-Loop)

After this plan is implemented and merged:

1. Run **Prompt A** (updated `copilot-role-intelligence.md`) in M365 Copilot → RM Role Intelligence Profile
2. Run **Prompt A** again → UW Role Intelligence Profile
3. Run **Prompt B** (updated `copilot-use-case-mapping.md`) for each role → Use Case Mapping
4. Run **Prompt C** (updated `copilot-course-design-brief.md`) for each role → Course Design Brief
5. Run `python scripts/generate_course_content.py rm_course_design_brief.md` → 7 RM JSON files
6. Run `python scripts/generate_course_content.py uw_course_design_brief.md` → 7 UW JSON files
7. Deploy with `bash scripts/sync_deploy.sh`
