================================================================================
PRD.md — AI Hero Academy — MVP Product Requirements Document
Version 1.0 | June 2025
================================================================================

TABLE OF CONTENTS
-----------------
1.  Executive Summary
2.  Problem Statement
3.  Target Users
4.  Product Vision and MVP Scope
5.  MVP Scope Boundaries
6.  User Experience Flow
7.  Detailed Screen Specifications
8.  Domain and Skill Taxonomy
9.  Content Architecture
10. Module Sequencing Logic
11. Navigation Structure
12. Success Metrics and Acceptance Criteria
13. Security, Compliance, and Data Classification
14. Out of Scope (Post-MVP)


================================================================================
1. EXECUTIVE SUMMARY
================================================================================

AI Hero Academy is an internal Databricks App that evaluates, trains, and
benchmarks employees on AI skills through real-life, job-specific use cases
and AI coaching powered by Mosaic AI Foundation Models.

The MVP focuses on a single role — Relationship Manager (RM) — and delivers
a complete learning loop:

  1. DIAGNOSE the employee's AI skill level through a role-specific assessment
  2. MAP GAPS using AI-generated personalized gap analysis
  3. TRAIN through structured courses combining reading, hands-on practice
     with an AI coach, and post-module evaluation
  4. SCORE AND TRACK progress as employees complete modules and retake
     assessments

The app is NOT a Learning Management System. It is a skills-plus-scenario-
plus-benchmark layer that teaches by doing, not by watching.

KEY DESIGN PRINCIPLES:

  - Job-anchored personalization: everything flows from the employee's
    actual job role, responsibilities, and real use cases
  - Learn by doing: training is scenario-based practice, not passive
    content consumption
  - Measure real ability: assessments test task performance and judgment,
    not knowledge recall
  - AI-coached, human-validated: AI coaches and scores in real time;
    humans curate and approve all static content before it goes live
  - Developmental framing: gap maps show growth paths, not rankings
    or punitive scores; scores are visible only to the employee


================================================================================
2. PROBLEM STATEMENT
================================================================================

The organization is rolling out AI tools (Microsoft 365 Copilot) across the
enterprise. Employees need to develop practical AI skills — not theoretical
knowledge — to use these tools effectively and safely in their actual work.

Current gaps:

  - Employees do not know which AI use cases are relevant to their specific
    job role and daily workflows
  - Generic AI training (videos, slide decks, tip sheets) does not connect
    to real workflows and does not build lasting habits
  - There is no way to measure practical AI skill levels across the
    organization or identify where the biggest gaps are
  - Employees lack safe practice environments to build AI habits before
    using AI tools on real client work
  - The organization's GenAI policy requires human review of all AI outputs
    and prohibits sharing non-public information with AI tools, but
    employees have not practiced applying these rules in realistic
    scenarios where the pressure to skip verification is real

The organization already has:

  - A well-documented library of 47 real-life AI use cases mapped to
    personas, triggers, workflows, outputs, and constraints
  - Corporate job descriptions and role intelligence for key roles
  - A mandatory Copilot training and attestation program (policy awareness)
  - An internal GenAI governance framework with clear rules

What is missing is the bridge between policy awareness and practical skill:
the ability to practice, be coached, be assessed, and track improvement
over time in the context of real job tasks.


================================================================================
3. TARGET USERS
================================================================================

3.1 MVP: RELATIONSHIP MANAGERS (RMs)
-------------------------------------

Role summary (extracted from corporate intelligence):

Relationship Managers are client-facing professionals who manage customer
relationships across segments (Small Business, Mid-Market, Large/Strategic).
They work with Associate Relationship Managers (ARMs) who handle early-stage
prospecting and research, then hand off qualified leads to RMs for discovery
and relationship management.

Key characteristics relevant to training design:

  ATTRIBUTE                  DETAIL
  -------------------------  ------------------------------------------------
  Official title variants    Relationship Manager, Account Manager (Small
                             Business), Associate Relationship Manager (ARM)
  Departments                Ontario Region, Quebec Region, MMB West, Market
                             Development, Sectors and International Advisory
  Primary tools              Outlook, Teams, Excel, Word, PowerPoint,
                             C3 (CRM), Salesforce
  Daily work                 Discovery meetings, CRM documentation, lead
                             management, client follow-ups, pipeline hygiene
  Biggest time sinks         CRM activity logging, lead aging compliance,
                             forecasting field maintenance, repetitive
                             outbound follow-ups
  KPI structure              Customer Growth 35%, Customer Experience 30%,
                             Process and Behaviours 25%, Education and
                             Growth 10%
  KPI specifics              Lead responsiveness SLA (3 business days for
                             new leads), lead aging compliance, forecasting
                             completeness (probability and close date),
                             NPS, retention, multi-solution adoption
  ARM support model          ARMs research leads (revenue, markets, decision
                             makers), enter context in C3, book meetings;
                             RMs take over for discovery and relationship
                             management
  AI governance context      Mandatory Copilot training and attestation
                             already exists; explicit policy: no non-public
                             information in AI tools; human review required
                             for all AI outputs; approved applications only
  Segments served            Small Business (under 10M revenue), Mid-Market,
                             Large/Strategic with segment-specific routing
  Internal stakeholders      Sales Operations, Marketing, Exporter
                             Engagement Team, CRM/Salesforce SMEs, NEXUS
                             enablement team, direct managers
  External stakeholders      Canadian companies (customers and prospects),
                             financial institution partners

3.2 SECONDARY USERS (Post-MVP)
-------------------------------

3.2.1 UNDERWRITER (UW) — v1 IN PROGRESS (Feb 2026)

  All UW content has been generated and is loaded into the app:
  12 diagnostic items (3 per domain), 5 training courses with
  reading content, practice scenarios, and evaluation items.
  The diagnostic and course module flows are fully multi-role aware.

  Remaining blocker: Welcome page (pages/00_Welcome.py) still
  hardcodes role_id = 'rm'. Task 9.4 (PLAN.md) will wire the role
  selector to display both RM and UW, enabling UW users to onboard.

3.2.2 OTHER ROLES (Post-MVP)

  The following roles are planned for future versions but remain
  explicitly out of scope until after the UW role is validated:

  - Finance Analysts
  - Customer Care Team
  - IT / DevOps
  - Legal / Compliance
  - Program Managers
  - Internal Audit
  - Corporate Communications
  - Economics (Office of Chief Economist)


================================================================================
4. PRODUCT VISION AND MVP SCOPE
================================================================================

4.1 VISION
-----------

Every employee has a personalized AI skills profile tied to their job, a
clear gap map showing where to improve, and structured practice scenarios
that build real competence — all powered by AI coaching and grounded in
the organization's actual use cases and policies.

4.2 MVP SCOPE SUMMARY
-----------------------

  DIMENSION              MVP SCOPE
  ---------------------  ------------------------------------------------
  Roles supported        1 (Relationship Manager)
  Skill domains          4 (Prompting, Verification, Data Safety,
                         Tool Fluency)
  Skill levels           0-4 scale per domain
  Skill tiers            1 (Foundations only)
  Diagnostic             12 items (3 per domain, mixed item types)
  Training courses       5 (mapped to top RM use cases)
  Course structure       Reading then Hands-on Practice with AI Coach
                         then Post-module Evaluation
  Modules per course     3 sub-modules (reading, practice, evaluation)
  Dashboard              Employee-only (personal progress view)
  AI models              Mosaic AI Foundation Model APIs (single endpoint)
  Hosting                Databricks App (Streamlit)
  Authentication         Databricks workspace SSO
  Persistence            Delta tables in Unity Catalog
  Language               English only


================================================================================
5. MVP SCOPE BOUNDARIES
================================================================================

5.1 EXPLICITLY IN SCOPE
-------------------------

  - Role selection (dropdown with 1 option: Relationship Manager)
  - 12-question diagnostic assessment with 3 item types:
    MCQ, prompt sandbox, and micro-task
  - AI-generated personalized gap map after diagnostic
  - 5 training courses with 3 sub-modules each
  - AI coach during hands-on practice (chat-based, max 15 turns)
  - Post-module mandatory evaluation that updates gap map and scores
  - Employee home page with progress tracking
  - Permanent skills profile and results page
  - Retake diagnostic capability
  - Full state persistence in Delta tables (cross-device, cross-session)
  - Personalized module sequencing based on gap priorities
  - Module locking (sequential unlock after completing prior module)

5.2 EXPLICITLY OUT OF SCOPE
-----------------------------

  - Manager or leadership dashboard views
  - Multiple roles (only RM in MVP)
  - Proficient tier (only Foundations tier in MVP)
  - Content generation UI or admin interface
  - Agent pipeline for automated role-to-use-case mapping
  - Human review queue for AI scoring
  - MLflow integration for prompt or model versioning
  - SQL Warehouse for analytics
  - Materialized views
  - Badge export or HR system integration
  - Content management, SCORM, or LMS features
  - Mobile-optimized layout (desktop-first only)
  - Multilingual or bilingual content (English only)
  - Real-time notifications or email reminders
  - Peer comparison or leaderboard features
  - Integration with external learning platforms


================================================================================
6. USER EXPERIENCE FLOW
================================================================================

6.1 JOURNEY STATES
-------------------

Every user is in exactly one of these states at any time:

  STATE                CONDITION                     DEFAULT PAGE
  -------------------  ----------------------------  ----------------
  new_user             No profile record exists       Welcome screen
  needs_diagnostic     Profile exists, no diagnostic  Diagnostic
  needs_course         Diagnostic done, no course     Skills Profile
  in_training          Course created, in progress    Home
  completed            All 5 modules completed        Home

6.2 FIRST VISIT FLOW
----------------------

  Welcome Screen
       |
       | User selects role (Relationship Manager)
       | Clicks "Start My Diagnostic"
       v
  Diagnostic Screen
       |
       | User answers 12 questions (MCQ + sandbox + micro-task)
       | Clicks "Submit" on final question
       v
  Loading Screen ("Analyzing your responses...")
       |
       | AI scores all responses
       | AI generates personalized gap map
       | Results written to Delta
       v
  Skills Profile Screen
       |
       | User sees domain scores, gap map narrative
       | Clicks "Build My Training Course"
       v
  Loading Screen ("Building your personalized course...")
       |
       | System creates 5 training_progress records
       | Module sequence personalized by gap priorities
       v
  Home Screen
       |
       | User sees course with Module 1 available, Modules 2-5 locked
       | Clicks "Start Module 1"
       v
  Course Module Screen (repeats for each module)

6.3 RETURNING VISIT FLOW
--------------------------

  App loads
       |
       | System reads user_email from SSO
       | System queries Delta for user state
       v
  Route to appropriate page based on state:
       |
       |-- new_user -----------> Welcome Screen
       |-- needs_diagnostic ---> Diagnostic Screen
       |-- needs_course -------> Skills Profile (with "Build Course" CTA)
       |-- in_training --------> Home Screen (with current progress)
       |-- completed ----------> Home Screen (all modules complete)

6.4 INSIDE A TRAINING MODULE FLOW
-----------------------------------

  Module Overview Screen
       |
       | Shows: title, domains, what you will learn, sub-module status
       | CTA: "Start Reading"
       v
  Reading Sub-module
       |
       | User reads content (concept, example, anti-pattern, takeaway)
       | Clicks "I've read this — Start Practice"
       | Delta write: reading_completed_at
       v
  Practice Sub-module (AI Coach)
       |
       | User sees scenario and simulated content
       | Task 1: user submits response, coach replies
       | Task 2: user submits response, coach replies
       | Task 3: user submits response, coach replies
       | Task 4: user submits response, coach replies
       | (Max 15 total coach turns across all tasks)
       | Clicks "Complete Practice"
       | Delta write: coach_session + practice_completed_at
       v
  Evaluation Sub-module (Mandatory Quiz)
       |
       | User answers 4 questions (3 MCQ + 1 performance task)
       | Clicks "Submit" on final question
       v
  Loading Screen ("Scoring your responses...")
       |
       | AI scores responses
       | AI updates gap map
       | Domain scores recalculated
       | Next module unlocked
       | Delta writes: evaluation_results + gap_maps + training_progress
       v
  Module Results Screen
       |
       | Shows: module score, per-domain breakdown, coach note
       | CTAs: "View Updated Skills Profile" / "Start Module N"
       v
  Home Screen (updated progress)

6.5 RETAKE DIAGNOSTIC FLOW
----------------------------

  Skills Profile Screen
       |
       | User clicks "Retake Diagnostic"
       v
  Diagnostic Screen (same 12 questions)
       |
       | On completion: new diagnostic_session created
       | New gap map generated
       | Course module sequence may reorder based on new gaps
       | All prior progress is preserved (completed modules stay completed)
       v
  Skills Profile Screen (updated scores and gap map)


================================================================================
7. DETAILED SCREEN SPECIFICATIONS
================================================================================

7.1 WELCOME SCREEN
--------------------

Trigger: User has no record in learner.user_profiles

Elements:
  - App logo/icon area
  - Title: "AI Hero Academy"
  - Tagline: "Master the AI skills that matter for YOUR job"
  - Value proposition text (3 lines max):
    "This is not a course about AI. It is practice USING AI for your
    actual work — through real scenarios, hands-on experiments, and
    AI coaching."
  - Time estimate: "Your first step: a 5-minute diagnostic to see
    where you stand."
  - Role selector: dropdown with label "Select your role"
    Options: ["Relationship Manager"] (single option in MVP)
  - CTA button: "Start My Diagnostic" (disabled until role selected)

Behavior:
  - On CTA click:
    1. Write new row to learner.user_profiles
    2. Store role_id in session_state
    3. Navigate to Diagnostic screen

Validation:
  - Role must be selected before CTA is enabled
  - If user already has a profile, redirect to Home instead

7.2 DIAGNOSTIC SCREEN
-----------------------

Trigger: User clicks "Start My Diagnostic" or "Retake Diagnostic"

Elements:
  - Header: "Diagnostic"
  - Question counter: "Question X of 12"
  - Domain label: shows which domain the current question tests
  - Progress bar: percentage complete (X/12 * 100)
  - Question content area (rendering varies by item type, see below)
  - Navigation: "Next" button (no back navigation)

Item type rendering:

  MCQ ITEMS:
    - Question text (may include a scenario paragraph above the question)
    - 4 radio button options (A, B, C, D)
    - "Next" button (disabled until an option is selected)

  PROMPT SANDBOX ITEMS:
    - Scenario description text (boxed/highlighted)
    - Instruction text: "Write the prompt you would give Copilot:"
    - Multi-line text input area (minimum 4 lines visible, expandable)
    - Character guidance: "Aim for 3-8 sentences"
    - "Submit" button (disabled if text area is empty)

  MICRO-TASK ITEMS:
    - Scenario description text
    - Embedded content to review (e.g., AI-generated recap text,
      displayed in a distinct box with a different background)
    - Instruction text (e.g., "Mark which 2 statements need
      verification and explain why")
    - Multi-line text input area (minimum 4 lines visible)
    - "Submit" button (disabled if text area is empty)

Final question behavior:
  - After submitting question 12, show loading state:
    "Analyzing your responses..." with a progress animation
  - AI scoring call runs (all 12 responses scored in one call)
  - Gap map generation call runs
  - Results written to Delta
  - Redirect to Skills Profile screen

Session state during diagnostic:
  - All responses stored in session_state as a list
  - If user refreshes mid-diagnostic, they restart from question 1
    (acceptable for a 5-minute assessment)
  - No partial saves to Delta during the diagnostic

7.3 SKILLS PROFILE SCREEN
---------------------------

Trigger: User has completed at least one diagnostic session

Elements:

  HEADER SECTION:
    - Title: "Your AI Skills Profile"
    - Role label: "Role: Relationship Manager"
    - Last assessed date: "Last assessed: [date]"
    - Overall level: "[X.X] / 4.0 — [Level Label]"
      (Level label derived from overall score:
       0.0-0.4 = Unaware, 0.5-1.4 = Explorer,
       1.5-2.4 = Practitioner, 2.5-3.4 = Proficient,
       3.5-4.0 = Champion)

  DOMAIN SCORES SECTION:
    - 4 horizontal progress bars, one per domain
    - Each bar shows:
      - Domain name (left-aligned)
      - Score "X.X / 4.0" (right-aligned)
      - Visual fill proportional to score
      - Color coding:
        0.0-1.4 = red/danger
        1.5-2.4 = yellow/warning
        2.5-4.0 = green/success

  GAP MAP SECTION:
    - Section title: "Your Gap Map"
    - AI-generated narrative as a list of 3-6 bullet points
    - Each bullet contains:
      - Priority icon: red circle (score below 1.5),
        yellow circle (score 1.5-2.4),
        green circle (score 2.5+)
      - Domain name in bold
      - Gap description (1-2 sentences, specific to their responses)
    - Bullets ordered by priority (biggest gap first)

  ASSESSMENT HISTORY SECTION:
    - Section title: "Assessment History"
    - Table with columns: Date, Overall Score, Prompting,
      Verification, Data Safety, Tool Fluency
    - One row per diagnostic session (most recent first)
    - Shows trend if multiple sessions exist

  ACTION BUTTONS:
    - "Retake Diagnostic" button (always visible)
    - "Build My Training Course" button (visible only if no course
      exists yet for this user)
    - "View My Course" button (visible if course already exists)

Behavior:
  - Domain scores are calculated as the weighted average of:
    - Latest diagnostic scores for that domain
    - All completed evaluation scores for that domain
    - Weighting: most recent assessment counts most
      (simple approach for MVP: latest diagnostic score is the
      baseline; each completed evaluation updates the domain score
      as the average of the diagnostic score and all evaluation
      scores for that domain)
  - Gap map is the most recent version from learner.gap_maps

7.4 HOME SCREEN
-----------------

Trigger: User has a profile and has completed diagnostic

Elements:

  GREETING:
    - "Welcome back, [display_name]"

  SKILLS SUMMARY CARD:
    - Overall level with label
    - Trend indicator compared to previous assessment:
      up arrow if improved, right arrow if same, down arrow if declined
    - Last updated date
    - "View Full Profile" link (navigates to Skills Profile)

  COURSE PROGRESS SECTION:
    - Section title: "My Training Course"
    - List of 5 modules, each showing:

      COMPLETED MODULE:
        - Module number and title
        - Domain focus labels
        - Sub-module indicators: checkmark Reading, checkmark Practice,
          checkmark Quiz
        - Score: "X.X / 4.0"

      IN-PROGRESS MODULE:
        - Module number and title
        - Domain focus labels
        - Sub-module indicators showing current state:
          checkmark for completed, blue dot for current,
          empty circle for not started
        - "Continue" button

      LOCKED MODULE:
        - Module number and title
        - Lock icon
        - Text: "Complete Module [N] first"
        - Greyed out / visually distinct

Behavior:
  - If no diagnostic taken: redirect to Welcome
  - If diagnostic taken but no course: redirect to Skills Profile
    with "Build Course" CTA visible
  - If course exists: show Home with current progress
  - "Continue" button on in-progress module navigates to the
    appropriate sub-module (reading if not started, practice if
    reading done, evaluation if practice done)

7.5 COURSE MODULE SCREEN
--------------------------

This is a single page with multiple sub-views depending on which
sub-module the user is in.

7.5.1 MODULE OVERVIEW SUB-VIEW

  Trigger: User clicks into a module from Home

  Elements:
    - Module number and title
    - Domain focus labels (primary and secondary)
    - "What you will learn" section (3 bullet points)
    - Sub-module progress strip:
      Three boxes in a row connected by arrows:
      [Read - X min] -> [Practice - X min] -> [Quiz - X min]
      Each box shows status: Done, Current, or Not Started
    - CTA button: context-dependent
      "Start Reading" if reading not done
      "Continue Practice" if reading done but practice not done
      "Take Quiz" if practice done but quiz not done
      "Review Results" if all done

7.5.2 READING SUB-VIEW

  Trigger: User clicks "Start Reading" or navigates to reading

  Elements:
    - Header: "Reading: [Module Title]"
    - Content sections rendered as clean formatted text:

      CONCEPT SECTION:
        - 2-4 paragraphs explaining the key concept
        - Specific to the RM role and the use case being taught

      GOOD EXAMPLE SECTION:
        - Boxed/highlighted area with label "Good Example"
        - Shows a realistic example of the skill done well
        - Annotation explaining why it is good

      ANTI-PATTERN SECTION:
        - Boxed/highlighted area with label "Common Mistake"
        - Shows a realistic example of the skill done poorly
        - Annotation explaining what went wrong

      KEY TAKEAWAY SECTION:
        - Callout box with distinct styling
        - 2-3 sentences summarizing the most important point

    - CTA at bottom: "I have read this — Start Practice"

  Behavior:
    - On CTA click:
      1. Write reading_completed_at to learner.training_progress
      2. Navigate to Practice sub-view

7.5.3 PRACTICE SUB-VIEW (AI Coach)

  Trigger: User clicks "Start Practice" or "Continue Practice"

  Elements:

    SCENARIO PANEL (top, always visible):
      - Label: "Scenario"
      - Scenario description text (2-4 paragraphs)
      - If applicable: simulated content box (e.g., an AI-generated
        recap or CRM entry for the user to review)

    TASK PANEL (middle):
      - Task indicator: "Task X of 4"
      - Task instruction text
      - Text input area for user response
      - "Submit" button

    COACH PANEL (below task, appears after submission):
      - Label: "AI Coach" with a robot/coach icon
      - Coach response text
      - Follow-up text input for user reply
      - "Reply" button
      - Turn counter: "Turn X of 15"

    NAVIGATION:
      - After completing coach exchange for a task (or after 3 turns
        on a single task), "Next Task" button appears
      - After all 4 tasks: "Complete Practice" button appears

  Behavior:
    - Each task allows up to 3 coach exchanges (user submit + coach
      reply = 1 exchange) before auto-advancing to next task
    - Total session capped at 15 turns across all tasks
    - If 15 turns reached before all tasks done:
      Show message: "You have reached the practice limit for this
      session. Let us move to the quiz to check your understanding."
      Show "Go to Quiz" button
    - On "Complete Practice" click:
      1. Write coach_session to learner.coach_sessions
      2. Write practice_completed_at to learner.training_progress
      3. Navigate to Evaluation sub-view
    - If user refreshes during practice:
      Coach conversation is lost (acceptable — practice is exploratory)
      User can restart practice from Task 1

7.5.4 EVALUATION SUB-VIEW (Mandatory Quiz)

  Trigger: User clicks "Take Quiz" after completing practice

  Elements:
    - Header: "Quiz: [Module Title]"
    - Question counter: "Question X of 4"
    - Progress bar
    - Question content (same rendering as diagnostic: MCQ or
      performance task)
    - "Next" button (no back navigation)

  Question composition per module:
    - Questions 1-3: MCQ (testing concepts from reading and practice)
    - Question 4: Performance task (new scenario, different from
      practice, requiring written response)

  Final question behavior:
    - After submitting question 4, show loading state:
      "Scoring your responses..."
    - AI scoring call runs
    - Gap map update call runs
    - Domain scores recalculated
    - Next module unlocked (status changed from "locked" to "available")
    - Results written to Delta
    - Navigate to Module Results sub-view

7.5.5 MODULE RESULTS SUB-VIEW

  Trigger: Evaluation scoring complete

  Elements:
    - Module title and overall score: "X.X / 4.0"
    - Per-domain score breakdown (only domains covered in this module):
      - Domain name, score, status icon (checkmark or warning)
    - AI-generated coach note (1-2 sentences):
      Encouraging, specific to their performance, hints at what
      the next module will cover
    - Confirmation text: "Your skills profile has been updated."
    - CTA buttons:
      "View Updated Skills Profile" (navigates to Skills Profile)
      "Start Module [N+1]" (navigates to next module overview)
      If all modules complete: "View Final Skills Profile"


================================================================================
8. DOMAIN AND SKILL TAXONOMY
================================================================================

8.1 DOMAINS
-------------

  DOMAIN 1: PROMPTING FOR OUTCOMES
    Structuring AI prompts with context, constraints, format, and
    audience to produce useful work outputs. Includes providing
    relevant CRM/ARM context, specifying deliverable format, setting
    scope limits, and iterating on prompts to improve results.

  DOMAIN 2: VERIFICATION AND JUDGMENT
    Checking AI outputs for accuracy, detecting hallucinations,
    identifying unsupported claims, knowing when to trust or reject
    AI suggestions, and applying the human review discipline required
    by organizational policy. Includes verifying facts against source
    data (CRM, transcripts, ARM notes) before acting on AI output.

  DOMAIN 3: DATA SAFETY AND COMPLIANCE
    Understanding what information can and cannot be shared with AI
    tools, applying the organization's GenAI policy in practice,
    handling sensitive client data appropriately, and recognizing
    when AI use crosses compliance boundaries. Specific to EDC:
    no non-public information in AI tools, approved applications
    only, mandatory human review.

  DOMAIN 4: TOOL FLUENCY (M365 + Copilot)
    Knowing which M365 tool and Copilot feature to use for which
    task, executing multi-step AI-assisted workflows efficiently,
    and understanding the capabilities and limitations of Copilot
    in Teams, Outlook, Excel, Word, and PowerPoint.

8.2 SKILL LEVELS
-----------------

  LEVEL 0 — UNAWARE
    Has not used AI tools. Does not know what is available.
    Observable: Cannot identify when AI could help. No prompt
    writing ability. Unaware of data safety rules for AI.

  LEVEL 1 — EXPLORER
    Has tried AI tools with basic prompting. No structured workflow.
    Observable: Writes vague prompts without context or constraints.
    Accepts AI outputs without checking. Unsure about what data is
    safe to share with AI tools.

  LEVEL 2 — PRACTITIONER
    Uses structured prompts. Verifies outputs. Follows data safety rules.
    Observable: Includes context and constraints in prompts. Checks
    key facts against source data before using AI output. Knows what
    information must not be entered into AI tools.

  LEVEL 3 — PROFICIENT
    Adapts workflows to complex scenarios. Handles edge cases.
    Can teach others.
    Observable: Chains multi-tool workflows (e.g., Teams transcript
    to verified recap to CRM log to follow-up email). Catches subtle
    errors and hallucinations. Applies policy correctly in ambiguous
    situations.

  LEVEL 4 — CHAMPION
    Designs new use cases. Mentors peers. Contributes to best practices.
    Observable: Creates reusable prompt templates for the team.
    Identifies new AI opportunities in RM workflows. Coaches
    colleagues on effective and safe AI use.

8.3 SCORING RULES
-------------------

  Item scoring:
    - MCQ items: correct answer = level-appropriate score (typically
      4 for best answer, 3 for acceptable, 1-2 for partially correct,
      0 for incorrect/unsafe); specific scoring defined per item
    - Prompt sandbox items: AI-scored against a rubric with 3-4
      weighted criteria; each criterion scored 0-1; total scaled to 0-4
    - Micro-task items: AI-scored against a rubric with 2-3 weighted
      criteria; total scaled to 0-4
    - Performance task items (in evaluations): same as prompt sandbox

  Domain score calculation:
    - After diagnostic only: average of the 3 diagnostic item scores
      for that domain
    - After completing evaluations: average of diagnostic scores AND
      all evaluation scores for that domain (equal weight per item)

  Overall score:
    - Average of 4 domain scores

  Level label derivation from score:
    0.0 to 0.4  = Unaware
    0.5 to 1.4  = Explorer
    1.5 to 2.4  = Practitioner
    2.5 to 3.4  = Proficient
    3.5 to 4.0  = Champion


================================================================================
9. CONTENT ARCHITECTURE
================================================================================

9.1 STATIC CONTENT (same for all RMs, pre-seeded)
---------------------------------------------------

  - Domain definitions and level descriptors
  - Role profile (RM)
  - Use case library (47 use cases, 5 mapped to RM)
  - Diagnostic items (12 items)
  - Training courses (5 courses):
    - Reading content (1 per course)
    - Practice scenarios with tasks (1 scenario with 4 tasks per course)
    - Practice coach system prompts (1 per course)
    - Evaluation items (4 per course, 20 total)
    - Scoring rubrics (per evaluation item)

9.2 DYNAMIC CONTENT (personalized per employee, AI-generated)
--------------------------------------------------------------

  - Gap map narrative (generated after diagnostic and after each
    evaluation; specific to the employee's scores and responses)
  - Course module sequence (ordered by the employee's gap priorities)
  - AI coach conversations (unique per practice session, adapts to
    what the employee writes)
  - Evaluation feedback and rationale (AI-generated per submission)
  - Module results coach note (personalized encouragement)

9.3 CONTENT RELATIONSHIP MAP
------------------------------

  Role (RM)
    |
    |-- has 5 mapped Use Cases
    |     |
    |     |-- each Use Case maps to 1 Training Course
    |           |
    |           |-- 1 Reading Module
    |           |-- 1 Practice Scenario (with 4 tasks + coach prompt)
    |           |-- 4 Evaluation Items (3 MCQ + 1 performance task)
    |
    |-- has 12 Diagnostic Items (3 per domain)
    |
    |-- has 4 Domains (each with level descriptors)


================================================================================
10. MODULE SEQUENCING LOGIC
================================================================================

After the diagnostic, the 5 training modules are ordered for each
employee based on their domain scores. The algorithm prioritizes a
"quick win" first to build confidence, then addresses the biggest gaps.

ALGORITHM:

  Step 1: Identify the quick-win domain
    - Find domains where the employee scored between 1.5 and 2.5
    - If multiple, pick the one closest to 2.0
    - If none in this range, skip to Step 2

  Step 2: Identify gap domains
    - Find domains where the employee scored below 1.5
    - Order ascending (lowest score = biggest gap = highest priority)

  Step 3: Identify strong domains
    - Find domains where the employee scored above 2.5
    - Order ascending

  Step 4: Build priority sequence
    - Priority order: quick-win domain first, then gap domains,
      then remaining domains, then strong domains

  Step 5: Map domains to courses
    - Each course has a primary domain
    - Order courses by their primary domain's position in the
      priority sequence
    - If two courses share a primary domain, order by secondary
      domain priority

  Step 6: Assign sequence numbers
    - Module 1 = first in sequence (unlocked immediately)
    - Modules 2-5 = locked (unlock sequentially as prior module
      is completed)

EXAMPLE:

  Employee scores:
    Prompting: 2.0, Verification: 0.8, Data Safety: 1.2, Tool Fluency: 3.0

  Quick win: Prompting (2.0, in range 1.5-2.5)
  Gaps: Verification (0.8), Data Safety (1.2)
  Strong: Tool Fluency (3.0)

  Priority: Prompting > Verification > Data Safety > Tool Fluency

  Module sequence:
    1. Course with Prompting as primary domain (quick win)
    2. Course with Verification as primary domain (biggest gap)
    3. Course with Data Safety as primary domain (second gap)
    4. Second course with Prompting/Verification (remaining)
    5. Course with Tool Fluency as primary domain (strong area)


================================================================================
11. NAVIGATION STRUCTURE
================================================================================

The app has 4 primary pages accessible via sidebar navigation:

  PAGE                SIDEBAR LABEL    ICON    VISIBILITY
  ------------------  ---------------  ------  -------------------------
  Home                Home             house   Always (after onboarding)
  Skills Profile      Skills Profile   chart   Always (after diagnostic)
  My Course           My Course        grad    Always (after course created)
  Diagnostic          Diagnostic       flag    Hidden after first completion
                                               (accessible via "Retake"
                                               button on Skills Profile)

Sidebar behavior:
  - Pages that are not yet relevant are hidden (not greyed out)
  - New users see only the Welcome screen (no sidebar)
  - After diagnostic: Home and Skills Profile appear
  - After course creation: My Course appears
  - Diagnostic page is hidden from sidebar after first completion
    but accessible via the "Retake Diagnostic" button

Deep linking:
  - Each page has a stable URL path
  - Users can bookmark and return to any page
  - The app checks user state on every page load and redirects
    if the user is not yet eligible for that page


================================================================================
12. SUCCESS METRICS AND ACCEPTANCE CRITERIA
================================================================================

12.1 MVP SUCCESS METRICS (First 8 Weeks Post-Launch)
------------------------------------------------------

  METRIC                        TARGET    MEASUREMENT
  ----------------------------  --------  --------------------------------
  Diagnostic completion rate    >80%      diagnostic_sessions count vs
                                          invited RM count
  Course start rate             >60%      training_progress rows with
                                          status not equal to locked,
                                          divided by diagnostic completions
  Module completion rate        >50%      Users completing at least 3 of
                                          5 modules
  Skill improvement             >=0.5     Average domain score increase
                                          comparing diagnostic to final
                                          evaluation scores
  User return rate              >40%      Users with multiple distinct
                                          active dates
  AI coach engagement           >5 turns  Average total_turns per
                                          coach_session
  Diagnostic duration           <8 min    Average time from first question
                                          to completion
  Practice session duration     5-15 min  Average time per practice session

12.2 FUNCTIONAL ACCEPTANCE CRITERIA
-------------------------------------

  AC-01: A new user can complete the full journey (welcome through
         diagnostic through course creation through module 1 completion)
         in a single session without errors.

  AC-02: A returning user lands on the Home page and sees their
         current progress accurately reflected.

  AC-03: A user who closes the browser and returns on a different
         device sees all their completed progress preserved.

  AC-04: The diagnostic scores all 12 items and produces a gap map
         within 45 seconds of submission.

  AC-05: The AI coach responds to user input within 10 seconds
         during practice sessions.

  AC-06: Completing a module evaluation updates the user's domain
         scores and gap map, and unlocks the next module.

  AC-07: The module sequence is personalized based on the user's
         diagnostic scores (not the same for every user).

  AC-08: A user can retake the diagnostic and see updated scores
         and gap map without losing completed module progress.

  AC-09: All AI calls that fail display a graceful error message
         and do not lose user progress.

  AC-10: No real client names, financial figures, or non-public
         information appears in any training content.


================================================================================
13. SECURITY, COMPLIANCE, AND DATA CLASSIFICATION
================================================================================

13.1 DATA CLASSIFICATION
--------------------------

  DATA TYPE                CLASSIFICATION       HANDLING
  -----------------------  -------------------  ---------------------------
  Employee email/name      Internal / PII       Stored in Delta; accessed
                                                only by the employee
  Diagnostic responses     Internal             Stored in Delta; no
                                                external sharing
  Skill scores             Internal/Sensitive   Visible only to the
                                                employee; no manager view
  Gap map narratives       Internal             Personal to the employee
  Coach conversations      Internal             Stored in Delta; contain
                                                only simulated data
  AI call logs             Internal/Operational Used for monitoring and
                                                debugging only

13.2 CONTENT SAFETY RULES
---------------------------

  - All training scenarios use fictional company names and data
  - No real client names, financial figures, or non-public information
    in any seeded content
  - Practice scenarios explicitly teach safe data handling as part
    of the curriculum
  - AI coach system prompts include instructions to flag if a user
    attempts to input what appears to be real client data during
    practice
  - Simulated CRM entries, email threads, and meeting transcripts
    use clearly fictional entities (e.g., "Northern Fabrication Ltd.",
    "Maple Industries Ltd.", "Pacific Trading Co.")

13.3 AI SAFETY RULES
----------------------

  - All AI scoring uses low temperature (0.1) for consistency
  - AI coach uses moderate temperature (0.4) constrained by system
    prompt rules
  - No AI output is presented as authoritative or used for employment
    decisions
  - All scoring includes rationale text that the user can read
  - The app does not compare employees to each other
  - Scores are developmental, not evaluative for HR purposes

13.4 ACCESS CONTROL
---------------------

  - Authentication via Databricks workspace SSO (no custom auth)
  - Each user can only see their own data
  - No admin role in MVP (content is seeded via notebooks)
  - Delta tables use Unity Catalog permissions:
    - content schema: read-only for the app service principal
    - learner schema: read-write for the app service principal,
      filtered by user_email in all queries
    - system schema: write for the app, read for administrators


================================================================================
14. OUT OF SCOPE (POST-MVP)
================================================================================

The following features are explicitly deferred. They are documented here
so the coding agent does not build toward them or create abstractions
that anticipate them unless doing so costs zero additional effort.

  FEATURE                              TARGET VERSION
  -----------------------------------  ---------------
  Additional roles                     v1
  Agent pipeline for content gen       v1
  Admin UI for content management      v1
  Manager dashboard                    v1
  Leadership dashboard                 v2
  Proficient tier (advanced courses)   v1
  MLflow prompt versioning             v1
  SQL Warehouse analytics              v1
  Materialized views                   v1
  Badge export / HR integration        v2
  Multilingual content (French)        v2
  Mobile-optimized layout              v2
  Real-work evidence collection        v2
  Peer coaching / community            v2
  Email notifications / reminders      v2
  Leaderboard / peer comparison        v2 (if ever)
  Integration with external LMS        v2
  Custom model fine-tuning             v2
  Offline mode                         Not planned


================================================================================
END OF PRD.md
================================================================================
