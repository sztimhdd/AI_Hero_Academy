PM / Program Manager Use Case Mapping (Clean Version)
This document maps Project Manager (PM) / Program Manager use cases to the 110-item Gen‑AI use case library in Complete‑List‑Categorized‑110.xlsx.
Selections follow the agreed relevance scoring and domain rules and only use titles that exist in the source file.

TASKS 1 & 2 — Filter, Score, and Map to PM Domains
Selected PM‑Relevant Use Cases
































































































#Use Case Title (verbatim)RelevanceDomainCapstone1Co pilot for Program ManagementHIGHStrategic PromptingYES2Meeting "Recap" feature in MS‑Teams for Project Managers / Scrum Masters (PMs / SMs)HIGHAugmented CommunicationYES3Record governance – Summarizing Meeting notes and actions (with attendees tagged)HIGHResponsible AIYES4Teams Premium – AI Notes from Transcripts (inquiry into whether this meets our AI use policy)HIGHResponsible AIYES5Automated Portfolio Reporting AgentMEDIUMData‑Driven Decision MakingYES6Executive Brief SummariesMEDIUMCritical EvaluationYES7Multi‑Document SummarizationMEDIUMStrategic PromptingNO8Policy SummarizationMEDIUMResponsible AINO9Incident Communication DraftingMEDIUMAugmented CommunicationNO10Project Investment SummaryMEDIUMData‑Driven Decision MakingNO11Board Report SummariesMEDIUMAugmented CommunicationNO12Board Report Summaries AgentMEDIUMData‑Driven Decision MakingNO
Why These Are HIGH / MED for PMs

Multiple use cases explicitly describe PM / Program work, including:

Creating high‑level project plans and visuals
Capturing meeting minutes and action items
Acting as the system of record for delivery teams


Several additional use cases are adjacent but directly adaptable to PM workflows:

Portfolio reporting
Executive and board briefings
Policy summaries
Incident communications
Investment summaries



(All rationale is grounded in the use‑case descriptions in the source library — no inferred roles or invented behaviors.)

TASK 3 — Course Anchors (7 Courses)
Course 1 — Responsible AI

course_id: pm_c1_responsible_ai
Use case: Teams Premium – AI Notes from Transcripts (inquiry into whether this meets our AI use policy)
Rationale: PMs producing meeting minutes from transcripts must apply policy rules (public vs. non‑public data) before using AI‑generated notes.
Suggested title: Use AI meeting notes safely at EDC


Course 2 — Strategic Prompting

course_id: pm_c2_strategic_prompting
Use case: Co pilot for Program Management
Rationale: PMs rely on AI to draft project plans, job aids, and process maps; prompt quality directly affects output usefulness.
Suggested title: Prompt Copilot to draft usable project plans


Course 3 — Critical Evaluation

course_id: pm_c3_critical_eval
Use case: Executive Brief Summaries
Rationale: PMs must validate AI‑generated executive briefs for accuracy, gaps, and decision risk before leaders act on them.
Suggested title: Review AI briefs like an executive editor


Course 4 — Relationship Intelligence

course_id: pm_c4_relationship_intel
Use case: Customer Interaction Recap
Rationale: PMs use AI‑generated recaps to align internal stakeholders quickly by summarizing context, decisions, and next steps.
Suggested title: Use AI recaps to align stakeholders fast


Course 5 — Data‑Driven Decision Making

course_id: pm_c5_data_decision
Use case: Automated Portfolio Reporting Agent
Rationale: PMs and program leads use portfolio reporting to detect trends, risks, and exceptions that require action or escalation.
Suggested title: Use AI to surface portfolio signals early


Course 6 — Augmented Communication

course_id: pm_c6_augmented_comm
Use case: Meeting "Recap" feature in MS‑Teams for Project Managers / Scrum Masters (PMs / SMs)
Rationale: PMs are often the record‑keepers and need fast, accurate meeting summaries to keep delivery moving.
Suggested title: Turn meetings into actions with AI recaps


Course 7 — Capstone

course_id: pm_c7_capstone
Use cases:

Co pilot for Program Management
Meeting "Recap" feature in MS‑Teams for PMs / SMs
Record governance – Summarizing Meeting notes and actions
Automated Portfolio Reporting Agent


Rationale: Brings together strategic prompting, augmented communication, responsible AI, and data‑driven decisions into a single end‑to‑end PM workflow.
Suggested title: Run a program week with Copilot safely


TASK 4 — Gap Check
Relationship Intelligence domain:
No strong PM‑specific use case is explicitly defined in the library.
Recommendation:
Synthesize a realistic PM scenario grounded in day‑to‑day delivery work.
Suggested scenario seed:

Use AI to prepare a stakeholder briefing pack (risks, decisions required, tailored messages) from approved internal notes — without pasting non‑public information into the wrong AI surface.

All other domains have at least one HIGH or MED anchor directly supported by the use‑case library.

## Copy-paste pack for Prompt C (ONLY Tasks 3 & 4)

### Course 1 – Responsible AI

course\_id: pm\_c1\_responsible\_ai  
Use case: Teams Premium - AI Notes from Transcripts (inquiry into whether this meets our AI use policy)  
real\_use\_case: Teams Premium - AI Notes from Transcripts (inquiry into whether this meets our AI use policy)  
Rationale: PMs producing minutes from transcripts must apply the public/non-public test and policy boundaries before using AI notes.  
Suggested title: Use AI meeting notes safely at EDC

### Course 2 – Strategic Prompting

course\_id: pm\_c2\_strategic\_prompting  
Use case: Co pilot for Program Management  
real\_use\_case: Co pilot for Program Management  
Rationale: PMs can use AI to draft high-level project plans, job aids, and process maps—good prompting determines usefulness.  
Suggested title: Prompt Copilot to draft usable project plans

### Course 3 – Critical Evaluation

course\_id: pm\_c3\_critical\_eval  
Use case: Executive Brief Summaries  
real\_use\_case: Executive Brief Summaries  
Rationale: PMs must validate AI-generated executive briefs before leaders act on them, checking accuracy and omissions.  
Suggested title: Review AI briefs like an executive editor

### Course 4 – Relationship Intelligence

course\_id: pm\_c4\_relationship\_intel  
Use case: Customer Interaction Recap  
real\_use\_case: Customer Interaction Recap  
Rationale: PMs can use recaps to align internal stakeholders faster by summarizing call/email context and next steps consistently.  
Suggested title: Use AI recaps to align stakeholders fast

### Course 5 – Data-Driven Decision Making

course\_id: pm\_c5\_data\_decision  
Use case: Automated Portfolio Reporting Agent  
real\_use\_case: Automated Portfolio Reporting Agent  
Rationale: PMs and program leads use portfolio reporting to spot trends, risks, and exceptions that need decisions and escalation.  
Suggested title: Use AI to surface portfolio signals early

### Course 6 – Augmented Communication

course\_id: pm\_c6\_augmented\_comm  
Use case: Meeting "Recap" feature in MS-Teams for Project Managers /Scrum Masters (PMs / SMs)  
real\_use\_case: Meeting "Recap" feature in MS-Teams for Project Managers /Scrum Masters (PMs / SMs)  
Rationale: PMs are often the record-keepers and need fast, accurate meeting summaries and action capture to keep work moving.  
Suggested title: Turn meetings into actions with AI recaps

### Course 7 – Capstone

course\_id: pm\_c7\_capstone  
Use case(s): Co pilot for Program Management  
real\_use\_case: Co pilot for Program Management; Meeting "Recap" feature in MS-Teams for Project Managers /Scrum Masters (PMs / SMs); Record governance - Summarizing Meeting notes and actions (with attendees tagged); Automated Portfolio Reporting Agent  
Rationale: Integrates strategic prompting (plans), augmented communication (recaps), responsible AI (record governance), and data-driven decisions (portfolio reporting) in one end-to-end PM workflow.  
Suggested title: Run a program week with Copilot safely

Domain Relationship Intelligence: No strong use case match found in the library.  
Recommend synthesizing a scenario directly from the role profile.  
Suggested scenario seed: Use AI to prepare a stakeholder briefing pack (risks, decisions needed, tailored messages) from approved internal notes—without pasting non-public details into the wrong AI surface.
