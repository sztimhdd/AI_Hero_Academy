# Kickstart Prompt — Coursework Sanitization

> Copy the entire block below and paste it as your first message in a fresh Claude Code session.

---

## Agent Prompt

You are implementing the **Coursework Sanitization** task for the AI Hero Academy app.
Goal: reduce EDC-specific branding occurrences from **85 → 0** across all content files.

Full plan: [`plans/coursework-sanitization-plan.md`](plans/coursework-sanitization-plan.md)

**Before writing a single line of code**, read these files in full:

1. [`plans/coursework-sanitization-plan.md`](plans/coursework-sanitization-plan.md) — full spec, replacement dictionary, acceptance criteria
2. [`content/courses.json`](content/courses.json) — 28 courses; check `tagline`, `description`, `real_use_case` (10 EDC refs)
3. [`content/practice_scenarios.json`](content/practice_scenarios.json) — scenario prose and coach prompts (**33 EDC refs — highest density**)
4. [`content/diagnostic_items.json`](content/diagnostic_items.json) — item scenario and question text (12 EDC refs)
5. [`content/evaluation_items.json`](content/evaluation_items.json) — question text, scenario text, rubrics (3 EDC refs)
6. [`content/reading_content.json`](content/reading_content.json) — flat prose fields (10 EDC refs)
7. [`content/reading_content_structured.json`](content/reading_content_structured.json) — **nested JSON sub-objects** rendered as UI cards in `pages/04_Course_Module.py`; requires special handling (14 EDC refs)
8. [`content/roles.json`](content/roles.json) — role descriptions (3 EDC refs)

Only after reading all eight files should you begin implementation.

**Key "do not touch" rules** (memorize before writing any code):

- Fictional client/company names (`Meridian Trade Finance Bank`, `Bluewave`, `Westport Composites`, `Crestwood`, `Northern Fabrication`, `Maple Industries`, `Vantara Foods`, `Irongate Civil`) — **do not change**
- `credit committee` — generic financial term, **keep as-is**
- `SAFE Abstraction Method` — named framework, **keep the name**; only strip surrounding EDC sentences
- Microsoft product names (`M365`, `Copilot`, `Teams`) — keep the product name; only strip `EDC-approved` / `within EDC tenant` wrapper phrases
- JSON structural keys, IDs, and role codes — **nothing structural changes**

---

## AC-1 — Build and run dry-run audit

Implement `scripts/sanitize_content.py` with four CLI modes:

```bash
python scripts/sanitize_content.py --dry-run        # Audit all 8 files, no writes
python scripts/sanitize_content.py --apply           # Apply replacement dictionary to all 8 files
python scripts/sanitize_content.py --apply --llm     # Apply replacements + LLM rewrite for residuals
python scripts/sanitize_content.py --validate-only   # Structural validation CI gate
```

**Replacement dictionary** — apply in this exact priority order (longest patterns first):

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

**Special handling for `reading_content_structured.json`**: the `concept_text_structured`, `good_example_structured`, `anti_pattern_structured`, and `takeaway_structured` fields are embedded JSON objects (stored as JSON strings within the outer JSON). Walk these nested structures by parsing them as JSON, applying substitutions to leaf string values only, then re-serializing to JSON string before writing back.

Run dry-run immediately after building:

```bash
python scripts/sanitize_content.py --dry-run
```

Expected: **85 total EDC occurrences** across 8 files, matching the table in the plan. If the count differs, investigate before proceeding.

**Git checkpoint:**

```bash
git add scripts/sanitize_content.py
git commit -m "feat: add content sanitization script (dry-run, apply, validate modes)"
```

---

> **`/compact` before AC-2**
>
> ```text
> /compact AC-1 done — sanitize_content.py built, dry-run confirmed 85 EDC occurrences.
> Preserve: replacement dictionary (priority 1–16), special handling rule for
> reading_content_structured.json, do-not-touch list (Meridian Trade Finance Bank,
> Bluewave, Westport, credit committee, SAFE Abstraction Method, M365/Copilot).
> Drop: all file-reading context and code exploration.
> ```

---

## AC-2 — Apply replacements and validate

```bash
# Step 1: Apply string replacements
python scripts/sanitize_content.py --apply

# Step 2: Run validate-only
python scripts/sanitize_content.py --validate-only
# Expected: exits 0, prints "✓ 0 EDC occurrences found"
```

If `--validate-only` exits non-zero (residual EDC refs survived the dictionary):

```bash
# Step 3: LLM rewrite for residuals
python scripts/sanitize_content.py --apply --llm

# Step 4: Re-validate
python scripts/sanitize_content.py --validate-only
```

For LLM rewrite (`--llm` flag), use Gemini 2.0 Flash via `utils/ai.py` helpers (or direct `google.genai` SDK call). Per-passage prompt:

```text
You are rewriting training content for a generic financial services organization
called "Apex Trade Finance". Rewrite the following passage so that:
- All references to "EDC", its policies, programmes, and internal systems are
  replaced with generic equivalents referencing "Apex Trade Finance".
- Do NOT change fictional client company names (Crestwood, Bluewave, Westport,
  Meridian Trade Finance Bank, Northern Fabrication, etc.).
- Do NOT change Microsoft product names (M365, Copilot, Teams).
- Do NOT change the SAFE Abstraction Method name.
- Do NOT change the meaning, scenario structure, difficulty, or answer keys.
- Return ONLY the rewritten text, no commentary.

Original:
{passage}
```

For `reading_content_structured.json`: rewrite leaf string values one by one — do NOT send the full JSON sub-object to the LLM.

If `--validate-only` still fails after `--apply --llm`, print the remaining occurrences, extend the replacement dictionary, and re-run until exit 0.

**Manual spot-check** (read directly in the sanitized JSON before committing):

- `practice_scenarios.json` — all `scenario_text` and `coach_system_prompt` for roles rm and an
- `reading_content_structured.json` — `cards[].body` and `guardrails[]` items for rm_c1
- `diagnostic_items.json` — items that previously referenced `EDC-approved AI tool`
- `courses.json` — all `real_use_case` fields; confirm `FinDev Canada` is gone
- `roles.json` — all `description` fields

Verify these are still present (must NOT have been changed):

- `Meridian Trade Finance Bank` in `diagnostic_items.json`
- `credit committee` in `evaluation_items.json`
- `SAFE Abstraction Method` in `reading_content.json`

**Git checkpoint:**

```bash
git add content/courses.json \
        content/practice_scenarios.json \
        content/diagnostic_items.json \
        content/evaluation_items.json \
        content/reading_content.json \
        content/reading_content_structured.json \
        content/roles.json
git commit -m "chore: sanitize content files — remove all EDC branding (85 → 0 occurrences)"
```

If LLM pass was also needed:

```bash
git add content/practice_scenarios.json content/reading_content.json content/reading_content_structured.json
git commit -m "chore: LLM-rewrite residual EDC references in content files"
```

---

> **`/compact` before AC-3**
>
> ```text
> /compact AC-2 done — all 85 EDC occurrences removed, validate-only exits 0.
> Preserve: AC-3 UAT test plan (reset_uat_user.py --role rm, bash run_uat.sh,
> Playwright journey through Module 1 Reading/Practice/Evaluation/Results),
> acceptance criteria AC-3 and AC-4 from the plan.
> Drop: substitution logs, LLM rewrite outputs, all content file context.
> ```

---

## AC-3 — App regression test

Reset the UAT test user to RM role and start the app:

```bash
python scripts/reset_uat_user.py --role rm
bash run_uat.sh
```

Use Playwright (`mcp__playwright__browser_*`) to exercise the full RM journey through `pages/04_Course_Module.py`:

1. Navigate to `http://localhost:8501` — take screenshot
2. Complete role selection → 12-question diagnostic → Skills Profile — take screenshot
3. Home → Module 1 Overview tab
4. Module 1 → Reading tab — cycle through all 4 sections (Concept / Example / Pitfall / Takeaway) — **take screenshot of Concept section**
5. Module 1 → Practice tab → submit a response to Task 1, verify coach reply renders — **take screenshot**
6. Module 1 → Evaluation tab → answer all 4 questions → Results page — **take screenshot**

At each step confirm:

- No visible `EDC` text anywhere in the rendered UI
- No empty fields (scenario text, reading card body text, question text, coach prompts)
- No `None`, `null`, or `[object Object]` rendered where content should be
- No Python exceptions in the terminal

If any regression is found: trace to the specific JSON field, fix the content directly in the JSON file, re-run `--validate-only`, and retest. Do NOT modify any application code.

---

## Final commit and plan update

```bash
# Confirm diff is content-only
git diff --stat HEAD

# Rename plan file to mark complete
mv plans/coursework-sanitization-plan.md "plans/[COMPLETED]coursework-sanitization-plan.md"
git add "plans/[COMPLETED]coursework-sanitization-plan.md" plans/coursework-sanitization-plan.md
git commit -m "docs: mark coursework sanitization plan complete"
```
