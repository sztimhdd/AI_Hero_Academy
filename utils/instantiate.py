"""
Placeholder instantiation for atomic modules and diagnostic items.

Converts role-agnostic atomic templates into role-specific content by
substituting {placeholder} variables with profile values.

Usage:
    from utils.instantiate import instantiate_atom, build_profile

    profile = build_profile("rm")
    instantiated = instantiate_atom(atom, profile)
"""

import copy

# Default placeholder values for the four existing roles.
# Keys match the placeholder names used in atomic_modules.json and
# atomic_diagnostic_items.json (e.g. {role}, {org_type}, {case_type}).
_ROLE_PROFILES: dict[str, dict[str, str]] = {
    "rm": {
        "role": "Relationship Manager",
        "org_type": "financial services firm",
        "case_type": "client relationship file",
        "data_types": "financial statements, credit analysis, and client correspondence",
        "sensitivity_level": "Non-Public Information",
        "workflow_goal": "accelerate relationship management and client outreach",
        "programme_name": "AI-Assisted Portfolio Review",
        "audience": "credit committee",
    },
    "uw": {
        "role": "Underwriter",
        "org_type": "trade finance firm",
        "case_type": "underwriting file",
        "data_types": "transaction documents, financial statements, and risk assessments",
        "sensitivity_level": "Confidential",
        "workflow_goal": "streamline underwriting analysis and risk decision-making",
        "programme_name": "AI-Assisted Deal Analysis",
        "audience": "risk committee",
    },
    "an": {
        "role": "Analyst",
        "org_type": "financial services firm",
        "case_type": "research and analysis file",
        "data_types": "financial data, industry reports, and internal research",
        "sensitivity_level": "Internal",
        "workflow_goal": "accelerate data analysis and insight generation",
        "programme_name": "AI-Assisted Research Program",
        "audience": "senior leadership",
    },
    "mk": {
        "role": "Marketing Coordinator",
        "org_type": "financial services firm",
        "case_type": "marketing campaign file",
        "data_types": "campaign briefs, market data, and content assets",
        "sensitivity_level": "Internal",
        "workflow_goal": "improve content quality and campaign effectiveness",
        "programme_name": "AI-Assisted Campaign Development",
        "audience": "marketing team",
    },
}


def build_profile(role_id: str, overrides: dict | None = None) -> dict[str, str]:
    """Return a placeholder context dict for the given role.

    Args:
        role_id: one of "rm", "uw", "an", "mk"
        overrides: optional key-value pairs to add or override in the base profile

    Returns:
        dict mapping placeholder names to substitution strings
    """
    base = _ROLE_PROFILES.get(role_id, _ROLE_PROFILES["rm"]).copy()
    if overrides:
        base.update(overrides)
    return base


def instantiate_atom(atom: dict, profile: dict[str, str]) -> dict:
    """Deep-copy an atomic module and substitute all {placeholder} occurrences.

    Placeholders absent from profile are left unchanged (e.g. {case_type} if
    profile omits that key), enabling partial instantiation for preview.

    Args:
        atom: raw atom dict from atomic_modules.json
        profile: dict mapping placeholder names to substitution strings

    Returns:
        new dict (deep copy) with placeholders substituted
    """
    return _substitute(copy.deepcopy(atom), profile)


def instantiate_diagnostic_item(item: dict, profile: dict[str, str]) -> dict:
    """Deep-copy an atomic diagnostic item and substitute all {placeholder} occurrences.

    Args:
        item: raw item dict from atomic_diagnostic_items.json
        profile: dict mapping placeholder names to substitution strings

    Returns:
        new dict (deep copy) with placeholders substituted
    """
    return _substitute(copy.deepcopy(item), profile)


def _substitute(obj, profile: dict[str, str]):
    """Recursively walk obj and replace {key} with profile[key] in all strings."""
    if isinstance(obj, str):
        for key, val in profile.items():
            obj = obj.replace(f"{{{key}}}", str(val))
        return obj
    if isinstance(obj, dict):
        return {k: _substitute(v, profile) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_substitute(item, profile) for item in obj]
    return obj
