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
  - 4 AI skill domains (always the same 4 titles; descriptors are role-specific)
  - 5 courses (1 per domain for courses 1–4; course 5 is a capstone integrating all 4 domains)
  - Per course: 1 reading module, 1 practice scenario (4 tasks), 4 evaluation items (3 MCQ + 1 performance task)
  - 1 diagnostic: 12 questions total (3 per domain: 1 MCQ + 1 prompt_sandbox + 1 micro_task)

The 4 fixed domain titles (descriptions and level descriptors must be adapted to the new role):
  Domain 1: Prompting for Outcomes
  Domain 2: Verification and Judgment
  Domain 3: Data Safety and Compliance
  Domain 4: Tool Fluency (M365 + Copilot)

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
EXAMPLE: DOMAIN SPECS (all 4, RM role)
════════════════════════════════════════════════════════════════════

DOMAIN 1 — Prompting for Outcomes
  domain_id: prompting
  title: Prompting for Outcomes
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

DOMAIN 2 — Verification and Judgment
  domain_id: verification
  title: Verification and Judgment
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
  level_4_descriptor: "Develops verification checklists for team use. Can explain failure modes of AI summarization. Trains peers on review discipline."

DOMAIN 3 — Data Safety and Compliance
  domain_id: data_safety
  title: Data Safety and Compliance
  description: "Applying the public/non-public test before inputting client data into AI tools.
  Abstracting and anonymizing non-public information (credit figures, deal terms, private
  expansion plans) while still getting useful AI assistance."
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

DOMAIN 4 — Tool Fluency (M365 + Copilot)
  domain_id: tool_fluency
  title: Tool Fluency (M365 + Copilot)
  description: "Choosing the right M365 Copilot surface (Outlook, Teams, Excel, Word/SharePoint)
  for each task and building multi-step workflows where output from one tool feeds the next —
  from meeting recap to CRM log to follow-up email."
  level_0_label: Unaware
  level_0_descriptor: "Has not used Copilot features in M365 tools for work tasks. Unaware of which tools have AI capabilities."
  level_1_label: Explorer
  level_1_descriptor: "Has tried one or two Copilot features (e.g., Outlook email draft). Does not connect tools into workflows."
  level_2_label: Practitioner
  level_2_descriptor: "Uses at least three M365 Copilot surfaces regularly. Builds simple two-step workflows (e.g., Teams recap → C3 log)."
  level_3_label: Proficient
  level_3_descriptor: "Designs multi-step workflows across 3+ Copilot surfaces. Chooses the right entry point based on input type. Recovers gracefully when one step produces poor output."
  level_4_label: Champion
  level_4_descriptor: "Documents and shares workflows with the team. Identifies new Copilot surfaces or features applicable to RM work. Trains peers on multi-step patterns."

════════════════════════════════════════════════════════════════════
EXAMPLE: COURSE SPECS (Course 1 shown in full; same structure for courses 2–5)
════════════════════════════════════════════════════════════════════

course_id: rm_c1_prompting
role_id: rm
primary_domain: prompting
sequence_order: 1
title: "Brief Like a Pro: From ARM Handoff to Discovery Brief"
tagline: "Turn a messy ARM handoff into a sharp discovery brief using the CRAF prompt framework."
description: "RMs spend significant time preparing for discovery calls. This course teaches the
CRAF framework (Context, Role, Action, Format) to produce briefing documents, discovery
questions, and talking points that are directly usable — not generic AI output that needs
full rewrites."
real_use_case: "Access to Copilot 365 for Business Development (Mid Market); Prospect
Intelligence; RM Support Agent"

════════════════════════════════════════════════════════════════════
EXAMPLE: SCENARIO SEEDS (Course 1 shown in full; same structure for courses 2–5)
════════════════════════════════════════════════════════════════════

Course 1 — Scenario seed:
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
  missing, ask which element they think is weakest. Flag if any real client data appears."

════════════════════════════════════════════════════════════════════
EXAMPLE: READING CONCEPT SPECS (Course 1 shown; same structure for courses 2–5)
════════════════════════════════════════════════════════════════════

Course 1 — Reading concept:
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
EXAMPLE: DIAGNOSTIC ITEM SEEDS (Prompting domain shown; same for all 4 domains)
════════════════════════════════════════════════════════════════════

Domain: prompting — 3 items

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
EXAMPLE: EVALUATION ITEM SEEDS (Course 1 shown; same for all 5 courses)
════════════════════════════════════════════════════════════════════

Course 1 (rm_c1_prompting) — 4 items

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

framework_names:
  NOTE: These 5 names are standardized across all roles. Confirm which apply; adapt the
  role-specific examples in SECTION E (concept_text, good_example, anti_pattern) accordingly.
  Do NOT invent new framework names unless a standardized name genuinely does not fit.

  - [Course 1 — Prompting domain: standardized name is "CRAF Framework" — use unless the role requires a meaningfully different prompting structure]
  - [Course 2 — Verification domain: standardized name is "VERIFY Checklist" — use unless the role's verification workflow diverges significantly]
  - [Course 3 — Data Safety domain: standardized name is "The SAFE Abstraction Method" — use unless the role has a distinct data-handling protocol]
  - [Course 4 — Tool Fluency domain: standardized name is "Copilot Surface Selector" — use unless the role's M365 tool set differs from standard]
  - [Course 5 — Capstone: standardized name is "End-to-End AI Workflow" — use unless a role-specific multi-domain framework name is warranted]

real_use_case:
  course_1: [verbatim use case title(s) from Prompt B Task 3 — do not paraphrase]
  course_2: [verbatim use case title(s) from Prompt B Task 3]
  course_3: [verbatim use case title(s) from Prompt B Task 3]
  course_4: [verbatim use case title(s) from Prompt B Task 3]
  course_5: [verbatim use case title(s) from Prompt B Task 3]
```

Each fictional company name must be unique across all 5 courses (no repeats). Use company names
appropriate to this role's client/counterparty universe (industries, sizes, geographies).

Ground every section in:
1. The Role Intelligence Profile (pasted above) — especially Sections 2, 3, 9, 13
2. The Use Case Mapping (pasted above) — use the proposed course anchors from Task 3
3. The attached use case CSV — reference use case titles by name in real_use_case fields
4. Your M365 knowledge of this role at EDC (emails, SharePoint, Teams, meeting transcripts)
   to make scenarios realistic and tools authentic

Produce these sections IN ORDER:

SECTION A — Role Entry
  role_id: [derive from role prefix]
  title: [exact job title]
  description: [2–3 sentences; what the role does, who it serves, who it works with]

SECTION B — All 4 Domain Specs
  For each domain:
  - Keep the 4 domain titles and IDs exactly as shown in the examples
  - Adapt the description to name the specific artifacts and workflows of THIS role
    (not "briefing documents, emails, CRM notes" for the RM — those were RM-specific)
  - Write level descriptors (0–4) with concrete, role-specific behavioral examples
  - Level 2 (Practitioner) is the target proficiency for training completion
  - Level 4 (Champion) represents peer teaching and team contribution behaviors

SECTION C — All 5 Course Specs
  For each course, provide:
  course_id, role_id, primary_domain, sequence_order, title, tagline, description,
  real_use_case (cite actual use case titles from the CSV attachment)
  - Course 5 must be a capstone that integrates all 4 domains in a single workflow
  - Course titles should be action-oriented and role-specific (not generic)
  - Use the Use Case Mapping's Task 3 course assignments as your anchor

SECTION D — All 5 Scenario Seeds
  For each course, provide:
  scenario_text, task_1_text through task_4_text, coach_system_prompt
  Requirements:
  - Write in second person ("You have just...", "You are preparing...")
  - Use FICTIONAL company names — invent plausible ones appropriate to this role's
    client/counterparty universe (e.g., industries, size bands, geographies this role works with)
  - Domain balance: all 4 domains must be represented across the 5 scenario seeds (courses 1–5).
    If the role profile's Section 13B has no scenario seed for tool_fluency, synthesize the
    Course 4 (Tool Fluency) scenario from the multi-step M365 Copilot chain workflows described
    in Sections 3–4 of the role profile (tool inventory, surfaces in active use, handoff steps).
  - Each scenario must create an AI temptation (something the learner might rush to do wrong)
    and a skill test (the discipline or judgment required to do it right)
  - Tasks should progress in difficulty: task_1 is foundational, task_4 is the hardest
  - Coach system prompt: tell the AI coach what NOT to do (do not write the answer for them),
    what to watch for (red flags like real data entry), and how to guide without solving

SECTION E — All 5 Reading Concept Specs
  For each course, provide:
  framework_name (give the concept a memorable name or acronym if appropriate),
  concept_text, good_example, anti_pattern, takeaway
  Requirements:
  - The framework must be actionable (a checklist, a test, a sequence of steps, or an acronym)
  - good_example: show a specific, realistic before/after using this role's actual tool names
  - anti_pattern: describe the exact wrong behavior and its consequence in this role's context
  - concept_text: 150–300 words; clear teaching narrative with role-specific examples

SECTION F — Diagnostic Item Seeds (12 items: 3 per domain)
  For each domain, produce 3 items:
  Item 1: mcq — tests conceptual knowledge of the domain
  Item 2: prompt_sandbox — asks the learner to write a prompt for a role-specific scenario
  Item 3: micro_task — asks the learner to analyze or correct something
  For each item: question_text, scenario_text (for items 2–3), options (for MCQ),
  correct_option (for MCQ), scoring rubric criteria (for items 2–3, 4 criteria scoring 0–1 each)

SECTION G — Evaluation Item Seeds (20 items: 4 per course)
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
    ### Domain: prompting
    ### Domain: verification
    ### Domain: data_safety
    ### Domain: tool_fluency
- Within SECTION C (Courses), use this exact sub-header format (parser-critical):
    ### Course 1 — [Title]
    ### Course 2 — [Title]
    ### Course 3 — [Title]
    ### Course 4 — [Title]
    ### Course 5 — [Title]
- Within SECTION D (Scenarios), use this exact sub-header format:
    ### Course 1 Scenario
    ### Course 2 Scenario
    (etc.)
- Within SECTION E (Reading), use this exact sub-header format:
    ### Course 1 Reading
    ### Course 2 Reading
    (etc.)
- Within SECTION F (Diagnostic), use this exact sub-header format:
    ### Diagnostic: prompting
    ### Diagnostic: verification
    ### Diagnostic: data_safety
    ### Diagnostic: tool_fluency
- Within SECTION G (Evaluation), use this exact sub-header format:
    ### Evaluation: Course 1
    ### Evaluation: Course 2
    (etc.)
- Within each section, use the field names from the examples (course_id, domain_id, etc.)
- No JSON — this is a brief, not code
- Do not truncate or abbreviate any section. If a section has 5 courses, produce all 5.

---

QUALITY RULES
- Every scenario must use FICTIONAL client/counterparty names — no real EDC clients, no
  real employees, no real transaction data.
- All tools and systems referenced must be tools this role actually uses (from the role profile).
- Descriptions and level descriptors must be specific to this role's workflows — not
  copy-pasted from the RM examples.
- If the use case mapping flagged a domain gap (Task 4), synthesize a scenario from the
  role profile's Section 13 operational anchors instead. For a tool_fluency gap specifically
  (the domain most likely to have no Section 13B scenario seed), draw from Sections 3–4 of the
  role profile — the tool inventory, M365 Copilot surfaces in active use, and any multi-step
  chain workflows described as pain points. Do NOT skip Course 4 or leave it generic.
- If you are uncertain about a role-specific detail, check your M365 knowledge of this
  role at EDC (SharePoint, emails, meeting transcripts). Do not guess.
- Do not truncate. Every section requires complete output.

NOW DO THE WORK.

---

NOTE FOR FOLLOW-UP REQUESTS:
If you receive a follow-up message asking you to fill in missing or incomplete sections,
output ONLY the requested sections under the heading:

## SUPPLEMENTAL OUTPUT

Use the same section headers and field labels as above (e.g., "### Domain: data_safety",
"### Course 3 — [Title]"). Do not re-output sections that were already complete.
```
