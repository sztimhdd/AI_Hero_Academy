# Phase 18 Kickstarter — Chinese Coursework & Content Localization

> Paste this entire prompt into a new Claude Code session to implement Phase 18.

---

## Mission

Implement full Simplified Chinese (简体中文) content localization for AI Hero Academy.
The i18n UI infrastructure (Phase 17) is already live — `lang` session state, sidebar toggle,
Firestore persistence, `t(key, lang)` translations for UI strings. Phase 18 adds:

1. **Language-aware content loaders** — `utils/content.py` getters accept `lang` param
2. **Chinese AI responses** — coach, gap map, scoring respond in Chinese when `lang="zh"`
3. **Translation pipeline** — `scripts/translate_content.py` populates `content/zh/`
4. **Real UI string translations** — replace all 140 `[ZH]` placeholders in `content/i18n/zh.json`

The app serves 4 roles (RM, UW, AN, MK) with 7 modules each (35 total courses) across
5 Streamlit pages. After Phase 18, switching the sidebar to 中文 delivers the full
training experience in Simplified Chinese.

---

## Key Files to Read First

Before writing any code, read these files to understand the current state:

1. `utils/content.py` — current getters (no lang param yet)
2. `utils/i18n.py` — the `t(key, lang)` pattern and SUPPORTED_LANGS
3. `content/i18n/zh.json` — 140 UI keys, all with `[ZH]` placeholders
4. `utils/ai.py` (or wherever gap map/scoring/coach calls live) — find system prompt patterns
5. `pages/04_Course_Module.py` — the page with most content getter calls
6. `plans/phase18-zh-content-plan.md` — the full plan (already written)

---

## Step 1 — Language-Aware Content Loaders (`utils/content.py`)

**Read the file first.**

Add `_load_lang(filename, lang)` helper just after the existing `_load()` function:

```python
def _load_lang(filename: str, lang: str = "en") -> dict | list:
    """Load lang-specific content file; falls back to English if not available."""
    if lang != "en":
        p = _CONTENT_DIR / lang / filename
        if p.exists():
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    return _load(filename)
```

Then add `lang: str = "en"` to these getters (use `_load_lang` instead of the module-level cache):

| Getter | File it loads |
|--------|---------------|
| `get_role(role_id, lang="en")` | `roles.json` |
| `get_domain(domain_id, role_id, lang="en")` | `domains.json` |
| `get_domain_descriptions(role_id, lang="en")` | `domains.json` |
| `get_diagnostic_items(role_id, lang="en")` | `diagnostic_items.json` |
| `get_course(course_id, lang="en")` | `courses.json` |
| `get_reading(course_id, lang="en")` | `reading_content.json` |
| `get_scenario(course_id, lang="en")` | `practice_scenarios.json` |
| `get_courses(role_id, lang="en")` | `courses.json` |
| `get_eval_items(course_id, lang="en")` | `evaluation_items.json` |

**Important:** The module-level caches (`ROLES`, `DOMAINS`, `COURSES`, etc.) at the top are
fine to keep for backward compatibility — they always load EN and are used by existing callers
that don't pass `lang`. The new lang-aware getters call `_load_lang` directly (no cache needed
for ZH — it's loaded fresh per call, acceptable for a low-RPS app).

---

## Step 2 — Update Pages to Pass `lang`

**Pattern:** Near the top of each page guard block, capture lang:

```python
lang = st.session_state.get("lang", "en")
```

Then pass it to every `content.*` call that returns user-visible text.

**Pages to update:**

### `pages/01_Diagnostic.py`
- `content.get_diagnostic_items(role_id)` → `content.get_diagnostic_items(role_id, lang=lang)`

### `pages/02_Skills_Profile.py`
- Any `content.get_domain(...)` calls → add `lang=lang`
- Any `content.get_domain_descriptions(...)` → add `lang=lang`

### `pages/03_Home.py`
- `content.get_courses(role_id)` → `content.get_courses(role_id, lang=lang)`
- Any `content.get_course(course_id)` → add `lang=lang`

### `pages/04_Course_Module.py`
- `content.get_course(course_id)` → add `lang=lang`
- `content.get_reading(course_id)` → add `lang=lang`
- `content.get_scenario(course_id)` → add `lang=lang`
- `content.get_eval_items(course_id)` → add `lang=lang`

### `app.py`
- Check if `get_role(...)` is called for display — if so, add `lang=lang`

---

## Step 3 — Chinese AI Responses

**Read `utils/ai.py` (or wherever AI calls live) first.**

Find the four AI call functions: `score_diagnostic`, `generate_gap_map`, `coach_response`,
`score_evaluation`. Each builds a system prompt string.

Add this helper:

```python
_LANG_INSTRUCTION = {
    "zh": (
        "\n\nIMPORTANT: All your responses MUST be written entirely in Simplified Chinese "
        "(简体中文). Do not use English except for: framework acronyms (SAFE, CRAF, VERIFY, "
        "TRACE, STAKE), fictional company names (Meridian, Aurora, Crestwood, etc.), "
        "and JSON field names. Maintain a professional financial services tone."
    )
}

def _lang_instruction(lang: str) -> str:
    return _LANG_INSTRUCTION.get(lang, "")
```

Then append `_lang_instruction(lang)` to the system prompt of each AI call. Thread `lang`
param through from the pages where these functions are called.

**Scoring in Chinese:** The rubric stays in English internally — Claude/Gemini can score
Chinese-language responses against English-language rubrics without issue. Only the
*output* (coach note, gap map bullets) needs to be in Chinese.

---

## Step 4 — Translation Pipeline (`scripts/translate_content.py`)

Build a batch translation script. Use the **existing WorkspaceClient pattern** from
`scripts/enrich_reading_content.py` or `scripts/atomize_coursework.py` — same SDK auth,
same retry logic, same ThreadPoolExecutor pattern.

**Serving endpoint:** `databricks-claude-sonnet-4-6` (quality matters for professional content)
**Temperature:** 0.1

### CLI interface

```bash
python scripts/translate_content.py              # translate all files
python scripts/translate_content.py --file courses      # single file
python scripts/translate_content.py --dry-run           # print to stdout
python scripts/translate_content.py --role rm           # filter to rm role only
```

### Translation system prompt

```
You are a professional Simplified Chinese (简体中文) translator for corporate AI training
materials in financial services.

Translation rules:
1. Translate ONLY the user-visible text fields specified in the task. Return valid JSON.
2. Keep ALL JSON keys, IDs, booleans, numbers, scoring weights in English as-is.
3. Framework acronyms (SAFE, CRAF, VERIFY, TRACE, STAKE): keep in English;
   on first use within a document add Chinese meaning in parentheses,
   e.g. "SAFE抽象法（敏感数据处理框架）".
4. Fictional company names (Meridian, Aurora, Crestwood, Apex, etc.): keep in English.
5. {placeholder} variables (e.g. {role}, {n}, {name}): keep exactly as-is.
6. Professional financial services register. Formal 您-form where appropriate.
7. Return only valid JSON — no markdown code fences, no explanation text.
```

### Files to translate (in order)

| Order | File | Batch size | Fields to translate |
|-------|------|------------|---------------------|
| 1 | `roles.json` | all 4 at once | `title`, `description` |
| 2 | `domains.json` | 6 per batch | `name`, `description`, all level descriptor values |
| 3 | `courses.json` | 5 per batch | `title`, `tagline`, `description`, `real_use_case` |
| 4 | `content/i18n/zh.json` | all 140 at once | all values (strip the `[ZH]` suffix first, then translate) |
| 5 | `diagnostic_items.json` | 5 per batch | `question_text`, `scenario_text`, `options[].text`, rubric `criteria[].name`, `criteria[].description` |
| 6 | `reading_content.json` | 3 per batch | `concept_text`, `good_example`, `anti_pattern`, `takeaway` |
| 7 | `evaluation_items.json` | 3 per batch | `scenario_text`, `question_text`, `options[].label`, rubric `criteria[].name`, `criteria[].description` |
| 8 | `practice_scenarios.json` | 2 per batch | `scenario_text`, `task_1_text`…`task_4_text`, `coach_system_prompt`, MCQ `task_mcq_options[].label` |

### Output

Write each translated file to `content/zh/{filename}`. Create the `content/zh/` directory
if it doesn't exist. Each file should be valid JSON with the same top-level structure as
the English original.

For `content/i18n/zh.json`, overwrite the existing file in place (not in a `zh/` subdirectory
— it's already at `content/i18n/zh.json`).

### Validation after each file

After writing each file:
```python
with open(out_path, encoding="utf-8") as f:
    parsed = json.load(f)
assert len(parsed) == len(original)   # same number of entries
print(f"  ✓ {filename}: {len(parsed)} entries written")
```

---

## Step 5 — Run the Translation Pipeline

From the VS Code terminal (auth handled by VS Code extension):

```bash
# Test with a small file first
python scripts/translate_content.py --file roles --dry-run
python scripts/translate_content.py --file roles

# Then progressively larger files
python scripts/translate_content.py --file domains
python scripts/translate_content.py --file courses
python scripts/translate_content.py --file i18n
python scripts/translate_content.py --file diagnostic_items
python scripts/translate_content.py --file reading_content
python scripts/translate_content.py --file evaluation_items
python scripts/translate_content.py --file practice_scenarios
```

Check `content/zh/` after each run:
```bash
ls content/zh/
python -c "import json; d=json.load(open('content/zh/courses.json')); print(list(d.values())[0]['title'])"
```

---

## Step 6 — Verification

Reset UAT user and run the app:

```bash
python scripts/reset_uat_user.py --role rm
bash run_uat.sh
```

Then use the Playwright MCP tools (`mcp__playwright__browser_*`) to:

1. Navigate to `http://localhost:8501`
2. Screenshot the Welcome page (English)
3. Switch sidebar language to 中文
4. Screenshot every page in zh mode:
   - Welcome page
   - Diagnostic (question text should be Chinese)
   - Skills Profile
   - Home (course titles should be Chinese)
   - Course Module reading view
   - Course Module practice (send a message, confirm coach replies in Chinese)
   - Course Module quiz (questions in Chinese)
   - Results page
5. Confirm no `[ZH]` or English fragments visible in zh mode
6. Switch back to English and confirm no regression

---

## Acceptance Criteria

- [ ] `content/zh/` contains 7 JSON files (roles, domains, courses, diagnostic_items,
      reading_content, practice_scenarios, evaluation_items)
- [ ] `content/i18n/zh.json` has real Chinese values (no `[ZH]` suffixes)
- [ ] Switching sidebar to 中文 → all visible text is Chinese
- [ ] AI coach responds in Simplified Chinese when lang = zh
- [ ] Gap map bullets are in Chinese when lang = zh
- [ ] English mode is completely unaffected (no regression)
- [ ] Playwright screenshots confirm visual correctness in zh mode

---

## What NOT to Do

- Do not translate: `course_id`, `role_id`, `domain_id`, `item_id`, `correct_option`,
  `scoring_rubric.correct/incorrect`, `task_modes`, timestamps, JSON keys
- Do not modify `content/atomic_modules*.json` or any atomic pipeline files
- Do not change the `SUPPORTED_LANGS` dict or add a new language — zh is already declared
- Do not `pip install` anything — all dependencies are in `.venv`
- Do not call MCP tools from sub-agents — call them directly in the main session

---

## Implementation Session Order

**Session 1 (infrastructure):** Steps 1 + 2 + 3 (no translation yet — just wiring)
**Session 2 (content):** Steps 4 + 5 (run the pipeline, populate content/zh/)
**Session 3 (verification):** Step 6 (Playwright UAT in zh mode)

After Session 1 completes, the app runs correctly in English (regression-free) and is
wired to serve Chinese content once `content/zh/` is populated.
