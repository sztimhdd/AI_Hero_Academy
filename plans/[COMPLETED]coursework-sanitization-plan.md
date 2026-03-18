# Coursework Sanitization Plan

**Status**: PENDING
**Date**: 2026-03-18
**Phase**: Content Cleansing — Remove EDC-Specific Branding from All Coursework

---

## Problem Statement

Eight `content/*.json` files contain references that identify the app as belonging to Export Development Canada (EDC): the organization name, internal programme names, tool-approval framing, data-classification language, and business-unit names. This makes the app non-portable — it cannot be demonstrated to external audiences, white-labelled, or adapted for other organizations without first cleaning the content.

The sanitization must produce clean JSON files where no EDC-specific text survives, while leaving every structural key, every course/domain relationship, all scoring rubrics, and all fictional client companies (Crestwood, Northern Fabrication, Maple Industries, Bluewave, Westport, etc.) fully intact.

### Actual EDC reference count (pre-sanitization audit)

| File | EDC occurrences |
| ---- | --------------- |
| `content/practice_scenarios.json` | 33 |
| `content/reading_content_structured.json` | 14 |
| `content/diagnostic_items.json` | 12 |
| `content/reading_content.json` | 10 |
| `content/courses.json` | 10 |
| `content/evaluation_items.json` | 3 |
| `content/roles.json` | 3 |
| **TOTAL** | **85** |

---

## Goals

1. Reduce EDC occurrence count from 85 to 0 across all content files.
2. Replace EDC-specific framing ("EDC-approved AI tool", "EDC's Responsible AI policy", "non-public EDC information") with generic equivalents.
3. Replace EDC's division names (FinDev Canada, Impact team, Company Information Management team) with generic equivalents.
4. Replace the organization name with the fictional stand-in **"Apex Trade Finance"** wherever a concrete name is needed for scenario realism.
5. Validate that every JSON file is still syntactically valid and every content field the app reads is non-empty after substitution.
6. Confirm zero app regressions via `bash run_uat.sh` and Playwright visual check.

---

## Out of Scope — Do NOT Change

- **Fictional client/company names**: Crestwood Logistics, Northern Fabrication Ltd., Maple Industries Ltd., Vantara Foods, Driftwood Packaging, Irongate Civil, **Bluewave**, **Westport Composites**, **Meridian Trade Finance Bank** — these are fictional clients used in scenarios and must not be altered.
- **"Meridian" as a client bank**: `Meridian Trade Finance Bank` in `diagnostic_items.json` is a fictional client, not an EDC programme — keep it.
- **Microsoft product names**: `M365`, `Copilot`, `Teams`, `SharePoint` as generic tool references — keep the product name; only strip the "EDC-approved" or "within EDC tenant" wrapper phrases.
- **`credit committee`**: Generic financial services term — keep as-is.
- **`SAFE Abstraction Method`**: A named framework in the reading content. Keep the name; only strip surrounding EDC context sentences if present.
- **`KYC / CIM Validation Agent`**: Functional label in `courses.json` — keep as-is; strip EDC context in surrounding description fields only.
- **Role names** (RM, UW, AN, MK) and display titles — generic job functions, no change needed.
- **JSON structural keys, field names, and IDs** — nothing structural changes.
- **`content/atomic_modules.json`** (if present from Phase 0.5) — generated file; will be regenerated after sanitization.
- **Any code** in `app.py`, `pages/`, `utils/` — pure content-only operation. `pages/04_Course_Module.py` renders content fields as-is; the page itself contains no EDC text.

---

## EDC-Specific Content Inventory

### Affected files and field paths

| File | Affected fields | Notes |
| ---- | --------------- | ----- |
| `content/courses.json` | `tagline`, `description`, `real_use_case` | 10 occurrences |
| `content/practice_scenarios.json` | `scenario_text`, `coach_system_prompt`, `task_1_text`–`task_4_text` | 33 occurrences; highest density |
| `content/diagnostic_items.json` | `scenario_text`, `question_text`, `answer_options[].text` | 12 occurrences |
| `content/evaluation_items.json` | `question_text`, `scenario_text`, `scoring_rubric` | 3 occurrences |
| `content/reading_content.json` | `concept_text`, `good_example`, `anti_pattern`, `takeaway` | 10 occurrences |
| `content/reading_content_structured.json` | `concept_text_structured`, `good_example_structured`, `anti_pattern_structured`, `takeaway_structured` (embedded JSON sub-objects) | 14 occurrences; special handling required — rendered as UI cards in `pages/04_Course_Module.py`; LLM rewrite must preserve nested structure |
| `content/roles.json` | `description` per role | 3 occurrences |

### Known EDC-specific strings to replace

#### Organization name variants

- `EDC` / `EDC's` / `at EDC` / `the EDC`

#### Programme / project names (strip EDC context, keep name)

- `Meridian Infrastructure Briefing` → `Meridian Infrastructure Programme`
- `Aurora Initiative` → keep as-is (no EDC context around it)
- `Cascade Portfolio` → keep as-is
- `Enterprise Intelligence Program` → keep as-is

#### Division / team names

- `FinDev Canada` → `the development finance division`
- `Impact team (FinDev Canada)` → `the development finance team`
- `Impact team` → `the development finance team` _(only in FinDev Canada context; keep standalone "Impact team" if it appears without FinDev)_
- `Company Information Management team` → `the client data management team`

#### Policy / governance framing

- `EDC's Responsible AI policy` → `your organization's AI use policy`
- `EDC-approved AI tool` → `your organization's approved AI tool`
- `EDC-approved` → `organization-approved`
- `non-public EDC information` → `non-public organizational data`

#### Internal document / system terminology

- `CIS buyer-file note` → `client file note`
- `within EDC's [system/tenant]` → `within the organization's [system/tenant]`
- `EDC data` → `organizational data`
- `EDC tenant` → `organization's tenant`

---

## Replacement Dictionary

Applied in **longest-match-first** order to prevent partial replacement (e.g., replacing `EDC's` before a bare `EDC` match would corrupt `EDC's Responsible AI policy`):

| Priority | Original | Replacement |
| -------- | -------- | ----------- |
| 1 | `EDC's Responsible AI policy` | `your organization's AI use policy` |
| 2 | `EDC-approved AI tool` | `your organization's approved AI tool` |
| 3 | `non-public EDC information` | `non-public organizational data` |
| 4 | `Impact team (FinDev Canada)` | `the development finance team` |
| 5 | `Meridian Infrastructure Briefing` | `Meridian Infrastructure Programme` |
| 6 | `Company Information Management team` | `the client data management team` |
| 7 | `CIS buyer-file note` | `client file note` |
| 8 | `FinDev Canada` | `the development finance division` |
| 9 | `EDC-approved` | `organization-approved` |
| 10 | `within EDC's` | `within the organization's` |
| 11 | `EDC tenant` | `organization's tenant` |
| 12 | `EDC data` | `organizational data` |
| 13 | `at EDC` | `at Apex Trade Finance` |
| 14 | `EDC's` | `Apex Trade Finance's` |
| 15 | `the EDC` | `Apex Trade Finance` |
| 16 | `EDC` _(word boundary `\bEDC\b`)_ | `Apex Trade Finance` |

**Apex Trade Finance** is the chosen stand-in org name. It is plausible for the export credit / trade finance context of the content and is clearly fictional.

**Case sensitivity**: Apply case-preserving regex. `edc` (all lowercase) should also be caught if present.

---

## Implementation Phases

### Phase 0 — Build & Audit (no writes to content files)

Write `scripts/sanitize_content.py` with a `--dry-run` mode:

1. Load all eight target `content/*.json` files.
2. Walk every string value recursively (nested objects and arrays, including embedded JSON strings in `reading_content_structured.json`).
3. Check each string against the replacement dictionary using word-boundary regex.
4. Print a report: `file → field path → matched pattern → occurrence count`.
5. Print the total occurrence count per file and grand total.
6. Exit non-zero if any occurrences found (CI gate).

Run `--dry-run` first. Confirm the output matches the 85-occurrence baseline before writing any content.

**Git checkpoint after Phase 0:**

```bash
git add scripts/sanitize_content.py
git commit -m "feat: add content sanitization script (audit + apply modes)"
```

---

> **`/compact` before Phase 1**
>
> ```text
> /compact Phase 0 complete — script built, dry-run verified 85 EDC occurrences.
> Preserve replacement dictionary, script CLI design, and 85-occurrence breakdown table.
> Drop all code exploration context.
> ```

---

### Phase 1 — Scripted String Replacement

Run:

```bash
python scripts/sanitize_content.py --apply
```

Algorithm:

1. For each target file: load JSON, walk all string values.
2. For each string: apply all substitutions from the replacement dictionary in priority order (row 1 before row 16).
3. **Special handling for `reading_content_structured.json`**: the structured sub-fields (`concept_text_structured`, etc.) are JSON objects serialized as strings within the outer JSON. Parse these nested JSON strings, apply substitutions to their string values, then re-serialize to JSON string before writing back.
4. Write the mutated JSON back to the same path (`indent=2`, `ensure_ascii=False`).
5. After each file write: reload and confirm valid JSON parse.
6. Log every substitution: `file | field path | matched pattern | old snippet (40 chars) → new snippet (40 chars)`.

After `--apply`, immediately run:

```bash
python scripts/sanitize_content.py --validate-only
```

Expected: EDC count drops from 85 toward 0. Any residual count means Phase 2 is needed.

**Git checkpoint after Phase 1:**

```bash
git add content/courses.json \
        content/practice_scenarios.json \
        content/diagnostic_items.json \
        content/evaluation_items.json \
        content/reading_content.json \
        content/reading_content_structured.json \
        content/roles.json
git commit -m "chore: apply scripted EDC→Apex Trade Finance string replacements across content files"
```

### Phase 2 — LLM-Assisted Rewrite for Residual Passages (if needed)

If `--validate-only` exits non-zero after Phase 1, residual EDC references survived (contextual references the dictionary could not cleanly resolve). Run:

```bash
python scripts/sanitize_content.py --apply --llm
```

For each string field still containing `EDC` after Phase 1, send to Gemini 2.0 Flash with this prompt:

```text
You are rewriting training content for a generic financial services organization
called "Apex Trade Finance". Rewrite the following passage so that:
- All references to "EDC", its policies, programmes, and internal systems are
  replaced with generic equivalents referencing "Apex Trade Finance".
- Do NOT change fictional client company names (Crestwood, Bluewave, Westport,
  Northern Fabrication, etc.) — these are fictional and must stay.
- Do NOT change Microsoft product names (M365, Copilot, Teams).
- Do NOT change the SAFE Abstraction Method name.
- Do NOT change the meaning, scenario structure, difficulty, or answer keys.
- Return ONLY the rewritten text, no commentary.

Original:
{passage}
```

For `reading_content_structured.json` residuals: parse the nested JSON sub-object, apply the LLM rewrite to each text leaf value independently, then re-serialize to valid JSON. Do NOT send the entire JSON sub-object to the LLM — iterate leaf by leaf.

LLM call config: `gemini-2.0-flash`, temperature 0.1, max_tokens 2048, 3 retries on failure.

Log: `file | field path | ORIGINAL → REWRITTEN`.

After `--apply --llm`, re-run `--validate-only`. Iterate (extend dictionary + re-run) until exit code 0.

**Git checkpoint after Phase 2 (only if LLM was needed):**

```bash
git add content/practice_scenarios.json \
        content/reading_content.json \
        content/reading_content_structured.json \
        content/diagnostic_items.json
git commit -m "chore: LLM-rewrite residual EDC references in content files"
```

---

> **`/compact` before Phase 3**
>
> ```text
> /compact Phases 1–2 complete — all 85 EDC occurrences removed, validate-only exits 0.
> Preserve acceptance criteria, manual spot-check list, and UAT test plan.
> Drop substitution logs and LLM rewrite outputs.
> ```

---

### Phase 3 — Structural Validation

Run `--validate-only`. It must assert:

1. **JSON validity**: every file reloads cleanly; abort with a clear message on parse error.
2. **Field completeness**: for every course in `courses.json`, `tagline` and `description` are non-empty. For every scenario, `scenario_text` is non-empty. For every diagnostic/eval item, `question_text` is non-empty.
3. **No residual EDC**: zero occurrences of standalone `EDC` (case-insensitive word-boundary). Exit non-zero + print offenders if any found.
4. **ID stability**: all course IDs, domain keys, item IDs, and role codes are identical to the pre-sanitization values (snapshot taken at Phase 0 start).
5. **Nested JSON integrity**: for `reading_content_structured.json`, each structured sub-field that was a valid JSON object before Phase 1 is still a valid JSON object after.

Exit code 0 = clean. This mode is the CI gate.

### Phase 4 — Manual Spot-Check (human review, no writes)

Before the final commit, read these high-risk passages directly in the sanitized JSON:

| File | What to review |
| ---- | -------------- |
| `practice_scenarios.json` | All `scenario_text` and `coach_system_prompt` for rm_c1–rm_c7 (33 EDC refs) |
| `reading_content_structured.json` | The `body` text inside `cards[]` and the `guardrails[]` list for rm_c1 (dense SAFE method content) |
| `reading_content.json` | `concept_text` and `takeaway` for rm_c1 and an_c1 |
| `diagnostic_items.json` | Items with `EDC-approved AI tool` in `question_text` (was rm_d4–rm_d6 area) |
| `courses.json` | All `real_use_case` fields for rm, uw, an, mk courses; confirm FinDev Canada is gone |
| `roles.json` | All `description` fields; confirm "EDC's Responsible AI policy" is gone |

Verify: `Meridian Trade Finance Bank` is still present (fictional client, must not be removed). Verify: `credit committee` is still present. Verify: `SAFE Abstraction Method` name is still present.

### Phase 5 — App Regression Test

Reset UAT test user and run:

```bash
python scripts/reset_uat_user.py --role rm
bash run_uat.sh
```

Use Playwright (`mcp__playwright__browser_*`) to exercise the full RM journey in `pages/04_Course_Module.py`:

1. Navigate to `http://localhost:8501`
2. Complete role selection → 12-question diagnostic → Skills Profile
3. Navigate to Home → Module 1 → Overview tab
4. Module 1 → Reading tab (all 4 sections: Concept / Example / Pitfall / Takeaway)
5. Module 1 → Practice tab → submit Task 1 response, verify coach reply renders
6. Module 1 → Evaluation tab → answer all 4 questions → Results page

Take a screenshot at steps 4, 5, and 6. Confirm:

- No visible `EDC` text anywhere in the rendered UI
- No empty scenario text, reading cards, question text, or coach prompts
- No `None`, `null`, or `[object Object]` displayed where content should be
- No Python exceptions in the terminal

If any regression is found: trace to the specific JSON field, fix the content directly in the JSON file, and re-run `--validate-only` before retesting.

---

## Script Design

### `scripts/sanitize_content.py`

```text
CLI:
  python scripts/sanitize_content.py --dry-run        # Audit only, no writes (Phase 0)
  python scripts/sanitize_content.py --apply           # Apply string replacements (Phase 1)
  python scripts/sanitize_content.py --apply --llm     # Apply replacements + LLM rewrite (Phase 2)
  python scripts/sanitize_content.py --validate-only   # Structural validation CI gate (Phase 3)

Key functions:
  load_content_files() → dict[str, Any]
  snapshot_ids(data) → dict                             # capture all IDs before mutation
  audit_edc_occurrences(data) → dict[str, list[Match]]
  apply_replacement_dict(data) → tuple[dict, int]       # returns mutated data + sub count
  handle_structured_field(value: str) → str             # parse embedded JSON, apply subs, re-serialize
  rewrite_residuals_with_llm(data) → dict
  validate_structure(data_before, data_after) → bool
  write_content_files(data) → None

Target files (hardcoded, in processing order):
  content/roles.json
  content/courses.json
  content/diagnostic_items.json
  content/evaluation_items.json
  content/practice_scenarios.json
  content/reading_content.json
  content/reading_content_structured.json              ← special handling

Excluded from processing:
  content/atomic_modules.json  (if present)
```

---

## Acceptance Criteria

**AC-1 — Script built and dry-run matches baseline**: `--dry-run` reports exactly 85 EDC occurrences across 7 files, matching the table in the Problem Statement. Script exits non-zero.

**AC-2 — Validate-only exits clean**: After applying all phases, `--validate-only` exits code 0, prints "✓ 0 EDC occurrences found", and confirms all 7 files structurally valid with no empty required fields.

**AC-3 — Content integrity**: All course IDs, domain keys, item IDs, role codes, and fictional client company names (including Meridian Trade Finance Bank, Bluewave, Westport) are identical to pre-sanitization values. `credit committee`, `SAFE Abstraction Method`, and Microsoft product names (M365, Copilot) are present and unchanged.

**AC-4 — App regression**: Full RM journey through Module 1 (Reading → Practice → Evaluation → Results) completes without errors. No `EDC` string visible in any rendered UI component.

**AC-5 — Commit diff is content-only**: `git diff --stat` shows changes only to `content/*.json` and `scripts/sanitize_content.py`. No application code modified.

---

## Risks

| Risk | Severity | Mitigation |
| ---- | -------- | ---------- |
| JSON parse failure after substitution | HIGH | Reload + validate after every file write; abort on parse error |
| Nested JSON corruption in `reading_content_structured.json` | HIGH | Parse embedded JSON separately; apply subs to leaf strings only; re-serialize and validate before write |
| Partial replacement (word-boundary regex edge cases) | MEDIUM | Use `\bEDC\b` regex; test on dry-run output first |
| LLM rewrite silently changes MCQ answer keys or rubric scoring | MEDIUM | LLM prompt explicitly prohibits changing meaning/difficulty; human review of all LLM-touched items |
| `practice_scenarios.json` has 33 occurrences embedded in long prose blocks | MEDIUM | Apply dictionary first; only send to LLM if dictionary can't resolve; log every change |
| `Impact team` appears in non-FinDev contexts | LOW | Only replace `Impact team` when adjacent to `FinDev Canada`; bare `Impact team` alone — review case by case |

---

## Definition of Done

- [ ] `scripts/sanitize_content.py` implemented with all four CLI modes
- [ ] `--dry-run` confirms 85 baseline occurrences
- [ ] `--apply` run; substitution log reviewed; count drops to 0 or near-0
- [ ] If LLM needed: `--apply --llm` run; log reviewed
- [ ] `--validate-only` exits code 0
- [ ] Git checkpoint after script, after string replacements, after LLM pass (if needed)
- [ ] Manual spot-check of high-risk passages completed (Phase 4)
- [ ] App regression confirmed via `bash run_uat.sh` + Playwright screenshots
- [ ] Final commit staged with content-only diff
