"""
Reset UAT test-user data in Firestore.

Run this before each clean UAT pass to delete all learner docs
for DEV_USER_EMAIL so the app starts from the Welcome page.

Usage:
    python scripts/reset_uat_user.py
        → Full wipe; app opens on Welcome page

    python scripts/reset_uat_user.py --role rm
        → Wipe + seed user_profiles (role_id=rm); app opens on Diagnostic

    python scripts/reset_uat_user.py --role rm --diag
        → Wipe + seed user_profiles + diagnostic_sessions + gap_maps;
          app opens on Skills Profile

    python scripts/reset_uat_user.py --profile course-built
        → Wipe + seed RM profile + diagnostic + gap_map + 7 training_progress rows
          (Module 1 unlocked, not started; Modules 2–7 locked)

    python scripts/reset_uat_user.py --profile m1-done
        → Wipe + seed RM profile with Module 1 complete + Module 2 unlocked

    python scripts/reset_uat_user.py --profile all-done
        → Wipe + seed RM profile with all 7 modules complete

Reads credentials from .env in the project root (same as run_uat.sh).
"""
import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path so utils/ is importable
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env from project root
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from utils.db import (  # noqa: E402 — must be after load_dotenv
    _get_db, create_profile, save_diagnostic, save_gap_map,
    create_progress, update_progress,
)

EMAIL = os.environ.get("DEV_USER_EMAIL", "dev@example.com")

# ── CLI args ────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Reset UAT user data in Firestore")

_mode = parser.add_mutually_exclusive_group()
_mode.add_argument(
    "--role",
    choices=["rm", "uw", "mk"],
    help="Seed a user_profiles doc for this role after wiping (app lands on Diagnostic)",
)
_mode.add_argument(
    "--profile",
    choices=["course-built", "m1-done", "all-done"],
    help=(
        "Seed a mid-journey fixture state for RM (app lands on Home). "
        "course-built: Module 1 unlocked, not started. "
        "m1-done: Module 1 complete, Module 2 unlocked. "
        "all-done: all 7 modules complete."
    ),
)
parser.add_argument(
    "--diag",
    action="store_true",
    help="Also seed diagnostic_sessions + gap_maps (requires --role; app lands on Skills Profile)",
)
args = parser.parse_args()

if args.diag and not args.role:
    parser.error("--diag requires --role")

# ── Helpers ──────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _wipe_user(email: str) -> None:
    db = _get_db()
    cols = ["training_progress", "gap_maps", "diagnostic_sessions", "coach_sessions"]
    for col in cols:
        docs = db.collection(col).where("user_email", "==", email).stream()
        for doc in docs:
            doc.reference.delete()
            print(f"  [deleted] {col}/{doc.id}")
    db.collection("user_profiles").document(email).delete()
    print(f"  [deleted] user_profiles/{email}")

# ── Wipe ────────────────────────────────────────────────────────────────────

print(f"Resetting UAT data for: {EMAIL}")
if args.role:
    print(f"Mode: --role {args.role}" + (" --diag" if args.diag else ""))
elif args.profile:
    print(f"Mode: --profile {args.profile}")
print()

_wipe_user(EMAIL)
print()

# ── Seed: --role ─────────────────────────────────────────────────────────────

if args.role:
    _name_map = {"rm": "RM Tester", "uw": "UW Tester", "mk": "MK Tester"}
    display_name = _name_map.get(args.role, f"{args.role.upper()} Tester")
    create_profile(EMAIL, display_name, args.role)
    print(f"  [ok] seeded user_profiles  (role_id={args.role}, display_name={display_name!r})")

# ── Seed: --diag ─────────────────────────────────────────────────────────────

if args.diag:
    now = _now_iso()
    session_id = str(uuid.uuid4())
    gap_map_id = str(uuid.uuid4())

    domain_scores = {
        "responsible_ai":      2.0,
        "strategic_prompting": 1.5,
        "critical_eval":       1.0,
        "relationship_intel":  1.5,
        "data_decision":       2.0,
        "augmented_comm":      1.5,
    }
    overall_score = round(sum(domain_scores.values()) / len(domain_scores), 2)

    bullets = [
        {"priority": 1, "domain_id": "critical_eval",
         "bullet": "Critical Evaluation (1.0): Practise reviewing AI outputs for accuracy before acting — challenge AI-generated summaries with at least one verification step."},
        {"priority": 2, "domain_id": "strategic_prompting",
         "bullet": "Strategic Prompting (1.5): Build more structured, context-rich prompts for your workflows — include client context, desired output format, and explicit constraints."},
        {"priority": 3, "domain_id": "relationship_intel",
         "bullet": "Relationship Intelligence (1.5): Explore using AI to prepare personalised client briefings and surface relationship patterns across your portfolio."},
    ]

    save_diagnostic(session_id, EMAIL, now, json.dumps({}), json.dumps({}),
                    json.dumps(domain_scores), overall_score)
    print(f"  [ok] seeded diagnostic_sessions  (session_id={session_id})")

    save_gap_map(gap_map_id, EMAIL, "diagnostic", session_id, json.dumps(bullets))
    print(f"  [ok] seeded gap_maps  (gap_map_id={gap_map_id})")

# ── Seed: --profile ──────────────────────────────────────────────────────────

if args.profile:
    from utils.content import COURSES  # noqa: E402

    rm_courses_sorted = sorted(
        [(cid, c) for cid, c in COURSES.items() if c.get("role_id") == "rm"],
        key=lambda x: x[1].get("sequence_order", 99),
    )
    rm_course_ids = [cid for cid, _ in rm_courses_sorted] or [
        "rm_c1_responsible_ai", "rm_c2_strategic_prompting", "rm_c3_critical_eval",
        "rm_c4_relationship_intel", "rm_c5_data_decision", "rm_c6_augmented_comm", "rm_c7_capstone",
    ]

    now = _now_iso()
    session_id = str(uuid.uuid4())

    _diag_scores = {
        "responsible_ai": 1.2, "strategic_prompting": 2.3, "critical_eval": 1.8,
        "relationship_intel": 1.5, "data_decision": 1.1, "augmented_comm": 1.6,
    }
    overall_score = round(sum(_diag_scores.values()) / len(_diag_scores), 2)

    _bullets_inprogress = [
        {"priority": 1, "domain_id": "responsible_ai",
         "bullet": "Your responses show difficulty distinguishing high-risk from low-risk AI use cases — prioritise the Responsible AI module."},
        {"priority": 2, "domain_id": "data_decision",
         "bullet": "Data interpretation tasks revealed uncertainty — the Data-Driven Decision Making module will strengthen your analytical confidence."},
        {"priority": 3, "domain_id": "strategic_prompting",
         "bullet": "Prompting quality improved notably in Module 1 — build on this momentum with chain-of-thought structures."},
    ]
    _bullets_alldone = [
        {"priority": 1, "domain_id": "critical_eval",
         "bullet": "You've reached Proficient level across all six AI domains — focus on applying structured prompting frameworks."},
        {"priority": 2, "domain_id": "strategic_prompting",
         "bullet": "Your critical evaluation skills are approaching expert level — challenge yourself further with real-time fact-checking."},
        {"priority": 3, "domain_id": "augmented_comm",
         "bullet": "Augmented Communication is your strongest domain — leverage this for stakeholder reporting."},
    ]

    _eval_scores = [3.2, 3.0, 2.8, 3.1, 2.9, 3.4, 3.1]
    _domain_scores_after = [3.1, 3.0, 2.9, 3.2, 2.8, 3.5, 3.3]

    create_profile(EMAIL, "UAT Tester RM", "rm")
    print(f"  [ok] seeded user_profiles  (role_id=rm)")

    save_diagnostic(session_id, EMAIL, now, json.dumps({}), json.dumps({}),
                    json.dumps(_diag_scores), overall_score)
    print(f"  [ok] seeded diagnostic_sessions  (overall={overall_score})")

    bullets = _bullets_alldone if args.profile == "all-done" else _bullets_inprogress
    save_gap_map(str(uuid.uuid4()), EMAIL, "diagnostic", session_id, json.dumps(bullets))
    print(f"  [ok] seeded gap_maps")

    for i, course_id in enumerate(rm_course_ids):
        seq = i + 1
        if args.profile == "course-built":
            create_progress(EMAIL, course_id, seq, is_locked=(seq > 1))
        elif args.profile == "m1-done":
            if seq == 1:
                create_progress(EMAIL, course_id, seq, is_locked=False)
                update_progress(EMAIL, course_id,
                    reading_completed_at=now, practice_completed_at=now,
                    evaluation_completed_at=now, evaluation_score=2.8, domain_score_after=2.1)
            elif seq == 2:
                create_progress(EMAIL, course_id, seq, is_locked=False)
            else:
                create_progress(EMAIL, course_id, seq, is_locked=True)
        elif args.profile == "all-done":
            create_progress(EMAIL, course_id, seq, is_locked=False)
            update_progress(EMAIL, course_id,
                reading_completed_at=now, practice_completed_at=now,
                evaluation_completed_at=now,
                evaluation_score=_eval_scores[i],
                domain_score_after=_domain_scores_after[i])

    print(f"  [ok] seeded training_progress  ({len(rm_course_ids)} rows, profile={args.profile!r})")

# ── Done ─────────────────────────────────────────────────────────────────────

print()
if args.profile:
    labels = {
        "course-built": "Home page (Module 1 unlocked, not started).",
        "m1-done":       "Home page (Module 1 complete, Module 2 unlocked).",
        "all-done":      "Home page (all 7 modules complete).",
    }
    print(f"Done. App will open on the {labels[args.profile]}")
elif not args.role:
    print("Done. App will open on the Welcome page.")
elif not args.diag:
    print("Done. App will open on the Diagnostic page.")
else:
    print("Done. App will open on the Skills Profile page.")
print("Run: python -m streamlit run app.py --server.port 8502")
