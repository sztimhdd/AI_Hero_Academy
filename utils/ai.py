import os
import re
import time
import uuid
import json
import logging

from google import genai
from google.genai import types


def call_llm(
    messages: list[dict],
    temperature: float = 0.1,
    user_email: str = None,
    call_type: str = "unknown",
) -> str:
    """
    Call Google Gemini API.

    messages: list of {"role": "system"|"user"|"assistant", "content": "..."}
    Returns the assistant reply string.
    Logs call details to console (DB logging disabled in Phase 2).
    """
    # Model selection based on call type
    if call_type in ["coach_response"]:
        model = os.environ.get("GEMINI_FLASH_MODEL", "gemini-3-flash-preview")
    else:
        model = os.environ.get("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")

    client = genai.Client()  # Uses GOOGLE_API_KEY env var

    # Extract system instruction if present
    system_instruction = None
    user_messages = []

    for msg in messages:
        if msg["role"] == "system":
            system_instruction = msg["content"]
        else:
            user_messages.append(msg)

    # Build conversation content
    conversation_content = ""
    for msg in user_messages:
        if msg["role"] == "user":
            conversation_content += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            conversation_content += f"Assistant: {msg['content']}\n"

    # Remove trailing newline
    conversation_content = conversation_content.rstrip()

    t0 = time.time()
    try:
        config = types.GenerateContentConfig(temperature=temperature)
        if system_instruction:
            config.system_instruction = system_instruction

        resp = client.models.generate_content(
            model=model,
            contents=conversation_content,
            config=config,
        )

        content = resp.text
        latency_ms = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, model, latency_ms, success=True)
        return content
    except Exception as e:
        latency_ms = int((time.time() - t0) * 1000)
        _log_call(user_email, call_type, model, latency_ms, success=False, error=str(e))
        raise


def _log_call(user_email, call_type, model, latency_ms, success, error=None):
    """Log AI call details to console (Phase 2: DB logging disabled)."""
    log_entry = {
        "timestamp": time.time(),
        "user_email": user_email or "unknown",
        "call_type": call_type,
        "model": model,
        "latency_ms": latency_ms,
        "success": success,
        "error": str(error)[:500] if error else None
    }

    if success:
        logging.info(f"AI call successful: {call_type} via {model} ({latency_ms}ms)")
    else:
        logging.error(f"AI call failed: {call_type} via {model} - {error}")

    # TODO Phase 3: Write to Firestore ai_call_log collection


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


def _score_batch(items: list[dict], user_email: str, call_type: str) -> dict:
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
"""
    raw = call_llm(
        [{"role": "user", "content": prompt}],
        temperature=0.1,
        user_email=user_email,
        call_type=call_type,
    )
    llm_scores = _extract_json(raw)["item_scores"]
    return {**local_scores, **llm_scores}


def score_diagnostic(responses_with_rubrics: list[dict], user_email: str = None) -> dict:
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
        batch_scores = _score_batch(items, user_email, call_type="diagnostic_scoring")
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


def generate_gap_map(
    domain_scores: dict,
    domain_descriptions: dict,
    user_email: str = None,
    source_type: str = "diagnostic",
) -> list[dict]:
    """
    Generate gap map bullets from domain scores.

    domain_scores: {"prompting": 2.0, "verification": 0.8, ...}
    domain_descriptions: {"prompting": "Structuring AI prompts...", ...}

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
}}"""

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
) -> str:
    """
    Get an AI coach response for the current practice turn.

    system_prompt: course-specific coach system prompt
    conversation: prior turns [{role, content}, ...]
    user_input: the learner's latest message

    Returns the coach reply string.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        *conversation,
        {"role": "user", "content": user_input},
    ]
    return call_llm(
        messages,
        temperature=0.4,
        user_email=user_email,
        call_type="coach_response",
    )


def score_evaluation(responses_with_rubrics: list[dict], user_email: str = None) -> dict:
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
        batch_scores = _score_batch(items, user_email, call_type="evaluation_scoring")
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


def generate_module_coach_note(
    module_title: str,
    evaluation_score: float,
    domain_scores: dict,
    next_module_title: str | None,
    user_email: str = None,
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

Return only the coach note text — no JSON, no quotes."""

    return call_llm(
        [{"role": "user", "content": prompt}],
        temperature=0.5,
        user_email=user_email,
        call_type="coach_response",
    )
