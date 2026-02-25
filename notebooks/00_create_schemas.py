# Databricks notebook source
# MAGIC %md
# MAGIC # 00 — Create Schemas and Tables
# MAGIC
# MAGIC Run this once to create all Unity Catalog schemas and Delta tables for AI Hero Academy.
# MAGIC Idempotent: uses CREATE TABLE IF NOT EXISTS throughout.

# COMMAND ----------

import os

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")

def sql(statement: str):
    spark.sql(statement).collect()  # Force eager execution

print(f"Connected to catalog: {CATALOG}")

# COMMAND ----------
# 1 — Create schemas
# Note: content schema removed — all content now served from JSON files in content/

for schema in ["learner", "system"]:
    sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{schema}")
    print(f"Schema {CATALOG}.{schema} — OK")

# COMMAND ----------
# 2 — learner schema tables

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
TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
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
TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
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
TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
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
TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
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
TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
""")
print("learner.coach_sessions — OK")

# COMMAND ----------
# 4 — system schema tables

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
TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
""")
print("system.ai_call_log — OK")

print("\n✓ All schemas and tables created successfully.")
