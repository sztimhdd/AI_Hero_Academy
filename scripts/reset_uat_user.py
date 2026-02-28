"""
Deletes all learner-schema rows for DEV_USER_EMAIL.
Run before a clean UAT pass: python scripts/reset_uat_user.py
"""
import os
import sys
import argparse
import uuid
import json
from datetime import datetime, timezone

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from utils.db import execute, _get_client

parser = argparse.ArgumentParser(description="Reset UAT user data")
parser.add_argument("--role", choices=["rm", "uw"], help="Seed a user_profiles row for this role")
parser.add_argument("--diag", action="store_true", help="Also seed a completed diagnostic_sessions + gap_maps row (requires --role)")
args = parser.parse_args()

if args.diag and not args.role:
    parser.error("--diag requires --role")

EMAIL = os.environ.get("DEV_USER_EMAIL", "uat-test@edc.ca")

print(f"Resetting UAT data for: {EMAIL}")

# Use Firestore client directly for deletions since execute() doesn't support DELETE yet.
db = _get_client()
user_ref = db.collection("users").document(EMAIL)

collections_to_delete = [
    "coach_sessions",
    "gap_maps",
    "training_progress",
    "diagnostic_sessions"
]

for sub in collections_to_delete:
    docs = user_ref.collection(sub).stream()
    count = 0
    for doc in docs:
        doc.reference.delete()
        count += 1
    print(f"  ✓ Deleted {count} documents from {sub}")

user_doc = user_ref.get()
if user_doc.exists:
    user_ref.delete()
    print(f"  ✓ Deleted user_profiles")

# 2. --role seed
if args.role:
    display_name = "RM Tester" if args.role == "rm" else "UW Tester"
    execute(
        "INSERT INTO users (user_email, display_name, role_id) VALUES (?, ?, ?)",
        [EMAIL, display_name, args.role]
    )
    print(f"  ✓ Seeded user profile for role: {args.role}")

# 3. --diag seed
if args.diag:
    session_id = str(uuid.uuid4())
    gap_map_id = str(uuid.uuid4())

    domain_scores_json = json.dumps({
        "prompting": 1.5,
        "verification": 1.0,
        "data_safety": 2.0,
        "tool_fluency": 1.5
    })
    
    # Needs 7 parameters: session_id, user_email, started_at, responses, item_scores, domain_scores, overall_score
    execute(
        "INSERT INTO diagnostic_sessions "
        "(session_id, user_email, started_at, completed_at, responses, item_scores, domain_scores, overall_score) "
        "VALUES (?, ?, CAST(? AS TIMESTAMP), current_timestamp(), ?, ?, ?, ?)",
        [session_id, EMAIL, True, "{}", "{}", domain_scores_json, 1.5]
    )
    print(f"  ✓ Seeded diagnostic session: {session_id}")

    bullets = [
        {"priority": 1, "domain_id": "verification", "bullet": "Needs improvement on verification."},
        {"priority": 2, "domain_id": "prompting", "bullet": "Prompting is decent but could be better."},
        {"priority": 3, "domain_id": "tool_fluency", "bullet": "Expand tool fluency usage."}
    ]
    execute(
        "INSERT INTO gap_maps "
        "(gap_map_id, user_email, source_type, source_id, bullets) "
        "VALUES (?, ?, ?, ?, ?)",
        [gap_map_id, EMAIL, "diagnostic", session_id, bullets]
    )
    print(f"  ✓ Seeded gap map: {gap_map_id}")

print("Done.")
