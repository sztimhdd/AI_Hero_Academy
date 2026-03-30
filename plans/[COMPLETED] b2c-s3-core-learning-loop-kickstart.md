# Kickstart: Sprint 3 — B2C Core Learning Loop
**Full plan:** `plans/b2c-s3-core-learning-loop-plan.md`

---

## What to Read First

1. `plans/b2c-s3-core-learning-loop-plan.md` — full spec, PACE enforcement, SSE pattern
2. `plans/b2c-ai-coach-gap-analysis.md` — PACE model spec, emotional detection patterns, UX counterparts
3. `utils/ai.py` — Python implementation to port: `call_llm_stream()`, `_LANG_INSTRUCTION`, streaming pattern
4. `content/pillars/p1_foundation.json` — actual pillar schema (must exist from Sprint 1)
5. `TDD.md` §2.3 (Gemini model, temperature)

**Prerequisites:** Sprint 2 complete (auth working, schema types exist).

---

## What to Build

Three components in dependency order: coach engine → daily module → synthesis agent.

**Coach engine first** — daily module calls it, so it must exist and be tested before building the module UX.

**`src/lib/coach/` library:**
- `pace.ts` — `incrementTurn(sessionId, taskId)`, `checkMastery(response)`, `emitTaskComplete(reason)`
- `assembler.ts` — `assembleCoachPrompt(template, profile, learnerModel, taskId) → string`
- `types.ts` — exported types
- `pace.test.ts` — unit tests: Q4 blocked, early exit, mastery signal

**API routes:**
- `POST /api/coach/session/start`
- `POST /api/coach/stream` (SSE — `Content-Type: text/event-stream`)
- `POST /api/coach/session/complete`
- `POST /api/quiz/score`
- `POST /api/synthesis/run`

**`/day/[pillar_id]` route** — 4 sub-sections: Reading / Practice / Quiz / Build.

---

## Non-Negotiable Rules

- Q4 is blocked server-side in `pace.ts` — not just in the system prompt
- SSE for streaming — not WebSocket, not polling
- Practice conversation in-memory only — not persisted until `/api/coach/session/complete`
- Content loaded from `content/pillars/*.json` — never from Firestore
- Synthesis is fire-and-forget — never blocks quiz pass or page response
- Gemini 2.0 Flash only — temperature 0.4 for coaching, 0.2 for synthesis, 0.1 for scoring

---

## Success Criteria (Done When)

- [ ] `pace.test.ts` all tests pass: Q4 blocked, early exit, mastery signal ✅
- [ ] Streaming coach chat: messages stream via SSE in real-time ✅
- [ ] "Question N of 3" visible throughout practice ✅
- [ ] Quiz pass: `quiz_passed: true`, P2 unlocked, badge shown ✅
- [ ] Quiz fail: hints + retake work ✅
- [ ] `learner_model` updated after Day 1 quiz pass (verify in Firestore) ✅
- [ ] Day 2 coach injects Day 1 `daily_summary` from `learner_model` ✅
- [ ] Mobile-responsive at 375px ✅
