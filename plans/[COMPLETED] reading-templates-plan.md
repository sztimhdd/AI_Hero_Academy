# Plan: Reading Content Template System

**Status**: READY TO IMPLEMENT
**Branch**: `feature/reading-templates`
**Scope**: `scripts/enrich_reading_content.py` (new) + `utils/content.py` + `pages/04_Course_Module.py`
**Research basis**: Full audit of 21 reading items in `content/reading_content.json` (March 2026) +
UX mockups in `references/ux-mockups/` (4 HTML templates, March 2026) +
Streamlit 1.54.0 native component docs

---

## Architecture Decision

**Why a separate enrichment script, not inline in `generate_course_content.py`:**
- `generate_course_content.py` is already an 8-stage pipeline; adding a 9th stage bloats it
- Enrichment is a one-time post-processing step, not a generation step
- The script can be run independently after adding a new role — no changes to the generator
- Output is a separate `content/reading_content_structured.json` — original JSON stays pristine

**Data flow:**
```
content/reading_content.json  (original, unchanged)
         ↓
scripts/enrich_reading_content.py  (AI extraction)
         ↓
content/reading_content_structured.json  (new; only sub-fields, keyed by course_id)
         ↓
utils/content.py  get_reading_structured(course_id)
         ↓
pages/04_Course_Module.py  template renderers
```

**Fallback strategy:** If `reading_structured` returns `None` for a course, the renderer
falls back to the current flat-text display. New roles work immediately after generation;
enrichment can be run asynchronously.

---

## Content Audit Results (March 2026)

All 21 items (7 courses × 3 roles: RM, UW, AN) follow consistent patterns:

| Field | Pattern | Notes |
|-------|---------|-------|
| `concept_text` | Named acronym framework (CRAF, SAFE, VERIFY, RELATE, SIGNAL, SIFT, STAKE, TRACE) with 4–6 lettered steps | All have a guardrails/constraints section |
| `good_example` | Before/After contrast with fictional company name + prompt text | All use a specific scenario setup |
| `anti_pattern` | Single failure scenario with cascade consequences | All have a clear root lesson |
| `takeaway` | 20–30 words, action-oriented, punchy | Short enough to be the "statement" without extraction |

Extraction reliability: **~95%** — high consistency makes AI extraction low-risk.

---

## Sub-Field Schemas

`content/reading_content_structured.json` is a dict keyed by `course_id`. Each value contains
only the structured sub-fields (original flat-text fields remain in `reading_content.json`).

```json
{
  "rm_course_1": {
    "concept_text_structured": {
      "framework_acronym": "CRAF",
      "intro": "Financial analysis write-ups are high-stakes but repetitive...",
      "cards": [
        {"letter": "C", "title": "Context", "body": "Tells the AI what case it's working on..."},
        {"letter": "R", "title": "Role",    "body": "Assigns a professional identity..."},
        {"letter": "A", "title": "Action",  "body": "Defines the exact deliverable..."},
        {"letter": "F", "title": "Format",  "body": "Controls structure: headings, bullet order..."}
      ],
      "guardrails": [
        "Use only provided data.",
        "Label any missing figures as UNKNOWN.",
        "Do not recommend approval or decline.",
        "Strictly separate facts from interpretation."
      ]
    },
    "good_example_structured": {
      "scenario": "An analyst at Meridian Analytics needs Copilot to identify compliance risks...",
      "before_prompt": "Summarize the compliance risks for ABC Holdings Ltd., registration 8847291...",
      "before_issue": "Contains identifiable private data (name, registration, internal rating).",
      "after_prompt": "What are typical compliance risks for a mid-sized private manufacturing company incorporated in Ontario with a three-tier ownership structure including a foreign holding entity?",
      "after_benefit": "No names, numbers, or internal ratings — safe for Copilot input.",
      "outcome": "Copilot returns a structured compliance checklist the analyst maps back to the real file."
    },
    "anti_pattern_structured": {
      "headline": "The Hallucination Cascade",
      "failure_scenario": "An analyst forwards a Copilot-generated cost-reduction figure directly to the Finance Director without verifying against source data.",
      "chain": [
        "The Finance Director presents the 31% figure (actual: 3.1%) in a board pack.",
        "The decimal error surfaces during audit preparation.",
        "The team must issue a formal correction and the board pack is recalled."
      ],
      "root_lesson": "Never forward AI calculations without independent validation against source data."
    },
    "takeaway_structured": {
      "statement": "Mastering CRAF means any generative AI tool becomes a disciplined drafting assistant — not a free-form writer you have to heavily correct.",
      "action_1": {"title": "Complete the Framework", "body": "Resist the urge to just ask the AI to 'make it sound professional.' A true structured prompt requires all four CRAF elements."},
      "action_2": {"title": "Ground Every Request", "body": "Always paste the source data into the same prompt — do not rely on the AI's training knowledge for client-specific figures."}
    }
  }
}
```

**Schema constraints:**
- `cards`: 4–6 items (one per acronym letter); `letter` is always a single uppercase character
- `guardrails`: array of strings; `[]` if no constraints section in the source text
- `chain`: 2–4 items — the cascade/domino steps from mistake to consequence
- `action_1` / `action_2`: always present; AI generates these from the full item context if not explicit in `takeaway`

---

## Streamlit Rendering Strategy

All renderers operate **inside the existing `_, content_col, _ = st.columns([1, 4, 1])` wrapper**
in `pages/04_Course_Module.py`. Width constraint is already handled.

### Template RT-A: Concept (acronym card grid)

```python
def _render_concept(rs: dict) -> None:
    """Renders concept_text_structured as an acronym card grid."""
    st.caption(rs.get("framework_acronym", ""))
    if rs.get("intro"):
        st.markdown(rs["intro"])

    cards = rs.get("cards", [])
    LETTER_ICONS = ["🔵", "🟣", "🔴", "🟢", "🟡", "🟠"]
    if cards:
        cols = st.columns(2)
        for i, card in enumerate(cards):
            with cols[i % 2]:
                with st.container(border=True):
                    icon = LETTER_ICONS[i % len(LETTER_ICONS)]
                    st.markdown(f"**{icon} {card['letter']} — {card['title']}**")
                    st.markdown(card["body"])

    if rs.get("guardrails"):
        items = "\n".join(f"- {g}" for g in rs["guardrails"])
        st.info(f"**Essential guardrails**\n\n{items}")
```

### Template RT-B: Good Example (before/after comparison)

```python
def _render_good_example(rs: dict) -> None:
    """Renders good_example_structured as a Before/After comparison."""
    if rs.get("scenario"):
        with st.container(border=True):
            st.caption("📋 Scenario")
            st.markdown(rs["scenario"])

    col_b, col_a = st.columns(2)
    with col_b:
        st.caption("❌ Before")
        with st.container(border=True):
            st.code(rs.get("before_prompt", ""), language=None)
            if rs.get("before_issue"):
                st.caption(f"⚠️ {rs['before_issue']}")
    with col_a:
        st.caption("✅ After")
        with st.container(border=True):
            st.code(rs.get("after_prompt", ""), language=None)
            if rs.get("after_benefit"):
                st.caption(f"✓ {rs['after_benefit']}")

    if rs.get("outcome"):
        st.success(rs["outcome"])
```

### Template RT-C: Anti-Pattern (failure + cascade + root lesson)

```python
def _render_anti_pattern(rs: dict) -> None:
    """Renders anti_pattern_structured as an incident report with cascade chain."""
    if rs.get("failure_scenario"):
        with st.container(border=True):
            st.caption("⚠️ What went wrong")
            st.markdown(rs["failure_scenario"])

    chain = rs.get("chain", [])
    if chain:
        st.markdown("**The cascade:**")
        for i, step in enumerate(chain, 1):
            st.markdown(f"{i}. {step}")

    if rs.get("root_lesson"):
        st.error(f"**Root lesson:** {rs['root_lesson']}")
```

### Template RT-D: Takeaway (focal statement + two action cards)

```python
def _render_takeaway(rs: dict) -> None:
    """Renders takeaway_structured as a focal card with two action points."""
    if rs.get("statement"):
        st.markdown(f"### {rs['statement']}")
        st.divider()

    a1 = rs.get("action_1", {})
    a2 = rs.get("action_2", {})
    if a1 or a2:
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown(f"**{a1.get('title', '')}**")
                st.markdown(a1.get("body", ""))
        with col2:
            with st.container(border=True):
                st.markdown(f"**{a2.get('title', '')}**")
                st.markdown(a2.get("body", ""))
```

**Wiring into `04_Course_Module.py`** (replace lines 264–278 inside `with content_col:`):

```python
with content_col:
    if section_idx == 0:
        rs = reading_s.get("concept_text_structured") if reading_s else None
        if rs:
            _render_concept(rs)
        elif reading.get("concept_text"):
            with st.container(border=True):
                st.markdown(reading["concept_text"])

    elif section_idx == 1:
        rs = reading_s.get("good_example_structured") if reading_s else None
        if rs:
            _render_good_example(rs)
        elif reading.get("good_example"):
            st.success(f"**Good example** — {reading['good_example']}")

    elif section_idx == 2:
        rs = reading_s.get("anti_pattern_structured") if reading_s else None
        if rs:
            _render_anti_pattern(rs)
        elif reading.get("anti_pattern"):
            st.warning(f"**Common mistake** — {reading['anti_pattern']}")

    elif section_idx == 3:
        rs = reading_s.get("takeaway_structured") if reading_s else None
        if rs:
            _render_takeaway(rs)
        elif reading.get("takeaway"):
            st.info(f"**Key takeaway** — {reading['takeaway']}")
        # Mark Reading Complete button follows (unchanged)
```

---

## Extraction Prompts

These prompts are embedded in `scripts/enrich_reading_content.py`.

### Prompt for `concept_text_structured`

```
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following concept_text field. The text describes a named
acronym framework (e.g. CRAF, SAFE, VERIFY) used in a professional AI workflow.

<concept_text>
{concept_text}
</concept_text>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{
  "framework_acronym": "<the acronym letters, e.g. CRAF>",
  "intro": "<1-2 sentences introducing the framework and why it matters>",
  "cards": [
    {"letter": "<single uppercase letter>", "title": "<one word>", "body": "<1-2 sentence description>"},
    ...one card per acronym letter...
  ],
  "guardrails": ["<constraint 1>", ...]
}

Rules:
- Extract one card per letter in the acronym, in order
- Preserve the source text closely; do not paraphrase beyond minor cleanup
- guardrails: extract any listed rules/constraints; use [] if none exist
- Return only the JSON object
```

### Prompt for `good_example_structured`

```
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following good_example field. The text describes a
before/after scenario comparing an unsafe AI prompt with a corrected version.

<good_example>
{good_example}
</good_example>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{
  "scenario": "<1 sentence: what task the practitioner is trying to accomplish>",
  "before_prompt": "<the unsafe/incorrect prompt or action, as a direct quote or close paraphrase>",
  "before_issue": "<1 sentence: what specific problem makes this unsafe or incorrect>",
  "after_prompt": "<the safe/correct prompt or action, as a direct quote or close paraphrase>",
  "after_benefit": "<1 sentence: what specific quality makes this version correct>",
  "outcome": "<1 sentence: what the corrected approach produces or achieves>"
}

Rules:
- before_prompt and after_prompt should read as actual prompt text (monospace-renderable)
- Keep before_issue and after_benefit short — they appear as captions under the prompt
- Return only the JSON object
```

### Prompt for `anti_pattern_structured`

```
You are a content structuring assistant for an AI skills learning platform.

Extract structured data from the following anti_pattern field. The text describes a
failure scenario and its consequences.

<anti_pattern>
{anti_pattern}
</anti_pattern>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{
  "headline": "<3-6 word name for this failure pattern>",
  "failure_scenario": "<2-3 sentences: what the practitioner did wrong and the immediate error>",
  "chain": ["<consequence 1>", "<consequence 2>", "<final impact (worst outcome)>"],
  "root_lesson": "<1-2 sentences: the specific rule or check that was skipped>"
}

Rules:
- chain: 2–4 items; each is a single step in the domino effect; final item is the most damaging outcome
- root_lesson must be actionable — what the learner should always do instead
- Return only the JSON object
```

### Prompt for `takeaway_structured`

```
You are a content structuring assistant for an AI skills learning platform.

Given the full reading item below, produce a structured takeaway with two action cards.

<concept_text>
{concept_text}
</concept_text>

<takeaway>
{takeaway}
</takeaway>

Output a single JSON object with exactly this schema — no prose, no markdown fences:
{
  "statement": "<the takeaway sentence — preserve exactly as written>",
  "action_1": {"title": "<3-5 word imperative>", "body": "<1-2 sentence elaboration>"},
  "action_2": {"title": "<3-5 word imperative>", "body": "<1-2 sentence elaboration>"}
}

Rules:
- statement: copy the takeaway text exactly; do not paraphrase
- action_1 and action_2: synthesise two complementary action points from the concept_text
  and takeaway; they should answer "what do I actually do differently on the job?"
- Return only the JSON object
```

---

## Tasks

### RT-1 — Streamlit docs research (pre-work, ≤30 min)

**Before writing any renderer code**, query Context7 for Streamlit 1.54.0 docs:

```
mcp__context7__resolve-library-id("streamlit")
mcp__context7__query-docs: "st.columns nested inside st.container border, st.code in columns, st.metric in container"
```

Confirm:
- `st.code(text, language=None)` renders as a styled monospace block — use this for prompt text
- `st.container(border=True)` accepts nested `st.code()`, `st.caption()`, `st.markdown()` — yes
- `st.columns(2)` inside a `with content_col:` context works correctly — yes

Document any surprises before proceeding.

---

### RT-2 — Build `scripts/enrich_reading_content.py`

**File**: `scripts/enrich_reading_content.py` (new — ~150 lines)

```python
#!/usr/bin/env python3
"""
Enrich content/reading_content.json with structured sub-fields for template rendering.

Reads:  content/reading_content.json
Writes: content/reading_content_structured.json

Run:
    python scripts/enrich_reading_content.py [--dry-run] [--course-id COURSE_ID]

Options:
    --dry-run     Print extracted JSON to stdout, do not write file
    --course-id   Process only one course (for testing)
"""
```

**Implementation sketch:**

```python
import argparse, json, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Reuse same SDK pattern as generate_course_content.py
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

HAIKU_ENDPOINT = os.environ.get("HAIKU_ENDPOINT", "databricks-claude-haiku-4-5")
CONTENT_DIR = Path(__file__).parent.parent / "content"

# (prompts defined as module-level constants — see plan section above)

@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
def _extract(w: WorkspaceClient, prompt: str) -> dict:
    """Call Haiku and return parsed JSON dict."""
    resp = w.serving_endpoints.query(
        name=HAIKU_ENDPOINT,
        messages=[ChatMessage(role=ChatMessageRole.USER, content=prompt)],
        temperature=0.0,
        max_tokens=1024,
    )
    text = resp.choices[0].message.content.strip()
    # Strip possible markdown fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)

def enrich_item(w: WorkspaceClient, course_id: str, item: dict) -> tuple[str, dict]:
    """Extract all 4 structured sub-fields for one reading item."""
    structured = {}
    # Extract each section; log and skip on failure (graceful degradation)
    for field, prompt_fn in [
        ("concept_text_structured",  lambda: CONCEPT_PROMPT.format(**item)),
        ("good_example_structured",  lambda: GOOD_EXAMPLE_PROMPT.format(**item)),
        ("anti_pattern_structured",  lambda: ANTI_PATTERN_PROMPT.format(**item)),
        ("takeaway_structured",      lambda: TAKEAWAY_PROMPT.format(**item)),
    ]:
        try:
            structured[field] = _extract(w, prompt_fn())
        except Exception as e:
            print(f"  WARN [{course_id}] {field}: {e}")
    return course_id, structured

def main():
    # ... argument parsing, load JSON, call enrich_item concurrently, write output
```

**Key design decisions:**
- Use **Haiku** (not Sonnet) — extraction is mechanical; Haiku handles JSON extraction reliably and is 5x cheaper
- Run all 4 field extractions for each item **sequentially** (not parallel) to avoid rate limits; items themselves can be processed **concurrently** (up to 4 workers)
- `--dry-run` prints JSON to stdout without writing — use for spot-checking
- `--course-id` processes a single course — use for testing one item before running all 21

---

### RT-3 — Update `utils/content.py`

Add a new getter alongside existing `get_reading_content()`:

```python
_READING_STRUCTURED: dict | None = None

def get_reading_structured(course_id: str) -> dict | None:
    """
    Returns the structured sub-fields dict for a course's reading content, or None
    if reading_content_structured.json has not been generated yet.
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

Note: use the same `_CONTENT_DIR` path constant already defined in `content.py`.

---

### RT-4 — Add template renderers to `pages/04_Course_Module.py`

1. At the top of the reading section (after `reading = get_reading_content(course_id)`), add:
   ```python
   reading_s = get_reading_structured(course_id)
   ```

2. Add the 4 renderer functions (`_render_concept`, `_render_good_example`,
   `_render_anti_pattern`, `_render_takeaway`) as module-level functions, before the
   `elif active_sub == "reading":` block.

3. Replace lines 264–278 (the `with content_col:` block) with the wiring code from the
   "Streamlit Rendering Strategy" section above.

4. The "Mark Reading Complete →" button and surrounding `st.divider()` remain untouched
   inside `section_idx == 3`.

---

### RT-5 — Run enrichment + spot-check

```bash
# 1. Test one item first
python scripts/enrich_reading_content.py --dry-run --course-id rm_course_1

# 2. If output looks good, run all 21 items
python scripts/enrich_reading_content.py

# 3. Verify the output file
python -c "import json; d=json.load(open('content/reading_content_structured.json')); print(len(d), 'courses enriched'); [print(k) for k in d]"
```

**Spot-check at least 3 items** (one per role) for:
- `concept_text_structured.cards` length matches acronym letter count
- `good_example_structured.before_prompt` and `after_prompt` are prompt-like text (not summaries)
- `anti_pattern_structured.chain` has 2–4 items
- `takeaway_structured.statement` matches original `takeaway` field exactly (no paraphrase)

Fix any malformed items manually or by re-running with `--course-id`.

---

### RT-6 — Visual verification with Playwright

After implementing renderers and running the local server:

```bash
bash run_uat.sh
```

Navigate to Module 1 → Reading → each of the 4 sections. Capture screenshots and verify:
- Concept: 2×N card grid visible; colored emoji letter badges; guardrails in `st.info()`
- Good Example: scenario card + Before/After columns; code blocks render monospace; `st.success()` outcome
- Anti-Pattern: failure scenario card; numbered cascade list; `st.error()` root lesson
- Takeaway: large `###` statement; 2-column action cards; "Mark Reading Complete →" below

---

## Implementation Order

```
RT-1  Streamlit docs research            ← prerequisite; do before any renderer code
RT-2  Build enrich_reading_content.py   ← independent; can start while RT-1 runs
RT-3  Add get_reading_structured()       ← 10-line change to utils/content.py
RT-5  Run enrichment (21 items)          ← requires RT-2 complete
RT-4  Add renderers + wiring             ← requires RT-3 and RT-5 (data needed to test)
RT-6  Visual verification (Playwright)   ← requires RT-4 complete + local server running
```

---

## Files Modified

| File | Change |
|------|--------|
| `scripts/enrich_reading_content.py` | **New** — AI extraction script |
| `content/reading_content_structured.json` | **New** — generated by the script |
| `utils/content.py` | Add `get_reading_structured()` getter |
| `pages/04_Course_Module.py` | Add 4 renderer functions; update reading `with content_col:` block |

**Not modified**: `content/reading_content.json`, `utils/styles.py`, any other page.

---

## Acceptance Checklist

- [ ] `python scripts/enrich_reading_content.py` completes without errors for all 21 items
- [ ] `content/reading_content_structured.json` contains exactly 21 keys (one per course_id)
- [ ] Concept section: 2×N card grid renders; each card has a colored emoji + letter + title + body
- [ ] Concept section: guardrails appear in an `st.info()` block below the card grid
- [ ] Good Example section: scenario card renders above Before/After columns
- [ ] Good Example section: Before column shows red-bordered container with `st.code()` block
- [ ] Good Example section: After column shows green-bordered container with `st.code()` block
- [ ] Good Example section: outcome renders as `st.success()`
- [ ] Anti-Pattern section: failure scenario in `st.container(border=True)` with "What went wrong" caption
- [ ] Anti-Pattern section: numbered cascade list renders correctly
- [ ] Anti-Pattern section: root lesson renders as `st.error()`
- [ ] Takeaway section: `###` statement renders as large text above action cards
- [ ] Takeaway section: 2-column action card grid renders; "Mark Reading Complete →" button follows
- [ ] Fallback: if `reading_content_structured.json` is deleted, flat-text rendering restores — no errors
- [ ] No `unsafe_allow_html=True` added anywhere in the renderer functions
- [ ] `bash run_uat.sh` passes all UAT scenarios; no regressions on other sub-views

---

## Out of Scope

- Modifying `content/reading_content.json` — source content stays untouched
- Modifying `generate_course_content.py` — enrichment is a separate post-processing step
- Adding structured templates to `evaluation_items.json` or `practice_scenarios.json`
- Animated card transitions (CSS-only; fragile across Streamlit versions)
- Colored card borders per letter (no color prop on `st.container(border=True)`)
- Online enrichment at app startup (enrichment is offline, committed to the repo)
