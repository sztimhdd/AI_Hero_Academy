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

    python scripts/reset_uat_user.py --profile course-built
        → Wipe + seed RM profile + diagnostic + gap_map + 7 training_progress rows
          (Module 1 unlocked, not started; Modules 2–7 locked);
          app opens on Home dashboard — UAT Group C entry point

    python scripts/reset_uat_user.py --profile m1-done
        → Wipe + seed RM profile with Module 1 complete + Module 2 unlocked;
          app opens on Home dashboard — UAT-10 / UAT-16 entry point

    python scripts/reset_uat_user.py --profile all-done
        → Wipe + seed RM profile with all 7 modules complete;
          app opens on Home dashboard — UAT-15 entry point

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

_mode = parser.add_mutually_exclusive_group()
_mode.add_argument(
    "--role",
    choices=["rm", "uw", "mk"],
    help="Seed a user_profiles row for this role after wiping (app lands on Diagnostic)",
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
elif args.profile:
    print(f"Mode: --profile {args.profile}")
print()

for table in TABLES:
    execute(f"DELETE FROM {CATALOG}.{table} WHERE user_email = ?", [EMAIL])
    print(f"  [ok] cleared {table}")

# ── Seed: --role ─────────────────────────────────────────────────────────────

if args.role:
    _name_map = {"rm": "RM Tester", "uw": "UW Tester", "mk": "MK Tester"}
    display_name = _name_map.get(args.role, f"{args.role.upper()} Tester")
    execute(
        f"INSERT INTO {CATALOG}.learner.user_profiles "
        f"(user_email, display_name, role_id, created_at) "
        f"VALUES (?, ?, ?, current_timestamp())",
        [EMAIL, display_name, args.role],
    )
    print(f"\n  [ok] seeded user_profiles  (role_id={args.role}, display_name={display_name!r})")

# ── Seed: --diag ─────────────────────────────────────────────────────────────

# DOMAIN REFACTOR NOTE (2026-03):
# After the hexagon domain refactor, domain_scores JSON columns store 6 new domain IDs:
#   responsible_ai, strategic_prompting, critical_eval,
#   relationship_intel, data_decision, augmented_comm
# Any diagnostic_sessions rows created before this refactor contain 4 old keys
# (prompting, verification, data_safety, tool_fluency) and will produce incorrect
# scores on the Skills Profile page.
# For dev/UAT: use this script to reset the test user (handles full row deletion).
# For production: a data migration is out of scope for MVP.

if args.diag:
    now = datetime.now(timezone.utc).isoformat()
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

    # Canned bullets: one per gap/borderline domain (ordered by priority)
    bullets = json.dumps([
        "Critical Evaluation (1.0): Practise reviewing AI outputs for accuracy before acting — challenge AI-generated summaries with at least one verification step.",
        "Strategic Prompting (1.5): Build more structured, context-rich prompts for your workflows — include client context, desired output format, and explicit constraints.",
        "Relationship Intelligence (1.5): Explore using AI to prepare personalised client briefings and surface relationship patterns across your portfolio.",
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

# ── Seed: --profile ──────────────────────────────────────────────────────────

if args.profile:
    from utils.content import COURSES  # noqa: E402

    # Resolve RM course IDs in sequence order from the content bundle
    rm_courses_sorted = sorted(
        [(cid, c) for cid, c in COURSES.items() if c.get("role_id") == "rm"],
        key=lambda x: x[1].get("sequence_order", 99),
    )
    rm_course_ids = [cid for cid, _ in rm_courses_sorted]

    if not rm_course_ids:
        # Fallback: hardcoded IDs matching courses.json naming convention
        rm_course_ids = [
            "rm_c1_responsible_ai",
            "rm_c2_strategic_prompting",
            "rm_c3_critical_eval",
            "rm_c4_relationship_intel",
            "rm_c5_data_decision",
            "rm_c6_augmented_comm",
            "rm_c7_capstone",
        ]

    now = datetime.now(timezone.utc).isoformat()
    session_id = str(uuid.uuid4())

    # Fixture diagnostic domain scores (mirrors demo persona 3c values)
    _diag_scores = {
        "responsible_ai":      1.2,
        "strategic_prompting": 2.3,
        "critical_eval":       1.8,
        "relationship_intel":  1.5,
        "data_decision":       1.1,
        "augmented_comm":      1.6,
    }
    overall_score = round(sum(_diag_scores.values()) / len(_diag_scores), 2)

    # Gap map bullets: in-progress for course-built/m1-done; advanced for all-done
    _bullets_inprogress = json.dumps([
        "Your responses show difficulty distinguishing high-risk from low-risk AI use cases "
        "— prioritise the Responsible AI module to develop safer judgment patterns in "
        "client-facing scenarios.",
        "Data interpretation tasks revealed uncertainty when validating AI-generated "
        "financial figures — the Data-Driven Decision Making module will strengthen your "
        "analytical confidence.",
        "Prompting quality improved notably in Module 1 — build on this momentum by "
        "experimenting with chain-of-thought structures in your next practice session.",
    ])
    _bullets_alldone = json.dumps([
        "You've reached Proficient level across all six AI domains — to progress toward "
        "Champion, focus on applying structured prompting frameworks to ambiguous, "
        "multi-step analytical tasks.",
        "Your critical evaluation skills are approaching expert level — challenge yourself "
        "further with real-time fact-checking exercises against live AI outputs in your workflow.",
        "Augmented Communication is your strongest domain — leverage this by experimenting "
        "with AI-assisted stakeholder reporting and presentation preparation.",
    ])

    # Evaluation scores per module for all-done profile
    _eval_scores = [3.2, 3.0, 2.8, 3.1, 2.9, 3.4, 3.1]
    _domain_scores_after = [3.1, 3.0, 2.9, 3.2, 2.8, 3.5, 3.3]

    # user_profiles
    execute(
        f"INSERT INTO {CATALOG}.learner.user_profiles "
        f"(user_email, display_name, role_id, created_at) "
        f"VALUES (?, ?, ?, current_timestamp())",
        [EMAIL, "UAT Tester RM", "rm"],
    )
    print(f"\n  [ok] seeded user_profiles  (role_id=rm, display_name='UAT Tester RM')")

    # diagnostic_sessions
    execute(
        f"INSERT INTO {CATALOG}.learner.diagnostic_sessions "
        f"(session_id, user_email, started_at, completed_at, "
        f" responses, item_scores, domain_scores, overall_score) "
        f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            session_id, EMAIL, now, now,
            json.dumps({}), json.dumps({}),
            json.dumps(_diag_scores), overall_score,
        ],
    )
    print(f"  [ok] seeded diagnostic_sessions  (session_id={session_id}, overall={overall_score})")

    # gap_maps
    bullets = _bullets_alldone if args.profile == "all-done" else _bullets_inprogress
    execute(
        f"INSERT INTO {CATALOG}.learner.gap_maps "
        f"(gap_map_id, user_email, source_type, source_id, bullets, generated_at) "
        f"VALUES (?, ?, ?, ?, ?, ?)",
        [str(uuid.uuid4()), EMAIL, "diagnostic", session_id, bullets, now],
    )
    print(f"  [ok] seeded gap_maps")

    # training_progress — 7 rows; structure depends on profile
    for i, course_id in enumerate(rm_course_ids):
        seq = i + 1

        if args.profile == "course-built":
            # Module 1 unlocked but nothing started; rest locked
            is_locked = "false" if seq == 1 else "true"
            execute(
                f"INSERT INTO {CATALOG}.learner.training_progress "
                f"(progress_id, user_email, course_id, module_sequence_order, is_locked) "
                f"VALUES (?, ?, ?, ?, {is_locked})",
                [str(uuid.uuid4()), EMAIL, course_id, str(seq)],
            )

        elif args.profile == "m1-done":
            if seq == 1:
                # Module 1: fully complete
                execute(
                    f"INSERT INTO {CATALOG}.learner.training_progress "
                    f"(progress_id, user_email, course_id, module_sequence_order, "
                    f"is_locked, reading_completed_at, practice_completed_at, "
                    f"evaluation_completed_at, evaluation_score, domain_score_after) "
                    f"VALUES (?, ?, ?, ?, false, ?, ?, ?, ?, ?)",
                    [str(uuid.uuid4()), EMAIL, course_id, str(seq), now, now, now, "2.8", "2.1"],
                )
            elif seq == 2:
                # Module 2: unlocked (next active module)
                execute(
                    f"INSERT INTO {CATALOG}.learner.training_progress "
                    f"(progress_id, user_email, course_id, module_sequence_order, is_locked) "
                    f"VALUES (?, ?, ?, ?, false)",
                    [str(uuid.uuid4()), EMAIL, course_id, str(seq)],
                )
            else:
                # Modules 3–7: locked
                execute(
                    f"INSERT INTO {CATALOG}.learner.training_progress "
                    f"(progress_id, user_email, course_id, module_sequence_order, is_locked) "
                    f"VALUES (?, ?, ?, ?, true)",
                    [str(uuid.uuid4()), EMAIL, course_id, str(seq)],
                )

        elif args.profile == "all-done":
            # All 7 modules complete and unlocked
            execute(
                f"INSERT INTO {CATALOG}.learner.training_progress "
                f"(progress_id, user_email, course_id, module_sequence_order, "
                f"is_locked, reading_completed_at, practice_completed_at, "
                f"evaluation_completed_at, evaluation_score, domain_score_after) "
                f"VALUES (?, ?, ?, ?, false, ?, ?, ?, ?, ?)",
                [
                    str(uuid.uuid4()), EMAIL, course_id, str(seq),
                    now, now, now,
                    str(_eval_scores[i]),
                    str(_domain_scores_after[i]),
                ],
            )

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
print("Run ./run_uat.sh and open http://localhost:8501")
