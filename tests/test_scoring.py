"""
Tests for utils/scoring.py — 6-domain model.
"""

import pytest
from utils.scoring import (
    DOMAIN_IDS,
    DOMAIN_DISPLAY_NAMES,
    get_level_label,
    calculate_domain_scores,
    calculate_overall_score,
    compute_current_domain_scores,
)

NEW_DOMAIN_IDS = [
    "responsible_ai",
    "strategic_prompting",
    "critical_eval",
    "relationship_intel",
    "data_decision",
    "augmented_comm",
]


# ── Domain model constants ────────────────────────────────────────────────────


def test_domain_ids_count():
    assert len(DOMAIN_IDS) == 6


def test_domain_ids_values():
    assert DOMAIN_IDS == NEW_DOMAIN_IDS


def test_domain_display_names_keys_match_ids():
    assert set(DOMAIN_DISPLAY_NAMES.keys()) == set(DOMAIN_IDS)


def test_domain_display_names_values_nonempty():
    for did, label in DOMAIN_DISPLAY_NAMES.items():
        assert label, f"Empty display name for domain {did!r}"


# ── Level label ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("score,expected_label", [
    (0.0, "Unaware"),
    (0.49, "Unaware"),
    (0.5, "Explorer"),
    (1.4, "Explorer"),
    (1.5, "Practitioner"),
    (2.4, "Practitioner"),
    (2.5, "Proficient"),
    (3.4, "Proficient"),
    (3.5, "Champion"),
    (4.0, "Champion"),
])
def test_get_level_label(score, expected_label):
    assert get_level_label(score) == expected_label


# ── calculate_domain_scores ───────────────────────────────────────────────────


def _make_item(domain_id: str, item_type: str, response, rubric: dict) -> dict:
    return {
        "item_id": f"test_{domain_id}",
        "domain_id": domain_id,
        "item_type": item_type,
        "response": response,
        "correct_option": "A" if item_type == "mcq" else None,
        "scoring_rubric": rubric,
    }


def test_calculate_domain_scores_returns_all_6_domains():
    # Signature: (diag_item_scores, diag_item_domains, eval_scores_by_module)
    item_scores = {f"item_{d}": 4.0 for d in DOMAIN_IDS}
    item_domains = {f"item_{d}": d for d in DOMAIN_IDS}
    result = calculate_domain_scores(item_scores, item_domains, [])
    assert set(result.keys()) == set(DOMAIN_IDS)


def test_calculate_domain_scores_correct_average():
    item_scores = {"item_ra_1": 4.0, "item_ra_2": 2.0}
    item_domains = {"item_ra_1": "responsible_ai", "item_ra_2": "responsible_ai"}
    result = calculate_domain_scores(item_scores, item_domains, [])
    assert result["responsible_ai"] == pytest.approx(3.0)
    # Domains with no items return 0.0
    for d in DOMAIN_IDS[1:]:
        assert result[d] == pytest.approx(0.0)


# ── calculate_overall_score ───────────────────────────────────────────────────


def test_calculate_overall_score_averages_6_domains():
    scores = {d: 2.0 for d in DOMAIN_IDS}
    assert calculate_overall_score(scores) == pytest.approx(2.0)


def test_calculate_overall_score_mixed():
    scores = {d: float(i) for i, d in enumerate(DOMAIN_IDS)}
    expected = sum(range(6)) / 6
    assert calculate_overall_score(scores) == pytest.approx(expected, abs=0.01)


# ── compute_current_domain_scores ────────────────────────────────────────────


def test_compute_current_domain_scores_uses_diag_only():
    diag = {d: 1.5 for d in DOMAIN_IDS}
    result = compute_current_domain_scores(diag, [])
    assert set(result.keys()) == set(DOMAIN_IDS)
    assert all(v == pytest.approx(1.5) for v in result.values())


def test_compute_current_domain_scores_eval_updates_domain():
    diag = {d: 1.5 for d in DOMAIN_IDS}
    eval_scores = [{"responsible_ai": 3.0}]
    result = compute_current_domain_scores(diag, eval_scores)
    # responsible_ai score should reflect the new eval input
    assert result["responsible_ai"] != pytest.approx(1.5)
