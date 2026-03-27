# Kickstart: Sprint 1 — B2C Content Generation
**Full plan:** `plans/b2c-s1-content-generation-plan.md`

---

## What to Read First

1. `plans/b2c-s1-content-generation-plan.md` — full spec, pipeline, pillar frameworks
2. `plans/b2c-ai-coach-gap-analysis.md` — PACE model, 7 gaps to fix (especially Gaps 1, 2, 3, 6)
3. `plans/b2c-transformation-roadmap.md` §3.2 (all 6 pillar skill maps), §3.5 (reuse map)
4. `content/atomic_modules_v2.json` — atoms to adapt as seed: `craf_framework`, `iterative_refinement`, `hallucination_patterns`, `responsible_ai__safe_framework`, `ai_tool_governance`, `universal_analysis`, `capstone__end_to_end_workflow`

---

## What to Build

Run the 7-agent pipeline for each pillar in this order: P1 → (P2+P5 parallel) → P3 → (P4+P6 parallel) → diagnostic+capstone.

**For each pillar, produce one approved JSON file** (`content/pillars/p{N}_{slug}.json`) conforming to the schema in the plan doc. All 7 agents must run; Agent 7 (QA Reviewer) must explicitly approve before moving to the next pillar.

**P1 is the pilot.** Validate the pipeline and output schema on P1 before running any other pillar. If QA fails P1, fix and re-run before proceeding.

---

## Non-Negotiable Rules

- **No hardcoded roles or employers** — all scenario parameters as `{declared_role}`, `{declared_industry}`, `{daily_work_desc}` slots
- **No employer-anchored coach identity** — "personal AI transformation coach", not "AI skills coach for [Company]"
- **PACE model in every coach prompt** — 3-question budget per task, emotional detection, mastery exit, build artifact closing task
- **`{prior_pillar_scores}` + `{prior_pillar_summaries}` slots** in every coach template (even if empty on Day 1)
- **P3 requires Tavily** — tool examples without live research are outdated and fail QA
- **P3 JSON must set** `"perishable_content": true`
- **P1 QA gate** — do not run P2–P6 until P1 passes Agent 7 review
- **Agent 5 (Coach Architect) = Claude Sonnet 4.6, not Gemini** — coach design quality matters
- **Agent 7 (QA Reviewer) = Claude Sonnet 4.6** — not self-review

---

## Success Criteria (Done When)

- [ ] `content/pillars/p1_foundation.json` — QA-approved ✅
- [ ] `content/pillars/p2_prompting.json` — QA-approved ✅
- [ ] `content/pillars/p3_tool_fluency.json` — QA-approved, `perishable_content: true` ✅
- [ ] `content/pillars/p4_configuration.json` — QA-approved ✅
- [ ] `content/pillars/p5_workflow.json` — QA-approved ✅
- [ ] `content/pillars/p6_agentic.json` — QA-approved ✅
- [ ] `content/pillars/capstone.json` — QA-approved, under 15 min ✅
- [ ] `content/diagnostic_pillar.json` — 5 MCQ items, role-agnostic ✅
- [ ] `content/diagnostic_generator_prompt.txt` — prompt + static fallback ✅
- [ ] `content/role_contexts.json` — 10+ archetypes ✅
- [ ] All coach prompts: PACE, learner-anchored, `{prior_pillar_scores}` slot, B2C data safety guardrail ✅
