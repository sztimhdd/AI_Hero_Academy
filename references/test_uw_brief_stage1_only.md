# Course Design Brief — Underwriter (UW) [TEST — Stage 1+3 only]
**Role:** Underwriter
**Prepared for:** AI Hero Academy content generation pipeline
**Note:** This is a minimal test brief to verify Stage 1 parser and Stage 3 QA gap check.
         Some sections are deliberately incomplete to exercise the gap-check/follow-up flow.

---

## MACHINE-READABLE HEADER

role_prefix: uw

company_map:
  course_1: Meridian Exports Inc.
  course_2: Brockton Manufacturing Ltd.
  # courses 3-5 intentionally omitted to exercise QA gap check

framework_names:
  - CRAF Framework (Context, Role, Action, Format)
  - VERIFY Checklist
  - The SAFE Abstraction Method
  - Copilot Surface Selector
  - End-to-End AI Workflow

real_use_case:
  course_1: Access to Copilot 365 for Underwriting Research; Prospect Intelligence
  course_2: Customer Interaction Recap; Meeting Recap in MS-Teams; Record Governance
  course_3: Non-public client data into MS Copilot (FinDev Canada use case)
  course_4: Business Enablement — Frontline Copilot Use Case Generation
  course_5: Automating Prospect Profiling; Sector Opportunity Identification

---

## SECTION A: Role Overview

**Role display name:** Underwriter

The Underwriter (UW) reviews credit applications from Canadian exporters, assesses financial risk, and structures EDC financing solutions. The role involves synthesizing complex financial information (financial statements, credit bureau reports, management bios, market intelligence) into risk assessments and deal memos used by Credit Committees.

Primary tools: C3 CRM, M365 (Teams/Outlook/Word/Excel), internal risk platforms, external financial databases.

---

## SECTION B: AI Skill Domain Profiles

### Domain: prompting

**Description:** Structuring AI prompts with context, constraints, format, and audience to produce outputs directly usable in UW workflows — credit memos, risk summaries, deal structures, and committee briefings.

- level_0_label: Unaware
- level_0_descriptor: Has not used AI prompting in work tasks. Cannot describe what makes a prompt effective.
- level_1_label: Explorer
- level_1_descriptor: Writes basic prompts ("summarize this financial statement"). Output is often too generic and requires full rewrite.
- level_2_label: Practitioner
- level_2_descriptor: Uses structured prompts with context and format instructions. Output is usually usable for first-draft credit memo sections with minor edits.
- level_3_label: Proficient
- level_3_descriptor: Adapts prompts for complex scenarios (e.g., sector-specific risk language). Adds constraints proactively. Iterates when output misses the mark.
- level_4_label: Champion
- level_4_descriptor: Designs reusable prompt templates for UW team workflows. Coaches colleagues on prompting structure. Contributes new use cases to the EDC AI use case library.

### Domain: verification

**Description:** Reviewing AI outputs critically before using them in credit assessments — catching hallucinated financial figures, invented analyst citations, and incorrect covenant interpretations in deal memos and risk summaries.

- level_0_label: Unaware
- level_0_descriptor: Treats AI outputs as accurate by default. Does not cross-reference financial figures against source documents.
- level_1_label: Explorer
- level_1_descriptor: Reads AI output before using it, but does not systematically verify figures against the original financial statements or credit bureau reports.
- level_2_label: Practitioner
- level_2_descriptor: Routinely cross-references AI output against source documents. Removes or corrects unverifiable statements before including in credit memos.
- level_3_label: Proficient
- level_3_descriptor: Identifies subtle hallucinations (plausible but wrong financial ratios, invented citations). Adjusts prompts to reduce hallucination risk. Reviews with a skeptical lens.
- level_4_label: Champion
- level_4_descriptor: Develops verification checklists for credit memo review. Can explain failure modes of AI financial summarization. Trains peers on review discipline.

### Domain: data_safety

**Description:** Applying the public/non-public test before inputting client financial data into AI tools. Abstracting non-public information (credit figures, deal terms, covenant details, internal risk ratings) while still obtaining useful AI assistance.

- level_0_label: Unaware
- level_0_descriptor: Unaware of the non-public data rule or does not apply it in practice. May paste full credit application data directly into AI tools.
- level_1_label: Explorer
- level_1_descriptor: Knows the rule ("don't share non-public info") but cannot reliably distinguish public from non-public in complex financial scenarios.
- level_2_label: Practitioner
- level_2_descriptor: Applies the public/non-public test consistently for standard cases. Abstracts borrower names, specific credit figures, and deal terms before prompting.
- level_3_label: Proficient
- level_3_descriptor: Handles borderline cases confidently (e.g., inferred financials, management commentary, internal risk ratings). Rewrites prompts to preserve utility while removing risk.
- level_4_label: Champion
- level_4_descriptor: Identifies novel compliance risks in new deal types. Advises team on safe data abstraction patterns. Acts as a data-safe AI usage model for the UW team.

### Domain: tool_fluency

**Description:** Choosing the right M365 Copilot surface (Outlook, Teams, Excel, Word) for each underwriting task and building multi-step workflows where output from one tool feeds the next — from Teams meeting recap to deal memo to committee slide.

- level_0_label: Unaware
- level_0_descriptor: Has not used Copilot features in M365 tools for underwriting work. Unaware of which tools have AI capabilities.
- level_1_label: Explorer
- level_1_descriptor: Has tried one or two Copilot features (e.g., Teams meeting recap). Does not connect tools into workflows.
- level_2_label: Practitioner
- level_2_descriptor: Uses at least three M365 Copilot surfaces regularly. Builds simple two-step workflows (e.g., Teams recap → Word deal memo draft).
- level_3_label: Proficient
- level_3_descriptor: Designs multi-step workflows across 3+ Copilot surfaces. Chooses the right entry point based on input type. Recovers gracefully when one step produces poor output.
- level_4_label: Champion
- level_4_descriptor: Documents and shares UW workflows with the team. Identifies new Copilot surfaces or features applicable to underwriting work. Trains peers on multi-step patterns.

---

## SECTION C: Course Structure

### Course 1 — Brief Like a Pro: From Application to Credit Memo Draft

- course_id: uw_c1_prompting
- primary_domain: prompting
- tagline: Turn a new credit application into a structured first-draft credit memo using the CRAF prompt framework.
- description: Underwriters spend significant time drafting credit memo sections from raw application data. This course teaches the CRAF framework (Context, Role, Action, Format) to produce risk summaries, sector analyses, and deal structure recommendations that are directly usable — not generic AI output that needs full rewrites.

### Course 2 — Recap, Review, Then Write: Credit Committee Prep Discipline

- course_id: uw_c2_verification
- primary_domain: verification
- tagline: Catch errors AI inserts into your deal summaries before they reach the Credit Committee.
- description: AI tools generate meeting recaps and document summaries automatically — but they hallucinate financial figures, invent citations, and misstate covenant terms. This course teaches a verification discipline specific to credit underwriting: what to check, how to check it, and how to produce a committee-ready summary.

### Course 3 — The Credit File Line: What Goes Into AI and What Doesn't

- course_id: uw_c3_data_safety
- primary_domain: data_safety
- tagline: Apply the public/non-public test before any credit file data touches an AI prompt.
- description: EDC's GenAI policy requires that non-public financial information never be input into unapproved AI tools. For UWs, this means credit application data must be abstracted before use. This course makes the abstraction process automatic and reliable.

### Course 4 — Your Deal Day Copilot Workflow

- course_id: uw_c4_tool_fluency
- primary_domain: tool_fluency
- tagline: Match the right M365 Copilot surface to each underwriting task and chain them into a deal workflow.
- description: M365 Copilot is available across Teams, Outlook, Excel, and Word — but the right surface for each task in the UW workflow is not obvious. This course teaches underwriters which tool to reach for first and how to chain outputs across surfaces into a complete deal-day workflow.

### Course 5 — Full Deal AI Workflow: From Application to Committee

- course_id: uw_c5_capstone
- primary_domain: prompting
- tagline: Run an end-to-end AI-assisted deal workflow: abstract, analyze, draft, verify.
- description: The capstone integrates all four UW AI skill domains in a realistic credit assessment scenario. Learners must abstract financial data before analysis, choose the right Copilot surfaces, write CRAF prompts for memo sections, and verify AI output before it reaches the Credit Committee.

---

## SECTION D: Scenario Seeds

### Course 1 Scenario

- scenario_text: You have just received a credit application for Meridian Exports Inc., a mid-market Canadian exporter seeking a $5M financing facility to support entry into Southeast Asian markets. Your ARM has uploaded the financial statements and company background to C3. You need to draft the "Company Overview" and "Risk Factors" sections of the credit memo before tomorrow's team review call.
- task_1_text: The ARM's C3 notes say: "Meridian — $42M revenue, 3yr avg EBITDA margin 11%, expanding into Vietnam and Thailand, management team stable, main risk is FX exposure." Write a CRAF prompt that would get Copilot to draft a structured "Company Overview" paragraph for the credit memo. Include Context, Role, Action, and Format instructions.
- task_2_text: Your first Copilot output is too generic — it describes a "growing Canadian company" without the specific financial context you provided. Identify what CRAF element is missing and rewrite the prompt to fix it.
- task_3_text: Now write a second CRAF prompt to draft the "Key Risk Factors" section. The section must include: FX exposure, concentration risk (two customers = 60% of revenue), and management succession risk. Include a format constraint specifying bullet format with severity ratings.
- task_4_text: The risk section draft looks good but uses the phrase "the company's financial position appears solid." This is unverified opinion language. Rewrite the prompt to add an output constraint that prevents unverified opinion statements and limits Copilot to fact-based observations from the inputs you provide.
- coach_system_prompt: You are an AI coaching assistant for AI Hero Academy, helping an Underwriter practice writing structured CRAF prompts for credit memo drafting. Guide the learner through prompt construction for the Meridian Exports scenario. If the learner appears to input what looks like real client data — real company names, real financial figures, or verbatim confidential records — flag it immediately and instruct them to use only the fictional scenario data provided.

### Course 2 Scenario

- scenario_text: You just finished a 45-minute deal review call with the Brockton Manufacturing deal team. Teams Copilot generated an automatic recap. Before you use it to draft the "Meeting Summary and Next Steps" section of the deal memo, you need to verify it carefully — the recap contains several financial figures, commitment attributions, and timeline references.
- task_1_text: The Teams Copilot recap says "The team agreed to a 5-year term at 3.2% fixed rate." Your notes say the team discussed 3.2% but did NOT finalize the term length. Identify this as an invented commitment and describe the correct process for handling it before logging to C3.
- task_2_text: The recap attributes the comment "EBITDA coverage looks thin at current projections" to the Credit Director. You have no memory of this being said. Describe the verification step you would take and what you would do if you cannot confirm the attribution.
- task_3_text: You find three figures in the recap that differ from your notes by more than 10%: $4.2M vs $4.5M for the financing amount, Q3 vs Q4 for expected close, and "two analysts reviewed" vs "one analyst reviewed." Using a structured checklist approach, document each discrepancy and your resolution for each.
- task_4_text: Write a prompt that would instruct Teams Copilot to produce a deal recap formatted specifically for credit memo input — with separate sections for "Decisions Made," "Open Items," and "Next Steps with Owner and Date" — and that explicitly avoids attribution of statements to specific individuals unless directly quoted.
- coach_system_prompt: You are an AI coaching assistant for AI Hero Academy, helping an Underwriter practice verification discipline for AI-generated meeting recaps and deal summaries. Guide the learner through the Brockton Manufacturing verification scenario. If the learner appears to input what looks like real client data — real company names, real financial figures, or verbatim confidential records — flag it immediately and instruct them to use only the fictional scenario data provided.

---

## SECTION E: Reading Content Seeds

### Course 1 Reading

- framework_name: CRAF Framework (Context, Role, Action, Format)
- concept_text: The CRAF Framework structures prompts into four mandatory components that together produce outputs directly usable in underwriting work. Context sets the deal situation. Role specifies the AI persona (e.g., "senior credit analyst reviewing a mid-market application"). Action defines the precise task. Format specifies the output structure expected in a credit memo.
- good_example: Before CRAF — "Summarize the financial risks for this company." After CRAF — "You are a senior credit analyst reviewing a mid-market manufacturing export company. Using only the financial data below: [abstracted data], draft the Risk Factors section of a credit memo. Include: FX exposure, customer concentration, and covenant headroom. Format as three numbered bullets, each under 60 words, fact-based only."
- anti_pattern: Inputting the prompt without the Role instruction causes the AI to write in a generic blog-style voice rather than credit-memo language, requiring a full rewrite. The most common failure is omitting the Format instruction, which causes the AI to produce flowing paragraphs instead of the structured bullet sections expected in EDC credit memos.
- takeaway: Every credit memo prompt must specify all four CRAF components — skip one and the output format or voice will miss the mark for committee use.

### Course 2 Reading

- framework_name: VERIFY Checklist (Verify figures, Evidence for attributions, Review commitments, Identify opinion language, Flag timelines, Yield a corrected version)
- concept_text: The VERIFY Checklist provides a structured six-step discipline for reviewing AI-generated meeting recaps and document summaries before they enter credit files or committee packages. Each step targets a specific failure mode of AI summarization in a financial context.
- good_example: V — Verify all financial figures against source documents (note discrepancies). E — Check every statement attribution ("X said...") against your own meeting notes. R — Flag any "the team agreed" or "it was decided" statements and verify against your notes. I — Remove or bracket any opinion language ("appears solid," "likely to succeed"). F — Verify all dates and deadlines against calendar invites or email confirmations. Y — Produce a corrected draft with tracked changes before logging to C3.
- anti_pattern: Treating the recap as the source of truth and logging it directly to C3 without verification. The most common error is correcting only financial figures while leaving opinion language and unverified commitments in place — these are equally dangerous in credit documentation.
- takeaway: The VERIFY Checklist takes five minutes but prevents committee-level errors that take days to correct in the credit file.

---

## SECTION F: Diagnostic Item Seeds

### Diagnostic: prompting
- Item 1 (MCQ): Which CRAF component is most commonly missing when a credit memo prompt produces output that is too generic and reads like a blog post rather than a financial document?
  - A: Context (the deal situation)
  - B: Role (the AI persona)
  - C: Action (the specific task)
  - D: Format (the output structure)
  - Correct: B
- Item 2 (prompt_sandbox): You need Copilot to draft the "Industry and Sector Risk" section of a credit memo for a Canadian food processor expanding into emerging markets. Write a CRAF prompt that would produce a usable first draft. The section should be 3 bullets, each under 50 words, and must reference commodity price volatility, currency risk, and regulatory market access.
- Item 3 (micro_task): Review this prompt and identify all CRAF elements that are missing or weak: "Write a risk summary for a company with $30M in revenue that exports to the US and Mexico." For each missing element, provide a corrected version of that element.

### Diagnostic: verification
- Item 1 (MCQ): An AI-generated meeting recap says "The Credit Director confirmed the $8.5M limit." Your notes say the Credit Director mentioned $8.5M as a starting point for discussion, not a confirmed limit. What is the correct next step?
  - A: Use the AI figure since it came from the Credit Director
  - B: Change the figure to match your notes and log it as a correction
  - C: Leave the discrepancy in the file and note it as "to be confirmed"
  - D: Flag the discrepancy, verify with the Credit Director, and update only after confirmation
  - Correct: D
- Item 2 (prompt_sandbox): Write a prompt that instructs Teams Copilot to generate a deal recap for a credit committee package. The prompt must specify: no attribution of statements to named individuals, separate sections for "Decisions Made" and "Open Items," and explicit instruction to flag uncertain figures with [UNVERIFIED] tags.
- Item 3 (micro_task): (Seeds only — full item to be generated by Assessment Designer)

---

## SECTION G: Evaluation Item Seeds

### Evaluation: Course 1
- 3 MCQ items testing CRAF framework application in credit memo context
- 1 performance task: Learner receives a raw ARM briefing note and must write a complete CRAF prompt to draft a "Company Overview" and "Risk Factors" section

### Evaluation: Course 2
- 3 MCQ items testing VERIFY checklist application
- 1 performance task: Learner receives an AI-generated deal recap with embedded errors and must apply the full VERIFY checklist, documenting each step
