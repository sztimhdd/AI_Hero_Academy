# Demo Mode — Agent Kickstart Prompt

Copy and paste the section below into a new Claude Code session to implement Phase 14.

---

## Kickstart Prompt

You are implementing **Phase 14: Demo Mode** for the AI Hero Academy Streamlit app.

### Read these files first (in order):

1. `plans/demo-mode.md` — full implementation plan (architecture, fixtures, step-by-step)
2. `utils/db.py` — understand `execute()` / `query_one()` before modifying
3. `utils/auth.py` — thin file, understand `get_user_email()`
4. `app.py` — the router; you will add demo detection here
5. `content/courses.json` — grep for `uw_c1_` and `an_c1_` to verify exact course IDs used in fixture data

### Branch setup (do this first):

```bash
git checkout main && git pull
git checkout -b feature/demo-mode
```

### What to build (summary):

1. **`utils/demo.py`** (new file) — fixture data for 4 personas + `ensure_demo_seeded()` + `_wipe_demo_user()`
2. **`utils/db.py`** — extract existing `execute()` body into `_raw_execute()`, add demo DML suppression guard to `execute()`
3. **`utils/auth.py`** — return demo persona email when `st.session_state["demo_mode"]` is True
4. **`app.py`** — detect `?demo=true` URL param (only when `LOCAL_UAT=true`), initialize demo session state, render profile dropdown in sidebar, handle profile switch with full session reset

### Key constraints:

- Demo mode activates ONLY when `LOCAL_UAT=true` env var is set (never in deployed app)
- Activation: `?demo=true` URL param; optional `?profile=3a|3b|3c|3d` param
- **No per-page changes** — zero modifications to `pages/00_Welcome.py` through `pages/04_Course_Module.py`
- Demo personas use virtual emails (`demo-{id}@demo.local`) — seeded into real DB lazily
- All DB writes (INSERT/UPDATE/DELETE) are suppressed silently while demo mode is active
- `_raw_execute()` bypasses the suppression — used only for fixture seeding in `utils/demo.py`
- Profile switch = wipe demo email rows + re-seed + full `st.session_state` reset + `st.rerun()`

### 4 demo personas:

| ID | Email | Role | Landing page |
|----|-------|------|-------------|
| `3a` | `demo-fresh@demo.local` | — | Welcome |
| `3b` | `demo-rm-diag@demo.local` | `rm` | Diagnostic |
| `3c` | `demo-uw-m1@demo.local` | `uw` | Home (Module 1 complete) |
| `3d` | `demo-an-all@demo.local` | `an` | Home (all 7 modules complete) |

### Fixture data (exact values — use these verbatim):

**3c diagnostic domain scores:**
```python
{"responsible_ai": 1.2, "strategic_prompting": 2.3, "critical_eval": 1.8,
 "relationship_intel": 1.5, "data_decision": 1.1, "augmented_comm": 1.6}
```
overall_score = 1.58

**3c gap map bullets (pre-written, stored as JSON array):**
```python
[
    "Your responses show difficulty distinguishing high-risk from low-risk AI use cases "
    "— prioritise the Responsible AI module to develop safer judgment patterns in "
    "client-facing scenarios.",
    "Data interpretation tasks revealed uncertainty when validating AI-generated "
    "financial figures — the Data-Driven Decision Making module will strengthen your "
    "analytical confidence.",
    "Prompting quality improved notably in Module 1 — build on this momentum by "
    "experimenting with chain-of-thought structures in your next practice session.",
]
```

**3c training_progress (UW courses):**
- Module 1 (`uw_c1_*`): all 3 timestamps set, evaluation_score=2.8, domain_score_after=2.1, is_locked=false
- Modules 2–7 (`uw_c2_*` through `uw_c7_*`): timestamps null, is_locked=true

**3d diagnostic domain scores:**
```python
{"responsible_ai": 2.1, "strategic_prompting": 2.4, "critical_eval": 1.9,
 "relationship_intel": 2.0, "data_decision": 1.8, "augmented_comm": 2.3}
```
overall_score = 2.08

**3d gap map bullets:**
```python
[
    "You've reached Proficient level across all six AI domains — to progress toward "
    "Champion, focus on applying structured prompting frameworks to ambiguous, "
    "multi-step analytical tasks.",
    "Your critical evaluation skills are approaching expert level — challenge yourself "
    "further with real-time fact-checking exercises against live AI outputs in your "
    "workflow.",
    "Augmented Communication is your strongest domain — leverage this by experimenting "
    "with AI-assisted stakeholder reporting and presentation preparation.",
]
```

**3d training_progress (AN courses):**
- All 7 modules: is_locked=false, all 3 timestamps set
- eval_scores: [3.2, 3.0, 2.8, 3.1, 2.9, 3.4, 3.1] (by module sequence)
- domain_score_after: [3.1, 3.0, 2.9, 3.2, 2.8, 3.5, 3.3]

### Verify course IDs before hardcoding:

```bash
python -c "import json; c=json.load(open('content/courses.json')); print([k for k in c if k.startswith('uw_') or k.startswith('an_')])"
```

Use the exact course_id strings returned by this command.

### Schema reference (columns you need for INSERT):

```sql
-- user_profiles
(user_email, display_name, role_id, created_at)

-- diagnostic_sessions
(session_id, user_email, role_id, overall_score, domain_scores, started_at, completed_at)
-- domain_scores is stored as a JSON string

-- gap_maps
(gap_map_id, user_email, session_id, bullets, created_at)
-- bullets is stored as a JSON string

-- training_progress
(progress_id, user_email, course_id, module_sequence_order, is_locked,
 reading_completed_at, practice_completed_at, evaluation_completed_at,
 evaluation_score, domain_score_after)
```

### Verify the schema before running inserts:

```python
# Use the databricks MCP tool to check actual column names:
# mcp__databricks-mcp-server__get_table("mdlg_ai_shared.learner.training_progress")
```

### Testing after implementation:

```bash
bash run_uat.sh
# Then open: http://localhost:8501/?demo=true&profile=3c
```

Verify:
- [ ] Sidebar shows "🎭 Demo Mode" + profile dropdown
- [ ] Profile 3c lands on Home with Module 1 complete (all 3 badges ✓)
- [ ] Skills Profile shows gap map bullets
- [ ] Switch to 3d → Home shows all 7 modules complete
- [ ] Completing a quiz step shows results but no new DB rows written
- [ ] `?demo=true` absent → no demo UI shown

### Commit when done:

```bash
git add utils/demo.py utils/db.py utils/auth.py app.py
git commit -m "feat(demo): add Demo Mode with 4 fixture personas (3a-3d)"
```

Then ask the user if they want to merge to main or keep the branch for review.
