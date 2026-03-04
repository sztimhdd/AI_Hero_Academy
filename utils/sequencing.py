"""
Module sequencing algorithm.

After the diagnostic, this determines the order in which the 5 training
courses are presented, personalised per learner.

Algorithm (from PRD §10):
1. Quick-win first: domain scoring 1.5–2.5, closest to 2.0
2. Gaps next: domains below 1.5, ascending (lowest first = biggest gap)
3. Remaining: domains not in quick-win, gaps, or strong
4. Strong last: domains above 2.5, ascending
5. Capstone is always module 5
"""

DOMAIN_TO_COURSE: dict[str, dict[str, str]] = {
    "rm": {
        "prompting":    "rm_c1_prompting",
        "verification": "rm_c2_verification",
        "data_safety":  "rm_c3_data_safety",
        "tool_fluency": "rm_c4_tool_fluency",
    },
    "uw": {
        "prompting":    "uw_c1_prompting",
        "verification": "uw_c2_verification",
        "data_safety":  "uw_c3_data_safety",
        "tool_fluency": "uw_c4_tool_fluency",
    },
}
CAPSTONE_COURSE_ID: dict[str, str] = {
    "rm": "rm_c5_capstone",
    "uw": "uw_c5_capstone",
}


def compute_module_sequence(domain_scores: dict, role_id: str = "rm") -> list[str]:
    """
    domain_scores: {"prompting": 2.0, "verification": 0.8, ...}
    role_id: "rm" or "uw" — determines which course IDs are assigned.
    Returns: list of 5 course_ids in personalised order (index 0 = Module 1).
    """
    course_map = DOMAIN_TO_COURSE.get(role_id, DOMAIN_TO_COURSE["rm"])
    capstone = CAPSTONE_COURSE_ID.get(role_id, CAPSTONE_COURSE_ID["rm"])

    quick_wins = sorted(
        [(d, s) for d, s in domain_scores.items() if 1.5 <= s <= 2.5],
        key=lambda x: abs(x[1] - 2.0),
    )
    gaps = sorted(
        [(d, s) for d, s in domain_scores.items() if s < 1.5],
        key=lambda x: x[1],  # lowest score first
    )
    strong = sorted(
        [(d, s) for d, s in domain_scores.items() if s > 2.5],
        key=lambda x: x[1],
    )
    placed = {d for d, _ in quick_wins + gaps + strong}
    remaining = [(d, s) for d, s in domain_scores.items() if d not in placed]

    ordered_domains = [d for d, _ in quick_wins + gaps + remaining + strong]
    sequence = [
        course_map[d]
        for d in ordered_domains
        if d in course_map
    ]
    sequence.append(capstone)
    return sequence[:5]
