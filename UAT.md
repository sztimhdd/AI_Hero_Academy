# UAT.md — AI Hero Academy MVP
## End-to-End User Acceptance Testing Specification
**Version**: 1.0 | March 2026

---

## Purpose

This document is the authoritative test specification for the AI Hero Academy MVP UAT. It is intended to be read and executed by a dedicated **Claude Code UAT Agent** using the Playwright MCP browser control tools and the Databricks MCP SQL execution tool against a locally running instance of the app.

---

## 1. Agent Instructions

### 1.1 Tools Required

| Tool | Purpose |
|------|---------|
| `mcp__playwright__browser_navigate` | Open URLs |
| `mcp__playwright__browser_snapshot` | Capture accessibility tree (use for all element discovery) |
| `mcp__playwright__browser_click` | Click elements by `ref` from snapshot |
| `mcp__playwright__browser_type` | Type text into inputs by `ref` |
| `mcp__playwright__browser_select_option` | Select dropdown values |
| `mcp__playwright__browser_wait_for` | Wait for text to appear or disappear |
| `mcp__playwright__browser_take_screenshot` | Capture screenshot on failure |
| `mcp__playwright__browser_scroll` | Scroll to reveal content |
| `mcp__playwright__browser_press_key` | Send keyboard events (e.g., Enter) |
| `mcp__databricks-mcp-server__execute_sql` | Run SQL to verify Delta writes |

### 1.2 How to Interact with Streamlit

Streamlit is a server-side-rendered app that rerenders the full DOM on every interaction. Follow this pattern for every interaction:

1. **Always call `browser_snapshot` first** to get the current accessibility tree and element refs
2. **Use the `ref` value** from the snapshot to target `browser_click` / `browser_type` — never guess refs
3. **After any click that should change UI state**, immediately call `browser_wait_for` with the text you expect to appear, OR `browser_wait_for textGone` if waiting for a loading indicator to disappear
4. **Re-snapshot after each rerender** before the next interaction — refs change on every Streamlit rerender

### 1.3 Handling Loading States

The app shows loading spinners during AI calls (scoring, gap map, coach responses). These can take 5–60 seconds depending on the call type.

```
Diagnostic scoring + gap map:   up to 60 seconds
Module evaluation scoring:      up to 45 seconds
AI coach response (one turn):   up to 15 seconds
Course creation (Build Course): up to 30 seconds
Page navigation/load:           up to 10 seconds
```

Pattern to wait for AI loading to complete:
```
browser_wait_for(textGone="Analyzing", timeout=60000)
browser_wait_for(textGone="Scoring", timeout=45000)
browser_wait_for(textGone="Building", timeout=30000)
```

If a loading state does not clear within the timeout: take a screenshot, mark the step as FAIL, and continue to the next scenario if possible.

### 1.4 Delta Verification Pattern

Use the Databricks MCP tool after critical writes to confirm data was persisted:

```
mcp__databricks-mcp-server__execute_sql(
  statement="SELECT ... FROM mdlg_ai_shared.learner.table WHERE user_email = 'uat-test@edc.ca'",
  warehouse_id="eaa098820703bf5f"
)
```

The test user email is defined in `.env` as `DEV_USER_EMAIL`. Default: `uat-test@edc.ca`.

### 1.5 AI Call Assertions

The app makes real LLM calls to Databricks Foundation Model endpoints. **Do NOT assert specific AI-generated text content** — it varies per call. Assert only:
- That the UI transitioned to the expected state (new heading, score visible, next section loaded)
- That structural elements appear (score is a number, gap map has bullets, coach replied)
- That data was written to Delta (via Delta Check SQL)

### 1.6 Failure Handling

If a step fails:
1. Call `browser_take_screenshot` immediately and note the filename
2. Log the failure as `[FAIL] UAT-NN: Step N — description of what was expected vs. what was seen`
3. Continue to the next scenario if the failure is not a blocking dependency
4. At the end, list all failures in a summary

### 1.7 Viewport

Set the viewport to 1280×800 before starting:
```
browser_resize(width=1280, height=800)
```

---

## 2. Pre-Test Setup

Run these commands in the project directory before starting the test suite:

```bash
# Step 1: Reset test user (wipes all Delta data for DEV_USER_EMAIL)
python scripts/reset_uat_user.py

# Step 2: Start the app (sources .env, starts Streamlit on port 8501)
bash run_uat.sh
```

Wait for the Streamlit server to print "You can now view your Streamlit app in your browser" before beginning.

**Verify app is running:**
```
browser_navigate(url="http://localhost:8501")
```
Expected: Welcome page loads (no redirect to login).

**Verify test user is clean (Delta check):**
```sql
SELECT COUNT(*) AS row_count FROM mdlg_ai_shared.learner.user_profiles
WHERE user_email = 'uat-test@edc.ca'
```
Expected: `row_count = 0`

---

## 3. Test Scenarios

---

### UAT-01: Welcome Page — New RM User Onboarding

**Purpose:** Verify a brand-new user can land on the Welcome page, select the Relationship Manager role, set a display name, and navigate to the Diagnostic.

**Pre-conditions:** Test user has no row in `learner.user_profiles` (confirmed by pre-test setup).

**Steps:**

1. Navigate to `http://localhost:8501`
2. Assert: Text "AI Hero Academy" is visible on the page
3. Assert: A role selector dropdown element is present
4. Assert: The "Start My Diagnostic" button (or equivalent CTA) is **disabled** (no role selected yet)
5. Select "Relationship Manager" from the role dropdown
6. Assert: The CTA button is now **enabled** (clickable)
7. Locate the display name input field
8. Clear any pre-filled text, then type: `UAT Tester RM`
9. Click "Start My Diagnostic" CTA button
10. Assert: The page transitions — Diagnostic content is visible (e.g., "Question 1 of 18" or orientation text appears)

**Delta Check — Verify profile was created:**
```sql
SELECT user_email, role_id, display_name
FROM mdlg_ai_shared.learner.user_profiles
WHERE user_email = 'uat-test@edc.ca'
```
✅ Expected: 1 row with `role_id = 'rm'` and `display_name = 'UAT Tester RM'`

---

### UAT-02: Diagnostic — Complete RM 18-Question Assessment

**Purpose:** Complete all 18 diagnostic questions across 6 domains and verify that AI scoring runs and produces a completed session with a gap map.

**Pre-conditions:** Follows UAT-01. User is on the Diagnostic page.

**Steps:**

1. Assert: An orientation screen is visible (contains text about the number of questions or time estimate)
2. Click the orientation CTA button to begin the diagnostic
3. For each question **N = 1 to 18**, repeat:
   a. Assert: A question counter text is visible (e.g., "Question N of 18" or "N / 18")
   b. Assert: A domain label/tag is visible on the question
   c. **If the question shows radio buttons (MCQ):**
      - Select the first radio option (option A)
      - Click "Next" button
   d. **If the question shows a text area (prompt sandbox or micro-task):**
      - Click into the text area
      - Type: `This is a UAT test response. I would structure my prompt with clear context about the client situation, specify the desired output format, include relevant constraints such as data safety rules, and ask for a specific deliverable.`
      - Click the "Submit" button
   e. Wait for the next question to appear before continuing
4. After submitting question 18:
   - Assert: A loading indicator or spinner appears (text like "Analyzing" or a spinner component)
   - Wait for loading to complete (`browser_wait_for textGone` on loading text, timeout: **60 seconds**)
5. Assert: The page has transitioned to the Skills Profile (text "Your AI Skills Profile" is visible, OR a numeric score is displayed)

**Delta Check — Verify diagnostic session was saved:**
```sql
SELECT session_id, overall_score, completed_at
FROM mdlg_ai_shared.learner.diagnostic_sessions
WHERE user_email = 'uat-test@edc.ca' AND completed_at IS NOT NULL
ORDER BY completed_at DESC LIMIT 1
```
✅ Expected: 1 row; `overall_score` is a decimal between 0.0 and 4.0; `completed_at` is not null

**Delta Check — Verify gap map was generated:**
```sql
SELECT gap_map_id, source_type, generated_at
FROM mdlg_ai_shared.learner.gap_maps
WHERE user_email = 'uat-test@edc.ca'
ORDER BY generated_at DESC LIMIT 1
```
✅ Expected: 1 row with `source_type = 'diagnostic'`

---

### UAT-03: Skills Profile — Scores, Gap Map, Build Course

**Purpose:** Verify the Skills Profile page renders domain scores, a gap map narrative, and assessment history; then confirm the "Build My Training Course" action creates 7 training progress records and navigates to Home.

**Pre-conditions:** Follows UAT-02. User is on the Skills Profile page.

**Steps:**

1. Assert: Heading "Your AI Skills Profile" is visible
2. Assert: An overall score value is visible (a decimal number)
3. Assert: A level label is visible and is one of: `Unaware`, `Explorer`, `Practitioner`, `Proficient`, `Champion`
4. Assert: Domain scores section is rendered (at least one domain name is visible with a score)
5. Assert: A section titled "Your Gap Map" or equivalent heading is present
6. Assert: At least **3 gap bullets** are visible under the gap map section
7. Assert: An assessment history section or table is visible with at least 1 data row
8. Assert: A "Build My Training Course" button is visible (course has not yet been built)
9. Assert: A "Retake Diagnostic" button is visible
10. Click "Build My Training Course"
11. Assert: A loading state appears (spinner or "Building" text)
12. Wait for loading to complete (timeout: **30 seconds**)
13. Assert: Page has navigated to the Home dashboard (text "Welcome back" is visible)

**Delta Check — Verify 7 training progress rows were created:**
```sql
SELECT course_id, module_sequence_order, is_locked
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca'
ORDER BY module_sequence_order
```
✅ Expected: **7 rows** total; the row with `module_sequence_order = 1` has `is_locked = false`; rows with `module_sequence_order = 2` through `7` have `is_locked = true`

---

### UAT-04: Home Dashboard — Module List and Lock State

**Purpose:** Verify the Home dashboard displays the personalized module list, with Module 1 unlocked and Modules 2–7 locked, and the summary card shows the user's score.

**Pre-conditions:** Follows UAT-03. User is on the Home page.

**Steps:**

1. Assert: A greeting with text "Welcome back" and the name "UAT Tester RM" is visible
2. Assert: A summary card shows a numeric overall score and a level label
3. Assert: Exactly **7 module cards** are listed (numbered 01 through 07)
4. Assert: Module 1 has an actionable CTA button (e.g., "Start Module", "Start Reading", or similar — not a lock icon or disabled state)
5. Assert: At least one of Modules 2–7 shows a locked state (lock icon, "locked" text, or a disabled/greyed appearance)
6. Assert: A link or button to "View Skills Profile" or "View Full Profile" is present in the summary card area

---

### UAT-05: Module 1 — Overview Sub-view

**Purpose:** Verify the Course Module overview sub-view renders the module title, step progress strip, and context-aware CTA before any sub-modules are completed.

**Pre-conditions:** Follows UAT-04. User is on the Home page.

**Steps:**

1. Click the CTA button on **Module 1** (the first unlocked module card)
2. Assert: A module number (e.g., "01") and module title text are visible
3. Assert: A step progress strip is visible showing at least the labels "Reading", "Practice", and "Quiz" (or equivalent abbreviations)
4. Assert: The primary CTA button text is "Start Reading" (or equivalent — reading has not yet been completed)
5. Note the module title text for reference in UAT-10 (to confirm Module 2 has a different title)

---

### UAT-06: Module 1 — Reading Sub-view

**Purpose:** Verify the reading content renders all required sections (concept, good example, common mistake, key takeaway) and marks reading complete on CTA click.

**Pre-conditions:** Follows UAT-05. User is on the Module 1 overview.

**Steps:**

1. Click the "Start Reading" CTA button
2. Assert: A reading content area is visible (at least one paragraph of text is present)
3. Assert: A "Good Example" section is visible — this will appear as a green/success styled box (`st.success`)
4. Assert: A "Common Mistake" section is visible — this will appear as a red/error styled box (`st.error`)
5. Assert: A "Key Takeaway" section is visible — this will appear as an info styled box (`st.info`) or a distinct callout
6. Scroll down to the bottom of the reading content
7. Assert: A CTA button with text resembling "I've read this" or "Start Practice" is visible at the bottom
8. Click the reading completion CTA button
9. Assert: The UI transitions to the Practice sub-view — a "Scenario" label or "Task 1 of 4" text becomes visible

**Delta Check — Verify reading completion was recorded:**
```sql
SELECT reading_completed_at
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca' AND module_sequence_order = 1
```
✅ Expected: `reading_completed_at` is not null

---

### UAT-07: Module 1 — Practice Sub-view (AI Coach)

**Purpose:** Verify the AI coach practice flow: the scenario panel renders, tasks advance sequentially, the coach responds to user input, and completing all 4 tasks enables the "Complete Practice" action.

**Pre-conditions:** Follows UAT-06. User is on the Practice sub-view.

**Steps:**

1. Assert: A "Scenario" label and scenario description text are visible at the top of the page
2. Assert: A "Task 1 of 4" indicator (or "Task 1") is visible
3. Assert: A text input or chat input field is present and interactable
4. Type into the input field: `I would start by reviewing the CRM notes and then craft a prompt with relevant context about the client's industry, recent interactions, and the specific output format I need from Copilot.`
5. Submit the response (click the submit button, or press Enter if it is a chat input)
6. Wait for the coach response to appear (timeout: **15 seconds**)
7. Assert: A coach reply message is visible in the conversation area (at least one message with the coach avatar or label)
8. Assert: A turn counter is visible (text like "Turn 1 of 15" or "Turn 2")
9. Locate and click the "Next Task" button (or equivalent advance button)
10. Assert: "Task 2 of 4" is now visible
11. Type into the input: `For this task, I would verify the AI-generated output against the original CRM data before sending it to the client, checking each factual claim against the source notes.`
12. Submit and wait for coach response (timeout: **15 seconds**)
13. Assert: Coach responds with a new message
14. Click "Next Task" to advance to Task 3
15. Assert: "Task 3 of 4" is visible
16. Type: `I would use only anonymized, fictional data in my Copilot prompts to comply with our data safety policy, keeping all real client information out of the AI tool.`
17. Submit and wait for coach response (timeout: **15 seconds**)
18. Assert: Coach responds
19. Click "Next Task" to advance to Task 4
20. Assert: "Task 4 of 4" is visible
21. Type: `For the final task, I would chain multiple Copilot steps: first generate a draft, then verify key facts, then refine the prompt to improve the output before using it in the final deliverable.`
22. Submit and wait for coach response (timeout: **15 seconds**)
23. Assert: Coach responds
24. Assert: A "Complete Practice" button (or equivalent) is now visible
25. Click "Complete Practice"
26. Assert: The UI transitions to the Evaluation sub-view (quiz questions appear, e.g., "Question 1 of 4" or "Quiz" heading)

**Delta Check — Verify coach session was saved:**
```sql
SELECT session_id, turn_count, completed_at
FROM mdlg_ai_shared.learner.coach_sessions
WHERE user_email = 'uat-test@edc.ca'
ORDER BY started_at DESC LIMIT 1
```
✅ Expected: 1 row; `turn_count > 0`; `completed_at` is not null

**Delta Check — Verify practice completion was recorded:**
```sql
SELECT practice_completed_at
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca' AND module_sequence_order = 1
```
✅ Expected: `practice_completed_at` is not null

---

### UAT-08: Module 1 — Evaluation Quiz

**Purpose:** Verify the 4-question quiz (3 MCQ + 1 performance task) renders correctly, AI scoring runs after final submission, and the results sub-view is reached.

**Pre-conditions:** Follows UAT-07. User is on the Evaluation sub-view.

**Steps:**

1. Assert: A quiz header or question counter is visible (e.g., "Question 1 of 4" or "Quiz")
2. **For Question 1 (MCQ):**
   a. Assert: Radio button options are visible
   b. Select the first available radio option
   c. Click the "Next" button
   d. Wait for Question 2 to load
3. **For Question 2 (MCQ):**
   a. Assert: Radio button options are visible
   b. Select the first available radio option
   c. Click the "Next" button
   d. Wait for Question 3 to load
4. **For Question 3 (MCQ):**
   a. Assert: Radio button options are visible
   b. Select the first available radio option
   c. Click the "Next" button
   d. Wait for Question 4 to load
5. **For Question 4 (performance task):**
   a. Assert: A text input area is visible (not radio buttons)
   b. Type: `I would first identify the key claims in the AI-generated summary, then verify each one against the original source data in CRM and meeting notes. Only after confirming accuracy would I include the content in the client report, and I would add a note that the draft was AI-assisted and human-reviewed.`
   c. Click the final "Submit" button
6. Assert: A loading state appears ("Scoring" text or spinner visible)
7. Wait for loading to complete (timeout: **45 seconds**)
8. Assert: The Results sub-view is now displayed — a module score value is visible (a decimal number)

**Delta Check — Verify evaluation score was written:**
```sql
SELECT evaluation_score, evaluation_completed_at, domain_score_after
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca' AND module_sequence_order = 1
```
✅ Expected: `evaluation_score` is a decimal between 0.0 and 4.0; `evaluation_completed_at` is not null; `domain_score_after` is not null

**Delta Check — Verify Module 2 was unlocked:**
```sql
SELECT is_locked
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca' AND module_sequence_order = 2
```
✅ Expected: `is_locked = false`

**Delta Check — Verify a new gap map was generated post-evaluation:**
```sql
SELECT source_type, generated_at
FROM mdlg_ai_shared.learner.gap_maps
WHERE user_email = 'uat-test@edc.ca'
ORDER BY generated_at DESC LIMIT 1
```
✅ Expected: `source_type = 'evaluation'`

---

### UAT-09: Module 1 — Results Sub-view

**Purpose:** Verify the results page shows the module score, an AI-generated coach note, and navigation CTAs for proceeding to Module 2.

**Pre-conditions:** Follows UAT-08. User is on the Results sub-view.

**Steps:**

1. Assert: A module score is visible (a decimal number between 0.0 and 4.0)
2. Assert: A coach note / feedback text block is visible (a non-empty text paragraph — content will vary; assert it is not empty)
3. Assert: A CTA button to proceed to Module 2 is visible (text like "Start Module 2", "Next Module", or "Go to Module 2")
4. Click the "Start Module 2" CTA button
5. Assert: The Module 2 overview sub-view loads — a module title different from Module 1's title is visible, and the step progress strip shows all stages as "not started" or "pending"

---

### UAT-10: Module 2 — Unlock and Reading Start Verification

**Purpose:** Confirm Module 2 is properly unlocked, has distinct content from Module 1, and navigating back to Home correctly reflects Module 1 as completed.

**Pre-conditions:** Follows UAT-09. User is on Module 2 overview.

**Steps:**

1. Assert: Module 2's title text is different from the Module 1 title noted in UAT-05
2. Assert: The step progress strip shows Reading, Practice, and Quiz all as "not started" or "pending" (none completed yet)
3. Assert: The primary CTA button says "Start Reading" (or equivalent)
4. Click "Start Reading"
5. Assert: Reading content loads — concept text is visible (at least one paragraph)
6. Assert: The reading content text is visually different from Module 1's reading content (distinct topic)
7. Navigate back to the Home dashboard (use the sidebar navigation or "Back to Dashboard" link)
8. Assert: Module 1's card on the Home page shows a completed state — a score value is displayed next to or within the Module 1 card
9. Assert: Module 2's card on the Home page shows an active/in-progress state — it has a CTA button (not locked)
10. Assert: Modules 3–7 remain locked

---

### UAT-11: Skills Profile — Post-Training Score Update

**Purpose:** Verify that the Skills Profile page reflects updated domain scores after Module 1 evaluation, with the assessment history showing at least the initial diagnostic and the post-evaluation update.

**Pre-conditions:** Follows UAT-10.

**Steps:**

1. Navigate to the Skills Profile page (use sidebar link "Skills Profile" or the "View Full Skills Profile" link from Home)
2. Assert: "Your AI Skills Profile" heading is visible
3. Assert: The overall score value is visible
4. Assert: The assessment history section or table shows at least **2 rows** (the initial diagnostic row plus any subsequent update), OR — if the history only shows diagnostic rows — the domain scores reflect non-zero values consistent with prior evaluation updates
5. Assert: The gap map section still has bullets (at least 3 visible)

---

### UAT-12: Retake Diagnostic — Progress Preservation

**Purpose:** Verify that starting a diagnostic retake from the Skills Profile works correctly, and that navigating away without completing it does NOT wipe prior training progress.

**Pre-conditions:** Follows UAT-11. User is on the Skills Profile page.

**Steps:**

1. Assert: The "Retake Diagnostic" button is visible on the Skills Profile page
2. Click "Retake Diagnostic"
3. Assert: The Diagnostic page loads — an orientation screen or "Question 1 of 18" counter is visible
4. If on the orientation screen, click through to begin the diagnostic
5. Assert: Question 1 is visible with radio buttons or a text input
6. Answer Question 1 (select any radio option for MCQ, or type a short response for text input)
7. Assert: Question 2 loads (the question counter advances — confirms partial diagnostic works)
8. Navigate back to the Home page **without completing** the diagnostic (use sidebar navigation — click "Home")
9. Assert: The Home page shows Module 1 with a **completed** state and its score (prior progress was NOT wiped)
10. Assert: Module 2 still shows as **unlocked** (is_locked = false)

**Delta Check — Confirm training progress is still intact:**
```sql
SELECT evaluation_completed_at, evaluation_score
FROM mdlg_ai_shared.learner.training_progress
WHERE user_email = 'uat-test@edc.ca' AND module_sequence_order = 1
```
✅ Expected: `evaluation_completed_at` is still not null (progress was preserved despite retake attempt)

---

### UAT-13: UW Role Smoke Test — Welcome and Diagnostic Start

**Purpose:** Verify that the Underwriter role is selectable from the Welcome page and that a UW user can begin the diagnostic flow.

**Pre-conditions:** Run `python scripts/reset_uat_user.py` to wipe the test user before this scenario.

> **Note on test user email:** If only one `DEV_USER_EMAIL` is configured, reset the user between UAT-12 and UAT-13. The UW smoke test will overwrite the RM user data for the same email.

**Steps:**

1. Run `python scripts/reset_uat_user.py` to reset test user data
2. Navigate to `http://localhost:8501`
3. Assert: The Welcome page loads (no redirect to another page)
4. Assert: "AI Hero Academy" text is visible
5. Locate the role selector dropdown and open it (click or snapshot to reveal options)
6. Assert: **"Underwriter"** is present as a selectable option in the dropdown
7. Select "Underwriter" from the dropdown
8. Assert: The CTA button ("Start My Diagnostic") becomes enabled
9. Clear the display name field and type: `UAT Tester UW`
10. Click "Start My Diagnostic"
11. Assert: The Diagnostic page loads (question counter or orientation screen visible)
12. If on an orientation screen, click through to begin
13. Assert: Question 1 is visible with a domain label/tag
14. Note the domain label — it should reflect a UW domain (may be the same domain names as RM; the key check is that content loads without errors)
15. Answer Question 1 (select any radio option or type a short response)
16. Assert: Question 2 loads successfully (confirms UW diagnostic flow is functional)

**Delta Check — Verify UW profile was created:**
```sql
SELECT user_email, role_id, display_name
FROM mdlg_ai_shared.learner.user_profiles
WHERE user_email = 'uat-test@edc.ca'
```
✅ Expected: 1 row with `role_id = 'uw'` and `display_name = 'UAT Tester UW'`

---

## 4. Pass/Fail Criteria

### PASS — All of the following must be true:

- [ ] UAT-01 through UAT-12 completed without unhandled Python exceptions or error messages on the happy path
- [ ] UAT-13 UW smoke test confirms "Underwriter" is in the role selector
- [ ] All Delta checks returned the expected row counts and non-null timestamps
- [ ] Module 2 `is_locked = false` after Module 1 evaluation completes (UAT-08 Delta check)
- [ ] No Streamlit error box (red `st.error`) appeared for a system-level error during normal usage

### FAIL — Any one of the following triggers an overall FAIL:

- [ ] App shows an unhandled Python exception traceback on any happy path step
- [ ] Any Delta check returns 0 rows where > 0 is expected
- [ ] A loading state (Analyzing / Scoring / Building) does not resolve within the stated timeout
- [ ] Module 2 remains locked (`is_locked = true`) after Module 1 evaluation completes
- [ ] "Underwriter" is missing from the Welcome page role selector dropdown
- [ ] Navigating away from a partial retake diagnostic wipes completed module progress

---

## 5. Known Limitations / Out of Scope

| Limitation | Reason |
|-----------|--------|
| AI coach text content is NOT asserted | LLM outputs vary per call |
| Modules 3–7 are not fully tested | Structurally identical to Module 1; covered by pattern |
| Exact gap map bullet text is not asserted | AI-generated; varies per call |
| Mobile / responsive layout not tested | Desktop-first MVP (1280×800) |
| Manager dashboard not tested | Does not exist in MVP scope |
| UW full course completion not tested | UW content loaded; smoke test confirms onboarding works |
| Error/failure path scenarios not tested | Graceful error messages tested only by inspection |

---

## 6. UAT Agent Kickoff Prompt

Copy and paste the following prompt into a **new Claude Code session** to start a UAT run. The agent will read this document and execute all scenarios autonomously.


---

```
You are a UAT testing agent for the AI Hero Academy MVP — a Streamlit-based Databricks App
running locally at http://localhost:8501.

Your job is to execute the full UAT test suite defined in UAT.md located at the project root.
Read UAT.md now and follow it exactly.

TOOLS AVAILABLE TO YOU:
- Playwright MCP (mcp__playwright__browser_*) — for all browser interactions
- Databricks MCP (mcp__databricks-mcp-server__execute_sql) — for Delta table verification
  Warehouse ID: eaa098820703bf5f

BEFORE YOU BEGIN:

Confirm your testing environment:

> 1. The app is running locally: `bash run_uat.sh` (port 8501)
> 2. The test user has been reset: `python scripts/reset_uat_user.py`
> 3. Your `.env` has `DEV_USER_EMAIL=uat-test@edc.ca` set
> 4. Playwright MCP is connected and functional

1. Set the viewport: browser_resize(width=1280, height=800)
2. Confirm the app is running by navigating to http://localhost:8501
3. Run the pre-test Delta check in UAT.md Section 2 to confirm the test user is clean
   Test user email: uat-test@edc.ca
4. Create a folder under /tests under the root project folder with date and commit ID to store all screenshots and logs.



EXECUTION RULES:
- Read UAT.md Section 1 (Agent Instructions) carefully before touching the browser
- Execute scenarios UAT-01 through UAT-13 in order
- For every browser interaction: snapshot first → get ref → click/type using ref → wait for rerender
- After every click that triggers a page change or AI call, call browser_wait_for before proceeding
- Run every Delta Check SQL query listed after each scenario using execute_sql
- If a step fails: take a screenshot immediately, log [FAIL] UAT-NN: Step N — expected X, got Y,
  then continue to the next scenario unless it is a hard dependency (noted in pre-conditions)
- Do NOT assert specific AI-generated text — only assert UI state transitions and structural elements
- UAT-13 requires resetting the test user first — run python scripts/reset_uat_user.py via Bash
  before navigating to the Welcome page for that scenario
- Put all screenshots and logs in the previously created folder under /tests folder in the project root folder.

OUTPUT FORMAT:
After completing all scenarios, print the Test Execution Summary using the template in
UAT.md Section 6. List every scenario result (PASS/FAIL), note any failures with screenshot
filenames, and state the overall PASS/FAIL verdict.

Begin now: read UAT.md, then start UAT-01.
```

---

## 7. Test Execution Summary Template

After completing the UAT run, fill in this summary:

```
UAT Execution Date: ___________
App version / Git commit: ___________
Test user email: uat-test@edc.ca

SCENARIO RESULTS:
UAT-01: PASS / FAIL — notes
UAT-02: PASS / FAIL — notes
UAT-03: PASS / FAIL — notes
UAT-04: PASS / FAIL — notes
UAT-05: PASS / FAIL — notes
UAT-06: PASS / FAIL — notes
UAT-07: PASS / FAIL — notes
UAT-08: PASS / FAIL — notes
UAT-09: PASS / FAIL — notes
UAT-10: PASS / FAIL — notes
UAT-11: PASS / FAIL — notes
UAT-12: PASS / FAIL — notes
UAT-13: PASS / FAIL — notes

OVERALL RESULT: PASS / FAIL

FAILURES REQUIRING INVESTIGATION:
- [list any FAILs with screenshot references]
```
