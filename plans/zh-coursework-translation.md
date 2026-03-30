# ZH Coursework Translation Plan
**Scope:** B2C pillar content P1–P6 (reading / practice / quiz / build artifact)
**Status:** ⬜ Not started
**Priority:** Required before public launch — roadmap §0 states "bilingual EN + ZH at all times"

---

## 1. What Needs Translating

### In-scope: all user-facing text in `content/pillars/p*.json`

| Field path | Example | Notes |
|------------|---------|-------|
| `pillar_name` | "AI Conceptual Foundation" | Translate |
| `coaching_vocabulary.{letter}` | "M: Model behavior — How LLMs actually work" | Translate description; keep letter key |
| `reading.concept_text` | Long-form educational prose | Translate + culturally adapt |
| `reading.good_example` | Story with named character | Translate; consider localizing persona names |
| `reading.anti_pattern` | Cautionary scenario | Translate; replace Western-specific references (see §4) |
| `reading.takeaway` | 2–3 sentence summary | Translate |
| `practice.scenario_template` | Template string with `{params}` | Translate; preserve all `{param}` slots verbatim |
| `practice.tasks[].title` | "Hallucination Hunt" | Translate |
| `practice.tasks[].learning_objective` | Assessment goal | Translate |
| `practice.tasks[].prompt_template` | Task prompt with `{params}` | Translate; preserve `{params}` |
| `practice.tasks[].rubric.{0-4}` | Scoring criteria per level | Translate; preserve scoring intent |
| `quiz.items[].question` | MCQ question text | Translate |
| `quiz.items[].options.{A-D}` | Answer options | Translate |
| `quiz.items[].explanation` | Post-answer explanation | Translate |
| `build_artifact.artifact_name` | "My Personal AI Tool Selection Checklist" | Translate |
| `build_artifact.artifact_description` | Description shown to learner | Translate |
| `build_artifact.prompt` | Artifact creation prompt with `{params}` | Translate; preserve `{params}` |
| `build_artifact.coach_closing_prompt` | Coach instruction (not shown to learner) | Translate |

### Out-of-scope: identifiers and metadata — do NOT translate

- `pillar_id`, `pillar_slug`, `day_number`, `estimated_minutes`, `perishable_content`, `last_updated`
- `framework` acronym values: MAPS, CRAF, CAST, BRIEF, CREW
- `task_id`, `item_id`, `type`, `correct_answer`, `score_weight`
- All `{declared_role}`, `{declared_industry}`, `{daily_work_desc}`, `{day_number}` template params

### AI/tech terms: preserve in English (per `_LANG_INSTRUCTION`)

The following must appear in their English form even in Chinese text:

```
LLM、GPT、Claude、Gemini、ChatGPT、RAG、CoT、JSON、API、MCP、
system prompt、temperature、Cursor、n8n、GitHub Copilot
```

---

## 2. Output Format

Parallel files under `content/zh/pillars/` — same directory pattern as legacy `content/zh/`:

```
content/
  pillars/            ← EN (existing, unchanged)
    p1_foundation.json
    p2_prompting.json
    ...
  zh/
    pillars/          ← NEW: ZH translations
      p1_foundation.json
      p2_prompting.json
      p3_tool_fluency.json
      p4_configuration.json
      p5_workflow.json
      p6_agentic.json
      capstone.json
```

Each ZH file is a **full copy** of the EN schema with translated values. The JSON structure and all keys are identical — only the string values change (except preserved identifiers and params listed above).

---

## 3. Cultural Adaptation Requirements

**These are NOT literal translation jobs — the content must feel native to a Chinese professional audience.**

### 3.1 Names and personas
- Replace Western names in stories (Nadia, Marcus) with plausible Chinese names (e.g., 雯静, 志强)
- Generic professional titles stay role-neutral (same as EN)

### 3.2 Examples requiring adaptation

| EN reference | Issue | ZH approach |
|-------------|-------|-------------|
| *Mata v. Avianca* (P1 anti-pattern: lawyer submits AI-hallucinated case citations to US federal court) | No Chinese recognition, foreign legal system | Replace with a documented ZH parallel: e.g., a Chinese lawyer citing non-existent cases in a contract dispute, or keep the case with a one-line gloss |
| US/Western companies used as examples | Less grounding for ZH audience | Replace fictional companies with ZH market equivalents (e.g., Meridian Dynamics → 远景咨询, Aurora → 朝霞科技) |
| Regulatory references | US/EU-specific | Replace with China-relevant context (PIPL for data protection, etc.) |
| Currency/figures | USD-denominated | Use CNY (e.g., $47,000 → 34万元) |

### 3.3 Register and tone
- **Simplified Chinese** (Mainland China standard), not Traditional
- Register: professional but approachable — same warmth as EN originals
- NOT corporate formal (公文体) — should read like a knowledgeable coach talking to a professional
- Technical explanations should be direct; avoid over-qualified academic phrasing
- Coach prompts (seen only by AI) can be slightly more direct than learner-facing text

---

## 4. Execution Approach

### Recommended: one pillar per Claude session, Opus 4.6

Each pillar JSON is ~5,000–8,000 words of EN content. Translation + cultural adaptation is a substantive task.

**Per-pillar process:**
1. Feed the full EN pillar JSON + the translation prompt (see `plans/zh-translation-prompt.md`)
2. Claude Opus 4.6 produces the full ZH JSON
3. Human review gate (see §5)
4. Write to `content/zh/pillars/{pillar}.json`

**Recommended sequence** (matches content generation order):
P1 → P2 → P5 (stable, low-perishable) → P3 → P4 → P6 → capstone

### Order within each pillar
Reading → Practice → Quiz → Build artifact (in that order, so each section informs the next)

---

## 5. Quality Review Gate

Every ZH pillar file must pass human review before merge. Reviewer checklist:

- [ ] All `{param}` slots intact and unchanged
- [ ] All technical terms (LLM, JSON, API, etc.) in English
- [ ] Framework acronyms (MAPS, CRAF, etc.) in English
- [ ] No `{` or `}` characters lost or doubled in translation
- [ ] Rubric scoring logic preserved — level 4 describes mastery, level 0 describes failure to engage
- [ ] Reading content: concept is accurate, not softened or simplified
- [ ] Good example and anti-pattern: culturally plausible for a Chinese professional context
- [ ] Register: natural professional Chinese, not machine-translated formal prose
- [ ] JSON is valid (`node -e "JSON.parse(require('fs').readFileSync('...'))"`)

---

## 6. App Integration — What Else Needs Changing

The app currently loads only EN pillar JSONs. Two changes needed after ZH content is ready:

### 6.1 Content loading (server-side)

In whichever route/server component loads pillar content, add lang-aware file selection:

```typescript
// Example pattern — adapt to actual loader location
const lang = user.lang ?? 'en';
const pillarPath = lang === 'zh'
  ? `content/zh/pillars/${pillarId}.json`
  : `content/pillars/${pillarId}.json`;
```

Fallback: if ZH file is missing for a pillar, fall back to EN silently.

### 6.2 Diagnostic content

`content/diagnostic_pillar.json` also needs ZH — create `content/zh/diagnostic_pillar.json` using the same translation prompt.

---

## 7. Scope Estimate

| Pillar | EN word count (approx) | Effort |
|--------|----------------------|--------|
| P1 Foundation | ~4,500 | Medium |
| P2 Prompting | ~4,500 | Medium |
| P3 Tool Fluency | ~4,000 | Medium-high (examples perishable) |
| P4 Configuration | ~4,500 | Medium |
| P5 Workflow | ~4,000 | Medium |
| P6 Agentic | ~4,500 | Medium |
| Capstone | ~2,000 | Low |
| Diagnostic | ~800 | Low |

**Total:** ~33,000 EN words → ~40,000 ZH characters (CN is denser)
One Claude Opus 4.6 session per pillar. Budget ~8 sessions including review cycles.

---

## 8. Open Decisions

- ⬜ **Who does the human review?** Native ZH speaker needed — confirm before starting
- ⬜ **Capstone priority** — low traffic at launch; can trail P1–P6 by one sprint
- ⬜ **Diagnostic pillar ZH** — needed if onboarding flow shows ZH to ZH-selected users
