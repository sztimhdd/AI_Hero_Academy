"""
Reset UAT test-user data in Delta tables.

Run this before each clean UAT pass to delete all learner-schema rows
for DEV_USER_EMAIL so the app starts from the Welcome page.

Usage:
    python scripts/reset_uat_user.py
        → Full wipe; app opens on Welcome page (default / existing behaviour)

    python scripts/reset_uat_user.py --role rm
        → Wipe + seed user_profiles (role_id=rm); app opens on Diagnostic

    python scripts/reset_uat_user.py --role uw
        → Wipe + seed user_profiles (role_id=uw); app opens on Diagnostic

    python scripts/reset_uat_user.py --role rm --diag
        → Wipe + seed user_profiles + diagnostic_sessions + gap_maps;
          app opens on Skills Profile

    python scripts/reset_uat_user.py --role uw --diag
        → Same as above for the UW role

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

from utils.db import execute  # noqa: E402 — must be after load_dotenv

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")
EMAIL = os.environ.get("DEV_USER_EMAIL", "dev@example.com")

# ── CLI args ────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Reset UAT user data")
parser.add_argument(
    "--role",
    choices=["rm", "uw"],
    help="Seed a user_profiles row for this role after wiping (app lands on Diagnostic)",
)
parser.add_argument(
    "--diag",
    action="store_true",
    help="Also seed a completed diagnostic_sessions + gap_maps row (requires --role; app lands on Skills Profile)",
)
args = parser.parse_args()

if args.diag and not args.role:
    parser.error("--diag requires --role")

# ── Wipe ────────────────────────────────────────────────────────────────────

# Order matters: delete child tables before user_profiles to avoid FK issues
TABLES = [
    "learner.coach_sessions",
    "learner.gap_maps",
    "learner.training_progress",
    "learner.diagnostic_sessions",
    "learner.user_profiles",
]

print(f"Resetting UAT data for: {EMAIL}")
print(f"Catalog: {CATALOG}")
if args.role:
    print(f"Mode: --role {args.role}" + (" --diag" if args.diag else ""))
print()

for table in TABLES:
    execute(f"DELETE FROM {CATALOG}.{table} WHERE user_email = ?", [EMAIL])
    print(f"  [ok] cleared {table}")

# ── Seed: --role ─────────────────────────────────────────────────────────────

if args.role:
    display_name = "RM Tester" if args.role == "rm" else "UW Tester"
    execute(
        f"INSERT INTO {CATALOG}.learner.user_profiles "
        f"(user_email, display_name, role_id, created_at) "
        f"VALUES (?, ?, ?, current_timestamp())",
        [EMAIL, display_name, args.role],
    )
    print(f"\n  [ok] seeded user_profiles  (role_id={args.role}, display_name={display_name!r})")

# ── Seed: --diag ─────────────────────────────────────────────────────────────

if args.diag:
    now = datetime.now(timezone.utc).isoformat()
    session_id = str(uuid.uuid4())
    gap_map_id = str(uuid.uuid4())

    domain_scores = {
        "prompting": 1.5,
        "verification": 1.0,
        "data_safety": 2.0,
        "tool_fluency": 1.5,
    }
    overall_score = 1.5

    # Canned bullets: one per gap/borderline domain (ordered by priority)
    bullets = json.dumps([
        "Verification (1.0): Practise reviewing AI outputs for accuracy and completeness before sharing with clients — challenge AI-generated summaries with at least one follow-up prompt.",
        "Prompting (1.5): Build more structured, context-rich prompts for complex RM scenarios — include client context, desired output format, and explicit constraints.",
        "Tool Fluency (1.5): Explore AI tool integrations for client research and CRM workflows — experiment with chaining tools to reduce manual steps.",
    ])

    execute(
        f"INSERT INTO {CATALOG}.learner.diagnostic_sessions "
        f"(session_id, user_email, started_at, completed_at, "
        f" responses, item_scores, domain_scores, overall_score) "
        f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            session_id,
            EMAIL,
            now,                        # started_at (ISO 8601 → TIMESTAMP)
            now,                        # completed_at (same — canned data)
            json.dumps({}),             # responses — empty (canned)
            json.dumps({}),             # item_scores — empty (canned)
            json.dumps(domain_scores),  # domain_scores
            overall_score,              # overall_score (DOUBLE)
        ],
    )
    print(f"  [ok] seeded diagnostic_sessions  (session_id={session_id})")

    execute(
        f"INSERT INTO {CATALOG}.learner.gap_maps "
        f"(gap_map_id, user_email, source_type, source_id, bullets, generated_at) "
        f"VALUES (?, ?, ?, ?, ?, ?)",
        [
            gap_map_id,
            EMAIL,
            "diagnostic",   # source_type
            session_id,     # source_id → links to the diagnostic session above
            bullets,
            now,
        ],
    )
    print(f"  [ok] seeded gap_maps            (gap_map_id={gap_map_id})")

# ── Done ─────────────────────────────────────────────────────────────────────

print()
if not args.role:
    print("Done. App will open on the Welcome page.")
elif not args.diag:
    print("Done. App will open on the Diagnostic page.")
else:
    print("Done. App will open on the Skills Profile page.")
print("Run ./run_uat.sh and open http://localhost:8501")
