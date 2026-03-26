# AI Coach Gap Analysis — B2C Redesign
**Date:** 2026-03-26 | **Context:** B2C pivot from banking B2B app

---

## What Was Analyzed

- `content/practice_scenarios.json` — 35 course-specific `coach_system_prompt` entries
- `content/atomic_modules_v2.json` — 21 atom `coach_system_prompt_template` entries
- `utils/ai.py` — `call_llm`, `call_llm_stream`, `_score_batch`, `score_byow_diagnostic`, `_LANG_INSTRUCTION`

---

## Core Design Philosophy — The PACE Model

The AI coach is not a journalist. It does not probe for its own sake. Every interaction follows PACE:

- **P — Purpose:** Declare the learning objective before generating a question. No question without a purpose.
- **A — Assess:** Read both the intellectual signal (what they understood) AND the emotional signal (how they're feeling) in the response.
- **C — Choose:** Select the right coaching move — Challenge / Clarify / Celebrate / Support — based on the assessment.
- **E — Exit:** Close the task the moment the learning objective is met. Never linger.

### 3-Question Budget Per Task (Hard Ceiling)

```
Q1 — Open probe:    Surface current thinking (always)
Q2 — Adaptive:      Challenge if shallow / Affirm and extend if good
Q3 — Synthesis:     Consolidate + bridge to build artifact

Early exit: Learning objective met after Q1 or Q2 → close immediately, skip remaining questions
Budget exhausted: Objective not met after Q3 → give direct insight + close. NEVER a 4th question.
```

### Emotional State Detection + Response

| Signal in learner response | Coach response |
|---------------------------|----------------|
| Short / dismissive (1 sentence, no reasoning) | Reframe without pressure: "Let me try a different angle..." |
| Frustrated / wrong repeatedly | Stop questioning. Give the insight directly with warmth. |
| Overconfident / surface-level | Gentle challenge: "Push one level deeper — what happens when...?" |
| Genuinely insightful | Explicit celebration + close. Never ask another question after this. |
| Confused / lost | Simplify + ground in their specific work context from onboarding profile. |

### Coach Emotional Range (4 Tones)

| Tone | When | Example |
|------|------|---------|
| **Curious** | Default, Q1 | "Walk me through how you'd approach this..." |
| **Celebratory** | Genuine insight demonstrated | "That's exactly it — and most people miss that nuance." |
| **Supportive** | Frustration or confusion detected | "This trips most people up. Let me try this differently." |
| **Challenging** | Surface answer from capable learner | "You're close — but you skipped a step. What happens right before that?" |

### UX Counterparts (Visual Pacing)

- **Progress indicator:** "Question 1 of 3" always visible — removes anxiety about endless questioning
- **Explicit closure moment:** Visual beat when task closes early (mastery signal) — learner feels completion
- **Bridge statement:** Every task ends with a one-line coach close that links to what's next — never ends mid-air
- **Never a 4th question:** Enforced at the system prompt level AND the application layer

---

## What the Current Coach Does Well (Keep)

| Strength | Where it lives |
|----------|---------------|
| One-question-per-turn discipline | All course coach prompts, explicitly enforced |
| Task-by-task guidance with specific triggers | Per-course system prompts |
| "Do not write for them" no-answers rule | All prompts |
| Data safety guardrail pattern | All prompts |
| Scope boundary enforcement | All prompts |
| Parameterized template structure `{role}`, `{organisation}`, `{scenario_name}` | Atom `coach_system_prompt_template` |
| Affirm → probe coaching rhythm | Atom prompts |

**The core coaching engine is excellent and fully reusable. The content wrapper needs replacing.**

---

## Gap 1 — Identity is employer-anchored, not learner-anchored

**Severity:** High

**Current:**
> "You are an AI skills coach for Apex Trade Finance Relationship Managers..."

**Problem:** B2C learners are not Apex Trade Finance employees. The employer framing breaks psychological rapport. The coach implicitly positions the learner as a subordinate in someone else's organization.

**Required fix:**
Shift to learner-anchored identity:
> "You are a personal AI transformation coach. Your learner is a [declared role/context] working through Day [N] of their 7-day AI transformation program."

The coach identity should serve *the learner's career goal*, not a fictional employer's compliance requirements.

---

## Gap 2 — Framework-locked coaching with no coverage for 3 of 6 pillars

**Severity:** Critical

**Current:** Every coach prompt is bound to one named framework:
- CRAF (strategic prompting)
- SAFE (responsible AI)
- VERIFY (critical evaluation)
- TRACE (data decision)
- STAKE (relationship intel)
- CSS (augmented comm)

**Problem:** Pillars 1 (AI Foundation), 4 (Configuration & Control), and 6 (Agentic System Design) have no named frameworks and zero coaching logic defined. A learner practicing temperature settings or agent role design has no coaching support.

**Required fix:**
Each new pillar needs a coaching vocabulary and probe library equivalent to what CRAF/VERIFY provide now:

| Pillar | Coaching vocabulary needed |
|--------|---------------------------|
| P1 — Foundation | LLM behavior patterns, hallucination signals, model selection reasoning |
| P4 — Configuration | System prompt anatomy, temperature tradeoffs, JSON schema design |
| P6 — Agentic Design | Workflow decomposition, agent role assignment, failure mode identification |

---

## Gap 3 — No progress awareness across the 7-day arc

**Severity:** High

**Current:** Each coach session is fully stateless. The Day 4 coach has no knowledge of what the learner demonstrated on Days 1–3.

**Problem:** A 7-day transformation arc requires continuity. Missed opportunity: if a learner mastered CRAF on Day 2, the Day 4 Configuration coach should bridge — "you already know how to structure a prompt; now let's pre-load that into a system prompt so you never repeat yourself."

**Required fix:**
Lightweight context injection at session start — the learner's completed pillar scores + a one-line capability summary — passed into the system prompt:

```
Learner context:
- P1 (Foundation): PASSED — demonstrated strong hallucination awareness
- P2 (Prompting): PASSED — CRAF-structured prompts, weak on context engineering
- Today: P3 (Tool Fluency) — Day 3
```

Coach uses this to calibrate depth and make explicit connections to prior learning.

---

## Gap 4 — Scoring is output-rubric only, reasoning quality undetected

**Severity:** Medium

**Current:** `_score_batch()` scores the final submitted response against a rubric (0–4). The coach conversation itself is not scored — only the task output.

**Problem:** For P2 (Prompting) and P6 (Agentic Design), *how the learner reasons* is as important as what they submit. A learner who produces a correct output by accident scores 4; a careful reasoner with an imperfect output scores 2. Both get identical feedback.

**Required fix:**
Two options:
- A) Coach extracts a reasoning quality signal from the conversation and passes it to the scoring layer as a modifier
- B) Quiz design includes explicit "explain your reasoning" items that the scorer can weight separately

Option B is simpler to implement and fits the existing `_score_batch` architecture.

---

## Gap 5 — Data safety guardrail is finance-context specific

**Severity:** Medium

**Current:**
> "If the learner inputs real client data — real company names, real financial figures, or verbatim confidential records — flag it immediately."

**Problem:** Calibrated for banking compliance. B2C learners have different threat surfaces: personal information, employer proprietary content, medical details, creative IP. The guardrail misses these entirely.

**Required fix:**
Universal B2C data safety guardrail:
> "If the learner inputs what appears to be real personal data (full names, addresses, medical information, employer proprietary content, financial credentials), flag it immediately and instruct them to use only the fictional scenario data provided. Do not engage with or build on any potentially real sensitive information."

---

## Gap 6 — No "Build artifact" coaching mechanic

**Severity:** High

**Current:** Coach guides learner through 4 tasks and the session ends. No closing mechanic to crystallize what was learned into a reusable output.

**Problem:** The 7-day arc's value proposition requires the learner to *build something tangible each day*. Without a closing artifact mechanic, learners finish practice with nothing to show or reuse. This also undermines the credential story — "what did you actually make?"

**Required fix:**
A closing task (Task 5 or post-Task 4 prompt) where the coach helps the learner produce their artifact:

> "Based on what you practiced today, write the [prompt template / system prompt / workflow map] you would actually use in your work. I'll help you refine it."

Artifact types by pillar:
| Pillar | Build artifact |
|--------|---------------|
| P1 | Personal AI tool selection checklist |
| P2 | Reusable prompt template for their job context |
| P3 | Tool selection decision framework (their version) |
| P4 | Configured system prompt they can deploy today |
| P5 | Documented 3-step AI workflow for a real task they do |
| P6 | Agent workflow design for a process they want to automate |

---

## Gap 7 — Language instruction hardcoded to financial acronyms

**Severity:** Low (but blocks multilingual launch)

**Current (`utils/ai.py`):**
```python
"Do not use English except for: framework acronyms (SAFE, CRAF, VERIFY, TRACE, STAKE),
fictional company names (Meridian, Aurora, Crestwood, Apex, etc.)"
```

**Problem:** All banking-context artifacts. New pillars use different technical vocabulary. The fictional companies are gone. Chinese-language learners need correct handling of AI-native terms.

**Required fix:**
Update `_LANG_INSTRUCTION` for new pillar vocabulary:
```python
"Do not use English except for: AI technical terms (LLM, GPT, Claude, RAG, CoT, JSON, API, MCP,
system prompt, temperature), tool names (ChatGPT, Midjourney, Cursor, n8n), and
fictional scenario names provided in the module."
```

---

## Summary

| Gap | Severity | Effort to fix |
|-----|----------|--------------|
| 1 — Employer-anchored identity | High | Low — rewrite coach identity header |
| 2 — No coaching logic for P1/P4/P6 | Critical | High — design 3 new coaching frameworks |
| 3 — No 7-day arc continuity | High | Medium — context injection at session start |
| 4 — Reasoning quality unscored | Medium | Medium — add reasoning items to quiz design |
| 5 — Finance-specific data safety | Medium | Low — replace one guardrail paragraph |
| 6 — No build artifact mechanic | High | Medium — design closing task per pillar |
| 7 — Financial acronyms in lang instruction | Low | Low — update one dict in ai.py |

**Net assessment:** The coaching engine (streaming, one-question discipline, task guidance, no-answers rule, scope enforcement) is production-quality and fully reusable. Gaps 1, 2, 3, and 6 must be resolved before any B2C content goes live.
