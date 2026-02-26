# Course Design Brief — Relationship Manager (RM) [TEST — Generated from Role Intelligence Profile]
**Role:** Relationship Manager
**Prepared for:** AI Hero Academy content generation pipeline (test run — rmgen prefix)
**Note:** This brief is derived from the RM Role Intelligence Profile to test the pipeline's
         content generation quality. Use role_prefix "rmgen" to avoid collision with existing "rm"
         content. Compare generated output against existing rm_* JSON files to evaluate agent quality.

---

## MACHINE-READABLE HEADER

role_prefix: rmgen

company_map:
  course_1: Northern Fabrication Ltd.
  course_2: Lakeshore Precision Inc.
  course_3: Cedarcrest Export Group
  course_4: Ridgeline Distribution Corp.
  course_5: Mapleton Trade Partners Ltd.

framework_names:
  - CRAF Framework (Context, Role, Action, Format)
  - The 4-Step Recap Verification Protocol
  - The SAFE Abstraction Method (Scope, Abstract, Fit-check, Execute)
  - Copilot Surface Selector
  - The RM AI Workflow (Abstract → Analyze → Draft → Verify)

real_use_case:
  course_1: Client Briefing Note Generation; Discovery Prep; CRM Activity Note Drafting
  course_2: Meeting Recap Verification; AI-Generated Summary Quality Control
  course_3: Non-public Client Data Handling; C3 Record Abstraction Before AI Use
  course_4: Teams-to-Outlook-to-C3 Multi-Step Copilot Workflow
  course_5: AI-Assisted Win-Back Campaign; End-to-End Client Engagement Workflow

---

## SECTION A: Role Overview

**Role display name:** Relationship Manager

The Relationship Manager (RM) is the primary client-facing role in EDC's Commercial Group. RMs manage a portfolio of Canadian exporters — sourcing leads, conducting discovery conversations, presenting EDC financing and risk solutions, logging all activity in C3 (EDC's CRM), and maintaining pipeline hygiene. They are supported by Associate Relationship Managers (ARMs) who handle early-stage prospecting and meeting booking.

The RM role produces three types of daily artifacts that AI can meaningfully accelerate: briefing documents for discovery calls (synthesizing ARM research from C3), meeting recaps and next-step emails (from Teams call transcripts), and CRM activity notes (summarizing interactions for pipeline hygiene).

Primary systems: C3 CRM, M365 (Teams/Outlook/SharePoint), internal knowledge portals.

Key compliance constraint: C3 contains non-public client information — revenue figures, deal terms, NPS scores, and financing details — that cannot be entered into non-approved AI tools. RMs must apply the public/non-public test before using Copilot with any client data.

Performance is measured on lead responsiveness (3-business-day SLA), pipeline forecasting completeness, CRM activity logging discipline, and customer retention (NPS + engagement rates).

---

## SECTION B: AI Skill Domain Profiles

### Domain: prompting

**Description:** Structuring AI prompts with enough context, role definition, and output format to produce briefing notes, discovery emails, and CRM activity summaries that are directly usable — not generic output that needs full rewrites before it can be sent or logged.

- level_0_label: Unaware
- level_0_descriptor: Has not used AI to draft any RM work artifacts. Cannot describe what a structured prompt looks like or how it differs from a casual question.
- level_1_label: Explorer
- level_1_descriptor: Has tried prompting Copilot for a discovery brief or email draft, but the output missed the client context and required substantial rewriting before it was usable.
- level_2_label: Practitioner
- level_2_descriptor: Builds prompts that include client context from C3 notes, a role instruction, and a format specification. Output is usually a usable first draft of a briefing note or follow-up email with only minor edits required.
- level_3_label: Proficient
- level_3_descriptor: Constructs layered prompts for complex RM scenarios — multi-solution presentations, ARM handoff briefs, win-back campaign emails. Adjusts constraints proactively when the first output misses tone or specificity. Iterates within a single session.
- level_4_label: Champion
- level_4_descriptor: Builds and shares reusable prompt templates for the RM team (e.g., a standard discovery brief template, a CRM note format). Runs prompt-sharing sessions at team standups. Contributes new RM use cases to the EDC AI use case library.

### Domain: verification

**Description:** Checking AI-generated meeting recaps, email drafts, and discovery summaries before they are logged in C3 or sent to a client — specifically catching invented commitments, wrong titles, hallucinated figures, and unverified decision attributions that Copilot routinely inserts into RM output.

- level_0_label: Unaware
- level_0_descriptor: Copies Teams Copilot meeting recap output directly into C3 activity notes without reading it. Assumes the AI captured what was said accurately.
- level_1_label: Explorer
- level_1_descriptor: Reads AI-generated recaps before using them but checks only obvious errors. Does not systematically compare figures, titles, or commitments against personal notes or calendar entries.
- level_2_label: Practitioner
- level_2_descriptor: Applies a consistent review process: verifies financial figures against C3 data, checks all decision attributions against notes, removes any "the client agreed to" language that was not explicitly confirmed in the meeting.
- level_3_label: Proficient
- level_3_descriptor: Identifies subtle hallucinations specific to RM recaps — plausible but wrong deal sizes, invented referral commitments, misattributed next steps. Adjusts the Teams Copilot prompt to reduce these error types in future recaps.
- level_4_label: Champion
- level_4_descriptor: Builds team-level verification checklists calibrated to RM recap errors. Can explain to ARMs why Copilot makes specific error types (commitment hallucination, title confusion). Trains new team members on the review process before they log to C3.

### Domain: data_safety

**Description:** Applying the public/non-public test before any client data from C3 enters an AI prompt. Abstracting or generalizing the non-public fields — deal terms, internal credit figures, NPS scores, client-shared financials — so the AI can still help without a policy violation.

- level_0_label: Unaware
- level_0_descriptor: Pastes full C3 client records — including financing amounts, NPS scores, and confidential deal notes — into Copilot Chat or other AI tools without thinking about what is and is not public information.
- level_1_label: Explorer
- level_1_descriptor: Knows the rule ("don't share client data with AI") but struggles to identify the boundary in real RM scenarios. Defaults to avoiding AI use on any client-related task, reducing the tool's practical value.
- level_2_label: Practitioner
- level_2_descriptor: Reliably abstracts standard non-public fields — replaces company name with "a $[range]M Ontario exporter", removes deal amounts, generalizes sector context. Applies the test consistently for routine CRM notes and briefing drafts.
- level_3_label: Proficient
- level_3_descriptor: Handles borderline RM cases confidently — inferred creditworthiness signals, internal NPS scores, management commentary from confidential calls. Rewrites prompts to preserve analytical utility while removing the specific identifying details.
- level_4_label: Champion
- level_4_descriptor: Identifies new compliance edge cases as RM workflows evolve (e.g., using AI to help interpret internal risk ratings). Advises ARMs and colleagues on safe abstraction patterns. Recognised by peers as the team's safe-AI reference point.

### Domain: tool_fluency

**Description:** Knowing which M365 Copilot surface to use first for each RM task — and then chaining outputs across surfaces into multi-step workflows: from the Teams meeting recap, through an Outlook follow-up email, to a polished C3 activity note, without losing continuity or retyping context at each step.

- level_0_label: Unaware
- level_0_descriptor: Has not used any Copilot feature in Teams, Outlook, or other M365 tools for RM work. Unaware that Copilot can summarize meeting transcripts, draft emails, or help write CRM notes.
- level_1_label: Explorer
- level_1_descriptor: Has used one Copilot surface (usually Teams meeting recap) but treats each tool independently. Does not carry output from one step into the next. Re-enters context manually at each stage.
- level_2_label: Practitioner
- level_2_descriptor: Uses at least three M365 Copilot surfaces for RM tasks. Builds a simple two-step workflow — Teams recap fed into an Outlook draft, or a briefing note used to anchor a CRM log entry.
- level_3_label: Proficient
- level_3_descriptor: Designs complete RM workflows across three or more surfaces — Teams → Outlook → C3 — selecting the entry point based on what source data is available. Adapts the workflow when one step produces poor output instead of abandoning the process.
- level_4_label: Champion
- level_4_descriptor: Documents and shares multi-step RM Copilot workflows with the team. Identifies new M365 Copilot surfaces (e.g., Copilot in SharePoint for proposal research) applicable to RM work. Runs workflow demonstrations at team meetings.

---

## SECTION C: Course Structure

### Course 1 — Brief Like a Pro: Discovery Prep with CRAF

- course_id: rmgen_c1_prompting
- primary_domain: prompting
- tagline: Turn ARM handoff notes into a structured discovery brief using the CRAF prompt framework.
- description: RMs spend significant pre-call time synthesizing ARM research from C3 into a discovery brief. This course teaches the CRAF framework — Context, Role, Action, Format — to produce briefing notes, first-contact emails, and talking points that are directly usable, not generic AI filler that requires rewriting before the call.

### Course 2 — Recap Ready: Verifying AI Meeting Summaries

- course_id: rmgen_c2_verification
- primary_domain: verification
- tagline: Catch the errors Teams Copilot inserts into your deal recaps before they reach C3 or a client.
- description: Teams Copilot generates meeting recaps automatically — but RMs who log them directly to C3 without checking are creating a record of what the AI invented, not what was said. This course teaches a four-step verification protocol specific to RM deal conversations: checking figures, attributions, commitments, and next steps before logging or sending.

### Course 3 — Safe Prompts: The C3 Data Line

- course_id: rmgen_c3_data_safety
- primary_domain: data_safety
- tagline: Apply the public/non-public test before any C3 client data enters a Copilot prompt.
- description: C3 holds the non-public information that clients share with EDC in confidence — deal terms, internal credit notes, NPS scores, financing amounts. This course makes the abstraction habit automatic: RMs learn to identify what must stay out of AI tools and how to rewrite prompts that preserve analytical value without the compliance risk.

### Course 4 — Your Deal Day Copilot Workflow

- course_id: rmgen_c4_tool_fluency
- primary_domain: tool_fluency
- tagline: Chain Teams, Outlook, and C3 into a seamless AI-assisted deal day workflow.
- description: M365 Copilot is live in Teams, Outlook, and Word — but the right surface depends on the task. This course teaches RMs which tool to start with and how to carry output across surfaces without losing context: from Teams meeting recap, to Outlook follow-up draft, to C3 activity note — all with Copilot as the connector.

### Course 5 — Full Deal Workflow: Abstract, Analyze, Draft, Verify

- course_id: rmgen_c5_capstone
- primary_domain: prompting
- tagline: Run a complete AI-assisted client engagement from ARM handoff to C3 log — safely and efficiently.
- description: The capstone integrates all four domains in a realistic RM deal scenario. Learners must apply the public/non-public test before prompting, choose the right Copilot surface at each step, use CRAF to draft call prep and follow-up artifacts, and verify AI output before it enters C3 or reaches a client.

---

## SECTION D: Scenario Seeds

### Course 1 Scenario

- scenario_text: Your ARM, Alex, just handed off Northern Fabrication Ltd. — a $38M Ontario precision parts manufacturer currently exploring trade credit insurance for their new Mexico and Colombia contracts. Alex's C3 notes include: revenue range, two key contacts, and a note that the CFO flagged cash flow predictability as the top concern. You have a 30-minute discovery call tomorrow morning and need to prepare a structured briefing note and a first question plan.
- task_1_text: Write a CRAF prompt to generate a discovery briefing note for your call with Northern Fabrication. Include all four CRAF elements and specify that the output should cover company overview, key risks, and three discovery questions to open the conversation.
- task_2_text: Your first output was too generic — the discovery questions could apply to any manufacturing company. Identify which CRAF element caused this and rewrite that element to anchor the questions specifically to Northern Fabrication's Mexico/Colombia expansion and the CFO's cash flow concern.
- task_3_text: After the call you need to log a C3 activity note. Write a CRAF prompt to draft a structured activity note from the following raw call notes: "CFO confirmed Mexico contract closes Q3, worried about peso volatility. Referred us to their trade lawyer re: contract structure. Booked follow-up for May 7." The note must include what was discussed, next steps, and the referral.
- task_4_text: Your activity note draft includes the phrase "the client appears to be a good fit for trade credit insurance." This is an opinion, not a documented fact from the call. Rewrite the prompt to add a constraint that prevents the AI from generating opinion or assessment language not directly supported by the notes you provide.
- coach_system_prompt: You are an AI coaching assistant for AI Hero Academy, helping a Relationship Manager practice writing structured CRAF prompts for client discovery and CRM documentation. Guide the learner through the Northern Fabrication scenario. If the learner pastes what appears to be real client data — actual company names outside the scenario, real EDC client figures, or verbatim C3 records — flag it immediately and instruct them to use only the fictional scenario data provided.

### Course 2 Scenario

- scenario_text: You just finished a 45-minute deal review call with the Lakeshore Precision Inc. team. Teams Copilot generated a recap automatically. Before you log it to C3 as the official activity record, you need to check it carefully — the call involved financial estimates, a referral commitment, and a conditional next step that depended on a client decision.
- task_1_text: The Teams recap says "the RM committed to sending a term sheet by end of week." Your notes say you agreed to send a product overview deck — not a term sheet. Identify this as an invented commitment and describe the exact edit you would make to the C3 activity note before logging.
- task_2_text: The recap attributes "the client's revenue is approximately $28M" to a statement from the client. Your notes show the CFO said "$25M to $30M range, not confirmed." Describe the verification step you would take and how you would log this range ambiguity correctly in C3.
- task_3_text: You find three discrepancies in the recap: wrong meeting date (shows April 3, should be April 5), wrong title for the client contact (shows "VP Operations", your notes say "Director of Finance"), and a hallucinated next step ("client to send RFP by April 15") that was never discussed. Document each discrepancy and your resolution for each before logging to C3.
- task_4_text: Write a Teams Copilot prompt that would produce a deal recap formatted specifically for C3 logging — with sections for "Discussion Points", "Commitments Made (Confirmed)", and "Next Steps (Owner and Date)" — and that explicitly instructs the AI to flag any figure or attribution it is not certain about with [UNCONFIRMED] tags.
- coach_system_prompt: You are an AI coaching assistant for AI Hero Academy, helping a Relationship Manager practice verification discipline for AI-generated meeting recaps. Guide the learner through the Lakeshore Precision scenario. If the learner pastes what appears to be real client data — actual EDC client names, real deal figures, or verbatim C3 records — flag it immediately and instruct them to use only the fictional scenario data provided.

### Course 3 Scenario

- scenario_text: You are preparing a briefing note for a credit committee presentation on Cedarcrest Export Group, a mid-market Quebec-based agri-food exporter. You want to use Copilot to draft the executive summary section. You have the C3 account record open, which includes: the client's EDC facility amount ($4.2M), their internal risk rating, NPS score from last year's survey, and two confidential notes from a previous RM about management credibility concerns.
- task_1_text: Before you use any of the C3 data in a Copilot prompt, apply the public/non-public test. List which fields from the C3 record are non-public and must be abstracted before prompting. For each non-public field, write the abstracted version you would use in the prompt.
- task_2_text: Write a Copilot prompt to draft the executive summary using only the abstracted or public versions of the C3 data. The summary should cover company profile, export markets, and the business rationale for the facility request — without any of the non-public details you identified in Task 1.
- task_3_text: A colleague suggests just entering all the C3 data into Copilot and then removing the non-public details from the output at the end. Explain why this approach violates EDC's GenAI policy, even if the final document doesn't contain the non-public information.
- task_4_text: The credit committee summary will reference "management credibility concerns documented in the previous RM's notes." Write an abstracted version of this reference that would be safe to include in a Copilot prompt — capturing the type of risk without including the specific confidential commentary.
- coach_system_prompt: You are an AI coaching assistant for AI Hero Academy, helping a Relationship Manager practice safe AI prompting with non-public client data. Guide the learner through the Cedarcrest Export Group scenario. If the learner pastes what appears to be real client data — actual EDC client names, real facility amounts, real internal ratings, or verbatim C3 records — flag it immediately and instruct them to use only the fictional scenario data provided.

### Course 4 Scenario

- scenario_text: You just finished a 30-minute intro call with Ridgeline Distribution Corp., a Vancouver-based logistics company exploring EDC trade credit insurance. Teams Copilot generated a recap. You need to send a follow-up email to the CFO before end of day, then log the call in C3 as an activity note. You want to chain Teams, Outlook, and your own notes into a seamless Copilot-assisted workflow without re-entering the same context three times.
- task_1_text: Start with Teams Copilot. Write a prompt to generate a structured call recap that separates "What was discussed", "What was agreed", and "Client's next decision". Explain why Teams is the right starting surface for this workflow step rather than going straight to Outlook or C3.
- task_2_text: Take the Teams recap output and use it as input for Outlook Copilot. Write a prompt to draft a follow-up email to the CFO that references two specific items from the recap — the client's stated interest and the agreed next step — and proposes a 20-minute call next week to present the trade credit insurance product overview.
- task_3_text: Now use your notes and the Teams recap together to write a C3 activity note via Copilot. Your prompt must include a format constraint: the note must have three labelled sections (Call Summary, Commitments, Next Steps with Date) and must not exceed 150 words total.
- task_4_text: Midway through the workflow the Teams recap produced a next step ("RM to send product brochure by Friday") that you did not actually commit to. Describe how you handle this error in the workflow — which step do you correct it, and how does the correction propagate into the Outlook email and C3 note without restarting the whole chain?
- coach_system_prompt: You are an AI coaching assistant for AI Hero Academy, helping a Relationship Manager practice multi-step M365 Copilot workflows for deal documentation. Guide the learner through the Ridgeline Distribution scenario. If the learner pastes what appears to be real client data — actual EDC client names, real deal figures, or verbatim C3 records — flag it immediately and instruct them to use only the fictional scenario data provided.

### Course 5 Scenario

- scenario_text: Your manager has asked you to run a win-back campaign for lapsed RM clients — accounts that had an active EDC relationship 18-24 months ago but have had no logged activity since. You have a C3 export of 12 lapsed accounts with: company name, last facility type, expiry date, last contact RM, and estimated revenue. Some records also contain internal notes from the previous RM. You want to use Copilot to help you prioritize, draft outreach, and log activity — but you need to do it safely and in the right sequence.
- task_1_text: Before using any of the C3 export data in a Copilot prompt, apply the public/non-public test to the fields in the export. Identify which fields you can use directly, which must be abstracted, and which should be excluded entirely from AI prompts. Write the abstraction rules you would apply to the lapsed account data.
- task_2_text: Using only the safe/abstracted data, write a CRAF prompt to help you prioritize the 12 accounts — ranking them by re-engagement potential based on facility type, revenue range, and time since last contact. Include format instructions to produce a ranked table with a one-sentence rationale per account.
- task_3_text: Choose the highest-priority account from your prioritization output (use Mapleton Trade Partners Ltd. as a stand-in). Write a CRAF prompt to draft a re-engagement email for the CFO — personal but professional, referencing the previous EDC relationship without disclosing specific non-public deal details.
- task_4_text: After your outreach call with Mapleton Trade Partners, use the Teams recap, your email thread, and your call notes to generate a complete C3 activity record. Write the multi-step Copilot workflow (which surfaces, in what order, with what prompts) you would use to produce an activity note that captures the win-back context, the current needs discussion, and the agreed next steps.
- coach_system_prompt: You are an AI coaching assistant for AI Hero Academy, helping a Relationship Manager practice a complete AI-assisted win-back workflow that integrates safe prompting, data abstraction, and multi-surface Copilot use. Guide the learner through the Mapleton Trade Partners win-back scenario. If the learner pastes what appears to be real client data — actual EDC client names, real deal figures, or verbatim C3 records — flag it immediately and instruct them to use only the fictional scenario data provided.

---

## SECTION E: Reading Content Seeds

### Course 1 Reading

- framework_name: CRAF Framework (Context, Role, Action, Format)
- concept_text: The CRAF Framework gives RMs four mandatory components for any Copilot prompt used in client work. Context sets up who the client is and what situation they are in. Role defines how Copilot should speak (e.g., "a senior RM drafting an internal briefing note"). Action specifies exactly what to produce. Format specifies the output structure (sections, length, tone). Missing any one element typically produces generic output that requires a full rewrite.
- good_example: Before CRAF — "Write a discovery brief for my new client." After CRAF — "Context: $38M Ontario precision parts manufacturer, exploring trade credit insurance for new contracts in Mexico and Colombia, CFO focused on cash flow predictability. Role: You are a senior RM at a Canadian export finance institution drafting a pre-call briefing note. Action: Produce a 3-section discovery brief covering company overview, key risks, and 3 discovery questions anchored to the Mexico/Colombia expansion. Format: Use labeled headers for each section. Max 250 words."
- anti_pattern: The most common CRAF failure is omitting Role — without it, Copilot writes in a generic advisory voice instead of the RM's internal documentation style, producing output that sounds like a marketing brochure rather than a briefing note.
- takeaway: Every client-facing or CRM artifact drafted with Copilot needs all four CRAF elements. Skipping one costs more time in rewrites than adding it upfront.

### Course 2 Reading

- framework_name: The 4-Step Recap Verification Protocol (Figure, Attribution, Commitment, Next Step)
- concept_text: Copilot meeting recaps in Teams fail in four predictable ways for RMs: wrong figures (hallucinated deal sizes or revenue numbers), misattributed statements (words put in the wrong person's mouth), invented commitments (RM or client "agreed to" something that was never said), and wrong next steps (actions assigned to the wrong person or with the wrong deadline). The 4-Step Recap Verification Protocol addresses each failure type in order.
- good_example: Step 1 (Figures): Cross-reference every number in the recap against your notes — revenue range, deal size, SLA. Step 2 (Attribution): Verify every "X said" or "X agreed" against your notes. Step 3 (Commitments): Flag any "will do by [date]" language and confirm it matches your notes before logging to C3. Step 4 (Next Steps): Verify owner and date for every next step against your calendar invite or notes.
- anti_pattern: The most common error is correcting figures while leaving unverified commitment language in place. "The client indicated interest in exploring a $3M facility" may be correct in dollar amount but wrong in the level of commitment — "indicated interest in exploring" is very different from "requested a term sheet."
- takeaway: The 4-Step protocol takes three minutes per recap. A wrong commitment logged to C3 can take days to correct and damage client trust.

### Course 3 Reading

- framework_name: The SAFE Abstraction Method (Scope, Abstract, Fit-check, Execute)
- concept_text: The SAFE Abstraction Method gives RMs a repeatable four-step process for using Copilot safely with client data. Scope — identify every field in your data source that might be non-public (facility amount, internal ratings, deal terms, NPS, confidential notes). Abstract — replace non-public fields with generalized equivalents. Fit-check — read the abstracted prompt aloud: does it still give Copilot enough context to be useful? Execute — run the prompt and verify the output doesn't inadvertently reconstruct the non-public details.
- good_example: Before SAFE: "Cedarcrest Export Group, $4.2M facility, risk rating B2, NPS 42, previous RM note: management credibility concern flagged." After SAFE: "A mid-market Quebec agri-food exporter, facility in the $3M–$5M range, historical relationship with active engagement, credit profile under review."
- anti_pattern: The most common error is the "clean it up later" approach — inputting all non-public data and planning to remove it from the output. The policy violation occurs at input, not output. The data has already been shared with the AI tool at that point.
- takeaway: Apply SAFE before the prompt, not after. The abstraction takes 60 seconds. A policy violation takes weeks to resolve.

### Course 4 Reading

- framework_name: Copilot Surface Selector
- concept_text: Each M365 Copilot surface is optimized for a specific input type and output format. Teams Copilot works best when the source is a meeting transcript — it can extract summaries, decisions, and action items from audio/text. Outlook Copilot works best when the source is an email thread or a brief you write — it drafts replies and new messages in your tone. Word/SharePoint Copilot works best for structured documents. The Surface Selector principle: choose the surface based on where your source data lives, not where you want the output to end up.
- good_example: Deal call just happened → start in Teams (source is audio). Need to send follow-up email → bring Teams output into Outlook, add client context. Need to log C3 note → use the Outlook draft and Teams recap together in Word or directly in C3 with a Copilot prompt. Each step feeds the next.
- anti_pattern: The most common error is starting in Outlook Copilot when the source is a meeting transcript. Outlook has no access to the Teams recording — the RM ends up retyping context from memory, which defeats the purpose of the workflow and increases hallucination risk.
- takeaway: Match the surface to the source. Teams for meetings, Outlook for email chains, Word for documents. Then chain the outputs.

### Course 5 Reading

- framework_name: The RM AI Workflow (Abstract → Analyze → Draft → Verify)
- concept_text: The RM AI Workflow sequences four steps that must happen in order for Copilot to be both safe and useful in a client engagement. Abstract — remove non-public data before any AI prompt (apply the SAFE method). Analyze — use Copilot to synthesize public/abstracted context into insights (prioritization, pattern recognition, gap identification). Draft — use CRAF-structured prompts to produce client-facing or CRM artifacts. Verify — apply the 4-Step Recap Protocol before logging or sending anything.
- good_example: Win-back workflow — Abstract: strip facility amounts and ratings from C3 export, replace with ranges. Analyze: prompt Copilot to rank accounts by re-engagement potential. Draft: CRAF prompt for re-engagement email per priority account. Verify: check all commitment language before sending — ensure the email doesn't imply EDC is offering a specific product or rate.
- anti_pattern: The most common workflow error is reversing the order — drafting first, then trying to verify and abstract retroactively. When the draft is already written with non-public data, the RM faces two bad choices: rewrite entirely or log a non-compliant record.
- takeaway: The sequence matters as much as the tools. Abstract before you analyze. Analyze before you draft. Verify before you send or log.

---

## SECTION F: Diagnostic Item Seeds

### Diagnostic: prompting
- Item 1 (MCQ): Which CRAF component is most commonly missing when a briefing note prompt produces output that is too generic to use for a specific client discovery call?
  - A: Context (the client situation)
  - B: Role (the AI persona)
  - C: Action (the specific task)
  - D: Format (the output structure)
  - Correct: B
- Item 2 (prompt_sandbox): Your ARM just handed off Ridgeline Distribution Corp. — a $22M Vancouver logistics company interested in trade credit insurance for new contracts in the Philippines. Write a complete CRAF prompt to produce a discovery briefing note with three client-specific discovery questions.
- Item 3 (micro_task): Review this prompt and identify all CRAF elements that are present or missing: "Write a follow-up email for my client meeting that covers what we discussed." For each missing element, write what it should say for an RM working on a financing inquiry with a mid-market exporter.

### Diagnostic: verification
- Item 1 (MCQ): Your Teams Copilot recap says "the client confirmed they want to proceed with a $2.5M trade credit insurance facility." Your notes say the client asked for pricing information on facilities in the $2M-$3M range. What is the correct next step before logging to C3?
  - A: Log the recap as written — the AI captured the spirit of the conversation
  - B: Change the figure to match your notes and log immediately
  - C: Flag the discrepancy, verify the exact statement with your notes, and log the verified version
  - D: Ask the client to confirm the figure via email before logging anything
  - Correct: C
- Item 2 (prompt_sandbox): Write a Teams Copilot prompt that produces a deal recap formatted for C3 logging, with separate sections for "Discussion Points", "Confirmed Commitments", and "Next Steps (Owner and Date)". Include an instruction that flags any figure or attributed statement the AI is not certain about.
- Item 3 (micro_task): (Seeds only — full item to be generated by Assessment Designer)

### Diagnostic: data_safety
- Item 1 (MCQ): You want to use Copilot to help write an executive summary for a credit committee deck. Your source is a C3 account record that includes: company name, revenue range (public estimate), EDC facility amount ($3.8M), internal risk rating, and last year's NPS score. Which fields must be abstracted before use?
  - A: Company name and revenue range only
  - B: EDC facility amount, internal risk rating, and NPS score
  - C: All fields — no C3 data should ever enter an AI prompt
  - D: Only fields that the client has not shared publicly
  - Correct: B
- Item 2 (prompt_sandbox): Write an abstracted version of the following C3 data that would be safe to include in a Copilot prompt: "Cedarcrest Export Group, $4.2M facility, risk rating B2, NPS 42, note: management credibility concern from previous RM."
- Item 3 (micro_task): (Seeds only — full item to be generated by Assessment Designer)

### Diagnostic: tool_fluency
- Item 1 (MCQ): You just finished a Teams call with a prospect. You need to send a follow-up email and log a C3 activity note. Which Copilot surface should you start with?
  - A: Outlook Copilot — draft the email first while the conversation is fresh
  - B: Teams Copilot — generate a meeting recap from the transcript first, then use it as input for the email and note
  - C: Word Copilot — write a structured document first, then adapt it for both email and C3
  - D: C3 directly — log the note first to capture the facts, then draft the email
  - Correct: B
- Item 2 (prompt_sandbox): (Seeds only — full item to be generated by Assessment Designer)
- Item 3 (micro_task): (Seeds only — full item to be generated by Assessment Designer)

---

## SECTION G: Evaluation Item Seeds

### Evaluation: Course 1
- 3 MCQ items testing CRAF framework application in RM client documentation (briefing notes, CRM activity entries, discovery emails)
- 1 performance task: Learner receives an ARM handoff note with client context and must write a complete CRAF prompt to draft a discovery briefing note, then identify and fix one specific CRAF weakness in a provided prompt example

### Evaluation: Course 2
- 3 MCQ items testing the 4-Step Recap Verification Protocol applied to a Teams recap with embedded errors
- 1 performance task: Learner receives a simulated Teams Copilot recap with three deliberate errors (invented commitment, wrong title, hallucinated figure) and must apply the full verification protocol, documenting each finding and correction

### Evaluation: Course 3
- 3 MCQ items testing the SAFE abstraction method in RM data safety scenarios (C3 records, NPS data, deal terms)
- 1 performance task: Learner receives a C3 account record and must apply the SAFE method in full — scope non-public fields, write abstracted versions, and draft a safe Copilot prompt using only the abstracted data

### Evaluation: Course 4
- 3 MCQ items testing Copilot surface selection and sequencing for RM multi-step workflows
- 1 performance task: Learner receives a post-call scenario and must design the full Teams → Outlook → C3 workflow — specifying which surface, which prompt (full CRAF), and what input from the previous step feeds into each stage

### Evaluation: Course 5
- 3 MCQ items integrating all four domain skills in capstone win-back scenarios
- 1 performance task: Learner receives a lapsed account C3 export and must complete the full RM AI Workflow — Abstract (identify non-public fields), Analyze (CRAF prioritization prompt), Draft (CRAF re-engagement email), Verify (apply 4-Step protocol to the email before sending)
