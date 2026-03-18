"""
Pre-seed all demo personas into remote Firestore.

Run this once to populate all 5 demo profiles (3a–3e) so they are
ready before any Playwright UAT or stakeholder demo session.

Usage:
    python scripts/seed_demo_personas.py
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from utils.demo import ensure_demo_seeded, DEMO_PROFILES  # noqa: E402

print("Seeding demo personas into Firestore...")
print(f"  GCP project: {os.environ.get('GCP_PROJECT_ID', '(not set)')}")
print()

for profile_id, profile in DEMO_PROFILES.items():
    print(f"  [{profile_id}] {profile['label']}")
    print(f"       email: {profile['email']}")
    try:
        ensure_demo_seeded(profile_id)
        print(f"       [ok] seeded")
    except Exception as exc:
        print(f"       [FAILED] {exc}")
    print()

print("Done. All demo personas are ready in Firestore.")
