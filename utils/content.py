"""
Content loader for AI Hero Academy.

Loads all static content JSON files once at module import time (i.e., once per
container process). Replaces the previous pattern of querying the content.*
Delta tables via SQL Warehouse on every page load.

All exported getters raise KeyError if the requested ID does not exist —
callers should handle this at the page level with a graceful error message.
"""

import json
from pathlib import Path

_CONTENT_DIR = Path(__file__).parent.parent / "content"


def _load(filename: str):
    with open(_CONTENT_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


# ── Module-level caches — loaded once at startup ──────────────────────────────

ROLES: dict = _load("roles.json")
DOMAINS: dict = _load("domains.json")
DIAGNOSTIC_ITEMS: list = _load("diagnostic_items.json")   # ordered by display_order
COURSES: dict = _load("courses.json")
READING: dict = _load("reading_content.json")
SCENARIOS: dict = _load("practice_scenarios.json")
EVAL_ITEMS: dict = _load("evaluation_items.json")

# Convenience mapping for generate_gap_map(): domain_id -> description string
# domains.json uses role-scoped top-level keys (e.g. "rm_prompting"); the domain_id
# field inside each entry is still the flat key ("prompting"). Build the mapping
# from field values so callers continue to use flat keys as before.
DOMAIN_DESCRIPTIONS: dict = {
    d["domain_id"]: d["description"]
    for d in DOMAINS.values()
}


# ── Typed getters ─────────────────────────────────────────────────────────────

def get_role(role_id: str) -> dict:
    return ROLES[role_id]


def get_domain(domain_id: str, role_id: str = "rm") -> dict:
    # DOMAINS keys are role-scoped ("rm_prompting"); look up by domain_id + role_id.
    match = next(
        (d for d in DOMAINS.values() if d["domain_id"] == domain_id and d.get("role_id") == role_id),
        None,
    )
    if match is None:
        # Fallback: any domain with matching domain_id
        match = next((d for d in DOMAINS.values() if d["domain_id"] == domain_id), None)
    if match is None:
        raise KeyError(f"No domain with domain_id={domain_id!r} found in domains.json")
    return match


def get_domain_descriptions(role_id: str = "rm") -> dict:
    """Return {domain_id: description} for the given role."""
    return {
        d["domain_id"]: d["description"]
        for d in DOMAINS.values()
        if d.get("role_id") == role_id
    }


def get_diagnostic_items(role_id: str = "rm") -> list:
    """Returns diagnostic items for the given role, ordered by display_order."""
    return [i for i in DIAGNOSTIC_ITEMS if i.get("role_id") == role_id]


def get_course(course_id: str) -> dict:
    return COURSES[course_id]


def get_reading(course_id: str) -> dict:
    return READING[course_id]


def get_scenario(course_id: str) -> dict:
    return SCENARIOS[course_id]


def get_eval_items(course_id: str) -> list:
    """Returns list of 4 evaluation items for the given course, ordered by sequence."""
    return EVAL_ITEMS[course_id]
