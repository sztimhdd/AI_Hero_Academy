# Databricks notebook source
# MAGIC %md
# MAGIC # 00 — Create Schemas and Tables
# MAGIC
# MAGIC Run this once to create all Unity Catalog schemas and Delta tables for AI Hero Academy.
# MAGIC Idempotent: uses CREATE TABLE IF NOT EXISTS throughout.

# COMMAND ----------

import os
from databricks.sdk import WorkspaceClient

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai")
WH_ID   = os.environ.get("DATABRICKS_WAREHOUSE_ID", "eaa098820703bf5f")

w = WorkspaceClient()

def sql(statement: str):
    result = w.statement_execution.execute_statement(
        warehouse_id=WH_ID,
        statement=statement,
        wait_timeout="60s",
    )
    if result.status.error:
        raise RuntimeError(f"SQL error: {result.status.error.message}\n\nStatement:\n{statement}")
    return result

print(f"Connected to catalog: {CATALOG}")

# COMMAND ----------
# MAGIC %md ## 1 — Create schemas

for schema in ["content", "learner", "system"]:
    sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{schema}")
    print(f"Schema {CATALOG}.{schema} — OK")

# COMMAND ----------
# MAGIC %md ## 2 — content schema tables

# roles
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.content.roles (
  role_id       STRING NOT NULL,
  title         STRING NOT NULL,
  description   STRING,
  department    STRING,
  PRIMARY KEY (role_id)
)
USING DELTA
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true')
""")
print("content.roles — OK")

# domains
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.content.domains (
  domain_id           STRING NOT NULL,
  role_id             STRING NOT NULL,
  title               STRING NOT NULL,
  description         STRING,
  level_0_label       STRING,
  level_0_descriptor  STRING,
  level_1_label       STRING,
  level_1_descriptor  STRING,
  level_2_label       STRING,
  level_2_descriptor  STRING,
  level_3_label       STRING,
  level_3_descriptor  STRING,
  level_4_label       STRING,
  level_4_descriptor  STRING,
  PRIMARY KEY (domain_id)
)
USING DELTA
""")
print("content.domains — OK")

# diagnostic_items
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.content.diagnostic_items (
  item_id         STRING NOT NULL,
  domain_id       STRING NOT NULL,
  item_type       STRING NOT NULL COMMENT 'mcq | prompt_sandbox | micro_task',
  question_text   STRING NOT NULL,
  scenario_text   STRING,
  options         STRING COMMENT 'JSON array of {{label, text}} for MCQ',
  correct_option  STRING COMMENT 'label of correct option for MCQ',
  scoring_rubric  STRING COMMENT 'JSON object of criteria for open-ended items',
  display_order   INT,
  PRIMARY KEY (item_id)
)
USING DELTA
""")
print("content.diagnostic_items — OK")

# courses
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.content.courses (
  course_id        STRING NOT NULL,
  role_id          STRING NOT NULL,
  primary_domain   STRING NOT NULL,
  title            STRING NOT NULL,
  tagline          STRING,
  description      STRING,
  real_use_case    STRING COMMENT 'The real EDC use case submission(s) this course is anchored to',
  sequence_order   INT,
  PRIMARY KEY (course_id)
)
USING DELTA
""")
print("content.courses — OK")

# reading_content
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.content.reading_content (
  content_id      STRING NOT NULL,
  course_id       STRING NOT NULL,
  concept_text    STRING NOT NULL COMMENT 'Core concept explanation',
  good_example    STRING NOT NULL COMMENT 'Annotated positive example',
  anti_pattern    STRING NOT NULL COMMENT 'Annotated negative example with explanation',
  takeaway        STRING NOT NULL COMMENT 'One-sentence practical rule',
  PRIMARY KEY (content_id)
)
USING DELTA
""")
print("content.reading_content — OK")

# practice_scenarios
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.content.practice_scenarios (
  scenario_id         STRING NOT NULL,
  course_id           STRING NOT NULL,
  scenario_text       STRING NOT NULL COMMENT 'Scene-setting context given to the learner',
  task_1_text         STRING NOT NULL,
  task_2_text         STRING NOT NULL,
  task_3_text         STRING NOT NULL,
  task_4_text         STRING NOT NULL,
  coach_system_prompt STRING NOT NULL COMMENT 'System prompt for the AI coach for this course',
  PRIMARY KEY (scenario_id)
)
USING DELTA
""")
print("content.practice_scenarios — OK")

# evaluation_items
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.content.evaluation_items (
  item_id        STRING NOT NULL,
  course_id      STRING NOT NULL,
  item_type      STRING NOT NULL COMMENT 'mcq | performance_task',
  sequence       INT   NOT NULL COMMENT '1-4; items 1-3 are MCQ, item 4 is performance_task',
  question_text  STRING NOT NULL,
  scenario_text  STRING COMMENT 'Additional scenario context for performance tasks',
  options        STRING COMMENT 'JSON array of {{label, text}} for MCQ',
  correct_option STRING COMMENT 'label of correct MCQ answer',
  explanation    STRING COMMENT 'Explanation of correct MCQ answer',
  scoring_rubric STRING NOT NULL COMMENT 'JSON object: criteria -> max_points',
  PRIMARY KEY (item_id)
)
USING DELTA
""")
print("content.evaluation_items — OK")

# COMMAND ----------
# MAGIC %md ## 3 — learner schema tables

# user_profiles
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.learner.user_profiles (
  user_email    STRING NOT NULL,
  display_name  STRING,
  role_id       STRING NOT NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (user_email)
)
USING DELTA
""")
print("learner.user_profiles — OK")

# diagnostic_sessions
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.learner.diagnostic_sessions (
  session_id     STRING NOT NULL,
  user_email     STRING NOT NULL,
  started_at     TIMESTAMP NOT NULL DEFAULT current_timestamp(),
  completed_at   TIMESTAMP,
  responses      STRING COMMENT 'JSON: item_id -> response_text',
  item_scores    STRING COMMENT 'JSON: item_id -> score (0.0-4.0)',
  domain_scores  STRING COMMENT 'JSON: domain_id -> score (0.0-4.0)',
  overall_score  DOUBLE,
  PRIMARY KEY (session_id)
)
USING DELTA
""")
print("learner.diagnostic_sessions — OK")

# gap_maps
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.learner.gap_maps (
  gap_map_id      STRING NOT NULL,
  user_email      STRING NOT NULL,
  source_type     STRING NOT NULL COMMENT 'diagnostic | evaluation',
  source_id       STRING NOT NULL COMMENT 'session_id or evaluation attempt id',
  bullets         STRING NOT NULL COMMENT 'JSON array of narrative bullet strings',
  generated_at    TIMESTAMP NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (gap_map_id)
)
USING DELTA
""")
print("learner.gap_maps — OK")

# training_progress
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.learner.training_progress (
  progress_id              STRING NOT NULL,
  user_email               STRING NOT NULL,
  course_id                STRING NOT NULL,
  module_sequence_order    INT    NOT NULL,
  is_locked                BOOLEAN NOT NULL DEFAULT true,
  reading_completed_at     TIMESTAMP,
  practice_completed_at    TIMESTAMP,
  evaluation_score         DOUBLE,
  evaluation_completed_at  TIMESTAMP,
  domain_score_after       DOUBLE COMMENT 'Domain score after this module evaluation',
  PRIMARY KEY (progress_id)
)
USING DELTA
""")
print("learner.training_progress — OK")

# coach_sessions
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.learner.coach_sessions (
  session_id           STRING NOT NULL,
  user_email           STRING NOT NULL,
  course_id            STRING NOT NULL,
  started_at           TIMESTAMP NOT NULL DEFAULT current_timestamp(),
  completed_at         TIMESTAMP,
  turn_count           INT    NOT NULL DEFAULT 0,
  conversation_json    STRING NOT NULL COMMENT 'JSON array of {role, content} turn objects',
  PRIMARY KEY (session_id)
)
USING DELTA
""")
print("learner.coach_sessions — OK")

# COMMAND ----------
# MAGIC %md ## 4 — system schema tables

# ai_call_log
sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.system.ai_call_log (
  log_id           STRING NOT NULL,
  user_email       STRING,
  call_type        STRING NOT NULL COMMENT 'diagnostic_scoring | gap_map | coach_response | evaluation_scoring',
  model_endpoint   STRING NOT NULL,
  prompt_tokens    INT,
  completion_tokens INT,
  latency_ms       INT,
  success          BOOLEAN NOT NULL,
  error_message    STRING,
  called_at        TIMESTAMP NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (log_id)
)
USING DELTA
""")
print("system.ai_call_log — OK")

print("\n✓ All schemas and tables created successfully.")
