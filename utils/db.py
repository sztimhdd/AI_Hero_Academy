"""
utils/db.py — Phase B: Firestore data layer.

All learner reads/writes go to Google Cloud Firestore.
Flat top-level collections mirror the old Delta schema exactly.

Collections:
  user_profiles/{user_email}
  diagnostic_sessions/{session_id}
  gap_maps/{gap_map_id}
  training_progress/{user_email}_{course_id}
  coach_sessions/{session_id}
  ai_call_log/{log_id}
"""
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
from google.cloud import firestore
from google.cloud.firestore import SERVER_TIMESTAMP

# Load .env from project root so credentials work regardless of how app is started.
load_dotenv(Path(__file__).parent.parent / ".env")

_db = None


def _get_db() -> firestore.Client:
    global _db
    if _db is None:
        project_id = os.environ.get("GCP_PROJECT_ID")
        # Resolve GOOGLE_APPLICATION_CREDENTIALS relative to project root if it's relative.
        creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if creds and not os.path.isabs(creds):
            abs_creds = str(Path(__file__).parent.parent / creds)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = abs_creds
        _db = firestore.Client(project=project_id)
    return _db


def _progress_key(user_email: str, course_id: str) -> str:
    return f"{user_email}_{course_id}"


# Set to True by ensure_demo_seeded() so db writes bypass the demo guard during seeding.
_DEMO_SEED_IN_PROGRESS: bool = False


def _is_demo_mode() -> bool:
    if _DEMO_SEED_IN_PROGRESS:
        return False
    try:
        import streamlit as st
        return bool(st.session_state.get("demo_mode"))
    except Exception:
        return False


def _ts_to_str(val) -> str | None:
    """Normalise Firestore DatetimeWithNanoseconds / datetime / string to ISO string."""
    if val is None:
        return None
    if hasattr(val, "isoformat"):
        return val.isoformat()
    return str(val)


# ── User profiles ────────────────────────────────────────────────────────────

def get_profile(user_email: str) -> dict | None:
    doc = _get_db().collection("user_profiles").document(user_email).get()
    if not doc.exists:
        return None
    d = doc.to_dict()
    d["user_email"] = user_email
    return d


def create_profile(user_email: str, display_name: str, role_id: str) -> None:
    _get_db().collection("user_profiles").document(user_email).set({
        "role_id": role_id,
        "display_name": display_name,
        "created_at": SERVER_TIMESTAMP,
    })


# ── Diagnostic sessions ───────────────────────────────────────────────────────

def get_latest_diagnostic(user_email: str) -> dict | None:
    # Fetch all sessions for this user, filter + sort in Python to avoid composite index.
    docs = (
        _get_db().collection("diagnostic_sessions")
        .where("user_email", "==", user_email)
        .stream()
    )
    rows = []
    for doc in docs:
        d = doc.to_dict()
        if d.get("completed_at") is None:
            continue
        d["session_id"] = doc.id
        d["completed_at"] = _ts_to_str(d.get("completed_at"))
        rows.append(d)
    if not rows:
        return None
    return sorted(rows, key=lambda r: r.get("completed_at") or "", reverse=True)[0]


def get_all_diagnostics(user_email: str) -> list[dict]:
    docs = (
        _get_db().collection("diagnostic_sessions")
        .where("user_email", "==", user_email)
        .stream()
    )
    rows = []
    for doc in docs:
        d = doc.to_dict()
        if d.get("completed_at") is None:
            continue
        d["session_id"] = doc.id
        d["completed_at"] = _ts_to_str(d.get("completed_at"))
        rows.append(d)
    return sorted(rows, key=lambda r: r.get("completed_at") or "", reverse=True)


def save_diagnostic(
    session_id: str,
    user_email: str,
    started_at: str,
    responses_json: str,
    item_scores_json: str,
    domain_scores_json: str,
    overall_score: float,
) -> None:
    _get_db().collection("diagnostic_sessions").document(session_id).set({
        "user_email": user_email,
        "started_at": started_at,
        "completed_at": SERVER_TIMESTAMP,
        "responses": responses_json,
        "item_scores": item_scores_json,
        "domain_scores": domain_scores_json,
        "overall_score": float(overall_score),
    })


# ── Gap maps ──────────────────────────────────────────────────────────────────

def get_latest_gap_map(user_email: str) -> dict | None:
    # Sort in Python to avoid composite index on (user_email, generated_at).
    docs = (
        _get_db().collection("gap_maps")
        .where("user_email", "==", user_email)
        .stream()
    )
    rows = []
    for doc in docs:
        d = doc.to_dict()
        d["gap_map_id"] = doc.id
        rows.append(d)
    if not rows:
        return None
    return sorted(rows, key=lambda r: str(r.get("generated_at") or ""), reverse=True)[0]


def save_gap_map(
    gap_map_id: str,
    user_email: str,
    source_type: str,
    source_id: str,
    bullets_json: str,
) -> None:
    _get_db().collection("gap_maps").document(gap_map_id).set({
        "user_email": user_email,
        "source_type": source_type,
        "source_id": source_id,
        "bullets": bullets_json,
        "generated_at": SERVER_TIMESTAMP,
    })


# ── Training progress ─────────────────────────────────────────────────────────

def get_all_progress(user_email: str) -> list[dict]:
    # Sort in Python to avoid composite index on (user_email, module_sequence_order).
    docs = (
        _get_db().collection("training_progress")
        .where("user_email", "==", user_email)
        .stream()
    )
    rows = []
    for doc in docs:
        d = doc.to_dict()
        d["progress_id"] = doc.id
        # Normalise timestamp fields to strings for consistency with old SQL layer
        for ts_field in ("reading_completed_at", "practice_completed_at", "evaluation_completed_at"):
            d[ts_field] = _ts_to_str(d.get(ts_field))
        rows.append(d)
    return sorted(rows, key=lambda r: r.get("module_sequence_order", 0))


def get_progress(user_email: str, course_id: str) -> dict | None:
    doc = _get_db().collection("training_progress").document(
        _progress_key(user_email, course_id)
    ).get()
    if not doc.exists:
        return None
    d = doc.to_dict()
    d["progress_id"] = doc.id
    for ts_field in ("reading_completed_at", "practice_completed_at", "evaluation_completed_at"):
        d[ts_field] = _ts_to_str(d.get(ts_field))
    return d


def get_progress_by_seq(user_email: str, seq: int) -> dict | None:
    docs = (
        _get_db().collection("training_progress")
        .where("user_email", "==", user_email)
        .where("module_sequence_order", "==", seq)
        .limit(1)
        .stream()
    )
    for doc in docs:
        d = doc.to_dict()
        d["progress_id"] = doc.id
        return d
    return None


def get_any_progress(user_email: str) -> dict | None:
    docs = (
        _get_db().collection("training_progress")
        .where("user_email", "==", user_email)
        .limit(1)
        .stream()
    )
    for doc in docs:
        d = doc.to_dict()
        d["progress_id"] = doc.id
        return d
    return None


def create_progress(user_email: str, course_id: str, seq: int, is_locked: bool) -> None:
    if _is_demo_mode():
        return
    _get_db().collection("training_progress").document(
        _progress_key(user_email, course_id)
    ).set({
        "user_email": user_email,
        "course_id": course_id,
        "module_sequence_order": seq,
        "is_locked": is_locked,
        "reading_completed_at": None,
        "practice_completed_at": None,
        "evaluation_completed_at": None,
        "evaluation_score": None,
        "domain_score_after": None,
    })


def update_progress(user_email: str, course_id: str, **fields) -> None:
    if _is_demo_mode():
        return
    _get_db().collection("training_progress").document(
        _progress_key(user_email, course_id)
    ).update(fields)


def unlock_progress(user_email: str, seq: int) -> None:
    """Set is_locked=False on the progress row with the given sequence order."""
    if _is_demo_mode():
        return
    docs = (
        _get_db().collection("training_progress")
        .where("user_email", "==", user_email)
        .where("module_sequence_order", "==", seq)
        .limit(1)
        .stream()
    )
    for doc in docs:
        doc.reference.update({"is_locked": False})


# ── Coach sessions ────────────────────────────────────────────────────────────

def save_coach_session(
    session_id: str,
    user_email: str,
    course_id: str,
    started_at: str,
    turn_count: int,
    conv_json: str,
) -> None:
    _get_db().collection("coach_sessions").document(session_id).set({
        "user_email": user_email,
        "course_id": course_id,
        "started_at": started_at,
        "completed_at": SERVER_TIMESTAMP,
        "turn_count": turn_count,
        "conversation_json": conv_json,
    })


# ── Backward-compat shim ─────────────────────────────────────────────────────

def escape(s: str) -> str:
    """No-op shim — kept for callers not yet migrated. Safe to call."""
    return s
