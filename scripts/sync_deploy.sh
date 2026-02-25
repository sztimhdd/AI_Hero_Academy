#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# sync_deploy.sh — Sync local files to workspace and redeploy the Databricks App
#
# Usage:
#   bash scripts/sync_deploy.sh
#
# What it does:
#   1. Syncs all non-.syncignore'd files to the Databricks workspace
#   2. Deploys the app from the synced workspace path
#
# Auth: uses --profile dev (Databricks CLI OAuth, ~/.databrickscfg)
# Path fix: MSYS_NO_PATHCONV=1 prevents Git Bash from mangling /Workspace paths
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

APP_NAME="my-ai-hero-academy-mvp"
WORKSPACE_PATH="/Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp"
PROFILE="dev"

cd "$PROJECT_ROOT"

echo "──────────────────────────────────────────────"
echo " Syncing to Databricks workspace..."
echo " ${WORKSPACE_PATH}"
echo "──────────────────────────────────────────────"
MSYS_NO_PATHCONV=1 databricks sync . "$WORKSPACE_PATH" --profile "$PROFILE"

echo
echo "──────────────────────────────────────────────"
echo " Deploying app: ${APP_NAME}"
echo "──────────────────────────────────────────────"
MSYS_NO_PATHCONV=1 databricks apps deploy "$APP_NAME" \
  --source-code-path "$WORKSPACE_PATH" \
  --profile "$PROFILE"

echo
echo "✓ Deployed successfully."
