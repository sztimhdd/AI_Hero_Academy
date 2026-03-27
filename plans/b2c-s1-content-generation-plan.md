# Sprint 1: B2C Content Generation
**Track:** A (Content — no code dependency)
**Depends on:** Nothing. Starts Day 1.
**Estimated effort:** L (multi-pillar, sequential with QA gates)

---

## Objective

Run the 7-agent multi-model pipeline to produce all content needed for the 7-day B2C program: 6 pillar modules (P1–P6), a universal diagnostic, the Day 7 capstone, and the role injection library. Content is generated before the app shell is built — content-first ensures the learning experience drives the architecture. P1 is the pilot; validate quality before running P2–P6.

---

## What Gets Built

```
content/
  pillars/
    p1_foundation.json      ← Day 1: AI Conceptual Foundation (MAPS coaching)
    p2_prompting.json       ← Day 2: Prompting & Context Engineering (CRAF)
    p3_tool_fluency.json    ← Day 3: AI Tool Fluency (CAST — perishable, Tavily-critical)
    p4_configuration.json   ← Day 4: AI Configuration & Control (BRIEF)
    p5_workflow.json        ← Day 5: Multi-AI Workflow Design
    p6_agentic.json         ← Day 6: Agentic System Design (CREW)
    capstone.json           ← Day 7: End-to-end challenge (all 6 pillars)
  diagnostic_pillar.json    ← 5 MCQs (P1–P5) + generator prompt
  diagnostic_generator_prompt.txt
  role_contexts.json        ← 10-15 role archetypes with scenario seeds
```

Each pillar JSON schema:
```json
{
  "pillar_id": "p1",
  "reading": { "concept_text", "good_example", "anti_pattern", "takeaway" },
  "practice": { "scenario_template", "tasks": [4 tasks], "coach_system_prompt_template" },
  "quiz": { "items": [3 MCQ + 1 open rubric], "pass_threshold": 2.5 },
  "build_artifact": { "artifact_type", "prompt", "coach_closing_prompt" }
}
```

---

## 7-Agent Pipeline (per pillar)

| Agent | Model | Input → Output |
|-------|-------|---------------|
| 1 — Research | Gemini 3.1 Pro + Tavily | Pillar definition → research brief (2026 examples, tools, patterns) |
| 2 — Curriculum | Gemini 3.1 Pro | Research brief → intermediate bar definition + learning arc |
| 3 — Content Writer | Gemini 3.1 Pro | Curriculum spec → `reading` JSON (under 1200 words EN) |
| 4 — Scenario Designer | Gemini 3.1 Pro | Curriculum + role_contexts → 4 parameterized tasks (no hardcoded roles) |
| 5 — Coach Architect | Claude Sonnet 4.6 | Curriculum + scenario + gap-analysis.md → `coach_system_prompt_template` |
| 6 — Assessment | Gemini 3.1 Pro | Curriculum + reading → 3 MCQ + 1 open rubric + `build_artifact_prompt` |
| 7 — QA Reviewer | Claude Sonnet 4.6 | All outputs → approve/reject: B2C tone, role-agnostic, calibration, EN/ZH readiness |

---

## Pillar-Specific Coaching Frameworks

Each pillar's Coach Architect agent must define a new coaching vocabulary:

| Pillar | Framework | Coaching vocabulary |
|--------|-----------|---------------------|
| P1 | **MAPS** | Model behavior · Awareness of limits · Practical application · Safety baseline |
| P2 | **CRAF** | Context · Role · Action · Format (reuse from existing atom, renew examples) |
| P3 | **CAST** | Capability · Access · Source-to-destination · Tradeoff |
| P4 | **BRIEF** | Behavior · Role · Instructions · Edge cases · Format |
| P5 | _(workflow)_ | Pipeline node · Handoff · Human checkpoint · Structured output |
| P6 | **CREW** | Components · Roles · Edge cases · Workflow map |

All coach prompts must implement PACE: 3-question budget per task, emotional detection (5 patterns), 4-tone range (curious/celebratory/supportive/challenging), mastery exit. Never a 4th question.

---

## Generation Order + Rationale

1. **P1** — pilot. Low research burden. Validate the pipeline and schema. Human QA gate before proceeding.
2. **P2 + P5** — parallel. Strong existing atom seed material. Both are straightforward.
3. **P3** — Tavily/Search is non-negotiable. Tool examples must be 2026-current. Mark JSON `perishable_content: true`.
4. **P4 + P6** — parallel after C3. Zero existing content. Highest research burden.
5. **Diagnostic + Capstone + role_contexts.json** — last. Requires knowing all pillar scope to write good diagnostic items and a capstone that spans all 6.

---

## Acceptance Criteria

1. All 7 pillar JSONs produced and QA-approved (Agent 7 sign-off required on each).
2. All practice scenarios: zero hardcoded roles/employers. All `{declared_role}`, `{declared_industry}`, `{daily_work_desc}` slots unfilled in templates.
3. All coach prompts: PACE enforced, learner-anchored identity ("personal AI transformation coach"), `{prior_pillar_scores}` + `{prior_pillar_summaries}` slots for 7-day arc continuity.
4. All coach prompts: B2C data safety guardrail (PII, employer content, medical — not banking-specific).
5. P3 JSON: `perishable_content: true`, `last_updated: "2026-03"`, sourced tool examples (Tavily-verified).
6. P4 coach: explicit bridge to P2 CRAF mastery ("you already know how to prompt; now pre-load it into a system prompt").
7. P5 vs P6 distinction explicit: P5 = human orchestrates; P6 = AI orchestrates.
8. `diagnostic_pillar.json`: 5 role-agnostic MCQs testing applied judgment, not framework names.
9. `diagnostic_generator_prompt.txt`: prompt template + static fallback.
10. `capstone.json`: all 6 pillars exercised, under 15 min, mixed input (2 text + 1 MCQ cluster + 1 file upload task).
11. `role_contexts.json`: 10+ archetypes covering: marketer, teacher, PM, analyst, nurse, HR, ops, freelancer, developer, student.

## Key Constraints (Non-Negotiable)

- Gemini 3.1 Pro for research/curriculum/content/scenario/assessment agents
- Claude Sonnet 4.6 for coach architect + QA reviewer agents
- No hardcoded roles. No employer-anchored framing. No banking context.
- PACE model is non-negotiable: 3Q budget, mastery exit, no 4th question.
- P1 QA must pass before running P2–P6.

## UAT Checkpoint

**Type: Content validation (no Playwright — no UI exists yet)**

After all pillar JSONs are generated and Agent 7 approved, run:

```bash
# 1. Schema validation — every pillar JSON must conform
python scripts/validate_pillar_schema.py content/pillars/

# 2. Slot integrity — no hardcoded roles anywhere in practice/coach fields
grep -r "Relationship Manager\|Underwriter\|Analyst\|bank\|financial institution" content/pillars/

# 3. PACE slot check — every coach_system_prompt_template must have required slots
grep -L "prior_pillar_scores\|prior_pillar_summaries\|declared_role" content/pillars/*.json

# 4. P3 perishable flag
python -c "import json; d=json.load(open('content/pillars/p3_tool_fluency.json')); assert d.get('perishable_content') == True"
```

All 4 checks must pass before this sprint is marked done. If any grep returns hits or any assert fails, fix before handing off to Sprint 3.

**P1 pilot gate (before running P2–P6):** Agent 7 must explicitly output `APPROVED` for P1. No implicit approval.

## Out of Scope

- ZH translation of pillar content (future content sprint after EN is stable)
- App rendering (Track B sprints)
- Ongoing content maintenance / tool updates (future)
