#!/usr/bin/env python3
"""
Phase 3: Multi-Agent Course Content Generation Script

Accepts a Course Design Brief markdown file and produces all 7 role-specific
JSON content files via an 8-stage multi-agent pipeline.

Usage:
    python scripts/generate_course_content.py <brief_filepath>

Pipeline stages:
    Stage 1  — Brief Parser Agent (Haiku)
    Stage 2  — Structural Generator (Haiku): roles.json, domains.json, courses.json
    Stage 3  — QA Gap Check (Sonnet): quality gate; prints follow-up prompt if gaps found
    Stage 4  — Course Content Agents x5 (Sonnet, parallel): reading + practice scenario
    Stage 5  — Assessment Designer (Sonnet, parallel with Stage 4): 12 diagnostic items
    Stage 6  — Evaluation Designer (Sonnet, sequential after Stage 4): 20 eval items
    Stage 7  — Final QA Agent (Sonnet): cross-validation
    Stage 8  — Assemble & Write: merge into existing content/ JSON files atomically
"""

import argparse
import io
import json
import os
import re
import sys
import tempfile
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
    TimeoutError as FuturesTimeoutError,
)
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.config import Config as DatabricksConfig
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from databricks.sdk.errors import DatabricksError
from tenacity import (
    retry,
    wait_random_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SONNET_ENDPOINT = os.environ.get("SONNET_ENDPOINT", "databricks-claude-sonnet-4-6")
HAIKU_ENDPOINT = os.environ.get("HAIKU_ENDPOINT", "databricks-claude-haiku-4-5")
CONTENT_DIR = Path(__file__).parent.parent / "content"
PARALLEL_TIMEOUT_SECONDS = 300

DOMAIN_IDS = ["prompting", "verification", "data_safety", "tool_fluency"]

# max_tokens budget per agent (Databricks default is 1,000 — must be set explicitly)
MAX_TOKENS = {
    "parser": 6000,   # each of the 3 parallel parser calls uses this; Haiku stays within 60s timeout
    "structural": 6000,  # 4 domains × 11 level fields + 5 courses generates ~3-5k tokens
    "qa": 2000,
    "course_content": 6000,
    "assessment": 7000,   # 12 items × ~500 tokens/item; extra headroom for rubric detail
    "evaluation": 8000,   # 20 items × ~400 tokens/item; performance tasks are verbose
    "final_qa": 2000,
}

_w: WorkspaceClient | None = None


def _get_client() -> WorkspaceClient:
    global _w
    if _w is None:
        # http_timeout_seconds=300 allows Sonnet to generate 5k+ token responses
        # (default 60s triggers ReadTimeout for large assessment/evaluation outputs)
        _w = WorkspaceClient(config=DatabricksConfig(http_timeout_seconds=300))
    return _w


# ---------------------------------------------------------------------------
# LLM call helper with tenacity retry
# ---------------------------------------------------------------------------


@retry(
    wait=wait_random_exponential(min=2, max=30),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(DatabricksError),
)
def call_llm(
    endpoint_name: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 4000,
) -> str:
    """Call a Databricks serving endpoint and return the assistant reply text."""
    w = _get_client()
    messages = [
        ChatMessage(role=ChatMessageRole.SYSTEM, content=system_prompt),
        ChatMessage(role=ChatMessageRole.USER, content=user_prompt),
    ]
    response = w.serving_endpoints.query(
        name=endpoint_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def extract_json(raw: str) -> dict | list:
    """Extract and parse a JSON object/array from a ```json ... ``` fenced block.

    Handles three cases:
    1. Full fenced block:  ```json ... ```
    2. Truncated fenced block: ```json ...  (closing fence absent — common on large outputs)
    3. Raw JSON with no fences (starts with { or [)

    All cases fall back to _repair_json_with_llm (Haiku) if json.loads fails.
    """
    # Case 1: full code fence
    match = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return _repair_json_with_llm(match.group(1))

    # Case 2: opening fence present but closing fence absent (truncated output)
    fence_match = re.search(r"```json\s*(\{|\[)", raw, re.DOTALL)
    if fence_match:
        json_start = fence_match.start(1)
        candidate = raw[json_start:].strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Try lightweight structural close first; if that still fails, use LLM repair
            candidate = _close_truncated_json(candidate)
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                return _repair_json_with_llm(candidate)

    # Case 3: raw JSON with no fences
    stripped = raw.strip()
    if stripped.startswith(("{", "[")):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            return _repair_json_with_llm(stripped)

    raise ValueError(
        f"No JSON block found in LLM response. First 500 chars:\n{raw[:500]}"
    )


def _close_truncated_json(s: str) -> str:
    """Attempt to close a truncated JSON string by appending missing closing chars.

    Works by scanning the string to track open brace/bracket depth, then
    appending the necessary closing characters. Handles strings and escapes.
    Only works for simple truncation (mid-value or mid-key cuts); does not
    attempt to repair malformed JSON.
    """
    depth: list[str] = []
    in_string = False
    escaped = False

    for ch in s:
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_string:
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch in ("{", "["):
            depth.append("}" if ch == "{" else "]")
        elif ch in ("}", "]"):
            if depth:
                depth.pop()

    # Close any open string first (in case truncated mid-string)
    closing = '"' if in_string else ""
    # Close open containers in reverse order
    closing += "".join(reversed(depth))
    return s + closing


def _repair_json_with_llm(malformed: str) -> dict | list:
    """Use Haiku to fix malformed JSON. Last-resort fallback in extract_json.

    Passes the broken JSON to Haiku with a strict repair-only system prompt.
    Caps input at 16 000 chars to stay within Haiku's context window.
    """
    print("  [JSON repair] Structural fix failed — calling Haiku to repair JSON...")
    raw = call_llm(
        endpoint_name=HAIKU_ENDPOINT,
        system_prompt=(
            "You are a JSON repair tool. The user will give you a malformed or truncated "
            "JSON string. Fix ALL syntax errors — missing commas, unclosed strings, "
            "truncated values, mismatched brackets, extra trailing text — and return "
            "ONLY the repaired, complete, valid JSON. No explanation, no markdown fences, "
            "no surrounding text. The output must start with { or [."
        ),
        user_prompt=malformed[:16000],
        temperature=0.0,
        max_tokens=MAX_TOKENS["parser"],
    )
    stripped = raw.strip()
    # Haiku should return raw JSON, but handle an accidental fence just in case
    fence = re.search(r"```(?:json)?\s*([\[{])", stripped, re.DOTALL)
    if fence:
        stripped = stripped[fence.start(1):]
        # Strip closing fence if present
        stripped = re.sub(r"\s*```\s*$", "", stripped)
    return json.loads(stripped)


# ---------------------------------------------------------------------------
# Atomic file write (Stage 8)
# ---------------------------------------------------------------------------


def atomic_write_json(filepath: str, data: object) -> None:
    """Write data to filepath atomically: write temp file then rename."""
    dir_ = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(dir_, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=dir_, delete=False, suffix=".tmp", encoding="utf-8"
    ) as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        tmp_path = f.name
    os.replace(tmp_path, filepath)  # atomic on POSIX + Windows


# ---------------------------------------------------------------------------
# Stage 1 — Brief Parser Agent
# ---------------------------------------------------------------------------


def parse_brief(filepath: str) -> dict:
    """Parse the Course Design Brief markdown file and return a spec dict.

    Handles two-pass merge: if a ## SUPPLEMENTAL OUTPUT section is present,
    its fields are merged into the main spec, overwriting any gaps.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: Brief file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    raw = path.read_text(encoding="utf-8")

    # Split main body from supplemental section
    main_text, supplemental_text = _split_supplemental(raw)

    print("  Extracting spec from main brief body...")
    spec = _llm_parse_brief(main_text)

    if supplemental_text.strip():
        print("  Supplemental section detected — merging into spec...")
        supplemental_spec = _llm_parse_brief(supplemental_text)
        spec = _merge_specs(spec, supplemental_spec)

    return spec


def _split_supplemental(raw: str) -> tuple[str, str]:
    """Split brief into (main_body, supplemental_section)."""
    marker = "## SUPPLEMENTAL OUTPUT"
    idx = raw.find(marker)
    if idx == -1:
        return raw, ""
    return raw[:idx], raw[idx + len(marker):]


def _split_brief_sections(brief_text: str) -> tuple[str, str, str]:
    """Split brief text into three parts for parallel parsing.

    Returns (structural_part, scenario_reading_part, assessment_part).
    Splits on ## SECTION markers when present; falls through to full text
    for each part if markers are absent (safe for partial/supplemental briefs).
    """
    import re

    section_d_match = re.search(r"^## SECTION D[:\s]", brief_text, re.MULTILINE)
    section_f_match = re.search(r"^## SECTION F[:\s]", brief_text, re.MULTILINE)

    if section_d_match and section_f_match:
        d_start = section_d_match.start()
        f_start = section_f_match.start()
        structural_part = brief_text[:d_start]
        scenario_reading_part = brief_text[d_start:f_start]
        assessment_part = brief_text[f_start:]
    elif section_d_match:
        d_start = section_d_match.start()
        structural_part = brief_text[:d_start]
        scenario_reading_part = brief_text[d_start:]
        assessment_part = brief_text[d_start:]  # overlap is fine — missing fields return null
    elif section_f_match:
        f_start = section_f_match.start()
        structural_part = brief_text
        scenario_reading_part = brief_text[:f_start]
        assessment_part = brief_text[f_start:]
    else:
        # No section markers — send full text to each parser (handles supplemental briefs)
        structural_part = brief_text
        scenario_reading_part = brief_text
        assessment_part = brief_text

    return structural_part, scenario_reading_part, assessment_part


def _parse_structural(text: str) -> dict:
    """Haiku call: extract role/company/domain/course fields from SECTIONS A–C."""
    system_prompt = """\
You are a structured data extractor for an AI skills course design pipeline.
Extract ONLY the fields shown in the output schema from the provided brief excerpt.
For fields not found, use null. Return ONLY a valid JSON object in a ```json ``` block.

Output schema:
{
  "role_prefix": string | null,
  "role_display_name": string | null,
  "company_map": {"1": string, "2": string, "3": string, "4": string, "5": string} | null,
  "framework_names": [string, string, string, string, string] | null,
  "real_use_cases": {"1": string, "2": string, "3": string, "4": string, "5": string} | null,
  "domain_seeds": {
    "prompting": {
      "description": string,
      "level_0_label": string, "level_0_descriptor": string,
      "level_1_label": string, "level_1_descriptor": string,
      "level_2_label": string, "level_2_descriptor": string,
      "level_3_label": string, "level_3_descriptor": string,
      "level_4_label": string, "level_4_descriptor": string
    } | null,
    "verification": {same shape} | null,
    "data_safety": {same shape} | null,
    "tool_fluency": {same shape} | null
  },
  "course_seeds": {
    "1": {"title": string, "tagline": string, "description": string,
          "real_use_case": string, "primary_domain": string} | null,
    "2": {same} | null, "3": {same} | null, "4": {same} | null, "5": {same} | null
  }
}

Notes:
- role_prefix: the 2–3 letter code from the MACHINE-READABLE HEADER (e.g. "rm", "uw")
- company_map: keys are "1" through "5" (strings), values are company names
- real_use_cases: keys are "1" through "5" (strings), values are use case title strings
- domain_seeds: extract from all ### Domain: <domain_id> sections found in the brief
- course_seeds: extract from ### Course 1 — [Title] through ### Course 5 — [Title]"""

    raw = call_llm(
        endpoint_name=HAIKU_ENDPOINT,
        system_prompt=system_prompt,
        user_prompt=f"Extract structured fields from this brief excerpt:\n\n{text}",
        temperature=0.1,
        max_tokens=6000,
    )
    return extract_json(raw)


def _parse_scenarios_and_reading(text: str) -> dict:
    """Haiku call: extract scenario_seeds and reading_seeds from SECTIONS D–E."""
    system_prompt = """\
You are a structured data extractor for an AI skills course design pipeline.
Extract ONLY scenario_seeds and reading_seeds from the provided brief excerpt.
For fields not found, use null. Return ONLY a valid JSON object in a ```json ``` block.

Output schema:
{
  "scenario_seeds": {
    "1": {
      "scenario_text": string,
      "task_1_text": string,
      "task_2_text": string,
      "task_3_text": string,
      "task_4_text": string,
      "coach_system_prompt": string
    } | null,
    "2": {same shape} | null,
    "3": {same shape} | null,
    "4": {same shape} | null,
    "5": {same shape} | null
  },
  "reading_seeds": {
    "1": {
      "framework_name": string,
      "concept_text": string,
      "good_example": string,
      "anti_pattern": string,
      "takeaway": string
    } | null,
    "2": {same shape} | null,
    "3": {same shape} | null,
    "4": {same shape} | null,
    "5": {same shape} | null
  }
}

Notes:
- scenario_seeds: from ### Course N Scenario sections; keys are "1" through "5" (strings)
- reading_seeds: from ### Course N Reading sections; keys are "1" through "5" (strings)
- If a course's scenario/reading is absent, use null for that key"""

    raw = call_llm(
        endpoint_name=HAIKU_ENDPOINT,
        system_prompt=system_prompt,
        user_prompt=f"Extract scenario_seeds and reading_seeds from this brief excerpt:\n\n{text}",
        temperature=0.1,
        max_tokens=6000,
    )
    return extract_json(raw)


def _parse_assessment(text: str) -> dict:
    """Haiku call: extract diagnostic_seeds and evaluation_seeds from SECTIONS F–G."""
    system_prompt = """\
You are a structured data extractor for an AI skills course design pipeline.
Extract ONLY diagnostic_seeds and evaluation_seeds from the provided brief excerpt.
For fields not found, use null. Return ONLY a valid JSON object in a ```json ``` block.

Output schema:
{
  "diagnostic_seeds": {
    "prompting": [
      {
        "item_type": string,
        "question_text": string,
        "scenario_text": string | null,
        "options": [{"label": string, "text": string}] | null,
        "correct_option": string | null,
        "rubric_criteria": [string] | null
      }
    ] | null,
    "verification": [same item shape] | null,
    "data_safety": [same item shape] | null,
    "tool_fluency": [same item shape] | null
  },
  "evaluation_seeds": {
    "1": [
      {
        "item_type": string,
        "question_text": string,
        "scenario_text": string | null,
        "options": [{"label": string, "text": string}] | null,
        "correct_option": string | null,
        "explanation": string | null,
        "rubric_keys": [string] | null
      }
    ] | null,
    "2": [same item shape] | null,
    "3": [same item shape] | null,
    "4": [same item shape] | null,
    "5": [same item shape] | null
  }
}

Notes:
- diagnostic_seeds: from all ### Diagnostic: <domain_id> sections found in the brief
- evaluation_seeds: from ### Evaluation: Course N sections; keys are "1" through "5" (strings)
- item_type values: "MCQ", "prompt_sandbox", "micro_task", "performance_task"
- For MCQ: populate options (list of {label, text}), correct_option, explanation; rubric_criteria=null
- For prompt_sandbox/micro_task: populate question_text; options=null, correct_option=null
- If a section is absent, use null"""

    raw = call_llm(
        endpoint_name=HAIKU_ENDPOINT,
        system_prompt=system_prompt,
        user_prompt=f"Extract diagnostic_seeds and evaluation_seeds from this brief excerpt:\n\n{text}",
        temperature=0.1,
        max_tokens=6000,
    )
    return extract_json(raw)


def _llm_parse_brief(brief_text: str) -> dict:
    """Parse a Course Design Brief by splitting into 3 parallel Haiku calls.

    Splits on SECTION D / SECTION F markers so each call handles a focused
    subset of fields — keeping output well under the 6k token limit and
    within the 60s HTTP read timeout per call.
    """
    structural_text, scenario_reading_text, assessment_text = _split_brief_sections(brief_text)

    with ThreadPoolExecutor(max_workers=3) as executor:
        f_structural = executor.submit(_parse_structural, structural_text)
        f_scenarios = executor.submit(_parse_scenarios_and_reading, scenario_reading_text)
        f_assessment = executor.submit(_parse_assessment, assessment_text)

        try:
            structural_result = f_structural.result(timeout=90)
            scenarios_result = f_scenarios.result(timeout=90)
            assessment_result = f_assessment.result(timeout=90)
        except FuturesTimeoutError:
            print(
                "\n  ERROR: Brief parsing timed out (>90 s). "
                "Check network connectivity and retry."
            )
            sys.exit(1)
        except Exception as e:
            print(f"\n  ERROR: Brief parsing failed: {e}")
            sys.exit(1)

    # Merge all three dicts into one spec
    spec = {}
    spec.update(structural_result)
    spec.update({k: v for k, v in scenarios_result.items() if v is not None})
    spec.update({k: v for k, v in assessment_result.items() if v is not None})
    return spec


def _merge_specs(main: dict, supplemental: dict) -> dict:
    """Merge supplemental into main: supplemental fills null/missing values only."""
    merged = dict(main)
    for key, val in supplemental.items():
        if val is None:
            continue
        if key not in merged or merged[key] is None:
            merged[key] = val
        elif isinstance(merged[key], dict) and isinstance(val, dict):
            merged_sub = dict(merged[key])
            for sub_key, sub_val in val.items():
                if sub_val is not None and (
                    sub_key not in merged_sub or merged_sub[sub_key] is None
                ):
                    merged_sub[sub_key] = sub_val
            merged[key] = merged_sub
    return merged


# ---------------------------------------------------------------------------
# Stage 2 — Structural Generator Agent
# ---------------------------------------------------------------------------


def generate_structural_json(spec: dict) -> tuple[dict, dict]:
    """Generate roles, domains, courses JSON entries via Haiku.

    Returns (structural_outputs, shared_context).
    """
    role_prefix = (spec.get("role_prefix") or "").lower().strip()
    role_display_name = (
        spec.get("role_display_name") or role_prefix.upper() or "Unknown Role"
    )

    # Load RM examples as few-shot reference
    try:
        rm_roles = json.loads((CONTENT_DIR / "roles.json").read_text(encoding="utf-8"))
        rm_domains = json.loads((CONTENT_DIR / "domains.json").read_text(encoding="utf-8"))
        rm_courses = json.loads((CONTENT_DIR / "courses.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  WARNING: Could not load RM reference files for few-shot examples: {e}")
        print("  Run the pipeline from the project root directory (content/ must exist).")
        rm_roles, rm_domains, rm_courses = {}, {}, {}

    # Compact few-shot snippets to stay within context budget
    rm_role_ex = json.dumps({"rm": rm_roles.get("rm", {})}, indent=2)[:400]
    rm_domain_ex = json.dumps(
        {"prompting": rm_domains.get("rm_prompting", {})}, indent=2
    )[:600]
    rm_course_ex = json.dumps(
        {"rm_c1_prompting": rm_courses.get("rm_c1_prompting", {})}, indent=2
    )[:500]

    # Derive domain IDs from brief spec (fall back to RM defaults so RM still works)
    spec_domain_ids = list(spec.get("domain_seeds", {}).keys()) or DOMAIN_IDS
    spec_domains_str = ", ".join(spec_domain_ids)
    # Capstone primary_domain = first domain (closest to prompting/foundational skill)
    capstone_primary_domain = spec_domain_ids[0] if spec_domain_ids else "prompting"
    domain_entries_hint = ", ".join(f'"{d}": {{...}}' for d in spec_domain_ids)

    system_prompt = f"""\
You are a structural JSON generator for an AI skills training pipeline.
You receive a role specification and produce three JSON structures:
1. A roles.json entry for the new role
2. Four domains.json entries (one per skill domain) for the new role
3. Five courses.json entries for the new role

SCHEMAS (from existing RM data):
roles.json entry: {{"<role_id>": {{"role_id": str, "title": str, "description": str, "department": str}}}}
domains.json entry: {{"<domain_id>": {{"domain_id": str, "role_id": str, "title": str,
  "description": str, "level_0_label": str, "level_0_descriptor": str, ..., "level_4_label": str,
  "level_4_descriptor": str}}}}
courses.json entry: {{"<course_id>": {{"course_id": str, "role_id": str, "primary_domain": str,
  "title": str, "tagline": str, "description": str, "real_use_case": str, "sequence_order": int}}}}

FIXED RULES:
- role_id = "{role_prefix}"
- domain_ids for this role (from brief): {spec_domains_str}
- course_id pattern for courses 1–4: {role_prefix}_c<N>_<domain_id>
- course_id for course 5 (capstone): {role_prefix}_c5_capstone
- Course 5 primary_domain = "{capstone_primary_domain}" (capstone integrates all domains)
- sequence_order 1–5 matching course positions

RM EXAMPLES (for structural reference only — do NOT copy RM-specific content):
Role: {rm_role_ex}
Domain: {rm_domain_ex}
Course: {rm_course_ex}

Return ONLY a valid JSON object inside a fenced json code block. No text outside the block.

Output structure:
{{
  "role_entry": {{"{role_prefix}": {{...}}}},
  "domain_entries": {{{domain_entries_hint}}},
  "course_entries": {{"{role_prefix}_c1_<domain>": {{...}}, ...}}
}}"""

    user_prompt = f"""\
Generate structural JSON for:

role_prefix: {role_prefix}
role_display_name: {role_display_name}

Domain seeds (use for role-adapted descriptions and level descriptors):
{json.dumps(spec.get("domain_seeds") or {}, indent=2)}

Course seeds (use for title, tagline, description):
{json.dumps(spec.get("course_seeds") or {}, indent=2)}

real_use_cases (verbatim — use for real_use_case field in courses.json):
{json.dumps(spec.get("real_use_cases") or {}, indent=2)}

Requirements:
- Adapt ALL domain descriptions and level descriptors to this role's specific workflows and artifacts.
  Do NOT copy RM-specific language.
- All 5 course_ids must follow the pattern exactly.
- Use the real_use_case strings verbatim (from the brief — these come from the EDC use case library)."""

    raw = call_llm(
        endpoint_name=HAIKU_ENDPOINT,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.1,
        max_tokens=MAX_TOKENS["structural"],
    )
    structural = extract_json(raw)

    # Validate course_ids — abort early rather than running 4 expensive Sonnet calls
    invalid_ids = [
        cid for cid in structural.get("course_entries", {})
        if not _validate_course_id(cid, role_prefix)
    ]
    if invalid_ids:
        print(
            f"\n  ERROR: Stage 2 produced invalid course_id(s): {invalid_ids}\n"
            f"  Expected pattern: {role_prefix}_c<N>_<domain_id>\n"
            f"  Retry — Haiku occasionally formats IDs incorrectly on first attempt."
        )
        sys.exit(1)

    # Build shared_context
    course_entries = structural.get("course_entries", {})
    course_id_map: dict[int, str] = {}
    for cid, cdata in sorted(
        course_entries.items(), key=lambda x: x[1].get("sequence_order", 99)
    ):
        seq = cdata.get("sequence_order")
        if seq:
            course_id_map[seq] = cid

    # Normalize company_map and real_use_cases keys to int
    raw_company = spec.get("company_map") or {}
    company_map: dict[int, str] = {int(k): v for k, v in raw_company.items() if v}

    raw_ruc = spec.get("real_use_cases") or {}
    real_use_cases: dict[int, str] = {int(k): v for k, v in raw_ruc.items() if v}

    shared_context: dict = {
        "role_prefix": role_prefix,
        "role_display_name": role_display_name,
        "company_map": company_map,
        "framework_names": spec.get("framework_names") or [],
        "domain_ids": list(spec.get("domain_seeds", {}).keys()) or DOMAIN_IDS,
        "course_id_map": course_id_map,
        "real_use_cases": real_use_cases,
    }

    return structural, shared_context


def _validate_course_id(course_id: str, role_prefix: str) -> bool:
    pattern = rf"^{re.escape(role_prefix)}_c[1-5]_\w+$"
    return bool(re.match(pattern, course_id))


# ---------------------------------------------------------------------------
# Stage 3 — QA Gap Check Agent
# ---------------------------------------------------------------------------


def qa_gap_check(spec: dict, structural: dict) -> tuple[bool, list[dict]]:
    """Check spec completeness and content quality.

    Returns (passed, flags). If passed is False, caller should print follow-up
    prompt and exit.
    """
    flags: list[dict] = []

    # --- Structural / missing field checks (no LLM needed) ---
    if not spec.get("role_prefix"):
        flags.append(
            {
                "type": "missing",
                "field": "role_prefix",
                "message": "role_prefix is missing from the brief (Section 1 / Machine-Readable Header)",
            }
        )

    company_map = spec.get("company_map") or {}
    for i in range(1, 6):
        val = company_map.get(str(i)) or company_map.get(i)
        if not val:
            flags.append(
                {
                    "type": "missing",
                    "field": f"company_map.course_{i}",
                    "message": f"Fictional company name for Course {i} is missing",
                }
            )

    real_use_cases = spec.get("real_use_cases") or {}
    for i in range(1, 6):
        val = real_use_cases.get(str(i)) or real_use_cases.get(i)
        if not val:
            flags.append(
                {
                    "type": "missing",
                    "field": f"real_use_cases.course_{i}",
                    "message": f"real_use_case string for Course {i} is missing",
                }
            )

    domain_seeds = spec.get("domain_seeds") or {}
    for d in (list(domain_seeds.keys()) or DOMAIN_IDS):
        ds = domain_seeds.get(d)
        if not ds:
            flags.append(
                {
                    "type": "missing",
                    "field": f"domain_seeds.{d}",
                    "message": f"Domain seed for '{d}' is entirely missing",
                }
            )
        else:
            for lvl in range(5):
                if not ds.get(f"level_{lvl}_descriptor"):
                    flags.append(
                        {
                            "type": "missing",
                            "field": f"domain_seeds.{d}.level_{lvl}_descriptor",
                            "message": f"Level {lvl} descriptor missing for domain '{d}'",
                        }
                    )

    scenario_seeds = spec.get("scenario_seeds") or {}
    required = [
        "scenario_text",
        "task_1_text",
        "task_2_text",
        "task_3_text",
        "task_4_text",
    ]
    for i in range(1, 6):
        ss = scenario_seeds.get(str(i)) or scenario_seeds.get(i)
        if not ss:
            flags.append(
                {
                    "type": "missing",
                    "field": f"scenario_seeds.{i}",
                    "message": f"Scenario seed for Course {i} is entirely missing",
                }
            )
        else:
            for field in required:
                if not ss.get(field):
                    flags.append(
                        {
                            "type": "missing",
                            "field": f"scenario_seeds.{i}.{field}",
                            "message": f"Field '{field}' missing in Course {i} scenario seed",
                        }
                    )

    # If structural flags exist, skip quality check (insufficient data for LLM)
    if flags:
        return False, flags

    # --- Quality check via Sonnet ---
    quality_flags = _llm_quality_check(spec)
    flags.extend(quality_flags)

    return len(flags) == 0, flags


def _llm_quality_check(spec: dict) -> list[dict]:
    """Use Sonnet to assess quality of scenario seeds, domain descriptors, reading seeds."""
    system_prompt = """\
You are a quality assurance agent for an AI skills training content pipeline.
Assess whether a Course Design Brief meets the quality standards required for content generation.

Check for these specific quality failures:

1. SCENARIO AI_TEMPTATION SPECIFICITY
   Each scenario seed must name a specific AI tool AND a specific failure mode.
   FAIL: "use AI carelessly", "rush to use Copilot without thinking"  (too vague — no tool, no failure mode)
   PASS: "paste the full C3 client record into Copilot Chat to draft an email without abstracting
         non-public fields first"  (names tool: Copilot Chat; names failure: skipping abstraction)

2. DOMAIN DESCRIPTOR ADAPTATION
   Domain level descriptors must be adapted to THIS role's workflows and artifacts.
   They must NOT be a copy of the RM (Relationship Manager) examples.
   FAIL: Descriptors identical or near-identical to RM examples (e.g., "Writes basic prompts.
         Output often requires heavy editing.") without role-specific context.
   PASS: Descriptors that name this role's specific documents, systems, or workflows.

3. READING CONCEPT FRAMEWORK CONCRETENESS
   Each reading concept seed should name a concrete, actionable framework (acronym, checklist,
   or named multi-step process). Vague topic names are not acceptable.
   FAIL: "Understanding AI limitations", "Best practices for verification"
   PASS: "CRAF Framework", "The 4-Point Verification Checklist", "The SAFE Abstraction Sequence"

For each quality issue found, output one flag. If no issues, return empty array.

Return ONLY a valid JSON object inside a fenced json code block. No text outside the block.
Output: {"flags": [{"type": "quality", "field": "...", "message": "..."}, ...]}"""

    user_prompt = f"""\
Check the quality of this Course Design Brief spec.

Scenario seeds (check AI_temptation specificity for each course):
{json.dumps(spec.get("scenario_seeds") or {}, indent=2)[:2000]}

Domain seeds (check level descriptors are role-adapted, not RM copy):
{json.dumps(spec.get("domain_seeds") or {}, indent=2)[:2000]}

Reading seeds (check each has a concrete, named framework):
{json.dumps(spec.get("reading_seeds") or {}, indent=2)[:2000]}

Role: {spec.get("role_display_name") or spec.get("role_prefix", "unknown")}"""

    raw = call_llm(
        endpoint_name=SONNET_ENDPOINT,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.1,
        max_tokens=MAX_TOKENS["qa"],
    )
    result = extract_json(raw)
    return result.get("flags", [])


def generate_followup_prompt(flags: list[dict], brief_filepath: str) -> str:
    """Format terminal output: flag list + ready-to-paste Copilot follow-up prompt."""
    missing_flags = [f for f in flags if f["type"] == "missing"]
    quality_flags = [f for f in flags if f["type"] == "quality"]

    lines = [
        "=" * 70,
        "BRIEF QUALITY GATE — FAILED",
        "=" * 70,
        "",
        f"Brief: {brief_filepath}",
        f"Issues: {len(flags)} total  ({len(missing_flags)} missing fields, "
        f"{len(quality_flags)} quality issues)",
        "",
    ]

    if missing_flags:
        lines.append("MISSING FIELDS:")
        for f in missing_flags:
            lines.append(f"  ✗ [{f['field']}]  {f['message']}")
        lines.append("")

    if quality_flags:
        lines.append("QUALITY ISSUES:")
        for f in quality_flags:
            lines.append(f"  ⚠ [{f['field']}]  {f['message']}")
        lines.append("")

    # Build the Copilot follow-up prompt
    missing_sections = _flags_to_section_labels(flags)

    lines += [
        "=" * 70,
        "READY-TO-PASTE COPILOT FOLLOW-UP PROMPT",
        "=" * 70,
        "",
        "Copy everything between the dashed lines and paste into Corp Copilot:",
        "",
        "---",
        "The Course Design Brief you generated has the following gaps.",
        "Please provide ONLY the missing or incomplete sections listed below.",
        "Output your response under the heading:",
        "",
        "  ## SUPPLEMENTAL OUTPUT",
        "",
        "Use the same section headers and field labels as your original output.",
        "Do not re-output sections that are already complete.",
        "",
        "SECTIONS NEEDED:",
    ]
    for section in missing_sections:
        lines.append(f"  - {section}")

    lines += [
        "",
        "SPECIFIC ISSUES TO ADDRESS:",
    ]
    for f in flags:
        lines.append(f"  - {f['message']}")

    lines += [
        "---",
        "",
        "=" * 70,
        "NEXT STEPS",
        "=" * 70,
        "",
        "1. Paste the prompt above into Corp Copilot",
        "2. Append Copilot's response to the END of your brief file:",
        f"   {brief_filepath}",
        f"3. Re-run:  python scripts/generate_course_content.py {brief_filepath}",
        "",
    ]

    return "\n".join(lines)


def _flags_to_section_labels(flags: list[dict]) -> list[str]:
    """Convert flags to human-readable brief section labels for the follow-up prompt."""
    sections: set[str] = set()
    for f in flags:
        field = f.get("field", "")
        if "role_prefix" in field or "company_map" in field or "real_use_case" in field:
            sections.add("## MACHINE-READABLE HEADER")
        elif field.startswith("domain_seeds."):
            parts = field.split(".")
            domain = parts[1] if len(parts) > 1 else "all"
            sections.add(f"### Domain: {domain}")
        elif field.startswith("scenario_seeds."):
            parts = field.split(".")
            num = parts[1] if len(parts) > 1 else "N"
            sections.add(f"### Course {num} Scenario")
        elif field.startswith("reading_seeds."):
            parts = field.split(".")
            num = parts[1] if len(parts) > 1 else "N"
            sections.add(f"### Course {num} Reading")
        elif field.startswith("diagnostic_seeds."):
            parts = field.split(".")
            domain = parts[1] if len(parts) > 1 else "all"
            sections.add(f"### Diagnostic: {domain}")
        elif field.startswith("evaluation_seeds."):
            parts = field.split(".")
            num = parts[1] if len(parts) > 1 else "N"
            sections.add(f"### Evaluation: Course {num}")
    return sorted(sections)


# ---------------------------------------------------------------------------
# Stage 4 — Course Content Agent (x5, run in parallel)
# ---------------------------------------------------------------------------


def generate_course_content(
    course_pos: int, spec: dict, shared_context: dict
) -> tuple[dict, dict]:
    """Generate paired reading_content and practice_scenario for one course.

    Returns (reading_entry, scenario_entry).
    """
    course_id = shared_context["course_id_map"].get(
        course_pos, f"{shared_context['role_prefix']}_c{course_pos}"
    )
    company_name = shared_context["company_map"].get(course_pos, f"Company{course_pos} Ltd.")
    real_use_case = shared_context["real_use_cases"].get(course_pos, "")
    framework_name = (
        shared_context["framework_names"][course_pos - 1]
        if course_pos <= len(shared_context["framework_names"])
        else ""
    )

    def _get_seed(seed_dict: dict | None, pos: int) -> dict:
        if not seed_dict:
            return {}
        return seed_dict.get(str(pos)) or seed_dict.get(pos) or {}

    scenario_seed = _get_seed(spec.get("scenario_seeds"), course_pos)
    reading_seed = _get_seed(spec.get("reading_seeds"), course_pos)
    course_seed = _get_seed(spec.get("course_seeds"), course_pos)

    # Load RM few-shot examples
    try:
        rm_reading = json.loads((CONTENT_DIR / "reading_content.json").read_text(encoding="utf-8"))
        rm_scenarios = json.loads(
            (CONTENT_DIR / "practice_scenarios.json").read_text(encoding="utf-8")
        )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  WARNING: Could not load RM reading/scenario examples: {e}")
        rm_reading, rm_scenarios = {}, {}
    rm_reading_ex = json.dumps(rm_reading.get("rm_c1_prompting", {}), indent=2)[:800]
    rm_scenario_ex = json.dumps(rm_scenarios.get("rm_c1_prompting", {}), indent=2)[:800]

    system_prompt = f"""\
You are a course content author for AI Hero Academy, an AI skills training program.
You generate one paired reading module and practice scenario for a single training course.

CONTENT CONSTRAINTS (apply to every word you write):
- Fictional company assigned to this course: "{company_name}"
  — Use this company in the practice scenario. Do NOT use any real company names, real EDC
    clients, real financial figures, or any other real entities.
  — The reading module good_example and anti_pattern may use different generic fictional names.
- All tools, systems, and workflows must match this role's actual work context (not RM-specific).
- Rubric scores: each criterion scored 0–1; total must be exactly 4.
- The coach system prompt MUST include this exact instruction (adapt wording to context):
  "If the learner appears to input what looks like real client data — real company names, real
  financial figures, or verbatim confidential records — flag it immediately and instruct them
  to use only the fictional scenario data provided."

FEW-SHOT EXAMPLE (RM, Course 1 — structure only, do NOT copy RM content):
Reading content example:
{rm_reading_ex}

Practice scenario example:
{rm_scenario_ex}

Return ONLY a valid JSON object inside a fenced json code block. No text outside the block.

Output:
{{
  "reading_content": {{
    "content_id": "rc_{course_id}",
    "course_id": "{course_id}",
    "concept_text": "...",
    "good_example": "...",
    "anti_pattern": "...",
    "takeaway": "..."
  }},
  "practice_scenario": {{
    "scenario_id": "ps_{course_id}",
    "course_id": "{course_id}",
    "scenario_text": "...",
    "task_1_text": "...",
    "task_2_text": "...",
    "task_3_text": "...",
    "task_4_text": "...",
    "coach_system_prompt": "..."
  }}
}}"""

    user_prompt = f"""\
Generate course content for:

course_id: {course_id}
role: {shared_context["role_display_name"]}
fictional company (use in scenario): {company_name}
real_use_case context: {real_use_case}
framework/technique to teach: {framework_name}

Course overview:
{json.dumps(course_seed, indent=2)}

Reading concept seed:
{json.dumps(reading_seed, indent=2)}

Scenario seed:
{json.dumps(scenario_seed, indent=2)}

Write production-quality content. Requirements:
- concept_text: 150–300 words; clear teaching narrative with role-specific examples
- The framework "{framework_name}" must be the actionable centrepiece of the reading module
- good_example: show realistic before/after using this role's actual tool names
- anti_pattern: describe the exact wrong behaviour and its consequence
- practice scenario must feature "{company_name}" and progress in difficulty (task_1 = foundational, task_4 = most challenging)
- coach system prompt must include the data safety guardrail instruction
- takeaway: one practical sentence summarising the most important point"""

    raw = call_llm(
        endpoint_name=SONNET_ENDPOINT,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.7,
        max_tokens=MAX_TOKENS["course_content"],
    )
    result = extract_json(raw)
    return result["reading_content"], result["practice_scenario"]


# ---------------------------------------------------------------------------
# Stage 5 — Assessment Designer (12 diagnostic items, parallel with Stage 4)
# ---------------------------------------------------------------------------


def generate_diagnostic_items(spec: dict, shared_context: dict) -> list[dict]:
    """Generate 12 diagnostic items: 3 per domain (MCQ + prompt_sandbox + micro_task)."""
    try:
        rm_diag = json.loads(
            (CONTENT_DIR / "diagnostic_items.json").read_text(encoding="utf-8")
        )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  WARNING: Could not load RM diagnostic examples: {e}")
        rm_diag = []
    rm_diag_list = rm_diag if isinstance(rm_diag, list) else list(rm_diag.values())
    rm_diag_ex = json.dumps(rm_diag_list[:3], indent=2)[:1200]

    domain_ids = shared_context.get("domain_ids", DOMAIN_IDS)
    domain_order_hint = ", ".join(
        f"{did} (display_order {i * 3 + 1}–{i * 3 + 3})"
        for i, did in enumerate(domain_ids)
    )

    system_prompt = f"""\
You are an assessment designer for AI Hero Academy, an AI skills training program.
You generate diagnostic items that measure a learner's current AI skill level.

ITEM TYPE REQUIREMENTS:
- mcq: 4 radio options (A–D). correct_option = label (e.g., "B").
  scoring_rubric: {{"correct": 4, "incorrect": 0}}
- prompt_sandbox: Learner writes an AI prompt for a given scenario.
  scoring_rubric: {{"criteria": [{{"name": str, "description": str, "max": 1}}, ...] — exactly 4 criteria, each max 1; total = 4}}
- micro_task: Learner analyses or corrects something.
  scoring_rubric: {{"criteria": [{{"name": str, "description": str, "max": int}}, ...] — criteria sum to exactly 4}}

PER DOMAIN: exactly 3 items — Item 1 (mcq), Item 2 (prompt_sandbox), Item 3 (micro_task).

ITEM ID PATTERN: {shared_context["role_prefix"]}_diag_<abbrev><N>_<type>
  Domains for this role: {', '.join(domain_ids)}
  Use first 1–3 letters of the domain_id as abbreviation (e.g. "prompting" → "p", "risk_assessment" → "ra").
  Example pattern: {shared_context["role_prefix"]}_diag_p1_mcq, {shared_context["role_prefix"]}_diag_v2_sandbox, {shared_context["role_prefix"]}_diag_ra3_task

CONTENT CONSTRAINTS:
- Use fictional company names only. No real companies, no real EDC clients.
- Items must be grounded in THIS role's actual workflows, tools, and artifacts.
- MCQ options: one clearly correct answer + three plausible distractors.
- All rubric criterion max values must sum to exactly 4 per item.

FEW-SHOT EXAMPLE (RM role):
{rm_diag_ex}

Return ONLY a valid JSON object inside a fenced json code block. No text outside the block.

Output: {{"items": [<12 item objects>]}}
Order: {domain_order_hint}.
Each item: {{item_id, domain_id, item_type, display_order, question_text, scenario_text,
             options, correct_option, scoring_rubric}}"""

    user_prompt = f"""\
Generate 12 diagnostic items for:

role: {shared_context["role_display_name"]}
role_prefix: {shared_context["role_prefix"]}

Domain seeds (use for role-specific terminology and workflows):
{json.dumps(spec.get("domain_seeds") or {}, indent=2)[:2000]}

Scenario seeds (use for realistic context ideas — adapt to diagnostic format, do not copy verbatim):
{json.dumps(spec.get("scenario_seeds") or {}, indent=2)[:1000]}

Produce exactly 3 items per domain: 1 MCQ + 1 prompt_sandbox + 1 micro_task.
Items must test concepts genuinely relevant to this role's work, not generic AI knowledge."""

    for attempt in range(1, 4):  # up to 3 attempts
        raw = call_llm(
            endpoint_name=SONNET_ENDPOINT,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=MAX_TOKENS["assessment"],
        )
        result = extract_json(raw)
        items = result if isinstance(result, list) else result.get("items", [])
        if len(items) >= 12:
            return items
        print(
            f"  [diagnostic retry {attempt}/3] Got {len(items)} items, expected 12 — retrying..."
        )
    print(f"  WARNING: Could not generate 12 diagnostic items after 3 attempts; got {len(items)}")
    return items


# ---------------------------------------------------------------------------
# Stage 6 — Evaluation Designer (20 items, sequential after Stage 4)
# ---------------------------------------------------------------------------


def generate_evaluation_items(
    course_contents: dict[int, tuple[dict, dict]],
    spec: dict,
    shared_context: dict,
) -> list[dict]:
    """Generate 20 evaluation items: 4 per course (3 MCQ + 1 performance_task).

    Runs after Stage 4 so it can align MCQs with what the reading concepts teach.
    """
    try:
        rm_eval = json.loads(
            (CONTENT_DIR / "evaluation_items.json").read_text(encoding="utf-8")
        )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  WARNING: Could not load RM evaluation examples: {e}")
        rm_eval = {}
    rm_eval_ex_list = (
        rm_eval.get("rm_c1_prompting", [])
        if isinstance(rm_eval, dict)
        else []
    )
    rm_eval_ex = json.dumps(rm_eval_ex_list[:2], indent=2)[:1000]

    # Build compact reading summaries to feed to the evaluation designer
    reading_summaries: dict[str, dict] = {}
    for pos, (reading, _) in course_contents.items():
        cid = reading.get("course_id", shared_context["course_id_map"].get(pos, ""))
        reading_summaries[cid] = {
            "concept_text_excerpt": (reading.get("concept_text") or "")[:300],
            "takeaway": reading.get("takeaway") or "",
        }

    system_prompt = f"""\
You are an evaluation designer for AI Hero Academy, an AI skills training program.
You generate post-module quiz items that verify learners absorbed each course's reading content.

ITEM TYPE REQUIREMENTS:
- mcq (sequence 1–3): 4 options (A–D). correct_option = label.
  Must align with what the reading concept EXPLICITLY teaches.
  scoring_rubric: {{"correct": 4, "incorrect": 0}}
  Include an explanation (1–2 sentences) of why the correct option is right.
- performance_task (sequence 4): Learner writes a full response to a new scenario.
  scoring_rubric must have EXACTLY 4 keys: key1, key2, key3, key4.
  Each key describes what the response must demonstrate to earn that 1 point. Total = 4.

ITEM ID PATTERN: ev_<course_id>_q<N>  (e.g., ev_uw_c1_prompting_q1)

CONTENT CONSTRAINTS:
- MCQ options and correct_option must test application of what the reading concept teaches.
- Performance task scenario must be different from the practice scenario (new situation, same skill).
- Use fictional company names only. No real companies.
- All rubric criteria must sum to exactly 4 per item.

FEW-SHOT EXAMPLE (RM role):
{rm_eval_ex}

Return ONLY a valid JSON object inside a fenced json code block. No text outside the block.

Output: {{"items": [<20 item objects>]}}
Order: all 4 items for Course 1 first, then Course 2, ..., Course 5.
Each item: {{item_id, course_id, item_type, sequence, question_text, scenario_text,
             options, correct_option, explanation, scoring_rubric}}"""

    user_prompt = f"""\
Generate 20 evaluation items for:

role: {shared_context["role_display_name"]}
role_prefix: {shared_context["role_prefix"]}

Course ID map (sequence_order → course_id):
{json.dumps(shared_context["course_id_map"], indent=2)}

Reading content summaries (MCQs MUST test what these concepts explicitly teach):
{json.dumps(reading_summaries, indent=2)}

Company map (use these fictional companies in performance task scenarios):
{json.dumps(shared_context["company_map"], indent=2)}

Produce 4 items per course (3 MCQ + 1 performance_task).
MCQ questions must be clearly answerable from the reading content of that course.
Performance task must present a NEW scenario (different from the practice scenario)
requiring the learner to apply the full course concept from scratch."""

    for attempt in range(1, 4):  # up to 3 attempts
        raw = call_llm(
            endpoint_name=SONNET_ENDPOINT,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=MAX_TOKENS["evaluation"],
        )
        result = extract_json(raw)
        items = result if isinstance(result, list) else result.get("items", [])
        if len(items) >= 20:
            return items
        print(
            f"  [evaluation retry {attempt}/3] Got {len(items)} items, expected 20 — retrying..."
        )
    print(f"  WARNING: Could not generate 20 evaluation items after 3 attempts; got {len(items)}")
    return items


# ---------------------------------------------------------------------------
# Stage 7 — Final QA / Validation Agent
# ---------------------------------------------------------------------------


def final_qa(
    all_outputs: dict, shared_context: dict
) -> tuple[bool, list[str]]:
    """Cross-validate all outputs for consistency, correctness, and compliance.

    Returns (passed, issues). If passed is False, do not write output files.
    """
    issues: list[str] = []
    role_prefix = shared_context["role_prefix"]

    # --- Structural validation (no LLM) ---

    # Validate all course_ids
    for pos, cid in shared_context["course_id_map"].items():
        if not _validate_course_id(cid, role_prefix):
            issues.append(
                f"Invalid course_id '{cid}': does not match {role_prefix}_c<N>_<domain_id>"
            )

    # Validate company uniqueness
    seen_companies: dict[str, int] = {}
    for pos in range(1, 6):
        company = shared_context["company_map"].get(pos, "")
        if company:
            if company in seen_companies:
                issues.append(
                    f"Company '{company}' is used in both Course {seen_companies[company]}"
                    f" and Course {pos} — each course must have a unique company"
                )
            else:
                seen_companies[company] = pos

    # Validate diagnostic item count
    diag_items = all_outputs.get("diagnostic_items", [])
    if len(diag_items) != 12:
        issues.append(
            f"Expected 12 diagnostic items, got {len(diag_items)}"
        )
    else:
        domain_counts: dict[str, int] = {}
        for item in diag_items:
            d = item.get("domain_id", "unknown")
            domain_counts[d] = domain_counts.get(d, 0) + 1
        for d in shared_context.get("domain_ids", DOMAIN_IDS):
            if domain_counts.get(d, 0) != 3:
                issues.append(
                    f"Diagnostic: expected 3 items for '{d}', got {domain_counts.get(d, 0)}"
                )

    # Validate evaluation item count
    eval_items = all_outputs.get("evaluation_items", [])
    if len(eval_items) != 20:
        issues.append(f"Expected 20 evaluation items, got {len(eval_items)}")

    # Skip LLM check if there are structural failures
    if issues:
        return False, issues

    # --- LLM cross-validation ---
    llm_issues = _llm_final_qa(all_outputs, shared_context)
    issues.extend(llm_issues)

    return len(issues) == 0, issues


def _llm_final_qa(all_outputs: dict, shared_context: dict) -> list[str]:
    """Use Sonnet for content-level cross-validation."""
    # Build compact summaries
    content_summaries = []
    for pos, (reading, scenario) in all_outputs.get("course_contents", {}).items():
        content_summaries.append(
            {
                "course_pos": pos,
                "course_id": reading.get("course_id"),
                "assigned_company": shared_context["company_map"].get(pos, ""),
                "scenario_text_excerpt": (scenario.get("scenario_text") or "")[:400],
                "coach_prompt_excerpt": (scenario.get("coach_system_prompt") or "")[:600],
                "takeaway": reading.get("takeaway") or "",
            }
        )

    system_prompt = """\
You are a final QA agent for AI skills training content.
Cross-validate these outputs for compliance and quality.

Check for:
1. REAL ENTITIES: Any real company names, real EDC clients, real financial institutions,
   or real financial figures in scenario_text or coach_system_prompt excerpts.
   Only flag if you can positively identify a real entity — do NOT flag fictional names.
2. COMPANY CONSISTENCY: The assigned company for each course should appear in that course's
   scenario_text. Flag ONLY if the excerpt is ≥150 chars AND a clearly different company
   name appears in it. If the excerpt is short or the company simply is not mentioned yet,
   do NOT flag.
3. DATA SAFETY GUARDRAIL: Each coach_system_prompt excerpt should contain language about
   flagging real client data. Flag ONLY if the excerpt is ≥400 chars AND such language is
   clearly absent. Short excerpts may be cut off before that section — do NOT flag those.
4. RUBRIC SCALE: For mcq items, rubric keys 'correct' and 'incorrect' with values 4 and 0
   are correct (4 points for a right answer). Only flag if rubric values for non-mcq items
   do not sum to 4.

Return ONLY a valid JSON object inside a fenced json code block. No text outside the block.
Output: {"issues": ["description", ...]}
If no issues found: {"issues": []}"""

    eval_sample = json.dumps(
        all_outputs.get("evaluation_items", [])[:4], indent=2
    )[:1500]
    diag_sample = json.dumps(
        all_outputs.get("diagnostic_items", [])[:3], indent=2
    )[:1000]

    user_prompt = f"""\
Cross-validate:

Company assignments per course:
{json.dumps(shared_context["company_map"])}

Course content summaries (scenario + coach prompt excerpts):
{json.dumps(content_summaries, indent=2)}

Sample evaluation items (first 4):
{eval_sample}

Sample diagnostic items (first 3):
{diag_sample}"""

    raw = call_llm(
        endpoint_name=SONNET_ENDPOINT,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.1,
        max_tokens=MAX_TOKENS["final_qa"],
    )
    result = extract_json(raw)
    return result.get("issues", [])


# ---------------------------------------------------------------------------
# Stage 8 — Assemble and Write
# ---------------------------------------------------------------------------


def assemble_and_write(
    structural: dict,
    all_outputs: dict,
    shared_context: dict,
    content_dir: Path,
) -> None:
    """Merge new role entries into existing content/ JSON files and write atomically.

    Never overwrites existing role entries. Guards against role_prefix collision.
    """
    role_prefix = shared_context["role_prefix"]

    # --- Collision guard ---
    existing_roles = json.loads(
        (content_dir / "roles.json").read_text(encoding="utf-8")
    )
    if role_prefix in existing_roles:
        print(
            f"ERROR: role_prefix '{role_prefix}' already exists in roles.json.\n"
            "       Aborting to prevent overwriting existing content.",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- Prepare merged data for each file ---

    # roles.json
    new_roles = dict(existing_roles)
    new_roles.update(structural.get("role_entry", {}))

    # domains.json — Stage 2 generates flat keys ("prompting", "verification", …).
    # Prefix them with role_prefix to produce role-scoped keys ("uw_prompting", …)
    # before merging, so entries from different roles never collide.
    existing_domains = json.loads(
        (content_dir / "domains.json").read_text(encoding="utf-8")
    )
    new_domain_entries = structural.get("domain_entries", {})
    scoped_domain_entries = {
        f"{role_prefix}_{k}": v for k, v in new_domain_entries.items()
    }
    domain_collisions = [k for k in scoped_domain_entries if k in existing_domains]
    if domain_collisions:
        print(
            f"ERROR: domain key(s) {domain_collisions!r} already exist in domains.json.\n"
            f"       Role '{role_prefix}' has already been added. Aborting to prevent overwrite.",
            file=sys.stderr,
        )
        sys.exit(1)
    new_domains = dict(existing_domains)
    new_domains.update(scoped_domain_entries)

    # courses.json
    existing_courses = json.loads(
        (content_dir / "courses.json").read_text(encoding="utf-8")
    )
    new_courses = dict(existing_courses)
    new_courses.update(structural.get("course_entries", {}))

    # reading_content.json
    existing_reading = json.loads(
        (content_dir / "reading_content.json").read_text(encoding="utf-8")
    )
    new_reading = dict(existing_reading)
    for reading, _ in all_outputs["course_contents"].values():
        new_reading[reading["course_id"]] = reading

    # practice_scenarios.json
    existing_scenarios = json.loads(
        (content_dir / "practice_scenarios.json").read_text(encoding="utf-8")
    )
    new_scenarios = dict(existing_scenarios)
    for _, scenario in all_outputs["course_contents"].values():
        new_scenarios[scenario["course_id"]] = scenario

    # diagnostic_items.json (list format)
    existing_diag = json.loads(
        (content_dir / "diagnostic_items.json").read_text(encoding="utf-8")
    )
    # Inject role_id into every new diagnostic item
    new_diag_items = [
        {**item, "role_id": role_prefix} for item in all_outputs["diagnostic_items"]
    ]
    # Collision guard: skip any item whose item_id already exists
    existing_ids = {i["item_id"] for i in (existing_diag if isinstance(existing_diag, list) else existing_diag.values())}
    new_diag_items = [i for i in new_diag_items if i["item_id"] not in existing_ids]
    if isinstance(existing_diag, list):
        new_diag = existing_diag + new_diag_items
    else:
        # dict format — append as keyed entries
        new_diag = dict(existing_diag)
        for item in new_diag_items:
            new_diag[item["item_id"]] = item

    # evaluation_items.json (dict keyed by course_id)
    existing_eval = json.loads(
        (content_dir / "evaluation_items.json").read_text(encoding="utf-8")
    )
    new_eval = dict(existing_eval)
    eval_by_course: dict[str, list] = {}
    for item in all_outputs["evaluation_items"]:
        cid = item.get("course_id", "unknown")
        eval_by_course.setdefault(cid, []).append(item)
    new_eval.update(eval_by_course)

    # --- Write all 7 files atomically ---
    writes = [
        (content_dir / "roles.json", new_roles),
        (content_dir / "domains.json", new_domains),
        (content_dir / "courses.json", new_courses),
        (content_dir / "reading_content.json", new_reading),
        (content_dir / "practice_scenarios.json", new_scenarios),
        (content_dir / "diagnostic_items.json", new_diag),
        (content_dir / "evaluation_items.json", new_eval),
    ]

    for filepath, data in writes:
        atomic_write_json(str(filepath), data)

    # --- Completion summary ---
    print()
    print("=" * 60)
    print("CONTENT GENERATION COMPLETE")
    print("=" * 60)
    print(f"  Role: {shared_context['role_display_name']} ({role_prefix})")
    print()
    print(f"Files written to {content_dir}/:")
    for filepath, _ in writes:
        print(f"  ✓  {filepath.name}")
    print()
    print("Entries added:")
    print(f"  roles.json              +1  (role: {role_prefix})")
    print(f"  domains.json            +4  (all 4 domains for {role_prefix})")
    print(f"  courses.json            +5  ({role_prefix}_c1 through {role_prefix}_c5)")
    print(f"  reading_content.json    +5")
    print(f"  practice_scenarios.json +5")
    print(f"  diagnostic_items.json  +12")
    print(f"  evaluation_items.json  +20  (5 course groups)")
    print()
    print("NEXT STEP: Deploy the updated app bundle so the new content/ JSON files are served.")
    print("  bash scripts/sync_deploy.sh")
    print()


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


def main() -> None:
    # Ensure UTF-8 output on Windows (symbols like ✓ ✗ ⚠ fail in cp1252 terminal)
    if hasattr(sys.stdout, "buffer") and getattr(sys.stdout, "encoding", "utf-8").lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    cli = argparse.ArgumentParser(
        description=(
            "Generate AI Hero Academy course content from a Course Design Brief.\n"
            "Produces all 7 role-specific JSON files in content/."
        )
    )
    cli.add_argument(
        "brief_filepath",
        help="Path to the Course Design Brief markdown file",
    )
    cli.add_argument(
        "--output-dir",
        metavar="DIR",
        default=None,
        help=(
            "Write output JSON files to DIR instead of content/. "
            "Existing content/*.json files are copied to DIR first so Stage 8 "
            "can merge safely. Useful for test runs that must not touch real content."
        ),
    )
    args = cli.parse_args()

    brief_path = args.brief_filepath
    if not os.path.exists(brief_path):
        print(f"ERROR: Brief file not found: {brief_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve output directory (default: content/)
    if args.output_dir:
        import shutil as _shutil
        content_dir = Path(args.output_dir)
        content_dir.mkdir(parents=True, exist_ok=True)
        for _src in CONTENT_DIR.glob("*.json"):
            _dst = content_dir / _src.name
            if not _dst.exists():
                _shutil.copy(_src, _dst)
    else:
        content_dir = CONTENT_DIR

    print()
    print("=" * 60)
    print("AI HERO ACADEMY — Course Content Generation Pipeline")
    print("=" * 60)
    print(f"  Brief: {brief_path}")
    if args.output_dir:
        print(f"  Output: {content_dir}  (test mode — real content/ not modified)")
    print()

    # ── Stage 1: Parse brief ──────────────────────────────────────────────
    print("[Stage 1] Parsing brief...")
    spec = parse_brief(brief_path)
    role_prefix = spec.get("role_prefix") or "?"
    role_display = spec.get("role_display_name") or role_prefix.upper()
    print(f"  Role detected: {role_display} ({role_prefix})")
    company_map_display = spec.get("company_map") or {}
    print(f"  Company map: {company_map_display}")
    print()

    # ── Stage 2: Structural generator ────────────────────────────────────
    print("[Stage 2] Generating structural JSON (roles / domains / courses)...")
    structural, shared_context = generate_structural_json(spec)
    print(f"  course_id_map: {shared_context['course_id_map']}")
    print()

    # ── Stage 3: QA gap check ─────────────────────────────────────────────
    print("[Stage 3] Running QA gap check...")
    passed, flags = qa_gap_check(spec, structural)
    if not passed:
        followup = generate_followup_prompt(flags, brief_path)
        print(followup)
        sys.exit(0)
    print("  ✓ QA gap check PASSED — proceeding to content generation")
    print()

    # ── Stages 4 + 5: Parallel content generation ────────────────────────
    print("[Stage 4+5] Generating course content + diagnostic items in parallel...")
    print(f"  Agents: 5 course content (Sonnet) + 1 assessment designer (Sonnet)")
    print(f"  max_workers=3 (rate-limit safe at ~2 req/s)")
    print()

    course_contents: dict[int, tuple[dict, dict]] = {}
    diagnostic_items: list[dict] = []

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_map: dict = {}

            # Submit 5 course content agents
            for pos in range(1, 6):
                f = executor.submit(generate_course_content, pos, spec, shared_context)
                future_map[f] = pos
                cid = shared_context["course_id_map"].get(pos, f"course_{pos}")
                company = shared_context["company_map"].get(pos, "?")
                print(f"  → Submitted: Course {pos} — {cid}  [{company}]")

            # Submit assessment designer
            diag_future = executor.submit(generate_diagnostic_items, spec, shared_context)
            future_map[diag_future] = "diagnostics"
            print(f"  → Submitted: Diagnostic items (12 items)")
            print()

            for future in as_completed(future_map, timeout=PARALLEL_TIMEOUT_SECONDS * 2):
                key = future_map[future]
                try:
                    result = future.result(timeout=PARALLEL_TIMEOUT_SECONDS)
                    if key == "diagnostics":
                        diagnostic_items = result
                        print(f"  ✓ Diagnostic items done  ({len(result)} items)")
                    else:
                        course_contents[key] = result
                        reading, _ = result
                        print(
                            f"  ✓ Course {key} done  "
                            f"({reading.get('content_id', shared_context['course_id_map'].get(key, ''))})"
                        )
                except FuturesTimeoutError:
                    print(
                        f"\nERROR: Agent for '{key}' timed out "
                        f"({PARALLEL_TIMEOUT_SECONDS}s). Aborting.",
                        file=sys.stderr,
                    )
                    raise SystemExit(1)
                except Exception as exc:
                    print(
                        f"\nERROR: Agent for '{key}' failed: {exc}", file=sys.stderr
                    )
                    raise SystemExit(1)
    except FuturesTimeoutError:
        # as_completed(timeout=...) raises TimeoutError at the iterator level (not inside the loop)
        print(
            f"\nERROR: Parallel agent pool timed out after {PARALLEL_TIMEOUT_SECONDS * 2}s. "
            "Not all agents completed. Aborting.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print()

    # ── Stage 6: Evaluation designer (sequential — needs Stage 4 output) ──
    print("[Stage 6] Generating evaluation items (sequential; uses Stage 4 reading content)...")
    evaluation_items = generate_evaluation_items(course_contents, spec, shared_context)
    print(f"  ✓ Evaluation items done  ({len(evaluation_items)} items)")
    print()

    # ── Stage 7: Final QA ─────────────────────────────────────────────────
    all_outputs = {
        "course_contents": course_contents,
        "diagnostic_items": diagnostic_items,
        "evaluation_items": evaluation_items,
    }
    print("[Stage 7] Running final QA / cross-validation...")
    qa_passed, qa_issues = final_qa(all_outputs, shared_context)
    if not qa_passed:
        print()
        print("=" * 60)
        print("FINAL QA FAILED — output files NOT written")
        print("=" * 60)
        print("Issues found:")
        for issue in qa_issues:
            print(f"  ✗ {issue}")
        print()
        print("Fix the issues above and re-run:")
        print(f"  python scripts/generate_course_content.py {brief_path}")
        sys.exit(1)
    print("  ✓ Final QA passed")
    print()

    # ── Stage 8: Assemble and write ───────────────────────────────────────
    print(f"[Stage 8] Writing output files to {content_dir}...")
    assemble_and_write(structural, all_outputs, shared_context, content_dir)


if __name__ == "__main__":
    main()
