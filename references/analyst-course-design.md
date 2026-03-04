## MACHINE-READABLE HEADER

role\_prefix: an

company\_map:
course\_1: Project Titan
course\_2: Aurora Initiative
course\_3: Polar Manufacturing Inc.
course\_4: Operation Lighthouse
course\_5: Horizon Program

framework\_names:

*   CRAF Framework
*   VERIFY Checklist
*   The SAFE Abstraction Method
*   Copilot Surface Selector
*   End-to-End AI Workflow

real\_use\_case:
course\_1: Board Report Summaries
course\_2: Financial Variance Analyzer
course\_3: KYC / CIM Validation Agent
course\_4: Access to Copilot 365 for Business Development
course\_5: Streamline production of Quarterly analysis and reporting; Financial Variance Analyzer

***

## SECTION A — Role Entry

role\_id: an  
title: Analyst (Non-IT)  
description: "Produces research, financial models, risk assessments, and analytical reports (e.g., credit memos, performance dashboards, sector briefs) that inform decisions by internal stakeholders such as underwriters, account managers, and senior leadership. Works across diverse data sources (CRM records, financial statements, survey data, economic reports) and tools (Excel models, Power BI dashboards, SharePoint repositories) to synthesize insights. Does not manage external client relationships directly — outputs are internal deliverables that support decision-making in various business units (Risk Management, Finance, Business Development, etc.)."

***

## SECTION B — Domain Specs

### Domain: prompting

domain\_id: prompting  
title: Prompting for Outcomes  
description: "Structuring AI prompts with clear context, role, action, and format so that Copilot’s outputs are immediately useful in an analyst’s workflow — from summarizing complex financial reports and research documents to drafting internal memos, variance analyses, or slide notes for senior management."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Has not used AI prompting in daily analytical tasks. May try one-word or very vague prompts; cannot explain what makes a prompt effective."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Writes basic prompts (e.g., 'Summarize this report') and gets generic or overly long outputs that require significant manual revision. Often unsure how to guide AI to specific insights or formats needed for internal stakeholders."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses structured prompts that provide context (e.g., dataset or report background), define the AI’s role (e.g., financial analyst or risk advisor), specify the task (summary, analysis, etc.), and request a clear format (bulleted list, table, executive summary). The AI’s output is usually on-point and needs only minor editing to be useful."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Adapts and refines prompts for complex analytical scenarios. Anticipates when the AI might misinterpret a request and preempts issues by adding guiding details or constraints (e.g., excluding certain sections, targeting specific metrics or time periods). Iteratively improves prompts when initial output is off-target, resulting in high-quality drafts for internal reports or presentations."  
level\_4\_label: Champion  
level\_4\_descriptor: "Designs and shares effective prompt templates for common analyst tasks (financial analysis, risk memos, data quality summaries, etc.). Coaches colleagues on how to craft detailed prompts using frameworks like CRAF. Regularly identifies new opportunities to use advanced prompting techniques (e.g., multi-step chained prompts) to streamline analytical workflows across the team."

### Domain: verification

domain\_id: verification  
title: Verification and Judgment  
description: "Reviewing and validating AI-generated outputs with a skeptical, data-driven eye before using them in analysis or reports. This includes catching hallucinated facts or figures, misinterpreted data trends, or incorrect statements in Copilot’s summaries of financial data, risk reviews, meeting notes, and research findings."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Assumes Copilot’s outputs are accurate by default. Tends to copy-paste AI-generated analysis or summaries (e.g. variance explanations, credit memo drafts) into deliverables without checking against source data or verifying claims."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Skims AI outputs and corrects obvious mistakes like typos, but doesn’t systematically verify facts or numbers. May overlook subtle errors in financial calculations or misattributed statements when reviewing AI-created content."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Consistently cross-checks key details from AI outputs against reliable sources. For example, compares Copilot’s summarized financial figures or risk ratings to the original spreadsheet and CRM data, and removes or corrects any discrepancies. Understands that AI can ‘make up’ plausible-sounding explanations, so verifies any claims or analysis (such as reasons for a budget variance) by consulting the actual data or documents before presenting results."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Routinely identifies subtle inaccuracies or implausible reasoning in AI outputs. Flags statements that don’t align with source data (e.g., a trend that wasn’t actually in the dataset or a misinterpreted KPI) and uses judgment to decide what to keep, correct, or discard. May re-prompt Copilot for sources or rerun analyses with different parameters to validate findings. Prevents misinformation by requiring evidence for each major insight from the AI."  
level\_4\_label: Champion  
level\_4\_descriptor: "Develops verification checklists or standard operating procedures for the analyst team to follow when using AI-generated content. Trains colleagues on common failure modes of AI in analytics (like hallucinated numeric calculations or incorrect attributions in meeting notes) and shares strategies to mitigate them. Advocates for features that improve AI transparency (such as source citation) and helps establish a culture of 'trust but verify' when leveraging AI for analysis."

### Domain: data\_safety

domain\_id: data\_safety  
title: Data Safety and Compliance  
description: "Applying EDC’s strict guidelines for handling sensitive information when using AI tools. This involves always performing the public/non-public information test before using any data in Copilot, and abstracting, anonymizing, or aggregating details from non-public sources (client financials, internal plans, confidential reports) so that no protected or private data is exposed in AI prompts or outputs."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Unaware of EDC’s GenAI data restrictions. May carelessly paste confidential content (e.g., client financial statements, internal strategy documents, personal identifiers) into public AI tools or prompts, risking data leaks."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Knows in theory that non-public information shouldn’t be shared with external AI, but has trouble identifying what counts as sensitive in practice. Might inadvertently include details like client names, deal amounts, or internal emails in Copilot prompts, especially under time pressure."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Consistently applies the public vs. non-public test. Before using Copilot, checks if data comes from public sources (e.g., published annual reports, press releases) or is confidential (e.g., unpublished financial results, internal risk ratings, personally identifiable information). Uses safe prompting techniques: replaces specific names and figures with generic descriptors or ranges, and avoids entering any private details into prompts. Ensures AI-generated outputs do not reveal protected data."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Preemptively identifies borderline cases and uses creative strategies to preserve confidentiality while still getting value from AI. For example, summarizes an internal report by providing only high-level trends or anonymized labels ("Client A" instead of the real name) to Copilot. If unsure about a piece of information, errs on the side of caution or seeks guidance. Regularly removes or masks sensitive data from both prompts and AI outputs (e.g., wiping out account numbers or specific client indicators) before sharing results."  
level\_4\_label: Champion  
level\_4\_descriptor: "Serves as a go-to resource on GenAI data compliance. Actively educates peers on safe AI usage, creating team guidelines or tip sheets for anonymizing inputs. Anticipates new data-safety challenges (like summarizing an embargoed third-party market report) and works with Data Governance or Compliance to develop guardrails. Demonstrates that high-quality analysis can be done with AI without ever exposing confidential information."

### Domain: tool\_fluency

domain\_id: tool\_fluency  
title: Tool Fluency (M365 + Copilot)  
description: "Choosing the optimal Copilot-enabled Microsoft 365 application for each step of the analyst’s workflow and chaining multiple Copilot tools together efficiently. This means leveraging the full M365 suite — Excel, Word, PowerPoint, Outlook, Teams — so that data and context stay within the right tools (e.g., analyzing data in Excel Copilot, drafting reports in Word Copilot, summarizing meetings in Teams) and outputs can flow from one stage to the next without manual copy-paste."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Has not tried Copilot in any Microsoft 365 app. Unaware of which M365 tools offer Copilot or how they might assist in analysis tasks."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Has experimented with one Copilot surface (e.g., tried drafting an email with Outlook Copilot or asking a general question in Teams Chat). Tends to stick to familiar tools and may not think to use other Copilot-enabled apps. Still copies data manually between apps (e.g., copying a Teams meeting transcript into Word to summarize it) instead of using Copilot’s integrated capabilities."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses multiple Copilot surfaces for daily tasks. For example, employs Copilot in Excel to analyze data trends or create charts, then uses Copilot in Word to draft internal reports or summaries leveraging that data, and might use Teams Copilot to recap meetings. Builds simple two-step workflows (e.g., generating a Power BI visual and then asking Word Copilot to create a commentary for a report). Reduces redundant work by letting Copilot retrieve content from where it already lives (emails, documents, spreadsheets) instead of manually transferring information."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Designs complex multi-step workflows spanning three or more M365 Copilot tools. For instance, after a meeting, uses Teams Copilot to get a transcript summary and action items, feeds those insights into Word Copilot to draft a meeting recap or a project update, and finally uses Outlook Copilot to draft a polished email to stakeholders — weaving together outputs from each step. Chooses the starting tool wisely (e.g., opening an Excel file with Copilot to ask questions about the data directly in Excel). Quickly pivots to another Copilot (e.g., switching to PowerPoint to create a chart slide) when the task demands it."  
level\_4\_label: Champion  
level\_4\_descriptor: "Shares efficient Copilot workflow templates across teams (e.g. “how to go from data to deck to email using Copilot”). Stays on top of new Copilot features in various apps and identifies how they can streamline analytic processes (like using the latest Teams features for cross-meeting summaries or OneNote Copilot for research logs). Coaches colleagues on eliminating unnecessary manual steps — for example, demonstrating how to link Copilot outputs from one app to the next via OneDrive/SharePoint rather than copying text. Ensures the team is comfortable using the full Microsoft Copilot ecosystem end-to-end for analytical tasks."

***

## SECTION C — Course Specs

### Course 1 – Prompting for Outcomes

course\_id: an\_c1\_prompting  
role\_id: an  
primary\_domain: prompting  
sequence\_order: 1  
title: "Summarize and Succeed: Board-Ready Briefs"  
tagline: "Turn dense reports into clear board-level summaries using structured prompts."  
description: "Analysts frequently need to condense large volumes of information — like lengthy performance reports or research findings — into concise, digestible briefs for senior management and committees. In this course, you’ll learn how to craft effective prompts that give Copilot the right context and instructions to produce an output you can use directly in your internal reports and presentations. We introduce the CRAF prompting framework (Context, Role, Action, Format) and apply it to real analyst scenarios such as creating an executive summary of a complex quarterly report. Mastering this skill will save you time while ensuring the AI’s draft aligns with what your stakeholders need."  
real\_use\_case: "Board Report Summaries"

### Course 2 – Verification and Judgment

course\_id: an\_c2\_verification  
role\_id: an  
primary\_domain: verification  
sequence\_order: 2  
title: "Trust but Verify: Validating AI Analyses"  
tagline: "Never take AI at face value — learn to fact-check and refine Copilot’s outputs."  
description: "As an analyst, accuracy is non-negotiable — an AI-generated variance analysis or risk assessment is only useful if it’s correct. This course develops your ability to detect and correct errors or unfounded claims in Copilot’s output before you rely on them. You’ll practice using the VERIFY Checklist, a systematic approach to reviewing AI outputs: checking figures against source data, questioning assumptions, and fixing logical inconsistencies. Through a realistic Financial Planning & Analysis scenario (an AI-drafted budget variance explanation), you’ll sharpen your judgment in evaluating AI suggestions: identifying subtle mistakes in calculations or reasoning and ensuring the final analysis can withstand scrutiny from managers and auditors."  
real\_use\_case: "Financial Variance Analyzer"

### Course 3 – Data Safety and Compliance

course\_id: an\_c3\_data\_safety  
role\_id: an  
primary\_domain: data\_safety  
sequence\_order: 3  
title: "Protect the Data: Safe AI Usage for Analysts"  
tagline: "Leverage AI without compromise — guard confidential data and comply with EDC’s policies."  
description: "Working with data comes with great responsibility. This course empowers analysts to use Copilot effectively while strictly adhering to EDC’s data security and privacy rules. You will learn the SAFE Abstraction Method for GenAI: a four-step approach to ensure you never expose Non-Public EDC Information when using AI. In a simulated **Know-Your-Customer (KYC)** scenario, you’ll practice identifying sensitive content (like personal identifiers, financial details, or internal rankings) and transforming or removing it before prompting Copilot. You’ll also learn how to interpret EDC’s Responsible AI policy in day-to-day work — so you can confidently use AI for data cleaning, onboarding, and analysis tasks without risking compliance violations."  
real\_use\_case: "KYC / CIM Validation Agent"

### Course 4 – Tool Fluency (M365 + Copilot)

course\_id: an\_c4\_tool\_fluency  
role\_id: an  
primary\_domain: tool\_fluency  
sequence\_order: 4  
title: "Copilot Power-User: Right Tool for the Task"  
tagline: "Master the entire Copilot toolkit — Excel, Word, PowerPoint, Teams, and Outlook — in tandem."  
description: "Why copy-paste data between apps when Copilot can seamlessly assist you within each tool you use? In this course, analysts learn how to maximize productivity by using Copilot across Microsoft 365. Through a **Business Development** support scenario, you’ll practice a multi-step workflow: extracting insights from CRM data in Excel, drafting a quick briefing deck in PowerPoint, and composing a summary email in Outlook — all with Copilot’s help. The course will show you how to decide which Copilot surface is best for a given task (e.g., Teams for meeting notes, Excel for analysis, Word for report writing) and how to link outputs from one tool to the next. By the end, you’ll be comfortable orchestrating Copilot across your toolset, reducing manual effort and keeping your analysis within EDC’s secure environment."  
real\_use\_case: "Access to Copilot 365 for Business Development"

### Course 5 – Capstone

course\_id: an\_c5\_capstone  
role\_id: an  
primary\_domain: prompting  
sequence\_order: 5  
title: "AI-Assisted End-to-End Analysis (Capstone)"  
tagline: "Put it all together: an AI-driven project from raw data to final presentation."  
description: "This capstone integrates all four skill domains in a realistic end-to-end workflow. You’ll step into the shoes of an EDC analyst tackling a time-sensitive **quarterly portfolio review**. Starting with a trove of inputs — an Excel dataset of portfolio metrics, a transcript of a team meeting, and an internal strategy memo — you will use Copilot to help at each stage: generating a draft analysis (Prompting), cross-checking and refining it (Verification), safeguarding client and EDC confidential info (Data Safety), and using multiple M365 tools to compile and share results (Tool Fluency). By completing this course, you’ll demonstrate your ability to orchestrate Copilot thoughtfully in complex, multi-step analytical tasks, just as you would on the job."  
real\_use\_case: "Streamline production of Quarterly analysis and reporting; Financial Variance Analyzer"

***

## SECTION D — Scenario Seeds

### Course 1 Scenario

scenario\_text: "It’s Monday morning, and your team has produced a **30-page Q4 performance review report** for a major internal project, <Project Titan>. On Wednesday, you need to present a one-page summary of this report to EDC’s Executive Committee. You want to use Copilot to draft the summary more quickly."  
task\_1\_text: "Write an initial prompt to **summarize the Project Titan Q4 Performance Report** for an executive-level audience. Include any context you think the AI will need (e.g. what the report covers, who the audience is), and specify the desired output (e.g. an executive summary highlighting key results)."  
task\_2\_text: "Copilot’s first draft is a generic summary that misses **several critical issues** from the report (for example, a major budget overrun in Project Titan’s expenses). Revise your prompt to **emphasize that the summary should highlight major issues and their impacts**, not just positive outcomes."  
task\_3\_text: "The revised summary is very detailed and too long for a one-page brief. Refine your prompt’s **Format** instructions to get a **more concise output** — for instance, by specifying a bullet-point list or a 200-word limit focusing on the top 3–5 points."  
task\_4\_text: "The summary still contains some technical jargon and granular data points that might confuse the Executive Committee. Add a constraint or instruction to your prompt to **ensure the final summary is written in clear, non-technical language** and omits low-level details that **Executives don’t need to see**."

coach\_system\_prompt: "You are an AI skills coach for EDC analysts learning to craft effective prompts. In this scenario, the learner is using Copilot to summarize a complex internal report for senior executives. Guide the learner with questions and hints about the CRAF framework — without giving away the full prompt. For example, if the prompt is missing context (like the project name or key data), ask them what context could be added. If the output is too generic or too detailed, remind them about adding specific **Action** instructions or tightening the **Format**. Ensure they avoid including any confidential numbers or names directly in the prompt (they should abstract if needed). Encourage them to iterate step by step, improving the prompt after seeing each draft."

### Course 2 Scenario

scenario\_text: "You’re in the **Enterprise Analytics & Forecasting** team and have used Copilot in Excel to generate a **variance analysis of the Aurora Initiative’s Q3 budget vs. actuals**. Copilot produced a narrative explaining the differences, including several statistics and reasons for variances."  
task\_1\_text: "Before using the AI-generated variance explanation, identify at least **one figure or claim** in the draft that you should verify. (For example, a percentage or dollar amount change that seems high or unexpected.)"  
task\_2\_text: "Now, **verify that figure** using the source data: cross-check it against the actual figures in the Aurora Initiative’s financial spreadsheet. Once you find the correct value, **update the AI’s statement** with the accurate number (if it was wrong) or mark it as confirmed (if it was right)."  
task\_3\_text: "The Copilot narrative attributed a cost increase to 'rising travel expenses,' but your detailed data shows travel costs actually went down. **Ask Copilot a follow-up or use a re-prompt** to correct this reasoning. (For example, you might direct the AI to only cite factors that are supported by the data, or you might manually adjust the explanation yourself.)"  
task\_4\_text: "Reflecting on this process, list **two specific checks** from the VERIFY Checklist that you applied (or should have applied) to ensure the final variance analysis is accurate and trustworthy. (For instance, cross-checking totals against the source data, verifying that explanations match known business context, etc.)"

coach\_system\_prompt: "You are an AI skills coach for EDC analysts practicing how to verify AI outputs. The learner has an AI-generated budget variance analysis for the Aurora Initiative and needs to vet it. Guide them by asking questions that prompt verification steps. For task 1, ask what specific figure stands out as needing confirmation. For task 2, ensure they mention how they would confirm or correct it (e.g. checking the financial system or spreadsheet). For task 3, prompt them to address the unsupported claim by either re-prompting Copilot with a constraint or using their own judgment to fix it. Throughout, remind them to use concrete data and to consider whether each part of the AI’s output can be backed by evidence. Do **not** let them just accept the AI’s reasoning without question."

### Course 3 Scenario

scenario\_text: "You are an **Information Analyst** in the Company Information Management (CIM) team. You’ve been assigned a new customer onboarding case: a company named <Polar Manufacturing Inc.>. You have various documents from the client, including a **certificate of incorporation (in French)** and a corporate ownership chart. You want to use Copilot to speed up verification and data entry, but you must ensure sensitive data stays protected."  
task\_1\_text: "Write a Copilot prompt to **summarize the French incorporation document** for Polar Manufacturing Inc. while **following EDC’s data safety rules**. (Hint: provide necessary context for translation/summary, but do **not** include any Non-Public Information like full names of individuals or registration numbers in your prompt.)"  
task\_2\_text: "Copilot’s summary of the document comes back, but you notice it **included a personal phone number and address of a director** from the text. This information is confidential. **Edit or re-prompt** to produce a version of the summary that **omits or anonymizes personal identifiers** (e.g., refer to 'the company’s director' without naming them, and exclude the exact contact details)."  
task\_3\_text: "For another new customer file, you need to get a summary of a sensitive internal credit report about a client’s financial health. **Explain in one sentence** how you would apply the "public/non-public" test *before* using Copilot, to ensure you don’t include any restricted information in your prompt."  
task\_4\_text: "Finally, your team asks for guidance on using AI within policy. **Draft a one-sentence tip** for fellow analysts, explaining how to handle confidential numerical data (like sales figures or credit limits) when using Copilot. (For example, should you share exact figures, ranges, percentages, or something else?)"

coach\_system\_prompt: "You are an AI skills coach for EDC analysts focused on data safety. The learner is working through a customer onboarding scenario using Copilot. Guide them to ensure **no confidential data** is shared in prompts or outputs. For task 1, ensure they include translation context but exclude any private identifiers or exact numbers from the prompt (you can ask what could be considered sensitive). For task 2, if they simply accept the AI’s output, ask how they might remove or mask the personal data. For the last two tasks, prompt them to articulate EDC’s rules (the public vs. non-public test and strategies like using ranges or generic terms instead of specific confidential data). Do not reveal policy text directly; let them frame it in their own words. Always remind them that protecting client and EDC data is the priority."

### Course 4 Scenario

scenario\_text: "You are a **Business Development Analyst** supporting the Mid-Market team. You have a list of lapsed clients and recent market data, and you’re tasked with identifying **win-back opportunities** for a new outreach campaign called <Operation Lighthouse>. You’ll need to analyze data, create a presentation slide, and send out an email – all in one morning – so you decide to use Copilot across **multiple M365 tools** to speed things up."  
task\_1\_text: "You export a list of lapsed clients and their recent activity from the C3 CRM. Open **Copilot in Excel** with this data and ask for insights: for example, **identify the top 5 clients** that saw significant drop-offs in business with EDC last year. Write the Excel Copilot prompt you would use to perform this analysis (include what you define as 'significant drop-off' so the AI knows what to look for)."  
task\_2\_text: "Copilot in Excel provides the top 5 clients and some key figures. Now you need a visual aid. Switch to **Copilot in PowerPoint**. Write a prompt to **create a single slide** (title it "Operation Lighthouse – Top 5 Win-Back Targets") that lists these 5 clients and one key insight (e.g., lost business volume) for each, as bullet points. (Assume you’ve pasted or linked the data from Excel into PowerPoint already.)"  
task\_3\_text: "Next, use **Copilot in Outlook** to draft a brief **email to the sales directors** in your team. The email should introduce the attached "Operation Lighthouse" slide, highlight that these are the top five lapsed clients to focus on, and invite the team to a meeting to discuss re-engagement strategies."  
task\_4\_text: "Thinking ahead, describe in 1–2 sentences how you could use Copilot to **streamline this entire workflow** the next time you must do it (from data extraction to analysis to presentation and email). Focus on how using multiple Copilot tools together saved time and which manual steps it helped eliminate."

coach\_system\_prompt: "You are an AI skills coach for EDC analysts practicing multi-tool Copilot workflows. The learner is in a Business Development scenario (Operation Lighthouse) using Excel, PowerPoint, and Outlook Copilot together. Guide them through the steps without giving the answers directly. For task 1, ensure they specify what constitutes a 'significant drop-off' and that they frame the question for Excel clearly (e.g., sorting or identifying top values). For task 2, remind them to think about what context PowerPoint Copilot needs (like the title, and the data that’s been imported). For task 3, encourage them to mention key pieces from the slide in the email and maintain a professional tone. For task 4, prompt them to reflect on how using different Copilot surfaces in sequence (Excel → PowerPoint → Outlook) avoids manual work (no copy-pasting data by hand, etc.) and how they plan the sequence. Ensure they are choosing the right tool for each part of the task."

### Course 5 Scenario

scenario\_text: "You are part of EDC’s **Portfolio Analytics** team preparing the **Horizon Program** quarterly review. You have multiple inputs: a detailed Excel file of portfolio performance metrics, a transcript of a recent portfolio review **meeting**, and an internal strategy memo about the Horizon Program’s goals. You need to produce a concise update for senior management and ensure it’s accurate and policy-compliant."  
task\_1\_text: "Start with **Copilot in Excel**. Write a prompt to analyze the portfolio metrics spreadsheet and identify **three key performance highlights** and **two areas of concern** for the quarter. Include enough context in your prompt (e.g., that this is for a quarterly portfolio review) so Copilot knows the purpose of the analysis."  
task\_2\_text: "One of Copilot’s highlighted “areas of concern” is a metric decline that you suspect is actually due to a data anomaly (and wasn’t mentioned in your team’s meeting). **Double-check this insight**: for example, you could **ask Teams Copilot** to search the Horizon Program meeting transcript for any discussion of that metric. What follow-up prompt or action would you take to verify whether this decline was already explained in the meeting?"  
task\_3\_text: "Now, open **Copilot in Word** to draft the one-page management update. Write a prompt guiding Copilot to combine the verified information: the three highlights from Excel, any clarifications from the meeting, and relevant points from the strategy memo. Emphasize that the output should be suitable for senior management (e.g., short, fact-focused paragraphs, no confidential details, and a brief recommendation section at the end)."  
task\_4\_text: "During editing, you notice Copilot’s draft briefly mentions an internal system name and includes a detailed figure from the strategy memo marked "EDC Confidential." These shouldn’t be in the version for management. **In one sentence, note what you will do to fix this** before finalizing the report (consider both removing sensitive content and applying the verification and prompting principles you've learned)."

coach\_system\_prompt: "You are an AI skills coach for EDC analysts working on an end-to-end AI-assisted project. The learner is combining data, meeting notes, and a memo using multiple Copilot tools. Guide them step-by-step. For task 1, ensure they craft a clear Excel prompt that yields both highlights and concerns with context. For task 2, encourage verifying suspicious insights by leveraging the Teams transcript (e.g., asking Copilot if that metric was discussed). For task 3, remind them to include all sources (data, meeting, memo) in the Word prompt and to specify an executive-friendly format. For task 4, check that they recognize the data safety and verification issues — they should mention removing the system name or confidential figure and double-checking that the final content is appropriate. Keep your guidance supportive and ask questions that prompt reflection, without directly providing the answer."

***

## SECTION E — Reading Concepts

### Course 1 Reading

framework\_name: "CRAF Framework (Context, Role, Action, Format)"  
concept\_text: "Great AI outputs start with great inputs. The **CRAF Framework** helps analysts remember the four key elements of a well-structured Copilot prompt:

*   **Context:** Provide background details. (What are you analyzing or summarizing? For whom?) For example, "Q4 performance report for Project Titan, to brief our Executive Team." Without context, Copilot might produce generic results that miss the point.
*   **Role:** Tell Copilot what perspective to take. (As an analyst, do you want it to behave like a financial advisor? A data analyst? An executive?) Specifying a role helps calibrate the tone and depth. E.g., "Act as a senior financial analyst at EDC." This way, the AI will use appropriate terminology and focus on relevant details.
*   **Action:** Be explicit about what you need. Do you want a summary, a list of insights, a comparison, an email draft? E.g., "Draft a one-page **executive summary** of the report, highlighting any performance issues and recommendations." Clear instructions prevent the AI from giving you something you didn’t want (like a lengthy essay when you needed bullet points).
*   **Format:** State how the output should look. Options include bullet points, tables, specified length, or sections with headings. For instance: "Format the output as 5 bullet points under 'Key Highlights' and 'Key Risks'." Format guides ensure the AI’s response is presentation-ready for your needs.  
    By including **all four CRAF elements** in your prompt, you dramatically increase the chances of getting a useful result. The AI knows *who* it’s writing as, *what* it’s writing about, *what* exactly it needs to produce, and *how* to present it."  
    good\_example: "*Prompt:* **"Context:** EDC 2025 Q2 Financial Results – an internal 20-page report with detailed financials and explanations of variances. **Role:** You are a financial analyst preparing a brief for the CFO. **Action:** Summarize the key points (revenue, expenses, profit and major variances) in plain language. **Format:** Provide a bulleted executive summary, 5 bullets or fewer, highlighting any areas of concern in bold."  
    **Why it works:** The prompt gives Copilot a clear picture of the situation (what report it’s summarizing and why), tells it to adopt the perspective of a financial analyst to match the expected insight level, explicitly asks for a summary of specific elements, and even defines the desired length and style of the output. The resulting draft is concise, focused, and needs minimal editing."  
    anti\_pattern: "*Prompt:* "Summarize this document for me."  
    **Why it fails:** There is no context about which document or what the focus should be. The AI doesn’t know who the audience is or which details matter, so the output might be overly generic or miss critical points. There is also no format guidance; you could end up with a verbose essay rather than the sharp executive summary you needed, meaning you’ll spend extra time fixing it."  
    takeaway: "Always set your AI up for success by giving it the right guidance. A well-crafted prompt using **CRAF** ensures that Copilot understands the content it’s working with, the role it should take, the precise task you need, and the format you expect. This results in outputs that are far closer to what you envisioned — saving you time in editing and rework."

### Course 2 Reading

framework\_name: "VERIFY Checklist"  
concept\_text: "Even the best AI can get things wrong or make things up. As an analyst, you must **VERIFY** every important detail. Use this mental checklist each time you review an AI-generated report or analysis:

*   **Verify key figures against source data:** Double-check numbers, dates, and totals. For instance, if Copilot says *"sales grew 15%"*, confirm that with the actual sales report or Excel sheet.
*   **Ensure reasoning matches evidence:** Ask yourself, "Do the explanations make sense given what I know?" If Copilot explains a variance by a factor you didn’t see in the data, it might be guessing. Press pause and investigate.
*   **Review for hallucinations or extra content:** AI might insert plausible-sounding facts that weren’t in your material. Look out for any names, statistics, or claims that you don’t recognize from the source. If Copilot summarizes a credit report, for example, check that every risk factor it lists was actually mentioned in the report.
*   **Find the original source if possible:** If Copilot references something (like "expenses rose by 10% due to travel costs"), trace that back to the original document or data. Use search or your own memory of the materials to confirm it.
*   **Yield to human judgment:** Ultimately, use your expertise to decide what stays and what goes. Don’t hesitate to remove or correct an AI-generated sentence if it seems off. It’s better to have a partially incomplete report than to include a confidently wrong statement.  
    By following the **VERIFY** Checklist, you ensure that **Copilot becomes a helpful assistant, not an authoritative source**. The result: you get the efficiency benefits of AI without compromising the accuracy and credibility of your analysis."  
    good\_example: "You use Copilot to draft a **variance analysis** of departmental spending. The AI output claims travel costs surged by 50%. Instead of just accepting that, you check the ledgers and realize travel costs actually *fell* 5%. You remove the incorrect sentence about travel costs and add a note explaining the true cause of increased expenses. **Why it works:** You caught a critical error that could have misled decision-makers. By verifying against the ledger (source data) and correcting the mistake, your final report remains accurate."  
    anti\_pattern: "An analyst copies a Copilot-generated **credit risk summary** directly into an email to a risk committee without reading it fully. The summary mentions a debtor default that never actually happened. **Why it fails:** The analyst didn’t verify the AI’s statements against the actual credit file, resulting in a false alarm. Such oversights can damage credibility and lead to poor decisions. The error could have been caught by carefully reviewing the output and checking it against known facts."  
    takeaway: "Copilot can draft analyses quickly, but it’s your responsibility to **verify every critical detail**. Always cross-check numbers and claims using trusted sources or calculations. If something looks surprising or unfamiliar, treat it as a red flag. By combining Copilot’s speed with your professional judgment and thorough verification, you ensure the final output is both efficient *and* reliable."

### Course 3 Reading

framework\_name: "SAFE Abstraction Method"  
concept\_text: "Before using Copilot with any real data, EDC analysts must **stay SAFE** — a method to ensure sensitive info is protected:

*   **S – Scrutinize the data:** Identify any Non-Public Information. This includes client confidential details (financials, ownership, personal data) and internal EDC information not meant for public disclosure (strategic plans, unpublished results, risk ratings). Always ask: *“Is this information available in the public domain?”* If the answer is *no or unsure*, treat it as sensitive.
*   **A – Abstract or Anonymize:** Once you spot sensitive elements, either remove them from your prompt or replace them with generic descriptors. For example, instead of feeding Copilot "John Doe from <Company>XYZ Corp</Company> with loan #12345 for $5M", you might say "the client’s CEO from a mid-sized tech company with a moderate loan balance". This shields actual identities and exact figures.
*   **F – Filter outputs:** After Copilot generates a response, review it for any accidentally revealed confidential info. If the AI’s answer includes a specific name, account number, or any private detail, edit it out. You are responsible for ensuring the final text is scrubbed of non-public data.
*   **E – Ensure compliance:** Remember EDC’s Responsible AI policy and data classification rules. Use only EDC-approved tools (Copilot is within our M365 tenant, which is good). Never paste data into unapproved external AI apps. When in doubt about a piece of information, consult your manager or simply *don’t include it* in your prompt.  
    Following the **SAFE** method means you still get insights from AI while keeping EDC’s and clients’ secrets safe. You’ll be able to leverage Copilot for things like KYC, data cleaning, and report drafting *without ever violating trust or policy*."  
    good\_example: "An **Information Analyst** needs to update a company profile using copilot. The analyst has a PDF with the client’s financial statements (non-public) and a news article about the client’s industry (public). They ask Copilot to summarize *only the industry trends from the news article* (public info) and consciously avoid sharing the private financials in the prompt. Later, when drafting a risk analysis using Copilot, they refer to the client as "the company" and convert exact revenue numbers into a percentage growth figure. **Why it works:** The analyst gets useful insights (industry trends, growth rates) from AI while keeping specific confidential figures and names out of the AI’s input and output."  
    anti\_pattern: "An analyst wants to translate a client’s **financial statement** from French to English, so they paste the entire PDF into a free online translation AI. **Why it fails:** The financial statement is Non-Public EDC Information, and uploading it to an unapproved external AI service violates EDC’s policies. There’s also no guarantee where that data might be stored or who can access it. The analyst should have used an internal tool or translated only the non-sensitive parts, keeping client data secure."  
    takeaway: "Always think twice before sharing information with an AI. When using Copilot or any AI, **if the data isn’t public, don’t paste it**. But that doesn’t mean you can’t use AI at all — it means you use SAFE abstraction techniques to still get the help you need (by describing or summarizing data in general terms) without exposing sensitive details. This ensures you remain compliant while working faster with AI."

### Course 4 Reading

framework\_name: "Copilot Surface Selector"  
concept\_text: "Microsoft 365 offers Copilot assistance in various apps — the key is to use the **right tool for the right task**. As an analyst, you often juggle emails, spreadsheets, documents, presentations, and meetings. The **Copilot Surface Selector** mindset will help you decide which Copilot to engage for a given job, and how to connect outputs from one tool to the next:\\

*   **Emails & Threads → Use Outlook Copilot:** For drafting or summarizing emails and extracting key points from lengthy email threads. Example: Use Outlook’s Copilot to summarize a long email chain with a client manager and draft a clear response with next steps.
*   **Data & Calculations → Use Excel Copilot:** For analyzing datasets, creating charts, and running quick calculations. If you have a sales dataset or budget in Excel, ask Excel’s Copilot to analyze trends or identify anomalies, instead of copying data into Word.
*   **Reports & Documents → Use Word Copilot:** For drafting and refining written reports, proposals, or memos. When writing a credit review or process document, open Copilot in Word so it can pull from the document’s content directly and help you format or summarize it.
*   **Presentations & Visuals → Use PowerPoint Copilot:** For generating slides or summarizing content into visual bullet points. If you need a slide deck of key insights, feed Copilot the core points (or an existing report) in PowerPoint to get a first draft of slides.
*   **Meetings & Notes → Use Teams Copilot (Recap):** After important meetings, use Teams Copilot’s meeting recap to get summaries of discussions, decisions, and action items, which you can then refine or integrate into reports.  
    The **Copilot Surface Selector** approach often means stringing these tools together: e.g., summarize a meeting in Teams → use that to draft a report in Word → pull in data via Excel → finalize slides in PowerPoint. The result: you save time and reduce manual copy-paste, with Copilot preserving context at each step."  
    good\_example: "After a portfolio review meeting, an analyst uses **Teams Copilot** to get the meeting recap and action items. Next, they open **Word Copilot** and prompt it to draft a follow-up report, referencing the transcript summary (saved to OneDrive) and some financial figures from an Excel file. Finally, they use **Outlook Copilot** to draft an email to stakeholders with key highlights from the attached report. **Why it works:** Each Copilot instance is used in the application best suited for the task (Teams for meeting notes, Word for writing the report, Outlook for emailing). The analyst can pull data and content directly from the integrated tools (OneDrive files, transcript) at each step, rather than manually transferring information, which saves time and reduces errors."  
    anti\_pattern: "An analyst tries to use a single Copilot Chat in Teams to do everything – from crunching numbers to writing the final email – by pasting raw spreadsheet data and long text and saying "write my report." **Why it fails:** Using the wrong Copilot surface leads to inefficient or poor results. The AI isn’t as effective because it doesn’t have the native access to the spreadsheet’s structure or the email context. The analyst ends up with a messy output (and possibly violates data policies by pasting sensitive data). They spend more time cleaning it up than they would have by using the dedicated Copilot tools in Excel, Word, and Outlook that are designed for those specific tasks."  
    takeaway: "Think of Copilot as an assistant **built into each app you use**. When you match the task to the right Copilot (email-related tasks in Outlook, data analysis in Excel, documentation in Word, etc.), you’ll get far better results with less cleanup. Moreover, by chaining these tools you maintain context and stay within EDC’s secure environment. **Switch Copilot gears** as you move through your workflow – it’s like having a team of specialized assistants, each one ready in the app where they’re strongest."

### Course 5 Reading

framework\_name: "End-to-End AI Workflow"  
concept\_text: "For complex projects, you can amplify your productivity by weaving all your AI skills together into an end-to-end workflow. This means planning how you’ll use Copilot at each step: from initial data gathering to final communication. Key principles include:

1.  **Plan the stages:** Break the task into phases (e.g., data analysis, drafting report, creating slides, crafting emails). Decide which Copilot tool fits each phase, and in what order. Starting in the right app ensures you have relevant context at your fingertips (data in Excel, transcripts in Teams, etc.).
2.  **Prompt intentionally at each step:** Apply the CRAF framework every time you use Copilot. For instance, when moving from an analysis in Excel to writing a report in Word, reformulate the context (“as per the analysis above…”) and specify the format anew (perhaps now you need full sentences instead of bullet points).
3.  **Verify along the way:** Don’t wait until the end to verify everything; incorporate checks after each major AI-driven step. If Excel Copilot gives you an insight, cross-check it before basing the Word draft on it. If Word Copilot drafts a report, review it thoroughly before sending it to PowerPoint or Outlook. Early correction prevents error compounding.
4.  **Ensure data safety at transitions:** When moving content from one tool to another, keep an eye out for any sensitive info that might slip through. For example, an AI-generated draft might include a confidential detail that was fine for internal analysis but not for a broader audience — remove or sanitize it before the next step.  
    By mastering an **End-to-End AI Workflow**, you transform Copilot from a one-off helper into a holistic productivity partner. You’re not just using AI in isolation; you’re orchestrating it throughout your process, combining tools and applying your prompting, verification, and data safety skills at every step. The payoff is a streamlined workflow where mundane tasks are accelerated and you retain full control over accuracy and compliance."  
    good\_example: "An FP\&A **analyst uses Copilot throughout an entire quarterly reporting process**. They start by using Excel Copilot to crunch the latest financials and identify key trends. Then, they feed those trends into Word Copilot to draft the narrative for the management report. They interrupt the process to verify Copilot’s explanations with the actual financial data and ensure no internal-only figures (like unannounced earnings targets) are mentioned. Next, they use PowerPoint Copilot to generate a slide deck of highlights for the executive meeting, drawing from the verified Word document. Finally, they use Outlook Copilot to draft an email to executives attaching the report and slides. **Why it works:** The analyst leveraged each Copilot where it was strongest and stitched the outputs together. By verifying and cleaning at each stage, the final deliverables were accurate and contained no sensitive info — all accomplished in a fraction of the time it would normally take."  
    anti\_pattern: "An analyst attempts to use Copilot for a complex project without a plan. They dump a mix of data and instructions into a single prompt in a random app, hoping for a finished analysis in one go. **Why it fails:** The output is disorganized and filled with errors. Without a step-by-step approach, the AI wasn’t given proper context at each stage. The analyst also neglected to verify intermediate results or remove confidential data, resulting in an error-riddled and non-compliant final product. In the end, they have to redo the work manually under tight deadlines — losing the very efficiency gains AI should provide."  
    takeaway: "Treat Copilot as a series of collaborative steps in your workflow, not a magic one-click solution. An effective end-to-end AI-assisted workflow involves using multiple Copilot tools in sequence, with you as the conductor — cueing up the right tool, feeding it the right prompt, and checking its output before moving to the next stage. This ensures you harness AI’s speed while you, the analyst, remain in control of quality and compliance throughout the process."

***

## SECTION F — Diagnostic Item Seeds

### Diagnostic: prompting

**Item 1 – mcq**  
question\_text: "An analyst writes the following prompt to Copilot: *"Summarize the attached 20-page industry report."* Which **CRAF element** is most obviously missing from this prompt?"  
options: A) Context about what specifically to focus on in the report  
B) A Role instruction for the AI  
C) A request for output in bullet point Format  
D) A specified Tone or style  
correct\_option: A  
scoring: correct = 4, incorrect = 0  
rationale: "The prompt lacks Context — it doesn’t tell Copilot what the summary is for or which points are important. Without context (e.g., purpose or audience for the summary), the AI may produce a generic overview rather than the focused insight the analyst needs."

**Item 2 – prompt\_sandbox**  
scenario\_text: "You have a detailed 15-page **internal report on customer service performance** that you need to summarize for a meeting with the VP of Customer Experience. The report covers multiple metrics (turnaround times, customer satisfaction scores, case volumes) and highlights a recent decline in satisfaction. The VP only has 5 minutes to read your summary, and cares mainly about issues and recommended fixes."  
question\_text: "Write a **CRAF-formatted prompt** to get a concise summary of the customer service performance report for the VP. Your prompt should provide Copilot with appropriate context, specify its role, clearly state the action, and describe the desired format of the output."  
scoring\_rubric\_criteria:

*   "Includes relevant **Context** (e.g., report topic, key problem of declining satisfaction, and that the audience is the VP of Customer Experience)": 1 point
*   "Sets a **Role** for the AI (e.g., as a data analyst or customer experience analyst preparing a VP brief)": 1 point
*   "Defines a clear **Action** (e.g., to summarize key findings and recommended fixes)": 1 point
*   "Provides a **Format** or length (e.g., brief executive summary or bullet points limited to a certain number or length appropriate for 5-minute read)": 1 point

**Item 3 – micro\_task**  
scenario\_text: "An analyst used Copilot to help prepare a research summary, but the result was too generic. The Copilot output begins: *"In today’s dynamic business environment, companies face many challenges..."* — which doesn’t mention any specifics from the research. The prompt the analyst gave was: *"Help me summarize the current market trends report."*"  
question\_text: "In one sentence, explain **why the Copilot’s summary came out generic** and **name two CRAF elements that were missing or insufficient in the analyst’s prompt** (from Context, Role, Action, Format)."  
scoring\_rubric\_criteria:

*   "Explanation identifies that **lack of specific context** led to a generic summary (e.g., the prompt didn’t provide details about which market or what to focus on)": 2 points
*   "Correctly names **two CRAF elements** that were missing or too vague (likely Context and Format or Context and Action in this example)": 2 points

### Diagnostic: verification

**Item 1 – mcq**  
question\_text: "When Copilot generates an analysis of your data, what is the **best practice** before you share or finalize the content?"  
options: A) Trust that the Copilot output is accurate if it looks confident  
B) Cross-check the key facts and figures against original data or reports  
C) Rely on a second AI to verify the first AI’s output  
D) Only correct obvious spelling or grammar issues  
correct\_option: B  
scoring: correct = 4, incorrect = 0  
rationale: "The most important step is to verify the content against authoritative sources. Copilot’s output can contain errors (even if it sounds confident), so an analyst should always cross-verify numbers, claims, and conclusions with the original data or documents before using the AI-generated content."

**Item 2 – prompt\_sandbox**  
scenario\_text: "Copilot created a draft analysis for **Project Aurora** that states: *"Profit in Q3 was $2 million higher than Q2, a 10% increase, due to improved operational efficiency."* You recall that Project Aurora had some one-time accounting adjustments in Q3, and you’re not sure the 10% figure is correct."  
question\_text: "Write a follow-up **Copilot prompt** to verify the accuracy of this statement. Your prompt should make Copilot double-check the profit figures and explain whether the *"10% increase due to operational efficiency"* claim is supported by the data (and if not, correct it)."  
scoring\_rubric\_criteria:

*   "Specifically references the profit figures or percentage in question (e.g., asking Copilot to check Q2 vs Q3 profit values)": 1 point
*   "Requests a verification or source for the claim (e.g., *"confirm if profit increased by 10% and cite how you know"*)": 1 point
*   "Mentions or hints at the known context (e.g., one-time adjustments or ensuring the explanation matches actual causes)": 1 point
*   "Maintains a neutral, analytical tone appropriate for an internal query": 1 point

**Item 3 – micro\_task**  
scenario\_text: "Copilot produced a summary of a risk review which includes a statement: *"The client’s revenue grew 25% last year,"* but the financial statements show only 5% growth. The analyst forwarded the summary to the team without checking. This was later caught as a mistake by a manager."  
question\_text: "In one sentence, **identify the analyst’s mistake** in this situation and **state what verification step from the checklist they missed**."  
scoring\_rubric\_criteria:

*   "Correctly identifies that the analyst failed to verify the AI’s statement (they took Copilot’s 25% growth claim at face value without cross-checking it against the actual financial statements)": 2 points
*   "References the specific verification step they missed (e.g., cross-checking the revenue figure against source data)": 2 points

### Diagnostic: data\_safety

**Item 1 – mcq**  
question\_text: "Which of the following **would be considered Non-Public EDC information** that you should *never* include in a Copilot prompt or conversation?"  
options: A) A statistic from EDC’s published annual report (last year’s total assets)  
B) The credit risk rating and internal loan exposure for a specific client  
C) A news headline about one of EDC’s customers  
D) The stock price of a publicly traded company client  
correct\_option: B  
scoring: correct = 4, incorrect = 0  
rationale: "Internal credit risk ratings and loan exposure figures for a client are confidential, Non-Public EDC Information. They must not be shared with external tools (including AI) or outside parties. In contrast, information that’s publicly available (like something in EDC’s annual report or a published stock price) isn’t confidential and wouldn’t violate policy if referenced appropriately."

**Item 2 – prompt\_sandbox**  
scenario\_text: "Original prompt (unsafe): *"Summarize our client <Company>AlphaTech Corp</Company>’s latest financial statement, which shows revenue of $120 million CAD and net income of $5.4 million CAD, and mention any issues. The CFO is Jane Doe."*  
This prompt contains **Non-Public Information** (the revenue and income are not public, and it names a person). You need to use Copilot while following EDC’s data safety rules."  
question\_text: "Rewrite the above prompt in a **data-safe way**. You still want a summary of the financial statement and any issues, but you **must remove or generalize the sensitive details** (the company name, exact figures, and any personal names) in the prompt."  
scoring\_rubric\_criteria:

*   "Company name is removed or replaced with a generic description (e.g., 'the client', or 'a mid-sized technology company')": 1 point
*   "Specific financial figures (revenue, income) are either omitted or converted into a non-identifying form (e.g., percentages, general terms like 'significant increase')": 1 point
*   "Personal name (CFO’s name) is removed or replaced with a role-only descriptor (e.g., 'the CFO')": 1 point
*   "Prompt still provides enough context for Copilot to do a useful summary (e.g., referencing it as a financial statement for a certain period, and asking for key issues)": 1 point

**Item 3 – micro\_task**  
scenario\_text: "An analyst is tempted to **use a free public AI tool** to translate a confidential contract quickly. This contract contains sensitive customer data and has not been published anywhere. According to EDC’s policies, why is this a bad idea?"  
question\_text: "In one sentence, explain **which policy rule the analyst would be breaking** by using an unapproved public GenAI tool for a confidential document, and **why this is dangerous**."  
scoring\_rubric\_criteria:

*   "Correctly identifies that this would violate EDC’s **Responsible Use of GenAI Policy** (specifically, the prohibition on inputting Non-Public EDC Information into unapproved/public AI tools)": 2 points
*   "Provides a valid reason, such as the risk of exposing sensitive client data to an external system or loss of control over where the data might be stored": 2 points

### Diagnostic: tool\_fluency

**Item 1 – mcq**  
question\_text: "You need Copilot’s help to digest the outcomes of yesterday’s lengthy team meeting and identify action items. Which **Copilot tool** should you use first?"  
options: A) Copilot in Word (to write a document)  
B) Copilot in Excel (to analyze data)  
C) Copilot in Teams (to generate a meeting recap)  
D) Copilot in Outlook (to draft an email)  
correct\_option: C  
scoring: correct = 4, incorrect = 0  
rationale: "Copilot in Teams (specifically the Teams meeting recap feature) is designed to summarize meetings, capturing key points and action items. Using Teams Copilot right after the meeting is the most efficient way to get a recap. The other tools (Word, Excel, Outlook) are not meant for directly summarizing meetings."

**Item 2 – prompt\_sandbox**  
scenario\_text: "You have a **spreadsheet of Q1 sales data by region** and want to quickly identify trends. You could copy the data into a Word document for Copilot to summarize, but that’s not efficient. Instead, you decide to use Copilot within Excel."  
question\_text: "Write a prompt *in Excel Copilot* asking it to analyze the Q1 regional sales data. Ask for two things: (1) a list of regions ranked by sales growth, and (2) a brief insight explaining a possible reason (from the data) for the top region’s performance."  
scoring\_rubric\_criteria:

*   "The prompt clearly states it’s about **Q1 regional sales data** and asks for analysis of sales growth by region": 1 point
*   "The prompt specifies the two requested outputs: a **ranked list of regions** and an **insight/explanation** for the top performer": 1 point
*   "The prompt is addressed to **Excel Copilot** (or otherwise makes it clear the user is in Excel context with a dataset)": 1 point
*   "It requests a concise analytical output (e.g., a short list and explanation, not a long essay), appropriate for quick analysis": 1 point

**Item 3 – micro\_task**  
scenario\_text: "An analyst used Word Copilot to perform a complex **financial calculation** that would have been easier in Excel. The result was confusing and had errors."  
question\_text: "In one sentence, explain **which Copilot tool would have been more appropriate** for this task and **why using that tool would improve the outcome**."  
scoring\_rubric\_criteria:

*   "Identifies that **Excel Copilot** (rather than Word) should have been used for complex calculations": 2 points
*   "Explains why (e.g., Excel Copilot has direct access to spreadsheet data and analytical functions, so it can compute and analyze data accurately, whereas Word Copilot is not designed for calculations)": 2 points

***

## SECTION G — Evaluation Item Seeds

### Evaluation: Course 1

**Item 1 – mcq**  
question\_text: "Which component of the CRAF framework tells Copilot **how to structure and present** its response?"  
options: A) Context | B) Role | C) Action | D) Format  
correct\_option: D  
explanation: "In a CRAF prompt, the **Format** element specifies the structure, style, or length of the output (e.g., bullet points, table, summary length). This helps Copilot shape the response in a directly usable way. (Context gives background details, Role sets the perspective, and Action defines the task, but Format deals with the presentation of the output.)"

**Item 2 – mcq**  
question\_text: "An analyst received a 5-paragraph Copilot summary that included a lot of filler text and missed key points. Which prompt refinement is **most likely to improve** the usefulness of the summary?"  
options: A) Adding more acronyms and technical terms to the prompt  
B) Specifying the audience and purpose of the summary in the prompt  
C) Removing formatting instructions to let Copilot write freely  
D) Asking Copilot to be more "creative" in its response  
correct\_option: B  
explanation: "Specifying the audience and purpose (part of providing **Context**) will guide Copilot to focus on relevant points and appropriate tone. By making the prompt more specific about what’s needed (e.g., a summary for a senior executive, focusing on key issues), the AI can produce a more concise and relevant output. The other options either don’t address the core issue or could make the output even less focused."

**Item 3 – mcq**  
question\_text: "In the CRAF framework, why is it beneficial to include a **Role** instruction (for example, "You are a senior financial analyst...") in your prompt?"  
options: A) It ensures the AI will only provide information that has been verified by real analysts  
B) It reduces the length of the AI’s response automatically  
C) It helps the AI adopt the appropriate perspective, tone, and level of detail for the task  
D) It is required for Copilot to access internal data sources like SharePoint  
correct\_option: C  
explanation: "Specifying a Role helps the AI understand the point of view and expertise it should adopt. For instance, telling Copilot to act as a senior financial analyst means the response will likely include more analytical insight and use terminology appropriate for that role, rather than a generic or novice tone. It doesn’t inherently verify data or control length; it’s about perspective."

**Item 4 – performance\_task**  
question\_text: "You have a 25-page **Q4 Operations Performance Report** for an internal project and must brief the **Chief Risk Officer (CRO)** on the most important findings. The CRO cares about any operational risks or performance issues. **Write a full CRAF prompt** to have Copilot generate a one-page summary for the CRO. The prompt should provide all necessary context (including the project name and that this is a Q4 operations report), specify an appropriate role for the AI, clearly state the action to perform, and define a concise format focusing on risks and issues."  
scoring\_rubric:

*   key1: "Provides specific **Context** (project name or topic of the operations report, the quarter Q4, and mention that the audience is the CRO interested in risks/performance issues)"
*   key2: "Includes a **Role** designation guiding the AI to write as a knowledgeable EDC analyst or operations expert reporting to an executive (CRO)"
*   key3: "Defines the **Action** clearly (e.g., "summarize the report’s key findings with emphasis on operational risks and performance issues")"
*   key4: "Gives a **Format** instruction for a one-page executive summary, for example by requesting a set of bullet points or a short paragraph for each key issue, ensuring brevity and clarity"

### Evaluation: Course 2

**Item 1 – mcq**  
question\_text: "Copilot generated a draft analysis that states: *"Department X’s expenses decreased by 5%, saving $2 million."* What is the **best next step** for the analyst before using this statement in a report?"  
options: A) Trust Copilot and use the statement as-is to save time  
B) Double-check the expense figures in the actual financial records for Department X  
C) Run the same prompt in a different AI tool to see if it gives the same statement  
D) Increase the temperature/creativity setting and re-run the prompt for a different answer  
correct\_option: B  
explanation: "The analyst should verify the accuracy of the AI’s statement by checking it against the source data (the department’s financial records). Even if the AI’s answer sounds plausible, confirming the 5% decrease and $2M saving from the actual data is essential. Using another AI or tweaking creativity won’t ensure accuracy; manual verification is needed."

**Item 2 – mcq**  
question\_text: "Which of the following **might indicate that an AI-generated summary contains a hallucination or error**?"  
options: A) It includes a figure or fact that was **not present** in the source data or documents  
B) The writing style is more informal than your usual report draft  
C) The summary is shorter than the original document  
D) It uses bullet points instead of paragraphs  
correct\_option: A  
explanation: "The clearest sign of a possible AI hallucination is when the output includes information or a level of detail that you don’t recall from the source. For example, if Copilot’s summary mentions a statistic or fact not found in your data, it may have fabricated it. Writing style or length may vary depending on instructions, but the inclusion of unprovided data is a red flag that requires verification."

**Item 3 – mcq**  
question\_text: "According to best practices for Verification and Judgment, when is the **appropriate time to review and fact-check Copilot’s output** for an analysis you will use in an internal report?"  
options: A) Only if the output will be shared outside your immediate team  
B) After inserting it into your report, during a final proofread  
C) Immediately after Copilot generates the output, before using it further  
D) It’s not necessary to fact-check if the output came from internal data  
correct\_option: C  
explanation: "You should review and verify Copilot’s output as soon as it’s generated and **before** you incorporate it into any deliverable. Catching errors early prevents them from propagating into reports or communications. Even if the content is for internal use, it should be fact-checked. Waiting until the very end (or not checking at all) is risky, as mistakes may be missed or harder to correct under time pressure."

**Item 4 – performance\_task**  
question\_text: "You used Copilot to draft a paragraph of analysis for the CFO about the **Aurora Initiative’s budget variance**. The AI’s version reads: *"The Aurora Initiative was under budget by $500K, a positive variance of 8%, due to higher-than-expected efficiency gains."* However, the actual figures show it was **over budget by $500K (an 8% overspend)**, not under. The AI also guessed a reason (“efficiency gains”) that is not supported by evidence. **Write the corrected version of this analysis paragraph** that you will deliver to the CFO *after verifying and fixing Copilot’s output*. (Ensure the financial fact is accurate and either provide a supported reason for the overspend or state that it’s under investigation.)"  
scoring\_rubric:

*   key1: "Correctly states the budget variance direction and amount (e.g., that the project was **over budget by $500K** or an 8% overspend, not under budget)"
*   key2: "Omits or replaces the unsupported explanation (the "efficiency gains" claim) with either a fact-based reason (if one is known from the data) or a note that the cause is being investigated"
*   key3: "Maintains a professional and concise tone appropriate for a CFO audience"
*   key4: "Demonstrates evidence of verification (e.g., the content reflects actual data). The sentence should not contain any information that isn’t confirmed by the provided figures or known context"

### Evaluation: Course 3

**Item 1 – mcq**  
question\_text: "All of the following are examples of **Non-Public Information** that an analyst must avoid inputting into Copilot **except**:"  
options: A) An internal slide deck marked "EDC Confidential"  
B) A list of customers with account details exported from CRM  
C) A published news article about one of EDC’s clients  
D) Unreleased quarterly financial results from EDC’s data warehouse  
correct\_option: C  
explanation: "Published news articles are public information, so referring to them in Copilot (or even copying segments) is generally allowed. In contrast, internal confidential decks, raw CRM exports of customer data, or unpublished financial results are all Non-Public Information. According to EDC’s Responsible AI guidelines, such data must not be directly input into external or unmanaged AI systems. Even with internal Copilot, analysts should abstract or omit the sensitive details."

**Item 2 – mcq**  
question\_text: "What is the **recommended approach** if you are unsure whether certain information is considered Non-Public (confidential) or Public before using Copilot?"  
options: A) Treat the information as Non-Public and avoid sharing it with Copilot until confirmed otherwise  
B) Assume it is public if you found it internally at EDC, and use it freely  
C) Ask Copilot if the information is confidential  
D) Break the information into parts and share it in separate prompts so it’s less detectable  
correct\_option: A  
explanation: "When in doubt, it’s best to err on the side of caution: treat the information as Non-Public. That means you should not include it in any Copilot prompts or outputs unless you can verify it’s already public. If you’re unsure about an item, you can often rephrase or abstract it (for example, refer in general terms) or seek guidance. The other options would either violate policy or could still expose sensitive data."

**Item 3 – mcq**  
question\_text: "Why is it **dangerous to paste a client’s unpublished financial statement into an online AI chatbot** (like a free web tool) for analysis?"  
options: A) The AI might not be able to understand financial data  
B) It violates EDC’s policy and could leak sensitive client information outside EDC’s secure environment  
C) The AI would refuse to read financial information  
D) There is no danger, as long as the client doesn’t find out  
correct\_option: B  
explanation: "Client financial statements are Non-Public Information. Pasting them into an unapproved external AI tool would violate EDC’s data security policies and risk exposing confidential data to unauthorized parties or servers outside EDC’s control. This can lead to severe legal and reputational consequences. Whether the AI can interpret the data is not the main issue — the primary concern is protecting sensitive information."

**Item 4 – performance\_task**  
question\_text: "You are analyzing an internal document that contains **sensitive data**: specific client names, loan amounts, and internal risk ratings. You want to ask Copilot to help summarize trends from this data for a report. **Draft a Copilot prompt that adheres to EDC’s data safety rules** by using the SAFE Abstraction Method. (The prompt should convey what you need from the data without revealing any confidential client identifiers or exact figures. For example, you might use aliases like 'Client A' and 'Client B' and general terms like 'high loan exposure' instead of precise amounts.)"  
scoring\_rubric:

*   key1: "Replaces or omits actual client names (uses generic labels like “Client A,” “the largest client,” or similar instead of real names)"
*   key2: "Does not include specific confidential numbers or ratings (e.g., uses relative terms or ranges such as “significant increase” or "top quartile risk rating" rather than exact figures or ratings)"
*   key3: "Provides enough **Context** about the data and what needs to be summarized (so that Copilot can still be effective even with abstracted input, e.g., indicating it’s a portfolio of clients with certain characteristics)"
*   key4: "Clearly states the **Action/Format**, e.g., asking for a summary of trends or comparisons without disclosing sensitive details, and perhaps requesting output in a safe format (like an aggregated overview or de-identified analysis)"

### Evaluation: Course 4

**Item 1 – mcq**  
question\_text: "For which task is it **most appropriate to use Copilot in Excel**, as opposed to Copilot in other applications?"  
options: A) Summarizing key decisions from a lengthy meeting transcript  
B) Drafting a professional response to a client’s email query  
C) Analyzing a large dataset to find trends or outliers  
D) Formatting and grammar-checking a policy document  
correct\_option: C  
explanation: "Excel Copilot is designed to work with structured data. If you need to find trends or outliers in a large dataset (like sales figures or survey results), using Copilot inside Excel is ideal because it has direct access to tables, formulas, and charts. The other tasks are better suited for different Copilot surfaces: meeting transcripts in Teams, emails in Outlook, documents in Word."

**Item 2 – mcq**  
question\_text: "What is a key advantage of chaining multiple Copilot tools in a workflow, rather than using just one tool for everything?"  
options: A) It eliminates the need to verify any outputs, since multiple AIs cross-check each other  
B) It keeps data and context within the most relevant apps, reducing manual copy-paste and errors  
C) It ensures that only public data is used  
D) It guarantees the final output will require no editing  
correct\_option: B  
explanation: "Using Copilot across the M365 suite allows each task to be handled in the optimal environment — for example, analyzing data in Excel where the data lives, and drafting text in Word where you can easily format it. This approach means you don’t have to manually copy-paste information between apps; Copilot can access the content directly (within the secure M365 environment), maintaining context and reducing the chance of errors. You still need to review outputs, and data safety depends on how you use it, but tool chaining can significantly improve efficiency and accuracy."

**Item 3 – mcq**  
question\_text: "Which scenario demonstrates **effective tool fluency** with Copilot?"  
options: A) Using Teams Copilot to generate a project status email, because you discussed the project in a meeting  
B) Copy-pasting a complex table into Word and using Word Copilot to perform calculations on it  
C) Using Excel Copilot to analyze data, then using Word Copilot to draft a report with that analysis, and finally Outlook Copilot to email the findings  
D) Relying on one Copilot tool (e.g., just Word) to perform every task, from data analysis to email writing, for simplicity  
correct\_option: C  
explanation: "Option C shows an analyst employing multiple specialized Copilot tools in sequence — Excel for data analysis, Word for reporting, and Outlook for communication — which is an example of great tool fluency. Options A and B demonstrate a mismatch between the tool and task (Teams Copilot is for meetings, not drafting new emails; Word Copilot isn’t suited for data calculations). Option D misses opportunities to leverage each tool’s strengths."

**Item 4 – performance\_task**  
question\_text: "Your team held a brainstorming meeting about improving the customer onboarding process, and you also have an Excel file with recent onboarding times and a draft action plan in Word. You want to use Copilot to help prepare a summary report for the **Onboarding Improvement Initiative** meeting next week. **Describe an end-to-end workflow (step-by-step)** for using **at least 3 different Copilot tools** to go from these inputs to a final report and an email to stakeholders. (Mention which Copilot you’d use at each step and what you’d do, e.g., "use Teams Copilot to summarize the meeting discussion… then Excel Copilot to analyze data… then Word to draft the report… then Outlook to draft an email...")."  
scoring\_rubric:

*   key1: "Identifies a logical **sequence of at least three Copilot-enabled applications** (e.g., Teams → Excel → Word → Outlook) that would be used in the workflow"
*   key2: "Describes an appropriate action or purpose for each chosen Copilot tool (e.g., Teams Copilot to get meeting notes, Excel Copilot to analyze timing data, Word Copilot to prepare the report, Outlook Copilot to draft the email)"
*   key3: "Demonstrates **verification or review steps** during the workflow (e.g., mentioning a step to check Copilot’s output at critical points before using it in the next tool)"
*   key4: "Demonstrates **data safety considerations** if applicable (e.g., mentioning removal or abstraction of any sensitive info when moving content between tools or sharing the final output)"
