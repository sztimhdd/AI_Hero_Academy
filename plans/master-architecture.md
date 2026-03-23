# Architectural Brainstorm: Atomic Modular Learning vs. Role-Based Curriculum

> Status: **In execution** — Phases 0–2 complete. Phase 3 (Path Assembler) is next.
>
> **Current app status (March 2026):** Five roles live (RM, UW, AN, MK, PM). 6-domain hexagon architecture. Bilingual UI — English / Chinese language switching via `utils/i18n.py` + `content/i18n/{en,zh}.json`; language persisted in Firestore user profile. Reading sub-view uses 4 visual section templates (Phase 14). MCQ hybrid practice model live across all 5 roles.
>
> **Atomic library status:**
>
> - `content/atomic_modules.json` — 35 role-specific draft atoms (5 roles × 7 courses), status="draft"
> - `content/atomic_modules_v2.json` — 15 canonical atoms (5 universal + 10 role-variant), status="canonical"/"role-variant"; task_mode + mcq_options patch pending
> - `content/atomic_overlap_report.json` — 6 merge groups documented
> - `content/atomic_diagnostic_items.json` — 36 items (covering all 5 roles)
> - `content/domains_universal.json` — 6 domains × 4 role variants
>
> **Phase completion:**
>
> - ✅ Phase 0: RM + UW + AN + MK live
> - ✅ Phase 0.5: Atomic data model + conversion pipeline (atomize_coursework.py)
> - ✅ Phase 0.6: Atomic diagnostic items
> - ✅ Phase 0.7: Universal domain descriptors
> - ✅ Phase 1 (PM): PM role content ingested and atomized (Engineer deferred to Phase 4)
> - ✅ Phase 2: Atom merge → canonical v2 library (scripts/merge_atoms.py); patch in progress
> - ✅ i18n: Bilingual EN/ZH infrastructure with browser lang detection
> - ✅ Phase 3: Path assembler + dynamic onboarding — 34/34 UAT checks pass (2026-03-23)

---

## Design Decisions (From Clarification)

| Question | Decision |
|---|---|
| Atom granularity | Same as today's module (reading + practice + eval, ~30 min) |
| Diagnostic | Keep both — intake form + 6-domain diagnostic, both feed path assembler |
| Scenario context | AI-generated at runtime from template + learner's stated context |
| Build sequence | Add PM + Engineer first (to map ~80% of atomic capabilities), then refactor |

---

## The Core Architecture (Target State)

```
LIBRARY LAYER
─────────────────────────────────────────────────────────────────────
  N atomic capability modules (role-agnostic)
  Each module has:
    - reading: generic AI capability explanation (no role coupling)
    - practice: task_template with {role}, {context}, {task} placeholders
    - eval: rubric that scores the AI capability (role-invariant)
    - scenario_template: base scenario + LLM fill instruction
    - domain: one of 6 domains (unchanged)
    - capability_tags: ["SAFE_framework", "prompt_scoping", ...]

ONBOARDING LAYER
─────────────────────────────────────────────────────────────────────
  Intake form:
    - Role description (free text, guided: "I manage X, my team does Y")
    - Top 3 daily AI use cases (multi-select or free text)
    - Biggest AI pain point ("what frustrates you most?")
  +
  6-domain diagnostic (existing, shortened to 6 items per domain split)
    → Outputs: domain gap scores (0–4 per domain)

PATH ASSEMBLER
─────────────────────────────────────────────────────────────────────
  Inputs:
    - Intake profile (role + use cases + pain points)
    - Diagnostic gap scores (domain priorities)
  Logic:
    - Filter: tags matching user's stated use cases → candidate set
    - Rank: by domain gap score (largest gap = highest priority)
    - Sequence: quick-win first (score 1.5–2.5) → gaps (< 1.5) → rest
    - Assemble: personalized path of N atoms (today: 5–7 modules)
  Output:
    - Ordered list of atom IDs with assembled scenario context

RUNTIME SCENARIO GENERATION (per practice/eval session)
─────────────────────────────────────────────────────────────────────
  Inputs: atom.scenario_template + learner.role_description + learner.use_cases
  LLM call (Haiku, temperature=0.4):
    "Given this generic scenario template and this learner's role context,
     produce a specific scenario in 2-3 sentences."
  Fallback: if LLM fails → use generic scenario template directly
```

---

## The "PM + Engineer First" Strategy — My Recommendation

**I agree with your instinct, with one critical modification.**

Adding PM and Engineer now is the RIGHT move strategically, but only if we author that content as **atomic-ready from day one** — not in the current role-coupled format.

### Why two more roles first makes strategic sense

1. **Overlap mapping**: 5 roles × 6 domains reveals which capabilities are truly universal vs. genuinely role-specific. That overlap IS the atomic library blueprint.
2. **Continued delivery**: We keep shipping value (2 more complete role curricula) while building toward v2.
3. **Proof-of-concept**: PM + Engineer become the template for AI scenario generation. If it works for them, retrofitting RM/UW/AN is pattern-proven.
4. **Content economics**: If "Strategic Prompting" is needed by all 5 roles, we write it ONCE as an atom, not 5 times. The atomic approach may actually **reduce** total content volume vs. adding 14 more role-specific modules.

### The critical modification: author PM + Engineer as atoms, not roles

**If we author PM + Engineer the same way we did RM/UW/AN, we create MORE migration debt.**

Instead, PM + Engineer modules should be authored with:
- `scenario_template` field (not `scenario`) — with placeholders for LLM to fill
- Generic reading content (no "as an analyst" or "as an RM" framing)
- Capability tags (for path assembly matching, not role_id coupling)
- A `role_variants_hint` field (a sentence telling the LLM how to adapt per role context)

This changes the content generation pipeline (the authoring prompt in `generate_course_content.py` needs one new system instruction). The output JSON adds two fields per module. Existing RM/UW/AN modules stay untouched until the migration phase.

### Content overlap prediction (before we write a line)

Based on the 6-domain model, my prediction of capability universality across roles:

| Domain | Universal? | Prediction |
| --- | --- | --- |
| `responsible_ai` | Very high | SAFE/VERIFY frameworks apply identically across RM, UW, AN, PM, Eng |
| `strategic_prompting` | High | Core prompting technique is universal; only scenario context differs |
| `critical_eval` | High | Evaluating AI output is a universal cognitive skill |
| `data_decision` | Medium | Data context is role-specific (loan data vs. project data vs. code review) |
| `relationship_intel` | Low | Genuinely role-specific (RM: client; PM: stakeholder; Eng: team) |
| `augmented_comm` | High | Document generation, meeting prep → nearly universal |

**Implication**: 4 of 6 domains can likely be represented by 1 atom each (used by all roles). Only `data_decision` and `relationship_intel` may need role-variant atoms. That's ~4 universal + 2 per-role = **4 + (2 × N roles) atoms total** — far fewer than N roles × 7 courses.

At 5 roles: ~14 atoms. At 10 roles: ~24 atoms. **Sublinear content growth** — this is the core value of the atomic architecture.

---

## Sequenced Roadmap (Chief Architect's Recommendation)

### Phase 0 — NOW (in progress): Ship RM + UW + AN
Complete the current role-based system. Reading templates, diagnostic shortening, AN content — all in progress. Ship and validate with real users.

### Phase 0.5 — Atomic Data Model + Conversion Pipeline

> Inserted between Phase 0 (ship) and Phase 1 (new content).
> Goal: design the atom schema, build the atomization factory, convert all 21 existing modules.
> The app DOES NOT change — it keeps running on the original JSON files.
> Output is a parallel `content/atomic_modules.json` ready for Phase 1 and Phase 3 to activate.

#### Sub-task A — Atomic JSON Schema Design

Define the canonical structure for `content/atomic_modules.json`.

Each atom is a COMPLETE, self-contained object (no runtime dependency on original JSON files):

```json
{
  "atom_id": "responsible_ai__safe_framework",
  "title": "Safe AI Prompting: The SAFE Abstraction Method",
  "domain": "responsible_ai",
  "capability_tags": ["SAFE_framework", "data_classification", "prompt_abstraction", "data_privacy"],
  "estimated_minutes": 30,
  "role_variants_hint": "For financial services: emphasize client data (KYC, credit files, NPI). For engineering: emphasize code secrets and API credentials. For ops/admin: emphasize internal process records. Adjust {data_type} and {compliance_context} placeholders accordingly.",
  "reading": {
    "concept_text": "...",       // de-roled: no 'as an analyst' framing; 'as a professional'
    "good_example": "...",       // generic fictional org (keep Meridian, Aurora etc. OK — they're already fictional)
    "anti_pattern": "...",       // mostly role-agnostic already
    "takeaway": "..."            // almost always fully generic
  },
  "practice": {
    "scenario_template": "You are a {role} at {org_type}. A {case_type} has been opened containing {data_types} — classified as {sensitivity_level}. Your manager has asked you to use AI to {workflow_goal}. Apply the SAFE Abstraction Method before each prompt.",
    "task_templates": [
      {
        "task_id": 1,
        "text_template": "...",  // de-roled; {programme_name} replaces 'Meridian Infrastructure Briefing'
        "skill_focus": "Apply SAFE Step 1: Scrutinize sensitive elements"
      }
    ],
    "coach_system_prompt_template": "..."  // de-roled; {role}, {organisation}, {scenario_name} as placeholders
  },
  "eval": {
    "items_ref": "evaluation_items.json",  // Phase 0.5: reference only; full de-role in Phase 2
    "source_course_ids": ["rm_course_1", "uw_course_1", "an_c1_responsible_ai"]
  },
  "source_course_ids": ["rm_course_1", "uw_course_1", "an_c1_responsible_ai"],
  "atomized_at": "2026-03-06",
  "status": "draft"
}
```

**Placeholder naming convention** (consistent across all atoms):

| Placeholder | Meaning |
|---|---|
| `{role}` | Learner's job title ("Relationship Manager", "Software Engineer") |
| `{org_type}` | Organization type ("financial services firm", "technology company") |
| `{case_type}` | Type of work case ("client onboarding file", "code review ticket") |
| `{data_types}` | What data is present ("incorporation documents, credit scores") |
| `{sensitivity_level}` | Classification ("Non-Public", "Confidential", "Internal") |
| `{workflow_goal}` | Task objective ("accelerate the verification process") |
| `{programme_name}` | Name of the project/programme ("Q3 Performance Review") |
| `{audience}` | Target audience ("Executive Committee", "technical lead") |

#### Sub-task B — Build `scripts/atomize_coursework.py`

Multi-agent LLM pipeline. Same SDK pattern as `enrich_reading_content.py`:
WorkspaceClient, tenacity retries, HAIKU_ENDPOINT, ThreadPoolExecutor(4), temperature=0.

**5 extraction calls per course** (sequential within a course, concurrent across courses):

1. **TAG_EXTRACTION** — input: `title + description` → output: `capability_tags` (JSON array, 3–6 tags)
2. **SCENARIO_TEMPLATE** — input: `scenario_text` → output: `scenario_template` (de-roled with `{}` placeholders)
3. **TASK_GENERALIZATION** — input: `task_1_text...task_4_text` → output: `task_templates[]` (remove fictional specifics, keep skill focus; preserve step numbers and headings)
4. **COACH_GENERALIZATION** — input: `coach_system_prompt` → output: `coach_system_prompt_template` (de-role organization, programme name, job title; insert `{role}`, `{scenario_name}`, `{organisation}`)
5. **ROLE_HINT** — input: `scenario_text + concept_text` → output: `role_variants_hint` (1–2 sentences: what changes across roles; which placeholders matter most)

**Reading content** (6th call, lighter):
- Light de-role pass on `concept_text` only: remove "As an analyst" → "As a professional"; keep all framework explanation intact
- `good_example`, `anti_pattern`, `takeaway` → copy as-is (already mostly role-agnostic; fictional org names are acceptable)

**Overlap detection** (post-processing, no LLM needed):
- Group atoms by `(domain, capability_tags overlap > 70%)` using simple set intersection
- Output `content/atomic_overlap_report.json`: list of merge candidate groups with source_course_ids
- No merging in Phase 0.5 — just flags for human review before Phase 2

**CLI interface** (same pattern as enrich_reading_content.py):
```bash
python scripts/atomize_coursework.py                        # all 21 courses
python scripts/atomize_coursework.py --dry-run              # print to stdout
python scripts/atomize_coursework.py --course-id an_c1_responsible_ai  # single test
```

**Output files:**
- `content/atomic_modules.json` — 21 atom stubs (1:1 with source courses, not yet merged)
- `content/atomic_overlap_report.json` — merge candidate groups for Phase 2 planning

#### Sub-task C — Convert and validate all 21 courses

```bash
# 1. Test one item
python scripts/atomize_coursework.py --dry-run --course-id an_c1_responsible_ai

# 2. Spot-check: do scenario_template placeholders cover all role-specific references?
#    Does coach_system_prompt_template remove "EDC analyst" type framing?
#    Does tag extraction capture the core framework (SAFE, CRAF, VERIFY, STAKE, TRACE)?

# 3. Run all 21
python scripts/atomize_coursework.py

# 4. Verify output
python -c "
import json
atoms = json.load(open('content/atomic_modules.json'))
print(f'{len(atoms)} atoms generated:')
for a in atoms:
    tags = len(a.get('capability_tags', []))
    has_scenario = '{role}' in a.get('practice', {}).get('scenario_template', '')
    print(f'  {a[\"atom_id\"]}: {tags} tags, scenario_template has placeholders={has_scenario}')
"

# 5. Check overlap report
python -c "
import json
report = json.load(open('content/atomic_overlap_report.json'))
print(f'{len(report[\"merge_candidates\"])} merge candidate groups:')
for g in report['merge_candidates']:
    print(f'  Domain: {g[\"domain\"]} | Courses: {g[\"source_course_ids\"]}')
"
```

**Expected overlap findings** (predicted before running):
- 6 groups of 3 (RM + UW + AN versions of same framework per domain)
- Each group = 1 future canonical atom
- Confirms: 21 raw atoms → ~6 canonical atoms post-Phase-2 merge (all 6 domains × 1 universal capability each)

#### Acceptance criteria for Phase 0.5

- `content/atomic_modules.json` has 21 entries (1:1 with source courses)
- Every atom has `capability_tags` (3–6 items), `scenario_template` (contains `{role}` and `{org_type}`), `coach_system_prompt_template` (no hardcoded "EDC", "analyst", role-specific org names)
- `content/atomic_overlap_report.json` correctly flags same-domain/same-framework groups
- App still runs on original JSON files — no regression
- Human spot-check: 3 atoms (1 per role) read as role-agnostic with no loss of instructional intent

---

### Phase 1 — PM + Engineer content (atomic-ready authoring)
- Modify `generate_course_content.py` system prompt to output atomic-ready JSON (scenario_template, capability_tags, role_variants_hint) — aligns with Phase 0.5 schema
- Survey PM + Engineer use cases via Copilot
- Generate PM + Engineer as atomic modules DIRECTLY — no source_course_ids needed (they are original atoms)
- Append to `content/atomic_modules.json` (or author separately in `content/atomic_pm_eng.json`)
- Deliver: ~12–14 new atoms, role-agnostic from day one
- Milestone: library has 21 converted atoms + 14 new atoms = 35 total (21 awaiting Phase 2 merge)

### Phase 2 — Knowledge-base refactor
- Use `atomic_overlap_report.json` as the merge blueprint
- Merge same-domain/same-framework atom groups into single canonical atoms
- Consolidate `task_templates` by taking the best version (highest quality scenario, most generalizable coach prompt)
- Deliver: unified library of ~20 canonical atoms (6 universal + role-variant atoms for `data_decision` + `relationship_intel`)
- De-role eval items in `evaluation_items.json` or inline into atoms

### Phase 3 — Onboarding + path assembler refactor
- Replace role-selection welcome screen with intake form (role description + use cases + pain points)
- Add path assembler logic (filter → rank → sequence based on intake + diagnostic)
- Connect runtime scenario generation (LLM fills templates at practice/eval time)
- Deliver: fully personalized first-run experience, role-agnostic routing

### Phase 4 — Continuous library expansion
- New AI capabilities → new atoms (never role-coupled)
- Role survey (Copilot) → capability tag augmentation, not new role curricula
- Library grows sublinearly: each new role adds 2 atoms max (the genuinely role-specific domains)

---

## Key Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| AI scenario generation quality is inconsistent | HIGH | Strong scenario_template with good examples; fallback to generic if LLM fails; human review of generated scenarios before user sees them (or acceptance criteria in generation) |
| Intake form inputs are too vague to drive good assembly | HIGH | Guided structured intake (role taxonomy dropdown + free text; use-case multi-select from curated list + free text option); LLM interprets and normalizes before assembly |
| Diagnostic + intake signals conflict (user says "prompting is pain point" but diagnostic shows prompting is strong) | MEDIUM | Path assembler rules: diagnostic gap is weighted 60%, intake signal 40%; diagnostic prevents "false pain points" from blocking known strengths |
| Phase 1 atomic authoring requires pipeline change mid-delivery | MEDIUM | Minimal pipeline change: one new field in the generation system prompt + two new JSON fields per module. Backward-compatible with Phase 0 modules. |
| Content overlap analysis in Phase 2 is complex | LOW | Can be done with a Databricks notebook (compare module titles, domains, reading text embeddings → cluster similar content) |

---

## Intake Form Design (Final — 2 Questions + Diagnostic)

Max 2 intake questions (frictionless) + existing 6-item diagnostic.

### Q1 — Role, workday, and wish (free text, long-form, voice-input required)

**Prompt:** "Tell us about your work. Describe your role and a typical day, and finish with this: if you had a magic wand that could make AI do one thing to make your work easier, what would it be?"

- Free text box, large (voice-to-text input is a must-have — use browser speech API)
- No character limit, no word count pressure
- The "magic wand" framing surfaces genuine motivation, not rehearsed answers
- This single field gives the path assembler: role context + daily task context + primary AI use case intent
- LLM parses all three dimensions in one call

### Q2 — AI tools exposure (MCQ, multi-select)

**Prompt:** "Which AI tools are you currently using or have been exposed to at work?" (select all that apply)

Curated options for 2026 corporate market:

- Microsoft Copilot (M365 — Word, Excel, Teams, Outlook)
- GitHub Copilot / Cursor (coding)
- ChatGPT (browser / API)
- Google Gemini / Gem
- Databricks AI / internal LLM tools
- AI features inside existing enterprise software (Salesforce, ServiceNow, etc.)
- None yet — just getting started

**Why this matters for path assembly:**
- M365 Copilot users → scenario language uses Copilot framing
- "None yet" → skip intermediate diagnostic questions, start with responsible_ai fundamentals
- Tells us assumed baseline for scenario generation (Copilot prompt structure vs. raw ChatGPT prompts are different)

### What the diagnostic adds (unchanged)

The existing 6-item diagnostic (1 per domain) provides structured gap scores.
Combined signal: Q1 → scenario context + primary intent → capability tag matching
Q2 → tool baseline → scenario framing + level calibration
Diagnostic → domain gap scores → module sequencing priority

### Path assembler inputs (final)

```text
learner_profile = {
  "role_text":       <Q1 free text>,
  "magic_wish":      <LLM-extracted from Q1>,
  "daily_tasks":     <LLM-extracted from Q1>,
  "ai_tools":        <Q2 multi-select>,
  "domain_gaps":     <diagnostic scores per domain>,
}
```

LLM (Haiku) parses Q1 into structured fields before path assembly. One extraction call, same pattern as `enrich_reading_content.py`.

---

## Atomic Capability Library: Taxonomy and Employee-Centric Design

> Research basis: Alan Turing Institute AI Skills for Business Framework (UK Gov, 2024/2025);
> WEF Future of Jobs 2025; McKinsey Superagency Report 2025; Predictive Index AI at Work Survey 2025;
> SFIA v9 (2024); Gartner AI workforce analysis 2025.

---

### The Employee vs. Company Tension

**What COMPANIES prioritize in AI training:**

- Governance, risk, and compliance (don't misuse AI)
- Acceptable use policies and auditability
- Standardized prompts for organizational consistency
- Data protection and regulatory adherence

**What EMPLOYEES want from AI training** (McKinsey 2025: 48% rank training as #1 adoption factor):

1. Personal time savings — "get my work done faster"
2. Skill marketability — "be more valuable, not replaced"
3. Confidence in their own output — "trust what I produce"
4. Role-specific applications — "what AI can do for MY actual job"
5. Workflow automation — "stop doing the same low-value tasks manually"
6. Meeting and communication intelligence — highest-frequency daily use cases

**The gap and its consequence**: Companies lead with "don't do X" (compliance-first);
employees want "do Y better" (capability-first). Training that leads with governance
creates shadow AI (employees using tools unofficially — McKinsey: 3x more AI usage than
leaders expect). Training that leads with personal productivity drives legitimate adoption.

**Design principle for the atomic library**: Every atom must answer the employee's implicit
question — *"what's in this for me, personally?"* — within the first two sentences of its
reading section.

---

### Industry Framework Alignment

The current 6-domain model maps cleanly to the Turing Institute's 5 dimensions for AI Workers:

| Our Domain | Turing Dimension | Primary Beneficiary | Employee Reframe |
| --- | --- | --- | --- |
| `responsible_ai` | Privacy & Stewardship | Company (risk) + Employee (reputation) | "Protect your professional reputation" |
| `strategic_prompting` | Specification & Engineering | Employee | "Your personal productivity superpower" |
| `critical_eval` | Evaluation & Reflection | Employee + Company | "Never be caught out by an AI error" |
| `data_decision` | Problem Solving & Analysis | Employee | "Generate insights in minutes, not hours" |
| `relationship_intel` | Problem Definition & Communication | Employee | "Know every stakeholder better than anyone" |
| `augmented_comm` | Problem Definition & Communication (output) | Employee | "Deliver polished outputs 3× faster" |

**Verdict**: The 6 domains are well-validated by industry research. No new domains are needed;
the gaps in current coverage are addressed by adding atoms *within* existing domains.

---

### Two-Level Library Architecture (Critical Clarification)

The library is organized in **two completely separate levels**. These must never be conflated:

```text
LEVEL 1 — DIMENSIONS (~6, stable, industry-validated)
    ↓  Each dimension is a broad AI capability domain (e.g. responsible_ai)
    ↓  Dimensions are fixed: they change only if the industry framework changes
    ↓
LEVEL 2 — ATOMIC SKILLS (many, grows with role coverage)
    Each atomic skill = one 30-min module (reading + practice + eval) targeting
    a SPECIFIC TASK PATTERN that employees do in their daily work.
    Two sub-types:
      ├── Universal atomic skills: framework-based, applicable across all roles
      │   (e.g. SAFE framework, CRAF method — scenario_template fills in role context)
      └── Role-task atomic skills: target a specific daily task one or more roles perform
          (e.g. "Project Status Update for Executives" for PM, "Code Review with AI" for Eng)
          These use scenario_template too, but the task itself is role-influenced.
```

**What the role surveys produce**: NOT new dimensions — new **atomic skills** within existing
dimensions. When we survey PM use cases, we discover PM-specific tasks in each dimension
and author atomic skills for those tasks. The dimensions stay at 6.

**Library growth model**: Each new role surveyed adds ~6–12 atomic skills (1–2 per dimension).
Roles that share a task pattern converge on the same atomic skill (sublinear growth).

---

### Proposed Atomic Skills per Dimension

#### Dimension 1 — `responsible_ai`: "Protect Your Professional Reputation"

| Atomic Skill | Task Pattern | Type | Status |
| --- | --- | --- | --- |
| SAFE Data Abstraction | Handling sensitive data before prompting | Universal (framework) | ✅ RM/UW/AN |
| AI Tool Governance | Choosing the right AI tool for a task; understanding policy | Universal | 🆕 Phase 1 |
| Shadow AI Risk Management | Evaluating risk when using unofficial AI tools | Universal | 🆕 Phase 4 |
| + PM-task atoms | e.g. Responsible AI in project estimation and forecasting | Role-task | 🆕 Phase 1 |
| + Eng-task atoms | e.g. Responsible AI use in code generation and review | Role-task | 🆕 Phase 1 |

**Employee hook**: "This isn't company rules — it's how you avoid a career-defining mistake."

---

#### Dimension 2 — `strategic_prompting`: "Your Personal Productivity Superpower"

| Atomic Skill | Task Pattern | Type | Status |
| --- | --- | --- | --- |
| CRAF Prompt Construction | Writing prompts that produce usable first-draft outputs | Universal (framework) | ✅ RM/UW/AN |
| Iterative Refinement Loops | Refining AI output through structured multi-turn dialogue | Universal | 🆕 Phase 1 |
| Reusable Prompt Templates | Building a personal library of prompts for recurring tasks | Universal | 🆕 Phase 4 |
| + PM-task atoms | e.g. AI-assisted project kickoff prompting, risk log generation | Role-task | 🆕 Phase 1 |
| + Eng-task atoms | e.g. Technical specification prompting, debugging workflow | Role-task | 🆕 Phase 1 |

**Employee hook**: "One reusable prompt for your most common task = hours recovered every week."

---

#### Dimension 3 — `critical_eval`: "Never Be Embarrassed by an AI Error"

| Atomic Skill | Task Pattern | Type | Status |
| --- | --- | --- | --- |
| VERIFY Output Checklist | Systematic validation before forwarding AI output | Universal (framework) | ✅ RM/UW/AN |
| Hallucination Pattern Recognition | Identifying the most common AI error types in professional work | Universal | 🆕 Phase 1 |
| Trust Calibration | Deciding when to verify rigorously vs. when to proceed confidently | Universal | 🆕 Phase 4 |
| + PM-task atoms | e.g. Verifying AI-generated timeline and budget estimates | Role-task | 🆕 Phase 1 |
| + Eng-task atoms | e.g. Code hallucination patterns; reviewing AI-generated test cases | Role-task | 🆕 Phase 1 |

**Employee hook**: "One unchecked AI error forwarded to leadership can undo months of credibility."

---

#### Dimension 4 — `data_decision`: "Generate Insights in Minutes, Not Hours"

| Atomic Skill | Task Pattern | Type | Status |
| --- | --- | --- | --- |
| TRACE Data Workflow | Structured pipeline from raw data to AI-assisted insight | Universal (framework) | ✅ RM/UW/AN |
| Research Synthesis | Summarizing and cross-referencing multiple sources with AI | Universal | 🆕 Phase 1 |
| Data Storytelling | Turning AI-generated analysis into stakeholder-ready narrative | Universal | 🆕 Phase 4 |
| + PM-task atoms | e.g. AI-assisted velocity analysis, retrospective pattern mining | Role-task | 🆕 Phase 1 |
| + Eng-task atoms | e.g. Log analysis, performance profiling with AI assistance | Role-task | 🆕 Phase 1 |

**Employee hook**: "The person who delivers insight in 20 minutes gets the next project."

---

#### Dimension 5 — `relationship_intel`: "Know Every Stakeholder Better Than Anyone"

| Atomic Skill | Task Pattern | Type | Status |
| --- | --- | --- | --- |
| Stakeholder Intelligence Gathering | Building comprehensive context profiles with AI research | Universal | ✅ RM/UW/AN |
| Meeting Intelligence | Pre-meeting research + real-time synthesis + action item extraction | Universal | 🆕 Phase 1 |
| Stakeholder Risk Signal Detection | Identifying emerging concerns in relationship data | Universal | 🆕 Phase 4 |
| + PM-task atoms | e.g. Sponsor alignment research, cross-team dependency mapping | Role-task | 🆕 Phase 1 |
| + Eng-task atoms | e.g. On-call context gathering, incident stakeholder mapping | Role-task | 🆕 Phase 1 |

**Employee hook**: "Walk into every meeting knowing more context than the person who called it."
**Note**: Meeting Intelligence is the #1 highest-demand new atom per McKinsey data — prioritize first.

---

#### Dimension 6 — `augmented_comm`: "Deliver Polished Outputs 3× Faster"

| Atomic Skill | Task Pattern | Type | Status |
| --- | --- | --- | --- |
| STAKE Stakeholder Writing | Tailoring any document to any audience | Universal (framework) | ✅ RM/UW/AN |
| Email and Message Drafting | Drafting, toning, refining async communications at scale | Universal | 🆕 Phase 1 |
| Meeting Summaries + Action Items | Structuring decisions and next steps from meeting notes | Universal | 🆕 Phase 1 |
| + PM-task atoms | e.g. Project brief, steering committee deck, change request | Role-task | 🆕 Phase 1 |
| + Eng-task atoms | e.g. Technical design doc, post-mortem write-up, PR description | Role-task | 🆕 Phase 1 |

**Employee hook**: "Email drafting and meeting summaries are the top 2 daily time sinks AI eliminates."
**Note**: Both universal Phase 1 atoms here are in the top 3 employee requests (McKinsey).

---

### Sequencing Principle for Path Assembly

`responsible_ai` is sequenced by gap score like all other dimensions — NOT forced first.
The learner's "magic wand wish" atom is delivered as early as possible.

Default priority (when gap scores are roughly equal or path assembler has no strong signal):

1. `strategic_prompting` — universal ROI, first-session "wow moment"
2. `augmented_comm` — second-highest frequency; visible daily payoff
3. `critical_eval` — protects credibility; pairs naturally with prompting
4. `data_decision` — analytical leverage; high confidence boost
5. `relationship_intel` — high value for stakeholder-facing roles
6. `responsible_ai` — when gap detected, frame as personal protection not compliance

**Key rule**: when the path assembler finds a `responsible_ai` gap, lead the module with
personal career protection framing — never corporate compliance framing. The learner
who already prompted safely before learning SAFE still benefits from understanding WHY.
The learner who hasn't is at risk — both messages land.

---

### Framing Rules for Atom Titles and Reading Content

| Rule | Wrong (company-centric) | Right (employee-centric) |
| --- | --- | --- |
| `responsible_ai` framing | "AI Policy Compliance" | "Safe AI Prompting: Protect Your Professional Reputation" |
| Opening sentence style | "As per EDC policy, employees must..." | "One forwarded hallucination can undo months of credibility. Here's how to prevent it." |
| Benefit statement | "This reduces regulatory risk" | "This gives you the confidence to use AI on any work, any time" |
| Skill description | "Understand acceptable use" | "Know exactly what you can do, and do it with confidence" |
| Anti-pattern framing | "Policy violation: unauthorized AI tool use" | "The career cost of shadow AI: a real scenario" |

**Rule**: Every atom's `concept_text` must answer the employee question within 2 sentences.
Every `takeaway` must name a concrete personal benefit.
Every `good_example` should show a time-saving or quality-improvement win, not just compliance.

---

### Gap Analysis vs. Industry Benchmarks

Capabilities in leading frameworks (Turing, WEF, SFIA) that are NOT yet in the library:

| Missing Capability | Industry Source | Proposed Resolution |
| --- | --- | --- |
| AI tool selection literacy | Turing (Specification), WEF (technological literacy) | New atom: `responsible_ai` → "AI Tool Governance" (Phase 1) |
| Iterative/agentic prompting | Turing (Specification advanced) | New atom: `strategic_prompting` → "Iterative Refinement Loops" (Phase 1) |
| Meeting intelligence | McKinsey top employee request | New atom: `relationship_intel` → "Meeting Intelligence" (Phase 1) |
| Email/async communication drafting | McKinsey top employee request | New atom: `augmented_comm` → "Email and Message Drafting" (Phase 1) |
| Personal prompt library/templates | SFIA continuous development | New atom: `strategic_prompting` → "Reusable Prompt Templates" (Phase 4) |
| AI-assisted learning loop | Turing (Evaluation/professional learning) | Cross-cutting — embedded in `critical_eval` Trust Calibration atom |

**Priority for Phase 1 authoring** (PM + Engineer surveys should generate these 4 atoms first):

1. Meeting Intelligence (`relationship_intel`)
2. Email and Message Drafting (`augmented_comm`)
3. Iterative Refinement Loops (`strategic_prompting`)
4. Hallucination Pattern Recognition (`critical_eval`)
