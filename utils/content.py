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


def _load_lang(filename: str, lang: str = "en") -> "dict | list":
    """Load lang-specific content file; falls back to English if not available."""
    if lang != "en":
        p = _CONTENT_DIR / lang / filename
        if p.exists():
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    return _load(filename)


# ── Module-level caches — loaded once at startup ──────────────────────────────

ROLES: dict = _load("roles.json")
DOMAINS: dict = _load("domains.json")
DIAGNOSTIC_ITEMS: list = _load("diagnostic_items.json")   # ordered by display_order
COURSES: dict = _load("courses.json")
READING: dict = _load("reading_content.json")
SCENARIOS: dict = _load("practice_scenarios.json")
EVAL_ITEMS: dict = _load("evaluation_items.json")

# Convenience mapping for generate_gap_map(): domain_id -> description string
# domains.json uses role-scoped top-level keys (e.g. "rm_responsible_ai"); the domain_id
# field inside each entry is the flat key (e.g. "responsible_ai"). Build the mapping
# from field values so callers use flat keys as before.
DOMAIN_DESCRIPTIONS: dict = {
    d["domain_id"]: d["description"]
    for d in DOMAINS.values()
}


# ── Typed getters ─────────────────────────────────────────────────────────────

def get_role(role_id: str, lang: str = "en") -> dict:
    if lang == "en":
        return ROLES[role_id]
    return _load_lang("roles.json", lang)[role_id]


def get_domain(domain_id: str, role_id: str = "rm", lang: str = "en") -> dict:
    # DOMAINS keys are role-scoped ("rm_prompting"); look up by domain_id + role_id.
    domains = _load_lang("domains.json", lang)
    match = next(
        (d for d in domains.values() if d["domain_id"] == domain_id and d.get("role_id") == role_id),
        None,
    )
    if match is None:
        # Fallback: any domain with matching domain_id
        match = next((d for d in domains.values() if d["domain_id"] == domain_id), None)
    if match is None:
        raise KeyError(f"No domain with domain_id={domain_id!r} found in domains.json")
    return match


def get_domain_descriptions(role_id: str = "rm", lang: str = "en") -> dict:
    """Return {domain_id: description} for the given role."""
    domains = _load_lang("domains.json", lang)
    return {
        d["domain_id"]: d["description"]
        for d in domains.values()
        if d.get("role_id") == role_id
    }


def get_diagnostic_items(role_id: str = "rm", lang: str = "en") -> list:
    """Returns diagnostic items for the given role, ordered by display_order."""
    items_data = _load_lang("diagnostic_items.json", lang)
    items = [i for i in items_data if i.get("role_id") == role_id]
    return sorted(items, key=lambda x: x.get("display_order", 99))


def get_course(course_id: str, lang: str = "en") -> dict:
    if lang == "en":
        return COURSES[course_id]
    return _load_lang("courses.json", lang)[course_id]


def get_reading(course_id: str, lang: str = "en") -> dict:
    if lang == "en":
        return READING[course_id]
    return _load_lang("reading_content.json", lang)[course_id]


def get_scenario(course_id: str, lang: str = "en") -> dict:
    if lang == "en":
        return SCENARIOS[course_id]
    return _load_lang("practice_scenarios.json", lang)[course_id]


def get_courses(role_id: str, lang: str = "en") -> list[dict]:
    """Returns all courses for the given role, ordered by sequence_order."""
    courses = _load_lang("courses.json", lang)
    return sorted(
        [c for c in courses.values() if c.get("role_id") == role_id],
        key=lambda c: c.get("sequence_order", 99),
    )


def get_eval_items(course_id: str, lang: str = "en") -> list:
    """Returns list of 4 evaluation items for the given course, ordered by sequence."""
    if lang == "en":
        return EVAL_ITEMS[course_id]
    return _load_lang("evaluation_items.json", lang)[course_id]


_READING_STRUCTURED: dict | None = None
_ATOMIC_MODULES: list | None = None
_ATOMIC_DIAGNOSTIC_ITEMS: dict | None = None
_DOMAINS_UNIVERSAL: dict | None = None


def get_atomic_modules() -> list:
    """Return all atomic modules from atomic_modules_v2.json (lazy-loaded)."""
    global _ATOMIC_MODULES
    if _ATOMIC_MODULES is None:
        p = _CONTENT_DIR / "atomic_modules_v2.json"
        if not p.exists():
            p = _CONTENT_DIR / "atomic_modules.json"  # fallback to v1
        _ATOMIC_MODULES = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    return _ATOMIC_MODULES


def get_atomic_diagnostic_items() -> dict:
    """Return all atomic diagnostic items from atomic_diagnostic_items.json (lazy-loaded)."""
    global _ATOMIC_DIAGNOSTIC_ITEMS
    if _ATOMIC_DIAGNOSTIC_ITEMS is None:
        p = _CONTENT_DIR / "atomic_diagnostic_items.json"
        _ATOMIC_DIAGNOSTIC_ITEMS = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return _ATOMIC_DIAGNOSTIC_ITEMS


def get_domains_universal() -> dict:
    """Return universal domain schema from domains_universal.json (lazy-loaded)."""
    global _DOMAINS_UNIVERSAL
    if _DOMAINS_UNIVERSAL is None:
        p = _CONTENT_DIR / "domains_universal.json"
        _DOMAINS_UNIVERSAL = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return _DOMAINS_UNIVERSAL


def get_reading_structured(course_id: str) -> dict | None:
    """
    Returns the structured sub-fields dict for a course's reading content, or None
    if reading_content_structured.json has not been generated yet.
    """
    global _READING_STRUCTURED
    if _READING_STRUCTURED is None:
        p = _CONTENT_DIR / "reading_content_structured.json"
        if p.exists():
            _READING_STRUCTURED = json.loads(p.read_text(encoding="utf-8"))
        else:
            _READING_STRUCTURED = {}
    return _READING_STRUCTURED.get(course_id)
