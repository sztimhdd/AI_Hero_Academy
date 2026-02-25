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

OUTPUT FORMAT (STRICT)
Provide the following sections with bullet points and operational detail. Keep it clean: no hyperlinks, no URLs.

SECTION 1: ROLE FUNDAMENTALS
- role_prefix: [2–3 lowercase letters uniquely identifying this role — e.g., "rm" for Relationship Manager, "uw" for Underwriter, "arm" for Associate Relationship Manager, "cs" for Customer Care Specialist. This prefix is used to build course_ids and file names in the generation pipeline.]
- Official job title(s) and variants used internally
- Departments / business units where this role sits (across segments)
- Reporting lines (what managers/leaders they typically report to — titles/roles, not names)
- Approximate headcount (only if you can find explicit evidence; otherwise say "not found")
- Seniority range / levels / sub-levels (only if evidence exists)

SECTION 2: CORE RESPONSIBILITIES (8–10)
For each responsibility:
- What they actually do (step-level actions)
- Frequency (daily/weekly/monthly/quarterly) and any SLAs
- Inputs they need and where they come from
- Outputs produced and who depends on them (internal roles + external stakeholders)
- Systems where the work is recorded (system-of-record)
- AI opportunity: which of these four skill areas most applies to this responsibility?
    Prompting for Outcomes | Verification and Judgment | Data Safety and Compliance | Tool Fluency (M365 + Copilot)
  If none clearly apply, say "not applicable."

SECTION 3: DAILY AND WEEKLY WORKFLOWS
- Typical Monday morning
- Typical week pattern (cadence, peaks, end-of-week admin)
- Recurring meetings: what they are, why they happen, what the role does in them
- Most time-consuming activities
- Most repetitive tasks
- Low-value/admin work (and why it exists)

SECTION 4: TOOLS AND SYSTEMS (COMPREHENSIVE)
List every tool you find evidence for, grouped by:
- Microsoft 365 tools
- CRM(s) and what they do in it
- Internal platforms/portals
- Data/reporting tools
- Any other software
For each tool: specific usage scenarios, typical artifacts created/updated, and pain points.

SECTION 5: DOCUMENTS AND CONTENT
A) They CREATE regularly:
- Document type
- Audience
- Typical length/format
- Frequency
- Source-of-truth location (e.g., CRM record vs. SharePoint vs. email attachment) — describe without links

B) They RECEIVE/READ/ANALYZE regularly:
- Document type
- Source
- What they look for
- Actions/decisions triggered

SECTION 6: COMMUNICATION AND STAKEHOLDERS
- Primary internal stakeholders (roles)
- External stakeholders
- Most common email types
- Meetings they lead vs attend
- Presentations/briefings: for whom and how often
- Communication tasks that take the most time/effort

SECTION 7: DATA AND INFORMATION HANDLING
- Types of customer/client data accessed
- Sensitive/confidential data categories encountered
- Compliance/regulatory constraints relevant to this role
- Financial data types handled (if any)
- PII exposure (if any)
- Biggest data-related risks
- Explicit "safe AI use" boundaries for this role based on EDC policy (what must never be entered into GenAI; human review; transparency expectations)

SECTION 8: DECISIONS AND JUDGMENT
- Most important decisions they make
- Where mistakes have biggest consequences
- What must be verified before acting
- Escalation triggers (when they must escalate vs decide)
- What "good judgment" looks like in observable behaviors

SECTION 9: PAIN POINTS AND TIME SINKS
- Common frustrations (only if evidenced)
- Manual work candidates for automation/acceleration
- Bottlenecks and where they occur (handoffs, approvals, systems)
- If they had 2 extra hours/week: where would it go (only if evidenced; otherwise provide 2–3 plausible options clearly labeled as "hypotheses")

SECTION 10: PERFORMANCE AND SUCCESS METRICS
- How performance is measured (KPIs/targets/SLAs) — only from evidence
- Observable behaviors of top performers vs average (only if evidence exists; otherwise label as hypotheses)
- Valued skills/capabilities
- Common development areas/skill gaps (only if evidence exists)

SECTION 11: CURRENT AI TOOL USAGE (IF EVIDENCED)
- Which AI tools are used (Copilot, approved tools)
- Use cases (what they use it for)
- What works well
- What concerns exist (privacy, accuracy, tone, compliance)
- Any known misuse/risky patterns (only if evidenced)

SECTION 12: REGULATORY AND COMPLIANCE CONTEXT
- Relevant regulations/standards affecting the role
- Client communication rules, record-keeping requirements
- Consequences of compliance failures (only if evidenced)
- Restrictions on AI use for specific tasks

SECTION 13: AI TRAINING DESIGN SEEDS
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
   Domain: [Exactly one of: prompting | verification | data_safety | tool_fluency]

   Do NOT use real client names. Invent plausible ones appropriate to this role's industry context.

C) Domain-to-workflow map (table):
   For each of the 4 AI skill domains below, list the 2–3 responsibilities or workflow moments
   where that domain would be most tested for this role:

   | Domain                          | Highest-Risk / Highest-Value Moments for This Role |
   |---------------------------------|----------------------------------------------------|
   | Prompting for Outcomes          |                                                    |
   | Verification and Judgment       |                                                    |
   | Data Safety and Compliance      |                                                    |
   | Tool Fluency (M365 + Copilot)   |                                                    |

QUALITY BAR / CONSTRAINTS
- No generic filler. If you can't find specifics, say "not found."
- Do not include any links or URLs in the output.
- Do not use individual names; use roles/titles.
- Use short bullets; avoid long paragraphs.
- End with a short "Evidence Coverage" section listing which enterprise sources were most useful
  (e.g., "onboarding guide," "workplan," "job aid," "policy," "meeting transcript") without links.

NOW DO THE WORK.
```
