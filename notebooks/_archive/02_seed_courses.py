# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Seed Courses
# MAGIC
# MAGIC Seeds all 5 RM training courses into:
# MAGIC - `content.courses` — course metadata
# MAGIC - `content.reading_content` — concept text, examples, takeaway
# MAGIC - `content.practice_scenarios` — scenario text, 4 tasks, AI coach system prompt
# MAGIC - `content.evaluation_items` — 3 MCQ + 1 performance task per course
# MAGIC
# MAGIC Idempotent: deletes existing rows for these course IDs before re-inserting.

# COMMAND ----------

import os, json

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")

def sql(statement: str):
    spark.sql(statement).collect()  # Force eager execution for DML statements

def escape(s: str) -> str:
    """Escape single quotes for SQL string literals."""
    return s.replace("'", "''")

COURSE_IDS = [
    "rm_c1_prompting",
    "rm_c2_verification",
    "rm_c3_data_safety",
    "rm_c4_tool_fluency",
    "rm_c5_capstone",
]

# Clear existing data for these courses (idempotent)
ids_sql = ", ".join(f"'{cid}'" for cid in COURSE_IDS)
for table in ["evaluation_items", "practice_scenarios", "reading_content", "courses"]:
    col = "course_id"
    sql(f"DELETE FROM {CATALOG}.content.{table} WHERE {col} IN ({ids_sql})")
    print(f"Cleared {table}")

# COMMAND ----------
# Course 1 — Brief Like a Pro: From ARM Handoff to Discovery Brief

C1_ID = "rm_c1_prompting"

sql(f"""
INSERT INTO {CATALOG}.content.courses
  (course_id, role_id, primary_domain, title, tagline, description, real_use_case, sequence_order)
VALUES (
  '{C1_ID}', 'rm', 'prompting',
  'Brief Like a Pro: From ARM Handoff to Discovery Brief',
  'Turn a messy ARM handoff into a sharp discovery brief using the CRAF prompt framework.',
  '{escape("RMs spend significant time preparing for discovery calls. This course teaches the CRAF framework (Context, Role, Action, Format) to produce briefing documents, discovery questions, and talking points that are directly usable — not generic AI output that needs full rewrites.")}',
  '{escape("Access to Copilot 365 for Business Development (Mid Market); Prospect Intelligence; RM Support Agent")}',
  1
)
""")
sql(f"""
INSERT INTO {CATALOG}.content.reading_content
  (content_id, course_id, concept_text, good_example, anti_pattern, takeaway)
VALUES (
  'rc_{C1_ID}', '{C1_ID}',
  '{escape("Great AI output starts with a great prompt. The CRAF framework gives you four elements that consistently produce usable output:\n\n**C — Context**: Who is the client? What situation are they in? What do you already know?\nExample: 'A $45M Ontario manufacturer exporting to the US and Germany, no current EDC relationship.'\n\n**R — Role**: What role should the AI play?\nExample: 'You are a senior Relationship Manager at a Canadian export finance institution.'\n\n**A — Action**: What exactly do you want it to do?\nExample: 'Draft a 200-word discovery brief with the key questions I should ask in my first call.'\n\n**F — Format**: How should the output be structured?\nExample: 'Use three sections: Business Context, Key Discovery Questions, and Recommended Next Step.'\n\nWhen all four elements are present, the AI knows who it is speaking as, who it is speaking about, what to produce, and how to present it. Missing any one element degrades the output — often dramatically.")}',
  '{escape("**Prompt:** 'Context: Maple Industries Ltd., a $45M Ontario manufacturer, was just handed off from our ARM team. They export to the US and Germany. They have no current EDC relationship and currently use another bank'\''s letter of credit facility. Role: You are a senior Relationship Manager at a Canadian export finance institution. Action: Draft a 200-word discovery brief with the key questions I should ask in my first call. Format: Use three sections — Business Context, Key Discovery Questions, and Recommended Next Step.'\n\n**Why it works:** The AI has a specific company profile (Context), a clear voice (Role), a concrete deliverable (Action), and knows exactly how to structure the output (Format). The result is usable with minor edits — not a 500-word generic overview of export finance.")}',
  '{escape("**Prompt:** 'Write a discovery brief for my new client.'\n\n**Why it fails:** The AI has no context about the client, no role to speak from, no specific deliverable, and no format guidance. The output will be a generic template applicable to any client — which means it'\''s useful to no one. The RM will spend more time editing than they saved by using AI. This is the single most common prompting mistake: treating AI like a search engine instead of a collaborator who needs context.")}',
  '{escape("A prompt is only as useful as the context you put in it. Specificity in all four CRAF elements — Context, Role, Action, Format — is what separates AI output you can use from output you have to rewrite.")}'
)
""")

C1_COACH = escape(
    "You are an AI coach for 'Brief Like a Pro', a course on structured AI prompting for "
    "Relationship Managers at a Canadian export finance institution. Your role is to guide "
    "learners through the CRAF framework (Context, Role, Action, Format).\n\n"
    "In this session the learner is practicing writing effective prompts for a discovery "
    "brief scenario. Their scenario: An ARM just handed off Maple Industries Ltd. — an "
    "Ontario manufacturer, $45M revenue, exports to US and Germany, no current EDC "
    "relationship.\n\n"
    "Your coaching guidelines:\n"
    "- Ask questions that prompt the learner to identify missing CRAF elements. Never write "
    "the prompt for them.\n"
    "- When Context is missing: 'What does the AI need to know about the client to give "
    "you a useful answer?'\n"
    "- When Role is missing: 'Have you told the AI what kind of professional is asking this?'\n"
    "- When Action is vague: 'What specific output are you asking for — a list of questions, "
    "a briefing document, talking points?'\n"
    "- When Format is missing: 'How do you want the output structured — sections, bullets, "
    "a specific length?'\n"
    "- Celebrate clear improvements: acknowledge which CRAF element they added and why it helps.\n"
    "- If a learner submits a strong CRAF prompt, affirm it and explain which elements are working.\n"
    "- Keep responses under 100 words.\n"
    "- Never tell the learner the 'right answer' — guide them to discover it."
)

sql(f"""
INSERT INTO {CATALOG}.content.practice_scenarios
  (scenario_id, course_id, scenario_text, task_1_text, task_2_text, task_3_text, task_4_text, coach_system_prompt)
VALUES (
  'ps_{C1_ID}', '{C1_ID}',
  '{escape("Your ARM, Jordan, just handed off Maple Industries Ltd. after a successful intro call. Notes show: Ontario manufacturer, $45M revenue, exports to US and Germany, currently uses another bank'\''s letter of credit facility, open to exploring alternatives. You have a discovery call with their CFO in two days. You want to use AI to help you prepare a discovery brief.")}',
  '{escape("Write a prompt to generate a discovery brief for your call with Maple Industries Ltd. What information does your prompt include? Type your prompt below.")}',
  '{escape("Your first prompt produced useful but generic questions — they could apply to any client. Add a format constraint to get a structured output with clearly labelled sections. What do you add to your prompt?")}',
  '{escape("The CFO at Maple Industries is technically sophisticated and has been using trade finance for 15 years. Add an audience constraint to tailor the tone so the output doesn'\''t explain basics. How does your revised prompt read?")}',
  '{escape("The revised output still includes a section on domestic financing that isn'\''t relevant to this client. Write an iteration prompt to remove that section and refocus the output on export finance opportunities only.")}',
  '{C1_COACH}'
)
""")

# Evaluation items — Course 1
sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C1_ID}_q1', '{C1_ID}', 'mcq', 1,
  'Which CRAF element is missing from this prompt: "Write an email to a prospect about our export financing products"?',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Context — there is no information about who the prospect is or their situation"},{"label":"B","text":"Role — the AI has not been told what professional is asking"},{"label":"C","text":"Action — the task (write an email) is not specified"},{"label":"D","text":"Format — the email structure has not been defined"}]))}',
  'A',
  '{escape("The prompt has an implied Role (an EDC employee), an Action (write an email), and an implied Format (email). What it completely lacks is Context — who is the prospect, what do they export, what is their current situation? Without context the AI will write a generic email applicable to no one in particular.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C1_ID}_q2', '{C1_ID}', 'mcq', 2,
  'A well-structured CRAF prompt should tell the AI:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"The client context, the role to speak from, exactly what to produce, and how to format the output"},{"label":"B","text":"The client'\''s full legal name, credit history, and account balance"},{"label":"C","text":"Your personal background, your manager'\''s name, and today'\''s date"},{"label":"D","text":"The AI tool version you are using and your preferred language"}]))}',
  'A',
  '{escape("CRAF = Context (who/what/situation) + Role (voice the AI speaks from) + Action (specific deliverable) + Format (structure of output). Together these four elements give the AI everything it needs to produce output that is specific and directly usable in an RM workflow.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C1_ID}_q3', '{C1_ID}', 'mcq', 3,
  'After using AI to draft a discovery brief, the best next step is:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Review it, remove anything inaccurate or generic, then use it"},{"label":"B","text":"Send it to the client immediately to save time"},{"label":"C","text":"Submit it to your manager for approval before using any AI output"},{"label":"D","text":"Regenerate it with a different prompt until it looks exactly right"}]))}',
  'A',
  '{escape("AI output is a starting point, not a final product. Reviewing and editing ensures accuracy and relevance before use. Sending unreviewed AI output to a client is a quality and trust risk. Regenerating indefinitely is inefficient. Manager approval is not the standard process for internal preparation documents.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C1_ID}_q4', '{C1_ID}', 'performance_task', 4,
  'Write a complete CRAF prompt to generate a one-page briefing document before your first discovery call with a new prospect.',
  '{escape("Company: Shoreline Advisory Group Ltd., a financial advisory firm based in Vancouver with approximately $20M in annual revenues. They are planning to expand into the US market over the next 12 months and have not worked with EDC before. You are an RM preparing for a discovery call with their VP of Finance.")}',
  NULL, NULL, NULL,
  '{escape(json.dumps({"context_present": 1, "role_present": 1, "action_specific": 1, "format_specified": 1}))}'
)
""")
print("Seeded Course 1: Brief Like a Pro")

# COMMAND ----------
# Course 2 — Recap, Review, Then Log: Post-Meeting AI Discipline

C2_ID = "rm_c2_verification"

sql(f"""
INSERT INTO {CATALOG}.content.courses
  (course_id, role_id, primary_domain, title, tagline, description, real_use_case, sequence_order)
VALUES (
  '{C2_ID}', 'rm', 'verification',
  'Recap, Review, Then Log: Post-Meeting AI Discipline',
  'Catch the errors AI puts into your meeting recaps before they make it into C3.',
  '{escape("Teams Copilot and similar tools generate meeting recaps automatically — but they hallucinate names, invent commitments, and misstate figures. This course teaches a verification discipline: what to check, how to check it, and how to log a corrected, reliable CRM note.")}',
  '{escape("Customer Interaction Recap; Meeting Recap in MS-Teams; Record Governance; Sales Transcript Analysis")}',
  2
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.reading_content
  (content_id, course_id, concept_text, good_example, anti_pattern, takeaway)
VALUES (
  'rc_{C2_ID}', '{C2_ID}',
  '{escape("AI meeting recap tools (like Copilot in Teams) generate summaries from audio and transcripts. They are fast — but error-prone in specific and predictable ways:\n\n**Common hallucination types in meeting recaps:**\n- **Wrong title**: 'CEO' when the person is a CFO\n- **Invented commitment**: 'committed to sending by Friday' when they only 'mentioned it'\n- **Fabricated figure**: '$3.5M facility' when the client said 'about three million'\n- **Unconfirmed plan**: 'expanding to Germany' when Germany was mentioned as a possibility\n- **Invented meeting**: 'follow-up scheduled for Nov 21' when no date was set\n\n**The verification checklist — check these four things before logging anything to C3:**\n1. **Dates**: Are all dates mentioned in the recap verifiable from your own notes or a confirmed calendar invite?\n2. **Names and titles**: Are all names spelled correctly and titles accurate?\n3. **Commitments**: Did the person actually commit, or did they 'mention', 'consider', or 'suggest'?\n4. **Figures**: Are all dollar amounts, percentages, and numerical references verifiable from your notes?")}',
  '{escape("Copilot generated: '\''Client mentioned interest in a $2M facility renewal.'\'' Before logging, I checked my notes — the client actually said '\''possibly around two million, but we haven'\''t finalized.'\'' I changed the CRM note to: '\''Client indicated a potential facility renewal in the $1.5–2M range, subject to board confirmation. To be confirmed at follow-up.'\'' Result: no false commitment in C3, and the follow-up note is actionable.")}',
  '{escape("Copilot generated: '\''Sarah Chen committed to sending the financial statements by Friday.'\'' I copied this directly into C3 without checking my notes. In my notes I had only written '\''Sarah mentioned statements'\'' with no deadline. Sarah never received a follow-up request because she never made that commitment — but C3 showed it as a pending action item for two weeks before I noticed. This created confusion with my ARM and eroded trust in the CRM data.")}',
  '{escape("Every AI-generated recap must pass four checks before it touches C3 or any permanent record: dates, names and titles, commitments, and figures. What you can'\''t verify from your own notes should not be logged.")}'
)
""")

C2_COACH = escape(
    "You are an AI coach for 'Recap, Review, Then Log', a course on AI output verification "
    "for Relationship Managers at a Canadian export finance institution.\n\n"
    "In this session the learner is reviewing a flawed Copilot meeting recap and practicing "
    "the verification discipline. The recap they are working with contains these specific "
    "errors compared to the RM's own notes:\n"
    "1. Michael Tremblay's title is CFO, not CEO\n"
    "2. Germany expansion is 'not confirmed', not stated as a definite plan\n"
    "3. The commitment to send financials was not firm ('said he'd try', no date)\n"
    "4. The facility size is 'about 3 million', not a confirmed $3.5M\n"
    "5. Interest in Export Guarantee was uncertain ('wasn't sure')\n"
    "6. The follow-up meeting on Nov 21 was not confirmed\n\n"
    "Your coaching guidelines:\n"
    "- Do NOT reveal these errors directly. Guide the learner to find them by asking: "
    "'How does what Copilot says compare to your own notes on that point?'\n"
    "- When a learner identifies an error, affirm and ask: 'Are there others?'\n"
    "- For Task 3 (C3 log format): coach toward present-tense, factual bullets that a "
    "colleague could act on without prior context.\n"
    "- For Task 4 (personal rule): accept any reasonable verification principle; probe "
    "for specificity ('What type of error would that rule catch?').\n"
    "- Keep responses under 100 words."
)

sql(f"""
INSERT INTO {CATALOG}.content.practice_scenarios
  (scenario_id, course_id, scenario_text, task_1_text, task_2_text, task_3_text, task_4_text, coach_system_prompt)
VALUES (
  'ps_{C2_ID}', '{C2_ID}',
  '{escape("You just finished a 30-minute Teams call with Northern Fabrication Ltd. (CFO: Michael Tremblay). Copilot generated the following recap:\n\n---\nCall with Northern Fabrication Ltd. — Nov 14, 2024\nAttendees: Sarah Chen (RM), Michael Tremblay (CEO), Jordan Park (ARM)\nSummary: Michael discussed the company'\''s plan to expand exports to France and Germany starting Q1 2025. He confirmed that they would send their most recent audited financials (FY2023) by November 18. The company currently has a $3.5M letter of credit facility with RBC, which expires in March 2025. Michael expressed strong interest in exploring EDC products, specifically BCAP and Export Guarantee.\nAction items:\n- Michael to send FY2023 financials by Nov 18\n- Sarah to prepare a product overview for the follow-up meeting on Nov 21\n---\n\nYour actual meeting notes: Michael — CFO not CEO. Mentioned possibly France, Germany not confirmed. Said he'\''d try to get financials but nothing firm. $3.5M LOC may be less — he said '\''about 3 million.'\'' Interested in BCAP, wasn'\''t sure about Export Guarantee. Follow-up not scheduled yet.")}',
  '{escape("Read the Copilot recap carefully and compare it to your meeting notes. List every factual error or unverifiable statement you can identify. Be specific about what the recap says versus what your notes show.")}',
  '{escape("Rewrite the recap to accurately reflect what was actually discussed, using your meeting notes as the source of truth. Correct every error you identified in Task 1.")}',
  '{escape("Write the corrected version as a CRM activity note ready to log into C3. Use present-tense, factual bullets. A colleague with no context should be able to act on this note without asking you questions.")}',
  '{escape("Based on this exercise, write one rule you would add to your personal verification checklist to catch this type of error in the future. Be specific about what the rule targets and how you would apply it.")}',
  '{C2_COACH}'
)
""")

# Evaluation items — Course 2
sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C2_ID}_q1', '{C2_ID}', 'mcq', 1,
  'An AI meeting recap says a client "committed to sending financials by Friday". Your notes say they "mentioned financials". What should you do before logging to C3?',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Change '\''committed'\'' to '\''mentioned'\'' and add '\''no firm deadline given'\''"},{"label":"B","text":"Log it as written — the AI is usually reliable about commitments"},{"label":"C","text":"Delete the financials reference entirely to avoid confusion"},{"label":"D","text":"Email the client to ask if they recall making the commitment"}]))}',
  'A',
  '{escape("The difference between '\''committed'\'' and '\''mentioned'\'' is material. Logging a false commitment creates follow-up risk and erodes CRM data quality. The correct action is to correct the language to match what was actually said and note that no deadline was set.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C2_ID}_q2', '{C2_ID}', 'mcq', 2,
  'Which of these is NOT a reliable source for verifying an AI meeting recap?',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Another AI-generated summary of the same call"},{"label":"B","text":"Your handwritten notes taken during the call"},{"label":"C","text":"A recorded transcript you reviewed manually"},{"label":"D","text":"A follow-up email listing agreed action items"}]))}',
  'A',
  '{escape("Using one AI output to verify another does not add reliability — both could share the same underlying hallucination from the same audio source. Personal notes, manually reviewed transcripts, and follow-up emails are independent sources that provide genuine verification.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C2_ID}_q3', '{C2_ID}', 'mcq', 3,
  'The best format for a CRM activity note after a client call is:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Factual, present-tense bullets with confirmed commitments and clear next steps"},{"label":"B","text":"A narrative paragraph that captures the tone and energy of the conversation"},{"label":"C","text":"The full Copilot transcript pasted verbatim"},{"label":"D","text":"A forward-looking interpretation of what the client probably wants next"}]))}',
  'A',
  '{escape("CRM notes are corporate memory. They should be factual, structured, and based only on what was confirmed — not speculative or narrative. A colleague or future RM reading the note should be able to understand the client'\''s situation and next steps without having been on the call.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C2_ID}_q4', '{C2_ID}', 'performance_task', 4,
  'The following AI-generated recap contains errors. Identify all errors and rewrite it as a corrected, CRM-ready activity note.',
  '{escape("AI Recap: Call with Eastport Composites Ltd. — Jan 9, 2025. Attendees: Priya Nair (RM), Daniel Osei (CEO). Daniel confirmed they are closing a $5M export contract with a US buyer this quarter. He committed to sending the signed term sheet by Jan 13. The company wants to explore BCAP and PRI immediately. Follow-up call scheduled for Jan 16.\n\nPriya'\''s notes: Daniel = CFO not CEO. $5M contract still in negotiation, not confirmed. He said he might send term sheet — no date given. Interested in BCAP, PRI is new to him and he asked for more info. Follow-up call TBD.")}',
  NULL, NULL, NULL,
  '{escape(json.dumps({"errors_identified": 1, "corrections_accurate": 1, "crm_ready_format": 1, "explanation_provided": 1}))}'
)
""")
print("Seeded Course 2: Recap, Review, Then Log")

# COMMAND ----------
# Course 3 — The C3 Line: What Goes Into AI and What Doesn't

C3_ID = "rm_c3_data_safety"

sql(f"""
INSERT INTO {CATALOG}.content.courses
  (course_id, role_id, primary_domain, title, tagline, description, real_use_case, sequence_order)
VALUES (
  '{C3_ID}', 'rm', 'data_safety',
  'The C3 Line: What Goes Into AI and What Doesn''t',
  'Apply the public/non-public test before any C3 data touches an AI prompt.',
  '{escape("EDC'\''s GenAI policy requires that non-public client information never be input into unapproved AI tools. For RMs, this means C3 data — credit figures, deal terms, NPS scores, relationship notes — must be abstracted before use. This course makes the public/non-public test automatic.")}',
  '{escape("Non-public client data into MS Copilot on the Web (FinDev Canada use case); Access to Copilot 365 for Business Development C3 extraction tension (Mid Market)")}',
  3
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.reading_content
  (content_id, course_id, concept_text, good_example, anti_pattern, takeaway)
VALUES (
  'rc_{C3_ID}', '{C3_ID}',
  '{escape("EDC'\''s GenAI governance policy draws a clear line: do not input non-public information into AI tools that are not approved to handle it. For RMs, the risk is real and specific — C3 contains confidential client data that clients share with EDC in confidence.\n\n**What counts as non-public information:**\n- Client credit facility amounts and terms\n- Deal structures, pricing, and transaction specifics\n- Client expansion plans mentioned in confidence\n- NPS scores and relationship health data\n- Verbatim CRM notes and relationship observations\n- Any client identifier combined with financial data\n\n**The public/non-public test:**\nBefore including any data in an AI prompt, ask: '\''Could this information appear in a press release without causing a compliance issue?'\'' If the answer is no — or even '\''maybe'\'' — abstract it first.\n\n**The abstraction technique:**\n- Replace client names with roles: '\''a mid-market manufacturing client in Ontario'\''\n- Round or range-ize figures: '\''$2.8M'\'' becomes '\''approximately $2–3M'\'' or '\''a mid-size facility'\''\n- Replace deal-specific dates with quarters: '\''expired September 2024'\'' becomes '\''expired in Q3 2024'\''\n- Remove relationship observations that identify the client relationship: '\''exploring alternatives due to pricing'\'' becomes '\''a client whose facility expired and has not renewed'\''")}',
  '{escape("Original prompt (unsafe): '\''Maple Industries Ltd. has a $4.5M BCAP facility expiring March 2025. Write a renewal outreach email.'\''\n\nSafe version: '\''One of my mid-market manufacturing clients in Ontario has an export finance facility expiring in Q1 2025. Write a renewal outreach email that emphasizes continuity of service and long-term relationship value. Format: 150 words, professional tone, no product-specific jargon.'\''\n\nWhy it works: The AI can write a perfectly useful, personalized-feeling email without knowing the client name, the exact amount, or the product type. The RM then personalizes manually before sending.")}',
  '{escape("An RM copied the full C3 client profile — company name, credit facility amount, deal history, NPS score, and relationship notes — and pasted it into Copilot on the Web with the prompt: '\''Write me an account strategy for this client.'\'' The output was useful, but the method put confidential client data into an unapproved AI surface. This is a direct violation of EDC'\''s GenAI policy, regardless of whether the output was ever used.")}',
  '{escape("Before hitting send on any AI prompt, ask: '\''Could this information appear in a press release?'\'' If not, abstract it first. The prompt can still be useful — often more so — without the specific details.")}'
)
""")

C3_COACH = escape(
    "You are an AI coach for 'The C3 Line', a course on data safety and GenAI compliance "
    "for Relationship Managers at a Canadian export finance institution.\n\n"
    "In this session the learner is practicing the public/non-public test and the abstraction "
    "technique using a C3 portfolio export scenario. The scenario involves 10 lapsed "
    "manufacturing clients. The non-public fields in this scenario are: company name "
    "(identifies the client), specific facility amounts, verbatim relationship notes. "
    "Last contact date and expiry date are borderline — they can be abstracted to quarters.\n\n"
    "Your coaching guidelines:\n"
    "- CRITICAL: If the learner includes any specific client name, exact facility amount, "
    "or verbatim relationship notes in a prompt, immediately flag: 'I notice your prompt "
    "includes [item]. This looks like non-public client information — what would a safe "
    "abstraction look like?'\n"
    "- For Task 1: guide toward the press release test — would this field appear publicly "
    "without issue?\n"
    "- For Task 2: coach toward replacing specifics with categories or ranges.\n"
    "- For Task 3: accept any prompt using abstracted data; as a bonus, coach toward CRAF "
    "structure.\n"
    "- For Task 4: NPS scores are non-public relationship health data — accept any "
    "explanation that reaches this conclusion. Ask: 'Would a client expect their NPS score "
    "to appear in a press release?'\n"
    "- Keep responses under 100 words."
)

sql(f"""
INSERT INTO {CATALOG}.content.practice_scenarios
  (scenario_id, course_id, scenario_text, task_1_text, task_2_text, task_3_text, task_4_text, coach_system_prompt)
VALUES (
  'ps_{C3_ID}', '{C3_ID}',
  '{escape("You are preparing a portfolio analysis and re-engagement campaign for 10 lapsed clients in the manufacturing sector. You exported the following fields from C3 for each client: company name, last contact date, facility type, facility amount, facility expiry date, and a notes field containing your relationship observations (e.g., '\''exploring alternatives due to pricing,'\'' '\''internal decision to pause,'\'' '\''went with competitor'\'').\n\nYou want to use Copilot to (1) identify which clients to prioritize for outreach and (2) draft an outreach email template for each priority segment.")}',
  '{escape("Review the C3 data fields listed in the scenario: company name, last contact date, facility type, facility amount, expiry date, and relationship notes. Which fields are non-public and must not go into an AI prompt as-is? Explain your reasoning for each field.")}',
  '{escape("One client entry reads: '\''Cedar Valley Foods Ltd. — last contact Mar 2024, BCAP, $3.1M, expired Jun 2024, notes: pricing concerns.'\'' Write an abstracted version of this entry that you could safely include in an AI prompt. What do you change and why?")}',
  '{escape("Using your abstracted version from Task 2, write a safe Copilot prompt asking it to draft a re-engagement email for this client type. Your prompt should not include any non-public information.")}',
  '{escape("A colleague argues that they can include a client'\''s NPS score (e.g., '\''NPS: 6'\'') in a Copilot prompt since '\''it'\''s just a number — no names attached.'\'' How do you respond? Is an NPS score public or non-public information?")}',
  '{C3_COACH}'
)
""")

# Evaluation items — Course 3
sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C3_ID}_q1', '{C3_ID}', 'mcq', 1,
  'You want to use Copilot to draft an outreach email for a client whose $3.2M facility is expiring. The safest approach is:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Describe the client as '\''a mid-market client with a facility expiring this quarter'\'' without naming the amount or client"},{"label":"B","text":"Include the exact facility amount so Copilot can write a more specific email"},{"label":"C","text":"Include the client name but not the facility amount"},{"label":"D","text":"Only use Copilot if the client has given verbal consent to share their data"}]))}',
  'A',
  '{escape("The safest prompt removes both the client identifier and the specific financial detail. The email can still be useful and personalized without these — Copilot does not need the exact figure to write an effective renewal message. Option C still identifies the client, which is non-public in combination with any relationship context.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C3_ID}_q2', '{C3_ID}', 'mcq', 2,
  'Which of the following C3 data fields is safe to include in a Copilot prompt without abstraction?',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"The client'\''s industry sector (e.g., '\''food processing'\'')"},{"label":"B","text":"The client'\''s exact credit facility amount"},{"label":"C","text":"A verbatim copy of your CRM relationship notes"},{"label":"D","text":"The client'\''s full legal name as it appears in C3"}]))}',
  'A',
  '{escape("Industry sector is typically publicly available information and does not identify the specific client or reveal confidential deal terms. The other options are all non-public: facility amount reveals deal terms, relationship notes are confidential observations, and the client'\''s name combined with any relationship context is identifying.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C3_ID}_q3', '{C3_ID}', 'mcq', 3,
  'The "press release test" for AI prompts means:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Only include information that could appear in a public press release without causing a compliance issue"},{"label":"B","text":"Ask your manager to review every AI prompt before you submit it"},{"label":"C","text":"Only use AI tools that are approved by the communications department"},{"label":"D","text":"Draft a press release first, then use it as context for your AI prompt"}]))}',
  'A',
  '{escape("The press release test is a quick mental check: if the information couldn'\''t appear publicly without causing a compliance or confidentiality issue, it shouldn'\''t go into an AI prompt. It'\''s a fast, practical way to apply the public/non-public rule in real-time without needing to consult a policy document.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C3_ID}_q4', '{C3_ID}', 'performance_task', 4,
  'Rewrite the following prompt so it is safe to use in Copilot. Remove or abstract all non-public information while keeping the prompt useful and specific enough to produce a usable email.',
  '{escape("Original prompt: '\''I need to re-engage Cedar Valley Foods Ltd., a food processing company in Manitoba. They had a $2.8M BCAP facility that expired in September 2024. My CRM notes say they are exploring other lenders due to pricing concerns. Write me a re-engagement email that addresses pricing objections and emphasizes EDC'\''s long-term partnership value.'\''")}',
  NULL, NULL, NULL,
  '{escape(json.dumps({"npi_removed": 1, "utility_preserved": 1, "prompt_functional": 1, "no_compliance_violation": 1}))}'
)
""")
print("Seeded Course 3: The C3 Line")

# COMMAND ----------
# Course 4 — Your Monday Morning Copilot Reset

C4_ID = "rm_c4_tool_fluency"

sql(f"""
INSERT INTO {CATALOG}.content.courses
  (course_id, role_id, primary_domain, title, tagline, description, real_use_case, sequence_order)
VALUES (
  '{C4_ID}', 'rm', 'tool_fluency',
  'Your Monday Morning Copilot Reset',
  'Match the right M365 Copilot surface to the right task and chain them into a workflow.',
  '{escape("M365 Copilot is available across Teams, Outlook, Excel, and Word — but the right surface for each task is not obvious. This course teaches RMs which tool to reach for first and how to chain outputs across surfaces into a complete Monday morning workflow: from missed call to briefing note to follow-up email.")}',
  '{escape("Business Enablement — Frontline Copilot Use Case Generation (explicitly names RMs and UWs); Request for Leadership from Small Business National Accounts; Meeting Recap; Record Governance")}',
  4
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.reading_content
  (content_id, course_id, concept_text, good_example, anti_pattern, takeaway)
VALUES (
  'rc_{C4_ID}', '{C4_ID}',
  '{escape("M365 Copilot is embedded across the tools you already use every day. The key skill is knowing which surface to reach for — and in what order.\n\n**Teams Copilot** — best for:\n- Summarizing meetings you attended or missed\n- Extracting action items and key decisions from transcripts\n- Getting a quick briefing on a long call\n\n**Outlook Copilot** — best for:\n- Drafting and replying to emails\n- Summarizing long email threads\n- Generating follow-up messages with clear next steps\n\n**Excel Copilot** — best for:\n- Analyzing exported data (pipeline, portfolio, prospect lists)\n- Identifying patterns, outliers, and priorities in structured data\n- Creating summaries and pivot-style insights from a dataset\n\n**Word / SharePoint Copilot** — best for:\n- Structuring unstructured content into a document format\n- Drafting briefing notes, one-pagers, and summaries from scratch\n- Turning a set of bullets into a polished narrative\n\n**Multi-step workflow principle:**\nOutput from one surface becomes the input for the next. A standard RM Monday workflow: Teams recap (extract information) → Word briefing note (structure it) → Outlook draft (communicate it). Each step takes approximately 2–3 minutes instead of 8–10.")}',
  '{escape("Monday morning, 8:45am. Jordan had a missed Friday call from Eastport Composites Ltd.:\n(1) Teams Copilot: '\''Summarize the missed call from Eastport Composites on Friday. List: key topics discussed, any commitments made by either party, and suggested next steps.'\'' — 2 min\n(2) Word Copilot: Pasted the summary. '\''Structure this as a one-page briefing note with sections: Client Context, Discussion Summary, Commitments, and My Recommended Next Step.'\'' — 3 min\n(3) Outlook Copilot: '\''Using the attached briefing note as context, draft a follow-up email to the CFO at Eastport Composites. Tone: professional and relationship-focused. Include: acknowledgement of the call, a clear next step with a proposed timeline, and an offer to connect this week.'\'' — 2 min\nTotal: 7 minutes. Jordan was fully caught up and had an outbound email ready before 9am.")}',
  '{escape("Jordan tried to use Outlook Copilot to summarize a Teams meeting he missed. Outlook doesn'\''t have access to Teams transcripts — it returned a generic message. He then tried to forward the Teams meeting invite to himself and ask Copilot to summarize the '\''attached meeting'\'' — no transcript, so it failed again. He ended up typing the recap manually from memory. The correct starting point was Teams Copilot, which has direct transcript access. Using the wrong surface for the input type means starting over.")}',
  '{escape("Match the tool to the input type: audio and transcripts belong in Teams; email threads belong in Outlook; spreadsheet data belongs in Excel; document drafting belongs in Word. Chain them in sequence — each step'\''s output is the next step'\''s input.")}'
)
""")

C4_COACH = escape(
    "You are an AI coach for 'Your Monday Morning Copilot Reset', a course on M365 Copilot "
    "tool selection and multi-step workflows for Relationship Managers at EDC.\n\n"
    "The learner is working through a Monday morning scenario involving: a missed Teams call "
    "from Eastport Composites Ltd., unanswered emails from Lakewood Tech Solutions, a pipeline "
    "review due to their manager, and a follow-up call to schedule.\n\n"
    "Your coaching guidelines:\n"
    "- When a learner chooses a wrong surface (e.g., Outlook to summarize a Teams call), ask: "
    "'What type of input does Copilot need for this task — a transcript, an email thread, or "
    "a document? Is that input available in Outlook?'\n"
    "- When a learner jumps between surfaces without explaining the handoff, ask: 'What are "
    "you bringing from the previous step into this one? What is the input for this step?'\n"
    "- For Task 4 (workflow description): probe for: what each step produces, what format "
    "the output is in, and how it feeds the next step.\n"
    "- Reinforce correct choices: explain briefly why that surface is the right one.\n"
    "- If a learner designs an efficient sequence, ask: 'What would you do if one step "
    "produced poor output — how would you recover?'\n"
    "- Do not prescribe the exact sequence — let the learner reason through it.\n"
    "- Keep responses under 100 words."
)

sql(f"""
INSERT INTO {CATALOG}.content.practice_scenarios
  (scenario_id, course_id, scenario_text, task_1_text, task_2_text, task_3_text, task_4_text, coach_system_prompt)
VALUES (
  'ps_{C4_ID}', '{C4_ID}',
  '{escape("It is Monday morning. You have four things to handle before noon:\n\n1. A missed Teams call from Friday afternoon with Eastport Composites Ltd. (CFO: Priya Nair) about a potential BCAP renewal — you were not on the call but the transcript is available in Teams.\n2. An unanswered email thread with Lakewood Tech Solutions (3 messages) about their upcoming US trade mission and how EDC can support them.\n3. A pipeline review report due to your manager by noon.\n4. A follow-up call to schedule with Eastport Composites based on whatever came up in the Friday call.\n\nYou have one hour. Use M365 Copilot across the right surfaces.")}',
  '{escape("For the missed Teams call with Eastport Composites, which M365 Copilot surface should you use first? Write the prompt you would use to extract the key discussion points and any commitments from the call.")}',
  '{escape("You now have a Teams Copilot summary of the Eastport call. Your manager has asked for a structured one-page briefing on this client before your noon pipeline review. Which Copilot surface would you use for this, and what prompt would you write?")}',
  '{escape("Draft the Outlook Copilot prompt you would use to reply to the Lakewood Tech Solutions email thread. Your reply should: acknowledge their trade mission timeline, propose a 20-minute call to discuss EDC support options, and confirm you will send relevant product information before the call.")}',
  '{escape("Describe your complete Monday morning Copilot workflow as a sequence. For each step, specify: (1) which M365 surface you use, (2) what you give it as input, (3) what output it produces, and (4) how that output feeds your next step. The workflow should cover all four Monday tasks.")}',
  '{C4_COACH}'
)
""")

# Evaluation items — Course 4
sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C4_ID}_q1', '{C4_ID}', 'mcq', 1,
  'You need to catch up on a 45-minute Teams meeting that happened while you were with another client. The meeting transcript is available. Which Copilot surface should you use?',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Teams Copilot — it has direct access to the meeting transcript"},{"label":"B","text":"Outlook Copilot — search for a follow-up email summarizing the meeting"},{"label":"C","text":"Word Copilot — paste the transcript text and ask for a summary"},{"label":"D","text":"Excel Copilot — structured data extraction works best for long meetings"}]))}',
  'A',
  '{escape("Teams Copilot is the only M365 surface with native access to Teams meeting transcripts. It can generate a summary, extract action items, and identify key decisions in seconds — without you manually copying or pasting anything. Outlook has no access to Teams transcripts, and Word/Excel Copilot would require manual effort to get the transcript in.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C4_ID}_q2', '{C4_ID}', 'mcq', 2,
  'You have a Copilot-generated meeting summary and want to turn it into a one-page structured briefing note for your manager. The best next step is:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Open Word and use Word Copilot to structure the summary into a briefing note format"},{"label":"B","text":"Email the summary to yourself and use Outlook Copilot to reformat it"},{"label":"C","text":"Paste it back into Teams chat and ask Teams Copilot to add headings"},{"label":"D","text":"Log it directly into C3 — a meeting summary is already a usable format"}]))}',
  'A',
  '{escape("Word Copilot is the right surface for document structuring and drafting. It can take unstructured text (a meeting summary) and reformat it into a professional briefing note with headings, sections, and consistent structure. Outlook is for email; Teams is for meeting data; C3 is for CRM logs — none of these are designed for document formatting.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C4_ID}_q3', '{C4_ID}', 'mcq', 3,
  'In a multi-step Copilot workflow, the correct sequence for going from a missed Teams call to a follow-up email is:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Teams Copilot (recap) → Word Copilot (briefing note) → Outlook Copilot (draft email)"},{"label":"B","text":"Outlook Copilot (summarize) → Word Copilot (structure) → Teams Copilot (send)"},{"label":"C","text":"Excel Copilot (analyze) → Teams Copilot (share) → Outlook Copilot (draft)"},{"label":"D","text":"SharePoint Copilot (search) → Teams Copilot (recap) → Word Copilot (summarize)"}]))}',
  'A',
  '{escape("The input type drives the starting surface: a Teams transcript starts in Teams. Structuring content into a document is Word'\''s strength. Drafting outbound communication is Outlook'\''s strength. The sequence follows the natural flow: extract information → structure it → communicate it.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C4_ID}_q4', '{C4_ID}', 'performance_task', 4,
  'Describe a complete three-step M365 Copilot workflow for the following scenario.',
  '{escape("You missed a Friday Teams call with a client about renewing their trade finance facility. The transcript is available in Teams. By noon on Monday you need to: (1) understand what was discussed and any commitments made, (2) prepare a one-page summary for your manager, and (3) send the client a follow-up email with clear next steps.\n\nFor each step, specify: which M365 Copilot surface you use, what prompt you write, and what the output is.")}',
  NULL, NULL, NULL,
  '{escape(json.dumps({"correct_tools_named": 1, "logical_sequence": 1, "handoff_between_steps": 1, "output_format_practical": 1}))}'
)
""")
print("Seeded Course 4: Your Monday Morning Copilot Reset")

# COMMAND ----------
# Course 5 — Win-Back and Portfolio Intelligence: AI for Pipeline Decisions

C5_ID = "rm_c5_capstone"

sql(f"""
INSERT INTO {CATALOG}.content.courses
  (course_id, role_id, primary_domain, title, tagline, description, real_use_case, sequence_order)
VALUES (
  '{C5_ID}', 'rm', 'prompting',
  'Win-Back and Portfolio Intelligence: AI for Pipeline Decisions',
  'Run an end-to-end AI-assisted win-back program: abstract, analyze, draft, verify.',
  '{escape("The capstone course integrates all four RM AI skill domains in a realistic win-back program scenario. Learners must abstract C3 data before analysis, choose the right Copilot surfaces, write CRAF prompts for outreach, and verify AI output before it reaches a client — all in the correct sequence.")}',
  '{escape("Access to Copilot 365 for Business Development — explicit C3 export and Excel win-back scenario (Mid Market); Automating Prospect Profiling; Sector Opportunity Identification Agent")}',
  5
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.reading_content
  (content_id, course_id, concept_text, good_example, anti_pattern, takeaway)
VALUES (
  'rc_{C5_ID}', '{C5_ID}',
  '{escape("A win-back program starts with data from C3 — lapsed clients, facility types, expiry dates, last contact records. The challenge: that data is non-public and cannot go directly into any AI tool that isn'\''t approved for confidential data.\n\n**The safe win-back workflow — in this exact order:**\n\n1. **Abstract first**: Replace client names with roles (e.g., '\''mid-market food processor'\''), round figures to ranges, replace specific dates with quarters, remove verbatim relationship notes.\n\n2. **Analyze with Excel Copilot**: Upload the abstracted dataset. Ask Excel Copilot to identify segments with the highest concentration of expiring facilities, patterns in lapse reasons, or priority tiers by approximate facility size.\n\n3. **Structure insights with Word Copilot**: Turn the Excel analysis into a targeting brief or prioritization summary.\n\n4. **Draft outreach with Outlook Copilot**: Write a CRAF prompt for each priority segment. Use abstracted client descriptions, not real names or figures.\n\n5. **Verify before sending**: Check all output against your own records. Delete any figure or claim you did not provide — AI will sometimes invent plausible-sounding details about clients it knows nothing about.\n\nAt every step: no raw C3 data, no real client names, no unverified figures in anything that leaves your drafts folder.")}',
  '{escape("Jordan ran a win-back program for 15 lapsed manufacturing clients:\n(1) Abstracted the C3 export: removed names, rounded amounts to size categories (small/mid/large), replaced specific dates with quarters, generalized notes to '\''pricing'\'' or '\''competitive loss'\'' or '\''internal pause'\''. — 10 min\n(2) Excel Copilot on abstracted data: '\''Analyze this dataset of lapsed clients. Identify which facility type and size category has the highest concentration of Q3-Q4 2024 expirations. Rank by win-back likelihood based on lapse reason.'\'' — 3 min\n(3) Outlook CRAF prompt: '\''Context: mid-market food processing clients whose BCAP facility expired in the last 6 months due to pricing. Role: you are a senior RM at a Canadian export finance institution. Action: draft a re-engagement email that acknowledges it'\''s been a while, references the value of BCAP without naming pricing. Format: 120 words, warm but professional.'\''\n(4) Verified output: deleted one claim about '\''current market rates'\'' that Jordan never provided — likely hallucinated. Personalized each email manually before sending. — 5 min")}',
  '{escape("An RM exported the full C3 portfolio list — real client names, exact facility amounts, NPS scores, relationship notes — directly into Excel and uploaded it to Copilot Chat for analysis. The output was accurate and useful. But the method put confidential client data into an unapproved AI surface. Regardless of the output quality, this is a policy violation. The analysis should be redone on an abstracted dataset.")}',
  '{escape("The sequence matters as much as the tools: abstract first, then analyze, then draft, then verify. Skipping abstraction or verifying last are the two most common compliance and quality failures in AI-assisted portfolio work.")}'
)
""")

C5_COACH = escape(
    "You are an AI coach for 'Win-Back and Portfolio Intelligence', the capstone course "
    "integrating all four RM AI skill domains: data safety, prompting, tool fluency, and "
    "verification.\n\n"
    "In this session the learner is running a simulated win-back program for 10 lapsed "
    "manufacturing clients. This is the most complex scenario in the training — learners "
    "must apply all four disciplines in the correct sequence.\n\n"
    "Your coaching guidelines:\n"
    "- DATA SAFETY (Tasks 1 and 3): If any specific client name or exact financial figure "
    "appears in a prompt, flag immediately: 'I notice your prompt includes [item]. This "
    "looks like non-public client data. What would a safe abstraction look like?'\n"
    "- PROMPTING (Tasks 2 and 3): Coach toward CRAF structure. Ask which element is "
    "missing if the prompt is weak.\n"
    "- TOOL FLUENCY (Task 2): If the learner chooses the wrong surface for data analysis, "
    "ask: 'Which Copilot surface is designed to work with structured spreadsheet data?'\n"
    "- VERIFICATION (Task 4): Do not reveal that the rate claim was hallucinated. Ask: "
    "'Where did this rate information come from? Can you verify it in your own records or "
    "notes?'\n"
    "- INTEGRATION: Refer back to earlier tasks: 'You abstracted well in Task 1 — apply "
    "that same discipline here in Task 3.'\n"
    "- This is a capstone — learners should apply prior courses independently. Reduce "
    "hints compared to earlier courses.\n"
    "- Keep responses under 120 words."
)

sql(f"""
INSERT INTO {CATALOG}.content.practice_scenarios
  (scenario_id, course_id, scenario_text, task_1_text, task_2_text, task_3_text, task_4_text, coach_system_prompt)
VALUES (
  'ps_{C5_ID}', '{C5_ID}',
  '{escape("You are running a Q1 win-back program for 10 lapsed manufacturing sector clients. Your C3 export contains the following fields for each client: company name, last contact date, facility type (BCAP or Export Guarantee), approximate facility amount, facility expiry date, and a notes field with the reason for lapse (e.g., '\''pricing concerns,'\'' '\''went with competitor,'\'' '\''internal decision to pause'\'').\n\nYour goal: use AI to (1) identify your top 3 priority targets and (2) draft re-engagement emails for each priority segment.")}',
  '{escape("Before using any AI tool, you need to abstract the C3 data. Write the abstracted version of this one client record: '\''Cedar Valley Foods Ltd. — last contact Mar 2024, BCAP, $3.1M, expired Jun 2024, notes: pricing concerns.'\'' What fields do you change, what do you change them to, and why?")}',
  '{escape("Using only abstracted data, write an Excel Copilot prompt to analyze the dataset of 10 lapsed clients and identify which segments (by facility type and approximate size category) represent the highest win-back priority. Your prompt should not include any real client names or exact dollar amounts.")}',
  '{escape("Write a complete CRAF prompt to draft a re-engagement email for your top priority segment: mid-market manufacturers whose BCAP facility expired in Q2–Q3 2024 due to pricing concerns. Do not include any real client information in your prompt.")}',
  '{escape("Copilot drafted a re-engagement email that includes this sentence: '\''Your facility was renewed at a rate of 3.2%, significantly below the market average of 4.1% at the time.'\'' You never provided any rate information in your prompt. What do you do before sending this email, and why?")}',
  '{C5_COACH}'
)
""")

# Evaluation items — Course 5
sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C5_ID}_q1', '{C5_ID}', 'mcq', 1,
  'Before using AI to analyze a C3 export for a win-back program, the first step is:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Abstract all non-public fields — remove client names, round amounts, generalize sectors"},{"label":"B","text":"Ask your manager for permission to upload the C3 data to Copilot"},{"label":"C","text":"Use only the last contact date field since dates are not confidential"},{"label":"D","text":"Run the analysis first, then redact sensitive output before sharing it"}]))}',
  'A',
  '{escape("Abstraction must happen before any AI tool receives the data. Running the analysis first and redacting later does not fix the policy violation — the non-public data has already been processed by an unapproved surface. Option C is insufficient: last contact date combined with facility type can still identify a client in context.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C5_ID}_q2', '{C5_ID}', 'mcq', 2,
  'A Copilot-generated outreach email includes a specific claim about a client interest rate that you never provided in your prompt. What should you do?',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Delete the claim — it is likely hallucinated since you never provided that data"},{"label":"B","text":"Keep the claim — Copilot probably accessed current market rate data"},{"label":"C","text":"Call the client first to confirm whether the rate is accurate"},{"label":"D","text":"Add a disclaimer saying the rate is approximate before sending"}]))}',
  'A',
  '{escape("If you did not provide the rate data, the AI invented it. AI models do not have access to private client records — any specific figure that appears without being in the prompt is a hallucination. Sending a hallucinated financial claim to a client is both inaccurate and a compliance risk. Delete it and replace with a verified or general statement.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C5_ID}_q3', '{C5_ID}', 'mcq', 3,
  'In a multi-step win-back workflow, the correct sequence is:',
  NULL,
  '{escape(json.dumps([{"label":"A","text":"Abstract C3 data → analyze with Excel Copilot → draft with Outlook Copilot → verify before sending"},{"label":"B","text":"Draft with Outlook Copilot → analyze with Excel → abstract data → verify and send"},{"label":"C","text":"Export raw C3 data → summarize with Teams Copilot → draft with Outlook → send"},{"label":"D","text":"Verify first → abstract → draft outreach → analyze results"}]))}',
  'A',
  '{escape("Data safety comes first (abstract), then analysis (Excel), then communication drafting (Outlook), then verification before anything goes to a client. Running steps out of order — especially drafting before abstracting or sending before verifying — creates compliance and quality risks that are difficult to reverse.")}',
  '{escape(json.dumps({"correct": 4, "incorrect": 0}))}'
)
""")

sql(f"""
INSERT INTO {CATALOG}.content.evaluation_items
  (item_id, course_id, item_type, sequence, question_text, scenario_text, options, correct_option, explanation, scoring_rubric)
VALUES (
  'ev_{C5_ID}_q4', '{C5_ID}', 'performance_task', 4,
  'Describe your complete AI-assisted win-back workflow for the scenario below.',
  '{escape("You have a C3 export of 8 lapsed clients in the food processing sector. You want to identify your top 3 priority targets and draft a personalized re-engagement email for each priority segment.\n\nFor each step of your workflow, describe: (1) which tool or Copilot surface you use, (2) what data preparation you perform before using it, (3) what prompt you write, and (4) what verification you perform before acting on the output.\n\nYour workflow must address all four RM AI skill domains: data safety, prompting structure, tool selection, and output verification.")}',
  NULL, NULL, NULL,
  '{escape(json.dumps({"data_safety_applied": 1, "craf_structure_present": 1, "correct_tool_sequence": 1, "verification_step_included": 1}))}'
)
""")
print("Seeded Course 5: Win-Back and Portfolio Intelligence")

# COMMAND ----------

print("\n✓ All 5 courses seeded successfully.")
print("\nVerification queries:")
print(f"  SELECT course_id, title FROM {CATALOG}.content.courses ORDER BY sequence_order;")
print(f"  SELECT count(*) FROM {CATALOG}.content.evaluation_items;  -- expect 20")
print(f"  SELECT count(*) FROM {CATALOG}.content.reading_content;   -- expect 5")
print(f"  SELECT count(*) FROM {CATALOG}.content.practice_scenarios; -- expect 5")
dbutils.notebook.exit("SUCCESS: All 5 courses seeded")
