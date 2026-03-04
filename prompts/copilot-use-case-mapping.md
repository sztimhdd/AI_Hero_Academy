# Prompt B — Use Case Mapping
**Tool:** Microsoft 365 Copilot (regular chat) or Claude Code
**Purpose:** Filter the EDC use case library to the most relevant cases for the target role, map them to the 6 AI skill domains, and propose course anchors
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

The program has 6 fixed skill domains — all roles use the same 6 domains:
  1. Responsible AI — applying the public/non-public test; abstracting sensitive data; AI usage policies
  2. Strategic Prompting — structuring AI prompts to produce directly usable outputs
  3. Critical Evaluation — reviewing AI outputs critically before acting on them
  4. Relationship Intelligence — using AI to strengthen client/stakeholder relationships
  5. Data-Driven Decision Making — using AI to surface insights and support decisions
  6. Augmented Communication — using AI to prepare, enhance, and tailor communications

Each role gets 7 courses:
  - Courses 1–6: one per domain
  - Course 7: a capstone that integrates all 6 domains in a single realistic workflow

INPUTS
Role: [INSERT ROLE TITLE]

Role Intelligence Profile:
[PASTE ROLE INTELLIGENCE PROFILE HERE — output from Prompt A]

Use case library: references/List-of-Use-Cases-all.csv
(CSV columns: Title, Business Line, Description)

---

TASK 1 & 2 — Filter, score, and map to domain (combined)
Read every row in the use case CSV. For each row, assess relevance to [INSERT ROLE]'s
day-to-day work based on the role profile above.

Score relevance:
  HIGH — task this role does directly, tools they use, or their department submitted it
  MEDIUM — adjacent workflow, different team, adaptable to this role's context
  LOW / SKIP — unrelated; skip these

Domain mapping (primary domain per use case):
  → Responsible AI: inputting client data, non-public information, privacy,
     data classification, compliance with AI usage policies
  → Strategic Prompting: drafting, prompt writing, generating structured content,
     research synthesis, preparing outputs for meetings or clients
  → Critical Evaluation: reviewing AI output, checking accuracy of generated
     text, summaries, recaps before acting on them
  → Relationship Intelligence: personalising outreach, briefing materials,
     client intelligence, stakeholder mapping, meeting prep with AI
  → Data-Driven Decision Making: using AI to analyse data, surface trends,
     build models or reports, support investment/underwriting decisions
  → Augmented Communication: drafting emails, presentations, summaries, and
     communications with AI; choosing the right Copilot surface; chaining M365
     tools across Outlook / Teams / Word / SharePoint
  → Capstone candidate: spans 2+ domains naturally

Output a compact shortlist of 8–12 HIGH and MEDIUM use cases.
Format as a table with EXACTLY these columns — no extra columns, no prose in cells:

| # | Use Case Title (verbatim) | Relevance | Domain | Capstone |
|---|---------------------------|-----------|--------|----------|

---

TASK 3 — Propose course anchors
Based on your table above, recommend which use case best anchors each of the 7 courses.
For each course, provide:
  - course_id: [role_prefix]_c[N]_[domain_id]  — e.g., uw_c1_responsible_ai, uw_c2_strategic_prompting
    (use the role prefix from Section 1 of the Role Intelligence Profile)
  - The use case title (verbatim from the CSV — do not paraphrase)
  - real_use_case: the verbatim use case title(s) from the CSV, exactly as they appear in the
    Title column. Do NOT paraphrase, shorten, or rephrase. This field is quoted directly into
    the course content JSON by the generation pipeline.
  - A 1-sentence rationale: what real task from this role does the use case connect to?
    (One sentence only — do not expand.)
  - A suggested course title (plain language, action-oriented, ~8 words)

Format:
  Course 1 – Responsible AI
    course_id: [role_prefix]_c1_responsible_ai
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV — multiple titles separated by semicolons]
    Rationale: [1 sentence]
    Suggested title: [draft course title]

  Course 2 – Strategic Prompting
    course_id: [role_prefix]_c2_strategic_prompting
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1 sentence]
    Suggested title: [draft course title]

  Course 3 – Critical Evaluation
    course_id: [role_prefix]_c3_critical_eval
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1 sentence]
    Suggested title: [draft course title]

  Course 4 – Relationship Intelligence
    course_id: [role_prefix]_c4_relationship_intel
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1 sentence]
    Suggested title: [draft course title]

  Course 5 – Data-Driven Decision Making
    course_id: [role_prefix]_c5_data_decision
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1 sentence]
    Suggested title: [draft course title]

  Course 6 – Augmented Communication
    course_id: [role_prefix]_c6_augmented_comm
    Use case: [verbatim title from CSV]
    real_use_case: [verbatim title(s) from CSV]
    Rationale: [1 sentence]
    Suggested title: [draft course title]

  Course 7 – Capstone
    course_id: [role_prefix]_c7_capstone
    Use case(s): [verbatim title(s) from CSV]
    real_use_case: [verbatim title(s) from CSV — all titles used, semicolon-separated]
    Rationale: [1 sentence explaining which domains it integrates and how]
    Suggested title: [draft course title]

---

TASK 4 — Gap check
For any domain where no use case in the shortlist is a strong fit, flag it explicitly:

  "Domain [X]: No strong use case match found in the library.
   Recommend synthesizing a scenario directly from the role profile.
   Suggested scenario seed: [1–2 sentences based on Section 6B of the role profile (AI Training Design Seeds)]."

If all 6 domains are covered, say: "All domains covered. No synthesis needed."

---

OUTPUT RULES
- Only reference use cases that actually exist in the CSV. Do not invent new ones.
- Keep rationales grounded in the role profile evidence. Do not use generic language.
- If you are uncertain about a domain mapping, note the ambiguity briefly.
- Plain markdown output. Compact table for Tasks 1–2. Structured list for Tasks 3–4.
- BREVITY IS CRITICAL: the output of this prompt is pasted into Prompt C (Course Design
  Brief), which has a limited context window. Every extra sentence in Tasks 1–2 burns
  context that Prompt C needs for content generation.
- When copying output to paste into Prompt C: include ONLY Tasks 3 and 4.
  Tasks 1–2 are for your own review — do not paste them into Prompt C.
```
