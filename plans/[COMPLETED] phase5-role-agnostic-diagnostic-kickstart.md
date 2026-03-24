# Phase 5 Kickstarter — Role-Agnostic Diagnostic & Intake

> Paste this entire prompt into a new Claude Code session to implement Phase 5.

---

## Mission

Break the role-based diagnostic bottleneck. Replace the role-gated MCQ diagnostic with
a universal "Bring Your Own Work" (BYOW) flow that produces valid domain scores for any
job title. Enrich the intake form. Add a universal `data_decision` atom.

Full plan: `plans/phase5-role-agnostic-diagnostic-plan.md`. Read it before starting.

---

## Key Files to Read First

1. `plans/phase5-role-agnostic-diagnostic-plan.md` — full plan, rubrics, acceptance criteria
2. `pages/01_Diagnostic.py` — current MCQ diagnostic page (full read required)
3. `pages/00_Welcome.py` — current intake form (read the LLM parse block ~line 345)
4. `utils/ai.py` — `score_diagnostic()` function — BYOW scorer must return identical shape
5. `content/diagnostic_items.json` — understand current schema (do NOT modify this file)
6. `utils/path_assembler.py` — `fill_scenario()` — check if new data_decision atom needs new placeholders
7. `.claude/evals/baseline-uat.md` — understand UAT structure before adding G7

**IMPORTANT:** After completing each major step, run `/compact` before starting the next.
Specify what to preserve. This sprint touches 5 files — context management is critical.

---

## Step 1 — Generate `data_decision__universal_analysis` atom

Use the existing `scripts/generate_atom.py`. First add the new atom spec to `ATOM_SPECS`
in that script, then generate.

**Atom spec to add to `ATOM_SPECS` dict:**

```python
"data_decision__universal_analysis": {
    "title": "Signal to Decision: AI-Assisted Analysis for Any Role",
    "domain": "data_decision",
    "capability_tags": [
        "data_synthesis",
        "ai_assisted_analysis",
        "decision_support",
        "insight_generation",
        "structured_reasoning",
    ],
    "employee_hook": (
        "Turn any dataset, report, or information pile into a clear decision "
        "recommendation in under 10 minutes — regardless of your role or industry."
    ),
    "framework": (
        "SIGNAL framework: Source (identify your inputs) → Interrogate (prompt AI to "
        "surface patterns) → Generate (produce structured insight) → Narrate (translate "
        "to plain language) → Act (link insight to decision) → Log (record for audit trail)"
    ),
    "priority": 1,
},
```

**Generate and validate:**

```bash
python scripts/generate_atom.py --atom-id data_decision__universal_analysis
```

Review output quality:
- `reading.concept_text` first 2 sentences answer "what's in this for ME"
- `good_example` is concrete and role-agnostic (not "your portfolio dashboard")
- `scenario_template` uses only allowed `{placeholder}` tokens
- `eval.items_ref == "inline"`, 4 inline items (3 MCQ + 1 perf task)

If quality is good, append to `content/atomic_modules_v2.json`:

```python
python -c "
import json
atoms = json.load(open('content/atomic_modules_v2.json', encoding='utf-8'))
new = json.load(open('tmp_dd_universal.json', encoding='utf-8'))
atoms.append(new)
with open('content/atomic_modules_v2.json', 'w', encoding='utf-8') as f:
    json.dump(atoms, f, indent=2, ensure_ascii=False)
print(f'Total: {len(atoms)} atoms')
"
```

Run validation:
```bash
.venv/Scripts/python -m pytest tests/test_path_assembler.py -v
```

**→ /compact after Step 1: preserve atom_id and validation result, remove generation output**

---

## Step 2 — Create `content/diagnostic_prompts.json`

Create this new file with exactly 6 prompts. Full content is in
`plans/phase5-role-agnostic-diagnostic-plan.md` Section 5.3 — copy it verbatim.

Schema per item:
```json
{
  "item_id": "byow_<domain>_1",
  "domain_id": "<domain>",
  "sequence": <1-6>,
  "prompt_text": "...",
  "scoring_rubric": {
    "4": "...",
    "3": "...",
    "2": "...",
    "1": "...",
    "0": "..."
  }
}
```

Verify the file loads cleanly:
```bash
.venv/Scripts/python -c "
import json
prompts = json.load(open('content/diagnostic_prompts.json', encoding='utf-8'))
print(f'{len(prompts)} prompts')
domains = [p['domain_id'] for p in prompts]
print('Domains:', domains)
assert len(prompts) == 6
assert len(set(domains)) == 6
print('OK')
"
```

---

## Step 3 — Add `score_byow_diagnostic()` to `utils/ai.py`

**Read `utils/ai.py` first.** Find `score_diagnostic()` (~line 169). Add the new function
immediately after it.

```python
def score_byow_diagnostic(
    responses: list[dict],
    user_email: str = None,
    lang: str = "en",
) -> dict:
    """
    Score 6 BYOW open-ended diagnostic responses in a single LLM call.

    responses: list of {
        "item_id": str,         # e.g. "byow_responsible_ai_1"
        "domain_id": str,
        "prompt_text": str,     # the question shown to the user
        "response_text": str,   # what the user typed
        "scoring_rubric": dict, # {"4": "...", "3": "...", ...}
    }

    Returns same shape as score_diagnostic():
        {
            "item_scores":   {"byow_responsible_ai_1": float, ...},
            "domain_scores": {"responsible_ai": float, ...},
            "overall_score": float,
        }
    """
```

**System prompt for the LLM call:**
```python
_BYOW_SCORER_SYSTEM = """\
You are an AI skills assessor scoring a professional's self-reported diagnostic responses.

Score each response 0–4 using the rubric provided per item.
Return ONLY valid JSON: {"scores": {"<item_id>": <float>, ...}}

Calibration guide:
- 0: No answer, irrelevant, or actively wrong
- 1.0–1.4: Vague awareness, no concrete action
- 1.5–2.4: Basic practical use, some structure (most first-time users)
- 2.5–3.4: Structured approach with specifics, demonstrates real usage
- 3.5–4.0: Mastery — systematic, verified, role-appropriate (rare)

Do not reward length. Reward specificity and structured thinking.\
"""
```

**User prompt construction:** Build a single message with all 6 responses + rubrics.
Format each as:
```
ITEM: byow_responsible_ai_1 (Domain: responsible_ai)
QUESTION: <prompt_text>
RESPONSE: <response_text>
RUBRIC: 4=<...> | 3=<...> | 2=<...> | 1=<...> | 0=<...>
```

**LLM call:** Use `call_llm()` (already in `utils/ai.py`), temperature=0.1,
`call_type="byow_diagnostic_scoring"`.

**Post-processing:** Parse JSON response → compute domain_scores (one item per domain,
so domain_score = item_score directly) → overall_score = mean of domain_scores.

**Cap each score:** `min(max(float(v), 0.0), 4.0)` before storing.

---

## Step 4 — Rewrite `pages/01_Diagnostic.py`

**Read the full file first** before making any changes.

**Remove:**
- `get_diagnostic_items` import and call
- `TOTAL = len(items)`, MCQ/micro_task loop, per-item rendering
- `role_id`-based item selection logic

**Keep unchanged:**
- Auth guard (`get_profile`, `st.switch_page` if no profile)
- `_lang` / `render_lang_sidebar`
- `get_domain_descriptions` (still used for gap map context)
- `score_diagnostic` import → **replace** with `score_byow_diagnostic`
- `generate_gap_map`, `save_diagnostic`, `save_gap_map`, `save_assembled_path`
- `assemble_path`, `get_atomic_modules`
- All downstream logic after scoring (Skills Profile redirect, etc.)

**New rendering block:**

```python
# Load universal BYOW prompts (no role param)
import json
from pathlib import Path
_PROMPTS_PATH = Path("content/diagnostic_prompts.json")
byow_prompts = json.loads(_PROMPTS_PATH.read_text(encoding="utf-8"))

st.header(t("diag.title", _lang))
st.write(t("diag.byow_intro", _lang))  # Add i18n key (see below)

responses = []
all_filled = True
for prompt in byow_prompts:
    val = st.text_area(
        prompt["prompt_text"],
        key=f"byow_{prompt['item_id']}",
        max_chars=500,
        help="Aim for 3–5 sentences.",
    )
    if not val or len(val.strip()) < 20:
        all_filled = False
    responses.append({
        "item_id": prompt["item_id"],
        "domain_id": prompt["domain_id"],
        "prompt_text": prompt["prompt_text"],
        "response_text": val or "",
        "scoring_rubric": prompt["scoring_rubric"],
    })

if st.button(t("diag.submit_btn", _lang), disabled=not all_filled, type="primary"):
    with st.spinner(t("diag.spinner_scoring", _lang)):
        result = score_byow_diagnostic(responses, user_email=user_email, lang=_lang)
    # ... save + redirect (same as current flow)
```

**Add 2 i18n keys** to `content/i18n/en.json` (and stub in `zh.json`):
- `"diag.byow_intro"`: `"Answer each question based on your own work experience. There are no right or wrong answers — your responses shape your personalised training path."`
- `"diag.submit_btn"` already exists — verify it does, add if missing

**Session state:** Replace `diag_item_index` / `diag_responses` with simpler:
`st.session_state["byow_submitted"] = True` after successful score + save.
Use `st.rerun()` to navigate to Skills Profile (same as current).

---

## Step 5 — Enrich intake in `pages/00_Welcome.py`

**Read the file first.** Find the LLM parse block (~line 345–390).

**Change 1 — Q1 label:** Find the `st.text_area` for Q1. Update its label/placeholder
to encourage JD paste:

```python
# Old label: t("welcome.q1_label", _lang)
# New: update the i18n key value in en.json:
# "welcome.q1_label": "Paste your job description, or describe your role and main responsibilities"
# "welcome.q1_placeholder": "You can paste a job posting, LinkedIn summary, or write 2-3 sentences about what you do and what your biggest time sinks are."
```

**Change 2 — LLM parse prompt:** Replace the existing `_parse_prompt` string:

```python
_parse_prompt = (
    "Extract structured information from this employee job description or self-description. "
    "Return ONLY valid JSON with exactly these keys:\n"
    "  role_text: job title in 3-5 words\n"
    "  daily_tasks: list of 4-5 specific task strings (verbs, e.g. 'review credit applications')\n"
    "  magic_wish: the primary AI benefit this person would want, one sentence\n"
    "  industry: industry or sector in 2-3 words (e.g. 'project finance', 'insurance', 'engineering')\n"
    "  org_type: type of organization in 3-5 words (e.g. 'financial Crown corporation')\n"
    "  seniority: one of: junior, mid, senior, executive"
)
```

**Change 3 — Remove keyword role_id inference block:**
Find and remove:
```python
if any(kw in _role_text_lower for kw in ["relationship manager", " rm ", ...]):
    _inferred_role_id = "rm"
elif ...
```
Replace with:
```python
# role_id: use Advanced Options selection if provided; else "universal"
_adv_sel = st.session_state.get("welcome_role", _adv_role_placeholder)
_inferred_role_id = _role_map.get(_adv_sel, "universal")
```

**Add `"universal"` to `_role_map`** (or handle it as the default — no atom loading
depends on role_id in the atom path).

---

## Step 6 — UAT

Extend `.claude/evals/baseline-uat.md` with **Group G: BYOW Diagnostic**.

Add the following test group based on the pattern in the existing groups:

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| G7.1 | Diagnostic page shows 6 text_area prompts, no MCQ | snapshot | 6 open text boxes visible, no radio buttons |
| G7.2 | Submit disabled with empty responses | snapshot | Button is disabled state |
| G7.3 | Submit enabled after filling all 6 (≥20 chars each) | snapshot | Button active |
| G7.4 | Scoring spinner appears on submit | snapshot | Spinner visible |
| G7.5 | Skills Profile hexagon renders with 6 valid scores | snapshot | No zero or None scores |
| G7.6 | Path assembles 7 modules | snapshot | 7 module cards on Home |
| G7.7 | RM shortcut (Advanced Options) still works end-to-end | manual | Select RM → complete BYOW → valid path |
| G7.8 | Unknown role text pasted → valid path (no errors) | manual | Paste Sr. Technical Advisor JD → complete |
| G7.9 | No console errors throughout | code | `browser_console_messages` clean |

**Reset for G7 tests:**
```bash
python scripts/reset_uat_user.py   # full wipe → Welcome page
```

Run the app:
```bash
bash run_uat.sh
```

Use Playwright MCP tools directly in the main session (never sub-agents):
```python
mcp__playwright__browser_navigate(url="http://localhost:8501")
```

---

## Done When

- `content/diagnostic_prompts.json` has 6 prompts, no `role_id`
- `01_Diagnostic.py` shows 6 BYOW text_areas for any user
- `score_byow_diagnostic()` returns `{item_scores, domain_scores, overall_score}`
- `data_decision__universal_analysis` atom in library — 21 total atoms
- Intake parse extracts 6 fields
- All pytest passing
- G7 UAT checks pass (G7.1–G7.9)

---

## Key Constraints

- `score_byow_diagnostic()` output shape MUST match `score_diagnostic()` exactly — nothing downstream changes
- `content/diagnostic_items.json` is NOT modified — legacy kept for ZH compat
- `get_diagnostic_items()` in `utils/content.py` is NOT removed — kept for potential admin use
- Gemini SDK: `google-genai` (not `google-generativeai`). Import: `from google import genai`
- All Playwright MCP calls in main session — never delegate to sub-agents
- `/compact` between each major step — this sprint is wide (5 files modified)
