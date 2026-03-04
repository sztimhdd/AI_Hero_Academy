## MACHINE-READABLE HEADER

```text
## MACHINE-READABLE HEADER

role_prefix: rm

company_map:
 course_1: Harbourline Fabrication Ltd.
 course_2: Prairie Pulse Foods Inc.
 course_3: SkyNorth Aero Components Inc.
 course_4: GlacierTech Robotics Ltd.
 course_5: Maple Ridge Exporters Co.
 course_6: Bluewave Marine Logistics Inc.
 course_7: Evergreen Advanced Materials Group

framework_names:
 NOTE: These names are standardized across all roles where possible. Confirm which apply;
 adapt the role-specific examples in SECTION E (concept_text, good_example, anti_pattern)
 accordingly. Do NOT invent new framework names unless a standardized name genuinely does
 not fit.

 - Course 1 — Responsible AI domain: The SAFE Abstraction Method
 - Course 2 — Strategic Prompting domain: CRAF Framework
 - Course 3 — Critical Evaluation domain: VERIFY Checklist
 - Course 4 — Relationship Intelligence domain: RELATE Framework
 - Course 5 — Data-Driven Decision Making domain: SIGNAL Framework
 - Course 6 — Augmented Communication domain: Copilot Surface Selector
 - Course 7 — Capstone: End-to-End AI Workflow

real_use_case:
 course_1: The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada).
 course_2: Prospect Intelligence
 course_3: Financial Variance Analyzer
 course_4: Customer Interaction Recap
 course_5: Market Insights Generator
 course_6: Record governance - Summarizing Meeting notes and actions (with attendees tagged)
 course_7: Access to Copilot 365 for Business Development; Customer Interaction Recap; Record governance - Summarizing Meeting notes and actions (with attendees tagged)
```

***

# SECTION A — Role Entry

role\_id: rm
title: Relationship Manager
description: "Manages a portfolio of Canadian exporter clients and prospects, building relationships, qualifying needs, and positioning EDC solutions (financing, insurance, guarantees). Coordinates internally with underwriters, product specialists, ARMs, Sales Ops, and risk/compliance partners to structure deals, keep pipeline data current, and resolve client issues while meeting governance and privacy obligations."

***

# SECTION B — All 6 Domain Specs

### Domain: responsible\_ai

domain\_id: responsible\_ai
title: Responsible AI
description: "Applying EDC’s safe AI-use boundaries before using AI in Relationship Manager workflows—especially when handling non-public client information (financial statements, KYC details, internal risk notes, deal terms). Focus is on sanitizing and abstracting inputs, keeping sensitive content inside approved environments, and avoiding accidental disclosure through AI-generated drafts in Outlook/Teams/Word."
level\_0\_label: Unaware
level\_0\_descriptor: "Copies client names, financial figures, or CRM notes directly into non-approved AI tools. Treats AI as a shortcut for analysis without considering confidentiality risks."
level\_1\_label: Explorer
level\_1\_descriptor: "Knows the rule ‘don’t share non-public info’ but struggles in real situations (e.g., what counts as non-public in a term sheet draft, internal risk rating references, or KYC details). Sanitization is inconsistent."
level\_2\_label: Practitioner
level\_2\_descriptor: "Consistently applies a public/non-public check before prompting. Rewrites prompts to remove client identifiers and sensitive numbers while keeping enough context to get useful help (e.g., ‘mid-market manufacturer exporting to US/EU’ instead of full CRM record)."
level\_3\_label: Proficient
level\_3\_descriptor: "Handles borderline cases confidently (e.g., internal pipeline notes, inferred financial stress, internal exposure/risk details). Uses SAFE-style abstraction so outputs remain useful for meeting prep, credit memo drafting, and follow-ups without leaking confidential content."
level\_4\_label: Champion
level\_4\_descriptor: "Spots new risk patterns (e.g., prompts that could re-identify clients through unique descriptors). Shares safe prompt examples with the team, reinforces correct tool boundaries, and models careful review before sending client-facing content."

***

### Domain: strategic\_prompting

domain\_id: strategic\_prompting
title: Strategic Prompting
description: "Structuring prompts so AI outputs are directly usable in RM work—prospect research summaries, tailored outreach drafts, discovery questions, pitch-deck outlines, and internal handoff notes—using the right context, constraints, and format so results don’t become generic sales fluff."
level\_0\_label: Unaware
level\_0\_descriptor: "Has not used AI prompting in RM tasks. Can’t explain what information the AI needs to produce usable outreach or meeting prep."
level\_1\_label: Explorer
level\_1\_descriptor: "Uses simple prompts (‘draft an email’, ‘summarize this company’). Output is generic and requires heavy rewriting; often misses exporter context or EDC positioning."
level\_2\_label: Practitioner
level\_2\_descriptor: "Uses structured prompts with clear audience, purpose, and format (e.g., 120-word email + 3 bullet-value points + 2 discovery questions). Outputs are usually usable with minor edits."
level\_3\_label: Proficient
level\_3\_descriptor: "Iterates intelligently when output misses the mark—tightens constraints, adds a competitive/industry angle, and requests specific deliverables (call script, objection handling, next-step options) matched to deal stage."
level\_4\_label: Champion
level\_4\_descriptor: "Builds reusable prompt templates for common RM flows (new lead → first email → call prep → follow-up). Coaches peers on prompt structure and shares examples that improve response rates while staying compliant."

***

### Domain: critical\_eval

domain\_id: critical\_eval
title: Critical Evaluation
description: "Reviewing AI outputs with a skeptical lens before using them in high-stakes RM work: financial ratio commentary from Excel, summaries of meetings/emails, pipeline insights from dashboards, and client-facing drafts. Focus is on catching incorrect numbers, invented facts, and misapplied interpretations before logging into CRM or sending externally."
level\_0\_label: Unaware
level\_0\_descriptor: "Assumes AI outputs are correct. Copies AI-written financial commentary or meeting recaps into records/emails without checking source data."
level\_1\_label: Explorer
level\_1\_descriptor: "Skims AI output for obvious issues but doesn’t systematically verify claims (dates, figures, commitments, next steps) against notes, files, or CRM entries."
level\_2\_label: Practitioner
level\_2\_descriptor: "Routinely verifies outputs against source material (client docs, meeting notes, dashboard numbers). Corrects or removes anything unverifiable before it becomes a client message or CRM update."
level\_3\_label: Proficient
level\_3\_descriptor: "Catches subtle, plausible errors (e.g., swapped units, misread variance drivers, wrong geography). Adjusts prompts to reduce hallucinations and asks AI to cite which input it used (where possible), then confirms manually."
level\_4\_label: Champion
level\_4\_descriptor: "Creates a simple verification checklist for team use (numbers, dates, commitments, product claims). Teaches peers common failure modes in summaries and analyses, improving overall record quality."

***

### Domain: relationship\_intel

domain\_id: relationship\_intel
title: Relationship Intelligence
description: "Using AI to synthesize relationship history and context so every interaction feels informed: compiling interaction timelines from emails/notes, surfacing open threads, identifying stakeholder preferences, and tailoring prep for quarterly reviews and high-stakes calls—without over-relying on automated recaps."
level\_0\_label: Unaware
level\_0\_descriptor: "Preps for meetings by memory or manual CRM review only. Doesn’t use AI to synthesize relationship history or spot patterns."
level\_1\_label: Explorer
level\_1\_descriptor: "Uses AI for generic company research or a high-level recap. Output isn’t tied to the specific relationship (deal stage, past friction points, internal commitments)."
level\_2\_label: Practitioner
level\_2\_descriptor: "Uses AI to produce a focused relationship brief: last interactions, unresolved asks, stakeholder map, and suggested agenda—then validates against CRM and key email threads before a call."
level\_3\_label: Proficient
level\_3\_descriptor: "Identifies relationship signals (e.g., repeated concerns, slow response patterns, decision-maker preferences). Adapts outreach and meeting structure accordingly, and avoids ‘surprise’ topics by confirming context."
level\_4\_label: Champion
level\_4\_descriptor: "Builds a lightweight relationship-brief template for the team (handoffs, annual reviews, escalations). Coaches peers to use AI as a starting point while preserving nuance and trust."

***

### Domain: data\_decision

domain\_id: data\_decision
title: Data-Driven Decision Making
description: "Using AI and analytics to prioritize effort and improve decisions: interpreting portfolio dashboards, spotting aging/stale leads, connecting market trends to outreach strategy, and stress-testing assumptions—while recognizing where AI lacks the commercial and relationship context the RM holds."
level\_0\_label: Unaware
level\_0\_descriptor: "Doesn’t use data tools to guide pipeline decisions. Relies on intuition and ad-hoc lists; misses aging leads or SLA risks."
level\_1\_label: Explorer
level\_1\_descriptor: "Views dashboards but mostly consumes metrics passively. Uses AI for generic market commentary without linking insights to specific pipeline actions."
level\_2\_label: Practitioner
level\_2\_descriptor: "Uses dashboards and AI explanations to take concrete actions: flags leads over SLA, identifies aging qualified leads, and chooses next-best outreach targets—then sanity-checks with relationship context and workload."
level\_3\_label: Proficient
level\_3\_descriptor: "Frames better questions for AI and analytics (by segment, sector, activity recency). Uses data to run ‘what if’ thinking (e.g., which accounts are most likely win-back) and documents rationale for prioritization."
level\_4\_label: Champion
level\_4\_descriptor: "Shares repeatable portfolio review patterns with the team (filters, thresholds, a short prioritization rubric). Helps peers interpret dashboards correctly and avoid false certainty from AI-generated insights."

***

### Domain: augmented\_comm

domain\_id: augmented\_comm
title: Augmented Communication
description: "Choosing the right M365 Copilot surface for RM communication work and chaining outputs end-to-end: meeting recap → action list → CRM update → follow-up email → internal handoff. Emphasis is on speed with control: accurate, compliant, and audience-appropriate messages across Outlook/Teams/Word/PowerPoint."
level\_0\_label: Unaware
level\_0\_descriptor: "Unaware of Copilot capabilities across Outlook/Teams/Word/PowerPoint/Excel. Drafts everything manually and doesn’t reuse AI outputs across steps."
level\_1\_label: Explorer
level\_1\_descriptor: "Uses Copilot in one place (e.g., email drafting) but doesn’t connect it to record governance (actions, owners) or pipeline hygiene."
level\_2\_label: Practitioner
level\_2\_descriptor: "Uses multiple Copilot surfaces and a simple chain (e.g., Teams recap → Outlook follow-up). Ensures action items are accurate and assigns owners clearly before sharing or logging."
level\_3\_label: Proficient
level\_3\_descriptor: "Designs multi-step workflows across 3+ surfaces (notes → recap → CRM fields → follow-up + internal summary). Recovers when one step is weak (re-prompts, tightens format, re-checks facts)."
level\_4\_label: Champion
level\_4\_descriptor: "Documents best-practice chains for the team (templates + do/don’t). Encourages consistent record governance and teaches peers how to keep outputs accurate and compliant under time pressure."

***

# SECTION C — All 7 Course Specs

### Course 1 — Safeguard Before You Summarize

course\_id: rm\_c1\_responsible\_ai
role\_id: rm
primary\_domain: responsible\_ai
sequence\_order: 1
title: "Safeguard Before You Summarize: Client Data and AI"
tagline: "Use SAFE abstraction to get AI help without exposing non-public client information."
description: "RMs often feel time pressure to summarize client documents, meeting notes, and deal context quickly. This course builds the habit of sanitizing inputs, choosing safe tools, and rewriting prompts so you keep confidentiality intact while still getting useful drafts for internal work."
real\_use\_case: "The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada)."

### Course 2 — Prompt for Prospect Precision

course\_id: rm\_c2\_strategic\_prompting
role\_id: rm
primary\_domain: strategic\_prompting
sequence\_order: 2
title: "Prompt for Prospect Precision: From Thin Lead to Strong Outreach"
tagline: "Turn minimal lead info into tailored outreach using CRAF."
description: "New leads often arrive with only basic details. This course teaches the CRAF framework (Context, Role, Action, Format) to generate usable prospect snapshots and first-contact emails that sound informed, relevant, and RM-authentic—not generic templates."
real\_use\_case: "Prospect Intelligence"

### Course 3 — Trust, Then Verify the Numbers

course\_id: rm\_c3\_critical\_eval
role\_id: rm
primary\_domain: critical\_eval
sequence\_order: 3
title: "Trust, Then Verify: Catching AI Errors in Financial Commentary"
tagline: "Use VERIFY to validate AI-driven variance explanations before sharing."
description: "When AI helps interpret financials or ratios, small errors can create big downstream risk. This course gives RMs a practical verification routine to confirm numbers, assumptions, and interpretations before anything reaches underwriting, CRM, or the client."
real\_use\_case: "Financial Variance Analyzer"

### Course 4 — Brief the Relationship, Not Just the Company

course\_id: rm\_c4\_relationship\_intel
role\_id: rm
primary\_domain: relationship\_intel
sequence\_order: 4
title: "Brief the Relationship: AI-Powered Meeting Prep That Keeps Nuance"
tagline: "Use RELATE to synthesize history, stakeholders, and open threads—then validate."
description: "RMs need more than a company summary—they need the relationship story: what happened, what’s unresolved, and what matters to the people in the room. This course teaches a structured way to generate relationship briefs from internal signals (notes, emails, prior actions) without over-relying on automated recaps."
real\_use\_case: "Customer Interaction Recap"

### Course 5 — Decide With Signals, Not Noise

course\_id: rm\_c5\_data\_decision
role\_id: rm
primary\_domain: data\_decision
sequence\_order: 5
title: "Decide With Signals: Turning Dashboards and Market Insights into Actions"
tagline: "Use SIGNAL to translate analytics into next-best actions for your portfolio."
description: "Dashboards and market tools can surface risks and opportunities—but only if you know what to look for and how to act. This course teaches RMs to combine portfolio analytics (lead aging, SLA risk, activity recency) with market insights to prioritize outreach and planning with clear rationale."
real\_use\_case: "Market Insights Generator"

### Course 6 — Close the Loop, Clean the Records

course\_id: rm\_c6\_augmented\_comm
role\_id: rm
primary\_domain: augmented\_comm
sequence\_order: 6
title: "Close the Loop: From Meeting to Actions to Clean Records"
tagline: "Use Copilot surfaces to produce accurate recaps, owners, and follow-ups—fast."
description: "RMs live in back-to-back calls. This course builds a repeatable multi-step workflow to convert meeting outcomes into action lists, clean CRM updates, and polished follow-ups—without losing accuracy, ownership clarity, or compliance discipline."
real\_use\_case: "Record governance - Summarizing Meeting notes and actions (with attendees tagged)"

### Course 7 — Capstone: Prospect to Portfolio Follow-Through

course\_id: rm\_c7\_capstone
role\_id: rm
primary\_domain: responsible\_ai
sequence\_order: 7
title: "End-to-End AI Assist: From Prospecting to Client Follow-Up"
tagline: "Run an integrated workflow across all six domains without cutting corners."
description: "A realistic, end-to-end RM scenario: use AI to identify and prioritize a target account, craft outreach, prepare for a meeting using relationship history, validate AI-assisted analysis, and deliver compliant follow-ups and record updates. Learners must demonstrate good judgment, verification, and safe handling of information across the full chain."
real\_use\_case: "Access to Copilot 365 for Business Development; Customer Interaction Recap; Record governance - Summarizing Meeting notes and actions (with attendees tagged)"

***

# SECTION D — All 7 Scenario Seeds

### Course 1 Scenario

scenario\_text: "You receive a confidential package from Harbourline Fabrication Ltd. (financial statements, a draft expansion plan, and a note asking for ‘a quick risk read’ before Friday). You’re tempted to paste the contents into an external AI tool to save time. You need AI help—but you must protect non-public client information and keep your workflow inside approved boundaries."
task\_1\_text: "Identify 5 specific pieces of information in the package that should NOT be entered into a non-approved AI tool. Rewrite them as SAFE abstractions (generic but still useful)."
task\_2\_text: "Write a SAFE-style prompt to generate a 1-page internal briefing note (not client-facing) using only abstracted inputs. Include a clear format (headings + bullets)."
task\_3\_text: "Your prompt still risks re-identification because the expansion plan references a unique project. Revise the prompt to remove re-identifying detail while preserving decision usefulness."
task\_4\_text: "You now need a client-facing email acknowledging receipt and outlining next steps—without revealing sensitive details back to the client or introducing new claims. Add constraints to your prompt to prevent accidental disclosure or invented facts."
coach\_system\_prompt: "You are an AI skills coach for EDC Relationship Managers. Help the learner apply Responsible AI and the SAFE Abstraction Method. Do NOT write the final prompt or the rewritten text for them. Ask guiding questions to help them spot non-public data and re-identification risk. Flag red flags: client names, exact revenue/ratios, internal risk ratings, KYC identifiers, deal terms, or any pasted document text. Encourage using abstracted descriptors and keeping drafts in approved environments."

### Course 2 Scenario

scenario\_text: "A new lead for Prairie Pulse Foods Inc. appears with minimal detail: ‘Agri-food exporter, Western Canada, exploring new markets, revenue range only.’ You need to send a first outreach email and propose a discovery call agenda. The temptation is to ask Copilot for a generic email and hit send."
task\_1\_text: "Write a CRAF prompt to generate (a) a 120-word outreach email and (b) 5 discovery questions tailored to an agri-food exporter. Include formatting requirements."
task\_2\_text: "The output is still generic. Revise your prompt to add context: likely export markets, common working-capital pressures, and what EDC can help with—without inventing facts about the company."
task\_3\_text: "You learn the prospect’s preferred language is French. Revise the Format instruction to produce a bilingual output (EN + FR) and add a constraint to keep product claims accurate and conservative."
task\_4\_text: "The draft email includes a claim about EDC ‘guaranteeing approvals.’ Add a constraint and a verification step instruction to prevent misleading product promises in the next iteration."
coach\_system\_prompt: "You are an AI skills coach for EDC Relationship Managers practicing the CRAF framework. Do NOT write the prompt for them. Instead, ask which CRAF element is weakest and what missing context would make the email truly specific. Watch for invented facts, over-promising language, and any sensitive internal info. Push them to add constraints (tone, accuracy, length, structure) and to request outputs that are directly usable."

### Course 3 Scenario

scenario\_text: "You are preparing for an internal credit discussion on SkyNorth Aero Components Inc. You use Excel to compute ratios and ask AI for a variance explanation. The AI produces confident commentary, but you know small numeric errors can derail underwriting trust. The temptation is to forward the commentary as-is to save time."
task\_1\_text: "List the 4 most important things you must verify before trusting an AI-written variance explanation (e.g., which numbers, what assumptions)."
task\_2\_text: "Write a prompt that asks the AI to explain variances while also requiring it to (a) show its calculation steps in plain language and (b) label anything it is unsure about."
task\_3\_text: "The AI commentary includes a driver that isn’t supported by your source numbers. Draft a follow-up prompt that forces the AI to stick strictly to the provided figures and to output a ‘source check’ section."
task\_4\_text: "Create a final ‘ready-to-share’ internal summary format: 6 bullets max, each bullet tied to a verified figure, and a final line listing ‘open questions to confirm with the client.’ Add those constraints to your prompt."
coach\_system\_prompt: "You are an AI skills coach for EDC Relationship Managers practicing Critical Evaluation using the VERIFY checklist. Do NOT calculate ratios or write the final summary for the learner. Guide them to cross-check numbers, isolate assumptions, and remove unverifiable claims. Red flags: invented market explanations, unsupported drivers, or any step that bypasses validation against the spreadsheet/source."

### Course 4 Scenario

scenario\_text: "You have a quarterly review meeting with GlacierTech Robotics Ltd. next week. You want a relationship brief that captures what matters: previous commitments, unresolved issues, stakeholder preferences, and what to push forward now. The temptation is to rely entirely on an AI-generated recap without checking the underlying threads."
task\_1\_text: "Write a prompt to generate a relationship brief using the RELATE framework. Specify sections: Relationship Timeline, Open Threads, Stakeholder Map, and Suggested Agenda."
task\_2\_text: "Your draft brief includes a ‘client concern’ you can’t find in your notes. Add a verification instruction that forces the AI to label each claim as ‘confirmed’ (supported by input) or ‘needs confirmation’ (not supported)."
task\_3\_text: "The meeting includes a new CFO. Revise your prompt so the brief includes a short ‘onboarding summary’ for the CFO: what EDC is doing today, what’s pending, and what decisions are needed."
task\_4\_text: "You need to personalize outreach to schedule pre-reads. Add constraints to generate two outputs: (1) a 90-word email to the CFO and (2) a separate 90-word email to the operations lead—each referencing only confirmed facts and preserving a professional tone."
coach\_system\_prompt: "You are an AI skills coach for EDC Relationship Managers practicing Relationship Intelligence with the RELATE framework. Do NOT write the brief or the emails. Ask questions that help the learner define what ‘confirmed’ means and what sources they will validate against (notes, email threads, CRM fields). Watch for hallucinated ‘issues,’ invented commitments, or overconfident stakeholder assumptions."

### Course 5 Scenario

scenario\_text: "It’s Monday morning pipeline review. You open a portfolio dashboard and see several leads approaching SLA thresholds and qualified leads aging past healthy ranges. You also have a market insight summary suggesting demand shifts in your region. The temptation is to let AI choose your week’s priorities automatically, without applying relationship context or sanity checks."
task\_1\_text: "From the dashboard cues, list 3 ‘signals’ that should change your actions this week (e.g., over-SLA leads, aging qualified leads, no planned activity). Explain why each signal matters."
task\_2\_text: "Write a prompt that asks AI to propose a prioritized top-10 outreach list, but requires it to explain the rationale using your SIGNAL framework (what signal, what action, what expected outcome)."
task\_3\_text: "Your first output ignores relationship nuance (e.g., a sensitive renewal). Add constraints that require a ‘human override’ step: where you insert relationship notes and the AI re-orders priorities accordingly."
task\_4\_text: "Turn the final prioritized list into a 30-minute ‘pipeline huddle’ script: 10 minutes metrics, 15 minutes top risks/opportunities, 5 minutes commitments. Add a constraint to keep it short and aligned to what dashboards actually show (no invented metrics)."
coach\_system\_prompt: "You are an AI skills coach for EDC Relationship Managers practicing Data-Driven Decision Making with the SIGNAL framework. Do NOT choose the priorities for them. Guide them to separate signal from speculation and to keep outputs grounded in the dashboard inputs. Red flags: invented KPIs, overconfident predictions, or decisions made without a stated rationale and a human review step."

### Course 6 Scenario

scenario\_text: "You finish a client call with Bluewave Marine Logistics Inc. and immediately have two more meetings. You need to capture decisions, action owners, and update records—fast. The temptation is to auto-send an AI recap without checking accuracy, owners, or tone."
task\_1\_text: "Design a Copilot Surface Selector plan: which tool do you start in (Teams/Outlook/Word) and what output do you need first? Explain in one sentence why."
task\_2\_text: "Write a prompt/instruction to generate a meeting recap with: Decisions (bold), Actions (owner + due date placeholder), and ‘Items to confirm’—with a constraint to avoid adding facts not said."
task\_3\_text: "Revise the instruction to produce two variants: (1) client-facing follow-up email (friendly, clear) and (2) internal handoff note (more detailed, includes risk/compliance reminders) while keeping sensitive details out of the client version."
task\_4\_text: "Add a final step: a ‘record governance’ checklist that ensures the recap is log-ready (correct attendees/owners, no confidential details, action phrasing is unambiguous). Embed this into your workflow so you don’t skip it under time pressure."
coach\_system\_prompt: "You are an AI skills coach for EDC Relationship Managers practicing Augmented Communication and record governance. Do NOT write the recap or emails. Guide them to select the right Copilot surface, define outputs, and add constraints that prevent hallucinations and privacy breaches. Watch for: invented decisions, missing owners, leaking sensitive details into client emails, and ‘send without review’ behaviors."

### Course 7 Scenario

scenario\_text: "Evergreen Advanced Materials Group is a high-potential exporter you want to win. You need to (1) pick the right outreach targets using business development Copilot workflows, (2) prepare a meeting brief using relationship history, (3) sanity-check an AI-assisted analysis, and (4) send compliant follow-ups and clean record updates. The temptation is to rush: paste too much data, trust AI outputs too much, and send drafts without verification."
task\_1\_text: "Draft a SAFE-abstracted input pack (no identifiers, no sensitive figures) that is sufficient for AI to help you: prospect snapshot + outreach angle + 3 discovery hypotheses."
task\_2\_text: "Write a CRAF prompt to produce: (a) a 120-word outreach email, (b) a 1-page meeting brief, and (c) 5 discovery questions—each clearly formatted."
task\_3\_text: "Add VERIFY steps: require the AI output to include a ‘checklist of what you must confirm’ before you log anything or send it externally (numbers, commitments, product claims, dates)."
task\_4\_text: "Design a Copilot Surface Selector chain that ends with (1) a client follow-up email, (2) an internal summary for underwriting/product partners, and (3) a record-ready action list—each with constraints to prevent sensitive leakage and invented facts."
coach\_system\_prompt: "You are an AI skills coach for EDC Relationship Managers guiding an End-to-End AI Workflow. Do NOT produce final prompts, emails, or briefs. Guide the learner to integrate SAFE, CRAF, VERIFY, RELATE, SIGNAL, and Copilot Surface Selector. Watch for: inclusion of non-public client data, invented metrics or promises, skipping verification, and failing to separate client-facing vs internal detail."

***

# SECTION E — All 7 Reading Concept Specs

### Course 1 Reading

framework\_name: "The SAFE Abstraction Method"
concept\_text: "RMs work with sensitive client information every day—financial statements, business plans, KYC details, internal pipeline notes. AI can help you summarize, draft, and organize, but only if you protect what must stay protected. SAFE is a practical method to ‘strip risk while keeping usefulness.’ **S**ubstitute identifiers (client name → ‘mid-market exporter’). **A**bstain from exact sensitive figures (replace with ranges or directional terms). **F**ocus on the decision (what you need to decide or prepare) rather than the raw document text. **E**nsure the tool boundary is right: keep sensitive work in approved environments and never paste full documents into non-approved tools. SAFE also reduces accidental re-identification: even if you remove the name, a unique project or niche geography can still reveal the client. The goal isn’t to be vague—it’s to be safely specific. With SAFE, you can get a draft briefing note, an internal Q\&A list, or a follow-up structure while staying within policy and protecting trust."
good\_example: "Before (unsafe): ‘Here is Harbourline Fabrication’s full 50-page financial report and expansion plan. Summarize risks and recommend terms.’
After (SAFE, approved boundary): ‘Context (abstracted): Mid-market Canadian manufacturer exporting to US/EU. Seeking growth financing; profitability declined last year; liquidity tight but improving. Action: Draft a 1-page internal briefing note: key questions to ask, potential risk themes to investigate, and next-step checklist. Format: headings + bullets. Constraint: Do not invent numbers or terms; label unknowns as “needs confirmation.”’"
anti\_pattern: "Copy-pasting a client’s full financial statements or CRM record into an external AI tool to ‘save time.’ Consequence: potential confidentiality breach and loss of trust; plus you may end up with invented numbers you can’t defend."
takeaway: "SAFE lets you use AI without ‘data dumping’: abstract what’s sensitive, keep focus on decisions, and stay inside approved tool boundaries."

### Course 2 Reading

framework\_name: "CRAF Framework"
concept\_text: "When a lead is thin, generic prompts produce generic outreach. CRAF helps you reliably get usable prospect outputs. **C—Context:** what you know (sector, region, exporter status, likely markets, business pressures) without inventing facts. **R—Role:** the voice you need (Relationship Manager at a Canadian export finance institution). **A—Action:** the deliverable (a short outreach email, discovery questions, call agenda). **F—Format:** how it should look (word count, bullets, bilingual structure). In RM work, Format is the difference between ‘a page of fluff’ and something you can send today. CRAF also helps you avoid compliance mistakes: you can constrain tone (professional, no overpromising), and tell AI to separate confirmed facts from hypotheses. The best prompts make the AI do the hard work (structure + drafting) while you keep ownership of truth, judgment, and relationship nuance."
good\_example: "Prompt (CRAF): ‘Context: Prairie Pulse Foods—agri-food exporter, Western Canada, exploring new markets; we only know sector + exporter status. Role: You are an RM at EDC. Action: Draft (1) a 120-word intro email proposing a 20-min discovery call and (2) five discovery questions focused on export growth and risk. Format: Email first (subject + 2 short paragraphs + 3 bullets), then questions as bullets. Constraints: Don’t invent company-specific facts; don’t promise approvals; keep product claims general.’"
anti\_pattern: "‘Write a sales email for this lead.’ Consequence: bland, non-specific email that sounds automated and can undermine credibility."
takeaway: "CRAF turns thin inputs into strong outputs—by being safely specific about context, deliverable, and structure."

### Course 3 Reading

framework\_name: "VERIFY Checklist"
concept\_text: "AI can be persuasive even when it’s wrong—especially with numbers. VERIFY is a quick discipline to prevent bad analysis from slipping into underwriting discussions or CRM notes. **V—Validate figures:** compare each key number/ratio to the spreadsheet/source. **E—Explain the math:** can you restate how the ratio/variance was derived? **R—Review assumptions:** what did the AI assume (seasonality, FX, one-time events) that isn’t in your data? **I—Investigate anomalies:** if something looks off, isolate the input cell/line item and re-check. **F—Flag uncertainty:** label anything not supported by the inputs as ‘needs confirmation.’ **Y—Your judgment:** decide what’s useful, what’s risky, and what questions to ask next. VERIFY doesn’t slow you down—it prevents rework and protects trust with partners who rely on your accuracy."
good\_example: "Before (unsafe): Forwarding AI commentary that claims ‘margin improved due to cost reductions’ without checking the cost lines.
After (VERIFY): ‘AI draft is a starting point. I validated revenue and gross margin % against the sheet, confirmed the variance math, removed unsupported drivers, and added 3 questions to confirm with the client (pricing, input costs, FX exposure).’"
anti\_pattern: "Treating AI narrative as ‘analysis done.’ Consequence: you may share incorrect drivers or ratios, weakening underwriting confidence and creating avoidable back-and-forth."
takeaway: "VERIFY makes AI output defensible: every claim must tie to a checked figure or be clearly flagged as uncertain."

### Course 4 Reading

framework\_name: "RELATE Framework"
concept\_text: "A relationship brief isn’t a company profile—it’s the story of interactions, commitments, and people. RELATE keeps AI-generated briefs useful and honest. **R—Recall timeline:** last touchpoints and outcomes (what happened). **E—Extract open threads:** unresolved asks, promised follow-ups, pending approvals. **L—List stakeholders:** who matters, what they care about, and how they prefer to work (only if supported by notes). **A—Align to meeting goal:** what decision or progress you need now. **T—Tailor agenda:** topics in the right order for the audience (e.g., new CFO needs a clean status recap first). **E—Evidence tagging:** label each brief item as ‘confirmed’ (from inputs) or ‘needs confirmation’ (not supported). This approach avoids the biggest relationship-intel trap: hallucinated ‘client concerns’ that never existed. You use AI to structure and surface patterns—then you validate so you don’t damage trust."
good\_example: "Prompt: ‘Use RELATE to draft a 1-page relationship brief for GlacierTech Robotics. Include sections: Timeline, Open Threads, Stakeholders, Suggested Agenda. Add an Evidence Tag (Confirmed / Needs Confirmation) per bullet. Constraint: Don’t invent issues or commitments.’"
anti\_pattern: "Asking AI for ‘a full recap of the relationship’ and believing it without checking threads. Consequence: you may raise non-existent problems or miss critical nuance, creating awkwardness in the meeting."
takeaway: "RELATE helps you prepare like you remember everything—without pretending AI is always right."

### Course 5 Reading

framework\_name: "SIGNAL Framework"
concept\_text: "Dashboards and market tools can overwhelm you with ‘noise.’ SIGNAL converts analytics into clear actions. **S—Spot the signal:** identify the metric cue that matters (e.g., lead over SLA, aging qualified lead, no planned activity). **I—Interpret meaning:** what risk/opportunity does it imply? **G—Ground with context:** add what you know (relationship sensitivity, upcoming travel, internal dependencies). **N—Name next action:** the specific next step (call, email, partner intro, internal escalation). **A—Assign timing:** when it happens this week and what ‘done’ looks like. **L—Log the rationale:** one sentence you can defend in a pipeline huddle. SIGNAL prevents a common failure mode: letting AI ‘auto-prioritize’ without human override. You want AI to propose options, not make decisions. Use SIGNAL to keep prioritization explainable and consistent."
good\_example: "‘Signal: Qualified lead >150 days old (highlighted) + no planned activity. Meaning: risk of stall. Context: client recently changed CFO. Next action: 15-min check-in call + send a one-page status recap. Timing: Tuesday morning. Log rationale: prevent stall and re-anchor stakeholder.’"
anti\_pattern: "‘AI says these are my top 10 accounts’ with no explanation. Consequence: you can’t defend trade-offs in huddles and you may ignore real relationship constraints."
takeaway: "SIGNAL turns analytics into decisions you can explain, execute, and defend."

### Course 6 Reading

framework\_name: "Copilot Surface Selector"
concept\_text: "RMs don’t just need a draft—they need a workflow. Copilot Surface Selector is a simple rule: start where the best input lives, then move outputs to where action happens. If the input is a meeting, start with the meeting recap surface; if it’s a document, start in Word; if it’s numbers, start in Excel; if it’s outreach, start in Outlook. Then chain outputs: recap → actions → internal note → client email → record update. The selector also forces two guardrails: (1) separate client-facing vs internal detail, and (2) never send without a verification pass (decisions, owners, dates, product claims). The point is speed with control—especially when you’re moving between calls and the temptation is to ‘auto-send’."
good\_example: "Workflow: Start from call recap → generate Decisions/Actions list → produce a client-friendly follow-up email → generate an internal handoff note → final ‘log-ready’ checklist. Constraint: ‘No invented commitments; mark unknown due dates as placeholders.’"
anti\_pattern: "One-click recap emailed to the client without review. Consequence: wrong owners, wrong dates, awkward tone, or accidental disclosure."
takeaway: "Pick the right surface, chain outputs, and always insert a verification gate before sending or logging."

### Course 7 Reading

framework\_name: "End-to-End AI Workflow"
concept\_text: "In real RM work, AI value comes from the full chain—not one isolated prompt. The End-to-End AI Workflow integrates six disciplines: SAFE (protect inputs), CRAF (get usable drafts), VERIFY (check numbers/claims), RELATE (keep relationship nuance), SIGNAL (act on analytics with rationale), and Copilot Surface Selector (choose the right tool at each step). The capstone mindset is simple: AI accelerates the draft and structure, but the RM owns truth, judgment, and trust. This workflow also prevents ‘compound error’: a small hallucination in a meeting brief becomes an incorrect email, then becomes a wrong CRM record. By inserting verification and constraints at each step, you keep speed and reduce risk. A strong end-to-end workflow is repeatable: you can run it every week for pipeline review, every time you onboard a new stakeholder, and after every key client call—without cutting corners."
good\_example: "‘Step 1 SAFE abstracted pack → Step 2 CRAF outputs (email + brief + questions) → Step 3 VERIFY checklist embedded → Step 4 RELATE evidence tags → Step 5 SIGNAL prioritization rationale → Step 6 surface chain for recap + follow-ups + record governance.’"
anti\_pattern: "Using AI as a ‘black box’: paste everything in, accept the output, send/log it immediately. Consequence: privacy risk + misinformation risk + relationship damage."
takeaway: "End-to-end wins are about disciplined handoffs between steps—every step has a guardrail."

***

# SECTION F — Diagnostic Item Seeds (18 items: 3 per domain × 6 domains)

### Diagnostic: responsible\_ai

Item 1 — type: mcq
Tests: recognizing unsafe AI input in RM work
question\_text: "Which input is MOST risky to paste into a non-approved AI tool?"
options: A) A public news link about a client’s sector | B) A sanitized description of a ‘mid-market exporter’ | C) A client’s full financial statement PDF text | D) A generic list of discovery questions
correct\_option: C
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox
Tests: writing a SAFE-abstracted prompt
scenario\_text: "A client emailed you a confidential expansion plan and asked for a quick summary of risks and questions to discuss."
question\_text: "Write a SAFE-style prompt to generate an internal 1-page briefing note without including client identifiers or sensitive figures."
scoring rubric criteria:

* "Substitutes identifiers (no client name or unique identifiers)": max 1
* "Avoids exact sensitive figures (uses ranges/directional terms)": max 1
* "Focuses on decision need (questions/next steps) rather than raw document text": max 1
* "Includes constraints to avoid invention and label unknowns": max 1

Item 3 — type: micro\_task
Tests: spotting re-identification risk
scenario\_text: "A prompt says: ‘Summarize the expansion plan for the only Canadian exporter building a cobalt refinery in \[specific small town].’"
question\_text: "In one sentence, explain why this is still risky even without a company name—and how you would abstract it safely."
scoring rubric criteria:

* "Identifies re-identification risk via unique descriptor": max 1
* "Proposes removing/abstracting unique location/project detail": max 1
* "Keeps useful context (industry/segment) without uniqueness": max 1
* "Mentions tool boundary/approved environment or ‘don’t paste raw plan’": max 1

***

### Diagnostic: strategic\_prompting

Item 1 — type: mcq
Tests: understanding what makes output usable
question\_text: "An RM gets a generic outreach email from AI. Which prompt change most directly increases specificity without inventing facts?"
options: A) Ask for a longer email | B) Add clear context + constraints + format (CRAF) | C) Remove the role instruction | D) Ask for more enthusiasm
correct\_option: B
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox
Tests: writing a complete CRAF prompt
scenario\_text: "New lead: agri-food exporter, Western Canada, exploring new markets. You need a first outreach email and discovery questions."
question\_text: "Write a CRAF prompt that produces a 120-word email and 5 discovery questions, with constraints to avoid invented facts and overpromising."
scoring rubric criteria:

* "Context includes realistic, non-invented sector/exporter pressures": max 1
* "Role instruction is present (RM/EDC voice)": max 1
* "Action specifies deliverables (email + questions) with limits": max 1
* "Format clearly structures output (sections/word count/bullets)": max 1

Item 3 — type: micro\_task
Tests: diagnosing missing CRAF elements
scenario\_text: "Prompt: ‘Write an email to this lead about our solutions.’ Output: generic, 400 words, vague."
question\_text: "Name the two missing CRAF elements that most likely caused the generic output and why."
scoring rubric criteria:

* "Correctly identifies missing/weak Context": max 1
* "Correctly identifies missing/weak Action and/or Format": max 1
* "Explains how missing elements produce generic output": max 1
* "Mentions adding constraints (no invented facts/word limit)": max 1

***

### Diagnostic: critical\_eval

Item 1 — type: mcq
Tests: recognizing AI risk in numeric commentary
question\_text: "Why is AI-written variance commentary risky to forward without review?"
options: A) It may use too many bullets | B) It can invent drivers not supported by data | C) It is always too short | D) It cannot use finance terms
correct\_option: B
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox
Tests: embedding verification in a prompt
scenario\_text: "You asked AI to explain ratio changes. It responded confidently with several drivers."
question\_text: "Write a prompt that forces the AI to show calculation steps in plain language and label any assumptions vs confirmed facts."
scoring rubric criteria:

* "Requires explicit separation of confirmed vs assumed": max 1
* "Asks for calculation logic/steps or traceability": max 1
* "Includes constraint to avoid adding data not provided": max 1
* "Specifies a tight output format (bullets/sections)": max 1

Item 3 — type: micro\_task
Tests: correcting an unverifiable claim
scenario\_text: "AI output: ‘Margins improved due to lower input costs,’ but your sheet shows input costs increased."
question\_text: "Write one corrected sentence that sticks to verified figures and adds a ‘needs confirmation’ note if required."
scoring rubric criteria:

* "Removes the incorrect driver": max 1
* "Anchors statement to verified figure/direction": max 1
* "Adds ‘needs confirmation’ when causality is unknown": max 1
* "Uses cautious, internal-appropriate tone": max 1

***

### Diagnostic: relationship\_intel

Item 1 — type: mcq
Tests: avoiding over-reliance on auto-recaps
question\_text: "What is the best way to use an AI-generated relationship recap?"
options: A) Use it as the only prep source | B) Use it as a starting draft, then validate against key threads/notes | C) Send it to the client as-is | D) Avoid it entirely
correct\_option: B
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox
Tests: RELATE-structured brief prompt
scenario\_text: "You have a quarterly review with a client, including a new CFO. You want a relationship brief with open threads and stakeholder notes."
question\_text: "Write a RELATE-based prompt that produces a 1-page brief and requires evidence tagging (confirmed vs needs confirmation)."
scoring rubric criteria:

* "Includes RELATE sections (timeline, open threads, stakeholders, agenda)": max 1
* "Requires evidence tagging/confirmation labeling": max 1
* "Adds a CFO onboarding mini-section": max 1
* "Includes a constraint against invented issues/commitments": max 1

Item 3 — type: micro\_task
Tests: spotting a hallucinated relationship claim
scenario\_text: "Brief says: ‘Client is unhappy with turnaround times,’ but your notes show no mention of dissatisfaction."
question\_text: "In one sentence, explain what you should do before using this claim in the meeting."
scoring rubric criteria:

* "States you must verify against notes/threads": max 1
* "Says to remove or label as unconfirmed if not supported": max 1
* "Mentions risk of damaging trust if wrong": max 1
* "Proposes a safe alternative (ask a neutral check-in question)": max 1

***

### Diagnostic: data\_decision

Item 1 — type: mcq
Tests: interpreting dashboard signals
question\_text: "A dashboard highlights a qualified lead in yellow due to age. What is the best first response?"
options: A) Ignore it; it will close itself | B) Immediately close the lead | C) Investigate activity recency and plan a next action | D) Ask AI to predict revenue
correct\_option: C
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox
Tests: SIGNAL-based prioritization prompt
scenario\_text: "It’s pipeline review day. You have multiple leads over SLA and aging qualified leads, plus limited time this week."
question\_text: "Write a prompt that asks AI to propose a top-10 priority list using SIGNAL (signal → meaning → context → next action → timing → rationale)."
scoring rubric criteria:

* "Explicitly requests SIGNAL structure in the output": max 1
* "Requires rationale per priority item": max 1
* "Includes a ‘human override/context’ step": max 1
* "Constrains output to avoid invented metrics": max 1

Item 3 — type: micro\_task
Tests: improving explainability
scenario\_text: "AI output: ‘These are your top accounts this week.’ No rationale provided."
question\_text: "Write one sentence instructing the AI to add explainable rationale tied to dashboard signals."
scoring rubric criteria:

* "Requests linking each priority to a specific signal": max 1
* "Requests a next action per item": max 1
* "Requests timing/urgency logic": max 1
* "Requests avoidance of speculation/invention": max 1

***

### Diagnostic: augmented\_comm

Item 1 — type: mcq
Tests: selecting the right Copilot surface
question\_text: "If your primary input is a meeting you just finished, where should you start your AI-assisted workflow?"
options: A) PowerPoint | B) Teams meeting recap surface | C) A blank Excel sheet | D) A public web chatbot
correct\_option: B
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox
Tests: record governance recap prompt
scenario\_text: "You finished a client call and need a recap with decisions and action owners, plus a client-friendly follow-up email."
question\_text: "Write instructions for AI to generate (1) a recap with Decisions (bold) + Actions (owner + due date placeholder) + Items to confirm, and (2) a client email that avoids sensitive details."
scoring rubric criteria:

* "Includes decisions/actions/items-to-confirm structure": max 1
* "Separates internal vs client-facing outputs": max 1
* "Adds constraint against invented facts/commitments": max 1
* "Adds a verification gate/checklist before sending": max 1

Item 3 — type: micro\_task
Tests: correcting a risky ‘send without review’ behavior
scenario\_text: "A learner says: ‘I’ll just send the auto-recap to save time.’"
question\_text: "Write one sentence explaining the risk and the minimum review step they must do."
scoring rubric criteria:

* "States risk of hallucinated decisions/owners or privacy breach": max 1
* "Requires checking decisions, owners, dates, product claims": max 1
* "Mentions separating client vs internal detail": max 1
* "Emphasizes accountability (RM owns accuracy)": max 1

***

# SECTION G — Evaluation Item Seeds (28 items: 4 per course × 7 courses)

### Evaluation: Course 1

Item 1 — type: mcq, sequence: 1
question\_text: "What does SAFE most directly help you do?"
options: A) Write longer prompts | B) Remove risk while keeping prompts useful | C) Avoid using AI entirely | D) Replace CRM updates
correct\_option: B
explanation: "SAFE is a method for abstracting sensitive inputs so you can still get useful AI help without exposing non-public data."

Item 2 — type: mcq, sequence: 2
question\_text: "Which is the best SAFE abstraction of ‘Client revenue is $47.3M and EBITDA margin is 12.8%’?"
options: A) Keep the exact numbers but remove the client name | B) ‘Mid-market exporter with stable profitability’ | C) ‘A company with $47M revenue’ | D) Paste the financial statement instead
correct\_option: B
explanation: "SAFE removes exact sensitive figures and keeps directional context that is still useful for drafting questions and briefs."

Item 3 — type: mcq, sequence: 3
question\_text: "What is a common re-identification trap?"
options: A) Using bullet points | B) Removing all context | C) Leaving a unique project/location detail that reveals the client | D) Asking for a shorter output
correct\_option: C
explanation: "Even without a name, unique descriptors can still identify the client, so they must be abstracted too."

Item 4 — type: performance\_task, sequence: 4
question\_text: "Scenario: You receive a confidential client package (financials + expansion plan). Write a SAFE-abstracted prompt that generates a 1-page internal briefing note with (1) risk themes to investigate, (2) questions for the client, and (3) next steps. Include constraints to avoid invented facts and to label unknowns."
scoring rubric:
key1: "Prompt removes identifiers and exact sensitive figures; avoids re-identifying uniqueness"
key2: "Prompt focuses on decision/use (briefing note) rather than pasting raw content"
key3: "Prompt includes constraints against invention and requires labeling uncertainty"
key4: "Prompt specifies a clear output format (sections + bullets/length)"

***

### Evaluation: Course 2

Item 1 — type: mcq, sequence: 1
question\_text: "In CRAF, which element most directly controls the structure of the output?"
options: A) Context | B) Role | C) Action | D) Format
correct\_option: D
explanation: "Format tells the AI how to lay out the answer (sections, bullets, word count, bilingual structure)."

Item 2 — type: mcq, sequence: 2
question\_text: "Your outreach draft sounds generic. Which change is most effective?"
options: A) Add a friendly emoji | B) Add specific context and constraints while avoiding invented facts | C) Remove the role instruction | D) Ask for ‘something better’
correct\_option: B
explanation: "Specific context + constraints increases relevance without hallucinating company-specific claims."

Item 3 — type: mcq, sequence: 3
question\_text: "Which constraint best prevents overpromising?"
options: A) ‘Sound enthusiastic’ | B) ‘Assume the client will buy’ | C) ‘Do not promise approvals; keep product claims general and accurate’ | D) ‘Make it 500 words’
correct\_option: C
explanation: "A direct constraint protects accuracy and compliance in client-facing messages."

Item 4 — type: performance\_task, sequence: 4
question\_text: "Scenario: New lead with minimal info (sector + exporter). Write a complete CRAF prompt to produce (1) a 120-word outreach email and (2) 5 discovery questions. Include constraints for accuracy, no invented facts, and a clear format."
scoring rubric:
key1: "Context is realistic and specific without inventing company facts"
key2: "Role matches RM/EDC voice and audience"
key3: "Action specifies both deliverables with limits (word count/question count)"
key4: "Format is explicit (email structure + bullet questions + constraints)"

***

### Evaluation: Course 3

Item 1 — type: mcq, sequence: 1
question\_text: "In VERIFY, what comes first?"
options: A) Your judgment | B) Validate figures | C) Flag uncertainty | D) Review assumptions
correct\_option: B
explanation: "You validate figures first so the rest of the interpretation is built on correct inputs."

Item 2 — type: mcq, sequence: 2
question\_text: "AI claims a variance driver that isn’t in your data. What should you do?"
options: A) Leave it; it sounds plausible | B) Remove it or label it ‘needs confirmation’ | C) Make the story stronger by adding more drivers | D) Send it to underwriting quickly
correct\_option: B
explanation: "Unverifiable drivers must be removed or clearly flagged to avoid misinformation."

Item 3 — type: mcq, sequence: 3
question\_text: "Which prompt addition best reduces hallucination in numeric commentary?"
options: A) ‘Use a confident tone’ | B) ‘Include calculation steps and label assumptions vs confirmed facts’ | C) ‘Make it longer’ | D) ‘Add jokes’
correct\_option: B
explanation: "Requesting traceability and labeling uncertainty forces the AI to be more disciplined and makes review easier."

Item 4 — type: performance\_task, sequence: 4
question\_text: "Scenario: You used AI to draft a variance explanation. Write a revised prompt that forces (1) calculation traceability in plain language, (2) separation of confirmed vs assumed, (3) a short list of open questions, and (4) a 6-bullet maximum output."
scoring rubric:
key1: "Requires explicit traceability or calculation logic"
key2: "Forces confirmed vs assumed labeling and avoids added data"
key3: "Includes open questions/uncertainty handling"
key4: "Constrains format tightly (6 bullets max + sections)"

***

### Evaluation: Course 4

Item 1 — type: mcq, sequence: 1
question\_text: "What is the biggest risk of using AI for relationship briefs?"
options: A) Too many headings | B) Hallucinated issues or commitments | C) Too few bullets | D) Too formal tone
correct\_option: B
explanation: "Invented relationship claims can damage trust and misdirect meeting strategy."

Item 2 — type: mcq, sequence: 2
question\_text: "In RELATE, what does ‘E—Evidence tagging’ do?"
options: A) Makes the brief longer | B) Forces claims to be labeled as confirmed vs needs confirmation | C) Adds marketing language | D) Sets meeting duration
correct\_option: B
explanation: "Evidence tagging keeps the brief honest and tells you what to verify before using it."

Item 3 — type: mcq, sequence: 3
question\_text: "A new CFO is joining the quarterly review. What prompt change helps most?"
options: A) Ask for more enthusiasm | B) Add a CFO onboarding summary section (status, pending, decisions needed) | C) Remove stakeholder details | D) Ask for 2 pages instead of 1
correct\_option: B
explanation: "A CFO needs a crisp status recap and decision framing, not only history."

Item 4 — type: performance\_task, sequence: 4
question\_text: "Scenario: Quarterly review with a client + new CFO. Write a RELATE-based prompt that produces a 1-page relationship brief with timeline, open threads, stakeholders, agenda, and evidence tags (confirmed vs needs confirmation). Include a constraint against inventing issues."
scoring rubric:
key1: "Includes RELATE sections and a CFO onboarding mini-section"
key2: "Requires evidence tagging per claim/bullet"
key3: "Adds constraints against invented issues/commitments"
key4: "Specifies crisp 1-page format (headings + bullets/limits)"

***

### Evaluation: Course 5

Item 1 — type: mcq, sequence: 1
question\_text: "Which is a ‘signal’ that should trigger action in pipeline review?"
options: A) A lead highlighted as over SLA | B) A nice-looking chart | C) A vague market rumor | D) An email you haven’t read
correct\_option: A
explanation: "Over-SLA leads are explicit cues that follow-up is required."

Item 2 — type: mcq, sequence: 2
question\_text: "In SIGNAL, what does ‘G—Ground with context’ mean?"
options: A) Ignore your relationship knowledge | B) Add what you know (constraints, sensitivities) before final prioritization | C) Ask for more charts | D) Let AI decide
correct\_option: B
explanation: "Grounding prevents automated prioritization from ignoring real-world relationship and capacity constraints."

Item 3 — type: mcq, sequence: 3
question\_text: "What makes a prioritized list ‘defensible’ in a huddle?"
options: A) It’s long | B) It has a rationale tied to a signal and a next action | C) It uses fancy language | D) It avoids deadlines
correct\_option: B
explanation: "A defensible list connects each priority to a signal, meaning, and concrete next action."

Item 4 — type: performance\_task, sequence: 4
question\_text: "Scenario: You see over-SLA leads and aging qualified leads in your dashboard. Write a prompt that asks AI to produce a top-10 priority list using SIGNAL (signal → meaning → context → next action → timing → rationale) and includes a human override step."
scoring rubric:
key1: "Requests SIGNAL-structured output for each item"
key2: "Requires rationale grounded in dashboard cues; avoids invented metrics"
key3: "Includes a human override/context insertion step"
key4: "Outputs actionable next steps with timing (this week) and clear ‘done’ criteria"

***

### Evaluation: Course 6

Item 1 — type: mcq, sequence: 1
question\_text: "What is the core idea of the Copilot Surface Selector?"
options: A) Always start in PowerPoint | B) Start where the best input lives, then chain outputs to where action happens | C) Use only one tool forever | D) Skip review to save time
correct\_option: B
explanation: "Surface selection is about choosing the best starting point for the input and then chaining outputs through the workflow."

Item 2 — type: mcq, sequence: 2
question\_text: "Which recap element most reduces confusion after a meeting?"
options: A) A long paragraph | B) Clear actions with owner + due date placeholder | C) More adjectives | D) Emojis
correct\_option: B
explanation: "Owners and due-date placeholders make accountability clear and reduce rework."

Item 3 — type: mcq, sequence: 3
question\_text: "What is the minimum ‘verification gate’ before sending a client follow-up drafted by AI?"
options: A) Check font size | B) Check decisions, owners, dates, and product claims for accuracy | C) Add more enthusiasm | D) Make it longer
correct\_option: B
explanation: "Verification protects accuracy and prevents accidental misinformation or overpromising."

Item 4 — type: performance\_task, sequence: 4
question\_text: "Scenario: You finished a client call and need (1) recap with decisions/actions and (2) a client follow-up email. Write a Copilot Surface Selector chain plan and include prompt constraints that prevent invented facts, separate internal vs client detail, and add a record governance checklist."
scoring rubric:
key1: "Selects an appropriate starting surface based on the input (meeting) and defines outputs"
key2: "Separates client-facing vs internal detail with explicit constraints"
key3: "Includes a verification gate (decisions/owners/dates/product claims)"
key4: "Adds record governance checklist for log-ready actions and accountability"

***

### Evaluation: Course 7

Item 1 — type: mcq, sequence: 1
question\_text: "What is the biggest risk of an end-to-end AI workflow?"
options: A) Too many templates | B) Compound error (one hallucination propagates into emails and records) | C) Too many bullets | D) Too short outputs
correct\_option: B
explanation: "If you don’t verify at each step, a small error can spread across outputs and become ‘official’."

Item 2 — type: mcq, sequence: 2
question\_text: "Which order best reflects a safe end-to-end workflow?"
options: A) Send email → verify → abstract | B) Abstract (SAFE) → prompt (CRAF) → verify (VERIFY) → communicate (surface chain) | C) Prompt → send → log | D) Skip abstraction to save time
correct\_option: B
explanation: "SAFE first protects inputs, then CRAF produces usable drafts, VERIFY ensures accuracy, and the surface chain executes communication and record updates."

Item 3 — type: mcq, sequence: 3
question\_text: "What is a ‘human override’ in this context?"
options: A) Letting AI decide faster | B) Inserting relationship context and judgment before final decisions or sending | C) Removing constraints | D) Making outputs longer
correct\_option: B
explanation: "Human override ensures AI suggestions are adjusted for real relationship nuance and constraints."

Item 4 — type: performance\_task, sequence: 4
question\_text: "Scenario: You’re pursuing a high-potential exporter. Create an end-to-end prompt/workflow plan that demonstrates SAFE abstraction, a CRAF prompt for outreach + meeting brief, embedded VERIFY checks, and a Copilot Surface Selector chain that ends in (1) client email, (2) internal summary, and (3) record-ready action list. Include constraints to avoid invented facts and sensitive leakage."
scoring rubric:
key1: "Demonstrates SAFE abstraction (no identifiers/sensitive figures; avoids re-identification)"
key2: "Includes a complete CRAF prompt with clear deliverables and strict format"
key3: "Embeds VERIFY checks (confirmed vs assumed, numbers/commitments/product claims) before sending/logging"
key4: "Defines a multi-step surface chain with separation of client/internal outputs and record governance"

***

**Grounding note (what this brief is based on):** Role workflows, tools, compliance constraints, and the Task 3 course anchors are grounded in
