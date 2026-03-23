"""
Tests for utils/sequencing.py — 6-domain / 7-course model.
"""

import pytest
from utils.sequencing import compute_module_sequence, DOMAIN_TO_COURSE, CAPSTONE_COURSE_ID

DOMAIN_IDS = [
    "responsible_ai",
    "strategic_prompting",
    "critical_eval",
    "relationship_intel",
    "data_decision",
    "augmented_comm",
]


def _make_scores(**overrides) -> dict:
    """Return a 6-domain score dict with a default score of 1.5, overridden per kwarg."""
    base = {d: 1.5 for d in DOMAIN_IDS}
    base.update(overrides)
    return base


# ── Course map constants ──────────────────────────────────────────────────────


def test_domain_to_course_has_all_roles():
    for role in ("rm", "uw", "an", "mk"):
        assert role in DOMAIN_TO_COURSE, f"Missing role {role!r} in DOMAIN_TO_COURSE"
        assert role in CAPSTONE_COURSE_ID, f"Missing role {role!r} in CAPSTONE_COURSE_ID"


def test_domain_to_course_has_6_domains_per_role():
    for role in ("rm", "uw", "an", "mk"):
        assert len(DOMAIN_TO_COURSE[role]) == 6, f"Expected 6 domains for {role!r}"


def test_capstone_course_id_correct():
    assert CAPSTONE_COURSE_ID["rm"] == "rm_c7_capstone"
    assert CAPSTONE_COURSE_ID["uw"] == "uw_c7_capstone"


# ── Sequence length and structure ────────────────────────────────────────────


def test_sequence_length_is_7_for_rm():
    seq = compute_module_sequence(_make_scores(), "rm")
    assert len(seq) == 7


def test_sequence_length_is_7_for_uw():
    seq = compute_module_sequence(_make_scores(), "uw")
    assert len(seq) == 7


def test_capstone_always_last_rm():
    seq = compute_module_sequence(_make_scores(), "rm")
    assert seq[-1] == "rm_c7_capstone"


def test_capstone_always_last_uw():
    seq = compute_module_sequence(_make_scores(), "uw")
    assert seq[-1] == "uw_c7_capstone"


def test_all_course_ids_are_rm_prefixed():
    seq = compute_module_sequence(_make_scores(), "rm")
    for cid in seq:
        assert cid.startswith("rm_"), f"Unexpected course_id {cid!r} for rm role"


def test_all_course_ids_are_uw_prefixed():
    seq = compute_module_sequence(_make_scores(), "uw")
    for cid in seq:
        assert cid.startswith("uw_"), f"Unexpected course_id {cid!r} for uw role"


def test_sequence_has_no_duplicates():
    seq = compute_module_sequence(_make_scores(), "rm")
    assert len(set(seq)) == len(seq), "Sequence contains duplicate course IDs"


# ── Ordering logic ────────────────────────────────────────────────────────────


def test_quick_win_first():
    """Domain closest to 2.0 in [1.5, 2.5] should be module 1."""
    scores = _make_scores(
        responsible_ai=2.0,      # exactly 2.0 — best quick win
        strategic_prompting=0.5, # gap
        critical_eval=0.5,       # gap
        relationship_intel=0.5,  # gap
        data_decision=0.5,       # gap
        augmented_comm=0.5,      # gap
    )
    seq = compute_module_sequence(scores, "rm")
    assert seq[0] == "rm_c1_responsible_ai"


def test_gaps_before_strong():
    """Domains below 1.5 (gaps) should appear before domains above 2.5 (strong)."""
    scores = _make_scores(
        responsible_ai=3.0,   # strong
        strategic_prompting=0.5,  # gap
        critical_eval=0.5,    # gap
        relationship_intel=1.5,   # quick-win
        data_decision=2.0,    # quick-win
        augmented_comm=3.5,   # strong
    )
    seq = compute_module_sequence(scores, "rm")
    gap_courses = {"rm_c2_strategic_prompting", "rm_c3_critical_eval"}
    strong_courses = {"rm_c1_responsible_ai", "rm_c6_augmented_comm"}
    # All gap courses should appear before all strong courses (excluding capstone)
    seq_no_capstone = seq[:-1]
    for gap_cid in gap_courses:
        for strong_cid in strong_courses:
            if gap_cid in seq_no_capstone and strong_cid in seq_no_capstone:
                assert seq_no_capstone.index(gap_cid) < seq_no_capstone.index(strong_cid), (
                    f"Gap course {gap_cid!r} should precede strong course {strong_cid!r}"
                )


def test_all_scores_equal_returns_7_courses():
    """Edge case: all domains have identical scores."""
    scores = {d: 2.0 for d in DOMAIN_IDS}
    seq = compute_module_sequence(scores, "rm")
    assert len(seq) == 7
    assert seq[-1] == "rm_c7_capstone"
