"""
Scoring utilities: MCQ answer checking, domain score calculation, level labels.
"""

import json


LEVEL_LABELS = [
    (0.0, 0.49, "Unaware"),
    (0.5, 1.4, "Explorer"),
    (1.5, 2.4, "Practitioner"),
    (2.5, 3.4, "Proficient"),
    (3.5, 4.0, "Champion"),
]

DOMAIN_DISPLAY_NAMES = {
    "responsible_ai":      "Responsible AI",
    "strategic_prompting": "Strategic Prompting",
    "critical_eval":       "Critical Evaluation",
    "relationship_intel":  "Relationship Intelligence",
    "data_decision":       "Data-Driven Decision Making",
    "augmented_comm":      "Augmented Communication",
}

DOMAIN_IDS = [
    "responsible_ai",
    "strategic_prompting",
    "critical_eval",
    "relationship_intel",
    "data_decision",
    "augmented_comm",
]


def get_level_label(score: float) -> str:
    """Return the level label for a 0–4 score."""
    for low, high, label in LEVEL_LABELS:
        if low <= score <= high:
            return label
    if score > 4.0:
        return "Champion"
    return "Unaware"


def get_score_color(score: float) -> str:
    """Return CSS colour class based on score range."""
    if score < 1.5:
        return "danger"
    if score < 2.5:
        return "warning"
    return "success"


def score_mcq(response: str, correct_option: str, rubric: dict) -> float:
    """
    Score a single MCQ item locally (no LLM call needed).
    Returns rubric['correct'] if answer matches, else rubric['incorrect'].
    """
    if not response or not correct_option:
        return float(rubric.get("incorrect", 0))
    if response.strip().upper() == correct_option.strip().upper():
        return float(rubric.get("correct", 4))
    return float(rubric.get("incorrect", 0))


def parse_rubric(rubric_json: str) -> dict:
    """Parse a JSON rubric string into a dict."""
    if isinstance(rubric_json, dict):
        return rubric_json
    try:
        return json.loads(rubric_json)
    except (json.JSONDecodeError, TypeError):
        return {}


def parse_options(options_json: str) -> list[dict]:
    """Parse MCQ options JSON string into list of {label, text} dicts."""
    if isinstance(options_json, list):
        return options_json
    if isinstance(options_json, dict):
        return [{"label": k, "text": v} for k, v in options_json.items()]
    try:
        parsed = json.loads(options_json) if options_json else []
        if isinstance(parsed, dict):
            return [{"label": k, "text": v} for k, v in parsed.items()]
        return parsed
    except (json.JSONDecodeError, TypeError):
        return []


_DIAG_ITEMS_PER_DOMAIN = 1
_EVAL_ITEMS_PER_MODULE = 4


def compute_current_domain_scores(
    diag_domain_scores: dict,
    eval_domain_scores: list,
) -> dict:
    """
    Equal-weight domain score calculation (TDD §8).

    diag_domain_scores: {"domain_id": float}  — mean of 1 diagnostic item per domain
    eval_domain_scores: [{"domain_id": float}] — one entry per completed evaluation;
                         value is domain_score_after (mean of 4 eval items)

    Each diagnostic item and each evaluation item are weighted equally.
    Returns {"domain_id": float}
    """
    buckets: dict[str, dict] = {d: {"sum": 0.0, "count": 0} for d in DOMAIN_IDS}

    for domain_id, score in diag_domain_scores.items():
        if domain_id in buckets:
            try:
                s = float(score)
                buckets[domain_id]["sum"] += s * _DIAG_ITEMS_PER_DOMAIN
                buckets[domain_id]["count"] += _DIAG_ITEMS_PER_DOMAIN
            except (TypeError, ValueError):
                pass

    for entry in eval_domain_scores:
        for domain_id, score in entry.items():
            if domain_id in buckets:
                try:
                    s = float(score)
                    buckets[domain_id]["sum"] += s * _EVAL_ITEMS_PER_MODULE
                    buckets[domain_id]["count"] += _EVAL_ITEMS_PER_MODULE
                except (TypeError, ValueError):
                    pass

    return {
        d: round(v["sum"] / v["count"], 2) if v["count"] > 0 else 0.0
        for d, v in buckets.items()
    }



def calculate_overall_score(domain_scores: dict) -> float:
    """Average of the 6 domain scores."""
    scores = [v for v in domain_scores.values() if v is not None]
    return round(sum(scores) / len(scores), 2) if scores else 0.0
