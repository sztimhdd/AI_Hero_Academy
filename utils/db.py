"""
Firestore database layer for AI Hero Academy.

Replaces Databricks Delta tables with GCP Firestore collections.
Maintains same API interface (execute, query_one) for backward compatibility.

Firestore Schema:
- users/{user_email} → user_profiles
- users/{user_email}/diagnostic_sessions/{session_id}
- users/{user_email}/gap_maps/{gap_map_id}
- users/{user_email}/training_progress/{progress_id}
- users/{user_email}/coach_sessions/{session_id}
- ai_call_log/{log_id} → top-level collection
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from google.cloud import firestore

_client = None


def _get_client() -> firestore.Client:
    """Get Firestore client instance."""
    global _client
    if _client is None:
        project_id = os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            raise RuntimeError("GCP_PROJECT_ID environment variable not set")
        _client = firestore.Client(project=project_id)
    return _client


def execute(statement: str, parameters: list = None) -> List[Dict]:
    """
    Execute a 'SQL-like' statement against Firestore.

    This function parses simplified SQL statements and converts them to Firestore operations.
    Supports: SELECT, INSERT, UPDATE for the 6 main collections.

    Returns list of dicts (same interface as original Databricks version).
    """
    statement = statement.strip()

    # Parse statement type
    if statement.upper().startswith("SELECT"):
        return _execute_select(statement, parameters)
    elif statement.upper().startswith("INSERT"):
        return _execute_insert(statement, parameters)
    elif statement.upper().startswith("UPDATE"):
        return _execute_update(statement, parameters)
    else:
        raise RuntimeError(f"Unsupported statement type: {statement[:20]}...")


def query_one(statement: str, parameters: list = None) -> Optional[Dict]:
    """Execute a statement and return the first row, or None."""
    rows = execute(statement, parameters)
    return rows[0] if rows else None


def escape(s: str) -> str:
    """Legacy function for SQL compatibility - no-op in Firestore."""
    return s


def _execute_select(statement: str, parameters: list = None) -> List[Dict]:
    """Parse SELECT statement and execute Firestore query."""
    db = _get_client()

    # Simple parser for the 6 main table patterns used in the app
    statement_lower = statement.lower()

    if "user_profiles" in statement_lower:
        user_email = parameters[0] if parameters else None
        if user_email:
            doc = db.collection("users").document(user_email).get()
            return [doc.to_dict()] if doc.exists else []
        return []

    elif "diagnostic_sessions" in statement_lower:
        user_email = parameters[0] if parameters else None
        if user_email:
            if "completed_at is not null" in statement_lower:
                # Get completed sessions only
                sessions = db.collection("users").document(user_email).collection("diagnostic_sessions").where("completed_at", "!=", None).stream()
            else:
                sessions = db.collection("users").document(user_email).collection("diagnostic_sessions").stream()
            return [doc.to_dict() for doc in sessions]
        return []

    elif "gap_maps" in statement_lower:
        user_email = parameters[0] if parameters else None
        if user_email:
            maps = db.collection("users").document(user_email).collection("gap_maps").stream()
            return [doc.to_dict() for doc in maps]
        return []

    elif "training_progress" in statement_lower:
        user_email = parameters[0] if parameters else None
        if user_email:
            progress = db.collection("users").document(user_email).collection("training_progress").stream()
            return [doc.to_dict() for doc in progress]
        return []

    elif "coach_sessions" in statement_lower:
        user_email = parameters[0] if parameters else None
        if user_email:
            sessions = db.collection("users").document(user_email).collection("coach_sessions").stream()
            return [doc.to_dict() for doc in sessions]
        return []

    elif "ai_call_log" in statement_lower:
        # Top-level collection
        logs = db.collection("ai_call_log").stream()
        return [doc.to_dict() for doc in logs]

    else:
        raise RuntimeError(f"Unsupported SELECT statement: {statement[:50]}...")


def _execute_insert(statement: str, parameters: list = None) -> List[Dict]:
    """Parse INSERT statement and execute Firestore write."""
    db = _get_client()
    statement_lower = statement.lower()

    if "user_profiles" in statement_lower:
        # Extract values from INSERT statement (simplified parser)
        # Expected: INSERT INTO users (user_email, display_name, role_id) VALUES (?, ?, ?)
        if parameters and len(parameters) >= 3:
            user_email, display_name, role_id = parameters[0], parameters[1], parameters[2]
            doc_data = {
                "user_email": user_email,
                "display_name": display_name,
                "role_id": role_id,
                "created_at": datetime.now()
            }
            db.collection("users").document(user_email).set(doc_data)
            return [doc_data]

    elif "diagnostic_sessions" in statement_lower:
        if parameters and len(parameters) >= 8:
            session_id, user_email = parameters[0], parameters[1]
            doc_data = {
                "session_id": session_id,
                "user_email": user_email,
                "started_at": datetime.now(),
                "completed_at": datetime.now() if parameters[2] else None,
                "responses": parameters[3] or "{}",
                "item_scores": parameters[4] or "{}",
                "domain_scores": parameters[5] or "{}",
                "overall_score": float(parameters[6]) if parameters[6] else 0.0
            }
            db.collection("users").document(user_email).collection("diagnostic_sessions").document(session_id).set(doc_data)
            return [doc_data]

    elif "gap_maps" in statement_lower:
        if parameters and len(parameters) >= 5:
            gap_map_id, user_email = parameters[0], parameters[1]
            doc_data = {
                "gap_map_id": gap_map_id,
                "user_email": user_email,
                "source_type": parameters[2],
                "source_id": parameters[3],
                "bullets": parameters[4],
                "generated_at": datetime.now()
            }
            db.collection("users").document(user_email).collection("gap_maps").document(gap_map_id).set(doc_data)
            return [doc_data]

    elif "training_progress" in statement_lower:
        if parameters and len(parameters) >= 5:
            progress_id, user_email = parameters[0], parameters[1]
            doc_data = {
                "progress_id": progress_id,
                "user_email": user_email,
                "course_id": parameters[2],
                "module_sequence_order": int(parameters[3]),
                "is_locked": bool(parameters[4]) if parameters[4] is not None else True,
                "reading_completed_at": None,
                "practice_completed_at": None,
                "evaluation_score": None,
                "evaluation_completed_at": None,
                "domain_score_after": None
            }
            db.collection("users").document(user_email).collection("training_progress").document(progress_id).set(doc_data)
            return [doc_data]

    elif "coach_sessions" in statement_lower:
        if parameters and len(parameters) >= 4:
            session_id, user_email = parameters[0], parameters[1]
            doc_data = {
                "session_id": session_id,
                "user_email": user_email,
                "course_id": parameters[2],
                "started_at": datetime.now(),
                "completed_at": None,
                "turn_count": 0,
                "conversation_json": parameters[3] or "[]"
            }
            db.collection("users").document(user_email).collection("coach_sessions").document(session_id).set(doc_data)
            return [doc_data]

    elif "ai_call_log" in statement_lower:
        if parameters and len(parameters) >= 6:
            log_id = parameters[0]
            doc_data = {
                "log_id": log_id,
                "user_email": parameters[1],
                "call_type": parameters[2],
                "model_endpoint": parameters[3],
                "prompt_tokens": int(parameters[4]) if parameters[4] else None,
                "completion_tokens": int(parameters[5]) if parameters[5] else None,
                "latency_ms": int(parameters[6]) if len(parameters) > 6 else 0,
                "success": bool(parameters[7]) if len(parameters) > 7 else True,
                "error_message": parameters[8] if len(parameters) > 8 else None,
                "called_at": datetime.now()
            }
            db.collection("ai_call_log").document(log_id).set(doc_data)
            return [doc_data]

    return []


def _execute_update(statement: str, parameters: list = None) -> List[Dict]:
    """Parse UPDATE statement and execute Firestore update."""
    db = _get_client()
    statement_lower = statement.lower()

    if "training_progress" in statement_lower:
        # Most UPDATE statements are for training_progress
        # Pattern: UPDATE training_progress SET field=? WHERE user_email=? AND course_id=?
        if parameters and len(parameters) >= 3:
            field_value, user_email = parameters[0], parameters[1]

            # Find the document to update
            progress_docs = db.collection("users").document(user_email).collection("training_progress").stream()

            for doc in progress_docs:
                doc_data = doc.to_dict()
                if len(parameters) > 2 and doc_data.get("course_id") == parameters[2]:
                    # Determine which field to update based on statement content
                    update_data = {}
                    if "reading_completed_at" in statement_lower:
                        update_data["reading_completed_at"] = datetime.now()
                    elif "practice_completed_at" in statement_lower:
                        update_data["practice_completed_at"] = datetime.now()
                    elif "evaluation_score" in statement_lower:
                        update_data["evaluation_score"] = float(field_value)
                        update_data["evaluation_completed_at"] = datetime.now()
                    elif "domain_score_after" in statement_lower:
                        update_data["domain_score_after"] = float(field_value)
                    elif "is_locked" in statement_lower:
                        update_data["is_locked"] = bool(field_value)

                    if update_data:
                        doc.reference.update(update_data)
                        return [doc_data | update_data]

    return []
