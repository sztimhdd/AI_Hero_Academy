"""
Reset UAT test-user data in Delta tables.

Run this before each clean UAT pass to delete all learner-schema rows
for DEV_USER_EMAIL so the app starts from the Welcome page.

Usage:
    python scripts/reset_uat_user.py

Reads credentials from .env in the project root (same as run_uat.sh).
"""
import os
import sys
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
print()

for table in TABLES:
    execute(f"DELETE FROM {CATALOG}.{table} WHERE user_email = ?", [EMAIL])
    print(f"  ✓  {table}")

print()
print("Done. Run ./run_uat.sh and open http://localhost:8501 to start fresh.")
