## MACHINE-READABLE HEADER

role_prefix: an

company_map:
  course_1: KYC Onboarding Review
  course_2: Meridian Infrastructure Briefing
  course_3: Aurora Initiative Variance Analysis
  course_4: Risk Enablement Working Group
  course_5: Cascade Portfolio Q3 Analytics
  course_6: Enterprise Intelligence Program
  course_7: Horizon Program Annual Review

framework_names:
  - The SAFE Abstraction Method
  - CRAF Framework
  - VERIFY Checklist
  - STAKE Framework
  - TRACE Framework
  - Copilot Surface Selector
  - End-to-End AI Workflow

real_use_case:
  course_1: KYC / CIM Validation Agent
  course_2: Board Report Summaries
  course_3: Financial Variance Analyzer
  course_4: Access to Copilot 365 for Business Development
  course_5: Financial Variance Analyzer; Streamline production of Quarterly analysis and reporting
  course_6: Streamline production of Quarterly analysis and reporting
  course_7: Streamline production of Quarterly analysis and reporting; Financial Variance Analyzer; KYC / CIM Validation Agent

---

## SECTION A — Role Entry

role_id: an
title: Analyst (Non-IT)
description: "Produces research, financial models, risk assessments, and analytical reports (e.g., credit memos, performance dashboards, sector briefs) that inform decisions by internal stakeholders such as underwriters, account managers, and senior leadership. Works across diverse data sources (CRM records, financial statements, survey data, economic reports) and tools (Excel models, Power BI dashboards, SharePoint repositories) to synthesize insights. Does not manage external client relationships directly — outputs are internal deliverables that support decision-making in various business units (Risk Management, Finance, Business Development, etc.)."

---

## SECTION B — Domain Specs

### Domain: responsible_ai

domain_id: responsible_ai
title: Responsible AI
description: "Knowing which research inputs and outputs are safe to pass into AI tools — distinguishing publicly available sector data, published annual reports, and news sources from embargoed third-party research, unpublished financial models, draft strategy documents, and non-public client data. Applying the public/non-public test before prompting, abstracting confidential inputs while preserving analytical utility, and ensuring AI outputs are cleansed of sensitive data before distribution."
level_0_label: Unaware
level_0_descriptor: "Unaware of EDC's GenAI data restrictions. May paste confidential content (client financials, internal strategy documents, CRM exports, personal identifiers) into public AI tools or M365 Copilot prompts without consideration."
level_1_label: Explorer
level_1_descriptor: "Knows in theory that non-public information shouldn't be shared with AI, but struggles to identify what counts as sensitive in practice. May inadvertently include specific client names, deal amounts, or internal credit ratings in prompts, especially under time pressure."
level_2_label: Practitioner
level_2_descriptor: "Consistently applies the public/non-public test before using Copilot. Checks whether data comes from public sources (e.g., published annual reports, press releases) or is confidential (e.g., unpublished financial results, internal risk ratings, personally identifiable information). Uses safe prompting techniques: replaces specific identifiers with generic descriptors, uses ranges instead of exact figures, and reviews AI outputs for accidentally revealed confidential details before sharing."
level_3_label: Proficient
level_3_descriptor: "Preemptively identifies borderline cases and applies creative abstraction strategies — e.g., summarizing an internal report by providing only high-level trends or anonymized labels ('Client A' instead of the real name) to Copilot. Handles ambiguous cases confidently: errs on the side of caution or seeks guidance rather than guessing. Rewrites prompts to preserve analytical utility while removing compliance risk."
level_4_label: Champion
level_4_descriptor: "Serves as a go-to resource on GenAI data compliance for the analyst team. Anticipates novel data-safety challenges (e.g., AI summarisation of embargoed third-party sector reports). Creates team guidelines for anonymizing inputs and documents safe vs. unsafe input patterns. Demonstrates that high-quality analysis can be done with AI without ever exposing confidential information."

### Domain: strategic_prompting

domain_id: strategic_prompting
title: Strategic Prompting
description: "Structuring AI prompts with clear context, role, action, and format so that Copilot's outputs are immediately useful in an analyst's workflow — from summarizing complex financial reports and research documents to drafting internal memos, variance analyses, sector briefs, or slide notes for senior management."
level_0_label: Unaware
level_0_descriptor: "Has not used AI prompting in daily analytical tasks. May try one-word or very vague prompts and cannot describe what makes a prompt effective."
level_1_label: Explorer
level_1_descriptor: "Writes basic prompts ('Summarize this report') and gets generic or overly long outputs that require significant manual revision. Often unsure how to guide AI to specific insights or formats needed for internal stakeholders."
level_2_label: Practitioner
level_2_descriptor: "Uses structured prompts that provide context (dataset or report background), define the AI's role (financial analyst, risk advisor), specify the task (summary, analysis, draft), and request a clear format (bulleted list, table, executive summary). Output is usually on-point and needs only minor editing to be useful."
level_3_label: Proficient
level_3_descriptor: "Adapts and refines prompts for complex analytical scenarios. Anticipates when the AI might misinterpret a request and preempts issues with guiding details or constraints (excluding certain sections, targeting specific metrics or time periods). Iterates effectively when initial output misses the mark — producing high-quality drafts for internal reports or presentations."
level_4_label: Champion
level_4_descriptor: "Designs and shares effective prompt templates for common analyst tasks (financial analysis, risk memos, data quality summaries, board briefings). Coaches colleagues on the CRAF framework. Identifies new opportunities to use multi-step chained prompts to streamline analytical workflows across the team."

### Domain: critical_eval

domain_id: critical_eval
title: Critical Evaluation
description: "Reviewing and validating AI-generated outputs with a skeptical, data-driven eye before using them in analysis or reports. This includes catching hallucinated facts or figures, misinterpreted data trends, or incorrect statements in Copilot's summaries of financial data, risk reviews, meeting notes, and research findings — and correcting them before they reach internal stakeholders."
level_0_label: Unaware
level_0_descriptor: "Assumes Copilot's outputs are accurate by default. Tends to copy-paste AI-generated analysis or summaries (variance explanations, credit memo drafts) into deliverables without checking against source data or verifying claims."
level_1_label: Explorer
level_1_descriptor: "Skims AI outputs and corrects obvious mistakes like typos, but doesn't systematically verify facts or numbers. May overlook subtle errors in financial calculations or misattributed statements when reviewing AI-created content."
level_2_label: Practitioner
level_2_descriptor: "Consistently cross-checks key details from AI outputs against reliable sources. Compares Copilot's summarized financial figures or risk ratings to the original spreadsheet and CRM data, and removes or corrects any discrepancies. Understands that AI can generate plausible-sounding but incorrect explanations — verifies any reasoning (such as causes of a budget variance) by consulting the actual data or documents before presenting results."
level_3_label: Proficient
level_3_descriptor: "Routinely identifies subtle inaccuracies or implausible reasoning in AI outputs. Flags statements that don't align with source data (a trend not actually in the dataset, a misinterpreted KPI) and uses judgment to decide what to keep, correct, or discard. Re-prompts Copilot for source citations or reruns analyses with different parameters to validate findings. Prevents misinformation by requiring evidence for each major AI-generated insight."
level_4_label: Champion
level_4_descriptor: "Develops verification checklists or SOPs for the analyst team when using AI-generated content. Trains colleagues on common failure modes of AI in analytics (hallucinated numeric calculations, incorrect attributions in meeting notes). Advocates for source-citation features and helps establish a culture of 'trust but verify' across the team."

### Domain: relationship_intel

domain_id: relationship_intel
title: Relationship Intelligence
description: "Using AI to understand and serve the decision-making needs of internal stakeholders — researching audience priorities before delivering a briefing, tailoring analytical outputs to the specific framing that underwriters, account managers, or senior leaders need, and personalizing the depth, emphasis, and format of deliverables based on who will act on them. Applies to both written deliverables (briefings, memos, decks) and verbal briefings (committee prep, cross-functional meetings)."
level_0_label: Unaware
level_0_descriptor: "Has not used AI to research or prepare for internal stakeholder interactions. Delivers the same analytical format to all audiences without adapting to their specific decision-making context or known priorities."
level_1_label: Explorer
level_1_descriptor: "Uses AI to generate generic background on a topic or audience (e.g., 'summarize what underwriters care about'). Output is not tailored to the specific stakeholder or deliverable context — the analyst still manually rewrites the framing for each audience."
level_2_label: Practitioner
level_2_descriptor: "Uses AI to synthesize what is known about a specific stakeholder's role, decision-making needs, and recent concerns — then adjusts the structure, emphasis, and level of detail of the deliverable accordingly. For example, uses Copilot to reframe a sector analysis differently for a risk-focused underwriter audience versus a growth-focused BD leader audience."
level_3_label: Proficient
level_3_descriptor: "Anticipates stakeholder objections, knowledge gaps, and preferred evidence types before delivering a briefing. Uses AI to surface previous analytical outputs or meeting notes relevant to the stakeholder's current priorities, and builds deliverables that address those needs pre-emptively. Adapts the AI briefing based on the forum (committee vs. one-to-one vs. written memo)."
level_4_label: Champion
level_4_descriptor: "Develops AI-assisted audience-profiling templates for repeated internal stakeholder types (UW committee, RM pipeline review, executive strategy session). Coaches peers on how to research an audience before a briefing and how to use Copilot to rapidly tailor analytical outputs. Acts as a model for audience-aware, stakeholder-centric analytical communication."

### Domain: data_decision

domain_id: data_decision
title: Data-Driven Decision Making
description: "Using AI to surface patterns in portfolio and financial data, identify anomalies in performance metrics, and support the interpretation of quantitative findings before they become internal recommendations. Combines AI-assisted analysis with cross-verification against source data — so that insights are both efficiently generated and reliably grounded. Applies to portfolio reviews, variance analysis, sector trend synthesis, and scenario modelling."
level_0_label: Unaware
level_0_descriptor: "Does not use AI for data analysis or portfolio decisions. Relies exclusively on manual Excel calculations, static reports, and personal intuition when interpreting financial or portfolio data."
level_1_label: Explorer
level_1_descriptor: "Uses AI to summarise sector reports or market news. Does not connect AI outputs to specific portfolio decisions or analytical conclusions — treats AI-generated summaries as informational rather than analytical inputs."
level_2_label: Practitioner
level_2_descriptor: "Uses AI to analyse portfolio performance data, flag anomalies or outliers, and draft initial variance interpretations. Validates AI-generated conclusions against source spreadsheets and known business context before including them in deliverables. Distinguishes between AI-detected patterns and AI-inferred explanations — verifying explanations independently."
level_3_label: Proficient
level_3_descriptor: "Designs AI queries to surface patterns across multiple data dimensions (sector, time period, exposure type, performance metric). Uses AI to stress-test preliminary interpretations ('Is this decline likely seasonal or structural?') before presenting to stakeholders. Builds multi-step analytical workflows where AI assists at each stage — extraction, pattern detection, narrative drafting — with human validation at each transition."
level_4_label: Champion
level_4_descriptor: "Develops team-level AI-assisted analytical workflows for recurring deliverables (quarterly portfolio reviews, annual sector assessments). Identifies data signals and AI query patterns that consistently surface useful insights. Shares prompt templates and verification protocols with peers — raising the team's overall analytical output quality and consistency."

### Domain: augmented_comm

domain_id: augmented_comm
title: Augmented Communication
description: "Choosing the right M365 Copilot surface for each step of the analyst's research-to-delivery workflow — using Copilot in Excel for data interpretation, Word for structuring draft briefings, Teams Recap for cross-functional meeting follow-up, and Outlook for stakeholder communications. Building multi-step workflows where output from one tool feeds the next, moving from raw data inputs to polished internal deliverables without manual re-entry."
level_0_label: Unaware
level_0_descriptor: "Has not used Copilot features in M365 tools for analytical or communication tasks. Manually copies content between apps (Teams meeting notes to Word, Excel data to email) and is unaware of which tools have AI capabilities."
level_1_label: Explorer
level_1_descriptor: "Has tried one or two Copilot features (e.g., drafting an email with Outlook Copilot or summarizing a document in Word). Does not connect tools into multi-step analytical workflows — still manually transfers data and summaries between applications."
level_2_label: Practitioner
level_2_descriptor: "Uses at least two M365 Copilot surfaces regularly for analytical work (e.g., Word for structuring a sector brief, Excel for summarizing model outputs). Connects outputs from one tool into the next step without manual re-entry — for example, using a Teams meeting recap as context when drafting a follow-up briefing in Word."
level_3_label: Proficient
level_3_descriptor: "Designs multi-step communication workflows across 3+ Copilot surfaces. Chooses the right entry point based on input type and output goal (data-in → Excel Copilot; meeting recap-in → Teams then Word; deliverable-out → Outlook). Recovers gracefully when one step produces poor output — adjusts the prompt before moving to the next tool rather than abandoning the workflow."
level_4_label: Champion
level_4_descriptor: "Documents and shares analytical communication workflows with the team (e.g., 'how to go from portfolio data to briefing deck to stakeholder email using Copilot'). Identifies new Copilot surfaces or features applicable to analyst work. Trains peers on multi-step patterns and helps eliminate unnecessary manual steps across the team."

---

## SECTION C — Course Specs

### Course 1 — Protect the Data: Safe AI Usage for Analysts

course_id: an_c1_responsible_ai
role_id: an
primary_domain: responsible_ai
sequence_order: 1
title: "Protect the Data: Safe AI Usage for Analysts"
tagline: "Leverage AI without compromise — guard confidential data and comply with EDC's policies."
description: "Working with data comes with great responsibility. This course empowers analysts to use Copilot effectively while strictly adhering to EDC's data security and privacy rules. You will learn the SAFE Abstraction Method for GenAI: a four-step approach to ensure you never expose Non-Public EDC Information when using AI. In a simulated Know-Your-Customer (KYC) onboarding scenario, you'll practice identifying sensitive content (personal identifiers, financial details, internal rankings) and transforming or removing it before prompting Copilot. You'll also learn how to interpret EDC's Responsible AI policy in day-to-day analyst work — so you can confidently use AI for data validation, document review, and research without risking compliance violations."
real_use_case: "KYC / CIM Validation Agent"

### Course 2 — Summarize and Succeed: Board-Ready Briefs

course_id: an_c2_strategic_prompting
role_id: an
primary_domain: strategic_prompting
sequence_order: 2
title: "Summarize and Succeed: Board-Ready Briefs"
tagline: "Turn dense reports into clear board-level summaries using structured prompts."
description: "Analysts frequently condense large volumes of information — lengthy performance reports, research findings, sector data — into concise briefs for senior management and committees. This course teaches the CRAF framework (Context, Role, Action, Format) applied to real analyst scenarios such as creating an executive summary of a complex quarterly report. You'll practice prompting with precision: specifying the audience, the key focus areas, and the exact format needed so Copilot's output is usable directly in your deliverables. Mastering this skill saves editing time while ensuring AI output aligns with what your stakeholders need."
real_use_case: "Board Report Summaries"

### Course 3 — Trust but Verify: Validating AI Analyses

course_id: an_c3_critical_eval
role_id: an
primary_domain: critical_eval
sequence_order: 3
title: "Trust but Verify: Validating AI Analyses"
tagline: "Never take AI at face value — learn to fact-check and refine Copilot's outputs."
description: "As an analyst, accuracy is non-negotiable — an AI-generated variance analysis or risk assessment is only useful if it's correct. This course develops your ability to detect and correct errors in Copilot's output before you rely on them. You'll practice the VERIFY Checklist, a systematic approach to reviewing AI outputs: checking figures against source data, questioning assumptions, and fixing logical inconsistencies. Through a realistic Financial Planning & Analysis scenario, you'll sharpen your judgment in evaluating AI suggestions — identifying subtle mistakes in calculations or reasoning and ensuring the final analysis can withstand scrutiny from managers and auditors."
real_use_case: "Financial Variance Analyzer"

### Course 4 — Know Your Audience: AI-Assisted Stakeholder Briefings

course_id: an_c4_relationship_intel
role_id: an
primary_domain: relationship_intel
sequence_order: 4
title: "Know Your Audience: AI-Assisted Stakeholder Briefings"
tagline: "Use AI to research your audience and tailor every deliverable to how they make decisions."
description: "Analysts produce deliverables for multiple internal audiences — risk-focused underwriters, growth-focused business development leaders, and time-pressured executives — yet the same data often needs to be framed differently for each. This course teaches the STAKE framework for audience intelligence: how to use AI to research a stakeholder's role and priorities, adapt the structure and emphasis of your analytical output, and prepare for the questions each audience is likely to ask. Through a realistic scenario where you must brief two different internal committees from the same underlying analysis, you'll practice using Copilot to tailor your deliverable without starting from scratch each time."
real_use_case: "Access to Copilot 365 for Business Development"

### Course 5 — From Data to Insight: AI-Assisted Portfolio Analysis

course_id: an_c5_data_decision
role_id: an
primary_domain: data_decision
sequence_order: 5
title: "From Data to Insight: AI-Assisted Portfolio Analysis"
tagline: "Surface anomalies, validate interpretations, and build AI-assisted analytical workflows for portfolio reviews."
description: "Analysts are expected to detect patterns and draw conclusions from complex financial and portfolio data — but AI can both accelerate and mislead that process. This course teaches the TRACE framework: a structured approach to using AI for data analysis while cross-verifying outputs against source data before conclusions reach internal stakeholders. You'll work through a realistic quarterly portfolio review scenario, using Excel Copilot to surface anomalies, verify AI-generated interpretations against the underlying data, and draft an evidence-based executive summary in Word Copilot — building judgment about when to trust AI analysis and when to investigate further."
real_use_case: "Financial Variance Analyzer; Streamline production of Quarterly analysis and reporting"

### Course 6 — Right Tool, Right Step: M365 Copilot for Analysts

course_id: an_c6_augmented_comm
role_id: an
primary_domain: augmented_comm
sequence_order: 6
title: "Right Tool, Right Step: M365 Copilot for Analysts"
tagline: "Master the Copilot toolkit — Excel, Word, Teams, PowerPoint, Outlook — in sequence."
description: "Why copy-paste data between apps when Copilot can seamlessly assist you within each tool you use? This course teaches analysts to maximize productivity by choosing the right M365 Copilot surface at each step of an analytical workflow — and to chain those surfaces together so output from one tool becomes the input for the next. Through a multi-step scenario building a programme intelligence brief, you'll practice a sequence from Teams meeting recap to Word briefing draft to Outlook stakeholder communication — eliminating manual transfers, reducing re-work, and keeping content within EDC's secure M365 environment."
real_use_case: "Streamline production of Quarterly analysis and reporting"

### Course 7 — Analyst in Action: End-to-End AI Workflow (Capstone)

course_id: an_c7_capstone
role_id: an
primary_domain: strategic_prompting
sequence_order: 7
title: "Analyst in Action: End-to-End AI Workflow (Capstone)"
tagline: "Put it all together — responsible, accurate, audience-aware, data-driven AI assistance from raw data to final communication."
description: "This capstone integrates all six skill domains in a realistic end-to-end workflow. You'll step into the shoes of an EDC analyst preparing an annual programme review for senior leadership. Starting from an Excel portfolio dataset, a Teams meeting transcript, and an internal strategy memo, you'll use AI at each stage: surfacing portfolio insights (Data-Driven Decision Making), verifying AI outputs before they enter the narrative (Critical Evaluation), tailoring the briefing for two different internal audiences (Relationship Intelligence), structuring the brief using CRAF (Strategic Prompting), maintaining data safety throughout (Responsible AI), and chaining Copilot tools across Excel to Word to Outlook (Augmented Communication). By completing this course, you demonstrate the ability to orchestrate AI across a complex, multi-step analytical workflow — just as you would on the job."
real_use_case: "Streamline production of Quarterly analysis and reporting; Financial Variance Analyzer; KYC / CIM Validation Agent"

---

## SECTION D — Scenario Seeds

### Course 1 Scenario

scenario_text: "You are an Information Analyst in the Company Information Management team. A new corporate client, KYC Onboarding Review, has been assigned to you for intake. You have several documents from the file: a certificate of incorporation in French, a corporate ownership chart, and a third-party credit bureau extract. Your task is to use Copilot to speed up verification and data entry. Before you start, you review EDC's Responsible AI policy."
task_1_text: "Write a Copilot prompt to summarize the French incorporation document for this client's file while following EDC's data safety rules. Provide necessary context for translation and summary, but do not include any Non-Public Information such as full names of individuals, registration numbers, or financial details in your prompt."
task_2_text: "Copilot's summary comes back, but it included a personal phone number and home address of a director from the certificate text. This information is confidential. Edit or re-prompt to produce a version that omits or anonymizes personal identifiers — refer to 'the company's director' without naming them and exclude exact contact details."
task_3_text: "You now need to summarize the credit bureau extract, which contains the client's credit score and loan history — both Non-Public. In one sentence, explain how you would apply the SAFE Abstraction Method before using Copilot on this document, so that the prompt contains no restricted data."
task_4_text: "Your team asks for a one-sentence data safety tip about handling confidential numerical data (like credit scores or loan balances) when using Copilot. Write the tip, explaining specifically whether analysts should share exact figures, ranges, or descriptive labels — and why."
coach_system_prompt: "You are an AI skills coach for EDC analysts focused on data safety. The learner is working through a customer onboarding scenario using Copilot on a file that contains Non-Public client data. Guide them to ensure no confidential data is shared in prompts or outputs. For task 1, ask what elements in the document could be considered sensitive. For task 2, if they accept the AI's output without editing, ask how they might remove or mask the personal data before it leaves their hands. For tasks 3 and 4, prompt them to articulate EDC's policy in their own words — the public vs. non-public test and strategies like using ranges or generic labels. Do not reveal policy text directly. Always remind them that protecting client and EDC data is the priority, not prompting speed."

### Course 2 Scenario

scenario_text: "It is Monday morning and the team has produced a 28-page performance report for the Meridian Infrastructure Briefing programme. On Wednesday you need to present a one-page summary to EDC's Executive Committee. The report covers three operational workstreams, budget performance, risk flags, and a set of strategic recommendations. You want to use Copilot to draft the summary more quickly."
task_1_text: "Write an initial CRAF-formatted prompt to summarize the Meridian Infrastructure Briefing Q3 Performance Report for an executive-level audience. Include context about the report (what it covers, who the audience is), specify the AI's role, state the action clearly, and request the output format you need."
task_2_text: "Copilot's first draft is a generic summary that missed several critical issues flagged in the report — specifically a budget shortfall in Workstream 2 and a delayed risk remediation. Revise your prompt to emphasize that the summary must highlight issues and their potential impacts, not only positive outcomes."
task_3_text: "The revised summary is detailed but too long for a one-page brief. Refine the Format instruction in your prompt to produce a more concise output — for example, by specifying a bullet-point structure or a strict word limit focusing on the top three to five points."
task_4_text: "The summary still contains technical acronyms and granular budget line items that may confuse the Executive Committee. Add a constraint to your prompt to ensure the final output is written in plain language and omits low-level operational detail that executives do not need."
coach_system_prompt: "You are an AI skills coach for EDC analysts learning to craft effective prompts for executive-level briefs. In this scenario the learner is using Copilot to summarize a complex internal programme report. Guide through the CRAF framework with questions and hints — do not write the prompt for them. If the prompt is missing context (report name, audience, key themes), ask what context would help Copilot focus. If the output is too generic or too detailed, ask which CRAF element is weakest. If sensitive operational data appears in the prompt (budget figures, risk ratings, internal programme codes), flag it. Encourage iteration step by step."

### Course 3 Scenario

scenario_text: "You are in the Enterprise Analytics and Forecasting team and have used Copilot in Excel to generate a variance analysis of the Aurora Initiative Variance Analysis programme's Q3 budget versus actuals. Copilot produced a narrative explaining the differences, including several statistics and reasons for variances. Before you send this to the Finance Director, you need to verify its accuracy."
task_1_text: "Before using the AI-generated variance explanation, identify at least one figure or claim in the draft that you should verify — for example, a percentage or dollar amount change that seems unexpectedly large or is attributed to a cause you do not recognize from the source data."
task_2_text: "Verify that figure using the source data: cross-check it against the actual numbers in the Aurora Initiative financial spreadsheet. Once you find the correct value, update the AI's statement with the accurate number if it was wrong, or mark it as confirmed if it was right."
task_3_text: "The Copilot narrative attributed a cost increase to 'rising travel expenses,' but your detailed data shows travel costs actually went down. Write a follow-up prompt to correct this reasoning — for example, by directing Copilot to cite only factors supported by the data, or by manually adjusting the explanation yourself and explaining why."
task_4_text: "Reflecting on this process, list two specific checks from the VERIFY Checklist that you applied (or should have applied) to ensure the final variance analysis is accurate and trustworthy. Name the check and explain briefly what you did — or what you should have done — at that step."
coach_system_prompt: "You are an AI skills coach for EDC analysts practicing how to verify AI outputs. The learner has an AI-generated budget variance analysis for the Aurora Initiative and needs to vet it before it goes to the Finance Director. Guide them by asking questions that prompt verification steps. For task 1, ask what specific figure stands out as needing confirmation. For task 2, ensure they describe how they would confirm or correct it (checking the financial spreadsheet, CRM records, or source calculations). For task 3, prompt them to address the unsupported claim — either by re-prompting with a constraint or using their own judgment to fix it. Throughout, remind them to use concrete data and to ask whether each part of the AI's output can be backed by evidence. Do not let them accept the AI's reasoning without question."

### Course 4 Scenario

scenario_text: "You have just completed a sector exposure analysis for the Clean Energy portfolio. This week you must present the same underlying analysis back-to-back to two different internal audiences: the Underwriting Committee (risk-focused, concerned with concentration risk and default scenarios) and the BD Leadership team (growth-focused, interested in sector opportunities and competitive positioning). You have your analysis saved in Word and must produce two tailored briefing packs — ideally without starting from scratch for each."
task_1_text: "Use Copilot to research what the Underwriting Committee cares about most in a sector exposure briefing. Write the Copilot research prompt you would use to surface the top three to four decision-making priorities or questions this audience typically brings to a risk committee — drawing on the role's known mandate and the Clean Energy context."
task_2_text: "Using what you learned about the UW Committee's priorities, rewrite the executive summary from your existing sector analysis using the STAKE framework — Surface their priority question, Tailor the framing (risk emphasis), Anchor the data to their known concerns, Keep out detail they do not need, Enable their next decision. The output should read like it was written for a risk committee, not a general audience."
task_3_text: "Now use Copilot to identify what the BD Leadership team would prioritize when reviewing the same Clean Energy data. Write a brief CRAF prompt that asks Copilot to reframe the sector analysis highlights for a growth-focused audience — specifying the audience shift and which data points to lead with."
task_4_text: "You have 25 minutes before the BD Leadership meeting. Using the UW version of the executive summary as a base, write a single Copilot prompt that converts it into the BD version — specifying the audience pivot, the change in emphasis, and the format expected for a leadership meeting intro slide."
coach_system_prompt: "You are an AI skills coach for EDC analysts practicing audience-aware stakeholder briefing with AI. The learner is preparing two versions of the same sector analysis for two very different internal audiences. Guide them through the STAKE framework without giving answers directly. For task 1, ask what they already know about how UW committees evaluate risk — and whether Copilot can help fill in what they do not know. For task 2, check that the output is genuinely re-framed for risk concerns, not just the same text lightly edited. For task 3, push them to specify the BD audience's decision context in the prompt, not just say 'for BD.' For task 4, ensure they identify what must change structurally (lead data, framing, format) and do not just soften the tone. Flag if any confidential credit data or client-specific risk ratings appear in the prompt."

### Course 5 Scenario

scenario_text: "You are on the Portfolio Analytics team reviewing Cascade Portfolio Q3 Analytics performance data. Excel Copilot has flagged a 32% decline in Sector D exposure across the portfolio — the largest quarterly shift in two years. Before this finding enters the management report, you need to determine whether this decline represents a real credit concern or is an artifact of early repayments by clients in that sector."
task_1_text: "Write an Excel Copilot prompt to analyze the Sector D data in detail and surface the top five accounts driving the portfolio decline. Specify what you define as the unit of analysis (exposure amount, number of facilities, or both) so the AI produces a focused ranked output rather than a generic summary."
task_2_text: "Copilot's output suggests the decline is due to 'reduced client risk appetite in the sector.' You suspect it is actually driven by early repayments, not new risk signals. Write a follow-up Excel Copilot prompt to isolate accounts with early repayment activity in Q3 and compare their share of the overall exposure decline."
task_3_text: "You have confirmed it is primarily early repayments — not a deterioration in credit quality. Now write a Word Copilot prompt to draft an executive summary paragraph that accurately characterizes this finding. The prompt must specify that the explanation should reflect the early repayment data you verified, not the AI's initial interpretation of 'reduced risk appetite.'"
task_4_text: "While reviewing the Word draft, you notice it includes a specific client's name and their exact repayment figure — both Non-Public. Apply the SAFE Abstraction Method: describe the two changes you would make to the paragraph before it is shared with the management committee."
coach_system_prompt: "You are an AI skills coach for EDC analysts working on AI-assisted portfolio analysis. The learner is investigating an unusual data pattern using Excel Copilot and then documenting the finding in Word. Apply the TRACE framework: guide them to Target the right question, find the Root cause, check for Anomaly artifacts, Cross-verify against source data, and draw Evidence-based conclusions. For task 1, ask what level of detail the prompt needs to distinguish between different drivers of exposure decline. For task 2, push them to frame the follow-up as a hypothesis test ('are early repayments the driver?'), not just a new data request. For task 3, check that the Word Copilot prompt explicitly anchors the explanation in the verified data — not the AI's earlier interpretation. For task 4, ensure they identify both the client name and the specific figure as Non-Public and apply abstraction, not just deletion."

### Course 6 Scenario

scenario_text: "You are a Senior Analyst supporting the Enterprise Intelligence Program. The programme lead held a strategy update meeting this morning, and you have the Teams transcript. You also have an Excel dashboard of the programme's current KPIs and a draft strategic memo in Word. By end of day you need to produce a polished one-page programme brief for the programme sponsor, distribute it to the steering committee via email, and log the key decisions from the meeting in the shared SharePoint folder."
task_1_text: "Start with Teams Copilot. Write a prompt to generate a structured meeting recap from the strategy update transcript — capturing decisions made, action items assigned, and any open risks flagged. Specify the output format you need so the recap can be used directly as an input in the next step."
task_2_text: "Move to Word Copilot. Using the Teams recap as context plus the key KPIs from the Excel dashboard, write a CRAF prompt to draft the one-page programme brief for the programme sponsor. Specify which Copilot surface you are working in and what the brief must include: a status summary, key decisions from today, KPI highlights, and next steps."
task_3_text: "Open Copilot in Outlook. Write a prompt to draft the distribution email to the steering committee attaching the programme brief. The email should reference the meeting decisions briefly, give the committee a clear ask (review and confirm no objections before Thursday), and maintain a professional tone appropriate for a senior audience."
task_4_text: "Reflect on the full workflow you just completed. Identify one step where using the wrong Copilot surface would have made the task harder or produced worse output — and explain in one sentence why that tool mismatch would have been a problem."
coach_system_prompt: "You are an AI skills coach for EDC analysts practicing multi-tool Copilot workflows. The learner is using Teams, Word, and Outlook Copilot in sequence to go from a meeting transcript to a finished programme brief and stakeholder email. Apply the Copilot Surface Selector mindset: guide them to match each task to the tool best suited for it. For task 1, check that the Teams recap prompt is specific enough to yield structured output (decisions, actions, risks) rather than a freeform summary. For task 2, ensure the Word prompt explicitly references the Teams output and Excel data as inputs — the learner should not re-summarize them manually. For task 3, make sure the email prompt specifies the ask and the audience tone, not just 'write an email about this.' For task 4, prompt them to think about what happens if they try to do data analysis in Word, or meeting notes in Outlook — ask what is lost. Flag if any sensitive programme financials or personnel details appear in the prompts."

### Course 7 Scenario

scenario_text: "You are the lead analyst on the Horizon Program Annual Review — a high-stakes deliverable for the programme's senior sponsor and two board subcommittees. You have four inputs: an Excel file of programme performance metrics, a Teams transcript from last week's cross-functional review meeting, a draft strategic memo marked Internal Use Only, and a previous year's annual report for comparison. The sponsor has asked for a polished annual review briefing by Friday that addresses both a risk-focused subcommittee and an investment-focused subcommittee."
task_1_text: "Use Excel Copilot to surface the top three performance highlights and two areas of concern from the programme metrics file. Write the prompt you would use — specifying the analytical frame (annual performance review), the output structure (highlights vs. concerns), and the level of detail appropriate for executive consumption. This tests your data_decision skills: targeting the right analytical question for the right audience."
task_2_text: "One of Copilot's flagged 'areas of concern' is a metric decline you suspect is a data anomaly — not a real programme risk. Use Teams Copilot to search the meeting transcript for any discussion of that metric. Write the follow-up prompt you would use in Teams, and describe what you would do if the transcript confirms the decline was already explained (e.g., a timing adjustment). This tests your critical_eval skills: verifying AI-generated insights before they enter the briefing."
task_3_text: "You are now building the briefing for the risk-focused subcommittee. Using the STAKE framework and Copilot in Word, write a prompt that produces the executive summary section of the annual review — framed for a risk-focused reader, drawing on the verified performance data and the meeting recap. Specify the audience and the framing explicitly. This tests your relationship_intel and strategic_prompting skills: audience-aware prompt construction."
task_4_text: "While editing the Word draft, you notice two problems: (a) the draft references a specific programme partner's financial exposure figure taken from the Internal Use Only memo — a Non-Public data point that must not appear in the stakeholder-facing version; and (b) the draft's second section still uses the risk-committee framing for the investment subcommittee. Describe the two specific corrections you would make and the Copilot tool or manual step you would use for each. This tests your responsible_ai and augmented_comm skills: data safety at handoff points in a multi-tool workflow."
coach_system_prompt: "You are an AI skills coach for EDC analysts completing the AI Hero Academy capstone. The learner is preparing a high-stakes annual programme review using all six AI skill domains. Do not give answers — guide through questions at each stage. For task 1, ask whether the prompt specifies what counts as a highlight versus a concern for this audience. For task 2, push the learner to articulate what they would do if the transcript does or does not confirm the anomaly — the verification step must be explicit. For task 3, check that the prompt names the specific audience and their primary lens (risk mitigation), not just 'executive summary.' For task 4, ensure the learner identifies both the data safety violation (Non-Public financial figure) and the audience mismatch (wrong framing for the investment subcommittee) as distinct problems requiring distinct fixes. Flag immediately if any real partner names, financial figures, or internal memo content appears verbatim in a prompt."

---

## SECTION E — Reading Concepts

### Course 1 Reading

framework_name: "The SAFE Abstraction Method"
concept_text: "Before using Copilot with any real data, EDC analysts must stay SAFE — a four-step method to ensure sensitive information is protected while still getting useful AI assistance. S — Scrutinize the data: Identify any Non-Public Information in what you are about to share. This includes client confidential details (financials, ownership records, personal data) and internal EDC information not meant for public disclosure (strategic plans, unpublished results, risk ratings, draft reports). Ask yourself: is this information available in the public domain? If the answer is no or uncertain, treat it as sensitive. A — Abstract or Anonymize: Once you spot sensitive elements, either remove them from your prompt or replace them with generic descriptors. Instead of feeding Copilot 'the client's CEO, Jane Smith, at XYZ Corp with a loan of $4.2M,' say 'the company's CEO at a mid-sized manufacturing client with a moderate loan balance.' This shields actual identities and exact figures. F — Filter outputs: After Copilot generates a response, review it for accidentally revealed confidential information. If the AI's output includes a specific name, account number, or any private detail that came from your source material, edit it out before sharing. E — Ensure compliance: Remember EDC's Responsible AI policy and data classification rules. Use only EDC-approved tools (M365 Copilot is within our tenant). Never paste data into unapproved external AI apps. When in doubt about a piece of information, consult your manager or simply do not include it in your prompt."
good_example: "An Information Analyst needs to use Copilot to identify key risks in a client's ownership structure. The file contains the client's registration number, director names, and an internal credit risk flag — all Non-Public. The analyst describes the client as 'a mid-sized private company in the manufacturing sector, incorporated in Ontario, with a three-tier ownership structure including a foreign holding entity' and asks Copilot to identify the typical compliance risks associated with this structure. No names, numbers, or ratings are in the prompt. The output is analytically useful and contains no confidential data. Why it works: the analyst preserved enough structural context to get a meaningful risk analysis while removing all identifiers."
anti_pattern: "An analyst wants to translate a client's financial statement from French to English quickly, so they paste the entire PDF into a free online AI translation tool. The financial statement contains the client's revenue, net income, loan covenants, and director signatures — all Non-Public EDC Information. Why it fails: the document has been shared with an unapproved external system with no control over where the data is stored or who can access it. This violates EDC's Responsible AI policy and exposes the firm to legal, regulatory, and reputational risk. The correct approach is to use M365 Copilot within the EDC tenant, and even then, to abstract or summarize sensitive financial details rather than pasting the raw document."
takeaway: "Always think twice before sharing information with an AI. If the data is not public, do not paste it — but that does not mean you cannot use AI. It means you apply SAFE abstraction: describe the data in general terms, use ranges instead of exact figures, and refer to entities by role rather than name. This keeps you compliant while still getting the analytical help you need."

### Course 2 Reading

framework_name: "CRAF Framework (Context, Role, Action, Format)"
concept_text: "Great AI outputs start with great inputs. The CRAF Framework helps analysts remember the four key elements of a well-structured Copilot prompt. C — Context: Provide background details. What are you analyzing or summarizing? For whom? For example, 'Q3 performance report for the Meridian Infrastructure Briefing programme, to be presented to the Executive Committee.' Without context, Copilot may produce generic results that miss the point entirely. R — Role: Tell Copilot what perspective to take. Should it behave like a senior financial analyst? A risk advisor? A communications specialist? Specifying a role calibrates the tone, depth, and terminology. 'Act as a senior analyst at a government-backed export credit agency' will produce more appropriate output than leaving this blank. A — Action: Be explicit about what you need. Do you want a summary, a list of key risks, a comparison, a narrative paragraph? 'Draft a one-page executive summary of the report, highlighting any performance issues and strategic recommendations' is a usable action instruction. 'Help me with this report' is not. F — Format: State how the output should look. Bullet points, table, paragraph, word limit, section headings, numbered list — be specific. 'Format the output as five bullet points under Key Highlights and Key Risks, each under 30 words' tells Copilot exactly what you need and makes the output presentation-ready. When all four CRAF elements are present, the AI knows who it is writing as, what it is writing about, what it needs to produce, and how to present it."
good_example: "Prompt: Context: EDC Q3 performance report for the Meridian Infrastructure Briefing programme — a 28-page internal report covering three operational workstreams, budget performance, and strategic recommendations. Role: You are a senior analyst at EDC preparing a brief for the Executive Committee. Action: Summarize the key performance findings, highlight any issues or risks that need executive attention, and list the top three recommendations. Format: Bullet points only, maximum five bullets per section, grouped under Performance Highlights and Issues Requiring Attention. Why it works: the prompt gives Copilot a clear picture of the document, the audience, the specific deliverable, and the exact structure required. The output will be directly usable with minimal editing."
anti_pattern: "Prompt: Summarize this report for me. Why it fails: there is no context about which report or what to focus on, no role to calibrate the tone, no specific deliverable, and no format guidance. Copilot might produce a verbose five-paragraph essay when you needed a five-bullet executive summary. The analyst spends more time editing than the AI saved — and the output may still miss the key issues that matter to the Executive Committee."
takeaway: "A prompt is only as useful as the context you put in it. Specificity across all four CRAF elements — who the AI is writing as, what it is working with, what it must produce, and how to structure it — is what separates output you can use from output you have to rewrite."

### Course 3 Reading

framework_name: "VERIFY Checklist"
concept_text: "Even the best AI can get things wrong. As an analyst, you must verify every important detail before it reaches a stakeholder. The VERIFY Checklist is a systematic review habit to build into every AI-assisted workflow. V — Verify key figures against source data: Double-check numbers, dates, and totals. If Copilot says expenses grew 12%, confirm that against the actual spreadsheet. E — Ensure reasoning matches evidence: Ask yourself whether the explanations make sense given what you know. If Copilot attributes a variance to a cause you did not see in the data, that is a red flag — investigate before including it. R — Review for hallucinations or extra content: AI sometimes inserts plausible-sounding facts that were not in your source material. Look out for any names, statistics, or claims you do not recognize. If Copilot summarizes a report and mentions a project milestone that was not in the document, it may have fabricated it. I — Identify the original source if possible: If Copilot references something, trace it back to the source document or data. If you cannot find the source, the claim should not be in your deliverable. F — Fix before distributing: Do not pass on errors you have spotted. Correct the figure, remove the unsupported claim, or rewrite the sentence before the output leaves your hands. Y — Yield to human judgment: Ultimately, use your expertise to decide what stays and what goes. An AI-generated analysis is a draft, not a final answer. If a sentence feels wrong, investigate it. It is better to have a shorter, accurate report than a longer one with a confidently wrong statement."
good_example: "You use Excel Copilot to draft a variance analysis for the Aurora Initiative Q3 budget. The AI output claims travel costs surged by 50% — a claim you do not recognize from the data. You check the travel ledger and find travel costs actually fell by 5%. You remove the incorrect sentence, identify the real cause of the variance from the source data, and rewrite the explanation with the correct figure. Why it works: you caught a critical error that would have misled the Finance Director. By verifying against the source and correcting the mistake, the final report remains accurate and defensible."
anti_pattern: "An analyst copies a Copilot-generated risk summary directly into a committee briefing without reading it in full. The summary mentions a client default that never actually happened — Copilot invented it based on a similar pattern in the training data. The committee raises the alert in the meeting and the analyst cannot explain where the information came from. Why it fails: the analyst did not verify the AI's statements against the actual credit file. The error was caught in public, damaging credibility. It would have taken less than two minutes to cross-check the key claims."
takeaway: "Copilot can draft analyses quickly, but it is your responsibility to verify every critical detail. Always cross-check numbers and claims using trusted sources. If something looks surprising or unfamiliar, treat it as a red flag — not a confirmation. Combining AI speed with your verification discipline is what produces output that is both efficient and reliable."

### Course 4 Reading

framework_name: "STAKE Framework (Surface, Tailor, Anchor, Keep out, Enable)"
concept_text: "An analytical output is only as useful as the decision it enables for the person reading it. The STAKE Framework helps analysts use AI to rapidly adapt a deliverable for a specific internal audience — without starting from scratch. S — Surface their priority question: Before you write or brief, identify the one question your audience most needs answered. A UW committee asks: 'What is the risk and how concentrated is it?' A BD leadership team asks: 'Where is the growth opportunity and how do we move on it?' Use Copilot to research audience context if you do not already know. T — Tailor the framing: Reorder and reframe your analysis so the answer to their priority question comes first — not buried in section four. Use Copilot to rewrite your executive summary with the audience's lens as the explicit instruction. A — Anchor the data to their concerns: Lead with the data points that are most relevant to this audience's mandate. A risk committee needs default scenarios and sector concentration; a growth team needs market share and pipeline signals. Copilot can help you identify which data to lead with. K — Keep out what does not serve them: Every audience has content that is noise for their decision. Remove it. A UW committee does not need competitive positioning slides; a BD team does not need concentration ratio calculations. Use Copilot to strip or de-emphasize content that will distract rather than inform. E — Enable their next decision: Close the briefing with a clear, audience-appropriate ask or recommendation — what are you asking them to decide or approve? A risk committee needs a risk mitigation recommendation; a BD team needs a pipeline or resource ask. Copilot can draft this closing section once you specify the decision context."
good_example: "An analyst has completed a Clean Energy sector exposure analysis. For the UW Committee, they use Copilot to rewrite the executive summary with this prompt: 'Reframe this sector summary for an underwriting risk committee. Lead with sector concentration risk and default scenario data. Remove market growth commentary. Close with a portfolio management recommendation.' The resulting brief is two pages instead of eight, leads with concentration ratios and stress test outcomes, and ends with a clear risk management recommendation — exactly what the UW Committee needs. Why it works: the audience's priority question was surfaced and the deliverable was anchored to it, with irrelevant content removed."
anti_pattern: "An analyst sends the same 12-page sector analysis to both the UW Committee and the BD Leadership team, changing only the cover page title. The UW Committee spends the first 20 minutes asking why the brief leads with growth projections. The BD team flags that they do not understand the concentration ratio tables. Why it fails: the same content cannot serve two different decision-making frames. Without audience tailoring, the analyst has made their stakeholders do the interpretive work — and created a less credible impression in both rooms."
takeaway: "The quality of a briefing is not measured by how much analysis it contains — it is measured by whether it enables the right decision for the right audience. The STAKE Framework, applied with Copilot, lets you tailor a deliverable for a specific internal audience quickly and confidently. Research the audience, reframe the lead, anchor the data, remove the noise, and enable the decision."

### Course 5 Reading

framework_name: "TRACE Framework (Target, Root cause, Anomaly check, Cross-verify, Evidence-based conclusions)"
concept_text: "AI can surface patterns in data faster than any manual review — but it can also invent explanations for those patterns that are plausible but wrong. The TRACE Framework gives analysts a structured approach to AI-assisted data analysis that produces reliable insights. T — Target the right question: Before asking AI to analyze data, be precise about what you are trying to find. 'Identify the top five accounts driving the Sector D exposure decline in Q3, ranked by exposure change' is a targetable question. 'Tell me about Sector D' is not. A well-targeted question produces a usable output; a vague one produces a narrative. R — Root cause, not just pattern: When AI surfaces an anomaly, your job is to find the real cause — not accept the AI's interpretation. AI will often propose the most statistically common explanation for a pattern. Your job is to test whether that explanation fits this specific data context. A — Anomaly check: Ask whether the pattern could be an artifact of data quality, timing, or methodology rather than a real business signal. A 32% decline in exposure might be real credit deterioration — or it might be early repayments, a reclassification, or a data export error. Always ask before interpreting. C — Cross-verify: Take the AI's output and check it against at least one independent source: the source spreadsheet, a CRM record, a meeting note, or a prior report. If the numbers match and the explanation holds up, proceed. If they do not, investigate before the output leaves your desk. E — Evidence-based conclusions: Every interpretive claim in your deliverable must be traceable to a data point you have verified. If you cannot point to the evidence, the conclusion does not belong in the report."
good_example: "An analyst uses Excel Copilot to investigate a 32% Sector D exposure decline. The AI suggests 'reduced client risk appetite.' The analyst applies TRACE: they Target the top five accounts driving the decline, conduct a Root cause investigation by filtering for early repayment activity, run an Anomaly check (was this a timing issue — did a large repayment hit on the last day of the quarter?), Cross-verify the early repayment amounts against the CRM, and write an Evidence-based conclusion: 'The Sector D exposure decline is attributable to early principal repayments by three clients, representing 87% of the change. No new credit deterioration indicators were identified.' Why it works: the conclusion is specific, supported, and verifiable — and the AI's generic interpretation was corrected."
anti_pattern: "An analyst asks Excel Copilot 'what are the main risks in the portfolio this quarter?' and receives a narrative that includes several plausible-sounding risk factors. The analyst copies the list into the quarterly management report without checking the underlying data. Two of the five risk factors listed by Copilot were not actually present in the Q3 data — they were extrapolated from Q2 patterns. The management committee flags the inconsistency in the review meeting. Why it fails: the analyst asked a vague question, did not apply TRACE, and did not cross-verify the AI's output against source data before distributing it."
takeaway: "AI is a pattern-detection engine, not an analyst. It can find what is unusual in your data faster than you can — but it cannot tell you whether that pattern is real, relevant, or correctly explained. TRACE gives you a systematic way to use AI's speed while applying your own analytical judgment at every step."

### Course 6 Reading

framework_name: "Copilot Surface Selector"
concept_text: "Microsoft 365 offers Copilot assistance across multiple applications — the key is to use the right tool for the right task and to chain outputs between tools so that each step feeds the next. As an analyst, your workflow moves from data to insights to narrative to communication. The Copilot Surface Selector mindset maps each stage to the optimal tool. Data and calculations: use Excel Copilot. When you have structured data — portfolio metrics, budget actuals, KPI dashboards — ask Excel Copilot to analyze, rank, flag anomalies, or draft a data commentary. It has direct access to your spreadsheet structure and can generate charts and pivot summaries without manual copy-out. Meetings and transcripts: use Teams Copilot. After a cross-functional meeting or programme review, use Teams Copilot's meeting recap to extract key decisions, action items, and open issues. The resulting structured output can then feed directly into a briefing without manual note-taking. Reports and documents: use Word Copilot. When writing a briefing, memo, sector review, or executive summary, Word Copilot works within the document you are building. It can draft sections, restructure arguments, summarize attached files, and incorporate content from other sources you reference. Presentations and visuals: use PowerPoint Copilot. When you need to convert a written analysis into a visual format for a committee or leadership meeting, PowerPoint Copilot can generate slides from a document or a set of bullet points. Stakeholder communications: use Outlook Copilot. For distributing briefings, summarizing email threads, or drafting follow-up communications to programme sponsors or committee members, Outlook Copilot drafts in context — it knows your role, tone preferences, and can reference attached files. Chaining these tools means output from one step becomes input for the next: Teams recap feeds into Word briefing, Word briefing feeds into PowerPoint slides, and PowerPoint summary feeds into Outlook distribution email."
good_example: "After the Enterprise Intelligence Program strategy update meeting, an analyst uses Teams Copilot to extract a structured recap of decisions and actions. They open Word Copilot and prompt it to draft the one-page programme brief using the Teams recap plus the KPI dashboard from Excel as inputs — referencing both files from OneDrive. They use the verified Word brief as the basis for a PowerPoint summary slide, then use Outlook Copilot to draft the distribution email to the steering committee attaching both the brief and the slide. No content was manually re-entered at any step. Why it works: each Copilot was used in the application best suited for the task, inputs flowed forward without copy-paste, and the analyst stayed within EDC's secure M365 environment throughout."
anti_pattern: "An analyst tries to use a single Copilot Chat session in Teams to do everything — pasting in spreadsheet data, meeting notes, and a document summary, then asking it to 'write my programme brief and a distribution email.' The output is disorganized, loses the structure of the Excel data, and contains formatting that does not match either Word or Outlook conventions. The analyst spends an hour reformatting. Why it fails: Teams Chat Copilot is not optimized for document authoring or email drafting. Using the wrong surface means the AI lacks the native context of the application — the spreadsheet structure, the document formatting, the email thread — and produces lower-quality output."
takeaway: "Think of Copilot as a set of specialized assistants, each built into the application where they work best. Match the task to the tool, then chain the tools so output from one step becomes input for the next. This is what eliminates manual re-entry, preserves context, and keeps your workflow inside EDC's secure environment."

### Course 7 Reading

framework_name: "End-to-End AI Workflow"
concept_text: "For complex, multi-audience analytical deliverables, you can amplify your productivity by weaving all six AI skills together into an end-to-end workflow. This means planning how you will use Copilot at each stage — from data analysis to narrative to communication — applying the right domain skill at each transition. Plan the stages: break the deliverable into phases (data analysis, insight validation, audience tailoring, drafting, communication) and decide which Copilot surface and which skill domain fits each phase. Starting in the right application with the right audience in mind prevents rework downstream. Responsible AI at every transition: when content moves between tools or from internal analysis to stakeholder-facing output, check for Non-Public data. What is safe to include in an internal Excel analysis may not be safe to include in a board briefing. Apply SAFE abstraction at each handoff. Prompt intentionally at each step: apply CRAF every time you engage a new Copilot surface. When moving from Excel analysis to Word drafting, the context changes — reformulate your prompt for the new surface and the new audience. Do not assume context carries forward. Verify before you proceed: incorporate VERIFY checks after each major AI-driven step, not just at the end. If Excel Copilot surfaces an anomaly, apply TRACE before basing the Word draft on it. Catching an error in Excel takes two minutes; catching it after it has been in a committee briefing takes much longer. Tailor for each audience: when the same deliverable serves multiple internal audiences, apply STAKE to produce audience-specific versions rather than sending a generic document to everyone. The capstone challenge requires you to do this for two subcommittees with different decision-making frames."
good_example: "An analyst preparing the Horizon Program Annual Review uses the following end-to-end workflow: Excel Copilot to surface performance highlights and concerns (data_decision); TRACE to verify a flagged anomaly against the Teams transcript (critical_eval); Word Copilot with a STAKE-informed prompt to draft the risk-subcommittee version of the executive summary (relationship_intel + strategic_prompting); SAFE abstraction to remove a partner financial figure before the document is shared externally (responsible_ai); PowerPoint Copilot to generate the investment-subcommittee slide deck from the verified Word document; Outlook Copilot to draft the sponsor distribution email. Each domain skill was applied at the stage where it was most needed. Why it works: the analyst orchestrated AI as a series of deliberate, verified steps — not a single bulk prompt."
anti_pattern: "An analyst attempts to produce the entire annual review in a single Copilot session: pastes all four inputs into a Teams Chat prompt and asks it to 'write the annual review for both subcommittees.' The output is a single undifferentiated document that does not reflect either subcommittee's priorities, contains a partner financial figure from the Internal Use Only memo, and presents unverified portfolio metrics as confirmed findings. The analyst submits it without review. Why it fails: no SAFE abstraction was applied, no TRACE verification was done, no STAKE tailoring was performed, and the wrong Copilot surface was used for a document authoring task. The efficiency gains from AI were entirely cancelled out by the rework and credibility cost."
takeaway: "An end-to-end AI workflow is not about doing everything faster with one prompt — it is about applying the right skill at the right stage, using the right tool, for the right audience. When you chain responsible data handling, structured prompting, critical verification, audience intelligence, analytical rigor, and the correct M365 surfaces together, you produce analytical deliverables that are both faster and more trustworthy than those produced without AI."

---

## SECTION F — Diagnostic Item Seeds

### Diagnostic: responsible_ai

item_1_type: mcq
question_text: "An analyst is preparing to use Copilot to summarize a client's credit file. The file contains the client's credit score, loan covenants, and director names. What should the analyst do before writing the prompt?"
options: A) Paste the full file into Copilot to get the most complete summary | B) Abstract or remove Non-Public details (credit score, names, covenants) and describe the client in general terms | C) Use an external AI tool for faster processing | D) Ask a colleague to review the Copilot output afterward
correct_option: B
explanation: "EDC's Responsible AI policy requires abstracting Non-Public Information before it enters any AI prompt. Credit scores, loan covenants, and director names are all Non-Public."

item_2_type: prompt_sandbox
scenario_text: "You have a PDF of a corporate client's ownership structure that contains director names, registration numbers, and an internal credit risk flag. You need to use Copilot to identify the typical compliance risks associated with this ownership type."
question_text: "Write the Copilot prompt you would use to get a useful compliance risk analysis without including any Non-Public data in the prompt."
scoring_rubric_criteria:
  - "No director names, registration numbers, or specific credit ratings appear in the prompt": max 1
  - "The prompt describes the ownership structure in general terms (e.g., 'a private company with a multi-tier ownership structure including a foreign holding entity')": max 1
  - "The prompt specifies a clear analytical question (e.g., 'identify typical compliance risks for this ownership type')": max 1
  - "The prompt does not reference any unapproved external AI tools": max 1

item_3_type: micro_task
scenario_text: "A colleague sends you this Copilot prompt they drafted: 'Summarize the risk profile for XYZ Corp: revenue $4.2M, CEO Jane Smith, loan covenant breach flagged in Q2, internal risk rating: High.' They are about to paste it into Copilot Chat."
question_text: "Identify the two specific data elements in this prompt that violate EDC's Responsible AI policy and explain in one sentence what the analyst should do instead."
scoring_rubric_criteria:
  - "Correctly identifies CEO name (Jane Smith) as a personally identifiable Non-Public element": max 1
  - "Correctly identifies specific financial figure ($4.2M revenue) or internal risk rating as Non-Public": max 1
  - "Proposes a concrete fix: replace with generic descriptors (e.g., 'a mid-sized client with a high risk rating') rather than deleting the analysis entirely": max 1
  - "Explains the policy rationale: Non-Public data must not enter AI prompts unabstracted": max 1

---

### Diagnostic: strategic_prompting

item_1_type: mcq
question_text: "An analyst writes this Copilot prompt: 'Summarize the Q3 report.' The output is a generic five-paragraph essay that misses the key budget issues. Which CRAF element is most likely the cause?"
options: A) The Role instruction is missing | B) The Context (what the report covers and who the audience is) is missing | C) The Action word 'summarize' is too vague | D) A Format constraint was not provided
correct_option: B
explanation: "Without context — what the report covers, who needs the summary, and what matters most — Copilot cannot focus its output. Context is the most impactful missing element here."

item_2_type: prompt_sandbox
scenario_text: "You need to summarize a 30-page programme performance report for the Executive Committee. The report covers three operational workstreams, budget performance, and strategic recommendations. The summary must be one page maximum."
question_text: "Write a CRAF-formatted prompt to produce this executive summary. Include all four elements: Context, Role, Action, and Format."
scoring_rubric_criteria:
  - "Context specifies the report content (workstreams, budget, recommendations) and the audience (Executive Committee)": max 1
  - "Role positions the AI as a senior analyst or equivalent, calibrating tone": max 1
  - "Action specifies a concrete deliverable (executive summary) and names key areas to highlight (e.g., issues, recommendations)": max 1
  - "Format specifies output structure (e.g., bullet points, word/section count, headers)": max 1

item_3_type: micro_task
scenario_text: "A colleague used this prompt: 'Write a one-page summary of the attached document for a risk meeting.' The output ignored three critical risk flags that were in the document."
question_text: "Identify which CRAF element(s) are weak or missing, and rewrite only the Action and Format components of the prompt to fix the problem."
scoring_rubric_criteria:
  - "Correctly identifies that Context (what the document is, which risks matter) or Action specificity is insufficient": max 1
  - "Revised Action explicitly directs Copilot to highlight critical risk flags and their potential impacts": max 1
  - "Revised Format specifies structure that surfaces issues (e.g., a 'Key Risks' section with a set number of bullets)": max 1
  - "The revised prompt components are role-appropriate and would produce a materially better output": max 1

---

### Diagnostic: critical_eval

item_1_type: mcq
question_text: "An analyst uses Copilot to generate a variance analysis narrative. Before sending it to the Finance Director, which action best demonstrates the VERIFY discipline?"
options: A) Re-run the Copilot prompt three times to confirm consistent output | B) Cross-check each key figure and cause-and-effect claim against the source spreadsheet | C) Ask a colleague to read the narrative for grammar and clarity | D) Shorten the narrative to reduce the number of claims that need checking
correct_option: B
explanation: "The VERIFY Checklist requires tracing key figures and reasoning back to the source data — not just re-prompting or peer editing."

item_2_type: prompt_sandbox
scenario_text: "Copilot has generated this budget variance sentence: 'Travel expenses increased 22% quarter-over-quarter, driven by expanded site visit activity in the Western region.' You open the travel ledger and find that travel costs fell by 3% and there were no Western region site visits recorded in Q3."
question_text: "Write the follow-up Copilot prompt you would use to correct this sentence, and explain in one sentence why you cannot simply accept the original."
scoring_rubric_criteria:
  - "The follow-up prompt explicitly anchors the correction to the verified source data (e.g., 'the travel ledger shows a 3% decrease')": max 1
  - "The prompt directs Copilot to remove the unsupported causal explanation ('Western region site visits')": max 1
  - "The explanation correctly identifies hallucination or unsupported inference as the problem": max 1
  - "The revised prompt would produce an accurate, evidence-based sentence": max 1

item_3_type: micro_task
scenario_text: "You receive this AI-generated risk summary: 'The client defaulted on a facility in Q2 of last year. Recovery proceedings are ongoing.' You check the credit file and find no record of any default for this client — the client is current on all obligations."
question_text: "Name the specific VERIFY step that would have caught this error, explain what you would do to correct the output, and describe one change to your workflow to prevent this type of error in the future."
scoring_rubric_criteria:
  - "Correctly names 'Review for hallucinations or extra content' (R in VERIFY) as the applicable step": max 1
  - "Correction action is concrete: remove the default claim and replace with a verified statement about client standing": max 1
  - "Workflow change is specific and preventive (e.g., 'always cross-reference client status in CRM before including any credit history claims')": max 1
  - "Response demonstrates understanding that AI can generate plausible but false credit history": max 1

---

### Diagnostic: relationship_intel

item_1_type: mcq
question_text: "An analyst must present the same sector exposure analysis to both the Underwriting Committee and the BD Leadership team. Using the STAKE framework, what is the FIRST step before writing either version?"
options: A) Draft the executive summary and then adjust the tone for each audience | B) Surface each audience's priority question — what they most need to decide | C) Remove all data that is not relevant to both audiences | D) Ask the programme lead which version to write first
correct_option: B
explanation: "STAKE begins with Surfacing the audience's priority question. Without knowing what each audience needs to decide, tailoring the framing and anchoring the data are guesswork."

item_2_type: prompt_sandbox
scenario_text: "You have completed a Clean Energy sector analysis. You need to prepare the executive summary section for the Underwriting Committee, whose primary concern is concentration risk and default scenarios."
question_text: "Write a Copilot prompt that uses the STAKE framework to produce the executive summary for the Underwriting Committee. Your prompt must name the audience and their decision lens explicitly."
scoring_rubric_criteria:
  - "Prompt names the Underwriting Committee as the specific audience": max 1
  - "Prompt specifies the decision frame (concentration risk, default scenarios) — not just 'risk audience'": max 1
  - "Prompt directs Copilot to lead with the audience's priority data (e.g., sector concentration ratios, stress test outcomes)": max 1
  - "Prompt includes at least one 'Keep out' instruction (e.g., remove market growth projections, remove competitive positioning commentary)": max 1

item_3_type: micro_task
scenario_text: "A colleague sends the same 10-page sector analysis report to both the Risk Committee and the Investment Committee, changing only the cover page. Both committees give critical feedback: the Risk Committee says the brief leads with growth projections they do not need; the Investment Committee cannot understand the concentration ratio tables."
question_text: "Using STAKE, identify two specific changes the analyst should have made for each audience before distributing."
scoring_rubric_criteria:
  - "For the Risk Committee: identifies that growth projections should be removed or moved to an appendix (K in STAKE — Keep out)": max 1
  - "For the Risk Committee: identifies that the brief should lead with concentration risk or default scenario data (T/A in STAKE — Tailor and Anchor)": max 1
  - "For the Investment Committee: identifies that concentration ratio tables should be explained or replaced with simpler data (T in STAKE — Tailor)": max 1
  - "For the Investment Committee: identifies that the brief should lead with opportunity signals or pipeline data relevant to their decision (A in STAKE — Anchor)": max 1

---

### Diagnostic: data_decision

item_1_type: mcq
question_text: "Excel Copilot flags a 28% decline in a portfolio sector's exposure. Before attributing this to credit deterioration in the management report, what is the FIRST step in the TRACE framework?"
options: A) Cross-verify the figure against the prior quarter's report | B) Target a precise question: identify the specific accounts driving the decline | C) Draft the management report paragraph with a caveat about uncertainty | D) Ask the Finance Director whether they noticed the trend
correct_option: B
explanation: "TRACE begins with Targeting the right question — specifically identifying the top accounts driving the change before investigating root cause or cross-verifying."

item_2_type: prompt_sandbox
scenario_text: "You are investigating a 28% decline in Sector D exposure. You suspect the cause may be early repayments rather than new credit deterioration. The data is in an Excel portfolio dashboard."
question_text: "Write the Excel Copilot prompt you would use to test your hypothesis. The prompt must frame this as a hypothesis test, not a general data request."
scoring_rubric_criteria:
  - "Prompt frames a specific hypothesis (e.g., 'determine whether early repayments account for the Sector D exposure decline')": max 1
  - "Prompt specifies the unit of analysis (accounts, facilities, or both) and the metric to isolate (early repayment activity in Q3)": max 1
  - "Prompt requests a ranked or structured output (e.g., top accounts by repayment amount vs. exposure change)": max 1
  - "Prompt does not accept the AI's earlier narrative interpretation as a given — it frames a competing hypothesis to test": max 1

item_3_type: micro_task
scenario_text: "A colleague uses Excel Copilot to analyze portfolio performance. They receive this output: 'The Sector D decline is attributable to reduced client risk appetite and tighter liquidity constraints across the sector.' They copy this sentence directly into the quarterly management report without further investigation."
question_text: "Identify which two TRACE steps the analyst skipped, and explain what specific action each skipped step would have required."
scoring_rubric_criteria:
  - "Correctly identifies Root cause (R) as skipped: the analyst accepted the AI's narrative without identifying the actual driver (e.g., early repayments vs. new credit risk)": max 1
  - "Correctly identifies Cross-verify (C) as skipped: the analyst should have checked the AI's claim against source data (CRM records, repayment schedules, sector news)": max 1
  - "Describes a specific action for Root cause step (e.g., filter for accounts with early repayment flags in Q3)": max 1
  - "Describes a specific action for Cross-verify step (e.g., compare AI's 'tighter liquidity' claim against actual sector credit metrics or news)": max 1

---

### Diagnostic: augmented_comm

item_1_type: mcq
question_text: "An analyst needs to go from a Teams meeting transcript to a finished one-page programme brief to a distribution email in a single afternoon. Using the Copilot Surface Selector, which is the correct tool sequence?"
options: A) Teams Copilot → Word Copilot → Outlook Copilot | B) Outlook Copilot → Word Copilot → Teams Copilot | C) Word Copilot → Teams Copilot → Outlook Copilot | D) A single Teams Chat Copilot session for all three steps
correct_option: A
explanation: "The correct chain matches each tool to the task it does best: Teams extracts meeting decisions, Word drafts the document, Outlook composes the distribution email."

item_2_type: prompt_sandbox
scenario_text: "You have just finished a strategy update meeting. You have the Teams meeting transcript. You need to draft a one-page programme brief in Word for the programme sponsor."
question_text: "Write the Word Copilot prompt you would use to draft the one-page brief. The prompt must reference the Teams meeting recap as an input and specify what the brief must include."
scoring_rubric_criteria:
  - "Prompt identifies Word Copilot as the tool being used (not Teams Chat or Outlook)": max 1
  - "Prompt references the Teams meeting recap as a named input (either as an attached file or described content)": max 1
  - "Prompt specifies the brief's required components (e.g., status summary, key decisions, KPI highlights, next steps)": max 1
  - "Prompt specifies a format constraint (one-page, bullet points, or equivalent)": max 1

item_3_type: micro_task
scenario_text: "A colleague tries to do the following in a single Teams Chat Copilot session: paste in their Excel KPI data, paste their meeting notes, and ask Copilot to 'write my programme brief and a distribution email.' The output is disorganized and the brief loses the Excel table structure."
question_text: "Identify the two specific Copilot Surface Selector principles the analyst violated, and for each violation, name the correct tool and explain why it would produce better output."
scoring_rubric_criteria:
  - "Identifies that data analysis (Excel KPI data) should be handled in Excel Copilot, not Teams Chat — because Excel Copilot has native access to spreadsheet structure": max 1
  - "Identifies that document authoring (programme brief) should be done in Word Copilot — because Word Copilot works within the document formatting context": max 1
  - "Identifies that email drafting should be done in Outlook Copilot — because Outlook Copilot knows email tone, threading, and attachment conventions": max 1
  - "Explains the chaining principle: each tool's output becomes the next tool's input, preserving context and structure without manual re-entry": max 1

---

## SECTION G — Evaluation Item Seeds

### Evaluation: Course 1

item_1_type: mcq
sequence: 1
question_text: "Which of the following correctly applies the SAFE Abstraction Method before using Copilot on a client ownership file containing director names and registration numbers?"
options: A) Paste the file into Copilot and instruct it not to include names in the output | B) Describe the ownership structure in general terms and replace identifiers with role-based labels | C) Use an external translation tool first, then paste into Copilot | D) Ask a colleague to review the Copilot output for any sensitive content
correct_option: B
explanation: "SAFE requires abstracting sensitive identifiers before the prompt is written — not relying on AI to filter them from output after the fact."

item_2_type: mcq
sequence: 2
question_text: "An analyst is about to prompt Copilot with a client's credit bureau extract that includes a credit score and loan history. Which action correctly applies the F step (Filter outputs) of SAFE?"
options: A) Skip the credit score and use only the qualitative narrative sections | B) After receiving the Copilot output, review it and remove any specific figures or client identifiers before sharing | C) Set the Copilot temperature to low to reduce the chance of sensitive content in the output | D) Include the credit score in the prompt but mark it as confidential
correct_option: B
explanation: "Filter outputs means reviewing AI-generated content after the fact and removing any confidential details before the output is shared or used in a deliverable."

item_3_type: mcq
sequence: 3
question_text: "Which of the following is an example of correctly applying the E step (Ensure compliance) in SAFE?"
options: A) Using a public AI chatbot but logging the session for audit purposes | B) Pasting a draft strategy document into Copilot after checking with IT | C) Using only EDC-approved M365 Copilot within the EDC tenant for all AI-assisted work | D) Deleting the AI-generated output immediately after use to prevent unauthorized access
correct_option: C
explanation: "Ensure compliance means using only approved tools within EDC's secure tenant — not ad hoc authorization checks or cleanup after the fact."

item_4_type: performance_task
sequence: 4
question_text: "You have a client file containing a certificate of incorporation (French), a corporate ownership chart, and a third-party credit bureau extract. All three documents contain Non-Public Information. Using the SAFE Abstraction Method, write the Copilot prompt you would use to analyze the compliance risks in this client's ownership structure. Your response must demonstrate all four SAFE steps: what you scrutinize, what you abstract, how you filter, and how you ensure compliance."
scoring_rubric_criteria:
  key1: "S — Scrutinize: response identifies specific Non-Public elements in the documents (director names, registration numbers, credit scores) before writing the prompt"
  key2: "A — Abstract: the prompt uses generic descriptors (e.g., 'a private company incorporated in Quebec with a three-tier ownership structure') rather than identifiers or exact figures"
  key3: "F — Filter: response describes a plan to review Copilot's output and remove any sensitive content that surfaces before the analysis is used"
  key4: "E — Ensure compliance: response references using only M365 Copilot within EDC's tenant and does not reference any external AI tools"

---

### Evaluation: Course 2

item_1_type: mcq
sequence: 1
question_text: "Which CRAF element is most responsible for ensuring Copilot produces an executive-level summary rather than an operational one?"
options: A) Context — specifying the document's contents | B) Role — positioning the AI as a senior analyst writing for an executive audience | C) Action — asking for a summary rather than an analysis | D) Format — specifying bullet points
correct_option: B
explanation: "Role calibrates the perspective, tone, and level of detail. Without a role instruction, Copilot defaults to a generic output that may not match executive expectations."

item_2_type: mcq
sequence: 2
question_text: "An analyst writes: 'Summarize the Q3 programme report, highlighting three risks for the Executive Committee.' Which CRAF element is still missing that would most improve the output?"
options: A) Context — what the report covers and its key themes | B) Role — the AI should be told to behave as an analyst | C) Action — 'summarize' is sufficient for a summary task | D) Format — the analyst should specify bullet points or word count
correct_option: D
explanation: "The prompt has Context (Q3 programme report), Role (implicit), and Action (summarize, highlight risks). Format is the missing element that would define structure and length."

item_3_type: mcq
sequence: 3
question_text: "A prompt produces a 500-word narrative when a 5-bullet executive summary was needed. Which revision most directly fixes this?"
options: A) Add more Context about the document | B) Change the Role instruction to 'expert analyst' | C) Add a Format instruction specifying exactly 5 bullets, maximum 30 words each | D) Change the Action from 'summarize' to 'condense'
correct_option: C
explanation: "The output length and structure problem is a Format issue. Specifying the exact number of bullets and word count per bullet gives Copilot the structural constraints it needs."

item_4_type: performance_task
sequence: 4
question_text: "You have a 28-page internal programme performance report for the Meridian Infrastructure Briefing that covers three operational workstreams, budget performance, and strategic recommendations. You must present a one-page summary to the Executive Committee on Wednesday. Write a complete CRAF-formatted Copilot prompt that would produce this summary. Then explain in one sentence why each of the four CRAF elements you included matters for this specific task."
scoring_rubric_criteria:
  key1: "Context specifies the report (Meridian Infrastructure Briefing, 3 workstreams, budget, recommendations) and the audience (Executive Committee)"
  key2: "Role positions the AI as a senior analyst or EDC programme advisor writing for executive consumption"
  key3: "Action specifies a concrete, complete deliverable (executive summary) and directs Copilot to highlight issues or risks, not just positive outcomes"
  key4: "Format specifies structure and length constraints (e.g., one page, 5 bullets max, grouped under named sections) that make the output presentation-ready"

---

### Evaluation: Course 3

item_1_type: mcq
sequence: 1
question_text: "An analyst receives a Copilot-generated variance analysis that attributes a cost increase to 'expanded procurement activity.' The analyst does not recognize this explanation from the source data. What does the VERIFY Checklist require at this point?"
options: A) Accept the explanation as Copilot likely found patterns not visible in the summary data | B) Re-run the Copilot prompt to see if the explanation changes | C) Trace the claim back to the source data — identify the original evidence or remove the unsupported claim | D) Flag the anomaly in a footnote and include it in the report with a caveat
correct_option: C
explanation: "I (Identify the original source) in VERIFY requires tracing every claim back to a verifiable source. If the source cannot be found, the claim must be removed before the report is distributed."

item_2_type: mcq
sequence: 2
question_text: "Which of the following is an example of correctly applying the Y step (Yield to human judgment) in VERIFY?"
options: A) Approving a Copilot-generated risk summary after running a grammar check | B) Deciding to investigate a Copilot statement that 'feels off' even though the numbers check out | C) Accepting any claim that cites a specific data point, even if the data point seems small | D) Asking Copilot to verify its own output by re-prompting with a confirmation question
correct_option: B
explanation: "Yield to human judgment means applying your own professional knowledge to validate the output — even when numbers appear to check out, an experienced analyst's intuition is itself a verification signal."

item_3_type: mcq
sequence: 3
question_text: "A Copilot-generated report mentions a client default that the analyst cannot find in the credit file. What specific VERIFY failure mode does this represent?"
options: A) Missing Format instruction in the original prompt | B) Hallucination — AI inserted a plausible but invented fact not present in the source material | C) Data quality error — the credit file was not uploaded correctly | D) Prompt injection — the client's document contained adversarial instructions
correct_option: B
explanation: "Hallucination (covered in the R step — Review for hallucinations) is when AI generates plausible-sounding content that was not in the source. The analyst must catch this by cross-referencing against the actual credit file."

item_4_type: performance_task
sequence: 4
question_text: "You used Excel Copilot to generate a variance analysis for the Aurora Initiative Q3 budget. The AI output contains three claims: (1) travel expenses increased 22%, (2) the increase was driven by expanded site visit activity, and (3) total programme cost exceeded budget by $180,000. You open the spreadsheet and find: travel costs fell 3%, there were no site visits in Q3, and total programme cost exceeded budget by $183,500. Apply the VERIFY Checklist to this output: identify which specific steps apply to each claim, describe what correction you would make, and write the follow-up Copilot prompt to produce an accurate version of the travel expense sentence."
scoring_rubric_criteria:
  key1: "V (Verify figures): correctly identifies claim 3 as having a wrong figure ($180K vs $183.5K) and states the correction"
  key2: "E (Ensure reasoning matches evidence): correctly identifies claim 2 as having unsupported causation (no site visits in Q3) and states it must be removed or replaced"
  key3: "R (Review for hallucinations): correctly identifies claims 1 and 2 together as hallucinated — neither the 22% increase nor the site visit explanation appeared in the source data"
  key4: "Follow-up prompt anchors the corrected sentence to verified source data (travel fell 3%) and directs Copilot to remove or replace the causal explanation with evidence-based language"

---

### Evaluation: Course 4

item_1_type: mcq
sequence: 1
question_text: "The STAKE framework begins with Surfacing the audience's priority question. For the BD Leadership team reviewing a Clean Energy sector analysis, which question best represents their priority?"
options: A) What is the probability of default in Sector D under a stress scenario? | B) What growth opportunities exist in the sector and how can EDC move on them? | C) What is the current concentration ratio for Clean Energy in the portfolio? | D) What regulatory constraints affect new facility approvals in this sector?
correct_option: B
explanation: "BD Leadership is growth-focused. Their priority question is about opportunity and action — not risk concentration or regulatory constraints, which are UW Committee concerns."

item_2_type: mcq
sequence: 2
question_text: "In the STAKE framework, which step ensures that content irrelevant to the audience's mandate is removed from the deliverable?"
options: A) Surface — identify the priority question | B) Tailor — reframe the analysis for the audience | C) Keep out — remove content that would distract from their decision | D) Enable — close with an audience-appropriate recommendation
correct_option: C
explanation: "K (Keep out) is the explicit step for removing content that does not serve the specific audience — such as removing competitive positioning slides from a risk committee brief."

item_3_type: mcq
sequence: 3
question_text: "An analyst sends the same 12-page sector analysis to both the Underwriting Committee and the BD Leadership team, changing only the title. Both committees give negative feedback. What is the primary STAKE failure?"
options: A) The analyst did not apply CRAF to the prompt that generated the report | B) The analyst skipped the Tailor and Keep out steps — neither version was adapted to its audience's decision frame | C) The analyst did not verify the data before distributing the report | D) The analyst used the wrong Copilot surface for the document
correct_option: B
explanation: "Sending the same document to two different audiences with different decision frames violates STAKE's Tailor and Keep out steps — the content, framing, and emphasis must differ for each audience."

item_4_type: performance_task
sequence: 4
question_text: "You have completed a Clean Energy sector exposure analysis. This week you must present the findings to two audiences: the Underwriting Committee (risk-focused: concentration risk, default scenarios) and the BD Leadership team (growth-focused: sector opportunities, competitive positioning). Using the STAKE framework, write the Copilot prompt you would use to produce the executive summary for the Underwriting Committee version. Then describe in 2–3 sentences what specific changes you would make to produce the BD Leadership version — without starting from scratch."
scoring_rubric_criteria:
  key1: "UW Committee prompt surfaces their priority question (concentration risk/default scenarios) and explicitly names them as the audience"
  key2: "UW Committee prompt includes a Tailor instruction (lead with risk data, use risk committee framing) and an Anchor instruction (reference concentration ratios or stress test outcomes)"
  key3: "UW Committee prompt includes at least one Keep out instruction (e.g., remove growth projections, remove competitive positioning commentary)"
  key4: "BD Leadership conversion description correctly identifies what must change (lead data: opportunity signals; framing: growth lens; close: pipeline/resource ask) and references using Copilot to make these changes from the UW version as a base"

---

### Evaluation: Course 5

item_1_type: mcq
sequence: 1
question_text: "In the TRACE framework, what distinguishes a 'targeted question' (T) from a vague data request?"
options: A) A targeted question is shorter and easier for Copilot to process | B) A targeted question specifies the unit of analysis, the metric, and the time frame — rather than asking for a general narrative | C) A targeted question uses the word 'analyze' rather than 'describe' | D) A targeted question avoids including any specific data in the prompt
correct_option: B
explanation: "Targeting means specifying exactly what you want to measure (e.g., top 5 accounts by exposure change in Q3) rather than asking for a general summary that will produce an undifferentiated narrative."

item_2_type: mcq
sequence: 2
question_text: "Excel Copilot suggests that the Sector D exposure decline is due to 'reduced client risk appetite.' An analyst applying TRACE correctly responds by:"
options: A) Accepting the explanation and adding a qualifier: 'per AI analysis, reduced risk appetite may be a factor' | B) Re-running the Excel Copilot prompt to see if the explanation changes | C) Forming a competing hypothesis (e.g., early repayments) and writing a follow-up prompt to test it against the data | D) Escalating to the portfolio manager before doing any further analysis
correct_option: C
explanation: "Root cause investigation (R in TRACE) requires testing a specific alternative hypothesis against the data — not accepting the AI's first interpretation or adding caveats to an unverified claim."

item_3_type: mcq
sequence: 3
question_text: "An analyst has confirmed through TRACE that the Sector D decline is due to early repayments. They then draft the management report paragraph in Word. Which action correctly applies the E step (Ensure compliance / Evidence-based conclusions) at this stage?"
options: A) Have a colleague review the paragraph before submitting | B) Include only claims traceable to verified data points — and apply SAFE abstraction before sharing the document | C) Reference the AI's original explanation as an alternative hypothesis in the footnotes | D) Run a final Copilot check to confirm the paragraph reads accurately
correct_option: B
explanation: "Evidence-based conclusions (E in TRACE) means every claim in the report is traceable to verified data. SAFE abstraction applies here because the document is moving toward a stakeholder-facing context."

item_4_type: performance_task
sequence: 4
question_text: "You are analyzing the Cascade Portfolio Q3 Analytics data. Excel Copilot has flagged a 32% decline in Sector D exposure and suggested it is due to 'reduced client risk appetite across the sector.' You suspect it may be early repayments. Apply the full TRACE framework: write the Excel Copilot prompt to test your hypothesis (T and R), describe the Anomaly check you would run (A), identify the Cross-verify step (C), and write the Word Copilot prompt to draft an Evidence-based paragraph for the management report once you have confirmed the cause (E)."
scoring_rubric_criteria:
  key1: "Excel Copilot prompt targets a specific question (top accounts driving the decline) and frames a hypothesis test (are early repayments the driver) — not a general 'analyze Sector D' request"
  key2: "Anomaly check identifies a plausible data artifact (e.g., large repayment hitting on last day of quarter, reclassification, data export error) and describes how to investigate it"
  key3: "Cross-verify step names an independent source to check against (CRM repayment records, client communication history, or prior quarter data) — not just re-prompting Copilot"
  key4: "Word Copilot prompt anchors the paragraph explicitly in the verified early repayment data, directs Copilot to remove the 'reduced risk appetite' explanation, and applies SAFE abstraction (no specific client names or exact repayment figures)"

---

### Evaluation: Course 6

item_1_type: mcq
sequence: 1
question_text: "An analyst needs to convert a Teams meeting transcript into a one-page programme brief for a sponsor and then send a distribution email to the steering committee. In the Copilot Surface Selector, which is the correct tool sequence?"
options: A) Teams Copilot (recap) → Word Copilot (brief) → Outlook Copilot (email) | B) Outlook Copilot (email) → Word Copilot (brief) → Teams Copilot (recap) | C) Word Copilot (brief) → Teams Copilot (recap) → Outlook Copilot (email) | D) A single Copilot Chat session in Teams for all three deliverables
correct_option: A
explanation: "Each tool is matched to its native task: Teams extracts decisions from the transcript, Word drafts the document, Outlook composes the distribution email. Chaining preserves context at each step."

item_2_type: mcq
sequence: 2
question_text: "Why is Teams Chat Copilot a poor choice for drafting a formatted one-page programme brief?"
options: A) Teams Chat Copilot cannot access SharePoint files | B) Teams Chat Copilot is not optimized for document authoring — it lacks the document formatting context that Word Copilot has natively | C) Teams Chat Copilot has a shorter output length limit than Word Copilot | D) Teams Chat Copilot does not support attaching files to outputs
correct_option: B
explanation: "The Copilot Surface Selector principle: each tool has native context for its application. Teams Chat lacks document structure awareness; Word Copilot works within the document and maintains formatting context."

item_3_type: mcq
sequence: 3
question_text: "An analyst finishes drafting the programme brief in Word using Excel and Teams inputs. What should their next Copilot tool be and why?"
options: A) PowerPoint Copilot — to convert the brief into slides for the meeting | B) Outlook Copilot — to draft the distribution email to the steering committee | C) Teams Copilot — to post a summary update in the programme channel | D) Word Copilot — to run a final grammar and clarity check on the brief
correct_option: B
explanation: "Once the document is complete, the next step in the workflow chain is distribution. Outlook Copilot drafts in the email context with awareness of tone, threading, and attachments."

item_4_type: performance_task
sequence: 4
question_text: "You are a Senior Analyst supporting the Enterprise Intelligence Program. This morning's strategy update meeting produced a Teams transcript. You also have an Excel KPI dashboard and a Word draft memo. By end of day you need: a structured meeting recap, a one-page programme brief for the sponsor, and a distribution email to the steering committee. For each of the three deliverables, write: (1) the Copilot surface you would use, (2) the prompt you would write, and (3) one sentence explaining what would go wrong if you used the wrong surface."
scoring_rubric_criteria:
  key1: "Meeting recap: correctly uses Teams Copilot; prompt specifies structured output (decisions, actions, open risks); explains that a different surface would lack access to the meeting transcript natively"
  key2: "Programme brief: correctly uses Word Copilot; prompt references Teams recap and Excel dashboard as named inputs; explains that Teams Chat would lose document formatting context"
  key3: "Distribution email: correctly uses Outlook Copilot; prompt specifies the audience (steering committee), the ask (review and confirm), and the professional tone; explains that Word Copilot would lack email threading and attachment conventions"
  key4: "All three prompts chain correctly: each step's output is referenced as input in the next step (Teams recap feeds Word brief; Word brief feeds Outlook email), with no manual re-entry described"

---

### Evaluation: Course 7

item_1_type: mcq
sequence: 1
question_text: "In the End-to-End AI Workflow for a multi-audience analytical deliverable, when should SAFE abstraction be applied?"
options: A) Only at the final step, before the document is distributed to external stakeholders | B) At every transition point where content moves from an internal analysis to a stakeholder-facing context | C) Only when the document contains client names or financial figures | D) Once, when the initial data is entered into Excel Copilot
correct_option: B
explanation: "SAFE abstraction must be applied at each handoff point — not just at the end. Content that is safe in an internal Excel analysis may contain Non-Public details that must be abstracted before it enters a Word brief or Outlook email."

item_2_type: mcq
sequence: 2
question_text: "An analyst applies TRACE to verify an Excel Copilot finding before drafting the Word section. Which domain skill does this represent in the end-to-end workflow?"
options: A) responsible_ai — protecting client data at a transition point | B) augmented_comm — choosing the correct Copilot surface | C) critical_eval — verifying AI-generated insights before acting on them | D) strategic_prompting — structuring the follow-up prompt correctly
correct_option: C
explanation: "Applying TRACE to verify a data finding before it enters the narrative is critical_eval — verifying AI outputs before acting on them — even though the tool being used is Excel Copilot."

item_3_type: mcq
sequence: 3
question_text: "An analyst must produce two versions of the same annual review for two subcommittees with different mandates. Which end-to-end workflow principle applies here?"
options: A) Apply SAFE abstraction twice — once per version | B) Apply STAKE to produce audience-specific versions rather than sending a generic document to both | C) Apply CRAF twice — once per prompt | D) Apply VERIFY to both versions before distribution
correct_option: B
explanation: "STAKE is the audience-tailoring framework. In an end-to-end workflow, it is applied when the same deliverable must serve multiple audiences with different decision frames."

item_4_type: performance_task
sequence: 4
question_text: "You are preparing the Horizon Program Annual Review for a programme sponsor and two board subcommittees (risk-focused and investment-focused). You have four inputs: an Excel metrics file, a Teams transcript, a draft strategy memo marked Internal Use Only, and last year's annual report. Walk through the end-to-end AI workflow for this deliverable. For each of the six skill domains, identify: (1) the stage in the workflow where that domain is most critical, (2) the specific action you would take, and (3) the tool you would use. Your response must reference all six domains: data_decision, critical_eval, relationship_intel, strategic_prompting, responsible_ai, augmented_comm."
scoring_rubric_criteria:
  key1: "data_decision and critical_eval: correctly applies Excel Copilot to surface performance highlights (data_decision), then applies TRACE to verify a flagged anomaly against the Teams transcript before it enters the narrative (critical_eval)"
  key2: "relationship_intel and strategic_prompting: correctly applies STAKE to identify each subcommittee's priority question, then uses CRAF in Word Copilot to draft audience-specific executive summary versions (relationship_intel + strategic_prompting)"
  key3: "responsible_ai: correctly identifies the Internal Use Only memo as a source of Non-Public data and applies SAFE abstraction before the partner financial figure enters any stakeholder-facing version"
  key4: "augmented_comm: correctly chains all Copilot surfaces (Excel → Teams → Word → Outlook) without manual re-entry, and identifies the correct surface for each step in the workflow"


