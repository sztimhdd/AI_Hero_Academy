# Phase 3: Multi-Agent Course Content Generation Script

> **Status:** DRAFT

---

## Specification

**Problem:** Creating course content for a new role currently requires Claude Code to generate all 7 JSON files in a single pass. This mixes near-deterministic schema conversion (roles, domains, courses) with deep content authoring (scenarios, reading concepts, assessments), degrading quality across both. There is no quality gate before content agents run, and no mechanism to recover from an incomplete or vague Course Design Brief without manual intervention.

**Goal:** A Python script (`scripts/generate_course_content.py`) that accepts a Course Design Brief markdown file and produces all 7 role-specific JSON content files. The script self-diagnoses brief quality, generates a targeted Copilot follow-up prompt if remediation is needed, and runs content agents in the correct parallelisation pattern. A human only intervenes when the brief is genuinely insufficient — and when they do, the script tells them exactly what to ask.

**Scope:**

In scope:

- `scripts/generate_course_content.py` — the full pipeline script
- Updates to `prompts/copilot-course-design-brief.md` (Prompt C) for parser-friendly output format
- Updates to `prompts/copilot-role-intelligence.md` (Prompt A) for `role_prefix` field and structured Section 13B
- Updates to `prompts/copilot-use-case-mapping.md` (Prompt B) for explicit `course_id` and verbatim `real_use_case` output

Out of scope:

- Seeding generated JSONs into Delta tables (existing notebook handles this)
- Admin UI or validation dashboard
- State persistence between script runs (re-run from Stage 1 on each invocation)
- Multi-role batch generation

**Success Criteria:**

- [ ] Script accepts a brief filepath as CLI argument and exits with a clear error if file is not found
- [ ] Parser correctly extracts: role_prefix, 5 fictional companies (course-mapped), framework_names, real_use_case strings, domain seeds, course seeds, scenario seeds
- [ ] Parser handles two-pass merge: main brief body + `## SUPPLEMENTAL OUTPUT` section appended by human
- [ ] QA gap check detects both missing fields and subpar quality (vague scenario seeds, un-adapted domain descriptors)
- [ ] When gaps found: script prints structured flag list + ready-to-paste Copilot follow-up prompt, exits cleanly
- [ ] When brief is clean: all 7 JSON files are written to `content/` with correct naming convention
- [ ] Stage 4 (5x course content agents) runs in parallel; Stage 6 (evaluation) runs after Stage 4 completes
- [ ] All generated `course_id` values follow `<role_prefix>_c<1-5>_<domain_id>` pattern
- [ ] No real company names, EDC client data, or non-fictional entities in any output
- [ ] Rubric scores are on 0–4 scale throughout
- [ ] Coach system prompts contain a data safety guardrail instruction
- [ ] Existing RM JSON files are never overwritten

---

## Pipeline Architecture

```text
Brief (markdown file)
        │
        ▼
┌─────────────────────┐
│  Stage 1            │  Haiku — Brief Parser Agent
│  Parse & Extract    │  Outputs: internal spec dict
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Stage 2            │  Haiku — Structural Generator
│  roles / domains /  │  Outputs: roles.json, domains.json,
│  courses JSON       │           courses.json (draft)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Stage 3            │  Sonnet — QA Gap Check Agent
│  Completeness &     │  PASS → proceed to Stage 4
│  Quality Gate       │  FAIL → print flags + follow-up
└────────┬────────────┘         prompt → exit
         │ PASS
         ▼
┌────────────────────────────────────────────────────┐
│  Stage 4 (parallel)         Stage 5 (parallel)     │
│  5x Course Content Agents   Assessment Designer    │
│  Sonnet                     Sonnet                 │
│  reading_content +          12 diagnostic items    │
│  practice_scenario          (3/domain: MCQ +       │
│  per course                 prompt_sandbox +       │
│                             micro_task)            │
└────────────────┬───────────────────────────────────┘
                 │  Stage 4 complete
                 ▼
┌─────────────────────┐
│  Stage 6            │  Sonnet — Evaluation Designer
│  evaluation_items   │  20 items (4/course: 3 MCQ + 1 perf_task)
│  JSON               │  Depends on Stage 4 reading content
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Stage 7            │  Sonnet — Final QA / Validation Agent
│  Cross-validate     │  Checks: FK consistency, rubric scales,
│  all outputs        │  company uniqueness, content alignment
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Stage 8            │  Orchestrator assembles + writes
│  Assemble & Write   │  7 JSON files to content/
└─────────────────────┘
```

---

## Remediation Loop

```text
Gap check FAIL
        │
        ▼
Print to terminal:
  ① Structured flag list (missing fields + quality issues)
  ② Ready-to-paste Copilot follow-up prompt:
     - References specific section labels from brief
     - Instructs Copilot to output ONLY missing sections
     - Instructs Copilot to use heading: ## SUPPLEMENTAL OUTPUT
        │
        ▼
Human action:
  - Pastes follow-up prompt into Corp Copilot
  - Appends Copilot's response to end of brief file
  - Re-runs: python scripts/generate_course_content.py <brief.md>
        │
        ▼
Parser two-pass merge:
  - Parses main brief body first
  - Detects ## SUPPLEMENTAL OUTPUT section
  - Merges supplemental fields, overwriting gaps
  - Proceeds to Stage 2
```

---

## Shared Context Object

The orchestrator maintains a `shared_context` dict injected into each agent's system prompt (only the relevant subset per agent):

```python
shared_context = {
  "role_prefix":        str,              # e.g. "uw"
  "role_display_name":  str,              # e.g. "Underwriter"
  "company_map":        {1: str, ..., 5: str},  # course_pos → company name
  "framework_names":    [str, ...],       # coined terms from brief
  "domain_ids":         ["prompting", "verification", "data_safety", "tool_fluency"],
  "course_id_map":      {1: str, ..., 5: str},  # e.g. {1: "uw_c1_prompting"}
  "real_use_cases":     {1: str, ..., 5: str},  # verbatim from Prompt B output
}
```

---

## Model Selection

| Agent | Model | Rationale |
| --- | --- | --- |
| Brief Parser | Haiku | Structured extraction; speed matters on re-runs |
| Structural Generator | Haiku | Near-deterministic schema conversion; low temp |
| QA Gap Check | Sonnet | Needs judgment for quality failures (not just missing fields) |
| Course Content × 5 | Sonnet | Narrative quality; good_example / anti_pattern require depth |
| Assessment Designer | Sonnet | Rubric design; MCQ distractor quality |
| Evaluation Designer | Sonnet | Must align with reading content; subtle calibration |
| Final QA | Sonnet | Cross-document reasoning |

---

## Content Constraints (enforced by agents + final QA)

- Fictional companies only — no real EDC clients, no real Canadian exporters
- Each of the 5 courses gets a distinct fictional company name
- `course_id` pattern: `<role_prefix>_c<N>_<domain_id>` (e.g., `uw_c2_verification`)
- `content_id` pattern: `rc_<course_id>` for reading; `ps_<course_id>` for scenarios
- Domain IDs must be exactly one of: `prompting`, `verification`, `data_safety`, `tool_fluency`
- Rubric scores: all criteria on 0–1 scale, total scaled to 0–4
- Every coach system prompt must include: instruction to flag if user appears to input real client data
- Capstone course (`c5`) uses `prompting` as `primary_domain` but integrates all 4 domains

---

## Output Files

All written to `content/` directory. Existing RM files are never modified.

| File | Keys | Notes |
| --- | --- | --- |
| `roles.json` | `role_id`, `display_name`, `description` | Add new role entry |
| `domains.json` | `domain_id`, `role_id`, `title`, `description`, `level_0_*` … `level_4_*` | 4 entries, role-adapted descriptors |
| `courses.json` | `course_id`, `role_id`, `primary_domain`, `title`, `tagline`, `description`, `real_use_case`, `sequence_order` | 5 entries |
| `reading_content.json` | `content_id`, `course_id`, `concept_text`, `good_example`, `anti_pattern`, `takeaway` | 5 entries |
| `practice_scenarios.json` | `scenario_id`, `course_id`, `scenario_text`, `task_1_text`…`task_4_text`, `coach_system_prompt` | 5 entries |
| `diagnostic_items.json` | `item_id`, `domain_id`, `item_type`, `question_text`, `options`/`scenario_text`, `correct_option`/`scoring_rubric` | 12 entries (3/domain) |
| `evaluation_items.json` | `item_id`, `course_id`, `item_type`, `question_text`, `options`, `correct_option`/`scoring_rubric` | 20 entries (4/course) |

---

## Tasks

### Prompt Updates

**Context:** `prompts/`

**Steps:**

1. [ ] Update `prompts/copilot-role-intelligence.md` (Prompt A):
   - Add `role_prefix` field to Section 1 (2–3 lowercase letters, e.g., `uw`, `cs`, `rm`)
   - Restructure Section 13B scenario seeds to use labeled fields: `Company:`, `Trigger:`, `AI_temptation:`, `Skill_test:`, `Domain:`

2. [ ] Update `prompts/copilot-use-case-mapping.md` (Prompt B):
   - Add `course_id` column to Task 3 output using the role prefix (`<prefix>_c1_prompting`, etc.)
   - Flag `real_use_case` as verbatim-quotable (not paraphrased)

3. [ ] Update `prompts/copilot-course-design-brief.md` (Prompt C):
   - Enforce stable, numbered section headers: `### Course 1 — [Title]`, `### Domain: prompting`, etc.
   - Add Machine-Readable Header block at top of output: `role_prefix`, `company_map`, `framework_names`, `real_use_case` strings
   - Add note at end of prompt: *"If you receive a follow-up request for missing sections, output under `## SUPPLEMENTAL OUTPUT` using the same section labels."*

**Verify:** Manually trace the parser logic against a sample brief to confirm all extraction targets are reachable by label/heading match.

---

### Stage 1 — Brief Parser Agent

**Context:** `scripts/generate_course_content.py`, `prompts/copilot-course-design-brief.md`, `content/` (schema reference)

**Steps:**

1. [ ] Implement CLI entry point: `python scripts/generate_course_content.py <brief_filepath>`
2. [ ] Implement `parse_brief(filepath) -> spec_dict`:
   - Detect and split `## SUPPLEMENTAL OUTPUT` section if present (two-pass merge)
   - Extract Machine-Readable Header block (role_prefix, company_map, framework_names, real_use_case)
   - Extract domain seeds (4 entries, level descriptors per level 0–4)
   - Extract course seeds (5 entries, one per section heading)
   - Extract scenario seeds (company, trigger, AI_temptation, skill_test, domain per course)
   - Extract reading concept seeds (framework, concept overview, example, anti-pattern per course)
   - Extract diagnostic item seeds (3 per domain)
   - Extract evaluation item seeds (4 per course)
3. [ ] Implement two-pass merge: supplemental fields overwrite gaps in main spec

**Verify:** Print parsed spec dict for a test brief; confirm all keys populated correctly.

---

### Stage 2 — Structural Generator Agent

**Context:** `scripts/generate_course_content.py`, `content/roles.json`, `content/domains.json`, `content/courses.json` (schema reference)

**Steps:**

1. [ ] Implement `generate_structural_json(spec_dict, shared_context) -> structural_outputs`:
   - Call Haiku with spec_dict + RM schema examples as system context
   - Temperature: 0.1
   - Generate `roles.json` entry, all 4 `domains.json` entries, all 5 `courses.json` entries
   - Validate all `course_id` values match `<role_prefix>_c<N>_<domain_id>` pattern before returning
2. [ ] Build `shared_context` dict from spec_dict + structural outputs (course_id_map, company_map, etc.)

**Verify:** Assert course_ids, domain_ids, and role_id are internally consistent across the 3 files.

---

### Stage 3 — QA Gap Check Agent

**Context:** `scripts/generate_course_content.py`

**Steps:**

1. [ ] Implement `qa_gap_check(spec_dict, structural_outputs) -> (passed: bool, flags: list[dict])`:
   - **Missing field checks**: role_prefix, all 5 companies, 5 real_use_case strings, 4 domain seeds with level descriptors, 5 scenario seeds with all 4 required fields
   - **Quality checks** (Sonnet call): scenario AI_temptation fields are specific (tool + failure mode named), domain descriptors are role-adapted (not RM copy), reading concept seeds name a concrete framework or technique
   - Return `passed=True` if zero flags; else return structured flag list
2. [ ] Implement `generate_followup_prompt(flags: list[dict]) -> str`:
   - Formats terminal output: flag list + ready-to-paste Copilot prompt
   - Copilot prompt references specific section labels, lists only what's missing, instructs `## SUPPLEMENTAL OUTPUT` format
3. [ ] If `passed=False`: print follow-up prompt to terminal, print re-run instructions, `sys.exit(0)`

**Verify:** Test with a deliberately incomplete brief; confirm terminal output is copy-paste ready.

---

### Stage 4 — Course Content Agents (parallel)

**Context:** `scripts/generate_course_content.py`, `content/reading_content.json`, `content/practice_scenarios.json` (schema reference)

**Steps:**

1. [ ] Implement `generate_course_content(course_spec, shared_context) -> (reading_entry, scenario_entry)`:
   - Single Sonnet call per course
   - System prompt includes: RM reading + scenario examples as few-shot, content constraints, company assigned to this course
   - Generates `reading_content` entry (concept_text, good_example, anti_pattern, takeaway) + `practice_scenario` entry (scenario_text, task_1–4, coach_system_prompt) as paired unit
   - Coach system prompt must include data safety guardrail
2. [ ] Run all 5 calls in parallel using `concurrent.futures.ThreadPoolExecutor`
3. [ ] Collect results; fail fast if any agent call errors (log error, exit with message)

**Verify:** Spot-check: scenario company name matches `shared_context.company_map[course_pos]` for each course.

---

### Stage 5 — Assessment Designer Agent (parallel with Stage 4)

**Context:** `scripts/generate_course_content.py`, `content/diagnostic_items.json` (schema reference)

**Steps:**

1. [ ] Implement `generate_diagnostic_items(spec_dict, shared_context) -> list[12 items]`:
   - Single Sonnet call
   - Receives all 4 domain seeds + RM diagnostic examples as few-shot
   - Generates 3 items per domain: 1 MCQ (with `options`, `correct_option`, scoring), 1 `prompt_sandbox`, 1 `micro_task`
   - All rubric criteria scores 0–1; total rubric scores to 4
2. [ ] Run in parallel with Stage 4 (same ThreadPoolExecutor pool)

**Verify:** Assert 12 items total; 3 per domain; all 3 item_types represented per domain; rubric max scores sum to 4.

---

### Stage 6 — Evaluation Designer Agent

**Context:** `scripts/generate_course_content.py`, `content/evaluation_items.json`, reading_content outputs from Stage 4

**Steps:**

1. [ ] Implement `generate_evaluation_items(course_contents, spec_dict, shared_context) -> list[20 items]`:
   - Runs after Stage 4 completes (sequential dependency)
   - Single Sonnet call
   - Receives all 5 reading_content entries + course specs as context
   - Generates 4 items per course: 3 MCQ + 1 `performance_task` with 4-key rubric (`key1`–`key4`, each 0–1)
   - MCQ options and correct_option must align with what the reading concept teaches

**Verify:** Assert 20 items total; 4 per course; `performance_task` rubric has exactly 4 keys summing to 4.

---

### Stage 7 — Final QA / Validation Agent

**Context:** `scripts/generate_course_content.py`, all prior agent outputs

**Steps:**

1. [ ] Implement `final_qa(all_outputs, shared_context) -> (passed: bool, issues: list[str])`:
   - Sonnet call with all 7 output drafts as context
   - Checks:
     - Fictional company names are consistent across reading examples, scenarios, diagnostic items
     - No company name appears in more than one course
     - All `course_id` and `domain_id` foreign key references are valid
     - All rubric scores are on 0–4 scale
     - No real EDC data, real client names, real financial figures
     - Evaluation items test what the corresponding reading concept teaches
2. [ ] If issues found: print issues to terminal, ask user to re-run (do not write partial files)
3. [ ] If passed: proceed to Stage 8

**Verify:** Test with a deliberately inconsistent output set (e.g., company name mismatch); confirm issues are caught.

---

### Stage 8 — Assemble and Write

**Context:** `scripts/generate_course_content.py`, `content/` directory

**Steps:**

1. [ ] Implement `assemble_and_write(all_outputs, content_dir)`:
   - Merge new role entries into each existing JSON file (load existing → add new entries → write back)
   - Never overwrite keys that already exist (guard: check for `role_prefix` collision before writing)
   - Write all 7 files atomically: write to temp files first, rename on success
2. [ ] Print completion summary to terminal: list of files written, entry counts added per file
3. [ ] Print next-step instruction: *"Run the seeding notebook to sync content/ to Delta tables."*

**Verify:** Confirm RM entries still intact after write; confirm new role entries present with correct key naming.

---

## Technical Implementation Details

### Databricks SDK — LLM Call Pattern

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from databricks.sdk.errors import DatabricksError

w = WorkspaceClient()  # auto-auth in VS Code + deployed App contexts

response = w.serving_endpoints.query(
    name="databricks-claude-sonnet-4-6",
    messages=[
        ChatMessage(role=ChatMessageRole.SYSTEM, content=system_prompt),
        ChatMessage(role=ChatMessageRole.USER,   content=user_prompt),
    ],
    temperature=0.7,
    max_tokens=4000,   # MUST set explicitly — default is only 1,000 tokens
)

# Extract text from response
text = response.choices[0].message.content
```

**Critical**: Databricks Foundation Model API defaults Claude to **1,000 max_tokens** if not set. Content agents generating reading concepts, scenarios, and rubrics will truncate without an explicit override.

### max_tokens Budget Per Agent

| Agent | Recommended max_tokens | Rationale |
| --- | --- | --- |
| Brief Parser (Haiku) | 2,000 | Outputs a structured dict summary, not full prose |
| Structural Generator (Haiku) | 3,000 | 3 JSON files, mostly short fields |
| QA Gap Check (Sonnet) | 2,000 | Flag list + follow-up prompt text |
| Course Content × 5 (Sonnet) | 6,000 | concept_text + good_example + anti_pattern + 4 tasks + coach prompt |
| Assessment Designer (Sonnet) | 5,000 | 12 items with rubrics |
| Evaluation Designer (Sonnet) | 6,000 | 20 items with options + rubrics |
| Final QA (Sonnet) | 2,000 | Issue list output only |

### Retry Strategy — tenacity

All LLM calls must be wrapped with tenacity retry to handle transient 429 rate-limit errors and occasional 5xx failures. Databricks pay-per-token endpoints allow ~2 requests/second per model family.

```python
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

@retry(
    wait=wait_random_exponential(min=2, max=30),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(DatabricksError),
)
def call_llm(endpoint_name, messages, temperature, max_tokens):
    return w.serving_endpoints.query(
        name=endpoint_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
```

Add `tenacity>=8.2.0` to `requirements.txt`.

### ThreadPoolExecutor — Parallel Stage Pattern

Stages 4 and 5 run 6 total Sonnet calls in parallel (5 course content + 1 assessment designer). At ~2 req/s rate limit, cap `max_workers=3` to avoid 429 cascade. Use `as_completed()` for fail-fast error handling with per-future timeout.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

PARALLEL_TIMEOUT_SECONDS = 180  # LLM content calls can take 60–120s

with ThreadPoolExecutor(max_workers=3) as executor:
    future_map = {
        executor.submit(generate_course_content, spec, shared_ctx): course_pos
        for course_pos, spec in course_specs.items()
    }
    # Add assessment designer to same pool
    diag_future = executor.submit(generate_diagnostic_items, spec_dict, shared_ctx)
    future_map[diag_future] = "diagnostics"

    results = {}
    for future in as_completed(future_map, timeout=PARALLEL_TIMEOUT_SECONDS * 2):
        key = future_map[future]
        try:
            results[key] = future.result(timeout=PARALLEL_TIMEOUT_SECONDS)
        except TimeoutError:
            print(f"ERROR: Agent for '{key}' timed out. Aborting.")
            raise SystemExit(1)
        except Exception as e:
            print(f"ERROR: Agent for '{key}' failed: {e}")
            raise SystemExit(1)
```

### JSON Output from LLM Agents

Instruct all agents to output **valid JSON only**. The system prompt for every agent must end with:

> "Return ONLY a valid JSON object inside a fenced json code block. No explanation, no surrounding text, no markdown outside the block."

Parse with:

```python
import re, json

def extract_json(raw: str) -> dict:
    match = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON block found in LLM response")
    return json.loads(match.group(1))
```

### Error Hierarchy from Databricks SDK

```python
from databricks.sdk.errors import (
    DatabricksError,   # base class
    NotFound,          # endpoint doesn't exist
    PermissionDenied,  # auth issue
    ResourceExhausted, # rate limit (429)
)
```

Catch `ResourceExhausted` specifically for rate-limit retry; catch `DatabricksError` broadly for other transient failures.

### Atomic File Write Pattern (Stage 8)

Prevent partial writes corrupting existing JSON files:

```python
import json, os, tempfile

def atomic_write_json(filepath: str, data: dict):
    dir_ = os.path.dirname(filepath)
    with tempfile.NamedTemporaryFile("w", dir=dir_, delete=False, suffix=".tmp") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        tmp_path = f.name
    os.replace(tmp_path, filepath)  # atomic on POSIX + Windows
```

### Endpoint Names (Confirmed)

Both endpoints confirmed available in workspace `adb-2717931942638877.17.azuredatabricks.net`:

| Model | Endpoint name | Use |
| --- | --- | --- |
| Claude Haiku 4.5 | `databricks-claude-haiku-4-5` | Parser, Structural Generator |
| Claude Sonnet 4.6 | `databricks-claude-sonnet-4-6` | All quality/content agents |

---

## Dependencies and Prerequisites

**New dependency — add to `requirements.txt`:**

- `tenacity>=8.2.0` — retry with exponential backoff for LLM calls

**Already in `requirements.txt`:**

- `databricks-sdk>=0.35.0` — serving endpoint calls, auth
- `python-dotenv>=1.0.0` — local `.env` loading

**Stdlib (no install needed):**

- `concurrent.futures` — ThreadPoolExecutor for parallel stages
- `json`, `re`, `os`, `tempfile`, `sys`, `argparse` — parsing, output, CLI

**Environment variables used by script:**

- `DATABRICKS_HOST` / `DATABRICKS_TOKEN` — handled by VS Code extension locally; injected by App runtime when deployed
- Script will default `SONNET_ENDPOINT` to `databricks-claude-sonnet-4-6` and `HAIKU_ENDPOINT` to `databricks-claude-haiku-4-5`; both overridable via env var

**Corp Copilot M365** — user-facing only; no programmatic dependency

---

## Open Questions

1. ~~**Haiku endpoint name**~~ — **Resolved**: `databricks-claude-haiku-4-5` confirmed available.
2. **Parallel call throttling** — **Resolved**: cap `max_workers=3` (not 6) and wrap all calls in tenacity with `wait_random_exponential(min=2, max=30)`. Benchmark on first real run; raise to 4 if latency is acceptable.
3. **Brief filepath convention** — Always require explicit CLI path for MVP (`python scripts/generate_course_content.py <brief.md>`). No default path lookup; reduces ambiguity when multiple brief files exist.
