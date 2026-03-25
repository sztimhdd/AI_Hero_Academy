import json
import os
import re
import time
import uuid

from google import genai
from google.genai import types
from utils.db import log_ai_call


def call_llm(
    messages: list[dict],
    temperature: float = 0.1,
    user_email: str = None,
    call_type: str = "unknown",
) -> str:
    """
    Call the Gemini API (gemini-2.0-flash).

    messages: list of {"role": "system"|"user"|"assistant", "content": "..."}
    Returns the assistant reply string.
    Always writes one entry to Firestore ai_call_log.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash"

    # Extract system instruction (first system message, if any)
    system_instruction = None
    conversation = []
    for m in messages:
        if m["role"] == "system" and system_instruction is None:
            system_instruction = m["content"]
        else:
            # Map "assistant" → "model" for Gemini
            role = "model" if m["role"] == "assistant" else m["role"]
            conversation.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )

    t0 = time.time()
    try:
        response = client.models.generate_content(
            model=model,
            contents=conversation,
            config=config,
        )
        content = response.text
        latency_ms = int((time.time() - t0) * 1000)
        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", None)
        completion_tokens = getattr(usage, "candidates_token_count", None)
        _log_call(user_email, call_type, model, latency_ms, success=True,
                  prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
        return content
    except Exception as e:
        latency_ms = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, model, latency_ms, success=False, error=str(e))
        raise


def _log_call(user_email, call_type, endpoint, latency_ms, success, error=None,
              prompt_tokens=None, completion_tokens=None):
    """Write one entry to Firestore ai_call_log. Silently ignore log failures."""
    log_ai_call({
        "log_id": str(uuid.uuid4()),
        "user_email": user_email or "",
        "call_type": call_type,
        "model_endpoint": endpoint,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "latency_ms": latency_ms,
        "success": success,
        "error_message": str(error)[:500] if error else None,
    })


_LANG_INSTRUCTION: dict[str, str] = {
    "zh": (
        "\n\nIMPORTANT: All your responses MUST be written entirely in Simplified Chinese "
        "(简体中文). Do not use English except for: framework acronyms (SAFE, CRAF, VERIFY, "
        "TRACE, STAKE), fictional company names (Meridian, Aurora, Crestwood, Apex, etc.), "
        "and JSON field names. Maintain a professional financial services tone."
    )
}


def _lang_instruction(lang: str) -> str:
    return _LANG_INSTRUCTION.get(lang, "")


def _extract_json(raw: str) -> dict:
    """Strip markdown fences and parse JSON. Raises ValueError with useful message on failure."""
    raw = raw.strip()
    # Handle ```json or ``` fences
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:]).strip()
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0].strip()
    if not raw:
        raise ValueError("LLM returned an empty response. Please try again.")
    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # Fallback: extract the first {...} block (handles preamble text before JSON)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError(f"LLM response was not valid JSON. Preview: {raw[:300]}")


def _score_batch(items: list[dict], user_email: str, call_type: str, lang: str = "en") -> dict:
    """
    Score a batch of items and return item_scores dict.
    MCQ items are scored locally (deterministic). Only open-ended items go to the LLM.
    """
    from utils.scoring import score_mcq

    local_scores: dict[str, float] = {}
    llm_items: list[dict] = []

    for item in items:
        if item.get("item_type") == "mcq":
            rubric = item.get("scoring_rubric") or {"correct": 4, "incorrect": 0}
            local_scores[item["item_id"]] = score_mcq(
                item.get("response", ""),
                item.get("correct_option"),
                rubric,
            )
        else:
            llm_items.append(item)

    if not llm_items:
        return local_scores

    payload = json.dumps(llm_items, ensure_ascii=False)
    prompt = f"""You are a scoring engine. Score the learner responses below against the rubrics provided.
Return ONLY valid JSON — no explanation, no markdown fences.

RESPONSES AND RUBRICS:
{payload}

Return exactly:
{{"item_scores": {{"<item_id>": <score_float>, ...}}}}

Rules:
- Each score is on a 0.0–4.0 scale.
- For open-ended items (prompt_sandbox, micro_task, performance_task): score each rubric criterion 0 to its max value, sum them, then scale the total to 0.0–4.0 by dividing by the sum of all max values and multiplying by 4.
{_lang_instruction(lang)}"""
    raw = call_llm(
        [{"role": "user", "content": prompt}],
        temperature=0.1,
        user_email=user_email,
        call_type=call_type,
    )
    llm_scores = _extract_json(raw)["item_scores"]
    return {**local_scores, **llm_scores}


def score_diagnostic(responses_with_rubrics: list[dict], user_email: str = None, lang: str = "en") -> dict:
    """
    Score all diagnostic responses by batching per domain (one LLM call per domain).

    responses_with_rubrics: list of {
        "item_id": str,
        "domain_id": str,
        "item_type": str,
        "response": str,
        "correct_option": str | None,   # for MCQ
        "scoring_rubric": dict,
    }

    Returns: {
        "item_scores": {"item_id": float, ...},
        "domain_scores": {"domain_id": float, ...},
        "overall_score": float,
    }
    """
    # Group items by domain
    by_domain: dict[str, list] = {}
    for item in responses_with_rubrics:
        by_domain.setdefault(item["domain_id"], []).append(item)

    all_item_scores: dict[str, float] = {}

    # Score each domain in a separate LLM call (avoids token-limit issues)
    for domain_id, items in by_domain.items():
        batch_scores = _score_batch(items, user_email, call_type="diagnostic_scoring", lang=lang)
        all_item_scores.update(batch_scores)

    # Compute domain scores
    domain_scores: dict[str, float] = {}
    for domain_id, items in by_domain.items():
        scores = [all_item_scores.get(i["item_id"], 0.0) for i in items]
        domain_scores[domain_id] = round(sum(scores) / len(scores), 4) if scores else 0.0

    overall_score = round(sum(domain_scores.values()) / len(domain_scores), 4) if domain_scores else 0.0

    return {
        "item_scores": all_item_scores,
        "domain_scores": domain_scores,
        "overall_score": overall_score,
    }


_BYOW_SCORER_SYSTEM = """\
You are an AI skills assessor scoring a professional's self-reported diagnostic responses.

Score each response 0–4 using the rubric provided per item.
Return ONLY valid JSON: {"scores": {"<item_id>": <float>, ...}}

Calibration guide:
- 0: No answer, irrelevant, or actively wrong
- 1.0–1.4: Vague awareness, no concrete action
- 1.5–2.4: Basic practical use, some structure (most first-time users)
- 2.5–3.4: Structured approach with specifics, demonstrates real usage
- 3.5–4.0: Mastery — systematic, verified, role-appropriate (rare)

Do not reward length. Reward specificity and structured thinking.\
"""


def score_byow_diagnostic(
    responses: list[dict],
    user_email: str = None,
    lang: str = "en",
) -> dict:
    """
    Score 6 BYOW open-ended diagnostic responses in a single LLM call.

    responses: list of {
        "item_id": str,
        "domain_id": str,
        "prompt_text": str,
        "response_text": str,
        "scoring_rubric": dict,  # {"4": "...", "3": "...", ...}
    }

    Returns same shape as score_diagnostic():
        {
            "item_scores":   {"byow_responsible_ai_1": float, ...},
            "domain_scores": {"responsible_ai": float, ...},
            "overall_score": float,
        }
    """
    blocks = []
    for r in responses:
        rubric = r["scoring_rubric"]
        rubric_str = " | ".join(f"{k}={v}" for k, v in rubric.items())
        blocks.append(
            f"ITEM: {r['item_id']} (Domain: {r['domain_id']})\n"
            f"QUESTION: {r['prompt_text']}\n"
            f"RESPONSE: {r['response_text']}\n"
            f"RUBRIC: {rubric_str}"
        )
    user_prompt = "\n\n".join(blocks)

    raw = call_llm(
        [
            {"role": "system", "content": _BYOW_SCORER_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        user_email=user_email,
        call_type="byow_diagnostic_scoring",
    )

    parsed = _extract_json(raw)
    raw_scores: dict = parsed.get("scores", {})

    item_scores: dict[str, float] = {}
    for r in responses:
        raw_val = raw_scores.get(r["item_id"], 1.0)
        item_scores[r["item_id"]] = round(min(max(float(raw_val), 0.0), 4.0), 4)

    domain_scores: dict[str, float] = {}
    for r in responses:
        domain_scores[r["domain_id"]] = item_scores[r["item_id"]]

    overall_score = round(sum(domain_scores.values()) / len(domain_scores), 4) if domain_scores else 0.0

    return {
        "item_scores": item_scores,
        "domain_scores": domain_scores,
        "overall_score": overall_score,
    }


def generate_gap_map(
    domain_scores: dict,
    domain_descriptions: dict,
    user_email: str = None,
    source_type: str = "diagnostic",
    lang: str = "en",
) -> list[dict]:
    """
    Generate gap map bullets from domain scores.

    domain_scores: {"responsible_ai": 2.0, "strategic_prompting": 0.8, ...}
    domain_descriptions: {"responsible_ai": "Applying AI usage policies...", ...}

    Returns list of {"priority": int, "domain_id": str, "bullet": str}
    """
    scores_text = json.dumps(domain_scores, ensure_ascii=False, indent=2)
    descs_text = json.dumps(domain_descriptions, ensure_ascii=False, indent=2)

    prompt = f"""You are a learning coach generating a personalized gap analysis for a learner at a Canadian export finance institution.

Domain scores (0–4 scale, where 0=Unaware and 4=Champion):
{scores_text}

Domain descriptions:
{descs_text}

Write 3–6 gap bullets. Order by priority (biggest gap = priority 1, i.e. lowest score first).
Each bullet must be:
- Specific and actionable (reference the actual domain context from the descriptions above)
- Encouraging and growth-focused — not punitive
- 1–2 sentences

Return ONLY valid JSON:
{{
  "gap_bullets": [
    {{"priority": 1, "domain_id": "...", "bullet": "..."}},
    ...
  ]
}}{_lang_instruction(lang)}"""

    raw = call_llm(
        [{"role": "user", "content": prompt}],
        temperature=0.4,
        user_email=user_email,
        call_type="gap_map",
    )

    result = _extract_json(raw)
    # Accept both "gap_bullets" and "bullets" in case the LLM varies the key name
    bullets = result.get("gap_bullets") or result.get("bullets") or []
    return bullets if isinstance(bullets, list) else []


def coach_response(
    system_prompt: str,
    conversation: list[dict],
    user_input: str,
    user_email: str = None,
    lang: str = "en",
) -> str:
    """
    Get an AI coach response for the current practice turn.

    system_prompt: course-specific coach system prompt
    conversation: prior turns [{role, content}, ...]
    user_input: the learner's latest message

    Returns the coach reply string.
    """
    messages = [
        {"role": "system", "content": system_prompt + _lang_instruction(lang)},
        *conversation,
        {"role": "user", "content": user_input},
    ]
    return call_llm(
        messages,
        temperature=0.4,
        user_email=user_email,
        call_type="coach_response",
    )


def score_evaluation(responses_with_rubrics: list[dict], user_email: str = None, lang: str = "en") -> dict:
    """
    Score evaluation quiz responses. Mirrors score_diagnostic: MCQ scored locally,
    open-ended via LLM (one call per domain), aggregates computed in Python.

    Returns: {
        "item_scores": {"item_id": float, ...},
        "domain_scores": {"domain_id": float, ...},
        "overall_score": float,
    }
    """
    # Group items by domain (evaluation items all share primary_domain in practice,
    # but handle the general case for robustness)
    by_domain: dict[str, list] = {}
    for item in responses_with_rubrics:
        by_domain.setdefault(item["domain_id"], []).append(item)

    all_item_scores: dict[str, float] = {}

    for domain_id, items in by_domain.items():
        batch_scores = _score_batch(items, user_email, call_type="evaluation_scoring", lang=lang)
        all_item_scores.update(batch_scores)

    # Compute domain scores in Python (equal weight per item)
    domain_scores: dict[str, float] = {}
    for domain_id, items in by_domain.items():
        scores = [all_item_scores.get(i["item_id"], 0.0) for i in items]
        domain_scores[domain_id] = round(sum(scores) / len(scores), 4) if scores else 0.0

    overall_score = round(sum(domain_scores.values()) / len(domain_scores), 4) if domain_scores else 0.0

    return {
        "item_scores": all_item_scores,
        "domain_scores": domain_scores,
        "overall_score": overall_score,
    }


_MCQ_DOMAINS = ["responsible_ai", "data_decision", "relationship_intel", "augmented_comm"]

_MCQ_GENERATOR_SYSTEM = """\
You are an AI skills assessor. Generate exactly 4 multiple-choice questions to assess a professional's
AI skills across 4 specific domains. Use their two text answers and role profile to make the questions
feel tailored to their actual work context.

Return ONLY valid JSON — no markdown fences, no explanation.

Format:
[
  {
    "domain_id": "<domain_id>",
    "question_text": "<question>",
    "options": [
      {"label": "A", "text": "<option text>", "score": <0.0|1.5|2.5|4.0>},
      {"label": "B", "text": "<option text>", "score": <0.0|1.5|2.5|4.0>},
      {"label": "C", "text": "<option text>", "score": <0.0|1.5|2.5|4.0>},
      {"label": "D", "text": "<option text>", "score": <0.0|1.5|2.5|4.0>}
    ]
  },
  ...
]

Rules:
- Exactly 4 items, one per domain_id in this order: responsible_ai, data_decision, relationship_intel, augmented_comm
- Each item has exactly 4 options labeled A, B, C, D
- Scores: one option scores 4.0, one scores 2.5, one scores 1.5, one scores 0.0 (in any order)
- Questions should reference the learner's work context where natural
- Options should be plausible and avoid obviously wrong answers\
"""


def generate_diagnostic_mcqs(
    q1_text: str,
    q2_text: str,
    intake_profile: dict,
    user_email: str = None,
    lang: str = "en",
) -> list[dict]:
    """
    Generate 4 personalized MCQ questions (one per MCQ domain) based on the learner's
    two open-ended text answers and their role intake profile.

    Returns a list of 4 MCQ dicts. Falls back to content/diagnostic_prompts.json
    fallback_mcqs on any error — never raises to the caller.
    """
    import json as _json
    from pathlib import Path

    def _load_fallback() -> list[dict]:
        try:
            data = _json.loads(Path("content/diagnostic_prompts.json").read_text(encoding="utf-8"))
            # Support both {"prompts":[], "fallback_mcqs":[]} and legacy bare list
            if isinstance(data, dict):
                return data.get("fallback_mcqs", [])
            return []
        except Exception:
            return []

    role_context = ""
    if intake_profile:
        role_text = intake_profile.get("role_text") or intake_profile.get("role_id", "")
        daily_tasks = intake_profile.get("daily_tasks", "")
        if role_text:
            role_context = f"Role: {role_text}\n"
        if daily_tasks:
            role_context += f"Daily work: {daily_tasks}\n"

    user_prompt = (
        f"{role_context}\n"
        f"Text Answer 1 (strategic prompting): {q1_text}\n\n"
        f"Text Answer 2 (critical evaluation): {q2_text}\n\n"
        f"Generate 4 MCQ questions for domains: {', '.join(_MCQ_DOMAINS)}"
        f"{_lang_instruction(lang)}"
    )

    try:
        raw = call_llm(
            [
                {"role": "system", "content": _MCQ_GENERATOR_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            user_email=user_email,
            call_type="mcq_generation",
        )
        # Strip markdown fences
        raw = raw.strip()
        if raw.startswith("```"):
            raw = "\n".join(raw.split("\n")[1:]).strip()
        if raw.endswith("```"):
            raw = raw.rsplit("```", 1)[0].strip()
        mcqs = json.loads(raw)

        # Validate structure
        if (
            not isinstance(mcqs, list)
            or len(mcqs) != 4
            or not all(
                isinstance(m, dict)
                and m.get("domain_id") in _MCQ_DOMAINS
                and isinstance(m.get("options"), list)
                and len(m["options"]) == 4
                and all(o.get("score") in (0.0, 1.5, 2.5, 4.0) for o in m["options"])
                for m in mcqs
            )
        ):
            raise ValueError("MCQ validation failed")

        return mcqs
    except Exception:
        return _load_fallback()


def score_hybrid_diagnostic(
    q1_text: str,
    q2_text: str,
    mcq_answers: dict,
    intake_profile: dict,
    user_email: str = None,
    lang: str = "en",
) -> dict:
    """
    Score the hybrid diagnostic: 2 open-ended text answers + 4 MCQ answers.

    mcq_answers: {domain_id: score_float} for the 4 MCQ domains

    Returns:
        {
            "item_scores":   {"sp_q1": float, "ce_q2": float, ...mcq_items...},
            "domain_scores": {domain_id: float, ...},
            "overall_score": float,
        }
    """
    from pathlib import Path as _Path
    import json as _json

    _raw = _json.loads(_Path("content/diagnostic_prompts.json").read_text(encoding="utf-8"))
    _prompt_list = _raw.get("prompts", _raw) if isinstance(_raw, dict) else _raw
    _sp_prompt = next((p for p in _prompt_list if isinstance(p, dict) and p.get("domain_id") == "strategic_prompting"), {})
    _ce_prompt = next((p for p in _prompt_list if isinstance(p, dict) and p.get("domain_id") == "critical_eval"), {})

    text_responses = [
        {
            "item_id": "hybrid_strategic_prompting",
            "domain_id": "strategic_prompting",
            "prompt_text": _sp_prompt.get("prompt_text", "Describe how you would use AI for a work task."),
            "response_text": q1_text,
            "scoring_rubric": _sp_prompt.get("scoring_rubric", {"4": "Specific structured prompt", "0": "No answer"}),
        },
        {
            "item_id": "hybrid_critical_eval",
            "domain_id": "critical_eval",
            "prompt_text": _ce_prompt.get("prompt_text", "What do you check before using AI output?"),
            "response_text": q2_text,
            "scoring_rubric": _ce_prompt.get("scoring_rubric", {"4": "Systematic verification", "0": "No answer"}),
        },
    ]

    text_result = score_byow_diagnostic(text_responses, user_email=user_email, lang=lang)

    # Merge: text domain scores + MCQ domain scores
    domain_scores = {**text_result["domain_scores"], **mcq_answers}
    overall_score = round(sum(domain_scores.values()) / len(domain_scores), 4) if domain_scores else 0.0

    # Build item_scores including MCQ items
    item_scores = {**text_result["item_scores"]}
    for domain_id, score in mcq_answers.items():
        item_scores[f"mcq_{domain_id}"] = score

    return {
        "item_scores": item_scores,
        "domain_scores": domain_scores,
        "overall_score": overall_score,
    }


def generate_module_coach_note(
    module_title: str,
    evaluation_score: float,
    domain_scores: dict,
    next_module_title: str | None,
    user_email: str = None,
    lang: str = "en",
) -> str:
    """
    Generate a 1–2 sentence personalised coach note for the module results screen.
    """
    prompt = f"""You are an encouraging AI learning coach for an RM skills training program.

The learner just completed: "{module_title}"
Their evaluation score: {evaluation_score:.1f} / 4.0
Domain scores from this module: {json.dumps(domain_scores)}
{"Next module: " + next_module_title if next_module_title else "This was the final module."}

Write a 1–2 sentence coach note that:
- Is specific to their score and the module content
- Is encouraging and forward-looking
- If there is a next module, hints at what skill it will build
- Uses second person ("You")

Return only the coach note text — no JSON, no quotes.{_lang_instruction(lang)}"""

    return call_llm(
        [{"role": "user", "content": prompt}],
        temperature=0.5,
        user_email=user_email,
        call_type="module_coach_note",
    )
