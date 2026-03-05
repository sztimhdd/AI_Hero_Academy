## MACHINE-READABLE HEADER

role\_prefix: uw

company\_map:
course\_1: Bayfield Composites Ltd.
course\_2: Northshore Windworks Inc.
course\_3: HarborGate Foods Ltd.
course\_4: Seabright Equipment Brokers Ltd.
course\_5: AtlasForge Machinery Ltd.
course\_6: PrairiePulse Exporters Inc.
course\_7: Cascadia Marine Systems Ltd.

framework\_names:
NOTE: These names are standardized across all roles where possible. Confirm which apply;
adapt the role-specific examples in SECTION E (concept\_text, good\_example, anti\_pattern)
accordingly. Do NOT invent new framework names unless a standardized name genuinely does
not fit.

*   The SAFE Abstraction Method
*   CRAF Framework
*   VERIFY Checklist
*   RELATE Framework (Review history, Extract concerns, Label stakeholders, Anticipate objections, Tailor response, Escalate wisely)
*   SIFT Variance Lens (Select variances, Isolate drivers, Forecast implications, Tie to risk appetite & next action)
*   Copilot Surface Selector
*   End-to-End AI Workflow

real\_use\_case:
course\_1: The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada).
course\_2: Use Generative AI to assist financial statements reporting
course\_3: UW Streamlining
course\_4: Customer Interaction Recap
course\_5: Financial Variance Analyzer
course\_6: Request for Customer Care Team
course\_7: Explore Copilot 360 Option for the Credit Insurance Program; Use Gen-AI to help provide company assessments. This is not a net new idea, but an attempt to leverage external tools - either CB Insights or Alphasense - as a search engine (which may themselves leverage AI) to help with investments due diligence

***

# SECTION A — Role Entry

role\_id: uw  
title: Underwriter  
description: "Assesses credit risk and structures financing or insurance decisions by analysing sensitive financial information, internal risk ratings, and policy constraints. Produces credit submissions/credit memos, records decisions in underwriting systems, and coordinates approvals within Delegation of Authority limits. Works closely with Business Development/Account Managers, Risk Management Office analysts, Legal, ESG/E\&S specialists, and Underwriting Operations to move transactions from intake through approval, documentation, and customer communication." [\[m365.cloud.microsoft\]]

***

# SECTION B — All 6 Domain Specs

### Domain: responsible\_ai

domain\_id: responsible\_ai  
title: Responsible AI  
description: "Applying EDC’s Responsible Use of Generative AI Policy before using AI tools in underwriting work. This includes identifying Non‑Public EDC Information (client financials, internal risk ratings, deal terms), using safe abstraction when prompting, and ensuring AI use aligns with audit/record expectations and tool approvals."   
level\_0\_label: Unaware  
level\_0\_descriptor: "Does not distinguish public vs non-public underwriting information. May paste raw borrower financial statements, CIS buyer-file text, or internal ratings into non-approved AI tools or personal accounts."   
level\_1\_label: Explorer  
level\_1\_descriptor: "Knows the rule (‘don’t share non-public info’) but struggles with real underwriting edge cases—e.g., whether a risk rating, covenant headroom, or internal rationale counts as non-public. Redaction is inconsistent or removes too much to be useful."   
level\_2\_label: Practitioner  
level\_2\_descriptor: "Consistently applies safe abstraction: removes names, IDs, exact figures, and deal-identifying details while preserving underwriting logic. Uses EDC-approved tools/surfaces and avoids exposing CIS/MBC/FACT content in unapproved contexts."   
level\_3\_label: Proficient  
level\_3\_descriptor: "Handles borderline cases confidently (e.g., internal risk outlook commentary, ‘confidential’ buyer-file notes, sanctions-related details). Rewrites prompts to preserve utility while removing risk, and adds explicit constraints (no guessing, cite sources, don’t invent figures)."   
level\_4\_label: Champion  
level\_4\_descriptor: "Proactively identifies new compliance risks in emerging workflows (e.g., summarizing long credit papers, using external research tools) and teaches safe patterns. Creates team-ready prompt templates/checklists that align with policy and audit expectations." [\[m365.cloud.microsoft\]], [\[Responsibl...AI Policy \| PDF\]] [\[m365.cloud.microsoft\]] [\[m365.cloud.microsoft\]], [\[Responsibl...AI Policy \| PDF\]], [\[08b. MBC -...rigination \| PowerPoint\]], [\[Applicatio...Book FACT \| Word\]] [\[m365.cloud.microsoft\]], [\[Credit Doc...ion in CIS \| Word\]], [\[Responsibl...AI Policy \| PDF\]] [\[m365.cloud.microsoft\]], [\[Responsibl...AI Policy \| PDF\]], [\[Re: Inquir...io Rollout \| Outlook\]]

***

### Domain: strategic\_prompting

domain\_id: strategic\_prompting  
title: Strategic Prompting  
description: "Structuring prompts so AI outputs are directly usable in underwriting artifacts—credit memo sections in Word, ratio/variance narratives from Excel, issue lists for approvals, and structured summaries for CIS/MBC notes—without turning into generic finance text."   
level\_0\_label: Unaware  
level\_0\_descriptor: "Has not used prompting for underwriting tasks or can’t explain what makes an effective prompt beyond ‘summarize this’."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Writes basic prompts. Output is often generic, misses underwriting-relevant sections (risk mitigants, conditions, rationale), or is too long/too shallow to paste into a credit submission."   
level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses a structured prompt (context + constraints + required sections). Produces a credit analysis narrative that fits the underwriting template with minor edits and includes explicit ‘don’t invent’ and ‘flag uncertainties’ instructions."   
level\_3\_label: Proficient  
level\_3\_descriptor: "Adapts prompts for complex deals (multi-tranche structures, unusual collateral, policy exceptions). Iterates quickly: adds missing risk factors, forces table outputs, and requests traceable reasoning aligned to the credit memo format."   
level\_4\_label: Champion  
level\_4\_descriptor: "Builds reusable prompt templates for recurring underwriting workflows (financial statement write-ups, covenant drafting, approval-briefs). Coaches colleagues and documents examples in a shared team space." [\[m365.cloud.microsoft\]] [\[m365.cloud.microsoft\]], [\[08b. MBC -...rigination \| PowerPoint\]]

***

### Domain: critical\_eval

domain\_id: critical\_eval  
title: Critical Evaluation  
description: "Critically reviewing AI outputs before using them in credit decisions or records—catching invented figures, wrong ratios, misread covenants, incorrect policy claims, or missing red flags in summaries of financials, risk ratings, and credit submissions."   
level\_0\_label: Unaware  
level\_0\_descriptor: "Treats AI output as accurate by default. Copies AI text into a credit memo or CIS/MBC notes without checking against source documents."   
level\_1\_label: Explorer  
level\_1\_descriptor: "Skims outputs for obvious errors but does not systematically verify. May miss plausible-but-wrong details (e.g., swapped years, misstated leverage, misclassified covenant)."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Routinely verifies AI output against originals (financial statements, model outputs, credit reports, policy excerpts). Removes unverifiable claims and recalculates any key ratios that would influence the recommendation."   
level\_3\_label: Proficient  
level\_3\_descriptor: "Uses a repeatable verification checklist and prompt constraints (cite, quote, ‘unknown if not present’). Detects subtle failure modes like ‘false certainty’ and incomplete risk coverage."  
level\_4\_label: Champion  
level\_4\_descriptor: "Creates team verification standards for AI-assisted underwriting (what must be recalculated, what must be cross-checked in system-of-record). Teaches peers how to reduce hallucinations through better prompting and sourcing discipline." [\[m365.cloud.microsoft\]]

***

### Domain: relationship\_intel

domain\_id: relationship\_intel  
title: Relationship Intelligence  
description: "Using AI to synthesize stakeholder context and interaction history—policyholder/broker communications, internal deal-team threads, and prior decisions—so responses and follow-ups are specific, empathetic, and consistent with what was previously communicated (without revealing confidential internal rationale)."   
level\_0\_label: Unaware  
level\_0\_descriptor: "Does not use AI to prepare for sensitive customer interactions. Replies reactively, relying on memory and templates without tailoring."   
level\_1\_label: Explorer  
level\_1\_descriptor: "Uses AI to draft replies but outputs are generic, overly apologetic, or too technical. Misses the customer’s actual concern and may omit the concrete next step needed to move the case forward."   
level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses AI to extract key concerns, summarize the history, and draft a tailored response that balances clarity, empathy, and policy consistency. Ensures the message avoids internal-only details and aligns with approved template language where appropriate."   
level\_3\_label: Proficient  
level\_3\_descriptor: "Anticipates objections and selects the right level of detail for the audience (policyholder vs broker vs internal AM). Uses AI to propose options/alternatives and to keep tone steady under pressure, then edits for precision and compliance."   
level\_4\_label: Champion  
level\_4\_descriptor: "Develops ‘relationship playbooks’ for high-friction scenarios (declines, reductions, sanctions-related constraints) and shares prompt patterns for consistent stakeholder management across the team." [\[m365.cloud.microsoft\]], [\[Underwrite...Templates \| Word\]] [\[Underwrite...Templates \| Word\]] [\[Underwrite...Templates \| Word\]], [\[Responsibl...AI Policy \| PDF\]] [\[Underwrite...Templates \| Word\]], [\[Russia - S...uideline_e \| Word\]]

***

### Domain: data\_decision

domain\_id: data\_decision  
title: Data-Driven Decision Making  
description: "Using AI to interpret financial and portfolio signals (variance analysis, early-warning dashboards, risk-rating outputs) to support underwriting decisions—while understanding data gaps, model limits, and when to escalate or request more information."   
level\_0\_label: Unaware  
level\_0\_descriptor: "Does not use AI to support analysis or prioritization. Relies on manual review and intuition without structuring the decision logic."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Uses AI for summaries but doesn’t connect outputs to a decision (approve/decline/conditions). May accept AI’s prioritization without validating inputs or understanding assumptions."   
level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses AI to identify key drivers (YoY variances, leverage changes, working capital shifts) and ties them to concrete underwriting actions (ask for clarifications, adjust terms, escalate). Validates against source data and policy limits."   
level\_3\_label: Proficient  
level\_3\_descriptor: "Designs multi-factor queries (sector + country risk + exposure concentration + covenant trajectory). Uses AI to stress-test assumptions and propose mitigants, then confirms with system-of-record data and specialist input."   
level\_4\_label: Champion  
level\_4\_descriptor: "Builds team templates for portfolio reviews and variance narratives. Shares decision heuristics that clarify when AI signals are ‘noise’ vs ‘actionable’ and helps peers avoid overconfidence in model-driven output." [\[m365.cloud.microsoft\]]

***

### Domain: augmented\_comm

domain\_id: augmented\_comm  
title: Augmented Communication  
description: "Choosing the right M365 Copilot surface (Outlook, Teams, Word, Excel, SharePoint/OneNote) and linking them into underwriting workflows—e.g., Teams recap → credit memo section in Word → decision email in Outlook → record update in CIS/MBC—while keeping the audit trail clean."   
level\_0\_label: Unaware  
level\_0\_descriptor: "Has not used Copilot features across M365 tools or does not know which surfaces are best for which underwriting tasks."   
level\_1\_label: Explorer  
level\_1\_descriptor: "Uses a single Copilot feature (often email drafting) but doesn’t connect outputs across tools. Re-enters the same info manually in multiple places."   
level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses at least three surfaces for underwriting communications and documentation (e.g., Excel → Word → Outlook). Builds a simple chain workflow and retains traceability (what came from where, what was verified)."   
level\_3\_label: Proficient  
level\_3\_descriptor: "Designs multi-step workflows across 3+ surfaces, choosing the best entry point based on input type (tables vs long text vs threads). Recovers gracefully when a step produces weak output and knows when to stop using AI and switch to manual."   
level\_4\_label: Champion  
level\_4\_descriptor: "Documents and shares ‘standard chains’ for common underwriting scenarios (urgent decision, committee pack, customer-care request). Helps the team reduce duplicate work and improve consistency without compromising confidentiality." [\[m365.cloud.microsoft\]], [\[08b. MBC -...rigination \| PowerPoint\]] [\[m365.cloud.microsoft\]] [\[m365.cloud.microsoft\]], [\[Underwrite...Templates \| Word\]]

***

# SECTION C — All 7 Course Specs

### Course 1 — Safe AI with Confidential Deal Data

course\_id: uw\_c1\_responsible\_ai  
role\_id: uw  
primary\_domain: responsible\_ai  
sequence\_order: 1  
title: "Safe AI with Confidential Deal Data"  
tagline: "Use the SAFE Abstraction Method to get AI help without leaking non-public underwriting information."  
description: "Underwriters handle highly sensitive financials and internal risk rationale. This course builds practical judgment for what can and cannot go into AI tools, and teaches SAFE Abstraction so learners can still get useful output while staying policy-safe and audit-ready."   
real\_use\_case: "The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada)." [\[m365.cloud.microsoft\]], [\[Responsibl...AI Policy \| PDF\]] [\[m365.cloud.microsoft\]]

### Course 2 — Prompting AI for Financial Analysis Write‑Ups

course\_id: uw\_c2\_strategic\_prompting  
role\_id: uw  
primary\_domain: strategic\_prompting  
sequence\_order: 2  
title: "Prompting AI for Financial Analysis Write‑Ups"  
tagline: "Turn messy financial inputs into a clean credit narrative using the CRAF framework."  
description: "Financial analysis write-ups are repetitive but high stakes. This course teaches structured prompting (CRAF) to produce underwriting-ready narratives from Excel tables and statement excerpts—focused on the risk story, not generic finance commentary."   
real\_use\_case: "Use Generative AI to assist financial statements reporting" [\[m365.cloud.microsoft\]]

### Course 3 — Let AI Read the Fine Print (Then Double‑Check It)

course\_id: uw\_c3\_critical\_eval  
role\_id: uw  
primary\_domain: critical\_eval  
sequence\_order: 3  
title: "Let AI Read the Fine Print (Then Double‑Check It)"  
tagline: "Use the VERIFY checklist to catch AI mistakes before they enter a credit decision or system-of-record."  
description: "AI can accelerate reading long submissions, reports, and decision histories—but it can also invent details. This course teaches a disciplined verification workflow (VERIFY) so underwriters can benefit from speed without sacrificing accuracy or policy alignment."   
real\_use\_case: "UW Streamlining" [\[m365.cloud.microsoft\]]

### Course 4 — Using AI to Deepen Client Insight and Rapport

course\_id: uw\_c4\_relationship\_intel  
role\_id: uw  
primary\_domain: relationship\_intel  
sequence\_order: 4  
title: "Using AI to Deepen Client Insight and Rapport"  
tagline: "Use RELATE to respond to high-friction stakeholders with precision, empathy, and consistency."  
description: "Underwriters regularly communicate declines, reductions, and information requests. This course shows how to use AI to synthesize interaction history and draft responses that protect the relationship—without revealing internal-only rationale or drifting from standard wording."   
real\_use\_case: "Customer Interaction Recap" [\[Underwrite...Templates \| Word\]], [\[Responsibl...AI Policy \| PDF\]] [\[m365.cloud.microsoft\]]

### Course 5 — Uncovering Financial Trends with AI Insights

course\_id: uw\_c5\_data\_decision  
role\_id: uw  
primary\_domain: data\_decision  
sequence\_order: 5  
title: "Uncovering Financial Trends with AI Insights"  
tagline: "Use SIFT to convert variance analysis into a clear underwriting action plan."  
description: "Variance analysis is everywhere in underwriting—yet it often becomes a wall of numbers. This course teaches underwriters to use AI to identify the few variances that matter, explain drivers, forecast implications, and tie insights to a concrete decision or next step."   
real\_use\_case: "Financial Variance Analyzer" [\[m365.cloud.microsoft\]]

### Course 6 — AI as Your Email and Message Drafting Partner

course\_id: uw\_c6\_augmented\_comm  
role\_id: uw  
primary\_domain: augmented\_comm  
sequence\_order: 6  
title: "AI as Your Email and Message Drafting Partner"  
tagline: "Pick the right Copilot surface and chain it end-to-end: recap → memo → decision email → record update."  
description: "Underwriters work across Outlook, Word, Teams, Excel, and SharePoint/OneNote while also updating underwriting systems. This course teaches the Copilot Surface Selector and multi-step workflows that reduce rework and improve consistency—while keeping records accurate and compliant."   
real\_use\_case: "Request for Customer Care Team" [\[m365.cloud.microsoft\]], [\[08b. MBC -...rigination \| PowerPoint\]] [\[m365.cloud.microsoft\]]

### Course 7 — End‑to‑End Underwriting with AI (From Analysis to Approval)

course\_id: uw\_c7\_capstone  
role\_id: uw  
primary\_domain: augmented\_comm  
sequence\_order: 7  
title: "End‑to‑End Underwriting with AI (From Analysis to Approval)"  
tagline: "Run a complete underwriting workflow using all 6 domains—fast, safe, and verifiable."  
description: "This capstone integrates Responsible AI, Strategic Prompting, Critical Evaluation, Relationship Intelligence, Data-Driven Decision Making, and Augmented Communication in one realistic underwriting case. Learners will move from intake → analysis → recommendation → approval support → stakeholder communication, using AI safely and transparently at each step."   
real\_use\_case: "Explore Copilot 360 Option for the Credit Insurance Program; Use Gen-AI to help provide company assessments. This is not a net new idea, but an attempt to leverage external tools - either CB Insights or Alphasense - as a search engine (which may themselves leverage AI) to help with investments due diligence" [\[m365.cloud.microsoft\]]

***

# SECTION D — All 7 Scenario Seeds

### Course 1 Scenario

scenario\_text: "You receive an urgent request to assess a new transaction for <Company>Bayfield Composites Ltd.</Company>. The package includes a confidential financial model, internal risk notes, and draft terms. The deal team wants a quick risk summary to decide whether to escalate for approval today. You want AI help—but the fastest path (pasting the whole package into a general AI chat) could violate policy and create an audit problem."  
task\_1\_text: "Write a SAFE Abstraction plan: list the exact elements you must remove or generalize before using AI (names, identifiers, exact figures, deal terms), and what safe placeholders you will use instead."  
task\_2\_text: "Draft a policy-safe prompt that asks for a risk summary and key mitigants using only your abstracted inputs (no client identifiers, no exact numbers). Include an explicit constraint: ‘If a detail is not provided, say UNKNOWN.’"  
task\_3\_text: "Your draft prompt still contains one ‘deal fingerprint’ (a detail that would let someone infer the client or transaction). Identify what it is and rewrite that part to preserve usefulness while removing traceability."  
task\_4\_text: "You need to share the AI output with an internal approver. Add a final instruction to your workflow that ensures the output is (a) verified, (b) appropriately attributed, and (c) safe to paste into a credit memo draft."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters. The learner is practicing Responsible AI using the SAFE Abstraction Method. Guide them by asking questions and prompting reflection—do not write the plan or prompt for them. Watch for red flags: real company names, exact financial figures, internal system IDs (CIS buyer IDs, MBC transaction numbers), internal ratings, covenant details, or copied text from confidential documents. If sensitive content appears, instruct the learner to remove/abstract it and explain why."

### Course 2 Scenario

scenario\_text: "You are drafting the financial analysis section for <Company>Northshore Windworks Inc.</Company> using an Excel table of key metrics (revenue, EBITDA, leverage, liquidity) and brief notes from the deal team. You want Copilot to generate a tight underwriting narrative that fits your credit memo structure. The temptation is to write ‘write the financial section’ and accept a generic answer that misses the real risks."  
task\_1\_text: "Write a CRAF prompt to produce a 250-word financial analysis narrative with three headings: Performance, Liquidity, Leverage. Include constraints: no invented numbers, highlight only the top 3 risks."  
task\_2\_text: "Your output is accurate but reads like a textbook. Revise the Role and Action so the narrative is written in an underwriter voice and explicitly ties changes to underwriting implications (e.g., covenants, conditions, mitigants)."  
task\_3\_text: "The deal team cares most about liquidity runway and working capital volatility. Revise the Format instruction so the output starts with a 3-bullet ‘So what?’ section before the headings."  
task\_4\_text: "The AI included a recommendation (‘approve’) even though you only asked for analysis. Add a constraint that prevents decision recommendations and forces the AI to separate facts from interpretations."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing the CRAF Framework. Guide the learner with questions—do not write the prompt. Look for missing CRAF elements, vague instructions, or prompts that invite hallucinations. Flag any sensitive info (client identifiers, exact figures, internal ratings). Encourage constraints like ‘use only provided data’ and ‘say UNKNOWN if missing.’"

### Course 3 Scenario

scenario\_text: "An internal AI tool generates a summary of a third-party submission for <Company>HarborGate Foods Ltd.</Company>, including key risks, ratios, and suggested mitigants. The summary looks polished, and you’re under time pressure to send an update to the approving authority. The temptation is to forward it as-is—even if it contains subtle errors that could mislead the decision."  
task\_1\_text: "Apply the VERIFY checklist: list the minimum source items you must check (financial statements, covenant definitions, ratings output, policy constraint) before using the summary."  
task\_2\_text: "Identify two statements in the AI summary that are ‘high impact if wrong’ and rewrite them as ‘verified facts’ vs ‘needs confirmation’ (without adding new data)."  
task\_3\_text: "Your check finds one ratio was miscalculated due to a year mismatch. Write a short instruction you would add to future prompts to reduce this failure mode."  
task\_4\_text: "Draft a one-paragraph approver update that uses only VERIFIED items and clearly labels anything pending, while maintaining a professional underwriting tone."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing Critical Evaluation with the VERIFY checklist. Do not fix the work for the learner. Ask what they would verify first and why. Watch for over-trust (‘looks right’), invented figures, and missing sourcing. If they include sensitive or real data, instruct them to abstract it."

### Course 4 Scenario

scenario\_text: "<Company>Seabright Equipment Brokers Ltd.</Company> sends an angry email claiming EDC ‘declined without reading the file’ after a credit limit reduction. Internally, you also have a Teams thread showing previous back-and-forth and the exact info that was missing. The temptation is to paste the whole thread into AI and send a generic apology. The skill test is to synthesize the history, keep tone calm, and give a precise next step—without leaking internal-only rationale."  
task\_1\_text: "Write a prompt that asks AI to summarize the interaction history into three parts: Customer concern, What we communicated, What we still need. Use only abstracted content (no internal names, no sensitive buyer-file text)."  
task\_2\_text: "Using the RELATE framework, write a prompt instruction that forces the AI to acknowledge emotion without admitting fault, and to propose 2 specific next-step options (information request vs alternative structure)."  
task\_3\_text: "The draft response is too technical. Revise the prompt so the response is written for a time-pressed customer, using plain language and one short paragraph + bullet list."  
task\_4\_text: "Add a guardrail to prevent the AI from referencing internal systems, internal risk codes, or internal committees in the customer-facing draft."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing Relationship Intelligence using RELATE. Guide with questions—do not write the email. Watch for: blaming language, over-disclosure of internal rationale, mention of internal codes (e.g., reason codes, risk levels), or sharing non-public data. Encourage empathy + clarity + next steps, and strict separation of internal vs external content."

### Course 5 Scenario

scenario\_text: "You are reviewing <Company>AtlasForge Machinery Ltd.</Company> and notice large year-over-year swings in margin and working capital in the financials. You want AI to help explain variances quickly, but the temptation is to accept the first explanation (which might be generic or wrong) and let it drive your decision. The skill test is to use AI to surface hypotheses, then validate and tie to a concrete underwriting action."  
task\_1\_text: "Write a prompt that applies SIFT: ask AI to select the top 5 variances, isolate likely drivers (as hypotheses), and list what evidence you’d need to confirm each driver."  
task\_2\_text: "Revise the prompt so AI must output: (a) variance table, (b) driver hypotheses, (c) underwriting implications, (d) next info request—each clearly separated."  
task\_3\_text: "The AI suggests a driver that is not supported by the provided numbers. Write the micro-instruction you would add to force ‘evidence-backed only’ reasoning."  
task\_4\_text: "Produce an action plan: 3 questions to the deal team, 2 mitigants to consider, and 1 escalation trigger—based only on verified variances."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing Data-Driven Decision Making with SIFT. Do not produce the analysis for the learner. Push them to separate hypotheses from facts, and to identify what data would confirm each claim. Flag any prompt content that includes exact client identifiers or confidential figures."

### Course 6 Scenario

scenario\_text: "A Customer Care Team request comes in for <Company>PrairiePulse Exporters Inc.</Company>. You need to (1) confirm the latest decision context, (2) draft a customer response using standard wording where appropriate, (3) update the record in the system-of-record, and (4) notify internal stakeholders. The temptation is to draft everything in one place and forget traceability. The skill test is to choose the right Copilot surface at each step and chain outputs safely."  
task\_1\_text: "Use the Copilot Surface Selector: decide which surface you’ll use for each step (Teams/Outlook/Word/Excel/SharePoint) and why, given the input types (thread, template language, tables, record notes)."  
task\_2\_text: "Draft a Copilot prompt for Outlook that generates a customer email using a ‘calm + clear + next steps’ structure, and explicitly avoids internal-only details."  
task\_3\_text: "Draft a Copilot prompt for Word that turns the verified facts into a short ‘decision rationale’ paragraph suitable for internal documentation (not customer-facing)."  
task\_4\_text: "Design a final ‘handoff’ step: write the checklist you will follow before copying AI text into the system-of-record (verification, confidentiality check, consistency with prior communications)."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing Augmented Communication and tool chaining. Do not write the emails or paragraphs. Watch for mixing internal and external messaging, missing verification, and any inclusion of non-public identifiers. Encourage explicit ‘source-of-truth’ steps and safe abstractions."

### Course 7 Scenario

scenario\_text: "You are leading an end-to-end underwriting case for <Company>Cascadia Marine Systems Ltd.</Company>. You must quickly build a company assessment (including external context), analyze financials and variances, validate risk signals, prepare an approval-ready recommendation, and communicate the decision to stakeholders. The temptation is to let AI ‘run the case’ end-to-end, including pulling in external data without checking quality or permissions. The skill test is to integrate all six domains into one controlled workflow with clear human checkpoints."  
task\_1\_text: "Design the End-to-End AI Workflow: list the 6 domain checkpoints (SAFE, CRAF, VERIFY, RELATE, SIFT, Surface Selector) and what artifact each checkpoint produces."  
task\_2\_text: "Write a prompt sequence (3 prompts) that: (1) creates an abstracted case brief, (2) generates a financial variance narrative, (3) drafts an internal recommendation section—each with constraints preventing invented facts."  
task\_3\_text: "You receive an external ‘company assessment’ summary from a tool. Apply VERIFY: list what you must confirm before using it (sources, recency, contradictions), and write the language you’ll add to your memo to properly qualify it."  
task\_4\_text: "Produce the final stakeholder pack outline: internal approver brief + customer message + record update note. Specify which parts are AI-assisted, what you verified, and what remains assumptions."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters guiding a capstone. Do not write the workflow or prompts for the learner—ask questions that force them to identify checkpoints, constraints, and verification steps. Watch for policy violations (non-public data in prompts, unapproved tool use), over-reliance on external summaries, and unclear separation between facts, assumptions, and recommendations."

***

# SECTION E — All 7 Reading Concept Specs

### Course 1 Reading

framework\_name: "The SAFE Abstraction Method"  
concept\_text: "Underwriting work is packed with non-public information—financial statements, internal risk ratings, covenant headroom, and decision rationale. AI can save time, but only if you keep sensitive data out of prompts and outputs that don’t belong in the record. SAFE is a practical, repeatable method you run before every AI-assisted underwriting task: **S**trip identifiers (names, IDs, deal fingerprints), **A**bstract numbers (replace exact figures with ranges or ratios), **F**ocus the ask (what you need the AI to do, not ‘analyze everything’), and **E**nforce constraints (no guessing, label unknowns, produce a safe format). SAFE is not about making prompts vague—it’s about removing what creates confidentiality risk while preserving what makes underwriting logic useful. If you can’t SAFE the input without losing meaning, that’s a signal to stop and use a different approach (manual analysis or an approved internal workflow)."   
good\_example: "Before: ‘Here is <Company>Bayfield Composites Ltd.</Company>’s full model and internal notes—summarize risk and recommend approval.’ After (SAFE): ‘Context: mid-market manufacturer; recent margin compression; liquidity tight but improving; exposure is material vs peer deals. Action: list top 5 risk themes + 5 mitigants. Constraints: no invented numbers; if missing, say UNKNOWN; output as bullets for an internal draft.’"  
anti\_pattern: "Pasting the full confidential model, internal ratings, and system notes into a general AI chat ‘for speed.’ Consequence: policy breach risk + accidental disclosure + unreliable audit trail."   
takeaway: "SAFE lets you keep AI benefits while protecting confidentiality. If you can’t abstract safely, don’t prompt—change the approach." [\[Responsibl...AI Policy \| PDF\]], [\[m365.cloud.microsoft\]]

### Course 2 Reading

framework\_name: "CRAF Framework"  
concept\_text: "Great underwriting output starts with a prompt that behaves like a mini-brief. CRAF gives you four elements that consistently produce usable drafts: **C—Context** (what case this is, what inputs matter), **R—Role** (who the AI is ‘being’ so tone and vocabulary fit underwriting), **A—Action** (the exact deliverable: a 250-word narrative, a table, a list of risks), **F—Format** (headings, bullets, order, length). In underwriting, missing Action or Format is the most common reason AI produces generic finance text. A good CRAF prompt also includes underwriting guardrails: ‘use only provided data,’ ‘don’t recommend approval,’ ‘label unknowns,’ and ‘separate facts from interpretation.’ This keeps your draft aligned to the credit memo structure and reduces rework."  
good\_example: "Prompt (CRAF): ‘Context: You are drafting the Financial Analysis section for an underwriting memo. Inputs: pasted table of metrics + brief notes. Role: Senior credit underwriter. Action: Write a 250-word narrative focusing on liquidity, leverage, and volatility drivers; highlight top 3 risks. Format: Start with 3 bullets “So what?”, then headings Performance / Liquidity / Leverage. Constraints: do not invent figures; say UNKNOWN if missing; no approval recommendation.’"  
anti\_pattern: "‘Write my credit memo.’ Consequence: generic output that misses the real risk story and wastes time editing."  
takeaway: "In underwriting, CRAF turns AI from a ‘writer’ into a controlled drafting assistant."

### Course 3 Reading

framework\_name: "VERIFY Checklist"  
concept\_text: "Underwriters can’t outsource judgment. AI summaries can be fast—and wrong in ways that look believable. VERIFY is a short checklist you run before any AI text enters a memo, an email, or a system-of-record: **V**alue at risk (what statements would change the decision if wrong?), **E**vidence match (does each key claim map to a source line/table?), **R**ecompute (recalculate critical ratios/variances from source), **I**nconsistencies (scan for contradictions vs other documents or prior decisions), **F**lags missing (what major risk categories are absent?), **Y**our conclusion (what you accept, reject, or mark pending). VERIFY forces you to label uncertainty and prevents ‘false certainty’ from creeping into underwriting decisions."  
good\_example: "After an AI summary flags ‘no liquidity concerns,’ you VERIFY: check the liquidity table, recompute runway months, and if missing, rewrite: ‘Liquidity runway needs confirmation; latest cash + facility availability not provided in the source excerpt.’"  
anti\_pattern: "Forwarding an AI-generated risk review to an approver without checking ratios or covenant definitions. Consequence: approver decisions based on incorrect facts."  
takeaway: "VERIFY is the difference between AI-assisted speed and AI-driven error."

### Course 4 Reading

framework\_name: "RELATE Framework"  
concept\_text: "Relationship intelligence in underwriting is not ‘being friendly’—it’s being precise, consistent, and calm when decisions are sensitive. RELATE helps you use AI without damaging trust: **R**eview history (what was asked, answered, promised), **E**xtract concerns (what the stakeholder is really upset about), **L**abel stakeholders (policyholder, broker, internal AM—each needs different detail), **A**nticipate objections (what they will push back on), **T**ailor response (plain language + specific next step), **E**scalate wisely (when to bring in manager/legal/other specialists). AI can help synthesize threads and propose wording, but you control disclosure: customer-facing messages must avoid internal codes, internal committee language, and non-public rationale."   
good\_example: "Before: ‘Sorry for the inconvenience. We can’t help.’ After (RELATE): ‘We understand this is urgent. Based on the information provided so far, we can’t confirm coverage at the level requested. If you share (1) latest payment experience details and (2) updated buyer financials, we can reassess within X business days. If timing is critical, we can discuss a temporary limit option.’"   
anti\_pattern: "Sending a generic apology drafted by AI that doesn’t answer the actual question or provide the next step. Consequence: escalations, rework, and relationship damage."  
takeaway: "RELATE turns AI drafting into stakeholder trust-building—without over-disclosure." [\[Underwrite...Templates \| Word\]], [\[Responsibl...AI Policy \| PDF\]] [\[Underwrite...Templates \| Word\]]

### Course 5 Reading

framework\_name: "SIFT Variance Lens"  
concept\_text: "Variance analysis becomes valuable only when it drives action. SIFT helps you use AI to move from numbers → drivers → underwriting implications. **S—Select** the few variances that matter (not every line item). **I—Isolate** likely drivers as hypotheses (pricing, volume, FX, one-time events, working capital shifts). **F—Forecast** implications (runway, covenant pressure, refinancing risk). **T—Tie** to risk appetite and the next action (ask for evidence, adjust structure, add conditions, escalate). AI is best at proposing driver hypotheses and structuring the narrative; you are responsible for confirming drivers with evidence and linking them to underwriting decisions."  
good\_example: "Prompt: ‘Given this table, select top 5 variances, propose 2 evidence-based driver hypotheses for each, list what evidence would confirm, and map each to an underwriting implication (covenant risk, liquidity risk, mitigant). Output: variance table + drivers + evidence needed + action.’"  
anti\_pattern: "Accepting the AI’s first driver explanation (‘margin fell due to competition’) without any evidence in the numbers. Consequence: wrong risk story and wrong conditions."  
takeaway: "SIFT keeps AI in the hypothesis lane—and keeps you in the decision lane."

### Course 6 Reading

framework\_name: "Copilot Surface Selector"  
concept\_text: "Underwriting work crosses tools: threads, documents, tables, and formal messages. The Copilot Surface Selector is a simple rule set: start where your **best input** lives, and end where your **official output** must land. Use Outlook Copilot for customer-ready drafts; Word Copilot for memo sections; Excel Copilot for interpreting tables; Teams Copilot for meeting/thread summaries; SharePoint/OneNote Copilot for retrieving prior artifacts. Then chain outputs with a verification step between every hop. The goal is not ‘more AI’—it’s less re-entry, cleaner audit trails, and fewer inconsistent messages."   
good\_example: "Teams recap → Word: draft ‘Risk & Mitigants’ section → Excel: validate ratios → Outlook: draft customer email using approved tone → final human check → record update in system-of-record."   
anti\_pattern: "Drafting the customer email from an internal credit memo paragraph without stripping internal language. Consequence: over-disclosure and confusion."  
takeaway: "Pick the surface that matches the input, then chain deliberately with verification gates." [\[m365.cloud.microsoft\]], [\[08b. MBC -...rigination \| PowerPoint\]] [\[m365.cloud.microsoft\]]

### Course 7 Reading

framework\_name: "End-to-End AI Workflow"  
concept\_text: "In the capstone, AI is not a single prompt—it’s a controlled workflow with checkpoints. Your end-to-end workflow should have (1) SAFE gating before any prompt, (2) CRAF prompting to generate draft artifacts, (3) VERIFY checks before anything becomes ‘official,’ (4) RELATE-driven communication shaping, (5) SIFT-driven decision logic, and (6) Surface Selection to move work across tools without losing traceability. The workflow is successful when every AI-assisted artifact is (a) policy-safe, (b) evidence-linked, and (c) clearly marked as draft vs verified. Your job is to decide where AI accelerates and where human judgment must dominate."  
good\_example: "A 6-step checklist with a ‘stop’ rule: if you can’t verify a critical claim, you either find the source or label it as pending—never let AI fill the gap."  
anti\_pattern: "Letting AI produce a full recommendation, then using it as the decision. Consequence: unmanaged risk and weak defensibility."  
takeaway: "End-to-end value comes from checkpoints, not from bigger prompts."

***

# SECTION F — Diagnostic Item Seeds (18 items: 3 per domain × 6 domains)

### Diagnostic: responsible\_ai

Item 1 — type: mcq  
Tests: identifying Non-Public EDC Information in underwriting prompts  
question\_text: "Which input is most clearly NOT safe to paste into a general AI chat when seeking help drafting an underwriting summary?"  
options: A) Public news article link about the borrower’s sector | B) A de-identified description of the deal (industry + size band + risk themes) | C) Copy/paste of internal risk rating commentary and exact covenant headroom | D) A generic question about how to structure a credit memo section  
correct\_option: C  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: writing a SAFE-abstraction prompt  
scenario\_text: "You have a confidential borrower package and need AI help identifying key risk themes. You cannot include client name, exact figures, or internal system notes."  
question\_text: "Write a prompt that uses SAFE Abstraction to request: top 5 risk themes + 5 mitigants, with ‘UNKNOWN if missing’ guardrail."  
scoring rubric criteria:

*   "Strips identifiers and avoids deal fingerprints": max 1
*   "Abstracts numbers (ranges/ratios) instead of exact figures": max 1
*   "Clear Action deliverable (risk themes + mitigants)": max 1
*   "Includes explicit constraints (no guessing / UNKNOWN)": max 1

Item 3 — type: micro\_task  
Tests: spotting a policy-unsafe detail  
scenario\_text: "Prompt excerpt: ‘Client: Bayfield Composites Ltd. Facility amount: $18.7M CAD. Covenant headroom: 1.2x. Please draft my approval note.’"  
question\_text: "In one sentence, identify the two most sensitive elements and how you would abstract them."  
scoring rubric criteria:

*   "Identifies client name as sensitive": max 1
*   "Identifies exact amount or covenant headroom as sensitive": max 1
*   "Proposes abstraction (industry/size band; ranges/ratios)": max 1
*   "Mentions using approved tools / policy-safe approach": max 1

***

### Diagnostic: strategic\_prompting

Item 1 — type: mcq  
Tests: knowing which CRAF element prevents generic output  
question\_text: "An underwriter’s prompt produces a long generic explanation of financial ratios. Which missing element most likely caused this?"  
options: A) Context | B) Role | C) Action | D) Format  
correct\_option: C  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: writing a complete CRAF prompt  
scenario\_text: "Inputs: a pasted Excel table of revenue, EBITDA, leverage, liquidity; brief notes: ‘margin down, WC volatile, liquidity improving.’"  
question\_text: "Write a CRAF prompt to produce a 250-word underwriting financial narrative with headings Performance/Liquidity/Leverage and a 3-bullet ‘So what?’ lead."  
scoring rubric criteria:

*   "Context states the underwriting artifact and what inputs are provided": max 1
*   "Role sets an underwriter voice": max 1
*   "Action specifies deliverable + word count + focus": max 1
*   "Format specifies lead bullets + headings + constraints": max 1

Item 3 — type: micro\_task  
Tests: diagnosing why output is generic  
scenario\_text: "Prompt: ‘Summarize these financials.’ Output: ‘Revenue changes can be caused by many factors…’"  
question\_text: "In one sentence, name two CRAF elements that were under-specified and what should be added."  
scoring rubric criteria:

*   "Correctly flags missing/weak Action": max 1
*   "Correctly flags missing/weak Format": max 1
*   "Suggests concrete additions (word count, headings, top risks)": max 1
*   "Mentions constraints (use only provided data / no guessing)": max 1

***

### Diagnostic: critical\_eval

Item 1 — type: mcq  
Tests: recognizing the highest-risk AI failure mode in underwriting  
question\_text: "Which AI mistake is most dangerous to copy into a credit recommendation?"  
options: A) Slightly formal tone | B) Invented covenant value that seems plausible | C) Minor grammar issues | D) Extra background sentence about the sector  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: writing a verification-oriented prompt  
scenario\_text: "You received an AI summary of a long submission. You must ensure it doesn’t invent ratios or omit key risks."  
question\_text: "Write a prompt that asks AI to produce a summary with citations/quotes from provided excerpts and to label any missing info as UNKNOWN."  
scoring rubric criteria:

*   "Explicitly requests evidence/quotes tied to claims": max 1
*   "Includes UNKNOWN / no guessing constraint": max 1
*   "Separates facts vs interpretation": max 1
*   "Defines a structured output for verification (table/checklist)": max 1

Item 3 — type: micro\_task  
Tests: applying VERIFY  
scenario\_text: "AI output says: ‘Liquidity is strong and improving.’ Source excerpt provided includes only income statement lines."  
question\_text: "In one sentence, explain why this claim fails VERIFY and what you would do next."  
scoring rubric criteria:

*   "Flags missing evidence (no liquidity data in source)": max 1
*   "States the correct next source needed (cash/availability/CF)": max 1
*   "Mentions rewriting claim as pending/UNKNOWN": max 1
*   "Shows skeptical review stance": max 1

***

### Diagnostic: relationship\_intel

Item 1 — type: mcq  
Tests: avoiding over-disclosure in customer communications  
question\_text: "Which detail should NOT be included in a customer-facing decline email draft?"  
options: A) What information is missing and how to submit it | B) A calm acknowledgement of urgency | C) Internal risk level label and internal reason code | D) A clear next step and timeline  
correct\_option: C  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: using RELATE to draft a response  
scenario\_text: "Customer email is angry about a reduction, claims they ‘provided everything.’ You also have internal notes about missing items."  
question\_text: "Write a prompt that asks AI to draft a response using RELATE: acknowledge concern, explain decision at a high level, request specific missing info, offer an alternative option—without internal-only details."  
scoring rubric criteria:

*   "Summarizes concern + history (Review/Extract)": max 1
*   "Tailors to audience (plain language, calm tone)": max 1
*   "Avoids internal-only rationale/codes/systems": max 1
*   "Includes specific next steps/options": max 1

Item 3 — type: micro\_task  
Tests: tone + specificity correction  
scenario\_text: "Draft AI reply: ‘We apologize for any inconvenience. Your request has been denied due to policy.’"  
question\_text: "Rewrite the sentence to be more specific and helpful while staying non-disclosive (one sentence)."  
scoring rubric criteria:

*   "Acknowledges concern without admitting fault": max 1
*   "Adds a concrete next step (what info is needed / option)": max 1
*   "Keeps plain language and concise tone": max 1
*   "Avoids internal policy jargon/codes": max 1

***

### Diagnostic: data\_decision

Item 1 — type: mcq  
Tests: distinguishing hypothesis vs verified driver  
question\_text: "AI says ‘margin fell due to competitive pressure.’ What is the best underwriter response?"  
options: A) Accept it and add to the memo | B) Treat as hypothesis and request evidence | C) Ignore all AI outputs | D) Escalate immediately without review  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: SIFT prompt creation  
scenario\_text: "You have a 3-year income statement and balance sheet summary with large YoY swings."  
question\_text: "Write a prompt that applies SIFT to output: top variances, evidence-backed hypotheses, implications, and next info requests."  
scoring rubric criteria:

*   "Selects limited ‘top’ variances (not everything)": max 1
*   "Separates hypotheses from verified facts": max 1
*   "Maps implications to underwriting actions": max 1
*   "Includes evidence requirement / UNKNOWN constraint": max 1

Item 3 — type: micro\_task  
Tests: spotting an unsupported inference  
scenario\_text: "Provided data: revenue flat, EBITDA down, AR up sharply. AI claim: ‘The company lost a major customer.’"  
question\_text: "In one sentence, explain why the claim is not supported and what a supported inference would look like."  
scoring rubric criteria:

*   "States claim is unsupported by provided data": max 1
*   "Suggests a supported inference (profitability pressure / WC build)": max 1
*   "Mentions evidence needed to confirm customer loss": max 1
*   "Keeps reasoning tied to numbers": max 1

***

### Diagnostic: augmented\_comm

Item 1 — type: mcq  
Tests: selecting the right Copilot surface  
question\_text: "You need to interpret an Excel variance table and turn it into a memo paragraph. Best starting surface?"  
options: A) Outlook | B) Excel | C) Teams | D) PowerPoint  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: designing a tool chain  
scenario\_text: "Inputs include: a Teams thread, an email template library, an Excel table, and a Word memo draft."  
question\_text: "Write a short plan (as a prompt to Copilot) that chains at least 3 surfaces in the right order, with a verification step before the final external email."  
scoring rubric criteria:

*   "Chooses appropriate surfaces for each input type": max 1
*   "Orders steps logically (summarize → draft → polish)": max 1
*   "Includes a verification gate": max 1
*   "Keeps internal vs external outputs separated": max 1

Item 3 — type: micro\_task  
Tests: identifying a chain failure  
scenario\_text: "A learner drafts a customer email directly from an internal memo paragraph that mentions ‘internal risk committee.’"  
question\_text: "In one sentence, identify the chain mistake and how to fix it using the Surface Selector."  
scoring rubric criteria:

*   "Flags internal-to-external leakage": max 1
*   "Recommends separating internal memo vs customer email": max 1
*   "Suggests correct surfaces (Word internal, Outlook external)": max 1
*   "Mentions final human check/verification": max 1

***

# SECTION G — Evaluation Item Seeds (28 items: 4 per course × 7 courses)

### Evaluation: Course 1

Item 1 — type: mcq, sequence: 1  
question\_text: "In SAFE Abstraction, what does ‘A’ primarily mean?"  
options: A) Add more detail | B) Abstract exact figures into ranges/ratios | C) Approve the AI output | D) Ask the AI to decide  
correct\_option: B  
explanation: "Abstracting reduces confidentiality risk while keeping analytical usefulness."

Item 2 — type: mcq, sequence: 2  
question\_text: "Which is the best ‘UNKNOWN’ guardrail instruction?"  
options: A) “Use your best guess if data is missing.” | B) “If a detail is missing, invent a plausible estimate.” | C) “If a detail is not provided, write UNKNOWN and list what would be needed.” | D) “Skip missing details silently.”  
correct\_option: C  
explanation: "It prevents hallucinations and creates a clear follow-up list."

Item 3 — type: mcq, sequence: 3  
question\_text: "What is a ‘deal fingerprint’?"  
options: A) A typo in a memo | B) A detail that can identify the deal even without the client name | C) A standard template heading | D) A public market statistic  
correct\_option: B  
explanation: "Fingerprints (unique amounts, locations, counterparties) can re-identify the case."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You have confidential inputs for <Company>Bayfield Composites Ltd.</Company> and need AI help summarizing top risks and mitigants. Write (1) a SAFE Abstraction plan and (2) a policy-safe prompt that requests a bullet summary and labels missing info as UNKNOWN."  
scoring rubric:
key1: "Plan strips identifiers and removes deal fingerprints (names/IDs/unique details)"
key2: "Plan abstracts exact figures into ranges/ratios while preserving risk meaning"
key3: "Prompt has a clear deliverable (top risks + mitigants) with constraints (no guessing/UNKNOWN)"
key4: "Prompt output format is specified (bullets/sections) and remains internal-safe"

***

### Evaluation: Course 2

Item 1 — type: mcq, sequence: 1  
question\_text: "Which CRAF element most directly controls length and structure?"  
options: A) Context | B) Role | C) Action | D) Format  
correct\_option: D  
explanation: "Format defines headings, bullets, and ordering."

Item 2 — type: mcq, sequence: 2  
question\_text: "Your AI output recommends ‘approve’ even though you asked only for analysis. Best fix?"  
options: A) Remove Role instruction | B) Add constraint: ‘Do not recommend approval/decline’ | C) Make the prompt shorter | D) Ask for a friendlier tone  
correct\_option: B  
explanation: "A constraint prevents scope creep into decisions."

Item 3 — type: mcq, sequence: 3  
question\_text: "Why is a Role instruction helpful in underwriting prompts?"  
options: A) It guarantees accuracy | B) It calibrates voice, assumptions, and relevance | C) It sets word count | D) It prevents confidentiality risk  
correct\_option: B  
explanation: "Role sets the perspective and vocabulary; it doesn’t replace verification."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You have an Excel table of metrics for <Company>Northshore Windworks Inc.</Company>. Write a complete CRAF prompt that produces a 250-word underwriting financial narrative with a 3-bullet ‘So what?’ lead and headings Performance/Liquidity/Leverage. Include ‘use only provided data’ and ‘UNKNOWN if missing’ constraints."  
scoring rubric:
key1: "Context clearly states underwriting artifact and inputs"
key2: "Role sets an underwriter voice and audience"
key3: "Action specifies deliverable, length, and focus (top risks/implications)"
key4: "Format defines lead bullets + headings + constraints (no guessing/UNKNOWN)"

***

### Evaluation: Course 3

Item 1 — type: mcq, sequence: 1  
question\_text: "In VERIFY, what does ‘R’ stand for?"  
options: A) Rewrite | B) Recompute | C) Reassure | D) Reduce  
correct\_option: B  
explanation: "Recompute critical ratios from sources."

Item 2 — type: mcq, sequence: 2  
question\_text: "Which claim should you verify first?"  
options: A) Tone sounds formal | B) A ratio that affects covenant compliance | C) Spelling of headings | D) Background sector definition  
correct\_option: B  
explanation: "High-impact claims must be checked first."

Item 3 — type: mcq, sequence: 3  
question\_text: "Best way to reduce ‘false certainty’ in AI summaries?"  
options: A) Ask AI to be confident | B) Ask AI to cite/quote sources and label UNKNOWN | C) Ask for longer output | D) Remove constraints  
correct\_option: B  
explanation: "Evidence-linking and UNKNOWN labeling reduce hallucinations."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You received an AI summary of <Company>HarborGate Foods Ltd.</Company>’s submission. Draft an approver update that includes only VERIFIED facts, labels pending items, and lists what you will check next using VERIFY."  
scoring rubric:
key1: "Identifies high-impact items and verifies against sources"
key2: "Clearly labels pending/UNKNOWN items without inventing details"
key3: "Separates facts from interpretations/recommendations"
key4: "Provides a next-step verification plan aligned to VERIFY"

***

### Evaluation: Course 4

Item 1 — type: mcq, sequence: 1  
question\_text: "In RELATE, what is the goal of ‘Label stakeholders’?"  
options: A) Assign blame | B) Decide what level of detail and tone fits each audience | C) Add internal codes | D) Make the email longer  
correct\_option: B  
explanation: "Different audiences need different framing and detail."

Item 2 — type: mcq, sequence: 2  
question\_text: "Which sentence is safest for a customer email?"  
options: A) “We reduced your limit because our internal risk score worsened.” | B) “We can’t cover because committee said no.” | C) “Based on the information provided so far, we’re unable to confirm coverage at the requested level; here’s what we need to reassess.” | D) “Our system CIS flagged you.”  
correct\_option: C  
explanation: "It’s clear, non-disclosive, and action-oriented."

Item 3 — type: mcq, sequence: 3  
question\_text: "Best AI prompt guardrail for customer-facing drafts?"  
options: A) “Include internal rationale for transparency.” | B) “Reference internal systems for clarity.” | C) “Avoid internal codes/systems/committees; use plain language; provide next steps.” | D) “Use legal language wherever possible.”  
correct\_option: C  
explanation: "It prevents internal leakage and improves clarity."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: <Company>Seabright Equipment Brokers Ltd.</Company> is angry about a reduction. Write a RELATE-based prompt that generates a calm, specific response: acknowledge concern, explain at a high level, request missing info, and offer an alternative option—without internal-only details."  
scoring rubric:
key1: "Prompt summarizes history and extracts the real concern"
key2: "Tailors tone and format to the audience (plain language, concise)"
key3: "Includes specific next steps/options and timelines"
key4: "Adds guardrails preventing internal disclosures (codes/systems/committees)"

***

### Evaluation: Course 5

Item 1 — type: mcq, sequence: 1  
question\_text: "In SIFT, what does ‘T’ stand for?"  
options: A) Talk | B) Tie to risk appetite & next action | C) Translate | D) Track  
correct\_option: B  
explanation: "SIFT ends in a decision-relevant action."

Item 2 — type: mcq, sequence: 2  
question\_text: "AI proposes a driver not supported by the numbers. Best response?"  
options: A) Paste it anyway | B) Mark it as hypothesis and request evidence | C) Remove all variance discussion | D) Escalate immediately  
correct\_option: B  
explanation: "Underwriters must separate hypotheses from verified facts."

Item 3 — type: mcq, sequence: 3  
question\_text: "What output structure best supports decision-making?"  
options: A) One long paragraph | B) Variance table + drivers + evidence needed + implications + actions | C) Only bullet points with no numbers | D) A persuasive approval recommendation  
correct\_option: B  
explanation: "It creates traceability from data → action."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You see large YoY swings for <Company>AtlasForge Machinery Ltd.</Company>. Write a SIFT prompt that outputs top 5 variances, evidence-backed hypotheses, underwriting implications, and an action plan (questions, mitigants, escalation trigger)."  
scoring rubric:
key1: "Selects a limited set of material variances"
key2: "Separates hypotheses from verified facts and demands evidence"
key3: "Maps implications to underwriting terms/conditions or info requests"
key4: "Produces a concrete action plan and avoids invented details"

***

### Evaluation: Course 6

Item 1 — type: mcq, sequence: 1  
question\_text: "Best surface to draft a customer-ready email with tone control?"  
options: A) Excel | B) Outlook | C) Teams | D) PowerPoint  
correct\_option: B  
explanation: "Outlook Copilot is designed for email drafting and tone refinement."

Item 2 — type: mcq, sequence: 2  
question\_text: "What is the most important ‘gate’ between tools in a chain workflow?"  
options: A) Adding emojis | B) Verification against source-of-truth | C) Making output longer | D) Asking AI to be confident  
correct\_option: B  
explanation: "Verification prevents errors and over-disclosure."

Item 3 — type: mcq, sequence: 3  
question\_text: "Which chain is most appropriate?"  
options: A) Customer email → internal memo → verification | B) Teams recap → Word memo draft → verification → Outlook email | C) PowerPoint slides → customer email | D) Outlook email → Excel analysis  
correct\_option: B  
explanation: "It starts with the right input source and inserts a verification gate."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: A Customer Care request arrives for <Company>PrairiePulse Exporters Inc.</Company>. Create a Copilot Surface Selector plan that chains 3+ tools and includes a final checklist before updating the system-of-record and sending the customer email."  
scoring rubric:
key1: "Selects appropriate surfaces based on input types (thread, template, table, memo)"
key2: "Orders steps logically and includes handoff outputs"
key3: "Includes verification and confidentiality checks before external send"
key4: "Separates internal documentation vs customer-facing messaging"

***

### Evaluation: Course 7

Item 1 — type: mcq, sequence: 1  
question\_text: "In the capstone workflow, when should you apply SAFE?"  
options: A) Only at the end | B) Before every prompt that uses case content | C) Only for customer emails | D) Only if the deal is large  
correct\_option: B  
explanation: "SAFE is a pre-prompt gate to prevent leakage."

Item 2 — type: mcq, sequence: 2  
question\_text: "What is the correct way to use an external ‘company assessment’ summary?"  
options: A) Copy it into the memo as fact | B) Use it as hypothesis input and VERIFY sources before using | C) Ignore it completely | D) Ask AI to rewrite it to sound confident  
correct\_option: B  
explanation: "External summaries must be verified for sourcing and recency."

Item 3 — type: mcq, sequence: 3  
question\_text: "What must be true before AI-assisted text becomes part of an approval recommendation?"  
options: A) It sounds professional | B) It is VERIFIED against sources and clearly labels assumptions | C) It is long and detailed | D) It includes a strong opinion  
correct\_option: B  
explanation: "Approval content needs evidence, traceability, and clear uncertainty labeling."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: End-to-end case for <Company>Cascadia Marine Systems Ltd.</Company>. Produce (1) a 6-checkpoint workflow plan using SAFE/CRAF/VERIFY/RELATE/SIFT/Surface Selector, and (2) a 3-prompt sequence that generates a case brief, variance narrative, and internal recommendation—each with ‘no guessing/UNKNOWN’ constraints and explicit verification steps."  
scoring rubric:
key1: "Workflow includes all 6 domains with clear artifacts and stop/verify gates"
key2: "Prompts are structured (CRAF-like) and policy-safe (SAFE applied)"
key3: "Verification steps are explicit and separate facts vs assumptions"
key4: "Outputs are mapped to stakeholder needs (internal brief, customer message, record note) without internal-to-external leakage"

***

If you want, I can also generate a compact “course-build checklist” for Claude Code that lists every required field per section (so nothing gets missed during content generation).
