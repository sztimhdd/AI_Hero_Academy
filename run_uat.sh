#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# run_uat.sh — Start AI Hero Academy locally for UAT / Playwright testing
#
# Usage:
#   1. Copy .env.example to .env and fill in GEMINI_API_KEY, GCP_PROJECT_ID,
#      GOOGLE_APPLICATION_CREDENTIALS, DEV_USER_EMAIL
#   2. ./run_uat.sh
#   3. Open http://localhost:8501 in any browser or Playwright
#
# To reset test-user data between runs:
#   python scripts/reset_uat_user.py
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "$SCRIPT_DIR/.env" ]; then
  echo "ERROR: .env not found."
  echo "       Copy .env.example to .env and set GEMINI_API_KEY, GCP_PROJECT_ID."
  exit 1
fi

# Load all vars from .env into this process's environment
set -a
# shellcheck source=.env
source "$SCRIPT_DIR/.env"
set +a

echo "──────────────────────────────────────────────"
echo " AI Hero Academy — UAT mode"
echo " User : ${DEV_USER_EMAIL:-dev@example.com}"
echo " Port : 8501"
echo "──────────────────────────────────────────────"

# Use .venv if present, otherwise fall back to system Python
PYTHON="${SCRIPT_DIR}/.venv/Scripts/python.exe"
if [ ! -f "$PYTHON" ]; then
  PYTHON="python"
fi

exec "$PYTHON" -m streamlit run "$SCRIPT_DIR/app.py" \
  --server.port 8501 \
  --server.enableCORS false \
  --server.enableXsrfProtection false
