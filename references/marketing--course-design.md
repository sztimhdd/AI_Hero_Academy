## MACHINE-READABLE HEADER

role\_prefix: mk

company\_map:
course\_1: Westport Composites Ltd.
course\_2: BrightWave Electronics Inc.
course\_3: Lakeview Foods Inc.
course\_4: Montane Aerospace Corp.
course\_5: Atlas Marine Equipment Co.
course\_6: NovaTech Innovations Inc.
course\_7: ExportBoost Program

framework\_names:

*   The SAFE Abstraction Method
*   CRAF Framework
*   VERIFY Checklist
*   TAILOR Approach
*   DECIDE Framework
*   Copilot Surface Selector
*   End-to-End AI Workflow

real\_use\_case:
course\_1: The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada).
course\_2: Content Creation & Lifecycle
course\_3: Customer Interaction Recap
course\_4: Prospect Intelligence
course\_5: Streamline production of Quarterly analysis and reporting
course\_6: Corporate Communications (translation, messaging)
course\_7: Exporter Journey Optimization Agent; Automating Prospect Profiling; Customer Interaction Recap; Streamline production of Quarterly analysis and reporting; Corporate Communications (translation, messaging)

***

SECTION A — Role Entry

role\_id: mk  
title: "Marketing & Communications (Business Partner/Manager Roles)"  
description: "Marketing professionals at EDC’s Communications & Marketing group plan and execute multi-channel campaigns to generate leads and promote solutions for Canadian exporters. They create and localize marketing content (emails, social posts, web copy, brochures) in both official languages, coordinate events and lead capture, and support sales teams with customer-focused materials. These roles collaborate closely with Regional segment teams, Sales (RMs/ARMs), Product units, and Corporate Communications to align messaging and ensure brand and compliance standards are met."

***

SECTION B — All 6 Domain Specs

### Domain: responsible\_ai

domain\_id: responsible\_ai  
title: Responsible AI  
description: "Using AI tools in marketing while strictly adhering to EDC’s data and ethics policies. This involves recognizing non-public information (like client contact lists, campaign plans, or unpublished financial figures) and removing or abstracting it before prompting AI. Marketers must ensure AI-generated content doesn’t violate privacy (e.g. CASL consent, Personal Information protection) and remains bias-free and compliant with legal/brand standards."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Does not distinguish between public and confidential data. May paste raw customer lists or unreleased campaign details directly into public AI tools, risking privacy and policy breaches."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Aware of data restrictions but applies them inconsistently. Sometimes shares potentially sensitive info with AI (e.g. uses real client names in prompts) or fails to consider CASL/Privacy implications in AI-assisted tasks."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Consistently applies the public vs. non-public test. Strips out personal identifiers and proprietary details from prompts (e.g. replaces client names with generic descriptors). Uses AI only in allowed platforms and double-checks outputs for any accidental leaks."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Proactively handles edge cases of data sensitivity (e.g. anonymizing a small-market client that might be identifiable by context). Skillfully rewrites prompts to preserve utility (getting useful insight or copy) while protecting all confidential bits. Ensures AI outputs include required disclaimers (like “for internal use”) when needed."  
level\_4\_label: Champion  
level\_4\_descriptor: "Advocates and innovates for data-safe AI usage. Creates team guidelines or templates for sanitizing marketing data before AI use. Identifies new risks (e.g. AI translation of client quotes without consent) and advises colleagues on compliant solutions. Serves as the model of protecting customer and company information while leveraging AI."

### Domain: strategic\_prompting

domain\_id: strategic\_prompting  
title: Strategic Prompting  
description: "Designing effective prompts to get high-quality AI output for marketing tasks — from drafting campaign content to summarizing insights. This means providing context about the audience and product, specifying the role or tone (e.g. “expert marketing copywriter”), clearly defining the task (email, post, analysis) and format. A well-structured prompt yields usable first-draft collateral (emails, blog outlines, social posts) that align with brand voice and require minimal rewrites."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Uses AI without thought to prompt structure. May type trivial commands like “Write something about EDC” and get generic, unusable content."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Attempts prompting but misses key elements (e.g. provides product info but no audience context or format). Outputs often come out off-target or overly generic, requiring significant editing."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Writes prompts with clear context (market, audience, product specifics), a defined AI role, explicit action, and desired format. For example, prompts Copilot to “Draft a 2-paragraph invitation email for a trade show, upbeat tone, include event details.” Usually gets a solid draft that needs only minor tweaks."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Tailors prompts for complex marketing scenarios. Dynamically adds constraints (e.g. ‘do not mention pricing’ or ‘use a friendly but professional tone’) and iterates based on output. Anticipates where the AI might misunderstand (like industry jargon) and includes clarifications in the prompt."  
level\_4\_label: Champion  
level\_4\_descriptor: "Develops prompt templates and best practices for marketing use cases (campaign emails, blog posts, data summaries). Mentors colleagues on being specific and structured in prompts. Pushes the boundaries of AI capabilities by creative prompt design, while still achieving on-brand results consistently."

### Domain: critical\_eval

domain\_id: critical\_eval  
title: Critical Evaluation  
description: "Scrutinizing AI-generated content and analyses for accuracy, compliance, and quality before use. Marketing staff must review every AI draft — checking facts (product details, statistics, client names), correcting any hallucinations or mistranslations, and ensuring the message aligns with brand guidelines and legal requirements (e.g. no unsupported claims, correct disclaimers). It’s about not taking AI output at face value, especially when representing EDC externally."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Assumes AI outputs are correct and publishes or uses them without review. Fails to catch AI-introduced errors (like an incorrect interest rate or a made-up client quote) or problematic language."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Does a basic read-through of AI-generated text but may miss subtle errors or implied promises. Might catch obvious mistakes (like a wrong company name) but not double-check numerical claims or legal fine print."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Routinely verifies AI outputs against trusted sources. If Copilot drafts a blog, cross-references any stats with the source data, ensures translations of slogans are accurate, and that no policy-violating language (e.g. “guarantee”) slipped in. Removes or corrects any content that can’t be verified."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Catches nuanced issues: e.g. an AI-generated customer story that sounds plausible but includes a product usage that never happened. Uses domain knowledge to spot where the AI over-generalized or oversold. Refines prompts to eliminate recurring inaccuracies (for instance, prompting the AI to not invent numbers)."  
level\_4\_label: Champion  
level\_4\_descriptor: "Sets up quality control checklists for AI outputs and shares them with the team. Can explain common failure modes of AI in marketing (such as outdated data, invented quotes) and coaches peers on fact-checking techniques. Helps integrate a “verify step” into standard content and analysis workflows."

### Domain: relationship\_intel

domain\_id: relationship\_intel  
title: Relationship Intelligence  
description: "Enhancing account-based marketing and personalized communications using AI combined with human insight. This means researching prospects and clients with AI (for public info like news, industry trends) and integrating it with internal knowledge (CRM notes, sales feedback) that shouldn’t be shared with AI directly. The goal is to tailor campaigns and messages so they resonate with individual client’s context and history, without ever compromising confidentiality."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Relies only on mass, one-size-fits-all content. Does not use available data about client or segment, nor AI tools, to customize messaging. Might blast the same generic email to all contacts, or share sensitive client info with AI incorrectly."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Uses AI for some basic research on clients (e.g. finds company descriptions or recent news) but stops short of true personalization. May incorporate obvious public facts into outreach, but misses deeper context from internal data or over-shares internal info with AI when trying to personalize."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Effectively combines AI-sourced insights with internal knowledge to craft tailored messages. For example, uses AI to get industry trends for a client’s sector, then manually adds knowledge of the client’s specific situation from CRM (without giving those details to the AI) to shape a customized value proposition."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Anticipates client needs by leveraging patterns (like AI analysis of similar clients) and the history of the account. Produces deeply personalized content — e.g. an email campaign that references a client’s recent milestones or pain points, all drawn from approved data. Never exposes non-public client strategies to AI, and yet still uses them to guide messaging."  
level\_4\_label: Champion  
level\_4\_descriptor: "Leads the way in account-centric AI usage. Builds playbooks for using AI to gather competitive intelligence and client industry news. Mentors colleagues on using AI to craft messages that feel individually tailored. Ensures that the team’s AI usage always respects client confidentiality while improving the relevance of outreach."

### Domain: data\_decision

domain\_id: data\_decision  
title: Data-Driven Decision Making  
description: "Leveraging AI to analyze marketing data (campaign metrics, lead behavior, survey responses) for insights that inform decisions—like refining targeting or channel mix—while adding human judgment. Marketers use Copilot in tools like Excel or Power BI to quickly surface patterns (e.g. which region responded best to a campaign), but they must validate these findings against raw data and contextual knowledge (seasonality, market conditions) before acting on them."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Makes marketing decisions purely on gut or gets overwhelmed by data. Does not use AI analytics tools at all, sticking to manual analysis (which might be shallow or slow), or alternatively trusts one data point without verification."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Has experimented with AI for analysis, e.g. asking Copilot to summarize a campaign report, but doesn’t integrate it into decision-making. Might get interesting charts or trends from AI but is unsure how to interpret them and often defaults back to old habits."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Uses AI routinely to crunch numbers and highlight patterns — for instance, asks Copilot to compare this quarter’s email click-through rates by product line. Verifies AI-highlighted trends with underlying data and considers external factors (e.g. a holiday affecting engagement) before deciding on a course of action."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Combines multiple data sets in AI analysis (website, email, CRM outcomes) to uncover complex insights like lead conversion drivers. Cross-examines AI’s conclusions with team knowledge (e.g. consulting Sales if an AI-flagged “hot lead” truly seems promising). Adjusts strategies confidently, using AI as a support tool, not an oracle."  
level\_4\_label: Champion  
level\_4\_descriptor: "Develops new metrics or dashboards with AI assistance to better measure marketing impact. Shares success stories where AI analysis led to improvement (and how verification was done). Coaches peers on asking the right analysis questions and verifying answers. Ensures the team moves toward data-informed decisions consistently, with AI as an accelerator that doesn’t bypass human insight."

### Domain: augmented\_comm

domain\_id: augmented\_comm  
title: Augmented Communication  
description: "Using AI across Microsoft 365 tools to streamline communication tasks, and knowing which Copilot to use for what job. Marketing and Communications staff often need to turn information from one format into another (meeting notes into an email, data into slides, English content into French). This skill is about choosing the right Copilot surface (Teams for meeting recap, Word for drafting content, Outlook for emails, PowerPoint for decks) and chaining them effectively. It also emphasizes ensuring all external communications are polished, bilingual where required, and have that human polish on AI-generated drafts."  
level\_0\_label: Unaware  
level\_0\_descriptor: "Does not use AI in communication workflows. Writes everything manually or uses each tool in isolation, unaware that Copilot could automate hand-offs (like from a transcript to summary) or help with translation. Struggles with repetitive comm tasks."  
level\_1\_label: Explorer  
level\_1\_descriptor: "Has tried AI in one tool (e.g., uses Outlook’s “Draft with Copilot” for an email) but uses it as a standalone convenience. Still copies and pastes information manually between apps. May not realize, for example, that Teams can summarize meetings or that Word can help format content for publishing."  
level\_2\_label: Practitioner  
level\_2\_descriptor: "Regularly uses at least three Copilot-enabled apps for comms. For example, after an event, uses Teams Copilot for the meeting recap, then Word Copilot to draft a blog from those notes, and Outlook Copilot to tailor follow-up emails. Understands which tool fits each stage (drafting long-form in Word vs quick messages in Outlook) and moves outputs from one to another smoothly."  
level\_3\_label: Proficient  
level\_3\_descriptor: "Designs multi-step workflows with AI assist. For instance, they might use Copilot in PowerPoint to turn a report into slides, then Teams to generate talking points from those slides for a meeting, then Outlook to craft a message sharing the deck. Can troubleshoot when one tool’s output isn’t perfect (e.g., editing the Word draft before using it in an email). Ensures French translations or alternative formats are addressed by the right tool (like using Translator or bilingual Copilot capabilities)."  
level\_4\_label: Champion  
level\_4\_descriptor: "Optimizes and shares end-to-end AI workflows for communications. Maybe creates a guide for the team on how to go from a webinar recording to a customer email plus an internal summary using Copilot. Always up to date on new Copilot features in M365 apps and pilots them (e.g., testing the latest Designer or PowerPoint AI features for marketing visuals). Sets a high bar for quality control in AI-assisted communications – every AI-drafted message that goes out is as polished and compliant as if written from scratch."

***

SECTION C — All 7 Course Specs

### Course 1 — Protect Non-Public Marketing Data in AI

course\_id: mk\_c1\_responsible\_ai  
role\_id: mk  
primary\_domain: responsible\_ai  
sequence\_order: 1  
title: "Protect Non-Public Marketing Data in AI"  
tagline: "Learn how to harness AI tools without leaking leads or confidential marketing info."  
description: "This course teaches marketers how to apply EDC’s Responsible AI guidelines day-to-day. You’ll learn to identify what counts as non-public data in marketing (e.g. customer lists, private campaign results, unreleased materials) and practice transforming it or abstracting it before using generative AI. Through real-world scenarios — like summarizing trade show leads or drafting content from internal data — you’ll master safe prompting techniques so you can still get AI’s help without ever compromising customer privacy, Canada’s Anti-Spam (CASL) compliance, or EDC’s reputation."  
real\_use\_case: "The main objective of this case is to obtain approval to input internal (i.e., non-public) client data into MS Copilot on the Web to increase work efficiency on the Impact team (FinDev Canada)."

### Course 2 — Prompt Better Marketing Drafts Faster

course\_id: mk\_c2\_strategic\_prompting  
role\_id: mk  
primary\_domain: strategic\_prompting  
sequence\_order: 2  
title: "Prompt Better Marketing Drafts Faster"  
tagline: "Turn a blank page into on-brand campaign content by mastering AI prompt strategy."  
description: "Marketers often face tight deadlines to create engaging content. In this course, you’ll adopt the CRAF prompting framework to produce quality first drafts of marketing materials in minutes. Learn how to feed Copilot the right context — from target audience and product value props to desired tone and format — so it can generate emails, social media posts, and blog outlines that hit the mark. We’ll transform vague prompts that yield generic fluff into strategic prompts that deliver usable copy tailored to your needs, reducing writing time while maintaining EDC’s voice."  
real\_use\_case: "Content Creation & Lifecycle"

### Course 3 — Review AI Recaps Before You Act

course\_id: mk\_c3\_critical\_eval  
role\_id: mk  
primary\_domain: critical\_eval  
sequence\_order: 3  
title: "Review AI Recaps Before You Act"  
tagline: "Never trust an AI summary blindly — learn to verify facts and filter outputs."  
description: "Marketing moves fast, but AI-generated recaps and content must be handled with care. This course builds your critical eye for evaluating AI outputs. You’ll practice with scenarios like getting a summary of a 10-page product brief or a webinar transcript and catching subtle errors or overstatements before they spread. We’ll cover the VERIFY checklist to double-check names, numbers, claims, translations, and tone. By course end, you’ll be able to confidently use AI to lighten your workload while ensuring any output that goes public (or to the team) is 100% accurate and compliant."  
real\_use\_case: "Customer Interaction Recap"

### Course 4 — Build Stronger Outreach With Prospect Insight

course\_id: mk\_c4\_relationship\_intel  
role\_id: mk  
primary\_domain: relationship\_intel  
sequence\_order: 4  
title: "Build Stronger Outreach With Prospect Insight"  
tagline: "Combine AI research with your inside knowledge to personalize marketing like never before."  
description: "In account-based marketing, one-size-fits-all approaches fall flat. This course shows how to use AI for quick insight into industries and companies, then fuse those insights with your internal intel about customers. You’ll use the TAILOR approach to maintain confidentiality (never leaking non-public facts) while still crafting highly personalized emails and social posts. Scenarios include prepping for a campaign targeting a key account — using AI to gather recent news and sector trends, adding your sales team’s private insights separately, and shaping messaging that speaks directly to the client’s situation."  
real\_use\_case: "Prospect Intelligence"

### Course 5 — Turn Campaign Data Into Better Decisions

course\_id: mk\_c5\_data\_decision  
role\_id: mk  
primary\_domain: data\_decision  
sequence\_order: 5  
title: "Turn Campaign Data Into Better Decisions"  
tagline: "Unlock hidden insights in marketing data using AI — and learn when to trust them."  
description: "Modern marketers rely on data, from email open rates to lead conversion metrics. In this course, you’ll learn how to use Copilot in tools like Excel and Power BI to analyze performance data quickly, and the DECIDE framework to validate AI-driven insights. We’ll practice on scenarios such as a quarterly marketing review: asking Copilot for trends and key takeaways, then verifying them against source data and business context. By the end, you’ll be able to leverage AI to make informed decisions about budget allocations, target segments, and strategy adjustments — with confidence that the insights are sound."  
real\_use\_case: "Streamline production of Quarterly analysis and reporting"

### Course 6 — Draft Clear Bilingual Marketing Communications

course\_id: mk\_c6\_augmented\_comm  
role\_id: mk  
primary\_domain: augmented\_comm  
sequence\_order: 6  
title: "Draft Clear Bilingual Marketing Communications"  
tagline: "Use AI across Office apps to draft, translate, and polish communications that resonate."  
description: "Marketing and Communications roles juggle internal memos, press releases, client emails, and more — often in both English and French. This course shows how to use the Copilot Surface Selector to streamline creating and repurposing content across Outlook, Word, Teams, and PowerPoint. You’ll practice multi-step workflows: for example, summarizing a Teams meeting into key points, expanding those in Word for an intranet article, and having Copilot help translate and format that content for a French version. We’ll also tackle an urgent external comms scenario, using AI to draft a message and then refining it to ensure it’s on-tone, accurate, and fully bilingual."  
real\_use\_case: "Corporate Communications (translation, messaging)"

### Course 7 — Run an AI-Assisted Marketing Workflow End-to-End

course\_id: mk\_c7\_capstone  
role\_id: mk  
primary\_domain: (integrated)  
sequence\_order: 7  
title: "Run an AI-Assisted Marketing Workflow End-to-End"  
tagline: "Integrate all six AI skill areas as you plan and execute a full campaign with AI support."  
description: "The capstone brings together everything you’ve learned in a realistic project. You’ll step into the shoes of a marketing lead running the **ExportBoost Program**, an initiative to improve the customer journey for exporters. Over this course, you will use AI to assist at each stage: safely analyzing customer data (Responsible AI), drafting content and strategic plans (Strategic Prompting), generating and verifying summaries of client interactions (Critical Evaluation), researching and tailoring outreach to key prospects (Relationship Intelligence), analyzing campaign performance (Data-Driven Decisions), and creating bilingual communications for stakeholders (Augmented Communication). By completing this project, you’ll demonstrate your ability to orchestrate AI tools throughout a marketing campaign while upholding EDC’s standards."  
real\_use\_case: "Exporter Journey Optimization Agent; Automating Prospect Profiling; Customer Interaction Recap; Streamline production of Quarterly analysis and reporting; Corporate Communications (translation, messaging)"

***

## SECTION D — All 7 Scenario Seeds

### Course 1 Scenario

scenario\_text: "You just returned from the Westport Composites trade show, where you collected a spreadsheet of 200 new contact leads, including names, companies, emails, job titles, and brief notes from conversations. You want to use Copilot to draft a follow-up marketing email to these leads, highlighting how EDC can help their business. However, you must ensure compliance with privacy regulations and EDC’s AI usage policies."  
task\_1: "Before using any AI tool, list at least three specific data points in the lead spreadsheet that you should NOT directly include in any prompt or upload (i.e., what counts as non-public personal information or sensitive data in this context?)."  
task\_2: "Now, describe how you could use AI to help draft an email without exposing those non-public details. What approach or strategy would you use when writing the prompt or using Copilot to get a useful draft safely?"  
task\_3: "Write a sample prompt you could feed to Copilot (in Outlook or Word) to generate a first draft of a follow-up email to these leads. Ensure the prompt is free of personal data yet provides enough context for the AI to produce a relevant result."  
task\_4: "After getting an AI-generated draft, you notice it accidentally included a placeholder like `<CompanyName>`. It might be tempting to just do a quick find-replace with the real company names. What should you do instead to finalize and personalize the emails for each recipient while staying compliant? Briefly explain."  
coach\_system\_prompt: "You are an AI skills coach for EDC’s Marketing team focusing on responsible AI use. The learner is figuring out how to use AI on a contact list without breaking data rules. Guide them with questions to identify sensitive data and abstract it. Do not give them the answer outright. If they propose including real names or emails in a prompt, remind them of privacy policy. If they are stuck on how to phrase a safe prompt, encourage them to think about describing the list in general terms (e.g., industry, roles) instead of providing raw data."

### Course 2 Scenario

scenario\_text: "You are a Marketing Manager preparing to announce a new partnership between EDC and a client, BrightWave Electronics Inc., a Toronto-based tech manufacturer. You need to produce a short blog post for EDC’s website about the partnership and a series of social media posts to promote it. You have a press release with all the details, but it’s written in formal language and is 5 pages long."  
task\_1: "Using the CRAF framework (Context, Role, Action, Format), write an initial prompt to have Copilot draft a 3-paragraph blog post about the EDC–BrightWave partnership. Be sure to include key context like who BrightWave is and what the partnership entails."  
task\_2: "The first AI draft of the blog post comes back very generic and reads like a press release, with too much jargon. What changes can you make to your prompt to get a more engaging, customer-friendly tone and a focus on how this partnership benefits clients? Revise your prompt accordingly."  
task\_3: "Now you want to create a concise LinkedIn post about the BrightWave partnership, drawing from the blog content. Write a new prompt to instruct the AI to generate a punchy, 2-3 sentence LinkedIn post that will grab attention. (Assume the AI has access to the blog draft for context.)"  
task\_4: "The AI’s first attempt at the social post is over-the-top and uses phrases like “revolutionary partnership” and excessive exclamation points. What instructions or edits would you apply to your prompt or the AI’s output to ensure the tone remains professional and on-brand for EDC?"  
coach\_system\_prompt: "You are an AI skills coach for marketing content creation. The learner is practicing strategic prompting with a partnership announcement. Don’t provide the final prompts, but ask questions to help them remember to include all CRAF elements (especially context about the partner and audience benefits, and format for each channel). If the output is too formal or too hype, ask how they can adjust tone or add instructions in the prompt. Ensure they consider different formats (blog vs social) and how to prompt for each."

### Course 3 Scenario

scenario\_text: "A product manager has sent you a dense 10-page technical brief about a new financing solution, full of jargon and data. They want you to turn it into a one-page blog post for small business owners by the end of the day. You decide to use Copilot in Word to help create a draft."  
task\_1: "Write a prompt asking Copilot to summarize the 10-page technical brief into a one-page blog post aimed at a general small business audience. Include instructions to simplify complex terms."  
task\_2: "Copilot produces a draft, but you notice it included a statistic from the brief: ‘EDC’s new product reduces costs by 15%.’ You’re not sure this number is accurate. What steps would you take to verify this statistic before using it, and what evidence or sources would you check?"  
task\_3: "Upon reviewing the draft, you find the AI added a customer quote that wasn’t in the original brief: “This solution is a game changer for my business,” said a fictional user. Explain why including this quote is problematic and how you would address it."  
task\_4: "The technical brief had some details that are sensitive (e.g., an internal code name for the product, and an example client deal that isn’t public). The AI included those in the draft blog. Describe how you would modify the draft to remove or replace such sensitive details, and how you might adjust your prompting next time to prevent this."  
coach\_system\_prompt: "You are an AI skills coach helping a Marketing learner practice critical evaluation of AI outputs. The learner has an AI-generated draft of a blog post based on a technical brief. Guide them to question the accuracy and appropriateness of each part of the output. If they seem to accept the AI’s content without question, ask which facts they should check and what might be missing (like disclaimers or a French version). If they focus on major errors, remind them to also watch for subtle issues (like tone or implied guarantees). Encourage them to explain how they’d correct any errors rather than just deleting content."

### Course 4 Scenario

scenario\_text: "Your team is launching an account-based marketing campaign targeting a key prospect: Montane Aerospace Corp., a large aviation parts exporter. You have internal notes from a recent RM meeting: Montane plans to expand into Asian markets next year (confidential). You also know from public news that Montane just opened a new office in Singapore. You want to craft a highly personalized introductory email to Montane’s CFO about how EDC can support their growth."  
task\_1: "First, use an AI tool to gather public information on Montane Aerospace and its industry. What kind of details would you ask the AI to find, and how would you ensure they come from public sources?"  
task\_2: "Now draft an AI prompt for an email to Montane’s CFO. In your prompt, provide relevant public context (e.g., mention their Singapore expansion) and ask the AI to write a brief, tailored email highlighting how EDC can help with their Asian market growth. **Do not** include any confidential info from the RM’s notes in your prompt."  
task\_3: "The AI’s email draft is fluent but something feels off — it mentions a specific dollar figure for Montane’s expansion plan that actually came from an internal source, not any public data you provided. How do you think this happened, and what should you do with that sentence in the draft?"  
task\_4: "You want the final email to feel personal and authentic. After removing or fixing any issues in the AI draft, what additional human touch would you add before sending, to maximize the email’s impact? (Consider tone, relationship context, next steps, etc.)"  
coach\_system\_prompt: "You are an AI skills coach for a marketing professional focusing on relationship intelligence. The learner is using AI to help personalize a communication to a key account. Steer them with questions. Make sure they think about what public info is useful and how to prompt for it. If they include the confidential expansion plan in the AI prompt, warn them about that and ask how they can hint at it without disclosing it. For the AI’s draft, prompt them to double-check any details that weren’t explicitly in the prompt. Encourage them to add an extra personal touch that AI wouldn’t know (e.g., referencing their own experiences or a recent conversation) while keeping it professional."

### Course 5 Scenario

scenario\_text: "It’s the end of Q3, and you need to report on marketing performance and adjust next quarter’s plan. You have data: emails sent, open rates per region, leads generated per campaign, and conversion-to-sales figures. You decide to use Copilot in Excel to summarize trends and then verify them with the team’s knowledge."  
task\_1: "What is one specific question you could ask Copilot (or an analysis prompt you could write) to start extracting insights from the Q3 marketing data? (For example, identifying the best-performing region or campaign.) Write the question you’d ask the AI."  
task\_2: "Copilot returns an insight: it says “Lead conversion rates jumped 30% in Atlantic Canada in Q3, more than any other region.” Before you include this in your report and act on it, what would you do to ensure this insight is accurate and meaningful? List two verification steps or considerations."  
task\_3: "Suppose on further investigation you find that the conversion spike in Atlantic Canada was largely due to one big deal closing, not an overall trend. How would you incorporate this context or nuance into how you present the insight in your report or plan for next quarter?"  
task\_4: "You want to use the AI findings to recommend an action for next quarter’s marketing strategy (for example, shifting more budget to a certain channel or region). Write one data-driven recommendation you might make, and explain how the evidence supports it."  
coach\_system\_prompt: "You are an AI skills coach guiding a marketer on data-driven decisions. The learner is using AI to analyze campaign data. Prompt them to be specific in what they ask the AI (instead of a vague “tell me something interesting”). When they get an insight, ask them how they will verify it – e.g., by checking raw numbers or discussing with sales. If they seem to accept the AI’s conclusion too quickly, challenge them: Could there be external factors or anomalies influencing the data? Encourage them to refine the insight with context (like a one-time event or small sample size) and turn it into a thoughtful recommendation."

### Course 6 Scenario

scenario\_text: "A sudden news article reports a potential economic downturn in an industry where many of EDC’s clients operate. Leadership asks you, as a Communications Advisor, to quickly draft an email to customers addressing this news and reassuring them of EDC’s support. The email must go out in English and French by end of day. You plan to use Copilot and other M365 tools to accelerate this under tight time constraints."  
task\_1: "You start by gathering the key points. Describe how you could use a Copilot tool to summarize the news article’s main points and the concerns clients might have, to inform your email. Which tool or approach would you use and what would you ask it for?"  
task\_2: "Now, write a prompt in Word (with Copilot) to draft the initial English version of the client email. Include context (the situation and who the audience is), the role/tone (reassuring, professional), and what action/outcome you want from the email."  
task\_3: "The draft email from Copilot sounds a bit generic and doesn’t mention any specific details of the news. What additional information or instructions will you add to the prompt (or the draft) to ensure the final email directly addresses the situation from the news article and EDC’s relevant services?"  
task\_4: "After refining the English email, you need a French version. How will you produce the French draft using AI, and what steps will you take to ensure the French email is as accurate and effective as the English one? (Consider both the tool and the review process.)"  
coach\_system\_prompt: "You are an AI skills coach for communications advisors. The learner is under time pressure to use AI across tools to create an English and French client email about a crisis. Guide them with questions. Ensure they think about which Copilot or feature to use at each step (e.g., Summarize in Teams or Bing for news; Draft in Word; Translate with Copilot). If their English draft lacks specifics, ask what key details from the news or EDC’s support offerings they could include. If they skip quality checks on the French version, remind them to review and possibly involve a bilingual colleague. Don’t give them the exact text, but lead them to cover all steps."

### Course 7 Scenario

scenario\_text: "You are the lead for the **ExportBoost Program**, an initiative to improve end-to-end experience for a set of growing exporter clients. This capstone scenario spans an entire mini-project:

*   **Planning Phase:** You have data on 50 target companies (size, sector, recent interactions) and want to identify which to prioritize.
*   **Execution Phase:** You’ll create personalized outreach and content for these companies, possibly including events or webinars.
*   **Follow-up Phase:** After executing a campaign, you’ll analyze results and report to leadership.
    Throughout, you’ll use AI tools to assist, while applying all your Responsible AI, Prompting, Evaluation, Relationship, Data and Communication skills."  
    task\_1: "Planning: You have the list of 50 target companies and some internal notes on each (e.g. one line about their needs). How would you use AI to help profile or prioritize these companies without exposing the internal notes? Describe the steps you take to safely leverage AI in this initial stage."  
    task\_2: "Execution: Now pick one high-priority company from the list (imagine one named **GlobeTech Solutions** in the tech sector). Outline how you would use AI to create a tailored outreach campaign for this company. (For example, using AI to draft content like an email or LinkedIn post, plus maybe an event invitation, while incorporating public info about GlobeTech and internal insights indirectly.)"  
    task\_3: "Follow-up Analysis: After the campaign, assume Copilot helped compile performance data: email open rates, responses from GlobeTech and others, etc., and produced a summary. What would you do to critically evaluate that AI-generated summary and extract reliable insights for your report? Provide two specific checks or questions you’d apply."  
    task\_4: "Reporting: Finally, you need to present results and next steps to the VP of Marketing. Describe how you would prepare this using AI tools (think of combining narrative and visuals). For example, what Copilot features might you use to create the slide deck or written report, and how would you ensure the final presentation is polished and bilingual?"  
    coach\_system\_prompt: "You are an AI skills coach guiding a learner through an end-to-end marketing scenario. Ensure they consider all six domains. In Planning, prompt them to use AI for analysis but with anonymized data. In Execution, look for strategic prompting and relationship personalization (without sharing secrets). In Follow-up, push them to verify AI’s analysis and consider data context. In Reporting, remind them to use the appropriate tools (maybe PowerPoint Copilot for slides, etc.) and to review the outputs (especially for bilingual needs). Ask probing questions if they overlook a domain (e.g., ‘How will you make sure no private data goes into your AI prompt?’ or ‘How will you double-check the insights Copilot gives you?’). The goal is to have them articulate a coherent plan utilizing AI at each step responsibly."

***

## SECTION E — All 7 Reading Concept Specs

### Course 1 Reading

framework\_name: "The SAFE Abstraction Method"  
concept\_text: "When working with AI, especially for marketing data, use the SAFE method to safeguard sensitive information without losing utility:

*   **S (Sensitive Info Identification):** First, **spot** any sensitive or non-public details in your materials. This includes client identities (names, emails), personal data, unreleased figures, or confidential strategies.
*   **A (Abstract or Anonymize):** **Remove or replace** those details in your prompt. For example, instead of using a real customer name, say “Client A (a mid-sized Ontario electronics manufacturer).” Summarize specifics (like “their revenue grew by X%” could become “double-digit revenue growth”) so the AI gets the picture without exact confidential numbers.
*   **F (Feed the Prompt Safely):** Now that it’s sanitized, **provide the prompt** to the AI tool. Include enough context — industry, role, needs — but only using public or anonymized info. This ensures you still get a useful output (like an email draft tailored to a type of client) without any privacy risk.
*   **E (Examine Output for Leaks):** Finally, **examine the AI’s output** carefully to ensure it didn’t reintroduce any hidden sensitive info or make up data. If it did, edit those out manually before using or sharing the content.

By following SAFE, you maintain compliance with privacy laws and EDC’s policies while still benefiting from AI speed. It’s a way to get specific, relevant results from AI without ever exposing data that must remain secure."  
good\_example: "Prompt (with SAFE applied): *“Draft a follow-up email for new leads I met at a trade show for manufacturers. Context: I spoke with over 100 Canadian manufacturing companies (avg \~$50M revenue) about EDC’s financing solutions for export growth. Role: You are a marketing copywriter. Action: Write a 3-paragraph professional email referencing the trade show conversation and inviting them to a webinar. Format: Email, warm tone, include a call-to-action to schedule a meeting.”*  \n**Why it works:** No personal details were included — company count and average size are abstracted, and the prompt focuses on general themes from the event (export growth financing) rather than specific confidential details. The AI has enough context to produce a tailored email, but nothing private is exposed."  
anti\_pattern: "Prompt (unsafe): *“Draft an email to follow up with leads from the Big Manufacturing Expo. The Excel file ‘ExpoLeads.xlsx’ has the list of 200 contacts with their names, emails, company financials, and what they asked about.”*  \n**Why it fails:** It attempts to feed real lead data directly (even the file name suggests confidential content). This violates policy by potentially uploading non-public personal and company data. Also, the prompt is vague about the email’s content — it doesn’t say what to include from those conversations. It would be both unsafe and likely to produce a meaningless email."  
takeaway: "**Always filter and abstract data before using AI.** By being SAFE — identifying sensitive data and removing or generalizing it — you can still get valuable AI assistance (like drafting content or analyzing info) without ever putting EDC or customer information at risk."

### Course 2 Reading

framework\_name: "CRAF Framework"  
concept\_text: "Great marketing outputs from AI start with great prompts. The **CRAF framework** ensures you give Copilot everything it needs to generate useful content, whether it’s an email, ad copy, or blog outline. CRAF stands for:

*   **C – Context:** Set the scene. Who is the audience or customer? What product, service, or campaign is this about? Provide any key details: e.g. “a new venture loan product for tech startups in Ontario, launching next month.”
*   **R – Role:** Assign the AI a role or persona to guide tone and knowledge. “You are a senior marketing copywriter at EDC,” will make the AI’s language and perspective more suitable than a generic internet voice.
*   **A – Action:** Be clear about what you want. Do you need a list of social post ideas? A 200-word email draft? “Draft an introductory email highlighting 3 benefits…” gives a specific goal.
*   **F – Format:** Tell the AI how to structure the output. Maybe “3 bullet points,” “two short paragraphs with a subject line,” or “in newsletter format with a headline.” This prevents wall-of-text or wrong style.

Include all four CRAF elements and your prompt will yield content that’s on-point. Missing one? You’ll likely get something too generic, overly verbose, or misaligned with what you need."  
good\_example: "Prompt: *“Context: EDC just partnered with BrightWave Electronics, a Toronto tech manufacturer, to help them expand globally. Audience: general business readers on our website. Role: Marketing copywriter at EDC. Action: Write a 3-paragraph news-style blog post announcing the partnership, highlighting how it benefits Canadian exporters (e.g., more financing options for tech companies). Format: Start with a headline, then an intro paragraph, a quote from EDC or BrightWave, and a conclusion with a call-to-action to learn more.”*  \n**Why it works:** Every CRAF element is there. The AI knows the who/what (BrightWave partnership, tech sector), the voice (EDC marketing copywriter, so professional and on-brand), the task (a specific announcement blog with a quote and CTA), and the format (headline + structured paragraphs). The output will be much closer to final draft quality."  
anti\_pattern: "Prompt: *“Write something about EDC’s new partnership.”*  \n**Why it fails:** It lacks Context (with which company? for what audience?), no Role (so AI might narrate in a weird tone or assume wrong perspective), vague Action (write something… what?), and no Format (could be a long essay or a single sentence—who knows). The result would likely be generic and not immediately usable, costing the marketer more time to rework completely."  
takeaway: "**Structure your prompts with CRAF to save time.** A well-crafted prompt is like a good creative brief to the AI — it yields output that is targeted, formatted, and closer to what you envisioned, meaning you can spend time polishing content instead of rewriting it from scratch."

### Course 3 Reading

framework\_name: "VERIFY Checklist"  
concept\_text: "AI can speed up content creation and summarization, but you must **VERIFY** everything it produces before trusting it. Use the VERIFY checklist as your guide:

*   **V – Verify Facts:** Check any numbers, dates, or facts against reliable sources. If Copilot says “exports grew 15%,” confirm that with your data or an official report.
*   **E – Evaluate Tone & Brand:** Make sure the output’s tone matches EDC’s voice (helpful, professional) and that it doesn’t include insensitive or off-brand phrasing. Ensure bilingual content aspects are handled (e.g., no English taglines left untranslated).
*   **R – Remove/Revise Inaccuracies:** If something seems off, it probably is. Delete or fix any statement you can’t support. For instance, if the AI invented a client quote or misattributed a statistic, correct it or cut it.
*   **I – Identify Missing Elements:** AI might omit important details (maybe it left out a disclaimer or a key benefit). Add anything crucial that’s absent, especially compliance elements like CASL unsubscribe lines or the French translation segment.
*   **F – Flag Confidential Info:** Ensure no internal-only information or personal data accidentally slipped into the output. The AI might recall a detail from context that shouldn’t be public — catch and remove those.
*   **Y – Yield Final Judgment:** Don’t just autopilot-send content because “AI wrote it.” The human (you) is the final gatekeeper. Only approve the content once you’re satisfied every part is correct and appropriate.

Following VERIFY means an AI draft is only a starting point — you turn it into a truly ready piece by fact-checking and fine-tuning all aspects."  
good\_example: "*AI Output (Event recap snippet):* “**EDC’s webinar last week was attended by over 500 companies. All participants found it extremely valuable, and EDC promised to solve all their export challenges.**”  \nUsing VERIFY:\n- **V (Verify Facts):** Check registration data — actually 350 companies attended, not 500+, so correct that number.\n- **E (Evaluate Tone):** “solve all their export challenges” over-promises; adjust tone to be realistic and aligned with EDC’s advisory role.\n- **R (Remove Inaccuracies):** “All participants found it extremely valuable” — we only have data from a subset via a survey, so soften this claim or cite the survey result.\n- **I (Identify Missing):** Add a note that the webinar recording is available in both English and French (important for audiences in both languages).\n- **F (Flag Confidential):** Ensure no internal project names or non-public insights (none here, but always check).\n- **Y (Yield Judgment):** After these edits, the revised recap is accurate and on-message, ready to publish."  
anti\_pattern: "*Marketing Email draft from AI:* “**Dear customer, Thanks for meeting our team. EDC will guarantee your success in expanding to Asia. – Sent from my iPhone**”  \nIssues:\n- No factual verification (does the solution guarantee success? No — that’s an over-claim and likely false).\n- Tone and closing are off-brand (“Sent from my iPhone” shouldn’t appear in a professional email; it probably crept in from training data!).\n- Missing key info (no mention of what solution or next steps) and no French version.\nIf someone just trusts this and hits send, it could mislead the client and violate EDC’s communications standards. Skipping verification here would be a serious mistake."  
takeaway: "**Never assume AI is 100% right.** Always VERIFY. You’re the editor-in-chief of AI content: fact-check numbers and claims, enforce the right tone and brand language, fill any gaps, and ensure no secrets or privacy breaches. Only once you’ve done that should AI-generated material see the light of day."

### Course 4 Reading

framework\_name: "TAILOR Approach"  
concept\_text: "Personalization is key in account-based marketing, and the **TAILOR approach** helps combine AI capabilities with your human insight — all while keeping data safe. Here’s how to TAILOR your strategy for each prospect:

*   **T – Think First (Internal Context):** Before turning to AI, recall what you already know about the client (from CRM notes, conversations, their past behavior). What are their goals or pain points? Also decide what sensitive info you must NOT share with AI.
*   **A – Ask AI for Public Intel:** Use AI to research **public** information about the client or their industry. For example, prompt it for recent news on the company, industry trends, or general challenges companies like them face. This gives you fresh, external angles to complement your knowledge.
*   **I – Integrate Insights (Privately):** Combine the AI’s findings with your internal insights **in your own mind or offline**. Identify overlap: Did the AI mention a trend that aligns with the client’s stated expansion plan? Note how you can reference the trend without revealing anything confidential.
*   **L – Language and Tone Personalization:** Draft your message using a tone that fits the relationship. You can even prompt AI to help, e.g., “Write an email congratulating Client on their new plant opening (public news) and subtly connecting it to EDC solutions,” but you’ll add the personal touches (like referencing a previous meeting or mutual contact) yourself in the editing stage.
*   **O – Observe Privacy and Compliance:** Before sending or publishing, double-check that nothing in the output accidentally exposes internal data. Also ensure any personalization doesn’t inadvertently promise something inappropriate (e.g., referencing a confidential financing deal).
*   **R – Refine and Review:** Finally, polish the content. Does it truly read like one-to-one communication? Edit in a warm greeting, perhaps a detail only a human would know (“I enjoyed our chat about your hometown hockey team”). AI can draft, but the human touch makes it genuine.

By using TAILOR, you leverage AI to get smart background content and save time, but *you* are still orchestrating the message to be both highly relevant and perfectly appropriate for that specific client."  
good\_example: "Scenario: Montane Aerospace Corp is expanding (public news) and you know from internal sources they had issues with supply chain financing.\n- You **Think First** about Montane: medium-size, long-time client, conservative culture. You decide not to mention their internal challenges directly.\n- You **Ask AI** for industry insights: e.g., “summarize recent trends in aerospace manufacturing in Asia-Pacific.” It returns info on supply chain risks due to tariffs.\n- You **Integrate Insights**: The tariff issue ties to Montane’s confidential concern. You plan to mention it generally: “Many aerospace firms face supply chain finance challenges with recent tariffs…” – a nod to their issue without saying it’s theirs.\n- You set a professional, optimistic **Language** and ask Copilot to draft an email congratulating their expansion and offering a discussion on mitigating supply chain risks.\n- You verify that nothing in the draft violates privacy (**Observe Privacy**), then **Refine** it with a personal line about your last meeting.\nThe final email references relevant industry news and common challenges, aligning with what you *know* Montane cares about, but doesn’t spill any secrets. It feels tailored and helpful."  
anti\_pattern: "An EDC marketer wants to impress a prospect and feeds the AI with internal CRM notes: *“Use the following: ‘Montane’s CFO told us they’re struggling with cash flow due to a secret new project.’ Write a LinkedIn message offering help.”*  \nThis results in a draft message that says, *“I know you’re struggling with cash flow for your upcoming project...”* – immediately raising red flags. The marketer has revealed sensitive info via the AI prompt and the message itself is far too personal (and creepy from the client perspective). Failing to TAILOR properly here breaches trust and policy in one go."  
takeaway: "**Personalization must be smart and safe.** The TAILOR approach lets you use AI to gather and shape great personalized content *without* ever betraying confidences. AI gives you broad insight and saves time on drafting, but your human judgment ensures the final communication speaks directly to the client’s known needs in a respectful, compliant way."

### Course 5 Reading

framework\_name: "DECIDE Framework"  
concept\_text: "To use AI insights for marketing decisions, follow the **DECIDE** framework — it ensures you harness data analytics responsibly and effectively:

*   **D – Define the Question:** Start by clearly defining what you need to know. Instead of asking AI generally about “campaign performance,” ask, for example, “Which customer segment had the highest email open rate in Q3?” A focused question yields a useful answer.
*   **E – Engage AI for Analysis:** Use Copilot or BI tools to crunch numbers and draft interpretations. For instance, ask Excel Copilot “Compare Q2 vs Q3 lead-to-opportunity conversion rates and identify any significant changes.” The AI will do the heavy lifting in seconds.
*   **C – Contextualize the Findings:** Don’t take the analysis at face value. Examine the context behind an AI-flagged trend. If Copilot says “Webinar attendance doubled,” recall context (was there a major event or an outlier?). Determine if it’s a genuine trend or an anomaly.
*   **I – Interpret with Insight:** Bring in human/business insight. Why might a metric be up or down? AI can connect dots to an extent, but you, as a marketer, know the on-the-ground reality (like a holiday or technical issue that impacted a campaign). Incorporate that into the interpretation.
*   **D – Decide and Act (with Validation):** Based on combined AI analysis and your insight, make a decision or recommendation (e.g. shift budget to a channel that AI showed had best ROI). But validate one more time — ensure the data supports it and consider running it by a colleague or a second data source if high-stakes.
*   **E – Evaluate Outcomes:** After acting, later evaluate if the decision was correct (close the loop). This isn’t directly an AI step, but it’s critical to building trust in using AI for decisions. If AI suggested something and you tried it, check the results and feed that learning into future AI interactions.

Using DECIDE means AI is a powerful assistant, not the decision-maker. You get speed and analytical power, but you frame the questions and double-check the answers so your choices are truly data-driven and sensible."  
good\_example: "Imagine Q4 ended and sales asks, “Where should we focus marketing next year?”\n- **D:** You Define a question for AI: e.g., “Which marketing channel generated the most qualified leads for us in 2025?”\n- **E:** You Engage AI (Power BI Copilot) to analyze lead data by channel.\nIt reports: “Webinars produced 40% of qualified leads, the highest of all channels, and their conversion rate was 15% versus 10% average.”\n- **C:** Contextualize: You recall that in 2025 we ran an unusually high number of webinars (so naturally they yielded more leads). Also, one webinar had a celebrity guest which spiked attendance – an outlier influencing the data.\n- **I:** Interpret with insight: The consistently strong conversion rate suggests webinars are indeed effective beyond the outlier. Perhaps customers prefer interactive content.\n- **D:** Decide and Act: You propose allocating more budget to webinars next year, but Validate by checking early Q1 data or running a pilot first rather than fully committing all resources.\n- **E:** Later, Evaluate: In Q2, you review if webinars continued to perform. This continuous learning refines how you use AI analyses going forward."  
anti\_pattern: "A marketer sees Copilot in Excel output: “Our social media ads were 50% less effective last month!” and immediately cuts the social ad budget by half. They didn’t ask what ‘effective’ meant, nor notice that last month there were site issues causing all channels to drop. They took AI’s flashy statistic without context or further digging. The result? Overreaction and misallocation of resources. The error here is failing to DECIDE properly — no careful question (just letting AI define ‘effective’), no context or insight added, just knee-jerk action. In short, treating AI’s output as gospel can lead to bad decisions."  
takeaway: "**Use AI as advisor, not dictator.** The DECIDE framework reminds you to ask clear questions and then validate AI’s answers with context and human insight. By doing so, your marketing decisions will be data-informed but also reality-checked — the best of both worlds."

### Course 6 Reading

framework\_name: "Copilot Surface Selector"  
concept\_text: "To maximize productivity, choose the right Copilot tool for each communication task — the **Copilot Surface Selector** helps you decide. Think in terms of **Where your content is coming from, and What you need to produce:**

*   **Emails → Use Outlook Copilot:** When you need to draft or reply to emails (especially one-to-one communications), Outlook’s Copilot is tuned for that. It knows email context like threads and can quickly generate professional responses or outreach emails.
*   **Documents (Press releases, Articles) → Use Word Copilot:** For long-form content or anything requiring rich formatting and iteration (press releases, internal briefs, blog articles), Word’s Copilot provides a better canvas. You can prompt it to draft text, then easily edit, comment, and refine right in Word.
*   **Meetings & Transcripts → Use Teams Copilot (Recap):** If you have a recorded meeting or call, Teams Copilot can summarize key discussion points, action items, and even sentiments. Use this to get raw material from a webinar or internal meeting before you polish it for wider distribution.
*   **Data to Insights or Visuals → Use Excel/Power BI and PowerPoint Copilot:** For any task where numbers are involved (e.g., compiling engagement metrics into a visual report), start with Excel’s Copilot to analyze or clean data. Then, use PowerPoint Copilot to create slides or graphics based on those insights for an executive update.
*   **Translations or Bilingual Content → Use the Multilingual Abilities in Copilot:** For instance, Word’s Copilot can help translate a document draft (especially if you prompt it section by section for accuracy). Always have a human bilingual review, but Copilot can do the heavy lifting quickly.

Often, you’ll **chain** these surfaces: e.g., Teams to summarize a meeting → Word to expand into an article → Outlook to disseminate highlights via email. By picking the right starting point, you minimize friction (since Copilot already has the context it needs).

Remember, each Copilot surface has strengths: one might remember the meeting you just had; another works with structured text better. The Surface Selector approach ensures you’re using the best tool for each job rather than forcing one AI tool to do everything."  
good\_example: "You held a client webinar and now need to follow up internally and externally:\n- First, you get a **Teams Recap** of the webinar recording to capture key questions and answers (saves you from re-watching 1 hour).\n- Next, you jump into **Word Copilot** with those key Q\&As to draft a blog post for the intranet summarizing the webinar for your colleagues.\n- Simultaneously, you use **Outlook Copilot** to draft a personalized follow-up email to all webinar attendees thanking them and highlighting one or two points (you feed it the key points from Teams Recap as context). It even helps you with a French version of the email.\nIn minutes, you have a blog draft and an email draft. Each Copilot was used in the environment best suited for the task and had the relevant context available (Teams had the conversation, Word for writing long text, Outlook for email contacts and tone), making the process seamless."  
anti\_pattern: "A marketer tries to do everything in one place: they copy-paste a meeting transcript into a Word prompt to get a summary, then copy that into an email, then use the same Word Copilot to translate to French. This all-in-one approach leads to mistakes — the Word summary missed some action items that Teams would have caught, and the translation was literal and missed some nuanced phrasing that a proper translation tool or human would catch. The result is disjointed communication that requires back-and-forth fixes. The misstep was not using the right Copilot for each step; a lot of manual patchwork ensued."  
takeaway: "**Match the tool to the task.** Copilot is integrated in many places — use that to your advantage. Ask: “Where is my source info? What do I need to create?” Then pick the Copilot surface that naturally handles that. You’ll get better results faster, and each step will feed the next with less copy-paste and less error."

### Course 7 Reading

framework\_name: "End-to-End AI Workflow"  
concept\_text: "Bringing it all together, an **End-to-End AI Workflow** means using AI across the full span of a project, applying each of the six skill domains as needed. For a marketing project, that could look like:

1.  **Start Safe (Responsible AI):** Begin by reviewing your inputs (contact lists, meeting notes, performance data) and cleansing or abstracting any non-public info. Set clear rules for yourself about what not to share with AI at each stage.
2.  **Ideation and Drafting (Strategic Prompting):** Use AI to brainstorm campaign ideas or draft content. Craft prompts (with CRAF) for things like “Outline a campaign plan for Product X launch” or “Draft a first-cut of an event invitation email.” Get that first batch of outputs to work with.
3.  **Review AI Outputs (Critical Evaluation):** For each AI-generated result, pause and apply VERIFY. Does that plan make sense? Is that email factually correct and on-brand? Iterate on the prompt or manually fix issues. Possibly loop back to AI with a refined prompt if needed.
4.  **Personalize and Target (Relationship Intelligence):** As you develop materials, use AI to gather additional insight on target audiences or key accounts (public info only), then weave in the custom touches yourself. For example, ask for “common challenges for food exporters in 2023” and use that intel to tailor a pitch, combined with knowledge of a specific client (without exposing your client’s name to AI).
5.  **Analyze and Decide (Data-Driven Decision Making):** Once the campaign is running or finished, feed data to AI to crunch numbers and highlight results. Maybe use Copilot to generate a performance report. But then interpret it with your understanding (maybe a low turnout was because of a storm that day – something AI wouldn’t know).
6.  **Multi-Channel Communication (Augmented Communication):** Finally, disseminate your findings and follow-ups efficiently. Use the Surface Selector: e.g., Teams to recap a wrap-up meeting, PowerPoint Copilot to draft slides for the results presentation, and Outlook to send personalized thank-you emails to participants. Ensure bilingual versions are created if needed.

Throughout an end-to-end workflow, you’re not using AI for the sake of it; you’re using it where it adds value: speeding up grunt work, offering creative suggestions, and processing data — all while **you** steer the ship, maintain compliance, and add the human touch. Done right, an AI-augmented workflow can significantly amplify your marketing impact and responsiveness."  
good\_example: "In the **ExportBoost Program** scenario, an end-to-end AI workflow might unfold like this:\n- **Responsible AI:** Before uploading a list of participants to analyze, you strip out names and use categories (SAFE in action).\n- **Strategic Prompting:** You ask Copilot in Word, “Draft an event agenda for a webinar on cash flow, aimed at mid-sized tech exporters,” providing context – it gives you a decent draft to build on.\n- **Critical Evaluation:** After Copilot drafts a post-event summary, you fact-check and notice it attributed a quote to the CEO that she didn’t actually say. You remove that (VERIFY applied).\n- **Relationship Intelligence:** You use Bing Chat (with only public info) to see recent news on three key companies to personalize follow-up emails. You find one just opened a UK office – great hook, which you manually tailor into your email (no AI needed for that part beyond giving you the news idea).\n- **Data-Driven Decision:** You run an Excel Copilot analysis on poll feedback from the event, which shows 90% want more training on risk management. Knowing one big client skewed it with multiple entries, you adjust for that and confirm there’s still a strong interest – so you decide to propose a new seminar on that topic.\n- **Augmented Communication:** To report results, you use PowerPoint Copilot to draft slides summarizing the webinar ROI. You then use Copilot’s translation suggestion to produce a French version of the summary slide content for bilingual delivery.\nEach step flows into the next, and AI is your helper at every stage, but you’re applying the right skill at the right time so the final outcomes are effective, accurate, and customized."  
anti\_pattern: "Imagine someone trying to use AI end-to-end without applying the skills: they dump raw data into ChatGPT (violating privacy), accept the first campaign idea it gives (no strategic prompting or relationship insight), send out AI-written emails without reading them (no evaluation or personalization), and blindly trust AI’s report of success. The result? Perhaps the AI suggested a generic campaign that doesn’t resonate, the emails contained an embarrassing error, and the report was misinterpreted. This “end-to-end” use of AI is end-to-end wrong. It underscores why each skill domain matters — you need *all of them* to truly optimize workflow."  
takeaway: "**End-to-end AI integration isn’t “set and forget” – it’s engage and elevate.** By weaving together safe data practices, smart prompting, critical review, personal context, verified analysis, and multi-tool workflows, you unlock AI’s full potential across a project. The sum is greater efficiency and impact, without ever losing the human judgment and personal touch that make marketing campaigns successful."

***

## SECTION F — Diagnostic Item Seeds

### Diagnostic: responsible\_ai

Item 1 — type: mcq  
question\_text: "Which of the following contains **non-public information** that should NOT be directly put into an AI prompt or tool?"  
options: A) A published news article about a client’s industry | B) A list of email addresses collected from an event sign-up form | C) A brochure from EDC’s public website | D) A statistic from a publicly released EDC annual report  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
scenario\_text: "You have an Excel file of 150 new leads from a webinar, including each person’s name, company, email, and specific question they asked. You want to use Copilot to draft a follow-up email that addresses some common questions. How can you write the prompt for Copilot **without exposing sensitive personal data**?"  
question\_text: "Write a prompt that you would give to Copilot to generate a follow-up email to webinar attendees, **avoiding any non-public personal details**. (Remember to describe the audience and their interests in general terms, rather than listing individual names or emails.)"  
scoring rubric criteria:
\- "No personal identifiers from the list are present (no individual names, emails, etc.)": max 1
\- "Mentions the webinar context and general topics of interest (e.g., “many attendees asked about X”) to give Copilot context": max 1
\- "Specifies the task (draft a follow-up email) and desired tone/format": max 1
\- "Uses only aggregated or anonymized descriptors for the leads (e.g., 150 tech industry attendees, small businesses, common questions on financing) without specific private info": max 1

Item 3 — type: micro\_task  
scenario\_text: "A marketer pasted a full list of client contact info into an AI chat to summarize it, and then realized this was a mistake."  
question\_text: "In one sentence, explain **why** directly sharing that client contact list with the AI was against policy."  
scoring rubric criteria:
\- "Mentions that it exposed non-public personal/company data or violates privacy/EDC AI policy": max 2
\- "Acknowledges the risk of external storage or unintended disclosure of that data": max 2

### Diagnostic: strategic\_prompting

Item 1 — type: mcq  
question\_text: "A marketer typed the prompt: *'Summarize what I should announce to clients about our new service.'* According to the CRAF framework, what is the **biggest missing element** in this prompt?"  
options: A) Context about which service and audience | B) A request for a specific format | C) The AI’s role | D) A friendly tone instruction  
correct\_option: A  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
scenario\_text: "EDC is launching an insurance product for small exporters. You have the key facts (coverage details, benefits) and target audience (Canadian small businesses new to exporting). You need Copilot to draft a one-page product overview for an email newsletter."  
question\_text: "Write a **complete CRAF prompt** to generate a first draft of the product overview for the newsletter. Include all necessary context about the product and audience, assign an appropriate role to the AI, specify the action, and define the format (e.g., length or structure of the overview)."  
scoring rubric criteria:
\- "Context is detailed (mentions it’s an insurance product for small exporters, and any key facts like coverage features)": max 1
\- "Role is given (e.g. AI should act as a marketing copywriter or product marketer writing to small business owners)": max 1
\- "Action is clear (e.g. draft a one-page overview or \~150-word blurb for a newsletter, highlighting benefits)": max 1
\- "Format is specified (newsletter style, possibly with a headline and short paragraphs, or bullet points as appropriate)": max 1

Item 3 — type: micro\_task  
scenario\_text: "Copilot produced a very generic output for a prompt about a new EDC service. The prompt was simply: *'Tell customers about our new loan program.'* The output said: *'We have an exciting new program to help your business grow.'* (and not much else useful)."  
question\_text: "In one sentence, explain why the output was so generic **and name two CRAF elements that were missing** from the original prompt."  
scoring rubric criteria:
\- "Identifies lack of specific Context as a reason (no details about the program or audience)": max 2
\- "Identifies another missing element (Action clarity or Format) as a reason (prompt didn’t say what to produce or how)": max 2

### Diagnostic: critical\_eval

Item 1 — type: mcq  
question\_text: "If Copilot provides a summary of last quarter’s marketing results and includes a statistic you’ve never seen before, what should you do first?"  
options: A) Include the statistic in your report to sound insightful | B) Double-check the statistic against the original data or source | C) Assume Copilot has access to secret data you don’t and use it | D) Ask Copilot to make the number even higher for a better impression  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
scenario\_text: "You used Copilot to draft a case study about a client’s success. The AI wrote: *"EDC’s loan helped increase the client’s revenue by 50% in one year."* You’re not sure that figure is accurate, and it wasn’t in the source info you provided."  
question\_text: "What follow-up prompt could you give Copilot to **verify or find the source** of that 50% increase claim before you publish the case study? Write a brief prompt asking Copilot to check this detail."  
scoring rubric criteria:
\- "The prompt directly addresses the questionable detail (mentions the “50% increase in revenue” and asks Copilot to confirm or provide source)": max 2
\- "It indicates the need for accuracy, possibly by instructing Copilot to only use provided data or to double-check the original document": max 1
\- "It does not simply accept the figure; it frames it as something to verify or expand on rather than blindly restating it": max 1

Item 3 — type: micro\_task  
scenario\_text: "Copilot drafted a social post about a new EDC service and included the line: *"EDC launched in 1985 and has helped 100k exporters."* In reality, EDC was founded in 1944 and the number of exporters helped is different."  
question\_text: "In one sentence, describe what went wrong with the AI’s statement and how you would correct it."  
scoring rubric criteria:
\- "Acknowledges the AI provided incorrect facts (wrong founding year or stats)": max 2
\- "States that you would fix it by using the correct information (and implies verifying against official sources)": max 2

### Diagnostic: relationship\_intel

Item 1 — type: mcq  
question\_text: "What is a safe and effective use of AI for account-based marketing?"  
options: A) Inputting a prospect’s confidential sales history to have AI craft a pitch | B) Asking AI for recent industry trends affecting your prospect’s sector, then tailoring your message using those trends | C) Having AI automatically send LinkedIn invites to all your prospect contacts | D) Using AI to generate a detailed email mentioning the prospect’s private expansion plans  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
scenario\_text: "You are preparing for a meeting with NovaTech Innovations Inc., a prospect. You know their industry (clean tech) and that they recently won an award (public news), and internally you’ve heard they’re interested in financing for a new project (not public). You want AI to help gather some background."  
question\_text: "Write a prompt to an AI assistant to get **publicly available insights** on NovaTech and the clean tech industry that could enrich your meeting prep. (Make sure your prompt does not include any confidential info about the new project.)"  
scoring rubric criteria:
\- "Clearly asks for public information (e.g., recent news, industry trends) about the company or sector": max 1
\- "Mentions the company name and context that are public (the award, industry) to focus the AI’s search": max 1
\- "Excludes any reference to the confidential new project or any non-public detail": max 1
\- "Specifies the output use (e.g., insights for a meeting prep) or format, so the AI gives a useful briefing": max 1

Item 3 — type: micro\_task  
scenario\_text: "An eager marketer prompted AI with: *“Using our private notes, draft an email to Montane Aerospace saying we know they plan a 20% expansion (from our confidential meeting).”* The AI produced an email including that detail."  
question\_text: "In one sentence, explain why sending this AI-created email to the client **would be a bad idea**."  
scoring rubric criteria:
\- "Highlights that it reveals non-public or confidential information back to the client (which could breach trust or confidentiality)": max 2
\- "Indicates it would be inappropriate or violate ethical/policy standards (using private info without permission)": max 2

### Diagnostic: data\_decision

Item 1 — type: mcq  
question\_text: "Copilot highlighted a 40% drop in webinar attendance for one region last month and labeled it a 'significant decline.' What should you do before deciding to cut webinars in that region?"  
options: A) Immediately reallocate the entire webinar budget from that region | B) Verify if any special circumstances (e.g., holidays or one-off events) caused the drop and check raw attendance numbers | C) Trust Copilot’s analysis and cancel all future webinars in that region | D) Announce to leadership that webinars are failing based on this drop  
correct\_option: B  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
scenario\_text: "You have a spreadsheet of marketing leads by source (webinar, email campaign, trade show) and their conversion rates. You want to use Excel Copilot to find insights for where to focus efforts."  
question\_text: "Write a Copilot prompt in Excel to identify which lead source has the **highest conversion rate** and to see if Copilot can find a reason or pattern (for example, maybe one source stands out in a particular segment). Make sure your prompt asks for both the comparison and any insight."  
scoring rubric criteria:
\- "The prompt explicitly asks for the highest conversion rate by lead source (so the AI will compare webinar vs email vs trade show conversions)": max 1
\- "It also asks for possible explanations or patterns (not just the numbers), inviting Copilot to analyze further (e.g., by segment or any notable attribute)": max 1
\- "Specifies or implies using the data given (so Copilot knows to use the spreadsheet’s data for the analysis)": max 1
\- "Is clearly phrased for Excel Copilot (mentions sources, conversion rates, maybe an instruction like 'analyze' or 'summarize')": max 1

Item 3 — type: micro\_task  
scenario\_text: "Copilot in Power BI suggests: *"Export sector leads were 30% of total, and this is a huge increase."* You recall that this percentage was always around 25-28% and that last quarter a new definition of “export sector” was used, making 30% not that unusual."  
question\_text: "In one sentence, explain how your contextual knowledge affects your interpretation of Copilot’s 30% finding."  
scoring rubric criteria:
\- "Mentions that historically it’s not a big change or that a definitional change occurred (providing context that the AI would not know)": max 2
\- "Concludes that therefore it’s not truly a 'huge increase,' showing the human insight tempering the AI’s claim": max 2

### Diagnostic: augmented\_comm

Item 1 — type: mcq  
question\_text: "You just finished a Teams meeting with a client and need to send a summary email of the discussion. What’s the most efficient Copilot-assisted workflow?"  
options: A) Use Teams Copilot to generate a meeting recap, then feed that recap to Outlook Copilot to draft the summary email | B) Ask Word Copilot to summarize the meeting from memory, then copy-paste into an email | C) Use PowerPoint Copilot to create slides of the meeting, then email those | D) Write and translate the email manually to be safe, avoiding Copilot  
correct\_option: A  
scoring: correct = 4, incorrect = 0

Item 2 — type: prompt\_sandbox  
scenario\_text: "You have a finalized English press release in Word about a new EDC program. You need a French version for simultaneous release."  
question\_text: "Write a prompt for Word Copilot (or another appropriate Copilot tool) to help **translate** the press release into French. Assume the press release text is available to Copilot. Include any instructions to ensure the translation maintains a professional tone and EDC’s style."  
scoring rubric criteria:
\- "Clearly requests a French translation of the provided English text (so the task is unambiguous)": max 1
\- "Specifies maintaining tone/style (e.g., professional, consistent with EDC voice, not a literal word-for-word if adjustments needed)": max 1
\- "Addresses the format (it’s a press release, so maybe instruct to keep structure, headings, etc., in the translation)": max 1
\- "Uses the appropriate tool context (e.g., indicates this is within Word or suggests it has the document content to translate)": max 1

Item 3 — type: micro\_task  
scenario\_text: "An EDC Communications Advisor used Outlook Copilot to draft an email and Word Copilot to draft a one-page fact sheet. They are considering which tool to use to polish a 10-slide presentation on the same topic."  
question\_text: "In one sentence, explain **why** using PowerPoint Copilot (rather than Word or Outlook Copilot) would be the best choice to help create or polish the slide deck."  
scoring rubric criteria:
\- "Explains that PowerPoint Copilot is designed for slide content/visuals/structure, so it can better format bullet points or suggestions for slides (where Word/Outlook are for text documents or emails)": max 2
\- "States that using the tool intended for presentations will yield a more appropriate output for a slide deck": max 2

***

## SECTION G — Evaluation Item Seeds

### Evaluation: Course 1 (mk\_c1\_responsible\_ai) — 4 items

Item 1 — type: mcq, sequence: 1  
question\_text: "In the SAFE Abstraction Method, what does the 'A' stand for and encourage you to do?"  
options: A) **Always Append Data** – add extra data to your prompt for clarity | B) **Anonymize Personal Details** – remove or replace names, emails, etc., with generic terms | C) **Ask for Evidence** – have the AI cite its sources | D) **Adjust Tone** – specify the tone of the AI’s response  
correct\_option: B  
explanation: "The 'A' in SAFE is about Anonymizing personal or sensitive details before using AI. It means replacing real identifiers with generic descriptions so no private info is shared."

Item 2 — type: mcq, sequence: 2  
question\_text: "You want Copilot to summarize insights from a confidential marketing survey. What **safe approach** should you take?"  
options:
A) Copy-paste the raw survey spreadsheet into the chat so Copilot has full context  
B) Upload the survey data to a public Google Doc and give Copilot the link  
C) Replace actual names and any identifying details with generic labels before asking Copilot to summarize trends  
D) Avoid using Copilot entirely, since it can’t ever be used with internal data  
correct\_option: C  
explanation: "The best practice is to remove or anonymize confidential data (names, personal details) and then use Copilot to summarize or analyze the trends. This way you still get insights without exposing sensitive information."

Item 3 — type: mcq, sequence: 3  
question\_text: "Why is it risky to include client email addresses or full names in an AI prompt when using Copilot?"  
options:
A) It might confuse the AI and lead to a wrong answer  
B) The AI could store or reveal that non-public information outside of EDC’s control  
C) Copilot will send emails to those addresses automatically  
D) There is no risk; Copilot fully deletes all prompt content immediately  
correct\_option: B  
explanation: "Non-public personal data (like client emails) should not be shared with external AI services because it may be retained or used in ways we can’t control. Including such data violates privacy policies and EDC’s usage guidelines."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "You have a list of new contacts from <Company>Westport Composites Ltd.</Company>’s expo (names, titles, emails) and notes about their needs. You want to use Copilot to draft a follow-up email template for these contacts. **Write the prompt** you would use to get Copilot’s help, applying the SAFE method to avoid including any private data. (Assume Copilot has general knowledge of the expo event.)"  
scoring rubric:
key1: "No direct personal data from the contact list is present – the prompt does not contain individual names, emails, or any identifying details from the list"  
key2: "Includes an abstracted description of the audience and context (e.g., 'met 150 manufacturing company representatives at an expo, many interested in financing solutions') instead of specific data"  
key3: "Clearly requests an email draft as the output, with relevant details (like referencing the expo and common interests) so the AI knows what to write"  
key4: "Specifies tone or style appropriate for follow-up (e.g., professional and helpful), and remains compliant (maybe reminding to include a thank-you for visiting booth, etc.)"

### Evaluation: Course 2 (mk\_c2\_strategic\_prompting) — 4 items

Item 1 — type: mcq, sequence: 1  
question\_text: "Which CRAF element tells Copilot **how to structure and format** its output?"  
options: A) Context | B) Role | C) Action | D) Format  
correct\_option: D  
explanation: "Format is the element that instructs the AI on the desired structure, length, or style of the output (e.g., bullet points, number of paragraphs)."

Item 2 — type: mcq, sequence: 2  
question\_text: "Copilot’s first draft of your email is 600 words long and rambling, but you need a short, snappy message. Which prompt revision would help the most?"  
options:
A) Add the target audience details to the Context  
B) Specify in the Action to "write no more than 150 words and include 3 bullet points highlighting benefits"  
C) Change the Role to "junior marketer" to simplify the language  
D) Ask for a friendlier tone  
correct\_option: B  
explanation: "Telling Copilot exactly what length and format you need (e.g. a 150-word limit and bullet points) directly addresses the issue of the draft being too long and unfocused. Context and tone help in other ways, but here the key fix is adding specific format/length instructions."

Item 3 — type: mcq, sequence: 3  
question\_text: "Your prompt includes: *"Role: You are an EDC marketing strategist."* How does adding a role instruction improve Copilot’s output?"  
options:
A) It guarantees the output will be shorter  
B) It gives the AI a perspective, influencing vocabulary and tone to match an EDC marketing professional  
C) It prevents any factual errors in the content  
D) It makes the AI run faster  
correct\_option: B  
explanation: "Defining the AI’s role (e.g., as an EDC marketing strategist) helps calibrate the style and terms used. The AI will write with a voice and depth appropriate for that persona, making the output more relevant and on-brand. It doesn’t inherently fix factual accuracy or response speed."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "<Company>Boreal Outfitters Ltd.</Company> is a $30M outdoor gear exporter in BC that has never worked with EDC. You have an introductory call with their VP soon, and you want to send a warm-up email outlining how EDC can help them grow globally. **Write a complete CRAF prompt** for Copilot to generate a 200-word outreach email draft for Boreal Outfitters. Include specifics about the company (industry, size, situation) as Context, an appropriate Role, a clear Action, and a structured Format for the email."  
scoring rubric:
key1: "Context is specific to Boreal Outfitters (mentions outdoor gear industry, approximate size, and the fact they are new to EDC and looking to grow internationally)"  
key2: "Role is defined (e.g., instructs the AI it is a marketing professional or EDC advisor crafting the email), guiding tone and perspective"  
key3: "Action clearly states the task (draft an introductory outreach email offering EDC’s help with global expansion) and a desired length (\~200 words)"  
key4: "Format is indicated (for instance, a professional email with greeting, 2-3 short paragraphs, and a call-to-action or offer to follow up) allowing the AI to structure the content properly"

### Evaluation: Course 3 (mk\_c3\_critical\_eval) — 4 items

Item 1 — type: mcq, sequence: 1  
question\_text: "You used Copilot to summarize a technical document for a blog. Which finding should raise a **red flag** and prompt further verification?"  
options:
A) The summary includes a statistic that wasn’t in the original document  
B) The summary is written in a friendly tone  
C) The summary is shorter than you expected  
D) The summary uses bullet points instead of paragraphs  
correct\_option: A  
explanation: "If Copilot’s output introduces a statistic or fact that you never saw in the original source, that’s a red flag for a possible hallucination or error. It needs to be verified. Tone, length, or format might require adjustments, but an unexpected fact is what clearly demands verification."

Item 2 — type: mcq, sequence: 2  
question\_text: "Before sending out an AI-generated marketing email draft to 1,000 customers, you should:"  
options:
A) Trust Copilot’s draft if it looks good – it’s trained on lots of emails  
B) Use the VERIFY checklist – fact-check any claims, ensure tone and translations are correct, and confirm no confidential info is included  
C) Run it through another AI to double-check (AI can verify AI)  
D) Just add a disclaimer that "This email was auto-generated"  
correct\_option: B  
explanation: "The correct approach is to thoroughly review the AI-generated draft using a process like the VERIFY checklist. That means checking facts, tone, compliance (CASL, branding, etc.), and any potential leaks. You should not send AI content unreviewed; a second AI isn’t reliable for verification without human oversight."

Item 3 — type: mcq, sequence: 3  
question\_text: "Copilot translated a portion of your English marketing newsletter into French. What is the **best** practice before publishing the French version?"  
options:
A) Trust the AI’s translation if it didn’t produce an error message  
B) Have a bilingual colleague or translator review the French text for accuracy and tone  
C) Run the French text back through English translation to see if it matches the original  
D) Shorten the French text because AI translations tend to be too long  
correct\_option: B  
explanation: "Even if Copilot provides a translation, it’s vital to have a human (preferably a professional translator or bilingual colleague) review it. They can catch nuances, errors, or tone issues that the AI might have missed. Automatic back-translation can help spot glaring errors, but it’s not a substitute for a proper human review."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Copilot created the following event summary for an external newsletter:\n\n\*“EDC hosted a webinar with **500+ attendees**. **Every participant found it extremely valuable**, proving that EDC **guarantees success** for Canadian exporters.”\*\n\nHowever, you have real data: 350 people attended, 90% gave positive feedback, and of course EDC cannot guarantee success. Also, you need to make sure the message is delivered in both English and French. **Rewrite the summary** to correct the inaccuracies and inappropriate claims, and include a note about bilingual availability (in English and French). The tone should remain positive but factual."  
scoring rubric:
key1: "Corrects the number of attendees (uses the accurate figure of 350, avoiding the inflated “500+” and ensuring the phrasing is precise)"  
key2: "Removes or amends the overgeneralization that “every participant found it extremely valuable” to something supported by the data (e.g., citing the 90% positive feedback in a factual way)"  
key3: "Eliminates the claim that EDC 'guarantees success', rephrasing to a more appropriate statement about support or enabling success without making absolute promises"  
key4: "Includes a bilingual element, such as mentioning that the summary or resources are available in both English and French (since external communications must be bilingual), and overall uses a professional, factual tone"

### Evaluation: Course 4 (mk\_c4\_relationship\_intel) — 4 items

Item 1 — type: mcq, sequence: 1  
question\_text: "Why should you avoid directly telling Copilot about a prospect’s **confidential business plans** when asking it to draft a personalized email?"  
options:
A) Because Copilot might mention those confidential plans in the email draft, revealing them in writing  
B) Because Copilot doesn’t know how to use that information effectively  
C) Because Copilot will refuse to use any business information in prompts  
D) Because it’s better to surprise the client with information to show you did research  
correct\_option: A  
explanation: "Including confidential business plans in a prompt is risky because the AI might spill those details in the output. This could breach confidentiality and damage trust if included in a client email. The safe approach is to use that knowledge indirectly and never feed it verbatim into the AI."

Item 2 — type: mcq, sequence: 2  
question\_text: "What is one major advantage of using AI for prospect research **before** a sales/marketing outreach?"  
options:
A) It completely replaces the need to review the CRM notes for that prospect  
B) It can quickly summarize public news, industry trends, or financial data relevant to the prospect’s context  
C) It will write the final pitch for you without any human input  
D) It ensures your outreach has no risk of error  
correct\_option: B  
explanation: "AI can rapidly gather and summarize public information (like recent news or industry reports) relevant to your prospect. This can give you valuable context to tailor your outreach. It doesn’t replace reviewing internal notes, and you still need to craft and check the final message yourself."

Item 3 — type: mcq, sequence: 3  
question\_text: "You asked Copilot to draft a LinkedIn message to a prospect. Which of these **edits** would make the message feel more personalized (beyond what AI alone might produce)?"  
options:
A) Adding a sentence referencing a recent public achievement of the prospect’s company  
B) Removing the greeting to save the prospect’s time  
C) Adding more generic product details about EDC’s offerings  
D) Using a lot of exclamation marks to show enthusiasm  
correct\_option: A  
explanation: "Referencing something specific and recent about the prospect’s company (that’s public information, like an award or new office) shows you’ve done your homework and makes the message more relevant. AI might not include that on its own unless prompted. In contrast, too many exclamation points or generic info can seem spammy or impersonal."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "<Company>Montane Aerospace Corp.</Company> is a large aerospace company. It’s a key prospect for EDC. You’ve gathered public info: they opened a new Singapore branch and were featured in an industry report about supply chain innovation. You also know from private talks that they’re facing cash flow timing issues (not public). **Draft a short LinkedIn message** (3-4 sentences) to Montane’s CFO that congratulates them on their expansion and subtly mentions how EDC’s solutions can help with common challenges like supply chain financing. Make sure the message uses the public facts and implies understanding of their needs *without explicitly stating anything confidential*. Aim for a personalized, professional tone."  
scoring rubric:
key1: "Incorporates a public congratulatory detail or acknowledgement of Montane’s recent achievements (e.g., the new Singapore branch or their mention in an industry report) to immediately signal the message is tailored to them"  
key2: "Makes a connection to EDC’s services in a relevant way, addressing a likely pain point (like supply chain financing or cash flow) **without disclosing Montane’s confidential issues** – e.g., phrasing it as a common industry challenge or offering help in that area generally"  
key3: "Maintains a professional and collegial tone appropriate for an outreach from a marketing/business professional to a CFO (e.g., respectful, concise, not overly salesy or familiar)"  
key4: "Feels personalized and specific rather than like a mass message – the content should clearly be something that couldn’t just be sent to anyone (achieved through the use of the above details and context)"

### Evaluation: Course 5 (mk\_c5\_data\_decision) — 4 items

Item 1 — type: mcq, sequence: 1  
question\_text: "After Copilot identifies a surprising trend in your campaign data, what is your **next step**?"  
options:
A) Immediately adjust the marketing strategy according to that trend  
B) Verify the trend with the raw data and consider context (e.g., events or anomalies that could have affected results)  
C) Present the trend to leadership as a key insight without additional checks  
D) Ignore the trend because AI often makes mistakes  
correct\_option: B  
explanation: "The wise step is to validate the AI-identified trend by checking it against the source data and considering any context that might explain it. This ensures the trend is real and meaningful before you act on it or report it. Immediate changes or blind acceptance could be risky if the trend is a blip or error."

Item 2 — type: mcq, sequence: 2  
question\_text: "Copilot analyzed your data and said: *“Emails sent on Tuesdays have 2x higher open rates than those sent on Fridays.”* What should you do with this information?"  
options:
A) Schedule all future emails for Tuesdays, since AI found they’re better  
B) Check if the dataset supports this (e.g., compare Tuesday vs Friday opens yourself) and recall if anything special happened on those days (like a holiday on that Friday)  
C) Conclude that Friday emails are useless and eliminate them entirely  
D) Poll the team to see if they agree, instead of looking at the data  
correct\_option: B  
explanation: "You should confirm Copilot’s analysis by examining the data and also adding context — maybe that Friday had lower opens due to a holiday or a technical issue. If Tuesdays indeed perform better consistently (without special circumstances), you can then consider adjusting your strategy. Acting without verification or context might lead to false conclusions."

Item 3 — type: mcq, sequence: 3  
question\_text: "How does using Copilot in Excel or Power BI help a non-analyst marketer when making decisions?"  
options:
A) It automatically makes all decisions for the marketer  
B) It quickly crunches numbers and highlights patterns or outliers that the marketer can then investigate further  
C) It replaces the need for any manual review of data  
D) It prevents any errors in the data  
correct\_option: B  
explanation: "Copilot can rapidly analyze large sets of data and point out trends, correlations, or anomalies, saving time and providing a starting point for insight. However, the marketer still needs to interpret those findings, verify them, and make the final decisions. It doesn’t remove the need for human analysis and it doesn’t guarantee error-free data."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "You’ve received a Copilot-generated analysis of your last email campaign. It says, *“Open rates increased from 10% to 15% (5 percentage points) after we personalized the subject lines.”* You believe this is accurate. **Write a brief summary (2-3 sentences)** for your quarterly report that states this insight in a clear way for stakeholders, and mention how confident you are in it. (Assume you verified the data and know that the increase is significant.)"  
scoring rubric:
key1: "Clearly communicates the key insight with the correct figures – e.g., stating that open rates improved from about 10% to 15% after implementing personalized subject lines"  
key2: "Provides a plausible interpretation or significance of this change (for example, that personalized subject lines likely contributed to the improvement in engagement)"  
key3: "Mentions the level of confidence or how it was verified (for instance, noting that this finding was confirmed by analyzing the email data or A/B test results)"  
key4: "Presents the information in a concise, executive-ready manner (2–3 sentences, in a positive but factual tone, suitable for a quarterly marketing report to leadership)"

### Evaluation: Course 6 (mk\_c6\_augmented\_comm) — 4 items

Item 1 — type: mcq, sequence: 1  
question\_text: "You have raw notes from a meeting in OneNote and need to draft a formal proposal from it in Word, then email that to a client. According to the Copilot Surface Selector, which sequence is most efficient?"  
options:
A) Use OneNote Copilot to convert notes to a proposal and then have Teams Copilot send the email  
B) Copy the notes into Word and use Word Copilot to draft the proposal, then use Outlook Copilot to help compose the email to the client with the proposal attached  
C) Summarize the notes with Excel Copilot, then paste the summary into an email  
D) Manually rewrite the notes into a proposal in Word, then copy-paste to Outlook Copilot  
correct\_option: B  
explanation: "The best workflow is to use Word’s Copilot to transform notes into a well-structured proposal (since Word is ideal for document drafting and formatting), and then use Outlook’s Copilot to draft an email to the client, attaching or incorporating the proposal. This way, you leverage each tool’s strengths and avoid unnecessary manual copying."

Item 2 — type: mcq, sequence: 2  
question\_text: "Which task is **best suited** for Teams (Meetings) Copilot as opposed to other Copilot interfaces?"  
options:
A) Drafting a new marketing plan document  
B) Summarizing a recorded client call and extracting action items  
C) Designing slides for a marketing presentation  
D) Composing a mass marketing email to clients  
correct\_option: B  
explanation: "Teams Meetings Copilot is designed to work with meeting content – it can summarize discussions, extract action items, and highlight who said what during a call. The other tasks listed (writing plans, designing slides, drafting mass emails) are better suited for Word, PowerPoint, and Outlook Copilot respectively."

Item 3 — type: mcq, sequence: 3  
question\_text: "When using Copilot to prepare content in both English and French, what is a good practice?"  
options:
A) Draft in English only; translating is not a concern for marketing  
B) Use Copilot to draft in one language (e.g., English) and then have it assist in translating or drafting the other language, followed by a human review of the translation  
C) Always draft everything in French first, then translate to English manually  
D) Avoid using Copilot for bilingual content entirely, since it can’t handle translations  
correct\_option: B  
explanation: "It’s efficient to leverage Copilot to produce content in one language and then use its capabilities to translate or draft the content in the second language. However, since translations may contain errors or lost nuances, a human should review the translated content for accuracy and tone. This approach combines AI speed with human quality control."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Describe a workflow using Copilot to create and distribute a marketing update in multiple formats: You need a 1-page internal report (Word document), a 3-slide summary for a meeting (PowerPoint), and a brief announcement email (Outlook) to notify staff. Outline, in 3-4 bullet points, how you would accomplish this with Copilot, specifying which tool you’d use at each step."  
scoring rubric:
key1: "Mentions using Word (and its Copilot) to draft the 1-page internal report, since Word is suited for detailed text documents"  
key2: "Includes using PowerPoint Copilot to generate or refine a 3-slide summary based on the report content (or directly from key points), leveraging the AI for visual/slide formatting"  
key3: "Describes using Outlook Copilot to compose the announcement email that will go out to staff, likely summarizing the report and attaching it or linking to it"  
key4: "Shows the logical order or integration – e.g., first preparing content (report) in Word, then distilling it into slides with PowerPoint, then crafting the email to distribute it – illustrating an efficient multi-surface workflow with Copilot"

### Evaluation: Course 7 (mk\_c7\_capstone) — 4 items

Item 1 — type: mcq, sequence: 1  
question\_text: "In an end-to-end AI-assisted marketing project, which of these sequences best reflects a safe and effective workflow?"  
options:
A) Upload raw client data → Have AI automatically generate plan, content, and analysis → Implement without oversight  
B) Define objectives & data (sanitize sensitive info) → Use AI for drafts/analysis at different stages → Review and refine each AI output → Deliver polished results  
C) Use one AI tool to do everything in one go, from start to finish, to save time  
D) Avoid using AI until the very final step, then try to apply it as a quick fix  
correct\_option: B  
explanation: "The ideal end-to-end workflow is to incorporate AI thoughtfully at each stage: start by preparing your data safely, use AI to assist with ideas, drafting, and analysis in each phase, but critically review and improve its outputs along the way. This ensures both efficiency and quality. The other options either over-rely on AI without oversight or underutilize it."

Item 2 — type: mcq, sequence: 2  
question\_text: "Which statement about using all six AI skill domains together is true?"  
options:
A) They are sequential steps that only work in order and never overlap  
B) In a real project, you often use multiple skills at once (e.g., prompt strategically while ensuring data is safe and then critically evaluate the output)  
C) You should only use one domain per task to avoid confusion  
D) If you master Strategic Prompting, you don’t need the other skills as much  
correct\_option: B  
explanation: "In practice, the domains blend. For example, you might use Responsible AI and Strategic Prompting simultaneously — writing a good prompt (prompting) that also abstracts sensitive data (responsible AI). Then you’d use Critical Evaluation on the output. All the skills reinforce each other rather than being isolated. Mastering one doesn’t eliminate the need for the others."

Item 3 — type: mcq, sequence: 3  
question\_text: "After completing an AI-assisted marketing campaign, what is an important final step to continue improving your AI usage?"  
options:
A) Delete all AI prompts and outputs to avoid any record of AI involvement  
B) Reflect on what AI did well or poorly (e.g., which prompts yielded good vs. bad results) and share these lessons with your team  
C) Immediately start the next project with the same AI approach without changes  
D) Conclude that you can now run campaigns with AI and minimal human input  
correct\_option: B  
explanation: "It’s important to conduct a retrospective on how AI contributed. Identifying what went well and what issues arose with prompts or outputs means you can refine your approach next time. Sharing with the team turns you into a Champion, helping everyone benefit. Wiping out records or blindly reusing approaches misses the opportunity to learn and improve."

Item 4 — type: performance\_task, sequence: 4  
question\_text: "Imagine you’re kicking off the **ExportBoost Program** (the capstone scenario described). **In 4-5 sentences, summarize your plan for using AI throughout this project**, touching on how you will apply responsible data handling, strategic prompting, critical evaluation of outputs, relationship intelligence for personalization, data-driven analysis, and multi-format communication. (This is a high-level summary to demonstrate your integrated approach.)"  
scoring rubric:
key1: "Mentions handling data responsibly at the start, for example indicating that you will remove or anonymize sensitive client information before using AI (Responsible AI)"  
key2: "Describes using AI for content generation or planning with well-crafted prompts (Strategic Prompting) and indicates that you will review and fact-check those outputs (Critical Evaluation)"  
key3: "Includes personalization steps like using AI to get public insights on clients and combining with internal knowledge to tailor outreach (Relationship Intelligence), without sharing confidential info with the AI"  
key4: "References using AI for analyzing campaign results (Data-Driven Decision Making) and employing appropriate Copilot tools for creating communications or reports (Augmented Communication), demonstrating a complete end-to-end vision"
