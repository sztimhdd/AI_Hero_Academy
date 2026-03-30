# AI Hero Academy — B2C Transformation Roadmap
**Status:** Sprints S1–S5 complete ✅ | Private beta ready
**Owner:** Product / Strategy | **Last updated:** 2026-03-30

> This is a living document. Update in-session as decisions are made.
> Unresolved items are marked ⬜. Confirmed decisions are marked ✅.

---

## 0. Strategic North Star

**Product:** Personal AI transformation tool — not a course platform, not an LMS.
**Promise:** Transform any individual into an HR-desired "AI-supercharged" professional in 7 days — regardless of role or industry.
**Audience:** Job seekers · New grads entering workforce · Mid-career workers facing AI displacement
**Output:** "AI-Supercharged Intermediate" credential after passing all pillar quizzes + Day 7 capstone.
**Differentiator:** Scenario-based practice with AI coaching, not passive content consumption. The learner *builds* a personal AI toolkit, not just a certificate.
**Business model:** Permanently free. The 7-day program is a top-of-funnel audience acquisition tool for paid online courses offered post-completion. No paywalls, no freemium gates — the credential and toolkit are the value exchange.
**Language:** Bilingual EN + ZH at all times. Not EN-first.

---

## 1. Learning Model (Lifecycle)

### 1.1 The 7-Day Transformation Arc

```
DAY 0   ONBOARDING + DIAGNOSTIC
        ├── Declare role context (job function + industry)
        ├── 12-item diagnostic → pillar gap scores
        └── Gap map generated → focus areas flagged (does not block progress)

DAY 1   PILLAR 1 — AI Conceptual Foundation
DAY 2   PILLAR 2 — Prompting & Context Engineering
DAY 3   PILLAR 3 — AI Tool Fluency
DAY 4   PILLAR 4 — AI Configuration & Control
DAY 5   PILLAR 5 — Multi-AI Workflow Design
DAY 6   PILLAR 6 — Agentic System Design

DAY 7   CAPSTONE — End-to-End AI Challenge
        ├── One scenario spanning all 6 pillars
        ├── AI-coached, not auto-graded
        └── PASS → "AI-Supercharged Intermediate" credential issued
```

### 1.2 Daily Module Structure (~90 min)

| Component | Time | Purpose |
|-----------|------|---------|
| **Reading** | ~20 min | Concept · Good example · Anti-pattern · Takeaway |
| **Practice** | ~40 min | 4 tasks + AI coach · Role context injected at runtime |
| **Quiz** | ~15 min | 4 questions · Must pass threshold to unlock next day |
| **Build** | ~15 min | 1 reusable artifact the learner keeps and owns |

### 1.3 Progression Logic

✅ **Linear sequence** — Day N unlocks after Day N-1 quiz is passed.
✅ **No level branching** — One module per pillar. Target: intermediate on completion.
✅ **Diagnostic informs coach depth, not routing** — Gap scores configure coach emphasis, not the learning path.
✅ **Quiz pass threshold** — Score ≥ 2.5 / 4.0 to pass.
✅ **Quiz fail handling** — Immediate retake, unlocked with coach hints surfaced alongside the questions. No retry limit.
✅ **Day 7 capstone format** — AI-coached challenge. Mix of: text input, screenshot/code snippet upload, MCQs. Under 15 mins. Learner encouraged to use their own AI tools to help. AI coach provides real-time guidance throughout.

### 1.4 Credential Model

**"AI-Supercharged Intermediate" credential on Day 7 completion:**

- **LinkedIn "Licenses & Certifications" one-click add** — standard deep link (`linkedin.com/profile/add?...`) with issuer, credential name, issue date, and credential ID pre-filled. Same pattern used by Google, Coursera, Credly.
- **Open Badge (PNG + embedded metadata)** — Open Badges 3.0 standard; machine-verifiable, works on LinkedIn, email signatures, resumes.
- **Social share card** — 1200×630px image generated at issuance (Cloud Run), pre-composed for LinkedIn / WeChat / Xiaohongshu / TikTok.
- **PDF certificate** — name + date + overall score + pillar breakdown. Downloadable.
- **No expiry at MVP.**

Badge image + metadata generated at issuance, stored in GCS, served via stable URL. No third-party credentialing platform needed at MVP scale.

### 1.6 Engagement & Retention Model (Industry Best Practice)

Informed by Duolingo, Uxcel, and gamification research:

- **Daily streak** — visible progress indicator; streak at risk notification if Day N not started by evening
- **Pillar badges** — awarded on quiz pass; shareable; visible on profile
- **Build artifact gallery** — cumulative personal toolkit the learner can review and export
- **Gap map delta** — after Day 7, re-run diagnostic to show score improvement vs. Day 0 baseline
- **Micro-pacing** — 90 min/day is the ceiling; modules are designed to feel completable in a lunch break
- **No punitive mechanics** — retakes are free, scores are private, gaps are framed as growth not failure

### 1.7 Role Context Injection

No hardcoded roles. Onboarding is a **personalization conversation**, not a form. Goal: extract rich context about the learner's role and day-to-day work to ground all subsequent AI coaching and scenario generation.

Structured outputs captured:

- **Job function:** marketer · analyst · teacher · nurse · PM · freelancer · student · developer · HR · ops
- **Industry:** tech · finance · healthcare · education · retail · creative · legal · public sector
- **Day-to-day work description** (free text, 2–3 sentences) — used as coach grounding context
- **Current AI tool usage** (free text) — calibrates coach depth for Day 1
- **Primary motivation** (job seeker / upskill for current role / career change / curiosity)

This full context object is stored on `user_profiles` and injected into every coach session via `{role}`, `{org_type}`, `{case_type}`, `{daily_work}` parameters. Same parameterization pattern as existing `atomic_modules_v2.json`, extended.

---

## 2. Content Generation Pipeline

### 2.0 Strategy: Content First, Multi-Agent

**Decision:** Content is generated before the Next.js app shell is built. Content-first prevents building empty UIs and ensures the learning experience drives the architecture, not the reverse.

**Method: Option D — Multi-Agent Content Creation Team**

A team of specialized Gemini 3.1 Pro agents, each with a defined role, equipped with Tavily + Google Search for live research. They operate like a real team of learning designers: researcher → curriculum designer → writer → scenario designer → coach architect → assessor → reviewer. Each agent produces one artifact; the next agent builds on it.

### 2.1 Agent Team Structure

```
ORCHESTRATOR
  └── Runs per pillar (P1 → P6)
  └── Parallelizes where safe: P1–P3 first pass, then P4–P6
  └── Feeds outputs forward as inputs to next agent

AGENT 1 — Research Agent  [Gemini 3.1 Pro + Tavily + Google Search]
  Role:   Research current state of the pillar domain
  Input:  Pillar definition + "2026 AI skills landscape"
  Output: Research brief (examples, tools, frameworks, best practices, real 2026 context)

AGENT 2 — Curriculum Designer  [Gemini 3.1 Pro]
  Role:   Define what "intermediate" looks like for this pillar;
          design the learning arc (what to teach, in what order)
  Input:  Research brief + pillar skill map + existing reusable atoms
  Output: Curriculum spec (learning objectives, key concepts, intermediate bar definition)

AGENT 3 — Content Writer  [Gemini 3.1 Pro / Claude Sonnet 4.6]
  Role:   Write the reading content
  Input:  Curriculum spec + research brief
  Output: reading JSON {concept_text, good_example, anti_pattern, takeaway}

AGENT 4 — Scenario Designer  [Gemini 3.1 Pro]
  Role:   Design the practice scenario + 4 parameterized tasks
  Input:  Curriculum spec + role_contexts.json (10-15 archetypes)
  Output: scenario_template + task_templates[4] with {role}/{org_type}/{case_type} slots

AGENT 5 — Coach Architect  [Claude Sonnet 4.6]
  Role:   Design the coaching framework + probe library for this pillar;
          write the coach_system_prompt_template
  Input:  Curriculum spec + scenario + b2c-ai-coach-gap-analysis.md
  Output: coach_system_prompt_template + per-task guidance + data safety guardrail

AGENT 6 — Assessment Designer  [Gemini 3.1 Pro]
  Role:   Write quiz questions + build artifact spec + closing prompt
  Input:  Curriculum spec + reading content
  Output: 3 MCQ items + 1 open rubric item + build_artifact_prompt

AGENT 7 — Quality Reviewer  [Claude Sonnet 4.6]
  Role:   Review full pillar package for B2C tone, accuracy,
          role-agnostic language, intermediate calibration, EN/ZH readiness
  Input:  All above outputs
  Output: Review notes + inline edits → final approved pillar JSON
```

### 2.2 Pillar Generation Order + Estimated Effort

| Pillar | Existing seed material | Research needed | New build effort |
| ------ | --------------------- | --------------- | ---------------- |
| P1 Foundation | `hallucination_patterns` + `ai_tool_governance` atoms | Low — stable concepts | Low |
| P2 Prompting | `craf_framework` + `iterative_refinement` atoms | Low — strong base | Low |
| P3 Tool Fluency | CAST framework (new) + live tool landscape research | High — Tavily/Search critical for current tool examples | Medium |
| P4 Configuration | Zero existing content | Medium — technical but documented | High |
| P5 Workflow | `universal_analysis` + `capstone` atoms | Low | Medium |
| P6 Agentic | Zero existing content | Medium — Tavily for real examples | High |

**Recommended generation sequence:** P1 → P2 → P5 (low effort, build momentum) → P3 → P4 → P6 (high effort, informed by prior pillars)

### 2.3 Diagnostic Question — AI-Generated from Onboarding Profile

The single text diagnostic question is **not static** — it is generated by a lightweight agent after the onboarding conversation completes, using the learner's declared role, industry, and daily_work_desc to make it feel personally relevant.

```
DIAGNOSTIC QUESTION GENERATOR [Gemini Flash]
  Input:  {declared_role}, {declared_industry}, {daily_work_desc}
  Prompt: "Generate one scenario-based diagnostic question for a {declared_role}
           in {declared_industry}. The scenario should involve a realistic task
           from their daily work: {daily_work_desc}. The question should reveal
           how the learner currently uses AI tools — without using jargon or
           signalling what the 'correct' answer is. Under 50 words."
  Output: Personalized text question, stored with diagnostic_session
```

Example outputs by role:
- *Teacher:* "You're preparing a differentiated lesson plan for a mixed-ability class next Monday. How would you use AI tools to help?"
- *Marketer:* "You need to launch a campaign for a new product in 3 days with minimal budget. Walk me through how you'd use AI."
- *PM:* "You have a sprint planning meeting tomorrow and the team is misaligned on priorities. How would you use AI to prepare?"

The proposed static fallback ("prepare for an important meeting...") remains as a safe default if generation fails.

---

## 3. Content Topology

### 2.1 The 6-Pillar Framework

| # | Pillar | Transformation | Core question learner can answer after |
|---|--------|---------------|----------------------------------------|
| 1 | **AI Conceptual Foundation** | Confused → Informed | "Why does AI behave like this?" |
| 2 | **Prompting & Context Engineering** | Asking → Communicating | "How do I get AI to do exactly what I need?" |
| 3 | **AI Tool Fluency** | One tool → Right tool | "Which AI tool do I reach for, and why?" |
| 4 | **AI Configuration & Control** | User → Configurator | "How do I shape how AI behaves, not just what I ask?" |
| 5 | **Multi-AI Workflow Design** | Task → Pipeline | "How do I chain AI tools into a repeatable workflow?" |
| 6 | **Agentic System Design** | Pipeline → Autonomous system | "How do I design a system where AI does the work?" |

### 2.2 Pillar Skill Maps

**Pillar 1 — AI Conceptual Foundation**
What LLMs are (probabilistic, not factual) · Model families and tradeoffs (reasoning vs. fast vs. multimodal) · Hallucination patterns and why they happen · The agentic shift: AI that acts vs. responds · AI governance basics: what's safe to put in, why it matters

**Pillar 2 — Prompting & Context Engineering**
Single-turn prompting (role/task/format/constraints) · Multi-step / chained prompting · Reverse prompting (meta-prompting: ask AI to write the prompt) · Chain-of-thought (CoT) · Few-shot prompting · Context engineering (designing full information environment before the model responds) · Persona / role injection · Constraint prompting · Iterative refinement loops

**Pillar 3 — AI Tool Fluency**
Framework: **CAST** (replaces M365-only CSS atom — CAST works for any job, any tool stack)
C — Capability: what does this task require? (generate / analyze / create visuals / write code / research / automate)
A — Access: is the data sensitive? is this tool cleared for it?
S — Source-to-destination: what format does the output need? does it feed into another tool?
T — Tradeoff: speed vs. accuracy vs. cost — what matters most for this specific task?

7 stable tool categories (capability-mapped, specific tools rotate but categories don't):
Conversational reasoning (ChatGPT, Claude, Gemini) · Deep research (Perplexity, Gemini Deep Research, NotebookLM) · Image generation (Midjourney, DALL-E, Ideogram) · Video & audio (Runway, ElevenLabs) · Vibe coding (Cursor, Windsurf, GitHub Copilot) · Workflow automation (n8n, Zapier AI, Make) · Productivity surfaces (M365 Copilot, Notion AI, Google Workspace AI)

> ⚠️ Most perishable pillar. CAST framework is the stable core; tool examples within categories are illustrative and dated.

**Pillar 4 — AI Configuration & Control**
System prompt design (anatomy, persistence, constraints) · Temperature & sampling (creativity vs. precision tradeoffs) · Structured output / JSON schema (machine-readable responses that plug into workflows) · Persona configuration (stable identities for reusable AI assistants) · Memory management (what to keep in context, what to exclude) · Tool/function calling (connecting AI to external actions: search, APIs, calendars) · Output length & format control · Model selection judgment

**Pillar 5 — Multi-AI Workflow Design**
Multi-AI collaboration patterns · Prompt chaining architecture (output A → input B, explicitly designed) · Human-in-the-loop placement (where judgment checkpoints belong) · AI output as structured data (treating responses as data objects, not prose) · Workflow documentation (capturing repeatable AI processes) · Agent orchestration basics (goal + tools → AI plans its own steps)
> P5 = human as orchestrator running tools in sequence

**Pillar 6 — Agentic System Design**
What agentic systems are (AI that plans, decides, and acts across multi-step tasks) · Workflow decomposition (breaking complex tasks into discrete steps) · Agent role assignment (researcher / writer / verifier / orchestrator) · Orchestrator vs. worker pattern · Human-in-the-loop placement in autonomous systems · Workflow transformation (redesigning existing processes around agent teams) · Tool assignment to agents (search, file access, API calls, code execution) · Failure mode thinking (catches without killing speed)
> P6 = AI as orchestrator, human as architect

### 2.3 Content Unit Count

```
18 universal modules (6 pillars × 1 module each)
  × 4 components: reading / practice / evaluation / build artifact
= 72 content units

+ 1 universal diagnostic (6 items: 1 open text + 5 MCQs)
+ 1 gap map template (pillar-scored, not role-scored)
+ 6 pillar badge / credential definitions
+ 1 role injection library (~10 declared role archetypes)
+ 1 Day 7 capstone module
```

vs. current: 35 role-specific courses × 4 components + role taxonomy = ~170 pieces, largely stranded after pivot.

### 2.4 Build Artifacts (per pillar)

Every artifact the learner produces is **stored in their profile** and accessible from a future "My AI Toolkit" page. These are personal assets, not throwaway exercises.

| Pillar | Artifact | Type |
| ------ | -------- | ---- |
| P1 | Personal AI tool selection checklist | Structured checklist |
| P2 | Reusable prompt template for their declared job context | Prompt template |
| P3 | Tool selection decision map (their customized version) | Decision framework doc |
| P4 | A configured system prompt they can deploy immediately | System prompt |
| P5 | Documented 3-step AI workflow for a real task they do | Workflow doc |
| P6 | Agent role definition doc for a process they want to automate | Agent design doc |

**Storage:** Saved to Firestore `build_artifacts` collection (new), linked to `training_progress`. Accessible via future "My AI Toolkit" profile page. Format: plain text / markdown, viewable and copyable in-app.

### 2.5 Asset Reuse Map

**Reuse with adaptation (from `atomic_modules_v2.json`):**
| Existing atom | New home |
|--------------|----------|
| `strategic_prompting__craf_framework` | P2 core framework |
| `strategic_prompting__iterative_refinement` | P2 advanced technique |
| `critical_eval__hallucination_patterns` | P1 reading content |
| `critical_eval__verify_framework` | P2/P6 judgment layer |
| `responsible_ai__safe_framework` | P1 practical application |
| `responsible_ai__ai_tool_governance` | P1 foundation |
| `augmented_comm__surface_workflow` | P3 tool selection framework |
| `augmented_comm__email_message_drafting` | P3 applied practice |
| `data_decision__universal_analysis` | P5 workflow pattern |
| `capstone__end_to_end_workflow` | Day 7 capstone structure |

**Retire:**
- All 35 role-specific courses (`rm_c*`, `uw_c*`, `an_c*`, `mk_c*`, `pm_c*`)
- All 11 role-specific `data_decision` and `relationship_intel` atom variants
- All 54 role-specific diagnostic items
- 6-domain taxonomy (`responsible_ai`, `strategic_prompting`, `critical_eval`, `relationship_intel`, `data_decision`, `augmented_comm`)

**Reuse unchanged:**
- 4-task practice structure and task mode pattern (open/MCQ)
- Reading structure (concept / good_example / anti_pattern / takeaway)
- `call_llm` / `call_llm_stream` / scoring engine in `utils/ai.py`
- Firestore data layer (profiles, progress, coach sessions, ai_call_log)
- All UI components from UX Revamp 2026

---

## 3. Data Model Future State

### 3.1 Core Collections (Firestore)

**`user_profiles/{user_email}`** — extended
```
user_email            string
display_name          string
profile_photo_url     string          # NEW: from OAuth provider
auth_provider         string          # NEW: "google"|"linkedin"|"wechat"|"tiktok" etc.
lang                  "en" | "zh"
declared_role         string          # NEW: e.g. "marketer", "teacher", "PM"
declared_industry     string          # NEW: e.g. "healthcare", "tech"
daily_work_desc       string          # NEW: free-text, used as coach grounding context
current_ai_usage      string          # NEW: free-text, calibrates Day 1 coach depth
primary_motivation    string          # NEW: "job_seeker"|"upskill"|"career_change"|"curiosity"
created_at            timestamp
program_started_at    timestamp       # NEW: Day 0 onboarding complete timestamp
streak_days           int             # NEW
last_active_date      date            # NEW
```

**`diagnostic_sessions/{session_id}`** — restructured
```
session_id        string
user_email        string
completed_at      timestamp
pillar_scores     map             # NEW: {p1: float, p2: float, ..., p6: float}
overall_score     float
item_scores       map
session_number    int             # 1 = baseline, 2+ = re-assessment
```

**`training_progress/{user_email}_{pillar_id}`** — restructured
```
user_email              string
pillar_id               string    # "p1" through "p6", "capstone"
day_number              int       # 1-7
sequence_order          int
is_locked               bool
reading_completed_at    timestamp
practice_completed_at   timestamp
quiz_completed_at       timestamp
quiz_score              float
quiz_passed             bool      # NEW: explicit pass flag
build_artifact          string    # NEW: the artifact the learner produced
build_completed_at      timestamp # NEW
pillar_score_after      float
```

**`coach_sessions/{session_id}`** — minimal changes
```
session_id        string
user_email        string
pillar_id         string          # replaces course_id
day_number        int             # NEW
role_context      string          # NEW: injected at session start
transcript        array
turn_count        int
created_at        timestamp
```

**`credentials/{user_email}_{credential_id}`** — NEW
```
user_email        string
credential_id     string          # e.g. "ai_supercharged_intermediate"
issued_at         timestamp
pillar_scores     map             # snapshot at time of issue
overall_score     float
```

**`learner_model/{user_email}`** — NEW (updated after each day by synthesis agent)
```
user_email            string
natural_strengths     array[string]
recurring_gaps        array[string]
mental_model_notes    string
preferred_framing     string        # "examples" | "challenge" | "abstract" | "concrete"
memorable_quotes      array[string] # verbatim from coach transcripts
daily_summaries       map           # {p1: string, p2: string, ...}
last_updated          timestamp
```

**`build_artifacts/{user_email}_{pillar_id}`** — NEW
```
user_email        string
pillar_id         string          # "p1" through "p6"
day_number        int
artifact_type     string          # "checklist"|"prompt_template"|"system_prompt"|"workflow_doc"|"agent_design"
artifact_title    string          # user-editable label
artifact_content  string          # markdown/plain text; the actual artifact
created_at        timestamp
updated_at        timestamp
```

**`ai_call_log/{log_id}`** — unchanged

### 3.2 Key Schema Changes from Current

| Current field | Future field | Change |
|--------------|-------------|--------|
| `role_id` (rm/uw/an/mk/pm) | `declared_role` + `declared_industry` | Free-form declaration replaces hardcoded role enum |
| `domain_scores` (6 domains) | `pillar_scores` (6 pillars) | Taxonomy rename |
| `course_id` | `pillar_id` | Rename + simplify |
| `domain_score_after` | `pillar_score_after` | Rename |
| — | `quiz_passed` | Explicit pass/fail gate |
| — | `build_artifact` | New artifact storage |
| — | `credentials` collection | New credential layer |
| — | `streak_days` / `last_active_date` | Engagement mechanics |

---

## 4. Architecture Future State

### 4.1 Current Architecture

```
Streamlit (GCP Cloud Run)
  └── Firestore (persistence)
  └── Gemini 2.0 Flash (AI coaching + scoring)
  └── Static content in content/*.json (bundled)
  └── Auth: GCP_USER_EMAIL env var
```

### 4.2 Future Architecture

```
Streamlit (GCP Cloud Run)          ← unchanged runtime
  ├── CONTENT LAYER
  │     ├── Universal modules (content/pillars/*.json)     ← new structure
  │     ├── Role injection library (content/role_contexts.json) ← new
  │     ├── Diagnostic items (content/diagnostic_pillar.json)   ← rebuilt
  │     └── Capstone (content/capstone.json)                    ← new
  │
  ├── AI LAYER
  │     ├── Gemini 2.0 Flash — coaching + scoring          ← unchanged
  │     ├── Role-injected coach prompts (runtime assembly)  ← new
  │     ├── 7-day context injection (pillar scores → coach) ← new
  │     └── Artifact generation assist (closing task)       ← new
  │
  ├── PERSISTENCE LAYER (Firestore)
  │     ├── user_profiles (extended)
  │     ├── diagnostic_sessions (pillar-scored)
  │     ├── training_progress (quiz_passed + build_artifact)
  │     ├── coach_sessions (role_context injected)
  │     ├── credentials (NEW)
  │     └── ai_call_log (unchanged)
  │
  └── CREDENTIAL LAYER (NEW)
        ├── Score card generator (Streamlit HTML component)
        └── LinkedIn / social share deeplinks
```

### 4.3 Content File Structure (Future)

```
content/
  pillars/
    p1_foundation.json
    p2_prompting.json
    p3_tool_fluency.json
    p4_configuration.json
    p5_workflow.json
    p6_agentic.json
    capstone.json
  diagnostic_pillar.json      ← 6 items: 1 open text + 5 MCQs (P1–P5)
  role_contexts.json          ← ~10-15 declared role archetypes with scenario seeds
  domains_b2c.json            ← renamed from domains.json, pillar-mapped
  i18n/
    en.json                   ← extended with new pillar keys
    zh.json                   ← extended
```

### 4.4 Tech Stack Decision — Streamlit vs. Next.js on GCP

**Constraint: Stay on GCP. Gemini API only. All GCP services preferred.**

The frontend framework question (Streamlit vs Next.js) is independent of the cloud provider — both run on Cloud Run. The GCP constraint changes the supporting services, not the migration recommendation itself.

#### Streamlit — Honest Limitations for B2C

| Limitation | Impact on this product |
| --- | --- |
| **No real auth** — `GCP_USER_EMAIL` env var is not real identity; Firebase Auth on Streamlit requires an awkward custom component wrapper | High — social login is a core requirement |
| **Full page reruns on every interaction** — entire script reruns on each widget event; `@st.fragment` is a partial workaround but fragile at scale | Medium — interaction-heavy 7-day practice sessions |
| **No SEO** — client-side rendering only; landing page and module pages not indexable | Medium — B2C organic discovery matters |
| **CSS customisation is a constant battle** — fights internal `data-testid` selectors; each Streamlit version can break custom CSS | Medium — already experienced in UX Revamp 2026 sprint |
| **Mobile UX is degraded** — Streamlit is desktop-first; ZH market is mobile-first | Medium |
| **File upload limits** — Streamlit file uploader has size/type constraints and no preview; needed for capstone screenshot upload | Medium |

#### Next.js on GCP — The Right Frontend, Same Cloud

**Next.js** (App Router) deployed to **Cloud Run** — same infrastructure you use today, same Docker deploy pipeline, same GCP project.

| Capability | GCP-native solution |
| --- | --- |
| **Social auth** | **Firebase Authentication** — Google OAuth native; LinkedIn + Facebook via OIDC; WeChat via custom token |
| **Database** | **Firestore** (keep, GCP-native, already set up) or **Cloud SQL PostgreSQL** (GCP-managed relational DB) |
| **File upload** | **Google Cloud Storage** — for capstone screenshots/artifacts, CDN via Cloud CDN |
| **API routes / AI calls** | Next.js API routes on Cloud Run — calls **Gemini API** exactly as today |
| **SEO** | Next.js server-side rendering — landing page and module pages indexable |
| **Mobile** | React + Tailwind — responsive by default |
| **Real-time streaming** | Server-Sent Events or WebSocket from Cloud Run — same Gemini streaming pattern |
| **Email notifications** | **Firebase Extensions** (Trigger Email) via Cloud Tasks |
| **Deployment** | **Cloud Run** — `gcloud run deploy`, same as today |
| **CDN** | **Firebase Hosting** (global CDN including Asia-Pacific) fronting Cloud Run |

#### Firestore vs Cloud SQL — The DB Question

Staying on GCP gives you a real choice here:

| Feature | Firestore (keep) | Cloud SQL PostgreSQL (upgrade) |
| ------- | ---------------- | ------------------------------ |
| Already set up | ✅ | ❌ migration needed |
| GCP-native | ✅ | ✅ |
| Relational queries, SQL joins | ❌ | ✅ |
| Progress analytics, aggregations | ❌ limited | ✅ |
| Cost at MVP scale | ✅ free tier generous | ✅ ~$10/mo micro instance |
| Schema flexibility (no migrations) | ✅ | ❌ |

**Recommendation: Keep Firestore for MVP.** The data model is already designed for it, it's free at MVP scale, and the B2C pivot doesn't require complex relational queries yet. Migrate to Cloud SQL post-MVP if analytics needs grow.

#### Recommendation: **Migrate frontend to Next.js, stay 100% on GCP**

Streamlit was right for the B2B internal tool. It is the wrong choice for a B2C product. The migration is fully contained within GCP:

- Next.js replaces Streamlit as the frontend — same Cloud Run deployment
- Firebase Authentication replaces `GCP_USER_EMAIL` — GCP-native
- Firestore stays unchanged — zero migration
- Google Cloud Storage added for file uploads — GCP-native
- Gemini API unchanged — same calls, TypeScript wrapper instead of Python

**Nothing leaves GCP.**

#### What Stays Unchanged

- Gemini 2.0 Flash — same API, called from Next.js API routes
- All content JSON files — structure unchanged
- Firestore — same collections, same data
- Cloud Run — same deployment target
- All coaching logic and prompt design — ported to TypeScript, logic identical

### 4.5 Auth Model

**EN market:** Google OAuth · LinkedIn OAuth · Facebook OAuth
**ZH market:** WeChat OAuth · LinkedIn OAuth (post-MVP)

**Implementation:** Firebase Authentication (GCP-native).

- Google: native Firebase provider ✅
- Facebook: native Firebase provider ✅
- LinkedIn: Firebase custom OIDC provider ✅
- WeChat: Firebase custom token — backend completes WeChat OAuth flow, mints a Firebase custom token ✅ (requires Weixin Open Platform registration with Chinese business entity or licensed partner)

> ⚠️ **WeChat constraint:** Requires Chinese business registration or licensed partner for Weixin Open Platform app. MVP launches with Google + LinkedIn + Facebook. WeChat added when entity is established.

Social login only — no email/password.

### 4.6 Capstone Scoring Rubric

Mixed-format assessment (text input + screenshot/image upload + MCQ). Proposed weighting:

| Component | Weight | Scoring method |
| --- | --- | --- |
| **MCQ questions** (3 questions) | 30% | Deterministic — correct/incorrect, 0 or 1 per question |
| **Text response** (1 open prompt: "describe your workflow") | 40% | LLM-scored against rubric (same `_score_batch` pattern); rewards specificity + structured thinking |
| **Screenshot / artifact upload** (1 upload: "show your AI tool output") | 30% | LLM vision scoring (Gemini multimodal): does the screenshot demonstrate the pillar skill? Rubric: correct tool used (10%), appropriate prompt visible (10%), output quality/verification (10%) |

**Pass threshold:** Overall capstone score ≥ 2.5 / 4.0 (consistent with daily quiz threshold).

**Time constraint:** Under 15 min total. MCQs take ~3 min, text response ~5 min, screenshot capture + upload ~2 min, AI scoring ~1 min. Learner is explicitly told: "Use your AI tools to help you answer."

**Retake:** Same as daily quiz — immediate retake with coach hints.

### 4.7 Post-7-Day Funnel

On credential issuance, learner sees:

```
🎉 You've completed the 7-day AI Transformation!

[Credential card + share buttons]

What's next?
  → Join our community: [WeChat QR code]
     Get early access to advanced courses, live sessions, and peer learning.
```

WeChat group QR code is the primary CTA. No hard sell. The group is the audience-building mechanism for future paid courses.

### 4.8 Key Architectural Decisions

✅ **Migrate frontend to Next.js, stay 100% on GCP** — Streamlit unsuitable for B2C; Next.js on Cloud Run is identical deployment
✅ **Database: Firestore** — GCP-native, already set up, free at MVP scale; Cloud SQL post-MVP if needed
✅ **Auth: Firebase Authentication** — GCP-native; Google + Facebook native; LinkedIn via OIDC; WeChat post-MVP
✅ **File storage: Google Cloud Storage** — GCP-native; capstone uploads + Cloud CDN
✅ **Deployment: Cloud Run** — unchanged; same Docker deploy pipeline
✅ **CDN: Firebase Hosting** — fronts Cloud Run; global including Asia-Pacific
✅ **Gemini 2.0 Flash** — unchanged; called from Next.js API routes; multimodal vision for capstone screenshot scoring
✅ **P3 content refresh** — Gemini + Brave Search researcher agent → ingestion-ready JSON → human review → redeploy
✅ **Streak notifications** — Firebase Extensions (Trigger Email) + Web Push; in-app fallback
✅ **Static content bundled** — all pillar JSONs bundled with app; no DB queries for content

---

## 5. UI/UX Future State

### 5.1 Page Map (Future)

```
00_Welcome.py          ← redesign: B2C value prop, social proof, 7-day promise
01_Onboarding.py       ← NEW: role declaration + diagnostic (replaces current Diagnostic)
02_Dashboard.py        ← replaces current Home; 7-day progress view, streak, gap map
03_Daily_Module.py     ← replaces Course_Module; unified reading/practice/quiz/build
04_Skills_Profile.py   ← keep; redesign for pillar scoring + credential display
05_Credential.py       ← NEW: credential display page with social share buttons
```

### 5.2 UX Design Principles (B2C)

**From B2B (compliance-driven) → B2C (motivation-driven):**

| B2B principle | B2C principle |
|--------------|--------------|
| Role/employer anchored | Learner career-anchored |
| Complete the program | Build your AI toolkit |
| Score visible to manager | Score private, credential shareable |
| 7 modules in order | 7 days with daily momentum |
| Framework names prominent (CRAF, SAFE) | Outcome language prominent ("write better prompts") |

**Key UX patterns to adopt (informed by Duolingo, Uxcel):**
- **Onboarding under 2 min** — role declaration + one warm-up question; no friction before first win
- **Day counter prominent** — "Day 3 of 7" is always visible; creates commitment and urgency
- **Streak mechanic** — daily return driver; gentle nudge if day not started by evening
- **Build artifact gallery** — visible accumulation of personal toolkit; tangible progress beyond scores
- **One-screen-one-task** — diagnostic questions and practice tasks are one per screen (already implemented in UX Revamp 2026 ✅)
- **Coach as conversation partner** — not a grader; tone is encouraging and curious, not evaluative
- **Credential as climax** — Day 7 completion is a moment, not a checkbox; visual celebration + immediate share CTA

### 5.3 Onboarding Flow — Detailed Design

Replaces current Diagnostic page. One question per screen. Feels like the coach getting to know you — not a form.

**Screen 0 — Welcome + Login**
3-line value prop ("Become AI-supercharged in 7 days. Free. Personalized. Proven.") + social login buttons + EN/中文 toggle. No product wall-of-text before login.

**Screen 1 — Role Declaration**
Two mobile-stacked dropdowns: job function (~12 options) + industry (~10 options). "Other" on both opens free-text. Stores: `declared_role`, `declared_industry`.

**Screen 2 — Daily Work (multi-select, NOT blank text)**
Headline: "What does a typical workday look like for you?"
Multi-select checkboxes (2-3 encouraged), not free text — mobile-first, higher completion:
Writing & editing · Data analysis & reporting · Client/stakeholder relationships · Meetings & coordination · Research & synthesis · Code & technical work · Content & campaigns · Other (free text)
Stores: `daily_work_tasks: [array]` — used by scenario seed generator.

**Screen 3 — AI Experience Level**
Headline: "How would you describe your current AI experience?"
Single select (4 options):
- I use AI tools daily — they're part of my workflow
- I use AI occasionally when I remember to
- I've experimented a few times but don't have a routine
- I'm brand new to AI tools
Stores: `current_ai_usage` band → maps to coach depth (daily/occasional/experimenting/new).

**Screen 4 — Motivation**
Headline: "What brought you here?"
Single select (4 options):
- Looking for a new job and want to stand out
- Want to use AI better in my current role
- Changing careers, need to future-proof
- Just curious
Stores: `primary_motivation` → coach uses this to frame "why this matters" in every session.
Job seekers hear: "here's how to talk about this in an interview."
Upskilling users hear: "here's how this applies to your current workflow."

**Transition screen — Setup moment**
Brief purposeful pause (not a spinner): "Setting up your personalized program... We're using your answers to generate a diagnostic that fits your work context."
This is when the diagnostic text question generator fires (Gemini Flash, ~2 sec).

**Screen 5 — Diagnostic Text Question (AI-generated)**
Headline: "One last thing — a quick snapshot of where you are today"
Subtext: "5 minutes. No wrong answers. This is for you, not a grade."
The AI-generated scenario question appears here, personalized to role + daily_work_tasks.
Character counter visible (encouraging, not limiting). Placeholder: "e.g., 'I'd start by asking ChatGPT to...'"
Static fallback if generation fails: "You have an important meeting tomorrow with someone you don't know well. Describe exactly how you would use AI tools to help you prepare."

**Screens 6–10 — 5 MCQs (one per screen)**
Scenario-based, best-practice format. Progress bar: "Question 2 of 5". No timer.

| Q | Pillar | Scenario angle |
| - | ------ | -------------- |
| 1 | P1 | "AI gives a confident-sounding answer. What do you do next?" |
| 2 | P2 | "Your first prompt gives a generic response. What's your next move?" |
| 3 | P3 | "You need to turn a long report into a 5-slide deck. Which approach?" |
| 4 | P4 | "You use the same AI assistant daily for similar tasks. What's smartest to set up once?" |
| 5 | P5/P6 | "You have a 5-step weekly process. AI could help with 3 steps. How do you approach it?" |

**Screen 11 — Gap Map Reveal**
Language-first, bands not raw scores. Radar chart (6 pillars, lightly filled).
1-2 sentence AI-generated summary: "Based on your responses, you have solid instincts around prompting and AI awareness. Your biggest growth opportunities are in Configuration and Agentic Systems — also the highest-leverage skills in 2026."
3 diagnostic bands:

| Band | Signal | Coach adjustment |
| ---- | ------ | ---------------- |
| New to AI | Text vague, P1/P2 wrong | More scaffolding, slower pace |
| Casual user | Basic structure, 2–3 MCQ correct | Assumes familiarity, pushes depth |
| Already fluent | Structured + specific, 4–5 MCQ correct | Skips basics, probes judgment + edge cases |

CTA: [Begin Day 1 →] — prominent, no friction.

### 5.4 Dashboard Design (Day View)

```
Header:   "Day 3 of 7 · 🔥 3-day streak"
Progress: [■■■□□□□] 3/7 pillars complete

TODAY
  [P3 card]  AI Tool Fluency
             Reading · Practice · Quiz · Build
             [Begin Day 3 →]

COMPLETED
  [P1 ✓]  AI Conceptual Foundation  · Score 3.4/4
  [P2 ✓]  Prompting & Context       · Score 3.1/4

COMING UP
  [P4]  AI Configuration & Control  (unlocks tomorrow)
  [P5]  Multi-AI Workflow Design
  [P6]  Agentic System Design
  [⚡] Capstone Challenge
```

### 5.5 Credential Display

```
┌─────────────────────────────────────────┐
│  ⚡ AI Hero Academy                      │
│                                         │
│  AI-Supercharged Intermediate           │
│                                         │
│  [Name]                                 │
│  Issued: March 2026                     │
│                                         │
│  Pillar scores:                         │
│  P1 ●●●●  P2 ●●●○  P3 ●●●●             │
│  P4 ●●○○  P5 ●●●○  P6 ●●●●             │
│                                         │
│  Overall: 3.3 / 4.0                     │
│                                         │
│  [Share on LinkedIn]  [Download PDF]    │
└─────────────────────────────────────────┘
```

---

## 6. AI Coach — Core Competitiveness

> The AI coach is the primary differentiator of the product. Not the content, not the credential — the coach.
> Full gap analysis + PACE model: see `plans/b2c-ai-coach-gap-analysis.md`

### 6.1 The PACE Coaching Model

The coach is not a journalist. It does not probe for its own sake. Every task interaction follows PACE:

- **P — Purpose:** Declare the learning objective before generating a question
- **A — Assess:** Read both intellectual signal (what they understood) AND emotional signal (how they feel)
- **C — Choose:** Challenge / Clarify / Celebrate / Support based on assessment
- **E — Exit:** Close the task the moment the learning objective is met. Never linger.

**3-question hard ceiling per task:**

- Q1 — Open probe: surface current thinking
- Q2 — Adaptive: challenge if shallow / affirm and extend if good
- Q3 — Synthesis: consolidate + bridge to build artifact
- Early exit: objective met after Q1/Q2 → close immediately
- Budget exhausted: give direct insight + close. Never a 4th question.

**Emotional state detection:**

| Signal | Coach response |
| ------ | -------------- |
| Short / dismissive | Reframe without pressure: "Let me try a different angle..." |
| Frustrated / wrong repeatedly | Stop questioning. Give insight directly with warmth. |
| Overconfident / surface-level | Gentle challenge: "Push one level deeper — what happens when...?" |
| Genuinely insightful | Explicit celebration + close. No more questions. |
| Confused / lost | Simplify + ground in their specific work context. |

**4 coach tones** — shifts naturally between: Curious (default) · Celebratory · Supportive · Challenging

### 6.2 Ultra-Personalization — The Secret Sauce

Five layers of personalization, compounding across 7 days:

| Layer | What it does | Most products reach |
| ----- | ------------ | ------------------- |
| L1 Profile | Role + industry + job context in every example | ✅ Common |
| L2 Performance | Adjusts challenge based on today's quiz score + retries | ⚠️ Rare |
| L3 Cross-day memory | Day 4 coach knows what you revealed on Day 1 | ❌ Almost nobody |
| L4 Learner model | Continuously updated portrait: strengths, blind spots, preferred framing | ❌ Nobody |
| L5 Work-grounded reality | Every example generated from learner's actual daily_work_desc | ❌ Nobody |

**The WOW moment** — by Day 3 the coach says:
> *"You mentioned on Day 1 that you usually paste the whole email into ChatGPT. What you're building right now is exactly the habit that replaces that. Let's make it specific to your Friday briefing workflow."*

### 6.3 The Learner Model — Living Firestore Document

A synthesis agent (Gemini Flash) runs after each day's session completes and updates:

```
learner_model/{user_email}:
  natural_strengths:    ["structured output thinking", "safety awareness"]
  recurring_gaps:       ["tends to trust AI output without verifying"]
  mental_model_notes:   "Thinks of AI as a search engine, not a collaborator"
  preferred_framing:    "responds to concrete examples over abstract rules"
  memorable_quotes:     ["I always just paste the whole email in"]
  daily_summaries:
    p1: "Strong on hallucination awareness, weak on model selection"
    p2: "Good CRAF instinct, skips context layer when rushed"
```

Injected into every subsequent coach session. By Day 4 the coach has a richer understanding of this learner than any 45-minute onboarding quiz could produce. **The product compounds — every day makes it more valuable.**

### 6.4 Work-Grounded Scenario Generation

At each session start, a scenario seed agent generates a task context from the learner's profile — never a generic placeholder:

```
Input:  daily_work_desc + declared_role + declared_industry + current pillar
Output: Role-specific scenario seed for practice tasks

Example — Analyst in retail:
"You compile weekly KPI dashboards for 3 retail brands and send exec
 summaries every Friday. Today you're setting up a system prompt for
 an AI assistant that drafts that summary. Your 3 audiences have
 different detail tolerance levels."
```

### 6.5 Coach Identity Template

```
You are a personal AI transformation coach in AI Hero Academy.
Your learner is a {declared_role} in {declared_industry}.
They are on Day {day_number} of their 7-day AI transformation program.

What you know about this learner:
- Daily work: {daily_work_desc}
- Prior performance: {learner_model_summary}
- Today's scenario: {generated_scenario_seed}

PACE model (non-negotiable):
- Maximum 3 questions per task. Never a 4th.
- Exit immediately when the learning objective is met — do not probe further.
- Detect emotional signals. Respond to the person, not just the content.
- Never write the answer. Guide through questions unless budget is exhausted.
- Bridge every task close to what comes next.
- [Pillar-specific framework and probe library below]
```

### 6.6 Coaching Frameworks — All 6 Pillars

| Pillar | Framework | Mental model shift |
| ------ | --------- | ------------------ |
| P1 Foundation | **MAPS** (Mechanism / Accuracy / Probabilistic / Spectrum) | "AI is a lookup" → "AI is probabilistic, spectrum from response to agent" |
| P2 Prompting | **CRAF** (existing atom) | "AI understands me" → "I need to communicate precisely" |
| P3 Tool Fluency | **CAST** (Capability / Access / Source-to-destination / Tradeoff) | "I use one tool" → "right tool for right task" |
| P4 Configuration | **BRIEF** (Background / Role / Instructions / Expected output / Fence) | "I prompt fresh each time" → "I set up AI like briefing a team member" |
| P5 Workflow | existing atoms (TRACE + capstone patterns) | "I use AI for tasks" → "I chain AI into pipelines" |
| P6 Agentic | **CREW** (Capabilities / Roles / Escalation / Workflow) | "I orchestrate AI" → "I design a team of AI workers" |

**MAPS probe vocabulary (P1):**
M — "When ChatGPT answers confidently, what's it actually doing under the hood?"
A — "What tasks would you trust AI output on without checking? What always needs verification?"
P — "If you run the same prompt twice, would you expect the same answer? Why or why not?"
S — "What's the difference between asking ChatGPT a question and giving an agent a goal?"
Mastery signal: can explain *why* AI hallucinates + can place 3 tools on the agency spectrum.

**CAST probe vocabulary (P3):**
C — "What does this task fundamentally require — generating, analyzing, creating visuals, writing code, researching, or automating?"
A — "What data are you working with here? Could any of it be sensitive or internal? Is this tool cleared for that?"
S — "Where does this output go — are you using it directly, or does it feed into another tool? What format does it need to arrive in?"
T — "For this specific task, what's the priority — speed, accuracy, or cost?"
Wrong patterns: public tool + confidential data (A fail) · wrong capability match (C fail) · output format mismatch (S fail) · slow model for bulk simple task (T fail)
Mastery signal: applies CAST to an unfamiliar tool and correctly identifies category + constraint profile.

**BRIEF probe vocabulary (P4):**
B — "What would you put in a system prompt for an assistant that helps you every Monday morning?"
R — "If your AI assistant had a job title, what would it be? What's its briefing?"
I — "What 3 things must it always do? What 2 things must it never do?"
E — "What format makes the output immediately usable without reformatting?"
F — "What single instruction prevents its most likely mistake for your work?"
Mastery signal: can write a working system prompt for a recurring real task — not generic.

**CREW probe vocabulary (P6):**
C — "What tools does each agent need — search, files, calendar, code? What context does it start with?"
R — "Which agent decides what happens next? Which ones execute? What if a worker gets it wrong?"
E — "At which step does a human check before the system continues? What triggers escalation?"
W — "What does agent A hand to agent B? Text, structured data, a decision? What breaks if the handoff is messy?"
Mastery signal: can sketch a 3-agent workflow for a real task — naming roles, tools, handoffs, one human checkpoint.

### 6.7 Coach Session Lifecycle

```
USER ARRIVES FOR DAY N
        ↓
[1] SCENARIO SEED GENERATOR (sync, ~2 sec, Gemini Flash)
        ↓
Session renders with personalized scenario
        ↓
Task 1 → Task 2 → Task 3 → Task 4  (PACE, 3 questions max each)
        ↓
[2] BUILD ARTIFACT MECHANIC (after Task 4, sync)
    Coach bridge statement → artifact prompt → learner submits → ONE coach review → close
    Artifact saved to build_artifacts/{user_email}_{pillar_id}
        ↓
Session marked complete
        ↓
[3] SYNTHESIS AGENT (async, background, Gemini Flash, temp 0.1)
    Reads full transcript → extracts learner_model update → writes to Firestore
    On failure: log + skip silently, next day's synthesis catches up
```

**[1] Scenario Seed Generator**
Input: declared_role + declared_industry + daily_work_desc + pillar + learner_model summary
Output: {scenario_text, task_context, fictional_entity}
Fallback: role_contexts.json archetype default — never blocks session

**[2] Build Artifact Prompts (per pillar)**

| Pillar | Artifact prompt |
| ------ | --------------- |
| P1 | "Write your personal AI reliability checklist — 5 checks you'll run before trusting any AI output in your {role} work." |
| P2 | "Write a reusable prompt template for the task you practiced today, specific to your actual workflow." |
| P3 | "Build your personal AI tool selection map: for each task type you do regularly, which tool category fits and why." |
| P4 | "Write the system prompt you would actually deploy for your most recurring AI task. Not a template — yours." |
| P5 | "Document the 3-step AI workflow you designed: each step, tool, input, and output. Make it repeatable." |
| P6 | "Sketch the agent workflow you designed: agent names, roles, tools, handoffs, and the one human checkpoint." |

Coach review after artifact submission: ONE pass only — affirm and close, or one improvement suggestion then close regardless. Not PACE.

**[3] Synthesis Agent Output Schema**
```json
{
  "natural_strengths_add":    ["new strength observed"],
  "recurring_gaps_add":       ["new gap observed"],
  "mental_model_update":      "updated one-line mental model description",
  "preferred_framing_update": "examples | challenge | abstract | concrete",
  "memorable_quotes_add":     ["verbatim quote from transcript"],
  "pillar_summary":           "one-line performance summary for this pillar"
}
```
Merge: additive for arrays, replace for strings. Timestamp updated.

**Lifecycle summary**

| Moment | Model | Sync | Fallback |
| ------ | ----- | ---- | -------- |
| Scenario seed | Gemini Flash | ✅ Sync ~2s | role_contexts default |
| Build artifact | Template + coach | ✅ Sync | Static pillar prompt |
| Synthesis agent | Gemini Flash 0.1 | ❌ Async | Log + skip |

### 6.8 Remaining Implementation Specs

| Item | Severity | Status |
| ---- | -------- | ------ |
| Universal B2C data safety guardrail (1 paragraph rewrite) | Medium | ⬜ During build |
| `_LANG_INSTRUCTION` updated for AI-native terms | Low | ⬜ During build |

---

## 7. Open Questions

- ⬜ **"My AI Toolkit" profile page** — postponed to post-MVP
- ⬜ **WeChat OAuth** — requires Chinese business registration or licensed partner; EN market launches first with Google/LinkedIn/Facebook; WeChat added when entity established
- ⬜ **Credential annual re-certification** — post-MVP; not in launch scope

---

## 8. Decided

### Learning Model

✅ **No level design** — one module per pillar; all targeting intermediate on completion
✅ **7-day linear arc** — no adaptive routing; diagnostic informs coach emphasis only
✅ **Quiz pass threshold** — score ≥ 2.5 / 4.0
✅ **Quiz fail handling** — immediate unlimited retake; coach hints surfaced alongside questions on retry
✅ **Day 7 capstone** — AI-coached challenge; text input + screenshot/code upload + MCQ; under 15 min; learner encouraged to use their own AI tools; pass threshold ≥ 2.5
✅ **Capstone scoring** — MCQ 30% (deterministic) + text response 40% (LLM rubric) + screenshot/artifact 30% (Gemini multimodal vision scoring)

### Product & Business

✅ **Monetization** — permanently free; top-of-funnel for paid online courses; post-7-day CTA = WeChat group QR code
✅ **Auth** — Firebase Authentication (GCP-native); Google + LinkedIn + Facebook (EN launch); WeChat post-MVP pending entity registration
✅ **Credential** — LinkedIn AI Skills Endorsement + social-shareable badge (LinkedIn, WeChat, Xiaohongshu, TikTok) + PDF certificate; no expiry at MVP
✅ **Language** — bilingual EN + ZH at all times; never EN-first

### Content

✅ **Pillar 6 = Agentic System Design** — replaces compliance-flavored framing
✅ **Pillar 5 vs 6 boundary** — P5 = human-orchestrated pipeline; P6 = AI-autonomous system designed by human
✅ **Role injection at runtime** — no hardcoded roles; user declares context at personalization onboarding
✅ **AI Coach = core product differentiator** — PACE model (3-question budget, emotional detection, mastery exit), ultra-personalization (5 layers), learner model (Firestore, updated daily by synthesis agent), work-grounded scenario generation at session init
✅ **Coaching frameworks — all 6 pillars decided:** P1=MAPS, P2=CRAF, P3=CAST, P4=BRIEF, P5=existing atoms, P6=CREW
✅ **Onboarding replaces diagnostic gate** — rich personalization conversation (daily_work_desc, current_ai_usage, motivation) + 6-item diagnostic (1 text + 5 MCQ, ~5 min); diagnostic is not a gate, just a calibrator; P6 score inferred from P5
✅ **P3 content strategy** — decision framework as stable core for MVP; tool examples illustrative and dated
✅ **Build artifacts** — stored in DB `build_artifacts` table; accessible from future "My AI Toolkit" page (post-MVP); plain text/markdown; viewable + copyable in-app; user-editable title
✅ **35 role-specific courses retired** — stranded after pivot

### Technical

✅ **Migrate frontend to Next.js, stay 100% on GCP** — Streamlit unsuitable for B2C; Next.js on Cloud Run, Firebase Auth, Firestore, GCS — nothing leaves GCP
✅ **Database: Firestore** — keep for MVP; GCP-native, already set up, free tier covers MVP scale; Cloud SQL post-MVP if analytics needs grow
✅ **Auth: Firebase Authentication** — GCP-native; Google + Facebook native; LinkedIn via OIDC; WeChat via custom token post-MVP
✅ **File storage: Google Cloud Storage** — GCP-native; capstone uploads with Cloud CDN
✅ **Deployment: Cloud Run** — unchanged; Next.js deploys via Docker to Cloud Run same as Streamlit today
✅ **CDN: Firebase Hosting** — fronts Cloud Run; global CDN including Asia-Pacific
✅ **P3 content refresh** — Gemini + Brave Search researcher agent pipeline → ingestion-ready JSON → human review → redeploy
✅ **Streak notifications** — Firebase Extensions (Trigger Email) + Web Push; in-app banner fallback
✅ **Existing coaching logic reusable** — one-question discipline, streaming, task guidance, no-answers rule all carry forward; ported to TypeScript API routes
✅ **Gemini 2.0 Flash** — unchanged; called from Next.js API routes; Gemini multimodal vision for capstone screenshot scoring
