"""
utils/path_assembler.py — Phase 3: Personalized atom path assembly.

Pure Python — no LLM, no Firestore. All logic is deterministic and testable.
"""
from __future__ import annotations


def tag_match_score(tags: list[str], intake: dict) -> float:
    """Fraction of atom capability_tags that appear as substrings in intake text.

    Combines magic_wish, daily_tasks, and ai_tools into a single keyword text.
    Returns 0.0–1.0.
    """
    if not tags:
        return 0.0
    parts = [
        intake.get("magic_wish") or "",
        " ".join(intake.get("daily_tasks") or []),
        " ".join(intake.get("ai_tools") or []),
        intake.get("role_text") or "",
    ]
    combined = " ".join(parts).lower()
    count = sum(1 for tag in tags if tag.replace("_", " ").lower() in combined or tag.lower() in combined)
    return min(count / len(tags), 1.0)


def assemble_path(
    intake_profile: dict,
    domain_scores: dict,
    atoms: list[dict],
    max_atoms: int = 7,
) -> list[str]:
    """Return an ordered list of atom_ids personalised for this learner.

    Assembly logic:
    1. FILTER: remove atoms whose domain score > 3.0 (unless no others remain).
    2. SCORE each remaining atom.
    3. SEQUENCE into four buckets (quick-win, gap, remaining, strong).
    4. DEDUPLICATE: keep highest-scored atom per domain.
    5. Cap at max_atoms; append capstone (domain == "capstone") last if room.
    """
    # ── 1. Filter ─────────────────────────────────────────────────────────────
    filtered = [a for a in atoms if domain_scores.get(a["domain"], 2.0) <= 3.0]
    if not filtered:
        filtered = list(atoms)

    # ── 2. Score ──────────────────────────────────────────────────────────────
    def _score(atom: dict) -> float:
        ds = domain_scores.get(atom["domain"], 2.0)
        gap = (4.0 - ds) / 4.0
        intake = tag_match_score(atom.get("capability_tags") or [], intake_profile)
        return round((gap * 0.6) + (intake * 0.4), 6)

    # ── 3. Sequence into buckets ───────────────────────────────────────────────
    quick_wins: list[tuple] = []
    gaps: list[tuple] = []
    strong: list[tuple] = []
    remaining: list[tuple] = []

    for atom in filtered:
        if atom.get("domain") == "capstone":
            continue  # handled separately at the end
        ds = domain_scores.get(atom["domain"], 2.0)
        s = _score(atom)
        if 1.5 <= ds <= 2.5:
            quick_wins.append((atom, s, ds))
        elif ds < 1.5:
            gaps.append((atom, s, ds))
        elif ds > 2.5:
            strong.append((atom, s, ds))
        else:
            remaining.append((atom, s, ds))

    quick_wins.sort(key=lambda x: x[1], reverse=True)
    gaps.sort(key=lambda x: x[2])           # ascending domain score (lowest gap first)
    remaining.sort(key=lambda x: x[1], reverse=True)
    strong.sort(key=lambda x: x[1])         # ascending total (least strong first)

    ordered: list[tuple] = quick_wins + gaps + remaining + strong

    # ── 4. Deduplicate by domain ──────────────────────────────────────────────
    # Track best atom per domain (highest total_score) and first position.
    domain_first_pos: dict[str, int] = {}
    domain_best: dict[str, tuple] = {}

    for i, (atom, s, ds) in enumerate(ordered):
        domain = atom["domain"]
        if domain not in domain_first_pos:
            domain_first_pos[domain] = i
        if domain not in domain_best or s > domain_best[domain][1]:
            domain_best[domain] = (atom, s)

    # Reconstruct in original bucket order (by first occurrence of each domain).
    sorted_domains = sorted(domain_first_pos.keys(), key=lambda d: domain_first_pos[d])
    result = [domain_best[d][0]["atom_id"] for d in sorted_domains[:max_atoms]]

    # ── 5. Append capstone if present and there's room ────────────────────────
    capstone_atoms = [a for a in atoms if a.get("domain") == "capstone"]
    if capstone_atoms:
        capstone_id = capstone_atoms[0]["atom_id"]
        if capstone_id not in result and len(result) < max_atoms:
            result.append(capstone_id)

    return result


def fill_scenario(atom: dict, intake_profile: dict, lang_code: str = "en") -> str:
    """Fill {placeholder} tokens in an atom's scenario_template.

    Substitutions applied:
      {role}              → intake_profile.role_text or "professional"
      {org_type}          → inferred from role_text
      {programme_name}    → "the project"
      {data_types}        → "your work data"
      {case_type}         → inferred from role_text (e.g. "client matter")
      {sensitivity_level} → "standard"
      {audience}          → inferred from role_text (e.g. "client" or "stakeholder")
      {workflow_goal}     → "deliver quality outcomes"
      {key_contact_change}→ "account stakeholder change"
      {lead_aging_days}   → "30"
      {SLA_breach_days}   → "5"

    Never raises — catches all exceptions and returns the raw template.
    """
    try:
        template: str = atom["practice"]["scenario_template"]
    except Exception:
        return ""

    try:
        role = (intake_profile.get("role_text") or "professional").strip() or "professional"
        role_lower = role.lower()

        if any(kw in role_lower for kw in ["bank", "financ", "lend", "credit", "invest", "capital"]):
            org_type = "financial services organization"
            case_type = "client portfolio matter"
            audience = "client"
        elif any(kw in role_lower for kw in ["insurance", "underwrite", "claim", "actuar"]):
            org_type = "insurance firm"
            case_type = "underwriting matter"
            audience = "underwriting stakeholder"
        elif any(kw in role_lower for kw in ["consult"]):
            org_type = "consulting firm"
            case_type = "client engagement matter"
            audience = "client"
        elif any(kw in role_lower for kw in ["government", "public", "municipal", "agency"]):
            org_type = "public sector organization"
            case_type = "programme matter"
            audience = "internal stakeholder"
        elif any(kw in role_lower for kw in ["relationship manager", " rm ", "client relationship"]):
            org_type = "financial services organization"
            case_type = "client relationship matter"
            audience = "client"
        elif any(kw in role_lower for kw in ["analyst", " an ", "analytics"]):
            org_type = "organization"
            case_type = "data analysis matter"
            audience = "business stakeholder"
        elif any(kw in role_lower for kw in ["market", "campaign", "brand"]):
            org_type = "organization"
            case_type = "marketing matter"
            audience = "target audience"
        elif any(kw in role_lower for kw in ["project manager", " pm ", "programme"]):
            org_type = "organization"
            case_type = "project matter"
            audience = "project stakeholder"
        else:
            org_type = "organization"
            case_type = "work matter"
            audience = "stakeholder"

        filled = template
        filled = filled.replace("{role}", role)
        filled = filled.replace("{org_type}", org_type)
        filled = filled.replace("{programme_name}", "the project")
        filled = filled.replace("{data_types}", "your work data")
        filled = filled.replace("{case_type}", case_type)
        filled = filled.replace("{sensitivity_level}", "standard")
        filled = filled.replace("{audience}", audience)
        filled = filled.replace("{workflow_goal}", "deliver quality outcomes")
        filled = filled.replace("{key_contact_change}", "account stakeholder change")
        filled = filled.replace("{lead_aging_days}", "30")
        filled = filled.replace("{SLA_breach_days}", "5")
        return filled
    except Exception:
        try:
            return atom["practice"]["scenario_template"]
        except Exception:
            return ""
