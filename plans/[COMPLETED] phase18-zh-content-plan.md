# Phase 18 — Chinese Coursework & Content Localization

> Status: **COMPLETE** — 2026-03-24 | 41/41 baseline UAT checks pass (100%)
> Last updated: 2026-03-24

---

## Context & What's Already Done

**Phase 17 (i18n infrastructure) is complete:**
- `utils/i18n.py` with `t(key, lang)` + browser detection + `SUPPORTED_LANGS`
- `content/i18n/en.json` and `content/i18n/zh.json` — 140 UI string keys
- Sidebar language toggle → Firestore persist → `_lang_from_profile` sentinel
- `st.session_state["lang"]` drives all UI string rendering across 5 pages

**Session 1 complete (March 2026):**
- `utils/content.py` — `_load_lang()` helper + `lang` param on all 9 user-content getters
- `utils/ai.py` — `_lang_instruction(lang)` helper; `generate_gap_map`, `coach_response`,
  `generate_module_coach_note` all accept `lang` and append Chinese instruction when `lang="zh"`
- All 5 pages updated to pass `lang=_lang` to every content getter and AI call
- `scripts/translate_content.py` — translation pipeline scaffold (single-pass, awaiting upgrade)

**What Session 1 did NOT do:**
- `content/i18n/zh.json` still has `[ZH]` placeholder suffixes — not real Chinese
- `content/zh/` directory does not exist yet — no translated content files
- Translation pipeline not yet upgraded to reflection workflow

---

## What Phase 18 Builds

A fully bilingual app where switching to 中文 delivers:
1. Real Chinese UI strings (not `[ZH]` placeholders)
2. Chinese course titles, descriptions, reading articles, practice scenarios, quiz questions
3. AI coach responding in Simplified Chinese when lang = "zh"
4. Gap map and scoring written in Chinese

**Target Chinese:** Simplified Chinese (简体中文) — professional financial services register.
**Framework acronyms (SAFE, CRAF, VERIFY, TRACE, STAKE)** are kept in English with a
Chinese explanation on first use — this is standard practice in Chinese corporate training.

---

## Content Scope

| File | Entries | Size | Fields to translate |
|------|---------|------|---------------------|
| `roles.json` | 4 | 2.2 KB | `title`, `description` |
| `domains.json` | 24 | 49.3 KB | `name`, `description`, level descriptors |
| `courses.json` | 35 | 29.7 KB | `title`, `tagline`, `description`, `real_use_case` |
| `diagnostic_items.json` | 54 | 75.3 KB | `question_text`, `scenario_text`, MCQ `options[].text`, rubric criterion `name`/`description` |
| `reading_content.json` | 35 | 124.0 KB | `concept_text`, `good_example`, `anti_pattern`, `takeaway` |
| `practice_scenarios.json` | 35 | 221.4 KB | `scenario_text`, `task_N_text`, `coach_system_prompt`, MCQ option labels |
| `evaluation_items.json` | 35 | 174.1 KB | `scenario_text`, `question_text`, MCQ option labels, rubric criterion `name`/`description` |
| `content/i18n/zh.json` | 140 | tiny | All 140 UI string values (replace `[ZH]` stubs) |

**Total: ~675 KB English → Simplified Chinese**

**Do NOT translate:** IDs, booleans, numeric weights, `correct_option` letters,
`scoring_rubric.correct/incorrect` integers, `task_modes`, timestamps.

---

## Architecture: Parallel `content/zh/` Directory

```
content/
  courses.json                ← EN (unchanged)
  reading_content.json        ← EN (unchanged)
  ...
  zh/
    courses.json              ← ZH translations (Phase 18)
    reading_content.json      ← ZH translations (Phase 18)
    practice_scenarios.json
    evaluation_items.json
    diagnostic_items.json
    roles.json
    domains.json
  i18n/
    en.json                   ← UI strings EN (done)
    zh.json                   ← UI strings ZH — real values (Phase 18)
```

**Fallback chain in `utils/content.py`:** ZH file → EN file → KeyError (unchanged behaviour).

---

## Translation Strategy (Research-Informed)

### Model: `databricks-claude-sonnet-4-6` (OAuth, no setup)

Research benchmark (COMET scores, EN→ZH):
- Claude Sonnet: **0.809** — best accuracy + JSON structure fidelity
- Gemini 1.5 Pro: 0.783 — good coverage, less consistent on professional register
- Claude wins specifically on "idiomatic expressions and technical terminology localization"

Gemini (via personal API key) is not used — OAuth is already wired, Claude scores higher
for this domain, and Databricks endpoint has no incremental cost.

### Workflow: Andrew Ng Reflection Workflow (3-step)

Single-pass translation produces robotic output. The reflection workflow measurably
improves naturalness by making the model critique and revise its own output:

```
Step 1 — TRANSLATE  (temp=0.3)
  Initial pass — warmer temperature gives more natural first-draft phrasing

Step 2 — REFLECT    (temp=0.1)
  Critique the translation for: accuracy, fluency, register, idiom, consistency
  Target: "style and tone should match professional Mainland Chinese business readers"

Step 3 — IMPROVE    (temp=0.2)
  Apply the critique — produce final translation
  Constraint: same JSON structure, same fields, no new keys
```

3× API calls per batch. Total ~120–150 calls for all 8 files. ~10–15 min end-to-end.

### RAG Style Reference: `references/zh-translation-reference.md`

A ~8,900-token curated Chinese AI training reference document injected into the
system prompt of every translation call. Compiled from:

| Source | Stars | Content |
|--------|-------|---------|
| `phodal/prompt-patterns` README | 3,089 ★ | Prompt设计模式 — natural Chinese AI vocabulary |
| `datawhalechina/llm-cookbook` 高级提示方法 | 23,598 ★ | Dense professional Chinese AI prose (CoT, ReAct, etc.) |
| `phodal/prompt-patterns` 设计模式类比 | 3,089 ★ | How Chinese authors explain abstract AI concepts |

**Injection point:** System prompt prefix in all 3 steps of the reflection chain.

### Domain Glossary (hardcoded in script)

Approved term pairs enforced in every translation call:

| English | Chinese |
|---------|---------|
| gap map | 差距图谱 |
| skills profile | 技能档案 |
| diagnostic | 技能测评 |
| AI coach | AI辅导员 |
| learning path | 学习路径 |
| prompt sandbox | 提示词沙盒 |
| evaluation | 综合评估 |
| course module | 学习模块 |
| domain score | 领域得分 |
| champion (level) | 卓越级 |
| proficient | 精通级 |
| practitioner | 实践级 |
| explorer | 探索级 |
| unaware | 认知前级 |

### Anti-Robotic Instructions (injected into all prompts)

```
- Avoid literal word-for-word translation.
- Use sentence structures natural to Mainland Chinese business readers.
- Prefer concise expressions — Chinese business writing is more compact than English.
- Use active voice where natural in Chinese.
- {placeholder} variables must be preserved exactly as-is.
```

### Temperature Settings

| Step | Temp | Rationale |
|------|------|-----------|
| Initial translate | 0.3 | Slightly warm → more natural first draft |
| Reflect/critique | 0.1 | Precise, analytical — catch real errors |
| Improve/final | 0.2 | Controlled refinement of the critique |

---

## Implementation Tasks

### 18.1 — Language-Aware Content Loaders ✅ COMPLETE

`utils/content.py`:
- `_load_lang(filename, lang)` helper with EN fallback
- `lang: str = "en"` param on all 9 getters: `get_role`, `get_domain`,
  `get_domain_descriptions`, `get_diagnostic_items`, `get_course`, `get_reading`,
  `get_scenario`, `get_courses`, `get_eval_items`

### 18.2 — Page Updates ✅ COMPLETE

All 5 pages pass `lang=_lang` to every content getter and AI call:
- `pages/01_Diagnostic.py` ✅
- `pages/02_Skills_Profile.py` ✅
- `pages/03_Home.py` ✅ (lang resolution moved before `get_course` call)
- `pages/04_Course_Module.py` ✅ (all 8 call sites updated)
- `app.py` — no content getter calls, no changes needed ✅

### 18.3 — AI Calls in Chinese ✅ COMPLETE

`utils/ai.py`:
- `_LANG_INSTRUCTION` dict + `_lang_instruction(lang)` helper
- `generate_gap_map(lang="en")` ✅
- `coach_response(lang="en")` ✅
- `generate_module_coach_note(lang="en")` ✅
- Scoring functions (`score_diagnostic`, `score_evaluation`) — rubric stays EN, scores are numeric, no lang param needed ✅

### 18.4 — Translation Pipeline Upgrade (`scripts/translate_content.py`)

**Current state:** Single-pass scaffold exists, writes to `content/zh/`.

**Upgrade required:**

1. **Load reference doc** at startup:
   ```python
   REF_DOC = (CONTENT_DIR.parent / "references" / "zh-translation-reference.md").read_text(encoding="utf-8")
   ```

2. **Load glossary** as a formatted string injected into every prompt.

3. **Replace `_translate_batch()` with `_translate_reflect_improve()`:**
   ```python
   def _translate_reflect_improve(w, batch, fields, task_desc):
       # Step 1: translate
       t1 = _call(w, _build_translate_prompt(batch, fields, task_desc), temp=0.3)
       # Step 2: reflect
       critique = _call(w, _build_reflect_prompt(batch, t1), temp=0.1)
       # Step 3: improve
       final = _call(w, _build_improve_prompt(batch, t1, critique), temp=0.2)
       return json.loads(_strip_fences(final))
   ```

4. **System prompt template** (all 3 steps):
   ```
   You are a professional Simplified Chinese (简体中文) translator for corporate AI
   training materials in financial services.

   Style reference — match the tone, register, and terminology of these Chinese AI
   training materials:
   <reference>
   {REF_DOC[:6000]}   ← trimmed to ~2K tokens, most relevant sections
   </reference>

   Approved glossary (always use these terms, no variation):
   <glossary>
   {GLOSSARY}
   </glossary>

   Translation rules:
   1. Translate ONLY user-visible text fields specified in the task.
   2. Keep ALL JSON keys, IDs, booleans, numbers, scoring weights in English as-is.
   3. Framework acronyms (SAFE, CRAF, VERIFY, TRACE, STAKE): keep in English; add
      Chinese meaning in parentheses on first use within a document.
   4. Fictional company names (Meridian, Aurora, Crestwood, Apex, etc.): keep in English.
   5. {placeholder} variables: preserve exactly as-is.
   6. Avoid literal word-for-word translation. Use natural Mainland Chinese business register.
   7. Return only valid JSON — no markdown fences, no explanation text.
   ```

5. **Reflect prompt:**
   ```
   Source (English):
   <source>{batch_json}</source>

   Initial translation (Chinese):
   <translation>{t1}</translation>

   You are a senior Chinese editor reviewing this translation for a corporate AI training
   platform targeting Mainland Chinese financial services professionals.

   Evaluate the translation on:
   - Accuracy: does it faithfully convey the English meaning?
   - Fluency: does it read naturally to a native Mainland Chinese reader?
   - Register: is it appropriately formal (business training, not casual)?
   - Terminology: are the glossary terms used correctly and consistently?
   - Idioms: are any English idioms translated too literally?

   Provide specific, actionable suggestions only. Reference specific phrases that need
   improvement. Be concise.
   ```

6. **Improve prompt:**
   ```
   Source (English):
   <source>{batch_json}</source>

   Initial translation:
   <translation>{t1}</translation>

   Editor suggestions:
   <suggestions>{critique}</suggestions>

   Apply the suggestions to produce the final improved translation.
   Rules:
   - Same JSON structure as the input — same keys, same entry count.
   - Only edit the text fields; keep all IDs, numbers, booleans unchanged.
   - If a suggestion conflicts with the glossary or rules, keep the glossary term.
   - Return only valid JSON — no markdown fences, no explanation.
   ```

### 18.5 — UI String Translations

Replace all `[ZH]` placeholders in `content/i18n/zh.json` with real Chinese.
Handled by the translation pipeline (file `i18n`).

Key principles:
- Keep labels short (Chinese UI labels can be shorter than English)
- `"Start My Diagnostic →"` → `"开始技能测评 →"`
- `"Module {n} of 7"` → `"第 {n} 模块，共 7 个"`
- Maintain all `{placeholder}` variables exactly

### 18.6 — Verification

1. `bash run_uat.sh` with `python scripts/reset_uat_user.py --role rm`
2. Switch language to 中文 via sidebar
3. Navigate all 5 pages — confirm Chinese UI strings
4. Complete diagnostic flow — confirm Chinese questions
5. Navigate to Course Module — confirm Chinese reading content
6. Start Practice — confirm coach responds in Chinese
7. Complete quiz — confirm Chinese questions + coach note in Chinese
8. Playwright screenshots of key pages in zh mode

---

## File Processing Order & Batch Sizes

| Order | File | Entries | Batch | API calls (×3) | Notes |
|-------|------|---------|-------|----------------|-------|
| 1 | `roles.json` | 4 | all 4 | 3 | Quickest — good smoke test |
| 2 | `domains.json` | 24 | 6 | 12 | Level descriptors are verbose |
| 3 | `courses.json` | 35 | 5 | 21 | |
| 4 | `i18n/zh.json` | 140 | all | 3 | Single call — UI strings |
| 5 | `diagnostic_items.json` | 54 | 5 | 33 | List structure (not dict) |
| 6 | `reading_content.json` | 35 | 3 | 36 | Longest per-entry content |
| 7 | `evaluation_items.json` | 35 | 3 | 36 | |
| 8 | `practice_scenarios.json` | 35 | 2 | 54 | Largest — coach prompts |

**Total: ~198 API calls, ~10–15 min end-to-end**

---

## Acceptance Criteria

- [ ] All 140 `content/i18n/zh.json` values are real Chinese (no `[ZH]` suffix)
- [ ] `content/zh/` has 7 translated files
- [ ] Glossary terms are consistent across all files
- [ ] Switching to 中文 in sidebar → all visible content is Chinese
- [ ] Spot-check: reading content flows naturally (not word-for-word literal)
- [ ] AI coach responds in Simplified Chinese when lang = zh
- [ ] Gap map bullets are in Chinese when lang = zh
- [ ] Scoring still works correctly (Chinese responses → English rubric → numeric score)
- [ ] English mode is completely unaffected (regression free)
- [ ] Playwright screenshots confirm visual correctness in zh mode

---

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Reflect step changes JSON structure | Low | Improve prompt: "same JSON structure, same keys" |
| Glossary terms inconsistently applied | Low | Glossary in all 3 prompt steps |
| `practice_scenarios` coach_system_prompt truncated (8K output cap) | Medium | Batch size = 2; detect truncation by JSON parse failure → retry batch size 1 |
| `diagnostic_items.json` is a list — index mapping may miss entries | Low | `id_to_idx` dict used; count assertion after each file |
| Reflection adds latency on large files | Medium | Run files sequentially; `--file` flag allows resuming |

---

## Execution Order

```
Session 1: 18.1 + 18.2 + 18.3   ✅ COMPLETE (March 2026) — UAT in progress
Session 2: 18.4 upgrade + run    → upgrade script to reflection workflow, then run all 8 files
Session 3: 18.5 + 18.6           → polish UI strings (if needed) + Playwright verification
```

Sessions 2 and 3 are independent of Session 1 UAT — can run in parallel.
