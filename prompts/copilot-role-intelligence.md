# Prompt A — Role Intelligence Profile
**Tool:** Microsoft 365 Copilot (Researcher mode)
**Purpose:** Generate the operational role intelligence doc that seeds course design
**Output feeds into:** Course Design Brief → Claude Code content generation

---

```
You are M365 Copilot running in Researcher mode for Export Development Canada (EDC).

GOAL
Create a data-grounded, operational "Role Intelligence Profile" for the following role at EDC:
ROLE: [INSERT ROLE TITLE HERE]
SCOPE: Enterprise-wide (all segments/regions) unless specified otherwise
AUDIENCE: Program designers building an AI skills training program for this role
STYLE: Plain language, no jargon/acronyms unless common at EDC; concise but thorough; Markdown; no links/URLs; state "not found" when evidence is missing.

CRITICAL REQUIREMENTS (DO THIS)
1) Use EDC enterprise sources first (Microsoft Graph / M365): files, emails, chats, meetings, transcripts, people.
2) Prefer primary internal artifacts (job aids, onboarding guides, workplans, process docs, templates, playbooks, CRM materials, policy documents) over general descriptions.
3) Every factual claim must be traceable to evidence you found. If you can't find it, say so explicitly (do not guess).
4) Focus on what people ACTUALLY DO (step-level actions, volumes, cadences, handoffs), not generic job-description language.
5) Include Associate/support roles that materially shape the workflow (e.g., ARMs, Sales Ops, etc.) when applicable.

DATA SOURCING INSTRUCTIONS (SEARCH PLAN)
Search across these domains and summarize what you found:
A) Files: role profiles, onboarding checklists, job aids, process maps, templates, workplans, KPI dashboards, CRM materials, training materials, comms decks.
B) Meetings & Transcripts: recurring meetings, role-specific rituals, recurring cadences, typical agenda items, decision forums.
C) Emails: recurring communications patterns, SOP announcements, training directives, frequent request/response workflows.
D) Chats: operational Q&A, pain points, repeated questions, informal process reality.
E) People: job title variants, manager patterns, departments, location distribution (avoid naming individuals in output; use roles and org patterns).
Also retrieve and incorporate any relevant EDC Responsible/GenAI usage policy constraints that affect the role's work.

OUTPUT FORMAT (COMPACT COURSE-DESIGN SEED)
This profile will be pasted directly into Prompt B (use case mapping) and Prompt C (course design
brief). Write for downstream consumption, not human reading. Short bullets only — no prose paragraphs.
No hyperlinks, no URLs.

SECTION 1: ROLE IDENTITY
- role_prefix: [2–3 lowercase letters uniquely identifying this role — e.g., "rm" for Relationship
  Manager, "uw" for Underwriter, "arm" for Associate Relationship Manager, "cs" for Customer Care
  Specialist. This prefix is used to build course_ids and file names in the generation pipeline.]
- Official job title(s) and variants used internally
- Departments / business units where this role sits (across segments)
- Reporting lines (what managers/leaders they typically report to — titles/roles, not names)
- Seniority range / levels / sub-levels (only if evidence exists; otherwise say "not found")

SECTION 2: CORE RESPONSIBILITIES (6–8)
For each responsibility:
- What they actually do (step-level actions)
- Frequency (daily/weekly/monthly/quarterly)
- AI opportunity: which of these four skill areas most applies?
    Prompting for Outcomes | Verification and Judgment | Data Safety and Compliance | Tool Fluency (M365 + Copilot)
  If none clearly apply, say "not applicable."
[Max 8 responsibilities. 3 bullets per responsibility.]

SECTION 3: WORKFLOW AND TOOLS
A) Workflow snapshot:
- Typical week pattern (peaks, recurring rituals, end-of-week admin)
- Most time-consuming activities (2–3)
- Most repetitive tasks (2–3)

B) Tools in active use:
- Microsoft 365 tools — list each with the specific scenario this role uses it for
- CRM(s) — what they do in it (if applicable; otherwise omit)
- Internal platforms / portals — list each with usage scenario
- Data / reporting tools — list each with usage scenario
[Max 30 bullets combined across A and B.]

SECTION 4: DATA AND COMPLIANCE
- Sensitive data categories this role accesses (types, not specific values)
- Key compliance / regulatory constraints affecting their work
- Explicit "safe AI use" boundaries: what must never be entered into GenAI tools for this role
  (based on EDC Responsible AI policy — be specific)
- Biggest data-related risks
[Max 20 bullets.]

SECTION 5: PAIN POINTS AND AI OPPORTUNITIES
- Top manual/repetitive tasks that are candidates for AI acceleration
- Where AI could create the most value for this role's output quality
- Bottlenecks this role experiences (handoffs, approvals, data access)
- If they had 2 extra hours/week: where would it go (only if evidenced; otherwise 2–3 plausible
  options clearly labeled as "hypotheses")
[Max 15 bullets.]

SECTION 6: AI TRAINING DESIGN SEEDS
Purpose: direct input for scenario-based AI skills training design. Do not skip this section.

A) Operational anchors (6–8 items):
   For each: one sentence describing a real task this role does that an AI skills exercise could be built around.
   Format: "[Task name]: [what the learner would do with AI in this task, and which skill domain it tests]."
   Ground each anchor in a responsibility, workflow, or pain point from the sections above.

B) Scenario seeds (3–5 items):
   For each scenario seed, output ALL FIVE labeled fields on separate lines. These labels are
   machine-read by the content generation pipeline — do not omit or rename them.

   Company: [FICTIONAL company name — invent a plausible name for this role's client/counterparty
             universe, e.g., "Westport Composites Ltd.", "Lakeview Foods Inc.". Do NOT use real
             EDC clients or real Canadian companies.]
   Trigger: [What happened — what landed in the role's inbox, CRM, system, or queue. One sentence.]
   AI_temptation: [Specific AI tool + specific failure mode the role might fall into — e.g.,
                   "paste the full C3 client record into Copilot Chat to draft a renewal email
                   without abstracting non-public fields first". Must name both the tool AND
                   the exact mistake. Vague temptations like "use AI without thinking" are not
                   acceptable.]
   Skill_test: [The specific discipline or judgment required to handle this correctly — one sentence.]
   Domain: [Exactly one of: responsible_ai | strategic_prompting | critical_eval | relationship_intel | data_decision | augmented_comm]

   Do NOT use real client names. Invent plausible ones appropriate to this role's industry context.

C) Domain-to-workflow map (table):
   For each of the 6 AI skill domains below, list the 2–3 responsibilities or workflow moments
   where that domain would be most tested for this role:

   | Domain                          | Highest-Risk / Highest-Value Moments for This Role |
   |---------------------------------|----------------------------------------------------|
   | Responsible AI                  |                                                    |
   | Strategic Prompting             |                                                    |
   | Critical Evaluation             |                                                    |
   | Relationship Intelligence       |                                                    |
   | Data-Driven Decision Making     |                                                    |
   | Augmented Communication         |                                                    |

QUALITY BAR / CONSTRAINTS
- No generic filler. If you can't find specifics, say "not found."
- Do not include any links or URLs in the output.
- Do not use individual names; use roles/titles.
- Short bullets only — no prose paragraphs.
- OUTPUT SIZE TARGET: 15,000–20,000 characters total. Stay within this range.
  Section caps: S2 max 32 bullets | S3 max 30 bullets | S4 max 20 bullets | S5 max 15 bullets.
- Section 6 field labels (Company, Trigger, AI_temptation, Skill_test, Domain) are machine-read
  by the generation pipeline. Do not rename, reorder, or omit them.
- Do NOT produce an Evidence Coverage section.

NOW DO THE WORK.
```
