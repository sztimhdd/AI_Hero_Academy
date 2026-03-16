# Reading Content Template System — Agent Kickstart Prompt

Copy the section below into a new Claude Code session to implement the reading templates.

---

## Kickstart Prompt

You are implementing the **Reading Content Template System** for the AI Hero Academy Streamlit app.

This work enriches the reading section of the Course Module page with 4 distinct visual
templates — one per section type — replacing the current flat-text rendering with
structured, card-based layouts built from native Streamlit components.

### Read these files first (in order):

1. `plans/reading-templates-plan.md` — full plan: schemas, renderer code, extraction prompts, tasks
2. `references/ux-mockups/concept_text.html` — mockup for Concept section (acronym card grid)
3. `references/ux-mockups/good_example.html` — mockup for Good Example (Before/After comparison)
4. `references/ux-mockups/anti_pattern.html` — mockup for Anti-Pattern (incident + cascade chain)
5. `references/ux-mockups/takeaway.html` — mockup for Takeaway (focal statement + action cards)
6. `pages/04_Course_Module.py` — the reading section is at lines 238–301 (the `elif active_sub == "reading":` block)
7. `utils/content.py` — you will add `get_reading_structured()` here
8. `scripts/generate_course_content.py` (lines 1–60 only) — understand the SDK pattern to reuse in the new script

### Branch setup (do this first):

```bash
git checkout main && git pull
git checkout -b feature/reading-templates
```

### What to build (6 tasks, in order):

---

**RT-1 — Streamlit docs research (do before writing any renderer)**

Query Context7 before writing any renderer code:

```python
mcp__context7__resolve-library-id("streamlit")
# then:
mcp__context7__query-docs: "st.columns st.container border nested st.code st.caption"
mcp__context7__query-docs: "st.segmented_control st.columns nested content rendering"
```

Confirm these behaviors in the docs before proceeding:
- `st.code(text, language=None)` renders as a styled monospace block ✓
- `st.container(border=True)` accepts nested `st.code()`, `st.caption()`, `st.markdown()` ✓
- `st.columns(2)` works inside a `with content_col:` context ✓

**Only proceed to RT-2 after confirming the above.**

---

**RT-2 — Build `scripts/enrich_reading_content.py`** (new file, ~180 lines)

Create `scripts/enrich_reading_content.py`. The script must:

1. Read `content/reading_content.json` (dict keyed by `course_id`)
2. For each of the 21 items, call Haiku to extract 4 structured sub-fields
3. Write `content/reading_content_structured.json` (dict keyed by `course_id`; each value has only sub-fields)

**Use the SDK pattern from `generate_course_content.py`** — same `WorkspaceClient`, same
`tenacity` retry, same `HAIKU_ENDPOINT` env var.

**Use `temperature=0.0`** for all extraction calls — deterministic output is critical.

**Process items concurrently** (up to 4 workers with `ThreadPoolExecutor`) but extract
the 4 sub-fields per item **sequentially** to avoid bursting the rate limit.

CLI interface:
```bash
python scripts/enrich_reading_content.py             # enrich all 21 items
python scripts/enrich_reading_content.py --dry-run   # print to stdout, no write
python scripts/enrich_reading_content.py --course-id rm_course_1  # single item test
```

**The 4 extraction prompts** (embed as module-level string constants):

**CONCEPT_PROMPT** (for `concept_text_structured`):
```
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following concept_text field. The text describes a
named acronym framework (e.g. CRAF, SAFE, VERIFY) used in a professional AI workflow.

<concept_text>
{concept_text}
</concept_text>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "framework_acronym": "<the acronym letters, e.g. CRAF>",
  "intro": "<1-2 sentences introducing the framework and why it matters>",
  "cards": [
    {{"letter": "<single uppercase letter>", "title": "<one word>", "body": "<1-2 sentence description>"}},
    ...one card per acronym letter...
  ],
  "guardrails": ["<constraint 1>", ...]
}}

Rules:
- Extract one card per letter in the acronym, in order
- Preserve the source text closely; do not paraphrase beyond minor cleanup
- guardrails: extract any listed rules/constraints; use [] if none exist
- Return only the JSON object
```

**GOOD_EXAMPLE_PROMPT** (for `good_example_structured`):
```
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following good_example field. The text describes a
before/after scenario comparing an unsafe AI prompt with a corrected version.

<good_example>
{good_example}
</good_example>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "scenario": "<1 sentence: what task the practitioner is trying to accomplish>",
  "before_prompt": "<the unsafe/incorrect prompt or action, as a direct quote or close paraphrase>",
  "before_issue": "<1 sentence: what specific problem makes this unsafe or incorrect>",
  "after_prompt": "<the safe/correct prompt or action, as a direct quote or close paraphrase>",
  "after_benefit": "<1 sentence: what specific quality makes this version correct>",
  "outcome": "<1 sentence: what the corrected approach produces or achieves>"
}}

Rules:
- before_prompt and after_prompt should read as actual prompt text (monospace-renderable)
- Keep before_issue and after_benefit short — they appear as captions under the prompt
- Return only the JSON object
```

**ANTI_PATTERN_PROMPT** (for `anti_pattern_structured`):
```
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following anti_pattern field. The text describes a
failure scenario and its consequences.

<anti_pattern>
{anti_pattern}
</anti_pattern>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "headline": "<3-6 word name for this failure pattern>",
  "failure_scenario": "<2-3 sentences: what the practitioner did wrong and the immediate error>",
  "chain": ["<consequence 1>", "<consequence 2>", "<final impact (most damaging outcome)>"],
  "root_lesson": "<1-2 sentences: the specific rule or check that was skipped>"
}}

Rules:
- chain: 2–4 items; each is a single step in the domino effect; final item is worst outcome
- root_lesson must be actionable — what the learner should always do instead
- Return only the JSON object
```

**TAKEAWAY_PROMPT** (for `takeaway_structured`):
```
You are a content structuring assistant for an AI skills learning platform.

Given the reading item below, produce a structured takeaway with two action cards.

<concept_text>
{concept_text}
</concept_text>

<takeaway>
{takeaway}
</takeaway>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{{
  "statement": "<the takeaway sentence — preserve exactly as written>",
  "action_1": {{"title": "<3-5 word imperative>", "body": "<1-2 sentence elaboration>"}},
  "action_2": {{"title": "<3-5 word imperative>", "body": "<1-2 sentence elaboration>"}}
}}

Rules:
- statement: copy the takeaway text exactly; do not paraphrase
- action_1 and action_2: synthesise two complementary action points from the concept_text
  and takeaway; they should answer "what do I actually do differently on the job?"
- Return only the JSON object
```

**Error handling**: if any single sub-field extraction fails after 3 retries, log a warning,
skip that sub-field for that item, and continue. Never abort the whole run.

---

**RT-3 — Update `utils/content.py`**

Read `utils/content.py` first. Then add alongside the existing `get_reading_content()` function:

```python
_READING_STRUCTURED: dict | None = None

def get_reading_structured(course_id: str) -> dict | None:
    """
    Returns structured sub-fields dict for a course's reading content,
    or None if reading_content_structured.json has not been generated yet.
    """
    global _READING_STRUCTURED
    if _READING_STRUCTURED is None:
        p = _CONTENT_DIR / "reading_content_structured.json"
        if p.exists():
            _READING_STRUCTURED = json.loads(p.read_text())
        else:
            _READING_STRUCTURED = {}
    return _READING_STRUCTURED.get(course_id)
```

Use the exact same `_CONTENT_DIR` path constant already in `content.py`. No other changes.

---

**RT-4 — Run enrichment for all 21 items**

```bash
# Step 1: test one item
python scripts/enrich_reading_content.py --dry-run --course-id rm_course_1

# Step 2: spot-check the output in the terminal:
# - concept_text_structured.cards length should match the acronym letter count
# - good_example_structured.before_prompt reads like an actual prompt
# - anti_pattern_structured.chain has 2–4 items
# - takeaway_structured.statement is an exact copy of the takeaway field

# Step 3: if the single item looks good, run all 21
python scripts/enrich_reading_content.py

# Step 4: verify the output file
python -c "
import json
d = json.load(open('content/reading_content_structured.json'))
print(f'{len(d)} courses enriched:')
for k, v in d.items():
    fields = [f for f in ['concept_text_structured','good_example_structured','anti_pattern_structured','takeaway_structured'] if f in v]
    print(f'  {k}: {len(fields)}/4 sub-fields')
"
```

If any item produced malformed JSON or missing sub-fields, re-run with `--course-id <id>`
to regenerate that item. Manually fix edge cases by editing the JSON directly.

---

**RT-5 — Add template renderers + wiring to `pages/04_Course_Module.py`**

1. Add the import at the top of the file:
   ```python
   from utils.content import get_reading_structured
   ```

2. Add 4 renderer functions as module-level functions, just before the
   `elif active_sub == "reading":` block. Use the exact code from the plan's
   "Streamlit Rendering Strategy" section (`_render_concept`, `_render_good_example`,
   `_render_anti_pattern`, `_render_takeaway`).

3. In the reading section, after `reading = get_reading_content(course_id)`, add:
   ```python
   reading_s = get_reading_structured(course_id)
   ```

4. Replace the `with content_col:` block (lines 264–278) with the structured/fallback
   wiring from the plan. The "Mark Reading Complete →" button block remains unchanged.

**Constraint**: the renderer functions must ONLY call native Streamlit components.
No `unsafe_allow_html=True`. No custom CSS injection. Fallback to flat text if
`reading_s` is None.

---

**RT-6 — Visual verification with Playwright**

After implementation, start the local server and verify each template visually:

```bash
bash run_uat.sh
```

Use Playwright MCP tools to:
1. Navigate to `http://localhost:8501`
2. Go to Home → Module 1 → Start Reading
3. Take a screenshot of the Concept section — verify 2×N card grid
4. Click to Example section — verify Before/After side-by-side layout
5. Click to Pitfall section — verify cascade chain + error callout
6. Click to Takeaway section — verify large statement + 2 action cards + complete button

Take screenshots at each section and confirm visual output matches the intent of the
`references/ux-mockups/*.html` mockups (structure and hierarchy, not pixel-perfect match).

**Also run:**
```bash
.venv/Scripts/python -m pytest tests/ -q
```

Confirm no scoring or navigation regressions.

---

### Key constraints:

- Only modify `pages/04_Course_Module.py`, `utils/content.py`, and create new files
  (`scripts/enrich_reading_content.py`, `content/reading_content_structured.json`)
- Do NOT modify `content/reading_content.json` — source content is read-only
- Do NOT modify `generate_course_content.py`
- Never add `unsafe_allow_html=True` in the renderer functions
- Keep the existing `st.segmented_control` navigation, `st.columns([1, 4, 1])` wrapper,
  and "Mark Reading Complete →" button logic completely unchanged
- Renderer functions are module-level (defined above the `elif active_sub` block),
  not nested inside the reading section

---

### Commit when done:

```bash
git add scripts/enrich_reading_content.py \
        content/reading_content_structured.json \
        utils/content.py \
        pages/04_Course_Module.py
git commit -m "feat(reading): structured template renderers + AI enrichment script"
```

Then ask the user if they want to merge to main or keep the branch for review.

---

### Acceptance checklist:

- [ ] `python scripts/enrich_reading_content.py` completes for all 21 items without errors
- [ ] `content/reading_content_structured.json` has exactly 21 keys, each with 4 sub-fields
- [ ] Concept: 2×N card grid with emoji-colored letter badges and body text
- [ ] Concept: guardrails in `st.info()` below the card grid
- [ ] Good Example: scenario card above Before/After columns; `st.code()` blocks for prompts
- [ ] Good Example: outcome in `st.success()`
- [ ] Anti-Pattern: failure scenario in bordered container; numbered cascade list; `st.error()` root lesson
- [ ] Takeaway: `###` statement + 2-column action cards + "Mark Reading Complete →" below
- [ ] Fallback: deleting `reading_content_structured.json` and reloading shows flat-text fallback — no errors
- [ ] No `unsafe_allow_html=True` in any renderer function
- [ ] `bash run_uat.sh` passes all UAT scenarios; no regressions on other sub-views
- [ ] Playwright screenshots confirm correct visual hierarchy for all 4 sections
