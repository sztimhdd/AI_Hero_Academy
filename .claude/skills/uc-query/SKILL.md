---
name: uc-query
description: Write or run a Unity Catalog SQL query against the mdlg_ai_shared catalog. Use when the user asks to query Delta tables, inspect data, debug learner state, or check seeded content.
---

Write and optionally execute a Unity Catalog SQL query for the **AI Hero Academy** app using the `mdlg_ai_shared` catalog.

> **Note**: The `content.*` Delta tables are retired. All static content is served from `content/*.json` files bundled with the app. Only `learner.*` and `system.*` tables are active.

## Catalog: `mdlg_ai_shared`

### `learner` schema — read-write, always filtered by `user_email`

| Table | Key columns |
|---|---|
| `learner.user_profiles` | `user_email`, `display_name`, `role_id`, `created_at` |
| `learner.diagnostic_sessions` | `session_id`, `user_email`, `responses` (JSON), `item_scores` (JSON), `domain_scores` (JSON), `overall_score`, `started_at`, `completed_at` |
| `learner.gap_maps` | `gap_map_id`, `user_email`, `source_type` (diagnostic/evaluation), `source_id`, `bullets` (JSON array), `generated_at` |
| `learner.training_progress` | `progress_id`, `user_email`, `course_id`, `module_sequence_order`, `is_locked`, `reading_completed_at`, `practice_completed_at`, `evaluation_completed_at`, `evaluation_score`, `domain_score_after` |
| `learner.coach_sessions` | `session_id`, `user_email`, `course_id`, `conversation_json` (JSON), `turn_count`, `started_at`, `completed_at` |

### `system` schema — written by app, read by admins

| Table | Key columns |
|---|---|
| `system.ai_call_log` | `log_id`, `user_email`, `call_type`, `model_endpoint`, `latency_ms`, `success`, `error_message`, `called_at` |

## How to run a query via Databricks MCP (preferred)

```python
# Use the mcp__databricks-mcp-server__execute_sql tool directly:
# warehouse_id: eaa098820703bf5f
# statement: "SELECT * FROM mdlg_ai_shared.learner.user_profiles LIMIT 10"
```

## How to run a query from app code

```python
from databricks.sdk import WorkspaceClient
import os

w = WorkspaceClient()
result = w.statement_execution.execute_statement(
    warehouse_id=os.environ["DATABRICKS_WAREHOUSE_ID"],  # eaa098820703bf5f
    statement="SELECT * FROM mdlg_ai_shared.learner.user_profiles WHERE user_email = ?",
    parameters=[{"name": "1", "value": "user@example.com"}],
    wait_timeout="30s",
)
rows = result.result.data_array  # list of lists
```

## Common UAT debug queries

### Check UAT test user state
```sql
SELECT * FROM mdlg_ai_shared.learner.user_profiles
WHERE user_email = 'uat-test@edc.ca'
```

### Verify --profile course-built seeding (module 1 unlocked, 2–7 locked)
```sql
SELECT module_sequence_order, course_id, is_locked,
       reading_completed_at, evaluation_completed_at
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca'
ORDER BY module_sequence_order
```

### Verify --profile all-done (0 null completions)
```sql
SELECT COUNT(*) as incomplete_modules
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca'
  AND evaluation_completed_at IS NULL
```

### Inspect latest gap map bullets
```sql
SELECT bullets, generated_at
FROM mdlg_ai_shared.learner.gap_maps
WHERE user_email = 'uat-test@edc.ca'
ORDER BY generated_at DESC
LIMIT 1
```

### Check latest diagnostic domain scores
```sql
SELECT domain_scores, overall_score, completed_at
FROM mdlg_ai_shared.learner.diagnostic_sessions
WHERE user_email = 'uat-test@edc.ca'
  AND completed_at IS NOT NULL
ORDER BY completed_at DESC
LIMIT 1
```

## Task

Given `$ARGUMENTS`:

1. **Understand the intent**: what data does the user want to inspect or modify?
2. **Write the SQL**: use fully-qualified names (`mdlg_ai_shared.<schema>.<table>`). For learner queries, always add `WHERE user_email = '<email>'` unless the intent is cross-user admin inspection.
3. **Show the query** clearly in a code block.
4. If the user wants to actually run it, use the `mcp__databricks-mcp-server__execute_sql` tool with `warehouse_id: eaa098820703bf5f`. Do not run destructive statements (DELETE, DROP, TRUNCATE) without explicit user confirmation.
5. **Explain the results** in plain language.

## Scoring reference (for gap analysis queries)

- Domain score = average of all scored items for that domain (diagnostic + completed evaluations, equal weight)
- Level labels: 0.0–0.4 Unaware · 0.5–1.4 Explorer · 1.5–2.4 Practitioner · 2.5–3.4 Proficient · 3.5–4.0 Champion
- 6 domains per role: `responsible_ai`, `strategic_prompting`, `critical_eval`, `relationship_intel`, `data_decision`, `augmented_comm`
