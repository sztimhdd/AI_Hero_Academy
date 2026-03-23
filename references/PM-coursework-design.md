
PM Coursework
MACHINE-READABLE HEADER
role_prefix: pm
company_map:  course_1: Atlas Delivery Renewal  course_2: NorthBridge CRM Release 2  course_3: Summit Portfolio Review  course_4: Horizon Service Transition  course_5: Beacon Capacity Dashboard  course_6: Maple Program SteerCo  course_7: Polaris Transformation Wave
framework_names:  NOTE: These names are standardized across all roles where possible. Confirm which apply;  adapt the role-specific examples in SECTION E (concept_text, good_example, anti_pattern)  accordingly. Do NOT invent new framework names unless a standardized name genuinely does  not fit.

Course 1 — Responsible AI domain: The SAFE Abstraction Method
Course 2 — Strategic Prompting domain: CRAF Framework
Course 3 — Critical Evaluation domain: VERIFY Checklist
Course 4 — Relationship Intelligence domain: ALIGN Map
Course 5 — Data-Driven Decision Making domain: SIGNAL Review
Course 6 — Augmented Communication domain: Copilot Surface Selector
Course 7 — Capstone: End-to-End AI Workflow
real_use_case:  course_1: Teams Premium - AI Notes from Transcripts (inquiry into whether this meets our AI use policy)  course_2: Co pilot for Program Management  course_3: Executive Brief Summaries  course_4: Customer Interaction Recap  course_5: Automated Portfolio Reporting Agent  course_6: Meeting "Recap" feature in MS-Teams for Project Managers /Scrum Masters (PMs / SMs)  course_7: Co pilot for Program Management; Meeting "Recap" feature in MS-Teams for Project Managers /Scrum Masters (PMs / SMs); Record governance - Summarizing Meeting notes and actions (with attendees tagged); Automated Portfolio Reporting Agent
capability_tags:  course_1: safe_framework, data_classification, transcript_review, policy_boundaries, manual_review  course_2: craf_framework, prompt_structuring, project_plan_drafting, output_formatting, constraint_setting  course_3: verify_checklist, executive_brief_review, hallucination_detection, source_validation, decision_risk  course_4: align_map, stakeholder_mapping, dependency_context, tailored_messages, meeting_prep  course_5: signal_review, trend_detection, portfolio_reporting, risk_prioritization, escalation_judgment  course_6: copilot_surface_selector, m365_workflow, meeting_recap, action_tracking, communication_drafting  course_7: end_to_end_ai_workflow, safe_framework, craf_framework, verify_checklist, signal_review, copilot_surface_selector
SECTION A — Role Entry
role_id: pm
title: Project Manager / Program Manager
description: Project and Program Managers at EDC run initiatives from intake through planning, delivery, reporting, and closure using EDC’s Initiative Lifecycle Framework and Planview as the system of record for initiatives. They serve sponsors, business partners, delivery teams, PMO/Orchestration, and senior decision forums by turning scope, risks, budget, schedule, and decisions into controlled execution and clear reporting. Their work is highly cross-functional and closely tied to artifacts such as project charters, business cases, high-level plans, risk logs, status reports, change requests, resource plans, and closure plans. %20-%20Job%20Aid.pdf?web=1)
SECTION B — All 6 Domain Specs
Domain: responsible_ai
domain_id: responsible_ai
title: Responsible AI
description: Applying EDC’s Gen AI policy before using AI on project transcripts, status reports, RAID content, budget summaries, stakeholder decks, and planning artifacts. For PMs, this means separating public from non-public content, keeping internal delivery data inside approved tools, and never using AI output without human review before it influences decisions, communications, or records. %20-%20Job%20Aid.pdf?web=1)
level_0_label: Unaware
level_0_descriptor: Uses AI on meeting notes, risk items, or project documents without checking whether the content is non-public or whether the tool is approved.
level_1_label: Explorer
level_1_descriptor: Knows there is a policy, but still struggles to tell which project data is safe to input, especially transcripts, financials, vendor content, and sponsor commentary.
level_2_label: Practitioner
level_2_descriptor: Consistently applies the public/non-public test, keeps project data in approved tools, abstracts sensitive details where needed, and manually reviews AI output before using it in reports or meeting records.
level_3_label: Proficient
level_3_descriptor: Handles borderline cases well, such as internal draft decks, schedule variance explanations, and steering committee notes; can rewrite prompts to preserve usefulness while removing sensitive details.
level_4_label: Champion
level_4_descriptor: Coaches peers on safe use patterns for recaps, status updates, and planning documents; spots new policy risks when AI features are added to existing platforms and escalates early.
Domain: strategic_prompting
domain_id: strategic_prompting
title: Strategic Prompting
description: Structuring AI prompts so they produce directly usable PM outputs such as draft charters, high-level plans, process maps, steering updates, action summaries, issue narratives, benefits statements, and stakeholder-ready slides. For PMs, prompt quality determines whether AI saves time or creates rework.
level_0_label: Unaware
level_0_descriptor: Has not used AI to support project planning or asks vague prompts like “summarize this project.”
level_1_label: Explorer
level_1_descriptor: Writes simple prompts but gets generic plans, weak action lists, or unfocused summaries that need heavy rewriting.
level_2_label: Practitioner
level_2_descriptor: Uses structured prompts with context, role, action, constraints, and format to generate usable first drafts for project plans, briefings, and status updates.
level_3_label: Proficient
level_3_descriptor: Iterates prompts based on audience, project stage, and artifact type; adds exclusions, format rules, and governance constraints before prompting.
level_4_label: Champion
level_4_descriptor: Creates reusable prompt patterns for common PM work such as monthly status, RAID updates, steering packs, and closure lessons learned.
Domain: critical_eval
domain_id: critical_eval
title: Critical Evaluation
description: Reviewing AI-generated project outputs before acting on them—especially executive summaries, meeting recaps, status narratives, risk statements, and portfolio signals. PMs need to catch invented decisions, wrong owners, missing caveats, and unsupported claims before anything is logged, shared, or escalated. %20-%20Job%20Aid.pdf?web=1)
level_0_label: Unaware
level_0_descriptor: Treats AI summaries or recommendations as accurate by default and forwards them without source checking.
level_1_label: Explorer
level_1_descriptor: Reads the output before sharing it, but checks only obvious errors and misses subtle omissions or false certainty.
level_2_label: Practitioner
level_2_descriptor: Verifies AI outputs against source notes, Planview data, meeting transcripts, and approved baselines; removes unsupported claims before use.
level_3_label: Proficient
level_3_descriptor: Detects plausible-but-wrong content such as misattributed decisions, incorrect status colour logic, or false trend signals in portfolio reporting.
level_4_label: Champion
level_4_descriptor: Builds review habits into team workflows and teaches others how to validate AI recaps, executive summaries, and dashboard narratives.
Domain: relationship_intel
domain_id: relationship_intel
title: Relationship Intelligence
description: Using AI to understand and support the human network around delivery: sponsors, business partners, product owners, platform owners, SMEs, PMO/Orchestration, finance, risk, change, and external vendors. For PMs, this means tailoring messages, surfacing dependencies, and preparing stakeholder-specific briefings without losing context or trust. Grounding comes from project team structures, steercos, RACI-style plans, and cross-team governance routines.
level_0_label: Unaware
level_0_descriptor: Uses the same generic message or meeting prep for all stakeholders, regardless of role or decision authority.
level_1_label: Explorer
level_1_descriptor: Uses AI to summarize prior notes, but does not adapt outputs to sponsor, SME, or delivery-team needs.
level_2_label: Practitioner
level_2_descriptor: Uses AI to pull together stakeholder history, open dependencies, and decision needs into targeted briefing packs or follow-up notes.
level_3_label: Proficient
level_3_descriptor: Anticipates what different groups need—executive decision points, delivery blockers, change impacts, operational readiness—and adjusts AI prompts and outputs accordingly.
level_4_label: Champion
level_4_descriptor: Develops team patterns for stakeholder briefings and decision-readiness packs; helps others use AI to improve alignment, not just speed.
Domain: data_decision
domain_id: data_decision
title: Data-Driven Decision Making
description: Using AI to interpret portfolio, schedule, cost, resource, and status data from Planview and related reports to support prioritization, escalation, re-baselining, and leadership reporting. PMs do not just summarize numbers—they decide what matters, what needs action, and what should be escalated. %20-%20Job%20Aid.pdf?web=1)
level_0_label: Unaware
level_0_descriptor: Does not use AI or data tools to interpret project metrics and relies mainly on instinct or fragmented updates.
level_1_label: Explorer
level_1_descriptor: Uses AI to summarize metrics but does not connect signals to management actions such as escalation, re-baseline, or resource correction.
level_2_label: Practitioner
level_2_descriptor: Uses AI to surface trends, exceptions, and likely risk areas from project and portfolio data, then validates those signals against project context before acting.
level_3_label: Proficient
level_3_descriptor: Uses AI to compare scenarios, stress-test assumptions, and prepare evidence-backed recommendations for sponsors or governance forums.
level_4_label: Champion
level_4_descriptor: Builds repeatable ways for teams to use AI with Planview and reporting data to improve capacity planning, issue visibility, and governance discipline.
Domain: augmented_comm
domain_id: augmented_comm
title: Augmented Communication
description: Choosing the right M365 Copilot surface and multi-step workflow for PM communication work—Teams for meeting recap, Word for formal docs, PowerPoint for steering decks, Outlook for follow-up emails, and Planview/Power BI outputs as source inputs. PMs need to move from discussion to record to action without duplicating effort or losing control. %20-%20Job%20Aid.pdf?web=1)
level_0_label: Unaware
level_0_descriptor: Uses one tool at a time and manually rewrites the same content across meeting notes, emails, and reports.
level_1_label: Explorer
level_1_descriptor: Has tried one Copilot surface, such as Teams recap or Outlook draft, but does not chain tools together.
level_2_label: Practitioner
level_2_descriptor: Uses multiple M365 surfaces to turn meetings into summaries, summaries into follow-up messages, and project data into stakeholder-ready communications.
level_3_label: Proficient
level_3_descriptor: Designs multi-step workflows across Teams, Word, PowerPoint, Outlook, and project systems based on the audience and deliverable needed.
level_4_label: Champion
level_4_descriptor: Shares communication workflows with the team, reduces duplicate manual writing, and helps peers choose the best Copilot surface for the job.
SECTION C — All 7 Course Specs
Course 1 — Use AI Meeting Notes Safely at EDC
course_id: pm_c1_responsible_ai
role_id: pm
primary_domain: responsible_ai
sequence_order: 1
title: Use AI Meeting Notes Safely at EDC
tagline: Keep meeting recap speed high without crossing EDC data and policy lines.
description: PMs regularly use transcripts and meeting notes to produce records, actions, and follow-ups. This course teaches them how to apply EDC’s Gen AI policy to transcripts, action logs, decisions, and sensitive project content so they can use AI safely inside approved workflows and avoid unsafe copying into the wrong tool.
real_use_case: Teams Premium - AI Notes from Transcripts (inquiry into whether this meets our AI use policy)
Course 2 — Prompt Copilot to Draft Usable Project Plans
course_id: pm_c2_strategic_prompting
role_id: pm
primary_domain: strategic_prompting
sequence_order: 2
title: Prompt Copilot to Draft Usable Project Plans
tagline: Turn vague project asks into clear, structured outputs that save time.
description: PMs create high-level plans, job aids, process maps, and internal communications. This course teaches the CRAF Framework for prompting AI to generate usable project planning outputs with the right audience, constraints, format, and governance context built in from the start.
real_use_case: Co pilot for Program Management
Course 3 — Review AI Briefs Like an Executive Editor
course_id: pm_c3_critical_eval
role_id: pm
primary_domain: critical_eval
sequence_order: 3
title: Review AI Briefs Like an Executive Editor
tagline: Catch the subtle errors before leaders act on the summary.
description: PMs often prepare executive or steering summaries from large volumes of project information. This course teaches a disciplined review method for checking AI-generated briefings against source data, approved plans, status logic, and actual decisions before any executive audience sees them. %20-%20Job%20Aid.pdf?web=1)
real_use_case: Executive Brief Summaries
Course 4 — Use AI Recaps to Align Stakeholders Fast
course_id: pm_c4_relationship_intel
role_id: pm
primary_domain: relationship_intel
sequence_order: 4
title: Use AI Recaps to Align Stakeholders Fast
tagline: Tailor one set of facts into the right message for each stakeholder group.
description: PM work depends on alignment across sponsors, delivery teams, SMEs, and support functions. This course teaches learners how to use AI to turn fragmented updates into stakeholder-specific briefing packs, highlight dependencies, and prepare targeted communications without losing nuance or trust. This course is synthesized from PM workflow evidence because the library has no strong PM-specific relationship-intelligence anchor.
real_use_case: Customer Interaction Recap
Course 5 — Use AI to Surface Portfolio Signals Early
course_id: pm_c5_data_decision
role_id: pm
primary_domain: data_decision
sequence_order: 5
title: Use AI to Surface Portfolio Signals Early
tagline: Turn portfolio data into action before risks become surprises.
description: PMs and program leads rely on Planview reporting and status data to spot risk, resource strain, schedule drift, and escalation needs. This course teaches how to use AI to interpret patterns in reporting data, distinguish signal from noise, and turn that into evidence-based recommendations. %20-%20Job%20Aid.pdf?web=1)
real_use_case: Automated Portfolio Reporting Agent
Course 6 — Turn Meetings into Actions with AI Recaps
course_id: pm_c6_augmented_comm
role_id: pm
primary_domain: augmented_comm
sequence_order: 6
title: Turn Meetings into Actions with AI Recaps
tagline: Build a clean M365 workflow from live discussion to follow-up.
description: PMs spend large amounts of time moving from meetings to summaries, actions, emails, and records. This course teaches how to choose the right M365 Copilot surface and chain outputs across Teams, Word, PowerPoint, Outlook, and project records so communication work is faster, cleaner, and easier to govern. %20-%20Job%20Aid.pdf?web=1)
real_use_case: Meeting "Recap" feature in MS-Teams for Project Managers /Scrum Masters (PMs / SMs)
Course 7 — Run a Program Week with Copilot Safely
course_id: pm_c7_capstone
role_id: pm
primary_domain: capstone
sequence_order: 7
title: Run a Program Week with Copilot Safely
tagline: Plan, recap, report, and escalate across one realistic PM workflow.
description: This capstone integrates all six domains in a single PM workflow: use AI to prepare planning outputs, recap meetings, maintain governance-ready records, interpret portfolio signals, and communicate clearly without breaking policy or trusting AI blindly. It reflects the real rhythm of PM work across planning, execution, reporting, and stakeholder alignment. %20-%20Job%20Aid.pdf?web=1)
real_use_case: Co pilot for Program Management; Meeting "Recap" feature in MS-Teams for Project Managers /Scrum Masters (PMs / SMs); Record governance - Summarizing Meeting notes and actions (with attendees tagged); Automated Portfolio Reporting Agent
SECTION D — All 7 Scenario Seeds
Course 1 Scenario
scenario_text: You have just finished a weekly delivery meeting for the fictional internal initiative Atlas Delivery Renewal. The Teams meeting was recorded and transcribed. The discussion included open vendor issues, tentative budget pressures, and comments from the sponsor about options not yet approved. You want to use AI to generate the meeting notes quickly, but you are under pressure to send a recap today.
task_1_text: Identify which parts of the meeting content are safe to use directly in an approved AI workflow and which parts require abstraction or extra caution.
task_2_text: Write a safe prompt for an approved AI tool to draft internal meeting notes without exposing unnecessary non-public detail.
task_3_text: Review a draft AI recap and mark any sentence that should not be forwarded as-is because it contains unsupported, sensitive, or incomplete information.
task_4_text: Produce a final short note to the team that keeps the useful actions and decisions while removing or rewriting risky content.
coach_system_prompt: You are an AI skills coach for EDC Project and Program Managers. The learner is practicing safe AI use with meeting transcripts and project records. Do not write the final answer for them. Ask guiding questions that help them classify data, choose approved use patterns, and keep human review in place. Flag any attempt to paste real non-public data, real employee information, actual customer information, credentials, contract clauses, or sensitive financial details. If the learner ignores policy risk, redirect them to the public/non-public test and manual review requirement.
role_variants_hint: For other internal delivery roles, keep {org_type} as an internal program and replace {case_type} with that role’s main governed artifact, such as “architecture review notes” or “change impact summary.”
Course 2 Scenario
scenario_text: You are preparing the planning package for NorthBridge CRM Release 2, a fictional internal initiative moving from planning into delivery. You have a rough scope statement, three expected milestones, a few dependency notes, and a sponsor request for a one-page high-level plan by tomorrow morning. You want AI to help draft the first version, but your first instinct is to type “build me a project plan” and hope for the best.
task_1_text: Write a CRAF prompt that asks AI to produce a one-page high-level project plan with milestones, dependencies, assumptions, and decision points.
task_2_text: Revise the prompt so the output is written for a sponsor, not a delivery team, and excludes unnecessary implementation detail.
task_3_text: Add constraints so the AI output matches EDC-style planning needs: concise, structured, and clear about unresolved dependencies and required approvals.
task_4_text: Your output still feels generic. Rewrite the weakest part of your prompt so the plan becomes specific enough to use with minor edits.
coach_system_prompt: You are an AI skills coach for EDC Project and Program Managers practicing the CRAF Framework. Do not draft the prompt for them. Help them strengthen Context, Role, Action, and Format step by step. If they forget audience, constraints, or decision needs, ask what the sponsor actually needs to know. Flag if they try to include real sensitive data or confidential vendor content.
role_variants_hint: For non-PM roles, keep the same prompt structure but replace {case_type} with the role’s core output, such as “analysis memo,” “product brief,” or “operations runbook.”
Course 3 Scenario
scenario_text: You are building an executive update for Summit Portfolio Review, a fictional quarterly review of several internal initiatives. An AI tool has already generated a concise summary from portfolio notes, meeting recaps, and status updates. It reads well, but you notice it may be too confident in a few places and might have blended separate issues into one story. Leaders will use this summary to decide where to focus attention.
task_1_text: Identify the three biggest risks of forwarding the AI summary without review.
task_2_text: Apply a verification method to check the summary against source categories: approved baseline, current status, decisions made, and unresolved risks.
task_3_text: Rewrite two sentences that overstate certainty, invent causality, or blur together unsupported points.
task_4_text: Produce a final executive summary that is shorter, more defensible, and clearly anchored in what is actually known.
coach_system_prompt: You are an AI skills coach for EDC Project and Program Managers practicing critical evaluation. Do not rewrite the learner’s full summary. Guide them to test claims against source evidence, separate verified facts from inference, and remove unsupported wording. Watch for blind trust in fluent AI language.
role_variants_hint: For analyst or advisory roles, replace {case_type} with “briefing note” or “analysis summary,” but keep the same verification discipline around source-backed claims.
Course 4 Scenario
scenario_text: You are preparing a stakeholder briefing pack for Horizon Service Transition, a fictional internal service change involving delivery, operations, change, and finance teams. Everyone needs a different version of the story: sponsors need decisions, operations needs readiness impacts, and the delivery team needs dependency clarity. You are tempted to send the same AI-generated recap to everyone because time is tight.
task_1_text: Map the main stakeholder groups and state what each one needs most from the briefing.
task_2_text: Write a prompt that asks AI to produce separate briefing sections for sponsor, operations, and delivery audiences from the same source notes.
task_3_text: Adjust the output so it highlights dependency risks and decision needs without blaming any group or creating unnecessary tension.
task_4_text: Create a short sponsor note and a short delivery-team note that use the same facts but different framing and detail levels.
coach_system_prompt: You are an AI skills coach for EDC Project and Program Managers practicing stakeholder-focused communication. Do not produce the final briefs. Help the learner distinguish audience needs, decision authority, and dependency context. Watch for over-sharing, one-size-fits-all messaging, or content that could damage trust between teams.
role_variants_hint: For customer-facing roles, replace {org_type} with a fictional external company and shift the stakeholder map toward client, partner, and internal support teams.
Course 5 Scenario
scenario_text: You are reviewing a fictional dashboard for Beacon Capacity Dashboard that shows project effort, overall status, and a few red signals across the portfolio. An AI assistant has summarized the dashboard and suggested which initiatives need escalation. You know the numbers matter, but you also know that PM judgment matters because some red indicators are expected and some are noise.
task_1_text: Identify which dashboard signals are descriptive, which are predictive, and which need more context before action.
task_2_text: Write a prompt asking AI to compare projects based on schedule drift, resource strain, and status trend while avoiding unsupported ranking language.
task_3_text: Review an AI-generated priority list and explain where it may be misleading because it lacks baseline or business context.
task_4_text: Write a short recommendation for leadership that names one project to watch, one to escalate, and one to leave alone—for reasons grounded in the data and context.
coach_system_prompt: You are an AI skills coach for EDC Project and Program Managers practicing AI-assisted decision support. Do not choose the projects for them. Help them separate signal from noise, validate AI interpretations against known context, and avoid overconfident conclusions from incomplete data.
role_variants_hint: For finance or analytics roles, keep the decision logic but replace {case_type} with “variance review,” “forecast pack,” or “dashboard commentary.”
Course 6 Scenario
scenario_text: You have just run the fictional Maple Program SteerCo meeting. The discussion produced decisions, follow-ups, open issues, and one unresolved sponsor request. Your job is to turn that into a clean communication chain: meeting recap, action list, and follow-up email. You could copy and paste manually across tools, but that will take too long and increases the chance of inconsistency.
task_1_text: Choose the best M365 Copilot surface for each step: recap, formal notes, slide-ready summary, and follow-up email.
task_2_text: Draft the workflow order that turns one meeting into multiple outputs with minimal duplication.
task_3_text: Improve an AI-generated follow-up email so it is clear, accurate, and aligned with the recap and action log.
task_4_text: Produce a final mini-workflow that shows how you would move from Teams recap to Word notes to Outlook follow-up while keeping governance and traceability intact.
coach_system_prompt: You are an AI skills coach for EDC Project and Program Managers practicing multi-step M365 communication workflows. Do not write the final workflow or email. Ask the learner to justify tool choice, sequence, and review steps. Watch for inconsistent outputs, loss of decisions between steps, or attempts to skip validation.
role_variants_hint: For roles that do less meeting governance, replace {case_type} with that role’s main communication chain, such as “analysis to slide deck” or “customer call to CRM note to email.”
Course 7 Scenario
scenario_text: It is a high-pressure week for Polaris Transformation Wave, a fictional internal program. On Monday you need a refreshed planning summary. On Wednesday you need accurate meeting recaps and action tracking. On Thursday you need a sponsor briefing that reflects new risks. On Friday you must review portfolio signals and prepare the monthly status update. AI could help at every step—but only if you use it safely, prompt it well, verify it carefully, tailor it to stakeholders, and choose the right tool each time.
task_1_text: Outline the end-to-end AI workflow you would use across the week, naming the domain discipline needed at each step.
task_2_text: Write one safe, structured prompt for the planning step and one for the sponsor briefing step.
task_3_text: Review a flawed AI output set containing an inaccurate recap, an overstated executive summary, and a weak escalation recommendation; mark what must be fixed and why.
task_4_text: Produce a final PM work package consisting of a one-paragraph status update, three action items, one sponsor ask, and one note on how you kept the workflow policy-safe.
coach_system_prompt: You are an AI skills coach for EDC Project and Program Managers in a capstone exercise. Do not solve the case for them. Help them sequence the workflow, apply the right framework at the right moment, and reflect on tradeoffs. Watch for policy breaches, shallow prompts, unverified claims, weak stakeholder targeting, and poor tool choices.
role_variants_hint: For any other role, keep the end-to-end structure but swap the weekly workflow moments for that role’s real operating cycle—intake, analysis, review, communication, and decision support.
SECTION E — All 7 Reading Concept Specs
Course 1 Reading
framework_name: The SAFE Abstraction Method
concept_text: PMs often work with AI at the exact point where speed and risk collide: meeting transcripts, status notes, RAID items, and sponsor commentary. The SAFE Abstraction Method gives a practical sequence for handling that tension. S — Scan the source for non-public content such as internal budgets, draft decisions, vendor issues, or named individuals. A — Abstract anything the AI does not need in exact form; replace names, dollar figures, or confidential identifiers with neutral descriptions. F — Fit the task to an approved tool and approved purpose. If the task is inside an approved M365 workflow, proceed; if it depends on an unapproved external surface, stop. E — Evaluate the output before use. PMs are not allowed to use AI output without manual review, and that matters most when the output becomes a record, a decision input, or a leadership communication. SAFE is not about making AI useless—it is about preserving utility while removing avoidable exposure. In PM work, the goal is usually not to tell AI every detail; it is to tell AI enough to produce a usable draft that you then review and finalize.
good_example: Before: “Summarize this transcript from our red project. Include the sponsor’s comments on vendor underperformance and the budget gap.” After: “Using this approved internal transcript excerpt, draft internal meeting notes with decisions, actions, and unresolved risks. Do not include named individuals or exact budget figures. Mark any unclear point as ‘needs confirmation.’” Why it works: it abstracts sensitive details, stays inside an approved internal-use pattern, and leaves room for human review.
anti_pattern: A PM pastes a raw transcript with internal budget pressures and vendor comments into the wrong AI surface, then forwards the output as meeting minutes without checking it. Consequence: policy breach risk, loss of context, and inaccurate records that others may treat as final.
takeaway: AI can speed up recap work, but only when PMs scan, abstract, fit to approved use, and evaluate before sharing.
Course 2 Reading
framework_name: CRAF Framework
concept_text: PMs rarely need “more words”; they need the right output—a sponsor-ready one-pager, a milestone plan, a process map draft, or a concise status narrative. The CRAF Framework helps produce that. C — Context: what initiative, what stage, what source inputs, what audience? R — Role: who should the AI act like—an enterprise PM, a PMO analyst, a steering-deck writer? A — Action: what exactly should it create—high-level plan, RAID narrative, stakeholder summary, milestone list? F — Format: how should the result be structured—bullet list, one-page summary, three headers, table draft? PM prompts fail when they skip context, bury the audience, or never state the actual deliverable. PM work also benefits from explicit constraints: “keep unresolved dependencies visible,” “do not invent dates,” or “flag any assumption.” Good prompting is not fancy prompting. It is disciplined specification of what matters. For PMs, that is especially important because planning outputs become governance inputs and downstream records. A weak prompt creates rework; a strong one creates a usable first draft.
good_example: “Context: internal CRM release planning, Stage 2, sponsor needs a one-page high-level plan today. Role: experienced enterprise PM. Action: draft a concise plan with milestones, dependencies, assumptions, and decisions needed. Format: four sections with bullets, max 250 words, no invented dates.” Why it works: it tells AI the situation, voice, deliverable, and structure.
anti_pattern: “Build me a project plan.” Consequence: generic output, missing governance context, missing audience fit, and more rewriting than manual drafting would have required.
takeaway: PM prompting improves when you specify the project context, the AI’s role, the exact artifact, and the structure you need.
Course 3 Reading
framework_name: VERIFY Checklist
concept_text: AI-generated PM outputs often fail in believable ways. They sound polished, but the risk is not obvious nonsense—it is subtle distortion: a decision stated too strongly, a dependency implied but never confirmed, an issue merged with a risk, or a status narrative that sounds more certain than the data supports. The VERIFY Checklist helps PMs review AI output before it influences action. V — Verify facts against source material. E — Examine omissions to see what is missing, not just what is wrong. R — Review ownership so actions, decisions, and escalations are assigned correctly. I — Inspect tone and certainty to remove overclaiming language. F — Find unsupported inference where the AI connected dots that the source never connected. Y — Yield only the defensible version—the version you could stand behind in a meeting. PMs need VERIFY because project communication is often used downstream by leaders, teams, and governance functions. A fluent but flawed summary can push a bad escalation, a wrong action owner, or a false sense of control. Critical evaluation is not about distrusting AI completely; it is about trusting it only after disciplined review. %20-%20Job%20Aid.pdf?web=1)
good_example: Before sending an executive update, the PM checks each sentence against the approved baseline, current status notes, and meeting outcomes, then changes “the vendor issue is resolved” to “the vendor mitigation plan is in progress; resolution is not yet confirmed.” That small edit prevents a misleading summary.
anti_pattern: Forwarding an AI-generated executive summary because it “sounds right” without checking whether the actions, decisions, and red indicators match the actual source material. Consequence: leadership acts on a narrative that was never verified.
takeaway: The best PM summary is not the most polished one—it is the one that remains true under scrutiny.
Course 4 Reading
framework_name: ALIGN Map
concept_text: PMs manage work through people. The same project fact means different things to different audiences. A sponsor wants decision clarity. Operations wants readiness impacts. Delivery teams want dependencies and timing. Finance wants variance explanation. The ALIGN Map helps PMs use AI to tailor the same core facts without fragmenting truth. A — Audience: who is this for? L — Lens: what does that audience care about most—decision, readiness, risk, timeline, budget? I — Impact: what changes for them because of this update? G — Gaps: what do they still need to know or decide? N — Next message: what is the most useful next communication? ALIGN prevents the common PM failure of sending the same generic recap to everyone. AI can help create multiple versions quickly, but PM judgment still decides the framing, emphasis, and detail level. ALIGN also supports relationship health: it avoids blaming language, reduces confusion, and helps each group feel seen in the communication. In internal programs, good stakeholder intelligence is often the difference between smooth coordination and recurring friction.
good_example: From one meeting recap, the PM generates: a sponsor note focused on decisions needed and risk impact; an operations note focused on cutover readiness; and a delivery note focused on blockers and dependencies. Same facts, different lens, no contradiction.
anti_pattern: Sending one AI-generated “all audience” summary to sponsors, delivery, and operations. Consequence: each group misses what matters most, and the PM creates more follow-up noise.
takeaway: AI helps stakeholder alignment only when the PM intentionally changes the lens, not the truth.
Course 5 Reading
framework_name: SIGNAL Review
concept_text: PMs are surrounded by status signals: red/green indicators, cost drift, schedule variance, resource strain, monthly reporting periods, and portfolio dashboards. AI can summarize those quickly, but PMs still need a decision method. SIGNAL Review is built for that. S — Source: where did the data come from—Planview, status update, dashboard extract? I — Indicator: what exactly is changing—cost, schedule, scope, resource, overall status? G — Ground truth: what baseline or business context explains the signal? N — Noise check: could the signal be expected, temporary, or misleading? A — Action: what management action follows—watch, correct, escalate, re-baseline? L — Leadership message: what do stakeholders need to hear in plain language? SIGNAL matters because PMs do not manage dashboards; they manage outcomes. A red signal is not automatically failure, and a green signal is not automatically safe. AI can help spot patterns and draft commentary, but PMs must interpret what is meaningful. Especially in portfolio settings, weak AI interpretation can turn routine variation into drama or hide real escalation needs under smooth wording. %20-%20Job%20Aid.pdf?web=1)
good_example: The dashboard shows schedule drift outside tolerance. The PM checks whether the project has already been re-baselined, confirms the forecasted end date versus baseline, and writes a short escalation note that explains both the data and the business consequence.
anti_pattern: Accepting an AI-generated “top three problem projects” list without checking baseline dates, known phase changes, or whether a red signal was already expected.
takeaway: Data-driven PM decisions come from interpreting signals with context, not from ranking charts at face value.
Course 6 Reading
framework_name: Copilot Surface Selector
concept_text: PM communication work becomes expensive when the same content is rewritten in every tool. The Copilot Surface Selector helps PMs choose the best M365 entry point for the job and build a clean chain across tools. Use Teams when the source is a meeting and you need recap or action capture. Use Word when the output must become a formal document, structured notes, or a controlled record. Use PowerPoint when the message must be consumed quickly by leaders in a visual format. Use Outlook when the final step is stakeholder follow-up or confirmation. Then connect them deliberately: meeting recap to formal notes, formal notes to sponsor slide, sponsor slide to follow-up email. The key skill is not knowing every feature. It is knowing the input type, the output goal, and the review point where human judgment stays in control. PMs benefit because they spend so much time converting one discussion into multiple communications. A good multi-step workflow reduces duplicate manual work, preserves consistency, and makes governance easier because each output traces back to a known source. %20-%20Job%20Aid.pdf?web=1)
good_example: Teams recap drafts action items from the meeting. Word turns the same content into formal minutes. Outlook uses the final reviewed minutes to draft a concise follow-up email. Each step is shorter because the previous one already did part of the work.
anti_pattern: Copying raw AI recap text from Teams directly into an email and then separately rebuilding the same content in a slide deck. Consequence: inconsistent wording, missing actions, and more manual cleanup.
takeaway: The right Copilot surface is the one that matches your source, your audience, and the next step in the workflow.
Course 7 Reading
framework_name: End-to-End AI Workflow
concept_text: PM work is not one AI moment. It is a chain. The best results come when each domain is applied at the right point in the workflow. Start with Responsible AI to decide what can safely be used and in which tool. Move to Strategic Prompting to generate a useful planning or briefing draft. Apply Critical Evaluation before any output becomes a record or decision input. Use Relationship Intelligence to shape the message for the right stakeholder. Use Data-Driven Decision Making to interpret signals, not just summarize them. Finish with Augmented Communication to move the work through the right M365 surfaces without duplicating effort. PMs need this end-to-end mindset because their outputs are interconnected. A recap becomes an action list. An action list becomes a status narrative. A status narrative becomes an executive message. One weak step contaminates the rest of the chain. The capstone framework teaches learners to think in sequence: what is the task, what is the risk, what is the right tool, what needs review, and who needs the final message? When PMs do this well, AI becomes a workflow accelerator rather than a workflow hazard. %20-%20Job%20Aid.pdf?web=1)
good_example: A PM safely abstracts meeting content, prompts AI for a concise recap, checks it against source notes, tailors the summary for the sponsor, then uses the right Copilot surfaces to create the final status update and follow-up email.
anti_pattern: Using AI separately in random places—one prompt for a plan, another for an email, another for a dashboard narrative—with no safety check, no validation, and no workflow logic. Consequence: fast fragments, weak control.
takeaway: PM AI maturity is not one skill. It is the ability to connect six skills across one governed workflow.
SECTION F — Diagnostic Item Seeds (18 items: 3 per domain × 6 domains)
Diagnostic: responsible_ai
Item 1 — type: mcq
question_text: A PM wants to use AI to draft meeting minutes from an internal project transcript that includes budget concerns and unapproved vendor options. What is the safest first action?
options:
A) Paste the full transcript into any AI tool because the output is only for internal use
B) Apply the public/non-public test, stay in an approved tool, and abstract details the AI does not need
C) Remove only the people names and keep all other exact details
D) Ask a colleague to use their personal device instead
correct_option: B
Item 2 — type: prompt_sandbox
scenario_text: You have a transcript from an internal delivery meeting with open risks, tentative options, and draft sponsor comments.
question_text: Write a safe prompt for an approved AI tool to draft internal meeting notes without exposing unnecessary non-public detail.
scoring rubric criteria:

Identifies that the task must stay within an approved AI workflow
Abstracts or excludes sensitive details not needed for the output
Requests a clearly bounded internal-use deliverable
Includes a cue for manual review or uncertainty handling
Item 3 — type: micro_task
scenario_text: A PM writes: “Summarize this full transcript and send polished minutes to the whole steering group. Include every budget detail and vendor option.”
question_text: Rewrite the instruction so it is policy-safer while still useful for drafting internal notes.
scoring rubric criteria:

Removes or abstracts sensitive project details
Keeps the task inside an approved internal-use pattern
Narrows the deliverable to what is needed
Preserves a human review step before sharing
Diagnostic: strategic_prompting
Item 1 — type: mcq
question_text: Which missing element most often causes AI-generated project plans to feel generic?
options:
A) Font preference
B) Context about the initiative stage, audience, and deliverable
C) Use of exclamation points
D) Asking for British spelling
correct_option: B
Item 2 — type: prompt_sandbox
scenario_text: You need a one-page high-level plan for a fictional internal initiative starting delivery next month.
question_text: Write a CRAF-style prompt that asks AI to produce a sponsor-ready high-level plan with milestones, dependencies, and decisions needed.
scoring rubric criteria:

Includes specific context about the initiative and audience
Includes a role instruction
Defines a concrete action and deliverable
Specifies a clear structure or output format
Item 3 — type: micro_task
scenario_text: Prompt used: “Create a project plan.” Output: a long, generic essay on project management best practices.
question_text: In one or two sentences, explain why the output is weak and name the two CRAF elements most clearly missing.
scoring rubric criteria:

Correctly identifies weak or missing context
Correctly identifies weak or missing action/format
Explains why the generic output happened
Uses PM-specific language rather than abstract prompt theory
Diagnostic: critical_eval
Item 1 — type: mcq
question_text: Why is fluent AI language especially risky in PM executive summaries?
options:
A) It makes the summary too short
B) It can hide unsupported assumptions behind polished wording
C) It prevents copy-paste
D) It always uses too many bullets
correct_option: B
Item 2 — type: prompt_sandbox
scenario_text: An AI-generated status summary says a vendor issue is resolved, but your notes only say a mitigation plan was discussed.
question_text: Write a prompt asking AI to regenerate the summary with stricter evidence handling and clear uncertainty language.
scoring rubric criteria:

Requests evidence-bound wording
Instructs the AI to flag uncertainty rather than invent closure
Keeps the scope limited to source-backed content
Specifies an output style suitable for PM reporting
Item 3 — type: micro_task
scenario_text: AI summary sentence: “Leadership approved the revised scope and the delay is now contained.” Source notes show: “leadership requested a revised scope option for next meeting; delay impact under review.”
question_text: Correct the AI sentence so it matches the source.
scoring rubric criteria:

Removes unsupported approval claim
Removes unsupported certainty about delay containment
Preserves what the source actually says
Uses concise PM reporting language
Diagnostic: relationship_intel
Item 1 — type: mcq
question_text: A sponsor, an operations lead, and a delivery lead all need an update from the same meeting. What is the best PM approach?
options:
A) Send the identical recap to all three to save time
B) Use the same facts but tailor emphasis and asks to each audience
C) Give the sponsor the longest version and everyone else nothing
D) Ask AI to choose the audience for you
correct_option: B
Item 2 — type: prompt_sandbox
scenario_text: You need AI to create a sponsor note and a delivery-team note from the same internal project recap.
question_text: Write a prompt that asks for two audience-specific outputs with different focus areas but consistent facts.
scoring rubric criteria:

Names at least two distinct audiences
Specifies what each audience cares about
Preserves one factual base across both outputs
Avoids blame or over-sharing
Item 3 — type: micro_task
scenario_text: Draft line for all audiences: “Everything is progressing well, though some teams need to move faster.”
question_text: Rewrite this into a sponsor-facing line and a delivery-facing line.
scoring rubric criteria:

Tailors the sponsor version to decision or risk visibility
Tailors the delivery version to actionable coordination
Avoids vague blame language
Keeps both lines aligned to the same core facts
Diagnostic: data_decision
Item 1 — type: mcq
question_text: What is the PM’s main job when using AI with portfolio status data?
options:
A) Accept the ranking with the highest confidence score
B) Turn every red signal into an escalation
C) Interpret the signals against baseline and business context before recommending action
D) Remove all data that looks negative
correct_option: C
Item 2 — type: prompt_sandbox
scenario_text: You have project data on overall status, schedule variance, and resource strain across five initiatives.
question_text: Write a prompt asking AI to identify which initiatives likely need watch, correction, or escalation—without inventing unsupported ranking logic.
scoring rubric criteria:

Specifies the decision categories or output structure
Tells AI to use evidence from provided metrics only
Requests uncertainty or caution where context is missing
Avoids overclaiming or unsupported prioritization language
Item 3 — type: micro_task
scenario_text: AI output: “Project A is clearly the highest priority problem because it is red.” Context you know: Project A was intentionally marked red to surface support needs early, while Project B has hidden resource strain but remains green.
question_text: Explain why the AI conclusion is weak and what additional context is needed.
scoring rubric criteria:

Identifies that colour alone is not enough
Recognizes the need for baseline and management context
Distinguishes signal from noise
Suggests a better evidence check before action
Diagnostic: augmented_comm
Item 1 — type: mcq
question_text: Which tool sequence is most sensible for turning one PM meeting into final follow-up communication?
options:
A) Outlook first, then Teams, then ignore formal notes
B) Teams recap, then formal notes in Word, then follow-up in Outlook
C) PowerPoint first, then raw chat copy
D) Excel only
correct_option: B
Item 2 — type: prompt_sandbox
scenario_text: You have just completed a steering meeting and need actions, formal notes, and a short follow-up email.
question_text: Write a prompt for Teams Copilot to generate the recap you would use as the first step in a broader communication workflow.
scoring rubric criteria:

Requests decisions, actions, and unresolved points clearly
Keeps the recap concise and structured
Prepares the output for downstream reuse
Signals the need for review before reuse
Item 3 — type: micro_task
scenario_text: Teams recap says “Action owner to be confirmed.” Your follow-up email draft says “Jordan will complete the task by Friday.”
question_text: Correct the communication chain so the email does not overstate what the recap actually confirmed.
scoring rubric criteria:

Detects the inconsistency across tools
Revises the email to match verified content
Keeps the message clear and useful
Preserves governance discipline across outputs
SECTION G — Evaluation Item Seeds (28 items: 4 per course × 7 courses)
Evaluation: Course 1
Item 1 — type: mcq, sequence: 1
question_text: Which statement best reflects EDC policy for Gen AI output used at work?
options:
A) It can be used without review if the audience is internal
B) It must always be manually reviewed before use
C) It may be trusted if the vendor is well known
D) It is safe if you remove people names only
correct_option: B
explanation: EDC’s policy requires manual human review before using or transmitting AI-generated content for work.
Item 2 — type: mcq, sequence: 2
question_text: A PM wants AI help on meeting notes that include budget pressure and draft options. What is the safest pattern?
options:
A) Paste everything into a public AI tool and clean it later
B) Use an approved tool, abstract unnecessary details, then review the output
C) Ask another employee to do it off network
D) Skip all abstraction because it is “just recap work”
correct_option: B
explanation: SAFE starts with data classification and abstraction, then keeps the task in an approved tool with manual review.
Item 3 — type: mcq, sequence: 3
question_text: Which of the following is the strongest red flag in a PM AI workflow?
options:
A) Asking for bullets instead of paragraphs
B) Using an approved internal tool to draft notes
C) Inputting non-public EDC information into the wrong AI surface
D) Requesting a short summary
correct_option: C
explanation: The core policy risk is exposing non-public EDC information in unapproved AI tools or workflows.
Item 4 — type: performance_task, sequence: 4
question_text: You have an internal transcript from a delivery meeting that includes tentative budget pressure, vendor issues, and unapproved next-step options. Write a short response showing: (1) what you would abstract, (2) what approved-use assumption you are making, (3) the safe prompt you would use for drafting notes, and (4) the review step you would take before sharing.
scoring rubric:
key1: Clearly distinguishes sensitive/non-public project content from lower-risk content
key2: Uses an approved internal-use pattern and does not rely on an unsafe tool assumption
key3: Writes a bounded prompt that abstracts or excludes unnecessary sensitive details
key4: Includes a manual review step that checks accuracy and appropriateness before sharing
Evaluation: Course 2
Item 1 — type: mcq, sequence: 1
question_text: In the CRAF Framework, which element most directly controls the structure of the output?
options:
A) Context
B) Role
C) Action
D) Format
correct_option: D
explanation: Format tells the AI how the response should be organized, sized, and presented.
Item 2 — type: mcq, sequence: 2
question_text: A PM prompt produces a generic essay instead of a sponsor-ready plan. Which change is most likely to fix it?
options:
A) Add emoji
B) Specify the audience, deliverable, and output structure
C) Remove all context
D) Ask for “better quality”
correct_option: B
explanation: Sponsor audience, concrete artifact, and structure are the core controls that make planning prompts usable.
Item 3 — type: mcq, sequence: 3
question_text: Why is a role instruction useful in PM prompting?
options:
A) It guarantees no hallucinations
B) It tells the AI to be shorter
C) It helps calibrate perspective, vocabulary, and relevance
D) It replaces the need for context
correct_option: C
explanation: Role sets the lens and implied expertise of the output but does not replace context or validation.
Item 4 — type: performance_task, sequence: 4
question_text: You need a one-page high-level plan for a fictional internal initiative entering delivery next month. The sponsor wants milestones, dependencies, assumptions, and decisions needed. Write a full CRAF prompt that would generate a usable first draft.
scoring rubric:
key1: Context clearly states initiative stage, audience, and purpose
key2: Role instruction is relevant to PM work
key3: Action specifies the exact artifact and content needed
key4: Format defines a concise structure suitable for sponsor review
Evaluation: Course 3
Item 1 — type: mcq, sequence: 1
question_text: Which flaw is most dangerous in an AI-generated executive summary?
options:
A) Slightly formal tone
B) Unsupported certainty stated as fact
C) Too many bullet points
D) Passive voice
correct_option: B
explanation: Executive summaries are risky when they overstate certainty or invent conclusions leaders may act on.
Item 2 — type: mcq, sequence: 2
question_text: What is the “E” in VERIFY mainly reminding the PM to check?
options:
A) Emoji use
B) Expenditure coding only
C) Omissions and missing context
D) Export settings
correct_option: C
explanation: Evaluation is not just spotting errors; it is checking what the AI left out that still matters.
Item 3 — type: mcq, sequence: 3
question_text: A summary says “scope is contained” but the source notes say “scope options under review.” What should the PM do?
options:
A) Keep the stronger wording because it sounds confident
B) Rewrite the sentence to match the source and show uncertainty
C) Delete the whole summary
D) Add more adjectives
correct_option: B
explanation: PM review must reduce unsupported certainty and restore source-accurate language.
Item 4 — type: performance_task, sequence: 4
question_text: You are given a short AI-generated executive update that overstates decisions, hides one unresolved dependency, and assigns an action to the wrong owner. Rewrite it into a defensible summary and briefly note what you changed.
scoring rubric:
key1: Removes unsupported or exaggerated claims
key2: Restores missing dependency or uncertainty
key3: Corrects ownership and action attribution
key4: Produces a concise executive-ready summary grounded in verifiable content
Evaluation: Course 4
Item 1 — type: mcq, sequence: 1
question_text: What is the PM risk of using the same AI-generated recap for sponsor, operations, and delivery audiences?
options:
A) The file size may be too small
B) Each audience may miss what matters most
C) AI will stop working
D) It will always become a slide deck
correct_option: B
explanation: One-size-fits-all messaging weakens stakeholder alignment because audiences need different emphasis.
Item 2 — type: mcq, sequence: 2
question_text: In the ALIGN Map, what does the “L” stand for?
options:
A) Length
B) Lens
C) Log-in
D) Language model
correct_option: B
explanation: Lens means the viewpoint or priority that matters most to a given audience.
Item 3 — type: mcq, sequence: 3
question_text: Which PM behavior best reflects relationship intelligence?
options:
A) Reusing the same note for everyone
B) Tailoring the same facts to different stakeholder needs
C) Letting AI choose who needs the message
D) Removing all nuance for speed
correct_option: B
explanation: Relationship intelligence is about audience fit, not changing the underlying facts.
Item 4 — type: performance_task, sequence: 4
question_text: From one fictional internal project recap, create two short outputs: a sponsor note focused on decisions and risk, and a delivery-team note focused on dependencies and next actions.
scoring rubric:
key1: Differentiates audience needs clearly
key2: Keeps the factual core consistent across both outputs
key3: Uses appropriate tone and detail level for each audience
key4: Avoids blame, vague language, or missing next steps
Evaluation: Course 5
Item 1 — type: mcq, sequence: 1
question_text: Which statement best reflects good PM use of AI with dashboard signals?
options:
A) Red always means immediate escalation
B) AI ranking is enough for action
C) Signals must be interpreted against baseline and context
D) Green always means no action needed
correct_option: C
explanation: PM judgment depends on context, not colour alone.
Item 2 — type: mcq, sequence: 2
question_text: In SIGNAL Review, which step asks whether a red signal may be expected or misleading?
options:
A) Source
B) Noise check
C) Action
D) Leadership message
correct_option: B
explanation: Noise check separates routine or explainable variation from meaningful escalation triggers.
Item 3 — type: mcq, sequence: 3
question_text: A schedule status is red because the forecasted end date is outside tolerance. What should the PM consider next?
options:
A) Whether the baseline itself changed or needs reapproval
B) Whether the colour looks bad in a slide
C) Whether the file should be archived
D) Whether the AI used more than 100 words
correct_option: A
explanation: Schedule signals only make sense relative to the approved baseline and re-baseline logic. %20-%20Job%20Aid.pdf?web=1)
Item 4 — type: performance_task, sequence: 4
question_text: You are given a fictional portfolio snapshot with three initiatives, each showing different mixes of schedule drift, resource strain, and overall status. Write a short recommendation naming one to watch, one to escalate, and one to leave alone, with evidence-based reasons.
scoring rubric:
key1: Correctly interprets the metrics rather than just restating them
key2: Shows awareness of baseline or management context
key3: Distinguishes watch/correct/escalate logic clearly
key4: Writes a concise leadership-ready recommendation
Evaluation: Course 6
Item 1 — type: mcq, sequence: 1
question_text: Which M365 surface is the best starting point when the source material is a recorded meeting?
options:
A) Outlook
B) Teams
C) Excel
D) None of them
correct_option: B
explanation: Teams is the natural entry point when the source is a meeting and recap or action capture is needed.
Item 2 — type: mcq, sequence: 2
question_text: Why should a PM avoid copying raw recap text straight into a stakeholder email?
options:
A) It may create inconsistency and skip review
B) Emails cannot contain summaries
C) Outlook removes bullets automatically
D) Teams outputs are never useful
correct_option: A
explanation: Good augmented communication keeps the chain consistent and reviewed before final use.
Item 3 — type: mcq, sequence: 3
question_text: What is the main value of a multi-step Copilot workflow for PMs?
options:
A) It makes meetings longer
B) It reduces duplicate writing while keeping outputs connected
C) It removes the need for governance
D) It avoids using Word or Outlook entirely
correct_option: B
explanation: PM communication work often repeats the same information in different forms; chaining tools reduces rework.
Item 4 — type: performance_task, sequence: 4
question_text: Design a short workflow for turning one steering meeting into (1) a reviewed recap, (2) formal notes, and (3) a follow-up email. Name the best tool for each step and explain one review control.
scoring rubric:
key1: Chooses sensible tools for source and output type
key2: Orders the steps logically
key3: Shows how outputs feed into later steps without duplication
key4: Includes a human review or consistency check before final communication
Evaluation: Course 7
Item 1 — type: mcq, sequence: 1
question_text: In an end-to-end PM AI workflow, which step should happen before prompting for content?
options:
A) Send the email
B) Apply the responsible AI screen to the source material
C) Escalate the issue
D) Build the slide deck
correct_option: B
explanation: Safe handling comes first; the workflow starts by checking what can be used and where.
Item 2 — type: mcq, sequence: 2
question_text: What most clearly shows multi-domain PM AI maturity?
options:
A) Using many tools randomly
B) Prompting, reviewing, tailoring, interpreting, and communicating in sequence
C) Writing the longest prompt possible
D) Trusting every AI recap
correct_option: B
explanation: Capstone performance is about applying the right discipline at the right workflow moment.
Item 3 — type: mcq, sequence: 3
question_text: Which of the following is the best sign that a PM workflow is still under human control?
options:
A) AI created the first draft quickly
B) The PM checked policy fit, validated claims, and adjusted outputs for audience and action
C) The PM used three different tools
D) The PM avoided all AI use
correct_option: B
explanation: The capstone is not about speed alone; it is about controlled, defensible workflow use.
Item 4 — type: performance_task, sequence: 4
question_text: You have one fictional PM workweek involving planning, meeting recap, sponsor briefing, portfolio review, and monthly status update. Describe the AI workflow you would use across the week and include: one safe-use check, one structured prompt, one verification step, one stakeholder tailoring move, one data interpretation step, and one communication chain choice.
scoring rubric:
key1: Sequences the workflow logically across the week
key2: Applies at least one concrete action from each relevant domain
key3: Keeps the workflow grounded in PM artifacts and tools
key4: Shows clear human judgment and control at every critical step


