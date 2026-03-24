# Phase 5 — Role-Agnostic Diagnostic & Intake

> Status: **PLANNED** — ready to start
> Last updated: 2026-03-24

---

## Context & What's Already Done

**Phase 4 complete (2026-03-24):** Atomic library has 20 canonical atoms. Eval loader
supports `items_ref == "inline"`. `fill_scenario()` handles all known placeholders.
42/42 pytest green.

**The problem Phase 5 solves:**
JD dry-run experiments across 4 EDC roles revealed one architectural conclusion:

> **The atoms are at critical mass. The diagnostic and intake are the bottleneck.**

| Layer | Current State | Phase 5 Target |
|-------|--------------|----------------|
| Atoms | 20 atoms, fill_scenario() role-agnostic | Unchanged — ready |
| `assemble_path()` | Fully role-agnostic | Unchanged — ready |
| Intake form | Q1 = free text, LLM extracts 3 fields | Q1 = JD paste encouraged, LLM extracts 6 fields |
| Role selector | Forced path into role-gated content | Optional shortcut only — no downstream gating |
| Diagnostic | `role_id`-gated MCQ items → noise for unknown roles | 6 BYOW open prompts → valid scores for any role |
| `data_decision` | 5 role-variant atoms, reading content has role residue | + 1 universal atom |

**Root cause:**
`01_Diagnostic.py` loads items via `get_diagnostic_items(role_id)`. Every item has a
hardcoded `scenario_text` embedding role-specific job context. A Sr. Technical Advisor,
Investment Analyst, or any role outside the 5 built personas gets items designed for
a different job. Their domain scores are noise. Their assembled path is random.

---

## What Phase 5 Builds

### 5.1 — New universal `data_decision` atom

Use existing `scripts/generate_atom.py`. One new atom:

| Atom ID | Title | Framework |
|---------|-------|-----------|
| `data_decision__universal_analysis` | "Signal to Decision: AI-Assisted Analysis for Any Role" | SIGNAL: Source → Interrogate → Generate → Narrate → Act → Log |

Employee hook: "Turn any dataset, report, or information pile into a clear decision
recommendation in under 10 minutes — regardless of your role or industry."

Capability tags: `data_synthesis`, `ai_assisted_analysis`, `decision_support`,
`insight_generation`, `structured_reasoning`

---

### 5.2 — Intake form enrichment (`pages/00_Welcome.py`)

**Q1 label change:** From "Tell us about your work" →
"Paste your job description, or describe your role and main responsibilities"

**LLM parse prompt upgrade:** Current prompt extracts 3 fields. Upgrade to extract 6:

```python
_parse_prompt = (
    "Extract structured information from this employee job description or self-description. "
    "Return ONLY valid JSON with these keys:\n"
    "  role_text: job title in 3-5 words\n"
    "  daily_tasks: list of 4-5 specific task strings\n"
    "  magic_wish: the primary AI benefit this person would want, one sentence\n"
    "  industry: industry or sector in 2-3 words\n"
    "  org_type: type of organization in 3-5 words\n"
    "  seniority: one of [junior, mid, senior, executive]"
)
```

**Role selector:** Stays in Advanced Options expander (unchanged location). When a known
role is selected, it pre-populates the intake profile AND skips the `role_id` inferred
keyword matching. Role shortcut still works — but the diagnostic no longer uses `role_id`
to load items.

**Remove:** The `_inferred_role_id` keyword matching block (`if "relationship manager" in...`).
Replace with: store whatever was selected in Advanced Options as `role_id` for Firestore
legacy compat only. Default: `"universal"` (new value — do not default to `"rm"`).

---

### 5.3 — BYOW diagnostic prompts (`content/diagnostic_prompts.json`)

New file. 6 prompts, one per domain. Schema:

```json
[
  {
    "item_id": "byow_responsible_ai_1",
    "domain_id": "responsible_ai",
    "sequence": 1,
    "prompt_text": "Describe a real or imagined work situation where you'd need to think carefully before using AI — for example, because of data sensitivity, tool approval, or professional risk. What would you consider?",
    "scoring_rubric": {
      "4": "Identifies specific data types or sensitivity levels; names a governance check (policy, approval, data residency); demonstrates systematic thinking",
      "3": "Raises a valid concern (sensitivity or approval) with some specificity; shows awareness of professional risk",
      "2": "Mentions general privacy or risk concerns but without specificity or a structured response",
      "1": "Vague answer (e.g. 'be careful') with no concrete consideration",
      "0": "No answer, irrelevant, or 'I would just use it'"
    }
  },
  {
    "item_id": "byow_strategic_prompting_1",
    "domain_id": "strategic_prompting",
    "sequence": 2,
    "prompt_text": "Pick a task you do regularly at work — a document, analysis, summary, or plan. Walk me through how you'd use AI to help you do it. Be as specific as you can about what you'd type.",
    "scoring_rubric": {
      "4": "Writes a specific, structured prompt with context, role, constraints, and output format; shows awareness of what good output looks like",
      "3": "Provides a reasonable prompt with some specificity; missing one key element (context, format, or constraint)",
      "2": "Describes using AI but prompt is vague (e.g. 'ask it to write a summary'); no structure",
      "1": "Mentions AI but no prompt attempt; or very generic (e.g. 'type my question')",
      "0": "No answer or 'I don't use AI'"
    }
  },
  {
    "item_id": "byow_critical_eval_1",
    "domain_id": "critical_eval",
    "sequence": 3,
    "prompt_text": "If an AI tool wrote a key paragraph for something important you were submitting — a proposal, report, or recommendation — what would you do before using it? Be specific.",
    "scoring_rubric": {
      "4": "Names specific checks (fact verification, source citation, internal consistency, stakeholder review); articulates what could go wrong",
      "3": "Describes 2+ concrete verification steps with some reasoning about risk",
      "2": "Says 'I'd review it' or 'check for errors' without specificity",
      "1": "Would use it with minimal or no check",
      "0": "No answer or 'trust the AI'"
    }
  },
  {
    "item_id": "byow_data_decision_1",
    "domain_id": "data_decision",
    "sequence": 4,
    "prompt_text": "Describe a situation where you had a lot of information to make sense of — data, documents, research — to reach a conclusion or recommendation. How would AI help with that?",
    "scoring_rubric": {
      "4": "Describes a specific workflow: what to feed AI, how to prompt for synthesis, how to verify the output, how to translate it into a decision",
      "3": "Identifies a realistic use case and a reasonable AI approach; missing verification or decision step",
      "2": "Mentions AI could summarize or analyze but no structured workflow",
      "1": "Vague ('AI could help me understand the data') with no specifics",
      "0": "No answer or not relevant"
    }
  },
  {
    "item_id": "byow_relationship_intel_1",
    "domain_id": "relationship_intel",
    "sequence": 5,
    "prompt_text": "Think about an important meeting or conversation coming up that you want to go well. How would or could AI help you prepare for it?",
    "scoring_rubric": {
      "4": "Describes a specific pre-meeting research workflow: stakeholder background, agenda synthesis, anticipated questions, post-meeting action capture",
      "3": "Identifies 2+ concrete prep activities AI could support; some specificity",
      "2": "Mentions AI could help with preparation but only one generic use (e.g. 'get background')",
      "1": "Vague or 'read their LinkedIn'",
      "0": "No answer or 'I don't prepare with AI'"
    }
  },
  {
    "item_id": "byow_augmented_comm_1",
    "domain_id": "augmented_comm",
    "sequence": 6,
    "prompt_text": "What's the most important or frequent written output in your job — a report, proposal, email, briefing? Walk me through how you'd use AI to help produce it better or faster.",
    "scoring_rubric": {
      "4": "Names a specific output type; describes a structured AI workflow (draft → tone calibration → review → edit loop); shows awareness of audience and confidentiality",
      "3": "Names the output and describes a reasonable 2-step AI process; missing audience or confidentiality awareness",
      "2": "Mentions using AI to draft something but no workflow structure",
      "1": "Vague ('have AI write it for me') with no process",
      "0": "No answer or 'I write everything myself'"
    }
  }
]
```

---

### 5.4 — BYOW scorer (`utils/ai.py`)

New function `score_byow_diagnostic()`. Returns **same shape** as `score_diagnostic()` —
no changes needed downstream (Skills Profile, gap map, path assembly all unchanged).

```python
def score_byow_diagnostic(
    responses: list[dict],   # [{item_id, domain_id, prompt_text, response_text}]
    user_email: str = None,
    lang: str = "en",
) -> dict:
    """
    Score 6 BYOW diagnostic responses in a single LLM call.

    Returns:
        {
            "item_scores":   {"byow_responsible_ai_1": float, ...},
            "domain_scores": {"responsible_ai": float, ...},
            "overall_score": float,
        }
    """
```

**LLM call design:** Single call (not per-domain like `score_diagnostic`). All 6 responses
+ all 6 rubrics in one prompt. `gemini-2.0-flash`, temperature 0.1.

**System prompt structure:**
```
You are an AI skills assessor scoring a professional's diagnostic responses.

Score each response on a 0–4 scale using the rubric provided.
Return ONLY valid JSON: {"scores": {"<item_id>": <float 0-4>, ...}}
Be calibrated: most working professionals score 1.5–2.5. Reserve 3.5–4.0 for
demonstrated mastery with specifics. Score 0 only for no answer.
```

**UX latency:** ~3–8 seconds after submit (single batch call, ~1700 input tokens).
Acceptable — same order as current diagnostic MCQ scoring.

**Model choice:** `gemini-2.0-flash` temperature 0.1 — fast, cheap, deterministic.
Use `databricks-claude-haiku-4-5` as fallback if Gemini quota exceeded.

---

### 5.5 — Diagnostic page rewrite (`pages/01_Diagnostic.py`)

**Replace** MCQ item rendering with 6 `st.text_area()` prompts. Key changes:

**Remove:**
- `get_diagnostic_items(role_id)` import and call
- `TOTAL = len(items)` MCQ loop
- Per-item MCQ/micro_task rendering
- `role_id`-based item selection

**Add:**
- Load `content/diagnostic_prompts.json` (no role param — universal)
- 6 `st.text_area()` prompts, all rendered at once (not sequenced one-by-one)
- Single "Submit Assessment →" button (enabled when all 6 have ≥ 20 chars)
- On submit: call `score_byow_diagnostic(responses, user_email, lang)`
- Everything downstream (save_diagnostic, generate_gap_map, assemble_path) unchanged

**UX flow change:** Current flow shows one question at a time (6 clicks to progress).
BYOW shows all 6 at once — user fills at their own pace, submits when done.
This is intentional: BYOW prompts benefit from seeing all 6 together (they can calibrate
the effort level and plan their responses).

**Minimum response length guard:** 20 chars per prompt before submit is enabled.
Show a character count hint: "Aim for 3–5 sentences per answer."

---

### 5.6 — UAT

Extend `.claude/evals/baseline-uat.md` with Group G: BYOW Diagnostic.

Test personas:
- `G7a` — Known role (RM shortcut selected in Advanced Options)
- `G7b` — Unknown role (Sr. Technical Advisor text pasted as Q1)
- `G7c` — Minimal answers (20 chars per prompt) → scores in low range (0.5–1.5)
- `G7d` — Rich answers → scores in mid-high range (2.0–3.5)

Key checks:
- All 6 prompts render, none gated by role
- Submit disabled until all 6 ≥ 20 chars
- Scoring spinner appears, completes in < 15 seconds
- Skills Profile renders with valid hexagon (no zero scores)
- Path assembly produces 7 atoms (no fallback errors)
- G7a (RM shortcut) still produces valid scores (regression)

---

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `content/diagnostic_prompts.json` has 6 prompts, one per domain, no `role_id` field | 🔜 |
| 2 | `01_Diagnostic.py` renders 6 text_area prompts for any user regardless of role | 🔜 |
| 3 | Submit disabled until all 6 responses ≥ 20 chars | 🔜 |
| 4 | `score_byow_diagnostic()` returns same dict shape as `score_diagnostic()` | 🔜 |
| 5 | A user who pastes the Sr. Technical Advisor JD gets a valid 7-module path | 🔜 |
| 6 | A user who selects RM shortcut still completes diagnostic successfully (regression) | 🔜 |
| 7 | `data_decision__universal_analysis` atom in library — inline eval, zero unfilled placeholders | 🔜 |
| 8 | Intake LLM parse extracts 6 fields including `industry` and `org_type` | 🔜 |
| 9 | `pytest` all passing | 🔜 |
| 10 | G7a–G7d UAT checks pass | 🔜 |

---

## New Files

- `content/diagnostic_prompts.json` — 6 BYOW prompts with scoring rubrics

## Modified Files

- `pages/00_Welcome.py` — enriched LLM parse prompt (6 fields), label update, remove `role_id` keyword inference
- `pages/01_Diagnostic.py` — replace MCQ rendering with BYOW text_area flow
- `utils/ai.py` — add `score_byow_diagnostic()`
- `content/atomic_modules_v2.json` — append `data_decision__universal_analysis`
- `.claude/evals/baseline-uat.md` — add G7 BYOW test group

## Non-Goals for Phase 5

- LinkedIn OAuth login (Phase 6)
- ZH translation of new diagnostic prompts (extend `translate_content.py` later)
- Rewriting existing `diagnostic_items.json` scenario_text fields (legacy kept as-is)
- Removing the `role_id` field from `user_profiles` Firestore (backward compat kept)
- Removing old `get_diagnostic_items()` from `utils/content.py` (kept for potential admin use)

---

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LLM scores BYOW responses inconsistently (same answer, different scores on retry) | Medium | Temperature 0.1 + calibration instruction in system prompt ("most professionals score 1.5–2.5") |
| Users write one-sentence answers, producing artificially low scores | Medium | 20-char minimum + "Aim for 3–5 sentences" hint; low scores are still valid signal |
| `score_byow_diagnostic()` LLM call times out for long responses | Low | Responses capped at 500 chars each via `maxlength` on text_area; total input stays < 3000 tokens |
| RM shortcut regression — role selector no longer gates diagnostic items | Low | G7a UAT specifically tests this path; `score_byow_diagnostic()` is role-agnostic by design |
| `data_decision__universal_analysis` atom content too generic | Medium | Human review before append; re-run `generate_atom.py` at temperature 0.5 if output is flat |
