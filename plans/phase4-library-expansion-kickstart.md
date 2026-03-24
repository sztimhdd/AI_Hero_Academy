# Phase 4 Kickstarter — Atomic Library Expansion

> Paste this entire prompt into a new Claude Code session to implement Phase 4.

---

## Mission

Expand the atomic module library from 15 → 20 canonical atoms by authoring 5 new
universal atoms directly in atomic-ready JSON format, and update the eval loader in
`pages/04_Course_Module.py` to support inline eval items so new atoms are fully
self-contained.

The full plan is at `plans/phase4-library-expansion-plan.md`. Read it before starting.

---

## Key Files to Read First

1. `plans/phase4-library-expansion-plan.md` — full plan with schema, tasks, acceptance criteria
2. `content/atomic_modules_v2.json` — read one complete canonical atom to understand the schema
3. `scripts/enrich_reading_content.py` — copy the SDK auth + retry + CLI pattern
4. `utils/path_assembler.py` — `fill_scenario()` function: know which `{placeholder}` tokens are handled
5. `pages/04_Course_Module.py` — find the eval item loading block (search for `source_course_ids`)

---

## Step 1 — Create `scripts/generate_atom.py`

Write a CLI script that generates a single atom as JSON using the Gemini API.

**Pattern:** Copy the WorkspaceClient + tenacity retry + argparse CLI structure from
`scripts/enrich_reading_content.py`.

**Model:** `gemini-2.0-flash`, temperature 0.3
**Auth:** `GOOGLE_APPLICATION_CREDENTIALS` from `.env` via `python-dotenv`

**CLI:**

```bash
python scripts/generate_atom.py --atom-id relationship_intel__meeting_intelligence
python scripts/generate_atom.py --atom-id <id> --dry-run   # print prompt, exit
```

**Hardcode this `ATOM_SPECS` dict in the script:**

```python
ATOM_SPECS = {
    "relationship_intel__meeting_intelligence": {
        "title": "Meeting Intelligence: Know Every Room Before You Walk In",
        "domain": "relationship_intel",
        "capability_tags": ["meeting_prep", "stakeholder_research", "action_item_extraction",
                            "pre_meeting_synthesis", "meeting_follow_up"],
        "employee_hook": "Walk into every meeting knowing more context than the person who called it.",
        "framework": "3-phase loop: Pre-meeting research → In-meeting synthesis → Post-meeting action capture",
        "priority": 1,
    },
    "augmented_comm__email_message_drafting": {
        "title": "Email Intelligence: Draft, Tone, and Send in Minutes",
        "domain": "augmented_comm",
        "capability_tags": ["email_drafting", "tone_calibration", "async_communication",
                            "stakeholder_messaging", "follow_up_sequencing"],
        "employee_hook": "Email drafting is the #1 daily time sink AI eliminates — reclaim it today.",
        "framework": "TONE framework: Target audience → Objective → Nuance → Edit loop",
        "priority": 2,
    },
    "strategic_prompting__iterative_refinement": {
        "title": "Iterative Prompting: From Good Output to Great Output",
        "domain": "strategic_prompting",
        "capability_tags": ["multi_turn_prompting", "output_refinement", "prompt_iteration",
                            "critique_prompting", "constraint_narrowing"],
        "employee_hook": "One more prompt turn converts a mediocre draft into something you'd actually send.",
        "framework": "REFINE loop: Review → Evaluate gap → Feed back constraint → Iterate → Next",
        "priority": 3,
    },
    "critical_eval__hallucination_patterns": {
        "title": "Hallucination Patterns: The 5 Most Dangerous AI Errors",
        "domain": "critical_eval",
        "capability_tags": ["hallucination_detection", "fact_verification", "ai_error_patterns",
                            "source_checking", "credibility_protection"],
        "employee_hook": "One unchecked AI error forwarded to leadership can undo months of credibility.",
        "framework": "5 error types: False facts, Fabricated citations, Plausible-but-wrong numbers, "
                     "Confident confabulation, Outdated information",
        "priority": 4,
    },
    "responsible_ai__ai_tool_governance": {
        "title": "AI Tool Governance: Choose the Right Tool, Every Time",
        "domain": "responsible_ai",
        "capability_tags": ["tool_selection", "ai_literacy", "policy_compliance",
                            "tool_risk_assessment", "approved_tools"],
        "employee_hook": "Knowing which AI tool to use — and which to avoid — is a career skill, not a policy box to check.",
        "framework": "SELECT framework: Sensitivity check → Evaluate alternatives → Legal/policy check → "
                     "Evaluate data residency → Compare output quality → Track and document",
        "priority": 5,
    },
}
```

**LLM system prompt** (instruct the model to output a complete atom JSON):

```
You are an instructional designer authoring atomic AI skills modules for a corporate training app.

Output a single JSON object — no markdown fences, no explanation.

The atom must follow this exact schema:
{
  "atom_id": "<atom_id>",
  "title": "<title>",
  "domain": "<domain>",
  "capability_tags": [...],         # 3–6 short snake_case tokens
  "estimated_minutes": 30,
  "role_variants_hint": "...",      # 1–2 sentences: what adapts per role; which placeholders matter
  "reading": {
    "concept_text": "...",          # 150–250 words; first 2 sentences answer: what's in this for ME?
    "good_example": "...",          # concrete time-saving or quality-improvement win
    "anti_pattern": "...",          # the costly mistake this skill prevents
    "takeaway": "..."               # one sentence: specific personal benefit
  },
  "practice": {
    "scenario_template": "...",     # must contain {role} and {org_type}; use allowed placeholders only
    "task_templates": [             # exactly 4 tasks
      {
        "task_id": 1,
        "text_template": "...",
        "skill_focus": "...",
        "task_mode": "open",        # "open" or "mcq"
        "mcq_options": null         # null if open; [{label, is_best}] if mcq
      }
    ],
    "coach_system_prompt_template": "..."   # no hardcoded role/org; use {role}, {organisation}, {scenario_name}
  },
  "eval": {
    "items_ref": "inline",
    "inline_items": [               # exactly 4 items: sequences 1–3 are mcq, sequence 4 is performance_task
      {
        "item_id": "ev_<atom_id>_q1",
        "item_type": "mcq",
        "sequence": 1,
        "question_text": "...",
        "scenario_text": "...",
        "options": [{"label": "A", "text": "..."}, {"label": "B", "text": "..."}, {"label": "C", "text": "..."}, {"label": "D", "text": "..."}],
        "correct_answer": "B",
        "score_value": 1
      },
      ... (q2, q3 same structure),
      {
        "item_id": "ev_<atom_id>_q4",
        "item_type": "performance_task",
        "sequence": 4,
        "question_text": "...",
        "scenario_text": "...",
        "rubric": [{"criterion": "...", "weight": 0.25}, {"criterion": "...", "weight": 0.25}, {"criterion": "...", "weight": 0.25}, {"criterion": "...", "weight": 0.25}]
      }
    ],
    "source_course_ids": []
  },
  "source_course_ids": [],
  "merged_from": [],
  "atomized_at": "2026-03-24",
  "status": "canonical"
}

Content rules:
1. reading.concept_text must answer "what's in this for ME personally?" in the first 2 sentences.
2. Every good_example shows a concrete time-saving or quality win — not just policy compliance.
3. scenario_template MUST use only these placeholders (no others):
   {role}, {org_type}, {case_type}, {data_types}, {workflow_goal}, {programme_name},
   {audience}, {sensitivity_level}, {scenario_name}, {organisation}, {domain}
4. Never hardcode "EDC", "analyst", or any real org name in the content.
5. Fictional company names in examples (Meridian, Aurora, Crestwood) are acceptable.
6. task_mode must be "open" or "mcq" — at least 1 of the 4 tasks should be "mcq".
7. eval questions must test the specific framework named in the atom, not generic AI knowledge.
8. Output only valid JSON — no prose, no markdown.
```

---

## Step 2 — Generate and Validate All 5 Atoms

Run in priority order. Review the JSON output before appending.

```bash
# P1 — highest priority
python scripts/generate_atom.py --atom-id relationship_intel__meeting_intelligence

# Review output. If quality is good, append to atomic_modules_v2.json.
# Repeat for each:
python scripts/generate_atom.py --atom-id augmented_comm__email_message_drafting
python scripts/generate_atom.py --atom-id strategic_prompting__iterative_refinement
python scripts/generate_atom.py --atom-id critical_eval__hallucination_patterns
python scripts/generate_atom.py --atom-id responsible_ai__ai_tool_governance
```

**Validation after all 5 are appended:**

```python
python -c "
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

atoms = json.load(open('content/atomic_modules_v2.json', encoding='utf-8'))
print(f'Total atoms: {len(atoms)}')   # expect 20

new_ids = [
    'relationship_intel__meeting_intelligence',
    'augmented_comm__email_message_drafting',
    'strategic_prompting__iterative_refinement',
    'critical_eval__hallucination_patterns',
    'responsible_ai__ai_tool_governance',
]

KNOWN_PLACEHOLDERS = dict.fromkeys([
    'role','org_type','case_type','data_types','workflow_goal',
    'programme_name','audience','sensitivity_level','scenario_name',
    'organisation','domain'
], 'X')

for a in atoms:
    if a['atom_id'] not in new_ids:
        continue
    tags_ok = 3 <= len(a.get('capability_tags', [])) <= 6
    inline_ok = a['eval'].get('items_ref') == 'inline'
    items_ok = len(a['eval'].get('inline_items', [])) == 4
    filled = a['practice']['scenario_template'].format_map(KNOWN_PLACEHOLDERS)
    unfilled = re.findall(r'\{[a-z_]+\}', filled)
    print(f'{a[\"atom_id\"]}:')
    print(f'  tags={tags_ok} inline={inline_ok} items={items_ok} unfilled={unfilled}')
" 2>&1 | cat
```

If `unfilled` is non-empty for any atom, add the missing placeholder to `fill_scenario()`
in `utils/path_assembler.py` before proceeding.

Also run the existing pytest suite — no regressions allowed:

```bash
.venv/Scripts/pytest tests/test_path_assembler.py -v
```

---

## Step 3 — Update Eval Loader in `pages/04_Course_Module.py`

**HOLD THIS STEP until Phase 3 ZH UAT is closed.**
(Risk: merge conflict in 53 KB file if ZH UAT raises a bug there.)

When ZH UAT is closed, read `pages/04_Course_Module.py` and find the block that loads
eval items via `source_course_ids`. Add the inline branch immediately before it:

```python
eval_section = atom.get("eval", {})
if eval_section.get("items_ref") == "inline":
    eval_items = eval_section["inline_items"]
else:
    # existing lookup — unchanged
    course_id = eval_section["source_course_ids"][0]
    eval_items = get_eval_items(course_id)
```

---

## Step 4 — Smoke Test

```bash
bash run_uat.sh
```

Use Playwright MCP tools directly in the main session (never via sub-agents):

```python
mcp__playwright__browser_navigate(url="http://localhost:8501")
```

Verify:

1. A demo persona (3a–3f) loads the Home page without errors
2. Click "Start Module 1" → Reading tab loads correctly
3. Navigate to Evaluation tab → questions render (tests inline eval if the path includes a new atom)
4. No Python exceptions in the terminal

---

## Done When

- `content/atomic_modules_v2.json` has 20 atoms
- All 5 new atoms pass validation (inline eval, no unfilled placeholders, 3–6 tags)
- `pytest tests/test_path_assembler.py` — all passing
- Smoke test confirms no regressions
- `pages/04_Course_Module.py` eval loader updated (after ZH UAT)
- PLAN.md Phase 4 acceptance criteria all ticked ✅

---

## Key Constraints

- Gemini SDK: `google-genai` (not `google-generativeai`). Import: `from google import genai`
- Auth: `GOOGLE_APPLICATION_CREDENTIALS` from `.env`, loaded via `python-dotenv`
- Temperature: 0.3 for content generation
- Never hardcode "EDC", "analyst", specific org names in atom content
- All `{placeholder}` tokens used in new atoms MUST also be handled in `fill_scenario()`
- Do NOT call MCP tools from sub-agents — call `mcp__playwright__browser_*` directly
- Do NOT `pip install playwright` — use the Playwright MCP server directly
