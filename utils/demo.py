"""
Demo Mode — fixture profiles for local UAT and stakeholder demos.

Activated via ?demo=true URL param when LOCAL_UAT=true.
Personas are pre-seeded into Firestore lazily on first selection.
All DB writes (DML) are suppressed while demo mode is active.
"""
import uuid
import json
from datetime import datetime, timezone
from utils.db import (
    _get_db,
    create_profile, save_diagnostic, save_gap_map, create_progress, update_progress,
)
from google.cloud import firestore as _fs

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
    "3e": {
        "label": "3e — MK, Module 3 in progress",
        "email": "demo-mk-m3@demo.local",
        "role_id": "mk",
        "display_name": "Morgan Patel (Demo)",
    },
}

DEFAULT_PROFILE = "3a"

# ── Fixture data ──────────────────────────────────────────────────────────────

_DIAG_DOMAIN_SCORES_3C = {
    "responsible_ai": 1.2,
    "strategic_prompting": 2.3,
    "critical_eval": 1.8,
    "relationship_intel": 1.5,
    "data_decision": 1.1,
    "augmented_comm": 1.6,
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
    "responsible_ai": 2.1,
    "strategic_prompting": 2.4,
    "critical_eval": 1.9,
    "relationship_intel": 2.0,
    "data_decision": 1.8,
    "augmented_comm": 2.3,
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

# UW course IDs in sequence order (matches content/courses.json)
_UW_COURSES = [
    "uw_c1_responsible_ai",
    "uw_c2_strategic_prompting",
    "uw_c3_critical_eval",
    "uw_c4_relationship_intel",
    "uw_c5_data_decision",
    "uw_c6_augmented_comm",
    "uw_c7_capstone",
]

# AN course IDs in sequence order (matches content/courses.json)
_AN_COURSES = [
    "an_c1_responsible_ai",
    "an_c2_strategic_prompting",
    "an_c3_critical_eval",
    "an_c4_relationship_intel",
    "an_c5_data_decision",
    "an_c6_augmented_comm",
    "an_c7_capstone",
]

_AN_MODULE_EVAL_SCORES = [3.2, 3.0, 2.8, 3.1, 2.9, 3.4, 3.1]
_AN_MODULE_DOMAIN_SCORES = [3.1, 3.0, 2.9, 3.2, 2.8, 3.5, 3.3]

# MK — modules 1 & 2 complete, module 3 reading done (halfway through)
_DIAG_DOMAIN_SCORES_3E = {
    "responsible_ai": 1.4,
    "strategic_prompting": 1.7,
    "critical_eval": 1.1,
    "relationship_intel": 1.6,
    "data_decision": 1.3,
    "augmented_comm": 2.0,
}

_GAP_BULLETS_3E = [
    "Your diagnostic revealed gaps in evaluating AI-generated content for accuracy and "
    "bias — the Critical Evaluation module is your highest priority and unlocks first.",
    "Responsible AI responses showed uncertainty around disclosure obligations in "
    "marketing communications — this module will help you apply the right guardrails "
    "before campaigns go live.",
    "Strategic Prompting showed strong instincts but inconsistent structure — "
    "Module 2 builds the repeatable frameworks that will make your AI-assisted "
    "content workflows more predictable.",
    "Augmented Communication is your strongest domain — continue leveraging this "
    "by applying AI tools to stakeholder briefs and executive summaries.",
]

_MK_COURSES = [
    "mk_c1_responsible_ai",
    "mk_c2_strategic_prompting",
    "mk_c3_critical_eval",
    "mk_c4_relationship_intel",
    "mk_c5_data_decision",
    "mk_c6_augmented_comm",
    "mk_c7_capstone",
]

_MK_MODULE_EVAL_SCORES = [3.1, 2.9]
_MK_MODULE_DOMAIN_SCORES = [2.2, 2.5]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _wipe_demo_user(email: str) -> None:
    """Delete all Firestore docs for a demo email (for clean re-seed)."""
    db = _get_db()
    collections = [
        "training_progress",
        "gap_maps",
        "diagnostic_sessions",
        "coach_sessions",
    ]
    for col in collections:
        docs = db.collection(col).where("user_email", "==", email).stream()
        for doc in docs:
            doc.reference.delete()
    # user_profiles uses email as doc ID
    db.collection("user_profiles").document(email).delete()


def ensure_demo_seeded(profile_id: str) -> None:
    """
    Seed fixture data for a demo profile into Firestore.
    Wipes existing data for this demo email first, then re-inserts.
    """
    profile = DEMO_PROFILES.get(profile_id)
    if not profile:
        return
    email = profile["email"]
    _wipe_demo_user(email)

    if profile_id == "3a":
        return  # fresh user — no rows needed

    # user_profiles
    create_profile(email, profile["display_name"], profile["role_id"])

    if profile_id == "3b":
        return  # RM at diagnostic start — only profile row needed

    # diagnostic_sessions (3c, 3d, 3e)
    _score_map = {"3c": _DIAG_DOMAIN_SCORES_3C, "3d": _DIAG_DOMAIN_SCORES_3D, "3e": _DIAG_DOMAIN_SCORES_3E}
    domain_scores = _score_map.get(profile_id, _DIAG_DOMAIN_SCORES_3D)
    overall = round(sum(domain_scores.values()) / len(domain_scores), 2)
    session_id = str(uuid.uuid4())
    save_diagnostic(
        session_id, email, _now_iso(),
        json.dumps({}),
        json.dumps({}),
        json.dumps(domain_scores),
        overall,
    )

    # gap_maps
    _bullets_map = {"3c": _GAP_BULLETS_3C, "3d": _GAP_BULLETS_3D, "3e": _GAP_BULLETS_3E}
    bullets = _bullets_map.get(profile_id, _GAP_BULLETS_3D)
    # Wrap as list of dicts to match the format written by the actual diagnostic flow
    bullets_list = [{"priority": i + 1, "domain_id": "", "bullet": b} for i, b in enumerate(bullets)]
    save_gap_map(str(uuid.uuid4()), email, "diagnostic", session_id, json.dumps(bullets_list))

    # training_progress
    if profile_id == "3c":
        for i, course_id in enumerate(_UW_COURSES):
            seq = i + 1
            create_progress(email, course_id, seq, is_locked=(seq > 1))
            if seq == 1:
                update_progress(email, course_id,
                    reading_completed_at=_now_iso(),
                    practice_completed_at=_now_iso(),
                    evaluation_completed_at=_now_iso(),
                    evaluation_score=2.8,
                    domain_score_after=2.1,
                    is_locked=False,
                )

    elif profile_id == "3d":
        for i, course_id in enumerate(_AN_COURSES):
            seq = i + 1
            create_progress(email, course_id, seq, is_locked=False)
            update_progress(email, course_id,
                reading_completed_at=_now_iso(),
                practice_completed_at=_now_iso(),
                evaluation_completed_at=_now_iso(),
                evaluation_score=_AN_MODULE_EVAL_SCORES[i],
                domain_score_after=_AN_MODULE_DOMAIN_SCORES[i],
            )

    elif profile_id == "3e":
        for i, course_id in enumerate(_MK_COURSES):
            seq = i + 1
            if seq <= 2:
                create_progress(email, course_id, seq, is_locked=False)
                update_progress(email, course_id,
                    reading_completed_at=_now_iso(),
                    practice_completed_at=_now_iso(),
                    evaluation_completed_at=_now_iso(),
                    evaluation_score=_MK_MODULE_EVAL_SCORES[i],
                    domain_score_after=_MK_MODULE_DOMAIN_SCORES[i],
                )
            elif seq == 3:
                create_progress(email, course_id, seq, is_locked=False)
                update_progress(email, course_id, reading_completed_at=_now_iso())
            else:
                create_progress(email, course_id, seq, is_locked=True)
