## MACHINE-READABLE HEADER

role\_prefix: uw

company\_map:
course\_1: HarborLight Components Ltd.
course\_2: Solstice Agri-Equipment Inc.
course\_3: IronPeak Renewables Ltd.
course\_4: Northstar Marine Furnishings Ltd.
course\_5: CedarBridge Infrastructure Partners

framework\_names:
NOTE: These 5 names are standardized across all roles. Confirm which apply; adapt the
role-specific examples in SECTION E (concept\_text, good\_example, anti\_pattern) accordingly.
Do NOT invent new framework names unless a standardized name genuinely does not fit.

*   CRAF Framework
*   VERIFY Checklist
*   The SAFE Abstraction Method
*   Copilot Surface Selector
*   End-to-End AI Workflow

real\_use\_case:
course\_1: Explore Copilot 360 Option for the Credit Insurance Program&#x20;
course\_2: Use Gen-AI to help provide company assessments.&#x20;
course\_3: The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada).&#x20;
course\_4: Record governance - Summarizing Meeting notes and actions (with attendees tagged)&#x20;
course\_5: UW Streamlining; Underwriting Knowledge Assistant; Pricing Benchmark Retrieval [\[<File>Comp...lsx</File> \| Excel\]](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D&file=Complete-List-Categorized-110.xlsx&action=default&mobileredirect=true)

***

# SECTION A — Role Entry

role\_id: uw  
title: Underwriter  
description: "Assesses credit risk and makes credit decisions for insurance and financing transactions. Produces and maintains the official credit file (analysis, rationale, conditions, approvals) and communicates decisions to clients, brokers, and internal partners. Works closely with Business Development/Account Managers, Risk Analysts, Legal, ESG, and Financial Crimes teams across the underwriting lifecycle."

***

# SECTION B — All 4 Domain Specs

### Domain: prompting

domain\_id: prompting  
title: Prompting for Outcomes  
description: "Structuring AI prompts so outputs are directly usable in underwriting workflows — decision emails to policyholders/brokers, first-draft credit memos/submissions, covenant and conditions summaries, and concise internal recommendations for approvals — while staying aligned to underwriting standards and approved wording libraries like [Underwriter Communication Email Templates.docx](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B7086EBA1-6F1E-43CD-97E3-8A6F5A149D81%7D\&file=Underwriter%20Communication%20Email%20Templates.docx\&action=default\&mobileredirect=true\&DefaultItemOpen=1\&EntityRepresentationId=28ba8c95-982a-405c-b7e3-9ad7d612ea55)." [\[Underwrite...Templates \| Word\]](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B7086EBA1-6F1E-43CD-97E3-8A6F5A149D81%7D&file=Underwriter%20Communication%20Email%20Templates.docx&action=default&mobileredirect=true&DefaultItemOpen=1)

level\_0\_label: Unaware  
level\_0\_descriptor: "Has not used AI for underwriting tasks. Cannot explain how to give context (deal type, audience, decision constraints) to get a useful draft."

level\_1\_label: Explorer  
level\_1\_descriptor: "Uses basic prompts (e.g., 'draft an email') with little context. Output is generic, may include inappropriate detail, and requires a full rewrite before it can be sent or filed."

level\_2\_label: Practitioner  
level\_2\_descriptor: "Writes structured prompts with: (1) underwriting context (product, decision type, what’s known/unknown), (2) audience (client vs internal), (3) constraints (no internal model details; plain language), and (4) format (bullet sections, short rationale + next steps). Produces drafts that need only minor edits for accuracy and tone."

level\_3\_label: Proficient  
level\_3\_descriptor: "Adapts prompts for complex cases (partial approvals, exceptions, sensitive wording). Anticipates failure modes (over-disclosure, invented facts) and adds guardrails (cite only provided facts; ask clarifying questions). Iterates quickly to reach a compliant, client-ready message."

level\_4\_label: Champion  
level\_4\_descriptor: "Builds reusable prompt templates for common underwriting moments (decline explanation, info request, conditional approval). Coaches peers and contributes improvements to shared drafting standards (e.g., ‘approved phrasing’ playbooks)."

***

### Domain: verification

domain\_id: verification  
title: Verification and Judgment  
description: "Critically reviewing AI-assisted underwriting outputs before acting — validating financial figures, risk flags, policy alignment, and delegated authority. Ensures drafts match source documents and underwriting guidance (e.g., [Credit Insurance Risk Assessment Guideline.pdf](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Credit%20Insurance%20Risk%20Assessment%20Guideline.pdf?web=1\&EntityRepresentationId=3008a9dc-0b2b-41a0-8614-af21acc6f0c8)) and do not substitute for required human judgment." [\[Credit Ins...Guideline \| PDF\]](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Credit%20Insurance%20Risk%20Assessment%20Guideline.pdf?web=1)

level\_0\_label: Unaware  
level\_0\_descriptor: "Treats AI output as accurate by default. Might copy AI-generated risk rationale into the file without checking against the financials or credit report."

level\_1\_label: Explorer  
level\_1\_descriptor: "Skims AI output for obvious errors but does not systematically cross-check numbers, dates, or policy requirements."

level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses a repeatable verification routine: cross-checks AI summaries against source docs (financial statements, credit reports, emails), confirms policy/DOA alignment, removes unverifiable statements, and documents what was checked before finalizing a decision."

level\_3\_label: Proficient  
level\_3\_descriptor: "Catches subtle errors (plausible-but-wrong covenants, swapped entities, invented thresholds). Tightens prompts to reduce hallucinations (e.g., ‘use only the pasted text’). Escalates uncertainty rather than guessing."

level\_4\_label: Champion  
level\_4\_descriptor: "Creates verification checklists for the team (what must be true before approving). Trains peers on common AI failure modes in credit analysis and on how to document verification in the credit file."

***

### Domain: data\_safety

domain\_id: data\_safety  
title: Data Safety and Compliance  
description: "Applying EDC’s rules before using AI with underwriting data — protecting non-public client financials, deal terms, and any personal information. Uses only approved tools and follows policy requirements in [Responsible Use of Generative AI Policy.pdf](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1\&EntityRepresentationId=2d3b55d1-ae5f-4dea-b575-9d7a1196c422) (e.g., human review, avoid non-approved tools, avoid unsafe data entry)." [\[Responsibl...AI Policy \| PDF\]](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1)

level\_0\_label: Unaware  
level\_0\_descriptor: "May paste client financial statements, names, or deal terms into public AI tools without considering classification."

level\_1\_label: Explorer  
level\_1\_descriptor: "Knows ‘don’t share confidential data’ but struggles with gray areas (market rumors, internal ratings, partial identifiers). Prompts may still include too much detail."

level\_2\_label: Practitioner  
level\_2\_descriptor: "Consistently applies a ‘public vs non-public’ test, strips identifiers, abstracts numbers into ranges, and chooses the correct approved Copilot surface. Can explain why a prompt is safe."

level\_3\_label: Proficient  
level\_3\_descriptor: "Handles borderline cases confidently (e.g., combining multiple data points that could re-identify a client). Designs prompts that preserve usefulness while eliminating sensitive content, and adds audit-friendly notes on how AI was used."

level\_4\_label: Champion  
level\_4\_descriptor: "Spots new risk patterns (e.g., re-identification risk, hidden PII in attachments). Advises the team on safe prompt patterns and contributes examples to training and controls."

***

### Domain: tool\_fluency

domain\_id: tool\_fluency  
title: Tool Fluency (M365 + Copilot)  
description: "Choosing the right Microsoft 365 Copilot surface for underwriting tasks and chaining outputs across tools — Teams meeting recap → Outlook follow-up email → SharePoint filing → Word memo edits → Excel checks — while keeping the credit file complete and compliant." (Example workflows appear in [Risk Underwriting Demo.pptx](https://edcanada.sharepoint.com/sites/NEXUS/_layouts/15/Doc.aspx?sourcedoc=%7B4AE8CAF9-164B-40C6-A281-8D39A065711D%7D\&file=Risk%20Underwriting%20Demo.pptx\&action=edit\&mobileredirect=true\&DefaultItemOpen=1\&EntityRepresentationId=554e365a-5449-4042-83b7-3d759f534ce2).) [\[Risk Under...iting Demo \| PowerPoint\]](https://edcanada.sharepoint.com/sites/NEXUS/_layouts/15/Doc.aspx?sourcedoc=%7B4AE8CAF9-164B-40C6-A281-8D39A065711D%7D&file=Risk%20Underwriting%20Demo.pptx&action=edit&mobileredirect=true&DefaultItemOpen=1)

level\_0\_label: Unaware  
level\_0\_descriptor: "Has not used Copilot features in Outlook/Teams/Word/Excel. Doesn’t know which tool is best for which task."

level\_1\_label: Explorer  
level\_1\_descriptor: "Uses one Copilot feature occasionally (e.g., draft an email) but does not connect steps (meeting recap doesn’t flow into record updates)."

level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses at least three Copilot surfaces and completes simple chains (Teams recap → Outlook email → save note to SharePoint). Chooses a surface based on input type (transcript vs document vs spreadsheet)."

level\_3\_label: Proficient  
level\_3\_descriptor: "Designs multi-step workflows across 3+ tools, recovers when one step fails (e.g., recap misses decisions), and knows when to switch surfaces (Excel for numbers, Word for narrative)."

level\_4\_label: Champion  
level\_4\_descriptor: "Documents best-practice tool chains for common underwriting cycles (triage day, credit committee week, end-of-week housekeeping). Coaches peers and shares new Copilot features that reduce repetitive work."

***

# SECTION C — All 5 Course Specs

### Course 1 — Write Client-Ready Credit Decisions with AI

course\_id: uw\_c1\_prompting  
role\_id: uw  
primary\_domain: prompting  
sequence\_order: 1  
title: "Write Client-Ready Credit Decisions with AI"  
tagline: "Turn a complex credit decision into a clear, compliant email using the CRAF Framework."  
description: "Underwriters write high-volume customer communications (approvals, declines, info requests) where wording matters. This course teaches the CRAF Framework (Context, Role, Action, Format) to generate usable first drafts in Outlook/Word while staying consistent with approved wording patterns (e.g., [Underwriter Communication Email Templates.docx](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B7086EBA1-6F1E-43CD-97E3-8A6F5A149D81%7D\&file=Underwriter%20Communication%20Email%20Templates.docx\&action=default\&mobileredirect=true\&DefaultItemOpen=1\&EntityRepresentationId=28ba8c95-982a-405c-b7e3-9ad7d612ea55)) and avoiding over-disclosure of internal credit models."   
real\_use\_case: "Explore Copilot 360 Option for the Credit Insurance Program" [\[Underwrite...Templates \| Word\]](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B7086EBA1-6F1E-43CD-97E3-8A6F5A149D81%7D&file=Underwriter%20Communication%20Email%20Templates.docx&action=default&mobileredirect=true&DefaultItemOpen=1) [\[<File>Comp...lsx</File> \| Excel\]](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D&file=Complete-List-Categorized-110.xlsx&action=default&mobileredirect=true)

***

### Course 2 — Trust but Verify: Validating AI’s Credit Analysis

course\_id: uw\_c2\_verification  
role\_id: uw  
primary\_domain: verification  
sequence\_order: 2  
title: "Trust but Verify: Validating AI’s Credit Analysis"  
tagline: "Use the VERIFY Checklist to catch errors before they reach the credit file or the client."  
description: "AI can speed up due diligence summaries and risk flag extraction, but underwriting requires disciplined verification. This course teaches a practical verification workflow (VERIFY Checklist) for checking AI-generated company assessments against source documents and underwriting guidance such as [Credit Insurance Risk Assessment Guideline.pdf](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Credit%20Insurance%20Risk%20Assessment%20Guideline.pdf?web=1\&EntityRepresentationId=3008a9dc-0b2b-41a0-8614-af21acc6f0c8), and documenting what was verified."   
real\_use\_case: "Use Gen-AI to help provide company assessments." [\[Credit Ins...Guideline \| PDF\]](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Credit%20Insurance%20Risk%20Assessment%20Guideline.pdf?web=1) [\[<File>Comp...lsx</File> \| Excel\]](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D&file=Complete-List-Categorized-110.xlsx&action=default&mobileredirect=true)

***

### Course 3 — Safely Harnessing AI with Confidential Data

course\_id: uw\_c3\_data\_safety  
role\_id: uw  
primary\_domain: data\_safety  
sequence\_order: 3  
title: "Safely Harnessing AI with Confidential Data"  
tagline: "Use the SAFE Abstraction Method to get AI help without leaking non-public client data."  
description: "Underwriters handle sensitive financial and personal data, so tool choice and prompt content must follow policy. This course teaches how to screen for sensitive data, abstract/anonymize safely, and use approved tools consistent with [Responsible Use of Generative AI Policy.pdf](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1\&EntityRepresentationId=2d3b55d1-ae5f-4dea-b575-9d7a1196c422)—especially under time pressure."   
real\_use\_case: "The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada)." [\[Responsibl...AI Policy \| PDF\]](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1) [\[<File>Comp...lsx</File> \| Excel\]](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D&file=Complete-List-Categorized-110.xlsx&action=default&mobileredirect=true)

***

### Course 4 — Mastering Copilot for Meetings and Follow-Ups

course\_id: uw\_c4\_tool\_fluency  
role\_id: uw  
primary\_domain: tool\_fluency  
sequence\_order: 4  
title: "Mastering Copilot for Meetings and Follow-Ups"  
tagline: "Use the Copilot Surface Selector to turn meetings into accurate actions and records."  
description: "Underwriters attend frequent huddles, deal forums, and pipeline reviews where decisions and actions must be captured and stored. This course trains learners to use Copilot across Teams, Outlook, and SharePoint to produce a meeting recap, validate it, send follow-ups, and file the record properly."  
real\_use\_case: "Record governance - Summarizing Meeting notes and actions (with attendees tagged)" [\[<File>Comp...lsx</File> \| Excel\]](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D&file=Complete-List-Categorized-110.xlsx&action=default&mobileredirect=true)

***

### Course 5 — AI in Action: End-to-End Underwriting Simulation

course\_id: uw\_c5\_capstone  
role\_id: uw  
primary\_domain: prompting  
sequence\_order: 5  
title: "AI in Action: End-to-End Underwriting Simulation"  
tagline: "Run an end-to-end AI-assisted workflow across documents, knowledge search, and pricing—without sacrificing judgment or compliance."  
description: "This capstone integrates all four domains in one realistic underwriting sprint: summarize a long third-party submission, pull internal guidance through an underwriting knowledge assistant, draft a recommendation and client note, retrieve pricing benchmarks, and validate everything before finalizing. Learners must demonstrate prompting skill, verification discipline, safe abstraction, and tool chaining."  
real\_use\_case: "UW Streamlining; Underwriting Knowledge Assistant; Pricing Benchmark Retrieval" [\[<File>Comp...lsx</File> \| Excel\]](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D&file=Complete-List-Categorized-110.xlsx&action=default&mobileredirect=true)

***

# SECTION D — All 5 Scenario Seeds

### Course 1 Scenario

scenario\_text: "You are underwriting a credit insurance limit decision for <Company>HarborLight Components Ltd.</Company>, a Canadian exporter selling industrial parts to a foreign buyer. The exporter is upset because their requested limit was partially approved with conditions. You need to respond today with a clear, courteous explanation and next steps. You want AI to help draft the email, but the first draft must be client-ready and must not reveal internal rating methods or confidential details."  
task\_1\_text: "Write a CRAF prompt that asks Copilot (Outlook) to draft a 180–220 word decision email explaining a partial approval with conditions, in plain language, with a short bullet list of next steps."  
task\_2\_text: "Your draft is too generic. Revise the Context and Action so the email includes: (a) a clear reason category (e.g., ‘limited recent financial information’), (b) what additional information would support reconsideration, and (c) an appeal/review path—without adding any internal model details."  
task\_3\_text: "The email tone is coming across as defensive. Add Role and Format instructions so the output is empathetic, factual, and structured as: ‘Decision’, ‘Why’, ‘What you can do next’."  
task\_4\_text: "The output includes a sentence that sounds like it references EDC’s internal risk rating model. Add a constraint to prevent any mention of internal scores, internal thresholds, or non-public sources, and force the AI to use only ‘information provided by the client’ phrasing."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters. The learner is practicing the CRAF Framework for client decision emails. Do not write the prompt for them. Ask guiding questions about missing CRAF elements and where the prompt is under-specified. Watch for red flags: real client names, deal amounts, internal ratings, or copying text from confidential files. If sensitive details appear, instruct the learner to abstract them before proceeding."

***

### Course 2 Scenario

scenario\_text: "You are evaluating a financing request from <Company>Solstice Agri-Equipment Inc.</Company>. You used AI to generate a one-page ‘company assessment’ summary from a mix of notes and a third-party report. The AI output looks polished but you know underwriting requires verification before relying on it in a credit submission or a risk decision."  
task\_1\_text: "List the first 4 checks you would do using the VERIFY Checklist before trusting the AI summary (focus on sources, numbers, and claims)."  
task\_2\_text: "Write a prompt that asks Copilot to produce a ‘verification plan’ table with columns: Claim, Source to check, How to confirm, Pass/Fail note—based only on the text you provide."  
task\_3\_text: "You discover one AI claim: ‘Revenue grew 18% YoY’ but your notes don’t show that. Write a short instruction you would add to the prompt to force the AI to mark any unsupported claims as ‘Unverified’ and to never invent numbers."  
task\_4\_text: "The AI summary recommends ‘approve with standard covenants’ without mentioning delegated authority or policy constraints. Write a prompt revision that requires: (a) DOA alignment check, (b) policy alignment check, and (c) a ‘what would make me escalate’ section."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing Verification and Judgment. Do not provide the learner’s final answers. Guide them to identify what must be verified and how. Flag any hallucination risk: invented figures, invented policy rules, invented approvals. If the learner includes real client identifiers or deal terms, instruct them to replace with placeholders or ranges."

***

### Course 3 Scenario

scenario\_text: "You received an email from <Company>IronPeak Renewables Ltd.</Company> with attached financial forecasts and a draft term sheet. You are under time pressure and tempted to paste the full documents into an external AI tool to get a quick risk summary. You must still get AI help, but you must do it safely and in line with [Responsible Use of Generative AI Policy.pdf](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1\&EntityRepresentationId=2d3b55d1-ae5f-4dea-b575-9d7a1196c422)."   
task\_1\_text: "Identify 5 types of information in this package that should be treated as non-public or sensitive in underwriting (write them as categories, not specifics)."  
task\_2\_text: "Use the SAFE Abstraction Method to rewrite the situation into a ‘safe prompt input’ (no names, no exact numbers, no identifiers). Write the abstracted context you would paste into Copilot."  
task\_3\_text: "Draft a prompt that asks Copilot to generate a risk-questions checklist (not a risk decision) based on your abstracted context, and includes a warning: ‘Do not provide final underwriting approval guidance’."  
task\_4\_text: "You need a paragraph for an internal memo, but you’re unsure whether a Copilot surface is approved for the content. Write the decision rule you will apply to choose: (a) internal M365 Copilot on a stored document, (b) a generic prompt with abstracted info, or (c) no AI use at all."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing Data Safety and Compliance. Do not write the learner’s final prompt. Guide them to remove sensitive details and choose safe tool patterns. Watch for: client names, exact amounts, term sheet clauses, personal information, internal risk ratings. If any appear, stop and require abstraction." [\[Responsibl...AI Policy \| PDF\]](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1)

***

### Course 4 Scenario

scenario\_text: "You just finished a weekly pipeline meeting about <Company>Northstar Marine Furnishings Ltd.</Company>. Decisions were made on what information is still needed and who will contact the customer. You want to use Copilot to create a meeting recap, assign actions, email the right people, and store the record in the deal’s SharePoint folder."  
task\_1\_text: "Using the Copilot Surface Selector, choose which tool you will start with (Teams, Outlook, Word, or SharePoint) and explain why in one sentence."  
task\_2\_text: "Write a prompt for Teams Copilot to generate a recap that includes: decisions, action items with owners, and deadlines—formatted as bullets. Include an instruction to label anything uncertain as ‘Needs confirmation’."  
task\_3\_text: "Now write a prompt for Outlook Copilot to draft a follow-up email that embeds the validated decisions and action list, and asks recipients to correct any ‘Needs confirmation’ items."  
task\_4\_text: "Write the final step instructions you would follow to store the recap as a formal record (where it goes, what filename pattern you use, and what you avoid including to protect confidentiality)."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters practicing Tool Fluency. Do not write the prompts for them. Ask them to justify tool choice and to ensure the recap includes decisions and actions. Watch for sensitive deal details and remind them to keep meeting records factual and minimal while still complete."

***

### Course 5 Scenario

scenario\_text: "You are assigned an urgent underwriting package for <Company>CedarBridge Infrastructure Partners</Company>. A partner bank sent a long credit submission. You must: (1) extract key risk flags quickly, (2) find internal guidance on how similar cases were handled, (3) draft a short internal recommendation and a client-facing update, and (4) sanity-check a proposed pricing range using benchmarks—all before end of day. You will use Copilot, but you must verify outputs and keep data safe."  
task\_1\_text: "Write a prompt (CRAF-style) to summarize the bank submission into: Key risks, missing information, and questions to resolve—using only the text you provide. Specify a 12-bullet maximum."  
task\_2\_text: "Use tool fluency: describe a 3-step Copilot chain (surface → output → next surface) to retrieve internal guidance (policy, templates, prior cases) without leaving M365."  
task\_3\_text: "Apply SAFE Abstraction: rewrite the pricing question so you can ask for benchmark ranges without sharing the client name, exact exposure, or confidential terms."  
task\_4\_text: "Apply VERIFY: list the exact verification steps you will take before you (a) paste any summary into the credit file and (b) send any client update."  
coach\_system\_prompt: "You are an AI skills coach for EDC Underwriters in a capstone simulation. Do not solve the tasks. Help the learner integrate prompting, verification, data safety, and tool chaining. Stop them if they include real identifiers, exact numbers, or internal model outputs. Push them to be specific about formats, constraints, and verification evidence."

***

# SECTION E — All 5 Reading Concept Specs

### Course 1 Reading

framework\_name: "CRAF Framework"  
concept\_text: "Underwriters don’t need ‘nice writing’—they need usable drafts that survive compliance and reduce rework. The CRAF Framework helps you control AI output so it matches underwriting reality. **Context** gives the situation (product, decision type, what’s known, what’s missing). **Role** tells the AI who it is (an underwriter writing a client email, not a sales pitch). **Action** defines the deliverable (e.g., a 200-word partial approval email with conditions and next steps). **Format** forces structure (headings + bullets) so you can review quickly and reduce accidental over-disclosure. In practice, CRAF is your guardrail against two common failures: (1) the AI invents rationale or numbers because you didn’t specify ‘use only provided facts,’ and (2) the AI includes internal underwriting language because you didn’t constrain tone and forbidden content. Pair CRAF with approved wording patterns from [Underwriter Communication Email Templates.docx](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B7086EBA1-6F1E-43CD-97E3-8A6F5A149D81%7D\&file=Underwriter%20Communication%20Email%20Templates.docx\&action=default\&mobileredirect=true\&DefaultItemOpen=1\&EntityRepresentationId=28ba8c95-982a-405c-b7e3-9ad7d612ea55) so the draft starts close to what your team already uses."   
good\_example: "Prompt: 'Context: Credit insurance limit decision email. Outcome is partial approval with conditions due to limited recent financial info. Do NOT mention internal risk ratings, thresholds, or non-public sources. Role: You are an EDC underwriter writing a client-facing email using plain language. Action: Draft a 180–220 word email that explains the decision, lists the conditions, and explains what information could support reconsideration. Format: Headings (Decision / Why / What you can do next), with bullet points under ‘What you can do next’.' Why it works: It constrains content, prevents internal leakage, and produces a reviewable structure."  
anti\_pattern: "Prompt: 'Write an email telling the client why we declined.' Why it fails: No context, no constraints, and no format. The AI may invent reasons, include internal model language, or produce a long generic template that wastes time and creates compliance risk."  
takeaway: "CRAF turns AI from ‘generic drafter’ into a controlled drafting assistant that produces underwriting-ready text you can validate and send." [\[Underwrite...Templates \| Word\]](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B7086EBA1-6F1E-43CD-97E3-8A6F5A149D81%7D&file=Underwriter%20Communication%20Email%20Templates.docx&action=default&mobileredirect=true&DefaultItemOpen=1)

***

### Course 2 Reading

framework\_name: "VERIFY Checklist"  
concept\_text: "AI can summarize and sound confident even when it’s wrong. Underwriting is high-stakes, so your default stance is: **use AI to accelerate reading, not to replace judgment**. The VERIFY Checklist is a simple routine you apply before any AI output becomes (a) a credit file record or (b) client communication. **V — Validate sources:** Is each claim traceable to a document you actually have? **E — Evaluate numbers:** Recalculate or cross-check key figures and ratios. **R — Review policy/authority:** Ensure the recommendation aligns with policy and delegated authority (don’t let AI suggest approvals you can’t sign). **I — Identify missing info:** What evidence is still needed to support the conclusion? **F — Flag uncertainty:** Mark anything unverified and remove it from decision text. **Y — Yield to escalation when unsure:** If uncertainty touches compliance, sanctions/KYC, or material exposure, escalate instead of guessing. Use [Credit Insurance Risk Assessment Guideline.pdf](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Credit%20Insurance%20Risk%20Assessment%20Guideline.pdf?web=1\&EntityRepresentationId=3008a9dc-0b2b-41a0-8614-af21acc6f0c8) as an anchor for what ‘must be true’ in credit insurance decisions."   
good\_example: "Before: AI output says ‘Revenue grew 18% YoY’ and ‘standard covenants apply.’ After applying VERIFY: you mark the revenue claim ‘Unverified—no source,’ you confirm covenants against the term sheet template, and you add a ‘Policy/DOA check’ section that states whether the decision must be escalated."  
anti\_pattern: "Copying an AI-generated company assessment into the credit memo because it ‘looks professional.’ Consequence: wrong numbers or invented claims enter the credit file, increasing audit and decision risk."  
takeaway: "If you can’t point to the source, it doesn’t belong in the credit file—VERIFY is how you keep AI helpful and safe." [\[Credit Ins...Guideline \| PDF\]](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Credit%20Insurance%20Risk%20Assessment%20Guideline.pdf?web=1)

***

### Course 3 Reading

framework\_name: "The SAFE Abstraction Method"  
concept\_text: "Time pressure is when data leaks happen. The SAFE Abstraction Method lets you use AI without exposing non-public client information. **S — Scan for sensitive content:** names, identifiers, deal terms, financial statements, personal data, internal ratings. **A — Abstract and anonymize:** replace names with roles (Exporter, Buyer, Bank), convert numbers to ranges (e.g., ‘mid seven figures’), remove unique facts that could identify the client. **F — Frame the question safely:** ask for checklists, questions, or structure—not final decisions or risk ratings. **E — Execute in approved environments + Evaluate:** use approved M365 Copilot surfaces on stored documents when allowed; otherwise use abstracted prompts; always do human review. This aligns with expectations in [Responsible Use of Generative AI Policy.pdf](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1\&EntityRepresentationId=2d3b55d1-ae5f-4dea-b575-9d7a1196c422), including that AI output must be reviewed and that non-public info must be protected."   
good\_example: "Before (unsafe): ‘Here’s the full term sheet for IronPeak Renewables… summarize and tell me if we should approve.’ After (SAFE): ‘Exporter in renewable energy seeking a guarantee; draft term sheet includes restrictive covenants and tight deadlines. Provide a checklist of questions to validate cash-flow assumptions and covenant feasibility. Do not recommend approval/decline.’"  
anti\_pattern: "Pasting full client financial forecasts into an external AI tool ‘just to save time.’ Consequence: policy breach and potential disclosure of protected information."  
takeaway: "SAFE keeps AI useful by changing *what you share* and *what you ask for*—so you get help without creating a data incident." [\[Responsibl...AI Policy \| PDF\]](https://edcanada.sharepoint.com/sites/EDCsGovernanceInstruments/Governance%20Instruments/Responsible%20Use%20of%20Generative%20AI%20Policy.pdf?web=1)

***

### Course 4 Reading

framework\_name: "Copilot Surface Selector"  
concept\_text: "Underwriters lose time when meeting outcomes don’t turn into actions and records. The Copilot Surface Selector helps you pick the right tool first, based on the input and the output you need. Start with **Teams Copilot** when your input is a meeting transcript/notes and you need a recap with decisions and actions. Use **Outlook Copilot** when the next step is a follow-up email that assigns actions and confirms deadlines. Use **Word Copilot** when you need a memo-style artifact (credit submission section, committee note). Use **Excel Copilot** when numbers or lists need checking (ratios, variance explanations). Finish in **SharePoint** by filing the approved record in the right location. The workflow mirrors the kind of multi-tool chains described in [Risk Underwriting Demo.pptx](https://edcanada.sharepoint.com/sites/NEXUS/_layouts/15/Doc.aspx?sourcedoc=%7B4AE8CAF9-164B-40C6-A281-8D39A065711D%7D\&file=Risk%20Underwriting%20Demo.pptx\&action=edit\&mobileredirect=true\&DefaultItemOpen=1\&EntityRepresentationId=554e365a-5449-4042-83b7-3d759f534ce2) (meeting recap → email → record)."   
good\_example: "A pipeline meeting ends → Teams Copilot creates a recap with ‘Decisions’ and ‘Actions’ → you edit and validate → Outlook Copilot drafts a follow-up email → you save the final recap to SharePoint under the deal folder with a consistent filename."  
anti\_pattern: "Starting in Word with ‘write meeting notes’ when the transcript is in Teams. Consequence: missing decisions, duplicated work, and weak recordkeeping."  
takeaway: "Pick the surface that matches the input. Chain outputs forward. Validate before you file or send." [\[Risk Under...iting Demo \| PowerPoint\]](https://edcanada.sharepoint.com/sites/NEXUS/_layouts/15/Doc.aspx?sourcedoc=%7B4AE8CAF9-164B-40C6-A281-8D39A065711D%7D&file=Risk%20Underwriting%20Demo.pptx&action=edit&mobileredirect=true&DefaultItemOpen=1)

***

### Course 5 Reading

framework\_name: "End-to-End AI Workflow"  
concept\_text: "The capstone skill is not ‘using AI’—it’s orchestrating AI safely across a full underwriting sprint. The End-to-End AI Workflow has four stages: **(1) Intake & Triage:** summarize long submissions into risks, missing info, and questions (prompting). **(2) Knowledge & Policy Pull:** retrieve internal guidance (policy, templates, past cases) using approved M365 search and Copilot surfaces (tool fluency). **(3) Drafting & Options:** draft internal recommendation + client update using constrained prompts (prompting + safety). **(4) Verify & Finalize:** apply VERIFY to ensure everything is sourced, accurate, and policy/authority-aligned (verification). This mirrors the intent of automation supports like [UCM - Credit Automation for Underwriters.docx](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B9CF76E2B-8514-4CBB-A179-AB6AC9D0BD32%7D\&file=UCM%20-%20Credit%20Automation%20for%20Underwriters.docx\&action=default\&mobileredirect=true\&DefaultItemOpen=1\&EntityRepresentationId=68683777-929e-4013-b65b-1ed8ed3a7115): faster turnaround while keeping the underwriter accountable for review and decision quality."   
good\_example: "You extract risk flags from a bank submission, pull relevant internal guidance, draft a short recommendation, ask for benchmark ranges using abstracted inputs, and then verify every claim before filing/sending."  
anti\_pattern: "One-shot prompting: ‘Summarize, decide, draft everything.’ Consequence: hallucinations, policy misalignment, and potential data exposure."  
takeaway: "The winning pattern is: **prompt → pull guidance → draft → verify**. Speed comes from the workflow, not from skipping judgment." [\[UCM - Cred...derwriters \| Word\]](https://edcanada.sharepoint.com/sites/CreditInsuranceResourceCenter/_layouts/15/Doc.aspx?sourcedoc=%7B9CF76E2B-8514-4CBB-A179-AB6AC9D0BD32%7D&file=UCM%20-%20Credit%20Automation%20for%20Underwriters.docx&action=default&mobileredirect=true&DefaultItemOpen=1)

***

# SECTION F — Diagnostic Item Seeds (12 items: 3 per domain)

### Diagnostic: prompting

Item 1 — type: mcq  
Tests: identifying the most important missing CRAF element for underwriting emails  
question\_text: "An underwriter writes: ‘Draft an email explaining my credit decision.’ What is the most important missing element for a usable output?"  
options: A) Context about the decision, audience, and constraints | B) A friendly tone request | C) A longer word count | D) A request for emojis  
correct\_option: A  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: writing a complete CRAF prompt for an underwriting email  
scenario\_text: "You need to request more information from a policyholder. Situation: export buyer limit request is missing recent financial statements and payment experience details. You must keep the email concise and plain language."  
question\_text: "Write a prompt using the CRAF Framework to draft a 150–180 word ‘request for information’ email with a bullet list of exactly 5 items needed."  
scoring rubric criteria:

*   "Context includes what is missing and why it matters (without internal model talk)": max 1
*   "Role sets the AI as an underwriter writing to a client in plain language": max 1
*   "Action defines the deliverable (info request email) with length + exactly 5 items": max 1
*   "Format requires headings or bullet structure for quick scanning": max 1

Item 3 — type: micro\_task  
Tests: diagnosing why AI output became generic  
scenario\_text: "AI output: ‘Please provide additional information so we can proceed. Thank you.’ Prompt used: ‘Write an email asking for more info.’"  
question\_text: "In one sentence, explain why the output is unhelpful and name two CRAF elements that are missing."  
scoring rubric criteria:

*   "Correctly identifies missing Context": max 1
*   "Correctly identifies missing Action specificity": max 1
*   "Correctly identifies missing Format constraints": max 1
*   "Explains consequence (generic, no actionable list)": max 1

***

### Diagnostic: verification

Item 1 — type: mcq  
Tests: recognizing the highest-risk verification failure  
question\_text: "Which is the riskiest behavior when using AI for a company assessment?"  
options: A) Using AI to summarize a report | B) Copying AI claims into a credit memo without checking sources | C) Asking for a shorter summary | D) Reformatting the summary into bullets  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: prompting for a verification plan (not a decision)  
scenario\_text: "You have an AI-generated paragraph claiming: ‘Liquidity improved, leverage decreased, and the outlook is stable.’ You have the financial statements and a credit report, but you haven’t checked them yet."  
question\_text: "Write a prompt that asks Copilot to produce a verification table: Claim | Source to check | How to confirm | Notes. Instruct it to label anything unsupported as ‘Unverified’."  
scoring rubric criteria:

*   "Requires use of a table with the specified columns": max 1
*   "Explicitly forbids inventing numbers or sources": max 1
*   "Includes ‘Unverified’ labeling rule for unsupported claims": max 1
*   "Keeps output focused on verification steps, not approval advice": max 1

Item 3 — type: micro\_task  
Tests: correcting an AI hallucination safely  
scenario\_text: "AI wrote: ‘The borrower has no covenant breaches in the last 12 months.’ You do not have covenant compliance evidence in your notes."  
question\_text: "Write the exact edit you would make to the sentence to keep it truthful and underwriting-appropriate."  
scoring rubric criteria:

*   "Removes the unsupported factual claim": max 1
*   "Replaces with a conditional/unknown statement (e.g., ‘not yet confirmed’)": max 1
*   "Adds a verification action (what evidence is needed)": max 1
*   "Maintains neutral, factual tone": max 1

***

### Diagnostic: data\_safety

Item 1 — type: mcq  
Tests: identifying unsafe data handling  
question\_text: "Which prompt is most likely to violate safe AI use rules for underwriters?"  
options: A) ‘Summarize the key questions I should ask about a generic term sheet structure’ | B) ‘Here is the full client financial statement PDF—summarize and recommend approve/decline’ | C) ‘Rewrite this email to be clearer, using placeholders for names’ | D) ‘Create a checklist for reviewing a credit report’  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: applying SAFE abstraction  
scenario\_text: "You have a draft term sheet with client name, exact amounts, and counterparties. You want AI help to generate a list of risk questions."  
question\_text: "Write a SAFE-abstraction version of the prompt input (2–4 sentences) that removes identifiers and exact numbers but keeps enough context to get useful risk questions."  
scoring rubric criteria:

*   "Removes names/unique identifiers": max 1
*   "Removes or ranges exact amounts/terms": max 1
*   "Keeps enough business context to be useful (product + general situation)": max 1
*   "Asks for questions/checklist (not a final credit decision)": max 1

Item 3 — type: micro\_task  
Tests: spotting hidden sensitive data  
scenario\_text: "A learner says: ‘I didn’t paste any names, just the borrower’s ownership structure and the bank account number is in the appendix.’"  
question\_text: "In one sentence, explain why this is still sensitive and what should be removed or abstracted."  
scoring rubric criteria:

*   "Identifies that ownership structure can be identifying/sensitive": max 1
*   "Identifies bank account number as sensitive": max 1
*   "States to remove/abstract these elements": max 1
*   "Mentions safe replacement (roles/placeholders/ranges)": max 1

***

### Diagnostic: tool\_fluency

Item 1 — type: mcq  
Tests: selecting the right Copilot surface  
question\_text: "You need a recap of decisions and action items from a Teams meeting. Where should you start?"  
options: A) Excel Copilot | B) Word Copilot | C) Teams Copilot | D) PowerPoint Copilot  
correct\_option: C  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
Tests: chaining tools (Teams → Outlook)  
scenario\_text: "A deal huddle ends with 3 action items and one decision. You need to send a follow-up email and store the recap."  
question\_text: "Write a Teams Copilot prompt that outputs: Decisions (bold), Actions (bulleted with owner + due date), and ‘Needs confirmation’ items."  
scoring rubric criteria:

*   "Requests explicit sections: Decisions, Actions, Needs confirmation": max 1
*   "Requires owner + due date fields for each action": max 1
*   "Adds uncertainty labeling rule": max 1
*   "Uses concise bullet formatting": max 1

Item 3 — type: micro\_task  
Tests: fixing a broken workflow step  
scenario\_text: "A Teams recap missed the main decision, but included lots of discussion. The learner wants to forward it as-is."  
question\_text: "In one sentence, state what they should do next (tool + instruction) to correct the recap before emailing."  
scoring rubric criteria:

*   "Says not to send as-is": max 1
*   "Selects the right next action (re-prompt Teams Copilot or edit manually)": max 1
*   "Specifies adding the missing decision explicitly": max 1
*   "Mentions validating against personal notes/agenda": max 1

***

# SECTION G — Evaluation Item Seeds (20 items: 4 per course)

### Evaluation: Course 1

Item 1 — type: mcq, sequence: 1  
question\_text: "In the CRAF Framework, which element most directly prevents an AI from mentioning internal risk ratings or thresholds?"  
options: A) Context | B) Role | C) Action | D) Format  
correct\_option: A  
explanation: "Context is where you state constraints like ‘do not mention internal models/thresholds’ and define what sources may be used."

Item 2 — type: mcq, sequence: 2  
question\_text: "Your AI-drafted client email is too long and includes generic export finance explanations. What prompt change fixes this fastest?"  
options: A) Add a friendlier tone request | B) Specify word count and required headings | C) Remove the Role instruction | D) Ask for more background paragraphs  
correct\_option: B  
explanation: "A concrete length limit and structure constraint reduces scope and forces relevance."

Item 3 — type: mcq, sequence: 3  
question\_text: "Which instruction best reduces hallucination risk in a decision email draft?"  
options: A) 'Be persuasive' | B) 'Use professional language' | C) 'Use only the facts provided below; do not invent details' | D) 'Make it longer'  
correct\_option: C  
explanation: "Forcing use of provided facts reduces invented rationales and numbers."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You must send a partial approval email to a policyholder. You can mention general reasons (e.g., incomplete information) but must not mention internal rating methods or non-public sources. Write a complete CRAF prompt to generate a 200-word email with headings: Decision / Why / What you can do next."  
scoring rubric:
key1: "Context includes decision type, audience, and forbidden content (no internal models/ratings/thresholds)"
key2: "Role positions AI as an underwriter writing in plain language and neutral tone"
key3: "Action specifies deliverable, length, and required content (conditions + reconsideration path)"
key4: "Format requires the exact headings and bullet list for next steps"

***

### Evaluation: Course 2

Item 1 — type: mcq, sequence: 1  
question\_text: "In VERIFY, which step ensures AI claims are traceable to evidence you actually have?"  
options: A) Evaluate numbers | B) Validate sources | C) Flag uncertainty | D) Yield to escalation  
correct\_option: B  
explanation: "Validate sources asks: ‘Where did this come from, and do I have it?’"

Item 2 — type: mcq, sequence: 2  
question\_text: "AI says: ‘No covenant breaches.’ You don’t have compliance reporting. What should you do?"  
options: A) Keep it because it sounds reasonable | B) Remove it or mark it unverified and request evidence | C) Replace with a stronger claim | D) Ask AI to restate it more confidently  
correct\_option: B  
explanation: "Underwriting requires evidence; unsupported claims must not enter the credit file."

Item 3 — type: mcq, sequence: 3  
question\_text: "Which prompt instruction best prevents AI from inventing financial ratios?"  
options: A) 'Use bullets' | B) 'Use only numbers explicitly provided; otherwise write “Not provided”' | C) 'Be concise' | D) 'Write like an expert'  
correct\_option: B  
explanation: "It forces the model to stop rather than fill gaps."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You have an AI-generated company assessment summary. Create a verification plan using VERIFY. Write a prompt that outputs a table with Claim / Source / How to confirm / Notes, and includes policy/DOA checks."  
scoring rubric:
key1: "Requires a structured verification table with the specified columns"
key2: "Includes instructions to label unsupported claims ‘Unverified’ and not invent data"
key3: "Includes policy and delegated authority alignment checks"
key4: "Includes an escalation trigger section for unresolved high-risk uncertainty"

***

### Evaluation: Course 3

Item 1 — type: mcq, sequence: 1  
question\_text: "In SAFE, which step is specifically about changing *what you ask* AI to do so it doesn’t act like an approver?"  
options: A) Scan | B) Abstract | C) Frame | D) Execute & Evaluate  
correct\_option: C  
explanation: "Frame shifts the request toward checklists/questions instead of approval decisions."

Item 2 — type: mcq, sequence: 2  
question\_text: "Which is the safest AI request when you only have abstracted deal context?"  
options: A) 'Approve or decline this deal' | B) 'Generate a checklist of questions and missing evidence to validate assumptions' | C) 'Predict default probability' | D) 'Rewrite the term sheet with client name included'  
correct\_option: B  
explanation: "A checklist supports judgment without requiring sensitive detail or substituting for approval."

Item 3 — type: mcq, sequence: 3  
question\_text: "A prompt includes ‘mid seven figures’ and ‘exporter in manufacturing’ but also includes a unique project codename used internally. What should you do?"  
options: A) Keep the codename; it’s not a name | B) Remove/replace the codename; it can re-identify the case | C) Add more detail to compensate | D) Ask AI to ignore it  
correct\_option: B  
explanation: "Unique identifiers can re-identify a case even without names."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You’re tempted to paste a full client forecast workbook into an external AI tool. Write a SAFE-compliant plan: (1) what you will remove/abstract, (2) what you will ask AI to produce, (3) where you will run it (approved surface), and (4) what human review you will do."  
scoring rubric:
key1: "Identifies sensitive elements to remove (names, exact numbers, identifiers, personal data)"
key2: "Uses abstraction (ranges/placeholders) while preserving context"
key3: "Requests safe outputs (questions/checklists/structure) rather than approval decisions"
key4: "Includes human review and verification before filing or sending"

***

### Evaluation: Course 4

Item 1 — type: mcq, sequence: 1  
question\_text: "You need to generate a meeting recap with decisions and action items. Which sequence best matches strong tool fluency?"  
options: A) Excel → Word → Teams → Outlook | B) Teams → Outlook → SharePoint | C) Outlook → Teams → SharePoint | D) PowerPoint → Word → Excel  
correct\_option: B  
explanation: "Start where the meeting content lives (Teams), then communicate (Outlook), then store the record (SharePoint)."

Item 2 — type: mcq, sequence: 2  
question\_text: "A Teams recap includes action items but no owners. What’s the best next step?"  
options: A) Send it anyway | B) Re-prompt Teams Copilot to add owner + due date fields | C) Move to Excel immediately | D) Delete it and take manual notes only  
correct\_option: B  
explanation: "Owners and dates are required for usable follow-up and recordkeeping."

Item 3 — type: mcq, sequence: 3  
question\_text: "What instruction best improves recap reliability?"  
options: A) 'Make it longer' | B) 'Include every conversation detail' | C) 'Label uncertain items as Needs confirmation' | D) 'Use emojis for clarity'  
correct\_option: C  
explanation: "It prevents false certainty and prompts human confirmation."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: After a deal huddle, you must produce a recap, send follow-ups, and store the record. Write: (a) a Teams Copilot prompt for recap + actions, and (b) an Outlook Copilot prompt for a follow-up email that requests corrections to ‘Needs confirmation’ items."  
scoring rubric:
key1: "Teams prompt requests Decisions + Actions with owner + due date + Needs confirmation"
key2: "Includes instruction to avoid inventing details and to flag uncertainty"
key3: "Outlook prompt produces concise follow-up email with embedded validated actions"
key4: "Includes a step to store the final record in the correct repository (SharePoint/deal folder) without sensitive excess detail"

***

### Evaluation: Course 5

Item 1 — type: mcq, sequence: 1  
question\_text: "In an end-to-end underwriting sprint, what should happen immediately after an AI summary of a long bank submission?"  
options: A) Send the summary to the client | B) Verify key claims against the source and identify missing info | C) Ask AI to decide approve/decline | D) Skip to pricing benchmarks  
correct\_option: B  
explanation: "Verification and missing-info identification prevents downstream errors."

Item 2 — type: mcq, sequence: 2  
question\_text: "Which action best demonstrates tool fluency when you need internal guidance on a policy rule?"  
options: A) Use a public web search with the client name | B) Use M365/SharePoint-based search and Copilot to locate the internal guidance | C) Ask AI to guess the policy | D) Ask a friend in chat to decide for you  
correct\_option: B  
explanation: "Internal guidance should be retrieved from approved internal repositories."

Item 3 — type: mcq, sequence: 3  
question\_text: "You want pricing benchmarks but have sensitive deal terms. What is the best SAFE approach?"  
options: A) Share the full term sheet | B) Abstract to ranges and ask for benchmark ranges and factors, not a final price | C) Ask for the exact rate you should charge | D) Don’t verify anything if AI seems confident  
correct\_option: B  
explanation: "Abstraction preserves confidentiality while still getting useful guidance."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Scenario: You must summarize a long submission, retrieve internal guidance, draft an internal recommendation and a client update, and check pricing benchmarks—fast. Write a step-by-step End-to-End AI Workflow plan (4 stages) that shows: prompts, tools/surfaces, SAFE constraints, and VERIFY steps before finalizing."  
scoring rubric:
key1: "Includes an intake/triage summary prompt with strict ‘use only provided text’ constraints"
key2: "Includes internal guidance retrieval step using appropriate M365 surfaces"
key3: "Includes SAFE abstraction for any benchmark/pricing question and client communications"
key4: "Includes explicit VERIFY steps (sources, numbers, policy/DOA, uncertainty, escalation triggers) before filing/sending"

***

**Source note (use case library):** All referenced use case titles above come from [Complete-List-Categorized-110.xlsx](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D\&file=Complete-List-Categorized-110.xlsx\&action=default\&mobileredirect=true\&EntityRepresentationId=218615c5-1774-48f6-b245-11684d68e1e5). [\[<File>Comp...lsx</File> \| Excel\]](https://edcanada-my.sharepoint.com/personal/hhu_edc_ca/_layouts/15/Doc.aspx?sourcedoc=%7B20AF7CD2-8D31-4881-BC1B-EF8D6683DE6C%7D&file=Complete-List-Categorized-110.xlsx&action=default&mobileredirect=true)
