# B2C Sprint Planning — Kickstarter Prompt
**For:** Planning agent session (new session)
**Date:** 2026-03-26

---

## Your Mission

You are a senior product and engineering planner. Your job is to read the B2C transformation roadmap, understand all design decisions made, and produce a complete sprint plan with individual plan docs and kickstarter prompts for each sprint — ready for execution.

---

## Step 1 — Read These Files First (in this order)

1. `plans/b2c-transformation-roadmap.md` — the authoritative design document. Read it fully. All product, content, coaching, UX, tech stack, and data model decisions are here.
2. `plans/b2c-ai-coach-gap-analysis.md` — AI coach design details, PACE model, gap analysis.
3. `PRD.md` — updated executive summary and product direction (v2.0).
4. `TDD.md` — updated tech stack (v2.0): Next.js + Firebase Auth + Firestore + GCS + Cloud Run.
5. `PLAN.md` — current state of legacy phases (all complete) + B2C phase overview skeleton.
6. `content/atomic_modules_v2.json` — existing 21 atoms (10 are reusable, review the reuse map in the roadmap).
7. `content/courses.json` — 35 role-specific courses (all being retired, understand what's being replaced).

---

## Step 2 — Understand the Two Parallel Tracks

**Track A — Content Generation** (no code dependency, can start Day 1)
- 7-agent pipeline: Research → Curriculum Designer → Content Writer → Scenario Designer → Coach Architect → Assessment Designer → Quality Reviewer
- Models: Gemini 3.1 Pro agents + Tavily/Google Search for live research
- Generate in order: P1 (MAPS) → P2 (CRAF) → P5 (existing atoms adapted) → P3 (CAST) → P4 (BRIEF) → P6 (CREW)
- P1 is the pilot — validate quality before running all pillars
- Each pillar output: reading JSON + practice scenario + coach_system_prompt_template + 4 quiz items + build artifact prompt
- Also needed: 6-item diagnostic (1 AI-generated text question + 5 MCQs) + Day 7 capstone

**Track B — Engineering** (sequential by dependency)
- Next.js scaffold → Firebase Auth → Firestore schema → Coach engine → Onboarding → Daily module → Synthesis agent → Dashboard → Credential → Capstone → i18n
- All GCP: Firebase Auth, Firestore, GCS, Cloud Run, Firebase Hosting
- Coach engine ports Python `utils/ai.py` logic to TypeScript API routes — same Gemini API, same PACE model
- Full dependency chain is in PLAN.md B2C phase overview

---

## Step 3 — Your Deliverables

For each sprint, produce:

### A. A plan doc: `plans/b2c-[track]-[N]-[slug]-plan.md`

Structure:
```
# Sprint: [Name]
**Track:** A (Content) or B (Engineering)
**Depends on:** [prior sprints]
**Estimated effort:** [S/M/L]

## Objective
One paragraph: what this sprint produces and why it matters.

## Acceptance Criteria
Numbered list of testable outcomes. Be specific.

## Key Decisions Already Made
Bullet list of relevant decisions from the roadmap — do not re-open these.

## Implementation Notes
Technical guidance for the executor. Reference specific files, collections, patterns.

## Out of Scope
What this sprint explicitly does NOT do.
```

### B. A kickstarter prompt: `plans/b2c-[track]-[N]-[slug]-kickstart.md`

A self-contained prompt an engineer or agent can execute in a new session with zero prior context. Must include:
- What to read first (specific files)
- What to build (clear scope)
- What NOT to do (guard rails)
- Success criteria (how to know it's done)
- Reference to the plan doc for full detail

---

## Step 4 — Prioritization Rules

Apply these rules when sequencing sprints:

1. **Content before app shell needs it** — P1 pilot must be done before B2C-E5 (daily module UX). Other pillars can lag slightly.
2. **Auth before everything else in Track B** — Firebase Auth is the foundation. Nothing else in Track B can start without B2C-E1.
3. **Coach engine before daily module** — B2C-E4 must complete before B2C-E5.
4. **Synthesis agent after coach sessions work** — B2C-E6 depends on B2C-E4 + B2C-E5.
5. **Credential and capstone are last** — B2C-E8 and B2C-E9 are the final engineering sprints.
6. **i18n runs last** — B2C-E10 ports all new keys to ZH after EN is stable.
7. **Small sprints over large ones** — prefer 2–4 day sprints with clear acceptance criteria over week-long ambiguous ones.

---

## Step 5 — Update PLAN.md

After writing all sprint docs, update `PLAN.md`:
- Fill in the B2C phase overview table with actual sprint names, effort estimates, and file references
- Add a "Critical Path" section showing the minimum viable sequence to reach Day 7 working end-to-end
- Add a "Parallel Opportunities" section showing what can run simultaneously

---

## Key Constraints to Respect (Do Not Re-Open)

- **Stay 100% on GCP** — Firebase Auth, Firestore, GCS, Cloud Run, Firebase Hosting. No Supabase, no Vercel, no third-party auth.
- **Gemini API only** — all AI calls via Gemini (Flash for coaching/scoring/synthesis, Pro for content generation). No OpenAI, no Anthropic in the app.
- **Next.js App Router** — not Pages Router. Server Components where possible.
- **Bilingual EN + ZH at all times** — every UI sprint must account for i18n. No EN-first shortcuts.
- **PACE model is non-negotiable** — 3-question budget per task, emotional detection, mastery exit. Coach engine must implement this exactly.
- **Content is role-agnostic** — no hardcoded roles. All scenarios injected at runtime from learner profile.
- **35 legacy courses are retired** — do not port them. The 10 reusable atoms (listed in roadmap §3.5) are adapted, not copied.
- **Free forever** — no payment integration, no paywalls, no freemium gates.

---

## Output Checklist

Before finishing, confirm you have produced:

- [ ] B2C-C1 plan + kickstart (P1 content pilot)
- [ ] B2C-C2 plan + kickstart (P2 + P5 content)
- [ ] B2C-C3 plan + kickstart (P3 CAST content)
- [ ] B2C-C4 plan + kickstart (P4 BRIEF content)
- [ ] B2C-C5 plan + kickstart (P6 CREW content)
- [ ] B2C-C6 plan + kickstart (diagnostic + capstone)
- [ ] B2C-E1 plan + kickstart (Next.js scaffold + Firebase Auth)
- [ ] B2C-E2 plan + kickstart (Firestore schema migration)
- [ ] B2C-E3 plan + kickstart (onboarding flow)
- [ ] B2C-E4 plan + kickstart (coach engine TypeScript port)
- [ ] B2C-E5 plan + kickstart (daily module UX)
- [ ] B2C-E6 plan + kickstart (synthesis agent)
- [ ] B2C-E7 plan + kickstart (dashboard + streak)
- [ ] B2C-E8 plan + kickstart (credential generation)
- [ ] B2C-E9 plan + kickstart (Day 7 capstone)
- [ ] B2C-E10 plan + kickstart (i18n port)
- [ ] PLAN.md updated with critical path + parallel opportunities

Total: 16 sprint pairs (32 files) + 1 PLAN.md update.
