# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Seed Roles and Domains
# MAGIC
# MAGIC Seeds the `content.roles` and `content.domains` tables.
# MAGIC Idempotent: deletes existing rows for the seeded role before re-inserting.

# COMMAND ----------

import os, json

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")

def sql(statement: str):
    spark.sql(statement).collect()  # Force eager execution for DML statements

def escape(s: str) -> str:
    """Escape single quotes for SQL string literals."""
    return s.replace("'", "''")

# COMMAND ----------
# Role: Relationship Manager

ROLE = {
    "role_id": "rm",
    "title": "Relationship Manager",
    "description": (
        "Client-facing professionals who manage prospect and customer relationships across EDC's "
        "Mid-Market, Small Business, and Regional segments. Core responsibilities include lead "
        "qualification, discovery conversations, CRM documentation, pipeline forecasting, and "
        "multi-solution adoption. Supported by Associate Relationship Managers (ARMs) for "
        "top-of-funnel prospecting. Performance measured on customer growth, customer experience, "
        "process discipline, and education KPIs."
    ),
    "department": "Business Development / Sales",
}

sql(f"DELETE FROM {CATALOG}.content.roles WHERE role_id = '{ROLE['role_id']}'")
sql(f"""
INSERT INTO {CATALOG}.content.roles (role_id, title, description, department)
VALUES (
  '{escape(ROLE['role_id'])}',
  '{escape(ROLE['title'])}',
  '{escape(ROLE['description'])}',
  '{escape(ROLE['department'])}'
)
""")
print(f"Seeded role: {ROLE['title']}")

# COMMAND ----------
# Domains: 4 AI skill domains for the RM role

DOMAINS = [
    {
        "domain_id": "prompting",
        "role_id": "rm",
        "title": "Prompting for Outcomes",
        "description": (
            "Structuring AI prompts with context, constraints, format, and audience to produce "
            "outputs that are directly usable in RM workflows — briefing documents, emails, "
            "CRM notes, and talking points."
        ),
        "level_0_label": "Unaware",
        "level_0_descriptor": "Has not used AI prompting in work tasks. Cannot describe what makes a prompt effective.",
        "level_1_label": "Explorer",
        "level_1_descriptor": "Writes basic prompts ('summarize this'). Output often requires heavy editing or is too generic to use.",
        "level_2_label": "Practitioner",
        "level_2_descriptor": "Uses structured prompts with context and format instructions. Output is usually usable with minor edits.",
        "level_3_label": "Proficient",
        "level_3_descriptor": "Adapts prompts for complex scenarios. Adds constraints proactively. Iterates when output misses the mark.",
        "level_4_label": "Champion",
        "level_4_descriptor": "Designs reusable prompt templates for team workflows. Coaches colleagues on prompting structure. Contributes new use cases.",
    },
    {
        "domain_id": "verification",
        "role_id": "rm",
        "title": "Verification and Judgment",
        "description": (
            "Reviewing AI outputs critically before acting on them — catching hallucinations, "
            "incorrect dates, invented facts, and misattributed statements in meeting recaps, "
            "summaries, and CRM entries."
        ),
        "level_0_label": "Unaware",
        "level_0_descriptor": "Treats AI outputs as accurate by default. Does not cross-reference against source material.",
        "level_1_label": "Explorer",
        "level_1_descriptor": "Reads AI output before using it, but does not systematically verify against independent sources.",
        "level_2_label": "Practitioner",
        "level_2_descriptor": "Routinely cross-references AI output against own notes. Removes or corrects unverifiable statements before logging.",
        "level_3_label": "Proficient",
        "level_3_descriptor": "Identifies subtle errors (plausible but wrong details). Adjusts prompts to reduce hallucination risk. Reviews with a skeptical lens.",
        "level_4_label": "Champion",
        "level_4_descriptor": "Develops verification checklists for team use. Can explain failure modes of AI summarization. Trains peers on review discipline.",
    },
    {
        "domain_id": "data_safety",
        "role_id": "rm",
        "title": "Data Safety and Compliance",
        "description": (
            "Applying the public/non-public test before inputting client data into AI tools. "
            "Abstracting and anonymizing non-public information (credit figures, deal terms, "
            "private expansion plans) while still getting useful AI assistance."
        ),
        "level_0_label": "Unaware",
        "level_0_descriptor": "Unaware of the non-public data rule or does not apply it in practice. May paste CRM records directly into public AI tools.",
        "level_1_label": "Explorer",
        "level_1_descriptor": "Knows the rule ('don't share non-public info') but cannot reliably distinguish public from non-public in real client scenarios.",
        "level_2_label": "Practitioner",
        "level_2_descriptor": "Applies the public/non-public test consistently. Abstracts client names and specific figures before prompting. Avoids policy violations.",
        "level_3_label": "Proficient",
        "level_3_descriptor": "Handles borderline cases confidently (e.g., NPS scores, internal notes, inferred financials). Rewrites prompts to preserve utility while removing risk.",
        "level_4_label": "Champion",
        "level_4_descriptor": "Identifies novel compliance risks in new use cases. Advises team on safe patterns. Acts as a data-safe AI usage model for peers.",
    },
    {
        "domain_id": "tool_fluency",
        "role_id": "rm",
        "title": "Tool Fluency (M365 + Copilot)",
        "description": (
            "Choosing the right M365 Copilot surface (Outlook, Teams, Excel, Word/SharePoint) "
            "for each task and building multi-step workflows where output from one tool feeds "
            "the next — from meeting recap to CRM log to follow-up email."
        ),
        "level_0_label": "Unaware",
        "level_0_descriptor": "Has not used Copilot features in M365 tools for work tasks. Unaware of which tools have AI capabilities.",
        "level_1_label": "Explorer",
        "level_1_descriptor": "Has tried one or two Copilot features (e.g., Outlook email draft). Does not connect tools into workflows.",
        "level_2_label": "Practitioner",
        "level_2_descriptor": "Uses at least three M365 Copilot surfaces regularly. Builds simple two-step workflows (e.g., Teams recap → C3 log).",
        "level_3_label": "Proficient",
        "level_3_descriptor": "Designs multi-step workflows across 3+ Copilot surfaces. Chooses the right entry point based on input type. Recovers gracefully when one step produces poor output.",
        "level_4_label": "Champion",
        "level_4_descriptor": "Documents and shares workflows with the team. Identifies new Copilot surfaces or features applicable to RM work. Trains peers on multi-step patterns.",
    },
]

sql(f"DELETE FROM {CATALOG}.content.domains WHERE role_id = 'rm'")

for d in DOMAINS:
    sql(f"""
    INSERT INTO {CATALOG}.content.domains (
      domain_id, role_id, title, description,
      level_0_label, level_0_descriptor,
      level_1_label, level_1_descriptor,
      level_2_label, level_2_descriptor,
      level_3_label, level_3_descriptor,
      level_4_label, level_4_descriptor
    ) VALUES (
      '{escape(d['domain_id'])}',
      '{escape(d['role_id'])}',
      '{escape(d['title'])}',
      '{escape(d['description'])}',
      '{escape(d['level_0_label'])}', '{escape(d['level_0_descriptor'])}',
      '{escape(d['level_1_label'])}', '{escape(d['level_1_descriptor'])}',
      '{escape(d['level_2_label'])}', '{escape(d['level_2_descriptor'])}',
      '{escape(d['level_3_label'])}', '{escape(d['level_3_descriptor'])}',
      '{escape(d['level_4_label'])}', '{escape(d['level_4_descriptor'])}'
    )
    """)
    print(f"Seeded domain: {d['title']}")

print("\n✓ Roles and domains seeded successfully.")
