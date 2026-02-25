# Prompt B — Use Case Mapping
**Tool:** Microsoft 365 Copilot (regular chat) or Claude Code
**Purpose:** Filter the EDC use case library to the most relevant cases for the target role, map them to the 4 AI skill domains, and propose course anchors
**Output feeds into:** Course Design Brief → Claude Code content generation

> **Where to run this:**
> - **Copilot (M365):** Upload `references/List-of-Use-Cases-all.csv` as a file attachment, then paste the prompt. Use regular chat mode, not Researcher mode — this is analysis, not M365 data retrieval.
> - **Claude Code (recommended):** Paste the prompt and reference the file directly at `references/List-of-Use-Cases-all.csv`. Claude Code reads the file with full fidelity and produces more structured, consistent output.
>
> **Prerequisite:** Complete Prompt A first. Paste the role intelligence profile output into the `[PASTE ROLE INTELLIGENCE PROFILE HERE]` placeholder below.

---

```
CONTEXT
You are helping design an AI skills training program for a new role at EDC (Export Development Canada).

The program has 4 fixed skill domains — all roles use the same 4 domains:
  1. Prompting for Outcomes — structuring AI prompts to produce directly usable outputs
  2. Verification and Judgment — reviewing AI outputs critically before acting on them
  3. Data Safety and Compliance — applying the public/non-public test; abstracting sensitive data
  4. Tool Fluency (M365 + Copilot) — choosing the right Copilot surface and chaining M365 tools

Each role gets 5 courses:
  - Courses 1–4: one per domain
  - Course 5: a capstone that integrates all 4 domains in a single realistic workflow

INPUTS
Role: [INSERT ROLE TITLE]

Role Intelligence Profile:
[PASTE ROLE INTELLIGENCE PROFILE HERE — output from Prompt A]

Use case library: references/List-of-Use-Cases-all.csv
(CSV columns: Title, Business Line, Description)

---

TASK 1 — Filter and score relevance
Read every row in the use case CSV. For each row, assess relevance to [INSERT ROLE]'s
day-to-day work based on the role profile above.

Score relevance using these criteria:
  HIGH — the use case describes a task this role does directly, names tools they use,
         or was submitted by their department / a closely related team
  MEDIUM — the use case is adjacent (similar workflow, different team) and could be
            adapted to this role's context
  LOW / SKIP — unrelated department, unrelated workflow, or too generic to adapt

Output a ranked shortlist of 8–12 HIGH and MEDIUM use cases only.
Format as a table:

| # | Use Case Title | Business Line | Why Relevant to [ROLE] | Relevance |
|---|----------------|---------------|------------------------|-----------|

---

TASK 2 — Map to AI skill domain
For each shortlisted use case, identify the primary AI skill domain it anchors:

  → Prompting for Outcomes:
     use cases about drafting, briefing, prompt writing, generating structured content,
     research synthesis, preparing for meetings or client interactions

  → Verification and Judgment:
     use cases about reviewing AI output, meeting recaps, summaries, audit review,
     checking accuracy of generated text before using it

  → Data Safety and Compliance:
     use cases about inputting client data, CRM exports, non-public information,
     privacy concerns, data classification, compliance checking

  → Tool Fluency (M365 + Copilot):
     use cases about choosing the right tool, chaining M365 surfaces, workflow
     automation, multi-step AI-assisted processes across Outlook / Teams / Excel / Word

  → Capstone candidate: use cases that span 2 or more domains naturally

Update the table with two new columns:

| # | Use Case Title | Business Line | Why Relevant | Relevance | Domain | Capstone (Y/N) |

---

TASK 3 — Propose course anchors
Based on your table above, recommend which use case best anchors each of the 5 courses.
For each course, provide:
  - course_id: [role_prefix]_c[N]_[domain_id]  — e.g., uw_c1_prompting, uw_c2_verification
    (use the role prefix from Section 1 of the Role Intelligence Profile)
  - The use case title (verbatim from the CSV — do not paraphrase)
  - real_use_case: the verbatim use case title(s) from the CSV, exactly as they appear in the
    Title column. Do NOT paraphrase, shorten, or rephrase. This field is quoted directly into
    the course content JSON by the generation pipeline.
  - A 1–2 sentence rationale: what real task from this role does the use case connect to?
  - A suggested course title (plain language, action-oriented, ~8 words)

Format:
  Course 1 – Prompting for Outcomes
    course_id: [role_prefix]_c1_prompting
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV — multiple titles separated by semicolons]
    Rationale: [1–2 sentences]
    Suggested title: [draft course title]

  Course 2 – Verification and Judgment
    course_id: [role_prefix]_c2_verification
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1–2 sentences]
    Suggested title: [draft course title]

  Course 3 – Data Safety and Compliance
    course_id: [role_prefix]_c3_data_safety
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1–2 sentences]
    Suggested title: [draft course title]

  Course 4 – Tool Fluency (M365 + Copilot)
    course_id: [role_prefix]_c4_tool_fluency
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1–2 sentences]
    Suggested title: [draft course title]

  Course 5 – Capstone
    course_id: [role_prefix]_c5_capstone
    Use case(s): [verbatim title(s) from CSV]
    real_use_case: [verbatim title(s) from CSV — all titles used, semicolon-separated]
    Rationale: [1–2 sentences explaining how it integrates multiple domains]
    Suggested title: [draft course title]

---

TASK 4 — Gap check
For any domain where no use case in the shortlist is a strong fit, flag it explicitly:

  "Domain [X]: No strong use case match found in the library.
   Recommend synthesizing a scenario directly from the role profile.
   Suggested scenario seed: [1–2 sentences based on Section 13B of the role profile]."

If all 4 domains are covered, say: "All domains covered. No synthesis needed."

---

OUTPUT RULES
- Only reference use cases that actually exist in the CSV. Do not invent new ones.
- Keep rationales grounded in the role profile evidence. Do not use generic language.
- If you are uncertain about a domain mapping, note the ambiguity briefly.
- Plain markdown output. Tables for Tasks 1–2. Structured prose for Tasks 3–4.
```
