# Prompt C — Course Design Brief
**Tool:** Microsoft 365 Copilot (regular chat mode — not Researcher mode)
**Attachments:** `references/List-of-Use-Cases-all.csv` (attach as a file)
**Paste in:** Output from Prompt A (role intelligence profile) + Output from Prompt B (use case mapping)
**Purpose:** Generate the full Course Design Brief for a new role — the structured document Claude Code uses to produce all 7 JSON content files
**Output feeds into:** Claude Code → JSON content generation (all 7 files)

> **How to use this prompt:**
> 1. Paste the full text below into Copilot chat
> 2. Replace every `[INSERT ...]` placeholder before sending
> 3. Attach `references/List-of-Use-Cases-all.csv` as a file
> 4. Review the output before passing to Claude Code — the brief is your quality gate

---

```
CONTEXT
You are a course designer for AI Hero Academy, an internal AI skills training program at
Export Development Canada (EDC). You are creating the Course Design Brief for a new role.
This brief is the complete specification Claude Code will use to generate all course content.
It must be detailed, grounded in the role's real workflows, and follow the exact structure shown
in the few-shot examples below.

PROGRAM STRUCTURE
Each role in AI Hero Academy gets exactly:
  - 6 AI skill domains (always the same 6 titles; descriptors are role-specific)
  - 7 courses (1 per domain for courses 1–6; course 7 is a capstone integrating all 6 domains)
  - Per course: 1 reading module, 1 practice scenario (4 tasks), 4 evaluation items (3 MCQ + 1 performance task)
  - 1 diagnostic: 18 questions total (3 per domain × 6 domains: 1 MCQ + 1 prompt_sandbox + 1 micro_task)

The 6 fixed domain titles (descriptions and level descriptors must be adapted to the new role):
  Domain 1: Responsible AI
  Domain 2: Strategic Prompting
  Domain 3: Critical Evaluation
  Domain 4: Relationship Intelligence
  Domain 5: Data-Driven Decision Making
  Domain 6: Augmented Communication

INPUTS
Role: [INSERT ROLE TITLE HERE]
Role ID prefix: [INSERT SHORT PREFIX — e.g., "uw" for Underwriter, "arm" for ARM]

Role Intelligence Profile (from Prompt A):
[PASTE PROMPT A OUTPUT HERE]

Use Case Mapping (from Prompt B):
[PASTE PROMPT B OUTPUT HERE]

---

FEW-SHOT EXAMPLES
The following are the complete, production-ready content specifications for the
Relationship Manager (RM) role. Use these as your structural and quality template.
Adapt every detail — descriptions, examples, scenarios, client types, tools, workflows —
to the new role. Do not copy RM-specific content.

════════════════════════════════════════════════════════════════════
EXAMPLE: ROLE ENTRY
════════════════════════════════════════════════════════════════════

role_id: rm
title: Relationship Manager
description: "Manages a portfolio of Canadian exporter clients across segments (Small Business,
Mid-Market). Responsible for lead qualification, discovery, solution positioning, pipeline
hygiene, and portfolio retention. Works closely with Associate Relationship Managers (ARMs),
Sales Operations, and internal product teams."

════════════════════════════════════════════════════════════════════
EXAMPLE: DOMAIN SPECS (all 6, RM role)
════════════════════════════════════════════════════════════════════

DOMAIN 1 — Responsible AI
  domain_id: responsible_ai
  title: Responsible AI
  description: "Applying EDC's Responsible AI usage policy before inputting client data into
  AI tools. Abstracting and anonymising non-public information (credit figures, deal terms,
  private expansion plans) while still getting useful AI assistance."
  level_0_label: Unaware
  level_0_descriptor: "Unaware of the non-public data rule or does not apply it in practice. May paste CRM records directly into public AI tools."
  level_1_label: Explorer
  level_1_descriptor: "Knows the rule ('don't share non-public info') but cannot reliably distinguish public from non-public in real client scenarios."
  level_2_label: Practitioner
  level_2_descriptor: "Applies the public/non-public test consistently. Abstracts client names and specific figures before prompting. Avoids policy violations."
  level_3_label: Proficient
  level_3_descriptor: "Handles borderline cases confidently (e.g., NPS scores, internal notes, inferred financials). Rewrites prompts to preserve utility while removing risk."
  level_4_label: Champion
  level_4_descriptor: "Identifies novel compliance risks in new use cases. Advises team on safe patterns. Acts as a data-safe AI usage model for peers."

DOMAIN 2 — Strategic Prompting
  domain_id: strategic_prompting
  title: Strategic Prompting
  description: "Structuring AI prompts with context, constraints, format, and audience to
  produce outputs that are directly usable in RM workflows — briefing documents, emails,
  CRM notes, and talking points."
  level_0_label: Unaware
  level_0_descriptor: "Has not used AI prompting in work tasks. Cannot describe what makes a prompt effective."
  level_1_label: Explorer
  level_1_descriptor: "Writes basic prompts ('summarize this'). Output often requires heavy editing or is too generic to use."
  level_2_label: Practitioner
  level_2_descriptor: "Uses structured prompts with context and format instructions. Output is usually usable with minor edits."
  level_3_label: Proficient
  level_3_descriptor: "Adapts prompts for complex scenarios. Adds constraints proactively. Iterates when output misses the mark."
  level_4_label: Champion
  level_4_descriptor: "Designs reusable prompt templates for team workflows. Coaches colleagues on prompting structure. Contributes new use cases."

DOMAIN 3 — Critical Evaluation
  domain_id: critical_eval
  title: Critical Evaluation
  description: "Reviewing AI outputs critically before acting on them — catching hallucinations,
  incorrect dates, invented facts, and misattributed statements in meeting recaps, summaries,
  and CRM entries."
  level_0_label: Unaware
  level_0_descriptor: "Treats AI outputs as accurate by default. Does not cross-reference against source material."
  level_1_label: Explorer
  level_1_descriptor: "Reads AI output before using it, but does not systematically verify against independent sources."
  level_2_label: Practitioner
  level_2_descriptor: "Routinely cross-references AI output against own notes. Removes or corrects unverifiable statements before logging."
  level_3_label: Proficient
  level_3_descriptor: "Identifies subtle errors (plausible but wrong details). Adjusts prompts to reduce hallucination risk. Reviews with a skeptical lens."
  level_4_label: Champion
  level_4_descriptor: "Develops verification checklists for team use. Can explain failure modes of AI summarisation. Trains peers on review discipline."

DOMAIN 4 — Relationship Intelligence
  domain_id: relationship_intel
  title: Relationship Intelligence
  description: "Using AI to prepare for client interactions with deeper context — researching
  client backgrounds, synthesising relationship history, and personalising outreach so every
  meeting, email, and follow-up reflects what the RM already knows about the client's
  situation, sector, and priorities."
  level_0_label: Unaware
  level_0_descriptor: "Has not used AI to research clients or prepare for meetings. Relies entirely on memory or manual CRM review before calls."
  level_1_label: Explorer
  level_1_descriptor: "Uses AI for basic client research (sector summaries, news). Output is generic and not tailored to the specific relationship or deal stage."
  level_2_label: Practitioner
  level_2_descriptor: "Uses AI to synthesise CRM notes, meeting history, and sector context into targeted briefing materials. Personalises outreach with relationship signals."
  level_3_label: Proficient
  level_3_descriptor: "Anticipates client objections and preferences using AI-surfaced relationship patterns. Adapts briefing depth based on deal stage and client sophistication."
  level_4_label: Champion
  level_4_descriptor: "Develops AI-assisted relationship playbooks for the team. Identifies client relationship signals that colleagues miss. Coaches peers on AI-powered meeting prep."

DOMAIN 5 — Data-Driven Decision Making
  domain_id: data_decision
  title: Data-Driven Decision Making
  description: "Using AI to surface portfolio patterns, identify cross-sell opportunities, and
  support deal qualification and pipeline prioritisation — without over-relying on AI outputs
  that lack the full commercial context an RM holds."
  level_0_label: Unaware
  level_0_descriptor: "Does not use AI for portfolio analysis or pipeline decisions. Relies exclusively on manual CRM review and intuition."
  level_1_label: Explorer
  level_1_descriptor: "Uses AI to summarise sector reports or market news. Does not connect AI outputs to specific deal or portfolio decisions."
  level_2_label: Practitioner
  level_2_descriptor: "Uses AI to analyse pipeline health, flag at-risk accounts, or identify cross-sell opportunities from CRM data. Validates AI suggestions against own knowledge."
  level_3_label: Proficient
  level_3_descriptor: "Designs AI queries to surface deal patterns across multiple factors (sector, tenure, product mix). Uses AI to stress-test assumptions before client conversations."
  level_4_label: Champion
  level_4_descriptor: "Develops team-level AI prompts for quarterly portfolio reviews. Identifies data signals that predict client attrition or expansion. Shares AI prioritisation frameworks with peers."

DOMAIN 6 — Augmented Communication
  domain_id: augmented_comm
  title: Augmented Communication
  description: "Choosing the right M365 Copilot surface (Outlook, Teams, Word/SharePoint)
  for each communication task and building multi-step workflows where output from one tool
  feeds the next — from meeting recap to CRM log to follow-up email."
  level_0_label: Unaware
  level_0_descriptor: "Has not used Copilot features in M365 tools for communication tasks. Unaware of which tools have AI capabilities."
  level_1_label: Explorer
  level_1_descriptor: "Has tried one or two Copilot features (e.g., Outlook email draft). Does not connect tools into multi-step communication workflows."
  level_2_label: Practitioner
  level_2_descriptor: "Uses at least three M365 Copilot surfaces regularly for RM communications. Builds simple two-step workflows (e.g., Teams recap → CRM log)."
  level_3_label: Proficient
  level_3_descriptor: "Designs multi-step communication workflows across 3+ Copilot surfaces. Chooses the right entry point based on input type and output goal. Recovers gracefully when one step produces poor output."
  level_4_label: Champion
  level_4_descriptor: "Documents and shares communication workflows with the team. Identifies new Copilot surfaces or features applicable to RM work. Trains peers on multi-step patterns."

════════════════════════════════════════════════════════════════════
EXAMPLE: COURSE SPECS (Course 2 shown in full; same structure for courses 1, 3–7)
════════════════════════════════════════════════════════════════════

course_id: rm_c2_strategic_prompting
role_id: rm
primary_domain: strategic_prompting
sequence_order: 2
title: "Brief Like a Pro: From ARM Handoff to Discovery Brief"
tagline: "Turn a messy ARM handoff into a sharp discovery brief using the CRAF prompt framework."
description: "RMs spend significant time preparing for discovery calls. This course teaches the
CRAF framework (Context, Role, Action, Format) to produce briefing documents, discovery
questions, and talking points that are directly usable — not generic AI output that needs
full rewrites."
real_use_case: "Access to Copilot 365 for Business Development (Mid Market); Prospect
Intelligence; RM Support Agent"

════════════════════════════════════════════════════════════════════
EXAMPLE: SCENARIO SEEDS (Course 2 shown in full; same structure for courses 1, 3–7)
════════════════════════════════════════════════════════════════════

Course 2 — Scenario seed:
  scenario_text: "Your ARM, Jordan, just handed off Maple Industries Ltd. after a successful
  intro call. Notes show: Ontario manufacturer, $45M revenue, exports to US and Germany,
  currently uses another bank's letter of credit facility, open to exploring alternatives.
  You have a discovery call with their CFO in two days. You want to use AI to help you
  prepare a discovery brief."
  task_1: "Write a prompt to generate a discovery brief for your upcoming call with Maple
  Industries. Your ARM's notes are your only input. Use the CRAF framework."
  task_2: "Your first prompt produced useful but generic questions. Revise it to add a
  competitive angle — you know they use a competitor's LC facility and are 'open to
  alternatives.'"
  task_3: "The CFO is technically sophisticated and time-pressured. Revise the format
  instruction so the output leads with the most critical questions first."
  task_4: "The revised output still includes a section on domestic financing that is
  irrelevant to an exporter. Write a constraint to remove it in the next prompt iteration."
  coach_system_prompt: "You are an AI skills coach for EDC Relationship Managers. The learner
  is practicing the CRAF prompt framework applied to discovery prep. Guide them to improve
  their prompts through questions — do not write the prompt for them. If a CRAF element is
  missing, ask which element they think is weakest. Flag if any sensitive or non-public data
  appears (client records, internal financials, unpublished research, system credentials,
  or similar)."

════════════════════════════════════════════════════════════════════
EXAMPLE: READING CONCEPT SPECS (Course 2 shown; same structure for courses 1, 3–7)
════════════════════════════════════════════════════════════════════

Course 2 — Reading concept:
  framework_name: "CRAF (Context, Role, Action, Format)"
  concept_text: "Great AI output starts with a great prompt. The CRAF framework gives you four
  elements that consistently produce usable output:
  C — Context: Who is the client? What situation are they in? What do you already know?
  R — Role: What role should the AI play?
  A — Action: What exactly do you want it to do?
  F — Format: How should the output be structured?
  When all four elements are present, the AI knows who it is speaking as, who it is speaking
  about, what to produce, and how to present it. Missing any one element degrades the output."
  good_example: "Prompt: 'Context: Maple Industries Ltd., a $45M Ontario manufacturer, exports
  to US and Germany. No current EDC relationship. Uses a competitor's LC facility.
  Role: Senior RM at a Canadian export finance institution.
  Action: Draft a 200-word discovery brief with key questions for the first call.
  Format: Three sections — Business Context, Key Discovery Questions, Recommended Next Step.'
  Why it works: specific company profile, clear voice, concrete deliverable, defined structure."
  anti_pattern: "Prompt: 'Write a discovery brief for my new client.'
  Why it fails: no context, no role, no specific deliverable, no format. Output is a generic
  template useful to no one. The RM spends more time editing than the AI saved."
  takeaway: "A prompt is only as useful as the context you put in it. Specificity in all four
  CRAF elements is what separates output you can use from output you have to rewrite."

════════════════════════════════════════════════════════════════════
EXAMPLE: DIAGNOSTIC ITEM SEEDS (Strategic Prompting domain shown; same for all 6 domains)
════════════════════════════════════════════════════════════════════

Domain: strategic_prompting — 3 items

  Item 1 — type: mcq
  Tests: knowing which CRAF element is most commonly missing
  question_text: "An RM writes this prompt: 'Summarize what I should say on my next call with
  this client.' What is the most important missing element?"
  options: A) Context about the client and call purpose | B) A format instruction |
            C) A word count limit | D) A language instruction
  correct_option: A
  scoring: correct = 4, incorrect = 0

  Item 2 — type: prompt_sandbox
  Tests: writing a complete CRAF prompt from a real scenario
  scenario_text: "You just received an ARM handoff. Notes: Riverstone Logistics Ltd., BC-based
  freight forwarder, $18M revenue, exploring EDC financing for first time, CFO meeting
  next Tuesday."
  question_text: "Write a prompt using the CRAF framework to generate a 150-word discovery
  brief for your CFO meeting."
  scoring rubric criteria:
    - "Context is specific (company type, size, situation)": max 1
    - "Role instruction is present": max 1
    - "Action is clearly defined with a deliverable": max 1
    - "Format specifies length or structure": max 1

  Item 3 — type: micro_task
  Tests: identifying which prompt element caused a weak output
  scenario_text: "An RM received this AI output: 'Here are some general questions to ask
  in your discovery call: What are your main business goals? What challenges are you
  facing? How can we help you?' The prompt was: 'Help me prepare for a client call.'"
  question_text: "In one sentence, explain why the output is generic and name the two CRAF
  elements that are missing."
  scoring rubric criteria:
    - "Correctly identifies Context as missing": max 2
    - "Correctly identifies Action or Format as missing": max 2

════════════════════════════════════════════════════════════════════
EXAMPLE: EVALUATION ITEM SEEDS (Course 2 shown; same for all 7 courses)
════════════════════════════════════════════════════════════════════

Course 2 (rm_c2_strategic_prompting) — 4 items

  Item 1 — type: mcq, sequence: 1
  question_text: "Which CRAF element tells the AI how to structure its output?"
  options: A) Context | B) Role | C) Action | D) Format
  correct_option: D
  explanation: "Format defines the structure, length, and layout of the output."

  Item 2 — type: mcq, sequence: 2
  question_text: "An RM's prompt produces a 600-word generic overview of export finance instead
  of a focused client brief. Which prompt change would most directly fix this?"
  options:
    A) Add the client's name to the Context section
    B) Change the Action to specify a word count and a list of exactly 5 discovery questions
    C) Remove the Role instruction
    D) Ask the AI to use a friendlier tone
  correct_option: B
  explanation: "A specific Action instruction with a word count and deliverable format
  constrains the output scope. The problem is an under-specified Action, not missing Context."

  Item 3 — type: mcq, sequence: 3
  question_text: "Why does adding a Role instruction ('You are a senior RM at a Canadian
  export finance institution') improve prompt output?"
  options:
    A) It gives the AI a persona that calibrates vocabulary, assumed knowledge, and perspective
    B) It tells the AI to use formal language
    C) It prevents the AI from hallucinating
    D) It sets the output length
  correct_option: A
  explanation: "Role sets the AI's perspective and domain expertise — which affects the
  vocabulary, assumptions, and relevance of output. It doesn't directly control length or
  prevent hallucination."

  Item 4 — type: performance_task, sequence: 4
  question_text: "You just received an ARM handoff for Clearwater Shipping Ltd., a Nova
  Scotia-based shipping company, $22M revenue, exports to Caribbean markets, currently has
  no EDC relationship. You have an intro call with the VP Operations in 3 days.
  Write a complete CRAF prompt to generate a 200-word discovery brief for this call."
  scoring rubric:
    key1: "Context includes company description, revenue/size signal, market context,
          and current relationship status with EDC"
    key2: "Role instruction positions the AI as an RM or equivalent export finance professional"
    key3: "Action specifies a concrete deliverable (discovery brief) with a word count or
          section count"
    key4: "Format defines the structure (sections, bullet list, headers, or equivalent)"

════════════════════════════════════════════════════════════════════
CONTRAST EXAMPLE: ANALYST ROLE (abbreviated — structural reference only)
Use this to calibrate tone and scenario structure when the target role is NOT
client-facing. The RM example above shows the client-relationship pattern; this
example shows the internal research-and-synthesis pattern.
════════════════════════════════════════════════════════════════════

role_id: an
title: Analyst (Financial / Business / Sector)
description: "Produces research, financial models, sector briefings, and analytical
reports that inform decisions by internal stakeholders (underwriters, RMs, leadership).
Works across data sources, Excel models, and SharePoint repositories. Does not manage
client relationships directly — outputs are internal deliverables."

DOMAIN 1 (Analyst contrast) — Responsible AI
  domain_id: responsible_ai
  description: "Knowing which research inputs and outputs are safe to pass into AI tools —
  distinguishing publicly available sector data from embargoed third-party reports,
  unpublished financial models, and draft strategy documents. Abstracting confidential
  inputs while preserving analytical utility."
  level_2_descriptor: "Applies the public/non-public test to research inputs. Does not
  paste draft strategy documents, embargoed reports, or internal financial models into
  non-approved AI tools. Shares abstracted summaries or anonymised data instead."
  level_4_descriptor: "Identifies novel compliance risks in analytical AI workflows (e.g.,
  AI summarisation of embargoed sector reports). Documents safe vs. unsafe input patterns
  for the team. Acts as a data-safe AI usage model for peers."

DOMAIN 6 (Analyst contrast) — Augmented Communication
  domain_id: augmented_comm
  description: "Choosing the right M365 Copilot surface for research and synthesis tasks —
  using Copilot in Word to structure draft briefings, Excel for data interpretation, and
  Teams Recap for cross-functional meeting follow-up. Building multi-step workflows from
  raw data inputs to polished internal deliverables."
  level_2_descriptor: "Uses at least two Copilot surfaces for analytical work (e.g., Word
  for structuring a sector brief, Excel for summarising model outputs). Connects outputs
  from one tool into the next step without manual re-entry."

Scenario seed (Analyst — internal stakeholder context):
  scenario_text: "You have just completed a sector intelligence review for the Clean Energy
  portfolio. You have an internal briefing with the Underwriting team on Thursday and need
  to turn your raw research notes — spread across three Word docs and a Teams meeting
  recap — into a sharp 1-page sector brief."
  task_1: "Write a CRAF prompt to generate an executive summary of the sector review using
  your Teams meeting recap as the primary input."
  task_2: "The draft summary cited a third-party report that is still under embargo. Identify
  the data safety failure and rewrite the offending sentence using only publicly available
  data."
  coach_system_prompt: "You are an AI skills coach for EDC Analysts. The learner is
  practicing structured prompting for internal research synthesis. Guide them through
  questions — do not write the prompt for them. Flag if any embargoed, draft, or
  non-public source material appears to have been pasted directly into the prompt."

════════════════════════════════════════════════════════════════════
END OF FEW-SHOT EXAMPLES
════════════════════════════════════════════════════════════════════

---

YOUR TASK
Produce the complete Course Design Brief for [INSERT ROLE TITLE] using the structure above.

Before any section content, output a MACHINE-READABLE HEADER BLOCK at the very top of your
response (before SECTION A). This block is parsed programmatically — use exactly this format:

```
## MACHINE-READABLE HEADER

role_prefix: [2–3 lowercase letters from Section 1 of the Role Intelligence Profile]

company_map:
  course_1: [FICTIONAL company name for Course 1 scenario]
  course_2: [FICTIONAL company name for Course 2 scenario]
  course_3: [FICTIONAL company name for Course 3 scenario]
  course_4: [FICTIONAL company name for Course 4 scenario]
  course_5: [FICTIONAL company name for Course 5 scenario]
  course_6: [FICTIONAL company name for Course 6 scenario]
  course_7: [FICTIONAL company name for Course 7 (capstone) scenario]

framework_names:
  NOTE: These names are standardized across all roles where possible. Confirm which apply;
  adapt the role-specific examples in SECTION E (concept_text, good_example, anti_pattern)
  accordingly. Do NOT invent new framework names unless a standardized name genuinely does
  not fit.

  - [Course 1 — Responsible AI domain: standardized name is "The SAFE Abstraction Method" — use unless the role has a distinct data-handling protocol]
  - [Course 2 — Strategic Prompting domain: standardized name is "CRAF Framework" — use unless the role requires a meaningfully different prompting structure]
  - [Course 3 — Critical Evaluation domain: standardized name is "VERIFY Checklist" — use unless the role's verification workflow diverges significantly]
  - [Course 4 — Relationship Intelligence domain: no standardized name yet — propose a memorable acronym or framework name grounded in this role's client/stakeholder context]
  - [Course 5 — Data-Driven Decision Making domain: no standardized name yet — propose a memorable acronym or framework name grounded in this role's data and decision workflows]
  - [Course 6 — Augmented Communication domain: standardized name is "Copilot Surface Selector" — use unless the role's M365 tool set differs significantly from standard]
  - [Course 7 — Capstone: standardized name is "End-to-End AI Workflow" — use unless a role-specific multi-domain framework name is warranted]

real_use_case:
  course_1: [verbatim use case title(s) from Prompt B Task 3 — do not paraphrase]
  course_2: [verbatim use case title(s) from Prompt B Task 3]
  course_3: [verbatim use case title(s) from Prompt B Task 3]
  course_4: [verbatim use case title(s) from Prompt B Task 3]
  course_5: [verbatim use case title(s) from Prompt B Task 3]
  course_6: [verbatim use case title(s) from Prompt B Task 3]
  course_7: [verbatim use case title(s) from Prompt B Task 3]

capability_tags:
  NOTE: 3–6 lowercase_snake_case tags per course capturing the core AI skill taught.
  Used for path assembly matching in the atomic library. Match the framework name
  (e.g., "safe_framework") and 2–5 specific skills demonstrated in that course.
  course_1: [3–6 tags — e.g., "safe_framework", "data_classification", "prompt_abstraction"]
  course_2: [3–6 tags — e.g., "craf_framework", "prompt_structuring", "output_formatting"]
  course_3: [3–6 tags — e.g., "verify_checklist", "hallucination_detection", "output_validation"]
  course_4: [3–6 tags — e.g., stakeholder/relationship-intelligence-specific]
  course_5: [3–6 tags — e.g., data/decision-specific]
  course_6: [3–6 tags — e.g., "copilot_surface_selector", "m365_workflow", "communication_drafting"]
  course_7: [3–6 tags spanning all 6 domains — this is the capstone]
```

Each fictional entity name must be unique across all 7 courses (no repeats). For client-facing
roles, use fictional external company names appropriate to this role's client universe (industries,
sizes, geographies). For internally-focused roles, use fictional internal project names, working
group names, or team initiatives that reflect realistic EDC internal work (e.g., "Credit Analytics
Working Group", "FinOps Modernization Initiative", "Enterprise Data Governance Program").

Ground every section in:
1. The Role Intelligence Profile (pasted above) — especially Sections 2, 3, 5, 6
2. The Use Case Mapping (pasted above) — use the proposed course anchors from Task 3
3. The attached use case CSV — reference use case titles by name in real_use_case fields
4. Your M365 knowledge of this role at EDC (emails, SharePoint, Teams, meeting transcripts)
   to make scenarios realistic and tools authentic

Produce these sections IN ORDER:

SECTION A — Role Entry
  role_id: [derive from role prefix]
  title: [exact job title]
  description: [2–3 sentences; what the role does, who it serves, who it works with]

SECTION B — All 6 Domain Specs
  For each domain:
  - Keep the 6 domain titles and IDs exactly as shown in the examples
  - Adapt the description to name the specific artifacts and workflows of THIS role
    (not "briefing documents, emails, CRM notes" for the RM — those were RM-specific)
  - Write level descriptors (0–4) with concrete, role-specific behavioral examples
  - Level 2 (Practitioner) is the target proficiency for training completion
  - Level 4 (Champion) represents peer teaching and team contribution behaviors

SECTION C — All 7 Course Specs
  For each course, provide:
  course_id, role_id, primary_domain, sequence_order, title, tagline, description,
  real_use_case (cite actual use case titles from the CSV attachment)
  - Course 7 must be a capstone that integrates all 6 domains in a single workflow
  - Course titles should be action-oriented and role-specific (not generic)
  - Use the Use Case Mapping's Task 3 course assignments as your anchor

SECTION D — All 7 Scenario Seeds
  For each course, provide:
  scenario_text, task_1_text through task_4_text, coach_system_prompt
  Requirements:
  - Write in second person ("You have just...", "You are preparing...")
  - Use FICTIONAL entity names — for client-facing roles, invent plausible external company names
    (industries, size bands, geographies); for internally-focused roles (analysts, advisors, IT),
    use fictional internal project names, working group names, or team initiatives rather than
    external client companies
  - Domain balance: all 6 domains must be represented across the 7 scenario seeds (courses 1–7).
    If the role profile's Section 6B has no scenario seed for augmented_comm, synthesize the
    Course 6 (Augmented Communication) scenario from the multi-step M365 Copilot chain workflows
    described in Section 3 of the role profile (Workflow and Tools).
  - Each scenario must create an AI temptation (something the learner might rush to do wrong)
    and a skill test (the discipline or judgment required to do it right)
  - Tasks should progress in difficulty: task_1 is foundational, task_4 is the hardest
  - Coach system prompt: tell the AI coach what NOT to do (do not write the answer for them),
    what to watch for (red flags like real data entry), and how to guide without solving
  - For each scenario, add a `role_variants_hint` line: one sentence stating which
    placeholder values ({role}, {org_type}, {case_type}) are most critical for this
    course's scenario and how they would shift for a different professional role
    (e.g., "For engineering roles, replace {case_type} with 'code review ticket'
    and {org_type} with 'technology company'.")

SECTION E — All 7 Reading Concept Specs
  For each course, provide:
  framework_name (give the concept a memorable name or acronym if appropriate),
  concept_text, good_example, anti_pattern, takeaway
  Requirements:
  - The framework must be actionable (a checklist, a test, a sequence of steps, or an acronym)
  - good_example: show a specific, realistic before/after using this role's actual tool names
  - anti_pattern: describe the exact wrong behavior and its consequence in this role's context
  - concept_text: 150–300 words; clear teaching narrative with role-specific examples

SECTION F — Diagnostic Item Seeds (18 items: 3 per domain × 6 domains)
  For each domain, produce 3 items:
  Item 1: mcq — tests conceptual knowledge of the domain
  Item 2: prompt_sandbox — asks the learner to write a prompt for a role-specific scenario
  Item 3: micro_task — asks the learner to analyse or correct something
  For each item: question_text, scenario_text (for items 2–3), options (for MCQ),
  correct_option (for MCQ), scoring rubric criteria (for items 2–3, 4 criteria scoring 0–1 each)

SECTION G — Evaluation Item Seeds (28 items: 4 per course × 7 courses)
  For each course, produce 4 items:
  Items 1–3: mcq — tests application of the course concept
  Item 4: performance_task — asks the learner to apply the full concept in a realistic task
  For each MCQ: question_text, 4 options, correct_option, explanation (1–2 sentences)
  For performance_task: question_text with embedded scenario, 4 scoring rubric keys
    (each key describes what the response must demonstrate to earn that point)

---

OUTPUT FORMAT
- Plain markdown
- Start with the MACHINE-READABLE HEADER block (see above) before any section content
- Use the top-level section headers exactly as labeled: SECTION A through SECTION G
- Within SECTION B (Domains), use this exact sub-header for each domain (parser-critical):
    ### Domain: responsible_ai
    ### Domain: strategic_prompting
    ### Domain: critical_eval
    ### Domain: relationship_intel
    ### Domain: data_decision
    ### Domain: augmented_comm
- Within SECTION C (Courses), use this exact sub-header format (parser-critical):
    ### Course 1 — [Title]
    ### Course 2 — [Title]
    ### Course 3 — [Title]
    ### Course 4 — [Title]
    ### Course 5 — [Title]
    ### Course 6 — [Title]
    ### Course 7 — [Title]
- Within SECTION D (Scenarios), use this exact sub-header format:
    ### Course 1 Scenario
    ### Course 2 Scenario
    (etc.)
- Within SECTION E (Reading), use this exact sub-header format:
    ### Course 1 Reading
    ### Course 2 Reading
    (etc.)
- Within SECTION F (Diagnostic), use this exact sub-header format:
    ### Diagnostic: responsible_ai
    ### Diagnostic: strategic_prompting
    ### Diagnostic: critical_eval
    ### Diagnostic: relationship_intel
    ### Diagnostic: data_decision
    ### Diagnostic: augmented_comm
- Within SECTION G (Evaluation), use this exact sub-header format:
    ### Evaluation: Course 1
    ### Evaluation: Course 2
    (etc.)
- Within each section, use the field names from the examples (course_id, domain_id, etc.)
- No JSON — this is a brief, not code
- Do not truncate or abbreviate any section. If a section has 7 courses, produce all 7.

---

QUALITY RULES
- Every scenario must use FICTIONAL names — no real EDC clients, no real employees, no real
  internal projects, no real transaction data. For client-facing roles use fictional company
  names; for internal roles use fictional project or team names.
- All tools and systems referenced must be tools this role actually uses (from the role profile).
- Descriptions and level descriptors must be specific to this role's workflows — not
  copy-pasted from the RM examples.
- If the use case mapping flagged a domain gap (Task 4), synthesise a scenario from the
  role profile's Section 6A operational anchors instead. For an augmented_comm gap specifically
  (the domain most likely to have no Section 6B scenario seed), draw from Section 3 of the
  role profile (Workflow and Tools) — the M365 Copilot surfaces in active use and any multi-step
  chain workflows described there. Do NOT skip Course 6 or leave it generic.
- If you are uncertain about a role-specific detail, check your M365 knowledge of this
  role at EDC (SharePoint, emails, meeting transcripts). Do not guess.
- Do not truncate. Every section requires complete output.

SIZE + URL RULES
- Do NOT include any hyperlinks or URLs anywhere in the output. Reference documents
  by name only (e.g., "the EDC Responsible AI Policy" — not a URL). URLs inflate
  file size and cause downstream JSON parse failures in the content generation pipeline.
- OUTPUT SIZE TARGET: 60,000–70,000 characters total. Stay within this range.
  If you exceed 70,000 characters, review for verbose repetition and URL leakage first.

NOW DO THE WORK.

---

NOTE FOR FOLLOW-UP REQUESTS:
If you receive a follow-up message asking you to fill in missing or incomplete sections,
output ONLY the requested sections under the heading:

## SUPPLEMENTAL OUTPUT

Use the same section headers and field labels as above (e.g., "### Domain: responsible_ai",
"### Course 3 — [Title]"). Do not re-output sections that were already complete.
```
