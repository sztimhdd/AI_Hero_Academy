"""
tests/test_path_assembler.py — Unit tests for utils/path_assembler.py.

Run: python -m pytest tests/test_path_assembler.py -v
"""
import pytest
from utils.path_assembler import assemble_path, fill_scenario, tag_match_score


# ── Fixture helpers ───────────────────────────────────────────────────────────

def _atom(atom_id: str, domain: str, tags: list[str] | None = None) -> dict:
    """Build a minimal atom dict for testing."""
    return {
        "atom_id": atom_id,
        "domain": domain,
        "capability_tags": tags or [],
        "status": "canonical",
        "practice": {
            "scenario_template": "You are a {role} at a {org_type}. Goal: {workflow_goal}.",
        },
    }


INTAKE_BASIC = {
    "role_text": "Relationship Manager",
    "daily_tasks": ["client meetings", "status reports"],
    "magic_wish": "draft meeting summaries faster",
    "ai_tools": ["Microsoft Copilot (M365 — Word, Excel, Teams, Outlook)"],
}

DOMAIN_SCORES_BASIC = {
    "responsible_ai": 1.0,   # gap
    "strategic_prompting": 2.1,  # quick_win
    "critical_eval": 1.8,    # quick_win
    "data_decision": 2.8,    # strong
    "relationship_intel": 1.3,  # gap
    "augmented_comm": 1.5,   # quick_win boundary
}

SIX_ATOMS = [
    _atom("a_responsible_ai",    "responsible_ai",    ["data_privacy", "responsible_use"]),
    _atom("a_strategic_prompting","strategic_prompting",["prompt_engineering", "meeting_summaries"]),
    _atom("a_critical_eval",     "critical_eval",     ["evaluation", "fact_checking"]),
    _atom("a_data_decision",     "data_decision",     ["data_analysis", "reporting"]),
    _atom("a_relationship_intel","relationship_intel",["client_management", "crm"]),
    _atom("a_augmented_comm",    "augmented_comm",    ["communication", "writing"]),
]


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_assemble_path_basic():
    """6 atoms 1 per domain — responsible_ai pinned last (before capstone)."""
    path = assemble_path(INTAKE_BASIC, DOMAIN_SCORES_BASIC, SIX_ATOMS)
    assert len(path) >= 1
    assert len(path) <= 7
    # responsible_ai should be in path regardless of its score
    assert "a_responsible_ai" in path
    # responsible_ai is pinned last — must appear after all other skill domains
    if "a_data_decision" in path:
        assert path.index("a_responsible_ai") > path.index("a_data_decision")


def test_assemble_path_quick_win_before_gap():
    """Domain score 2.0 (quick win) should come before domain score < 1.5 (gap)."""
    scores = {
        "strategic_prompting": 2.0,  # quick_win
        "responsible_ai": 1.0,       # gap
    }
    atoms = [
        _atom("a_prompting", "strategic_prompting"),
        _atom("a_rai", "responsible_ai"),
    ]
    path = assemble_path(INTAKE_BASIC, scores, atoms)
    assert "a_prompting" in path
    assert "a_rai" in path
    assert path.index("a_prompting") < path.index("a_rai")


def test_assemble_path_deduplicates_domain():
    """Two atoms with the same domain → only one atom_id in output."""
    scores = {"strategic_prompting": 2.0}
    atoms = [
        _atom("a_prompting_v1", "strategic_prompting", ["prompt_engineering"]),
        _atom("a_prompting_v2", "strategic_prompting", ["meeting_summaries", "draft"]),
    ]
    path = assemble_path(INTAKE_BASIC, scores, atoms)
    # Both have same domain; only one should appear
    assert len(path) == 1
    prompting_count = sum(1 for aid in path if "prompting" in aid)
    assert prompting_count == 1


def test_fill_scenario_placeholder_substitution():
    """{role} and {org_type} are replaced in the output."""
    atom = _atom("x", "augmented_comm")
    intake = {"role_text": "Relationship Manager", "daily_tasks": [], "magic_wish": "", "ai_tools": []}
    result = fill_scenario(atom, intake)
    assert "{role}" not in result
    assert "Relationship Manager" in result
    assert "{org_type}" not in result
    # org_type not inferrable from "Relationship Manager" directly → "organization"
    assert "organization" in result.lower() or "financial" in result.lower()


def test_fill_scenario_fallback():
    """Bad/missing input → returns raw template or empty string, never raises."""
    # Missing practice key
    bad_atom = {"atom_id": "x", "domain": "y"}
    result = fill_scenario(bad_atom, {})
    assert isinstance(result, str)  # no exception

    # None intake
    atom = _atom("x", "augmented_comm")
    result2 = fill_scenario(atom, None)  # type: ignore[arg-type]
    assert isinstance(result2, str)  # no exception


def test_assemble_path_capstone_appended_last():
    """Capstone atom (domain == 'capstone') is always appended last."""
    scores = {
        "strategic_prompting": 2.0,
        "responsible_ai": 1.0,
        "capstone": 3.5,
    }
    atoms = [
        _atom("a_prompting", "strategic_prompting"),
        _atom("a_rai", "responsible_ai"),
        _atom("a_capstone", "capstone"),
    ]
    path = assemble_path(INTAKE_BASIC, scores, atoms)
    assert "a_capstone" in path
    assert path[-1] == "a_capstone"


def test_assemble_path_never_empty():
    """assemble_path never returns an empty list when atoms are provided."""
    # All atoms have domain score > 3.0 → fallback to full list
    scores = {"strategic_prompting": 3.5, "responsible_ai": 3.8}
    atoms = [
        _atom("a_prompting", "strategic_prompting"),
        _atom("a_rai", "responsible_ai"),
    ]
    path = assemble_path(INTAKE_BASIC, scores, atoms)
    assert len(path) >= 1


def test_fill_scenario_all_common_placeholders_replaced():
    """All common placeholders ({case_type}, {sensitivity_level}, etc.) are replaced."""
    import re
    full_template_atom = {
        "atom_id": "x",
        "domain": "augmented_comm",
        "practice": {
            "scenario_template": (
                "You are a {role} at a {org_type}. "
                "Case: {case_type}. Sensitivity: {sensitivity_level}. "
                "Audience: {audience}. Goal: {workflow_goal}. "
                "Project: {programme_name}. Data: {data_types}."
            )
        },
    }
    intake = {"role_text": "Relationship Manager", "daily_tasks": [], "magic_wish": "", "ai_tools": []}
    result = fill_scenario(full_template_atom, intake)
    remaining = set(re.findall(r'\{(\w+)\}', result))
    assert remaining == set(), f"Unfilled placeholders remain: {remaining}"


def test_fill_scenario_no_unfilled_placeholders_in_all_real_atoms():
    """All real atoms in atomic_modules_v2.json produce scenario text with no unfilled placeholders."""
    import re
    from utils.content import get_atomic_modules
    atoms = get_atomic_modules()
    intake = {
        "role_text": "Relationship Manager",
        "daily_tasks": ["client briefs"],
        "magic_wish": "auto-summarize",
        "ai_tools": [],
    }
    failures = []
    for atom in atoms:
        filled = fill_scenario(atom, intake)
        remaining = set(re.findall(r'\{(\w+)\}', filled))
        if remaining:
            failures.append(f"{atom['atom_id']}: {remaining}")
    assert failures == [], "Atoms with unfilled placeholders:\n" + "\n".join(failures)
