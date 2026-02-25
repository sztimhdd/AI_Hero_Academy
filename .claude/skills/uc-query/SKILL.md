---
name: uc-query
description: Write or run a Unity Catalog SQL query against the mdlg_ai catalog. Use when the user asks to query Delta tables, inspect data, debug learner state, or check seeded content.
allowed-tools: Bash, Read
---

Write and optionally execute a Unity Catalog SQL query for the **AI Hero Academy** app using the `mdlg_ai` catalog.

## Catalog: `mdlg_ai`

### `content` schema — read-only, pre-seeded via notebooks

| Table | Key columns |
|---|---|
| `content.roles` | `role_id`, `role_name`, `description` |
| `content.domains` | `domain_id`, `domain_name`, `level_descriptors` (JSON) |
| `content.diagnostic_items` | `item_id`, `domain_id`, `question_text`, `item_type` (MCQ/prompt_sandbox/micro_task), `answer_key`, `rubric` |
| `content.courses` | `course_id`, `domain_id` (primary_domain), `course_name`, `description` |
| `content.reading_content` | `course_id`, `content_md` |
| `content.practice_scenarios` | `course_id`, `scenario_text`, `tasks` (JSON array of 4), `coach_system_prompt` |
| `content.evaluation_items` | `item_id`, `course_id`, `question_text`, `item_type`, `answer_key`, `rubric` |

### `learner` schema — read-write, always filtered by `user_email`

| Table | Key columns |
|---|---|
| `learner.user_profiles` | `user_email`, `display_name`, `role_id`, `created_at` |
| `learner.diagnostic_sessions` | `session_id`, `user_email`, `responses` (JSON), `item_scores` (JSON), `completed_at` |
| `learner.gap_maps` | `gap_id`, `user_email`, `session_id`, `source_type` (diagnostic/evaluation), `bullets` (JSON array), `created_at` |
| `learner.training_progress` | `user_email`, `course_id`, `module_order`, `is_locked`, `reading_completed_at`, `practice_completed_at`, `eval_score`, `eval_completed_at` |
| `learner.coach_sessions` | `session_id`, `user_email`, `course_id`, `transcript` (JSON), `turn_count`, `completed_at` |

### `system` schema — written by app, read by admins

| Table | Key columns |
|---|---|
| `system.ai_call_log` | `call_id`, `user_email`, `call_type`, `prompt`, `response`, `latency_ms`, `error`, `created_at` |

## How to run a query from app code

```python
from databricks.sdk import WorkspaceClient
import os

w = WorkspaceClient()
result = w.statement_execution.execute_statement(
    warehouse_id=os.environ["DATABRICKS_WAREHOUSE_ID"],  # eaa098820703bf5f
    statement="SELECT * FROM mdlg_ai.content.roles",
    wait_timeout="30s",
)
rows = result.result.data_array  # list of lists
```

## How to run a query via Databricks CLI (for debugging)

```bash
databricks statement-execution execute \
  --warehouse-id eaa098820703bf5f \
  --statement "SELECT * FROM mdlg_ai.learner.user_profiles LIMIT 10"
```

## Task

Given `$ARGUMENTS`:

1. **Understand the intent**: what data does the user want to inspect or modify?
2. **Write the SQL**: use fully-qualified names (`mdlg_ai.<schema>.<table>`). For learner queries, always add `WHERE user_email = '<email>'` unless the intent is cross-user admin inspection.
3. **Show the query** clearly in a code block.
4. If the user wants to actually run it, use the Databricks CLI command above. Do not run destructive statements (DELETE, DROP, TRUNCATE) without explicit user confirmation.
5. **Explain the results** in plain language.

## Scoring reference (for gap analysis queries)

- Domain score = average of all scored items for that domain
- Level labels: 0.0–0.4 Unaware · 0.5–1.4 Explorer · 1.5–2.4 Practitioner · 2.5–3.4 Proficient · 3.5–4.0 Champion
