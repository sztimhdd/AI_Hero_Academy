---
name: databricks-deploy
description: Sync local files and deploy the Databricks App to the workspace. Use when the user asks to deploy, ship, push to Databricks, or go live.
disable-model-invocation: true
allowed-tools: Bash
---

Deploy the **AI Hero Academy** Databricks App using the project configuration from CLAUDE.md.

## Project config (do not change without updating CLAUDE.md)

| Setting | Value |
|---|---|
| App name | `my-ai-hero-academy-mvp` |
| Workspace source path | `/Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp` |
| Workspace URL | `https://adb-2717931942638877.17.azuredatabricks.net` |
| CLI profile | `dev` (default when run from project directory) |

## Steps

1. **Confirm working directory** is the project root (contains `app.py`):
   ```
   ls app.py
   ```
   If not found, stop and tell the user to navigate to the project root.

2. **Sync local files** to the Databricks workspace:
   ```
   databricks sync . /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp
   ```
   Wait for sync to complete. Surface any sync errors before proceeding.

3. **Deploy the app**:
   ```
   databricks apps deploy my-ai-hero-academy-mvp --source-code-path /Workspace/Users/hhu@edc.ca/my-ai-hero-academy-mvp
   ```

4. **Report outcome**: If successful, confirm the app is deployed. If it fails, show the full error output and suggest next steps.

## Notes
- The `dev` profile is auto-selected when running from this project directory
- Auth is handled by Databricks VS Code extension metadata service — no token needed
- For live iteration during development, use `databricks sync --watch` instead of a full deploy
- Content schema tables (`mdlg_ai.content.*`) are NOT managed by this app — update them via seeding notebooks
