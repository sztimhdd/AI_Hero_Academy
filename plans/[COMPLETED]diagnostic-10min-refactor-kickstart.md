# Claude Code Kickstart Prompt — Diagnostic 10-Minute Refactor

Paste the block below as your opening message in a new Claude Code session.

---

## PASTE START

I need you to implement the diagnostic redesign described in
`plans/diagnostic-10min-refactor.md`. Read that file first — it is the authoritative
spec for this task.

### Project context

This is **AI Hero Academy**, a Databricks App (Streamlit + Python) that trains employees
on AI skills through a four-stage loop: Diagnose → Map Gaps → Train → Score.

Static content lives in `content/*.json` (loaded at startup by `utils/content.py`).
The diagnostic flow reads from `content/diagnostic_items.json`.

**Current state:**
- `content/diagnostic_items.json` has 54 items: 18 per role (rm / uw / an)
- Each role has 3 items per domain × 6 domains: 1 MCQ + 1 prompt_sandbox + 1 micro_task

**Goal:**
Reduce to 6 items per role (18 total) following the 10-minute sequence designed in the
plan. RM and AN keeper item IDs are already confirmed in the plan. UW item IDs need to be
identified from the live file on execution day (see Step 2 in the plan).

### Prerequisite check (do this FIRST before any edits)

```bash
.venv/Scripts/python -c "
import json
items = json.load(open('content/diagnostic_items.json'))
for role in ['rm', 'uw', 'an']:
    role_items = [i for i in items if i.get('role_id') == role]
    domains = set(i['domain_id'] for i in role_items)
    print(f'{role}: {len(role_items)} items, {len(domains)} domains: {sorted(domains)}')
"
```

**If UW has fewer than 18 items or is missing any of the 6 domains** — stop and tell me.
UW content regeneration must complete before this task can proceed.

**If all 3 roles have 18 items across 6 domains** — proceed with the plan.

### Execution

Follow the steps in `plans/diagnostic-10min-refactor.md` exactly:

1. List UW items to identify the correct item_id for each of the 6 UW keeper slots
2. Run the inline Python filter to reduce to 18 items + inject `display_order`
3. Grep app/utils code for any hardcoded question counts and fix them
4. Run UAT locally: `python scripts/reset_uat_user.py && bash run_uat.sh`
   — walk the full diagnostic as dev@example.com and confirm 6 questions appear
5. Commit and deploy: `bash scripts/sync_deploy.sh`

### Key files

- `plans/diagnostic-10min-refactor.md` — full spec and KEEP item ID lists
- `content/diagnostic_items.json` — the data file to edit
- `utils/content.py` — getter functions (read, don't assume)
- `app.py` — main app entry point (check for hardcoded counts)
- `scripts/reset_uat_user.py` — reset dev@example.com between test runs
- `CLAUDE.md` — project conventions and verification checklist

### Auth note

If you need to run `.venv/Scripts/python` scripts that call Databricks APIs, prefix with:
```
DATABRICKS_CONFIG_PROFILE=dev DATABRICKS_HOST=https://adb-2717931942638877.17.azuredatabricks.net
```
Background bash tasks lose VS Code auth context — run API-dependent scripts in the
foreground only.

## PASTE END
