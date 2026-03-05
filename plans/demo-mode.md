# Plan: Phase 14 — Demo Mode

**Status**: READY TO IMPLEMENT
**Branch**: `feature/demo-mode`
**Estimated scope**: 1 new file + 4 modified files; no per-page changes

---

## Overview

Add a Demo Mode to the app that:

1. Is activated via URL param `?demo=true` — only when `LOCAL_UAT=true` env var is set
2. Shows a Profile dropdown in the sidebar top-left replacing the UAT indicator
3. Offers 4 predefined learner personas (3a–3d) covering the full user journey
4. Pre-seeds fixture state into the DB for each persona (lazy, on first selection)
5. Suppresses all DB writes (DML) while demo mode is active
6. Resets cleanly on persona switch

---

## Architecture Decision

**Approach: Demo email + fixture seeding + DML suppression**

Each demo persona maps to a virtual email address (`demo-{id}@demo.local`). On persona
selection, fixture rows are inserted into the learner tables for that email. Pages then
work exactly as they do today — reading from the DB as usual — but `execute()` suppresses
any DML the user triggers (quiz submit, practice save, module unlock, etc.).

Benefits:
- **Zero per-page changes** — all 5 pages work with no modifications
- **Realistic UX** — pages render real content, real routing logic, real AI calls
- **Clean separation** — demo logic lives entirely in `utils/demo.py` + thin shims in `db.py`, `auth.py`, `app.py`

---

## Persona Definitions

| ID | Email | Role | Landing page | DB state |
|----|-------|------|--------------|----------|
| `3a` | `demo-fresh@demo.local` | — | Welcome | No `user_profiles` row |
| `3b` | `demo-rm-diag@demo.local` | `rm` | Diagnostic | `user_profiles` only |
| `3c` | `demo-uw-m1@demo.local` | `uw` | Home (M1 done) | Profile + diag + gap map + M1 progress |
| `3d` | `demo-an-all@demo.local` | `an` | Home (all done) | Profile + diag + gap map + all 7 modules |

---

## Fixture Data Spec

### Profile 3c — UW, Module 1 complete

**Diagnostic domain scores** (stored in `diagnostic_sessions.domain_scores` as JSON):
```json
{
  "responsible_ai": 1.2,
  "strategic_prompting": 2.3,
  "critical_eval": 1.8,
  "relationship_intel": 1.5,
  "data_decision": 1.1,
  "augmented_comm": 1.6
}
```
`overall_score`: `1.58`

**Gap map bullets** (stored in `gap_maps.bullets` as JSON array — these are pre-written fixture text):
```json
[
  "Your responses show difficulty distinguishing high-risk from low-risk AI use cases — prioritise the Responsible AI module to develop safer judgment patterns in client-facing scenarios.",
  "Data interpretation tasks revealed uncertainty when validating AI-generated financial figures — the Data-Driven Decision Making module will strengthen your analytical confidence.",
  "Prompting quality improved notably in Module 1 — build on this momentum by experimenting with chain-of-thought structures in your next practice session."
]
```

**`training_progress` rows** (7 rows for `uw_c1_*` through `uw_c7_*`):
- Module 1 (`uw_c1_responsible_ai`): `is_locked=false`, all 3 completion timestamps set, `evaluation_score=2.8`, `domain_score_after=2.1`, `module_sequence_order=1`
- Modules 2–7: `is_locked=true`, all timestamps null, `module_sequence_order=2–7`

### Profile 3d — AN, all modules complete

**Diagnostic domain scores**:
```json
{
  "responsible_ai": 2.1,
  "strategic_prompting": 2.4,
  "critical_eval": 1.9,
  "relationship_intel": 2.0,
  "data_decision": 1.8,
  "augmented_comm": 2.3
}
```
`overall_score`: `2.08`

**Gap map bullets** (post-completion, advanced framing):
```json
[
  "You've reached Proficient level across all six AI domains — to progress toward Champion, focus on applying structured prompting frameworks to ambiguous, multi-step analytical tasks.",
  "Your critical evaluation skills are approaching expert level — challenge yourself further with real-time fact-checking exercises against live AI outputs in your workflow.",
  "Augmented Communication is your strongest domain — leverage this by experimenting with AI-assisted stakeholder reporting and presentation preparation."
]
```

**`training_progress` rows** (7 rows for `an_c1_*` through `an_c7_*`):
- All 7 modules: `is_locked=false`, all 3 completion timestamps set, realistic `evaluation_score` (2.5–3.4), realistic `domain_score_after` (2.8–3.6), `module_sequence_order=1–7`

---

## Files to Create / Modify

| File | Action | Summary |
|------|--------|---------|
| `utils/demo.py` | **Create** | Fixture data, seeding logic, helpers |
| `utils/db.py` | **Modify** | Suppress DML when demo mode active |
| `utils/auth.py` | **Modify** | Return demo email when demo mode active |
| `app.py` | **Modify** | Detect URL param, render profile dropdown, handle switch |

---

## Implementation Steps

### Step 1 — Create git feature branch

```bash
git checkout -b feature/demo-mode
```

---

### Step 2 — Create `utils/demo.py`

New file. Contains:

```python
"""
Demo Mode — fixture profiles for local UAT and stakeholder demos.

Activated via ?demo=true URL param when LOCAL_UAT=true.
Personas are pre-seeded into the DB lazily on first selection.
All DB writes (DML) are suppressed while demo mode is active.
"""
import os
import uuid
import json
from datetime import datetime, timezone
from utils.db import _raw_execute  # internal bypass for seeding

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")

# ── Persona registry ──────────────────────────────────────────────────────────
DEMO_PROFILES = {
    "3a": {
        "label": "3a — Fresh user (Welcome)",
        "email": "demo-fresh@demo.local",
        "role_id": None,
        "display_name": "Demo User",
    },
    "3b": {
        "label": "3b — RM at Diagnostic",
        "email": "demo-rm-diag@demo.local",
        "role_id": "rm",
        "display_name": "Alex Chen (Demo)",
    },
    "3c": {
        "label": "3c — UW, Module 1 complete",
        "email": "demo-uw-m1@demo.local",
        "role_id": "uw",
        "display_name": "Jordan Lee (Demo)",
    },
    "3d": {
        "label": "3d — AN, all modules complete",
        "email": "demo-an-all@demo.local",
        "role_id": "an",
        "display_name": "Taylor Kim (Demo)",
    },
}

DEFAULT_PROFILE = "3a"

# ── Fixture data ──────────────────────────────────────────────────────────────

_DIAG_DOMAIN_SCORES_3C = {
    "responsible_ai": 1.2, "strategic_prompting": 2.3, "critical_eval": 1.8,
    "relationship_intel": 1.5, "data_decision": 1.1, "augmented_comm": 1.6,
}

_GAP_BULLETS_3C = [
    "Your responses show difficulty distinguishing high-risk from low-risk AI use cases "
    "— prioritise the Responsible AI module to develop safer judgment patterns in "
    "client-facing scenarios.",
    "Data interpretation tasks revealed uncertainty when validating AI-generated "
    "financial figures — the Data-Driven Decision Making module will strengthen your "
    "analytical confidence.",
    "Prompting quality improved notably in Module 1 — build on this momentum by "
    "experimenting with chain-of-thought structures in your next practice session.",
]

_DIAG_DOMAIN_SCORES_3D = {
    "responsible_ai": 2.1, "strategic_prompting": 2.4, "critical_eval": 1.9,
    "relationship_intel": 2.0, "data_decision": 1.8, "augmented_comm": 2.3,
}

_GAP_BULLETS_3D = [
    "You've reached Proficient level across all six AI domains — to progress toward "
    "Champion, focus on applying structured prompting frameworks to ambiguous, "
    "multi-step analytical tasks.",
    "Your critical evaluation skills are approaching expert level — challenge yourself "
    "further with real-time fact-checking exercises against live AI outputs in your "
    "workflow.",
    "Augmented Communication is your strongest domain — leverage this by experimenting "
    "with AI-assisted stakeholder reporting and presentation preparation.",
]

# UW course IDs in sequence order (must match content/courses.json)
_UW_COURSES = [
    "uw_c1_responsible_ai", "uw_c2_strategic_prompting", "uw_c3_critical_eval",
    "uw_c4_relationship_intel", "uw_c5_data_decision", "uw_c6_augmented_comm",
    "uw_c7_capstone",
]

# AN course IDs in sequence order (must match content/courses.json)
_AN_COURSES = [
    "an_c1_responsible_ai", "an_c2_strategic_prompting", "an_c3_critical_eval",
    "an_c4_relationship_intel", "an_c5_data_decision", "an_c6_augmented_comm",
    "an_c7_capstone",
]

_AN_MODULE_EVAL_SCORES = [3.2, 3.0, 2.8, 3.1, 2.9, 3.4, 3.1]  # per module
_AN_MODULE_DOMAIN_SCORES = [3.1, 3.0, 2.9, 3.2, 2.8, 3.5, 3.3]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _wipe_demo_user(email: str) -> None:
    """Delete all learner rows for a demo email (for clean re-seed)."""
    tables = [
        "learner.training_progress",
        "learner.gap_maps",
        "learner.diagnostic_sessions",
        "learner.user_profiles",
    ]
    for table in tables:
        _raw_execute(
            f"DELETE FROM {CATALOG}.{table} WHERE user_email = ?", [email]
        )


def ensure_demo_seeded(profile_id: str) -> None:
    """
    Seed fixture data for a demo profile into the DB.
    Wipes existing data for this demo email first, then re-inserts.
    Uses _raw_execute() to bypass DML suppression.
    """
    profile = DEMO_PROFILES.get(profile_id)
    if not profile:
        return
    email = profile["email"]
    _wipe_demo_user(email)

    if profile_id == "3a":
        return  # fresh user — no rows needed

    # user_profiles
    _raw_execute(
        f"INSERT INTO {CATALOG}.learner.user_profiles "
        f"(user_email, display_name, role_id, created_at) "
        f"VALUES (?, ?, ?, ?)",
        [email, profile["display_name"], profile["role_id"], _now_iso()],
    )

    if profile_id == "3b":
        return  # RM at diagnostic start — only profile row needed

    # diagnostic_sessions (3c and 3d)
    role_id = profile["role_id"]
    domain_scores = _DIAG_DOMAIN_SCORES_3C if profile_id == "3c" else _DIAG_DOMAIN_SCORES_3D
    overall = round(sum(domain_scores.values()) / len(domain_scores), 2)
    session_id = str(uuid.uuid4())
    _raw_execute(
        f"INSERT INTO {CATALOG}.learner.diagnostic_sessions "
        f"(session_id, user_email, role_id, overall_score, domain_scores, "
        f"started_at, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            session_id, email, role_id, str(overall),
            json.dumps(domain_scores), _now_iso(), _now_iso(),
        ],
    )

    # gap_maps
    bullets = _GAP_BULLETS_3C if profile_id == "3c" else _GAP_BULLETS_3D
    _raw_execute(
        f"INSERT INTO {CATALOG}.learner.gap_maps "
        f"(gap_map_id, user_email, session_id, bullets, created_at) "
        f"VALUES (?, ?, ?, ?, ?)",
        [str(uuid.uuid4()), email, session_id, json.dumps(bullets), _now_iso()],
    )

    # training_progress
    if profile_id == "3c":
        courses = _UW_COURSES
        for i, course_id in enumerate(courses):
            seq = i + 1
            is_locked = "false" if seq == 1 else "true"
            if seq == 1:
                _raw_execute(
                    f"INSERT INTO {CATALOG}.learner.training_progress "
                    f"(progress_id, user_email, course_id, module_sequence_order, "
                    f"is_locked, reading_completed_at, practice_completed_at, "
                    f"evaluation_completed_at, evaluation_score, domain_score_after) "
                    f"VALUES (?, ?, ?, ?, {is_locked}, ?, ?, ?, ?, ?)",
                    [
                        str(uuid.uuid4()), email, course_id, str(seq),
                        _now_iso(), _now_iso(), _now_iso(), "2.8", "2.1",
                    ],
                )
            else:
                _raw_execute(
                    f"INSERT INTO {CATALOG}.learner.training_progress "
                    f"(progress_id, user_email, course_id, module_sequence_order, is_locked) "
                    f"VALUES (?, ?, ?, ?, {is_locked})",
                    [str(uuid.uuid4()), email, course_id, str(seq)],
                )

    elif profile_id == "3d":
        courses = _AN_COURSES
        for i, course_id in enumerate(courses):
            seq = i + 1
            _raw_execute(
                f"INSERT INTO {CATALOG}.learner.training_progress "
                f"(progress_id, user_email, course_id, module_sequence_order, "
                f"is_locked, reading_completed_at, practice_completed_at, "
                f"evaluation_completed_at, evaluation_score, domain_score_after) "
                f"VALUES (?, ?, ?, ?, false, ?, ?, ?, ?, ?)",
                [
                    str(uuid.uuid4()), email, course_id, str(seq),
                    _now_iso(), _now_iso(), _now_iso(),
                    str(_AN_MODULE_EVAL_SCORES[i]),
                    str(_AN_MODULE_DOMAIN_SCORES[i]),
                ],
            )
```

---

### Step 3 — Modify `utils/db.py`

Add a `_raw_execute()` internal function (bypasses demo suppression) and guard DML in `execute()`.

```python
import streamlit as st
import re

_DML_RE = re.compile(r"^\s*(INSERT|UPDATE|DELETE|MERGE)\b", re.IGNORECASE)


def _is_demo_mode() -> bool:
    try:
        import streamlit as st
        return bool(st.session_state.get("demo_mode"))
    except Exception:
        return False


def _raw_execute(statement: str, parameters: list = None) -> list[dict]:
    """Execute without demo-mode suppression. Used by demo seeding only."""
    # (copy of the existing execute() body, with no demo guard)
    ...


def execute(statement: str, parameters: list = None) -> list[dict]:
    # Demo mode: suppress all DML silently
    if _is_demo_mode() and _DML_RE.match(statement):
        return []
    # ... existing implementation unchanged ...
```

Key detail: `_raw_execute()` is the existing implementation body extracted verbatim. `execute()` delegates to it after the demo guard.

---

### Step 4 — Modify `utils/auth.py`

```python
def get_user_email() -> str:
    try:
        import streamlit as st
        if st.session_state.get("demo_mode"):
            demo_id = st.session_state.get("demo_profile_id", "3a")
            from utils.demo import DEMO_PROFILES
            return DEMO_PROFILES[demo_id]["email"]
    except Exception:
        pass
    email = os.environ.get("DATABRICKS_USER_EMAIL")
    if not email:
        email = os.environ.get("DEV_USER_EMAIL", "dev@example.com")
    return email
```

---

### Step 5 — Modify `app.py`

Add demo mode detection, profile dropdown, and profile switch handler at the top of `app.py`
(before the user state check):

```python
import os
LOCAL_UAT = os.environ.get("LOCAL_UAT", "").lower() == "true"

# ── Demo Mode detection ───────────────────────────────────────────────────────
if LOCAL_UAT:
    from utils.demo import DEMO_PROFILES, DEFAULT_PROFILE, ensure_demo_seeded
    params = st.query_params
    if params.get("demo") == "true":
        # First load: initialize demo mode session state
        if "demo_mode" not in st.session_state:
            profile_id = params.get("profile", DEFAULT_PROFILE)
            if profile_id not in DEMO_PROFILES:
                profile_id = DEFAULT_PROFILE
            st.session_state["demo_mode"] = True
            st.session_state["demo_profile_id"] = profile_id
            ensure_demo_seeded(profile_id)
            # Clear routing state so app re-derives from seeded data
            for key in ["user_email", "user_state", "role_id"]:
                st.session_state.pop(key, None)
            st.rerun()

        # Render demo profile dropdown in sidebar
        with st.sidebar:
            st.markdown("**🎭 Demo Mode**")
            profile_labels = {pid: p["label"] for pid, p in DEMO_PROFILES.items()}
            current_id = st.session_state.get("demo_profile_id", DEFAULT_PROFILE)
            selected_label = st.selectbox(
                "Demo profile",
                options=list(profile_labels.values()),
                index=list(profile_labels.keys()).index(current_id),
                key="demo_profile_select",
                label_visibility="collapsed",
            )
            # Detect profile change
            selected_id = next(k for k, v in profile_labels.items() if v == selected_label)
            if selected_id != current_id:
                ensure_demo_seeded(selected_id)
                # Full session state reset
                keys_to_clear = [
                    k for k in st.session_state
                    if k not in ("demo_mode", "demo_profile_id", "demo_profile_select")
                ]
                for k in keys_to_clear:
                    del st.session_state[k]
                st.session_state["demo_profile_id"] = selected_id
                st.rerun()
            st.divider()
```

URL format to enter demo mode:
- `http://localhost:8501/?demo=true` → loads profile 3a (default)
- `http://localhost:8501/?demo=true&profile=3c` → loads profile 3c directly

---

### Step 6 — UAT testing

Run the Playwright UAT against demo mode URLs:

```bash
bash run_uat.sh
```

Manual checks (4 scenarios):

```text
1. ?demo=true               → Welcome page; no DB writes on role select
2. ?demo=true&profile=3b    → Diagnostic page for RM; questions load correctly
3. ?demo=true&profile=3c    → Home page; Module 1 complete (all 3 badges ✓); gap map visible on Skills Profile
4. ?demo=true&profile=3d    → Home page; all 7 modules complete; overall score ≥ 3.0
```

Also verify:
- [ ] Switching profile 3c → 3d refreshes to new state (new email, new rows)
- [ ] Completing a quiz step in demo mode (3b → finish diagnostic) shows results but no new `diagnostic_sessions` row
- [ ] Demo indicator visible in sidebar when `?demo=true`
- [ ] No demo UI elements when `?demo=true` is absent

---

### Step 7 — Commit and merge

```bash
git add utils/demo.py utils/db.py utils/auth.py app.py
git commit -m "feat(demo): add Demo Mode with 4 fixture personas (3a–3d)"
git checkout main
git merge feature/demo-mode
```

---

## Acceptance Checks

- [ ] `?demo=true` with no profile → Welcome page (profile 3a)
- [ ] `?demo=true&profile=3b` → Diagnostic page for RM user "Alex Chen (Demo)"
- [ ] `?demo=true&profile=3c` → Home page; Module 1 shown as complete (all 3 sub-badges ✓); gap map bullets visible on Skills Profile
- [ ] `?demo=true&profile=3d` → Home page; all 7 modules complete; score ≥ 3.0 in summary card
- [ ] Profile dropdown visible in sidebar top-left when demo mode active
- [ ] Switching profile 3c → 3d → page refreshes and shows AN state (different username, different modules)
- [ ] Completing a mock quiz in demo mode: AI scores and shows results, but no new rows in `diagnostic_sessions` or `training_progress`
- [ ] No demo UI visible when `?demo=true` is absent
- [ ] No demo UI visible in deployed app (only when `LOCAL_UAT=true`)

---

## Out of Scope

- Demo mode in deployed Databricks App (only local UAT)
- Seeding via scripts (lazy seeding in-app is sufficient)
- Dedicated demo email clean-up job (demo rows are tiny; clean up manually if needed via `reset_uat_user.py`)
- Demo mode for diagnostic questions (3b reaches Diagnostic but the form works as normal; quiz responses go through AI scoring but are not persisted)
