# Local UAT Mode Implementation Plan

> **Status:** DRAFT

## Specification

**Problem:** The Playwright MCP uses a Chromium browser that is not authenticated into the corporate Databricks environment and cannot be — by security policy. Manual local testing with `run_local.sh` also requires manually knowing and exporting several Databricks env vars each time.

**Key insight:** Chromium connects only to `localhost:8502`. It has zero direct Databricks connections. Only the Streamlit **Python process** authenticates to Databricks. Therefore, providing a Databricks PAT to the Python process's environment is sufficient to unblock both SQL warehouse access and AI endpoint calls for local UAT — no local DB layer or AI mock is needed.

**Goal:** A developer can run `./run_uat.sh` from the project root, open `http://localhost:8501` in Playwright Chromium (or any browser), and exercise the full app — Welcome → Diagnostic → Skills Profile → Home → Course Module — against real Databricks infrastructure, using a fixed test user identity. A visible "UAT" banner distinguishes local test sessions from production.

**Scope:**

In scope:
- `.env.example` — committed template listing all required env vars with placeholder values
- `.env` — gitignored local file where the developer puts real secrets (already in `.gitignore`)
- `run_uat.sh` — bash script that sources `.env` and starts Streamlit on port 8501
- `LOCAL_UAT=true` env var — activates test user identity and UAT banner
- UAT banner in the app UI (app.py) when `LOCAL_UAT=true`
- `scripts/reset_uat_user.py` — one-shot script to DELETE all `learner.*` rows for `DEV_USER_EMAIL` so test runs start clean

Out of scope:
- Local SQLite or JSON DB layer
- AI mocking / canned responses
- Changes to production code paths (no if/else branches in pages)
- Multi-user UAT or test fixtures for content schema

**Success Criteria:**

- [ ] `./run_uat.sh` starts the app with zero manual env var exports
- [ ] Playwright Chromium at `localhost:8501` can complete the full Welcome → Diagnostic flow without Databricks auth errors
- [ ] AI scoring (diagnostic submit) works end-to-end
- [ ] A yellow "UAT" badge is visible in the sidebar when `LOCAL_UAT=true`
- [ ] `python scripts/reset_uat_user.py` deletes all test-user rows and prints a confirmation
- [ ] `.env` is never committed (gitignore check passes)

---

## Context Loading

_Run before starting:_

```bash
read utils/auth.py
read utils/db.py
read app.py
read .gitignore
read .env.example   # may not exist yet
```

---

## Tasks

### Task 1: Credentials template and run script

**Context:** `.gitignore`, `app.yaml`, `utils/auth.py`

**Steps:**

1. [ ] Create `.env.example` at project root with ALL required env vars and placeholder values:
   ```
   # Databricks PAT auth (get token from workspace Settings → Developer → Access tokens)
   DATABRICKS_HOST=https://adb-2717931942638877.17.azuredatabricks.net/
   DATABRICKS_TOKEN=dapi...

   # SQL warehouse
   DATABRICKS_WAREHOUSE_ID=eaa098820703bf5f

   # AI serving endpoint
   SERVING_ENDPOINT_NAME=databricks-claude-sonnet-4-5

   # Unity Catalog
   UC_CATALOG=mdlg_ai_shared

   # UAT mode: fixed test-user identity + UAT banner
   LOCAL_UAT=true
   DEV_USER_EMAIL=uat-test@edc.ca
   ```

2. [ ] Verify `.env` is already listed in `.gitignore` (it is — line 6). No change needed.

3. [ ] Create `run_uat.sh` at project root:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

   if [ ! -f "$SCRIPT_DIR/.env" ]; then
     echo "ERROR: .env not found. Copy .env.example to .env and fill in your PAT."
     exit 1
   fi

   set -a
   source "$SCRIPT_DIR/.env"
   set +a

   echo "Starting AI Hero Academy in UAT mode (user: ${DEV_USER_EMAIL:-dev@example.com})"
   "$SCRIPT_DIR/.venv/Scripts/python.exe" -m streamlit run "$SCRIPT_DIR/app.py" \
     --server.port 8501 \
     --server.enableCORS false \
     --server.enableXsrfProtection false
   ```
   Mark executable: `chmod +x run_uat.sh`

4. [ ] Add `run_uat.sh` to `.syncignore` (if it exists) so it's not deployed to the workspace.

**Verify:** `bash run_uat.sh` starts Streamlit without credential errors; `http://localhost:8501` loads the Welcome page.

---

### Task 2: UAT banner in app UI

**Context:** `app.py`

**Steps:**

1. [ ] In `app.py`, after the `st.set_page_config(...)` call, add a sidebar UAT indicator that only renders when `LOCAL_UAT=true`:
   ```python
   import os
   if os.environ.get("LOCAL_UAT") == "true":
       st.sidebar.warning(
           f"⚠️ UAT MODE\nUser: {st.session_state.get('user_email', '...')}"
       )
   ```
   Place it after session state is initialised so `user_email` is available.

2. [ ] No changes to any page logic — the banner is purely informational.

**Verify:** With `LOCAL_UAT=true` in env, sidebar shows the yellow warning box. Without it, sidebar is unchanged.

---

### Task 3: UAT data reset script

**Context:** `utils/db.py`, `utils/auth.py`

**Steps:**

1. [ ] Create `scripts/reset_uat_user.py`:
   ```python
   """
   Deletes all learner-schema rows for DEV_USER_EMAIL.
   Run before a clean UAT pass: python scripts/reset_uat_user.py
   """
   import os, sys
   sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

   from dotenv import load_dotenv
   load_dotenv()  # reads .env from cwd

   from utils.db import execute

   CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")
   EMAIL = os.environ.get("DEV_USER_EMAIL", "dev@example.com")

   tables = [
       "learner.coach_sessions",
       "learner.gap_maps",
       "learner.training_progress",
       "learner.diagnostic_sessions",
       "learner.user_profiles",
   ]

   print(f"Resetting UAT data for: {EMAIL} in {CATALOG}")
   for table in tables:
       execute(f"DELETE FROM {CATALOG}.{table} WHERE user_email = ?", [EMAIL])
       print(f"  ✓ {table}")
   print("Done.")
   ```

2. [ ] Install `python-dotenv` if not already in `requirements.txt`:
   - Check `requirements.txt`; add `python-dotenv` if missing.

**Verify:** With `.env` sourced, `python scripts/reset_uat_user.py` prints one `✓` line per table and exits 0. Running the app again shows the Welcome page (profile gone).

---

## Notes

- The script uses `.venv/Scripts/python.exe` (Windows path). If running on Linux/macOS (CI), change to `.venv/bin/python`.
- `app.yaml` (deployed app config) is unaffected — `LOCAL_UAT` is never set there.
- The `DEV_USER_EMAIL` value (`uat-test@edc.ca`) is safe to share; all its data is owned by the test script. Use any email address that isn't a real employee's.
- Token expiry: Databricks PATs are long-lived (configurable). If the PAT expires, generate a new one in workspace Settings → Developer → Access tokens and update `.env`.
