# Sprint 3: B2C Core Learning Loop
**Track:** B (Engineering)
**Depends on:** Sprint 2 (auth + schema + onboarding), Sprint 1 P1 content (at minimum)
**Estimated effort:** L

---

## Objective

Build the heart of the product: the AI coach engine and the daily module experience. A learner who completes this sprint can go from Day 1 reading → AI-coached practice (PACE model) → quiz → build artifact, with personalized coaching drawing from their declared role context and growing 7-day learning history. The synthesis agent closes the arc by updating the learner model after each day, making each subsequent day's coach smarter.

---

## What Gets Built

**1. Coach Engine — TypeScript Port (E4)**

Ports `utils/ai.py` coaching logic to Next.js API routes. This is the most critical component in the product.

API routes:
- `POST /api/coach/session/start` — creates `coach_sessions` doc, returns `session_id`
- `POST /api/coach/stream` — **Server-Sent Events** route; streams Gemini 2.0 Flash coach response
- `POST /api/coach/session/complete` — writes final transcript + `practice_completed_at`

Core engine library (`src/lib/coach/`):
- `pace.ts` — turn counter per task (hard ceiling at 3); early exit on mastery; task completion signals
- `assembler.ts` — assembles final system prompt from template + profile + learner model
- `types.ts` — `CoachMessage`, `CoachSession`, `CoachStreamEvent`, `PaceState`
- `pace.test.ts` — unit tests: Q4 blocked, early exit detection, mastery signal

PACE enforcement (server-side, not just prompts):
- Track `task_turn_counts` per session in Firestore
- Q3 exhausted → emit `{ type: "task_complete", reason: "budget_exhausted" }` in stream
- Mastery marker in Gemini response → emit `{ type: "task_complete", reason: "mastery_early_exit" }`

Context injection at every session start:
- Role context: `{declared_role}`, `{declared_industry}`, `{daily_work_desc}` from `user_profiles`
- 7-day arc: `{prior_pillar_scores}`, `{prior_pillar_summaries}` from `learner_model` (Gap 3 fix)
- Language: ZH instruction injected if `user_profiles.lang = "zh"`

B2C data safety guardrail: PII / employer proprietary / medical content (replaces banking-specific guardrail).

**2. Daily Module UX (E5)**

Route: `/day/[pillar_id]` with 4 sub-sections:

| Sub-section | What it does |
|-------------|-------------|
| **Reading** | Renders `concept_text`, `good_example`, `anti_pattern`, `takeaway` from pillar JSON. "Mark as read" writes `reading_completed_at`. |
| **Practice** | 4-task AI coach chat. SSE streaming. "Question N of 3" indicator always visible. Task completion animation on early mastery. Build artifact editor on closing task. Session written on all 4 tasks + artifact complete. |
| **Quiz** | 4 questions (3 MCQ + 1 open rubric). Submit → `/api/quiz/score` → Gemini Flash batch scores. Pass (≥2.5): badge awarded + next day unlocked. Fail: hints shown + immediate retake. |
| **Build** | Artifact text editor. "Save to My Toolkit" → `build_artifacts` Firestore write. |

Navigation: sidebar/stepper showing Day 1–7 with lock/unlock state.

**3. Synthesis Agent (E6)**

Runs after each day's quiz pass. Fire-and-forget, non-blocking.

Route: `POST /api/synthesis/run`
- Reads day's `coach_sessions` transcript
- Gemini 2.0 Flash (temp 0.2): extracts `daily_summary`, up to 2 `natural_strengths`, up to 2 `recurring_gaps`, `preferred_framing` signal, optional `memorable_quote`
- Appends to `learner_model/{user_email}` (never overwrites existing arrays)
- `preferred_framing` consolidated to top-level after 2+ consistent days
- Failure: logged to `ai_call_log`, learner never blocked

Trigger from `/api/quiz/score`:
```typescript
fetch('/api/synthesis/run', { method: 'POST', body: JSON.stringify({...}) }).catch(() => {});
```

---

## Acceptance Criteria

1. `/api/coach/stream` streams Gemini responses via SSE ✅
2. PACE enforced server-side: Q4 blocked in unit test + integration ✅
3. Early exit: mastery signal emits `task_complete` event ✅
4. Role context from `user_profiles` injected into every coach session ✅
5. `{prior_pillar_scores}` + `{prior_pillar_summaries}` from `learner_model` injected (empty on Day 1) ✅
6. B2C data safety guardrail: PII-aware, not banking-specific ✅
7. `/day/p1` renders with all 4 sub-sections ✅
8. "Question N of 3" indicator visible throughout practice ✅
9. Streaming coach chat: messages stream character-by-character ✅
10. Build artifact saved to Firestore on "Save to My Toolkit" ✅
11. Quiz pass: `quiz_passed: true`, next pillar unlocked, badge shown ✅
12. Quiz fail: hints rendered, retake works without reload ✅
13. Synthesis runs after quiz pass (fire-and-forget) ✅
14. `learner_model` updated; Day 2 coach injection includes Day 1 summary ✅
15. Mobile-responsive at 375px ✅

## UAT Checkpoint

**Type: Full learning loop UAT (Playwright MCP, local) + PACE unit tests + legacy regression**

**Part A — PACE unit tests (must pass before Playwright UAT)**
```bash
npm test src/lib/coach/pace.test.ts
# Required: Q4 blocked, early exit on mastery, budget exhausted → direct insight
```
All tests must pass. If any fail, do not proceed to Playwright UAT.

**Part B — Learning loop UAT (Playwright MCP, local `http://localhost:3000`)**
```
Persona: test user, Day 1 unlocked (seed via scripts/seed-dev.ts)

UAT-S3-1:  /day/p1 renders all 4 sub-sections (Reading / Practice / Quiz / Build)
UAT-S3-2:  Reading content renders from p1_foundation.json (not Firestore)
UAT-S3-3:  "Mark as read" writes reading_completed_at to Firestore → Practice unlocks
UAT-S3-4:  Practice loads Task 1 with scenario text and chat input
UAT-S3-5:  "Question 1 of 3" indicator visible
UAT-S3-6:  Submit coach message → SSE stream renders response character-by-character
UAT-S3-7:  Q4 blocked server-side — 4th message in same task returns task_complete event
UAT-S3-8:  Early mastery exit — coach emits task_complete before Q3 when mastery signal present
UAT-S3-9:  Build artifact editor appears after Task 4 completes
UAT-S3-10: "Save to My Toolkit" writes build_artifacts doc to Firestore
UAT-S3-11: Quiz: 4 questions render (3 MCQ + 1 open)
UAT-S3-12: Quiz pass (≥2.5): quiz_passed=true, P2 unlocked, badge shown
UAT-S3-13: Quiz fail (<2.5): hints rendered, retake works without reload
UAT-S3-14: After quiz pass: learner_model updated in Firestore (synthesis fired)
UAT-S3-15: /day/p2 coach system prompt includes Day 1 daily_summary from learner_model
```
Gate: **14/15** pass. UAT-S3-8 (early mastery) acceptable as deferred if edge case hard to trigger.

**Part C — Legacy Streamlit regression (Playwright MCP, local port 8501)**
Run `.claude/evals/baseline-uat.md` — must pass **38/41**.
Failures in G2a or G4 block this sprint.

## Key Constraints

- Gemini 2.0 Flash only — no other model for coaching/scoring/synthesis
- SSE for streaming — not WebSocket
- Practice conversation in-memory until completion — refresh = restart from Task 1 (acceptable)
- Content loaded from JSON files — never from Firestore
- 3Q budget enforced in code — not just in system prompts

## Out of Scope

- Dashboard (Sprint 4)
- Credential generation (Sprint 4)
- Capstone UI (Sprint 4)
- Full ZH i18n (Sprint 4)
