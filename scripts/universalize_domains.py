#!/usr/bin/env python3
"""
Convert role-scoped domain entries in content/domains.json into a universal
domain schema stored in content/domains_universal.json.

Current schema (domains.json):
    24 top-level entries keyed by role-scoped ID, e.g. "rm_responsible_ai"
    Each entry: domain_id, role_id, title, description, level_0..4 labels + descriptors

Universal schema (domains_universal.json):
    6 top-level entries keyed by domain_id, e.g. "responsible_ai"
    Each entry:
        domain_id, title, description (from RM baseline — most complete)
        level_labels: {0..4: label}   (identical across all roles)
        level_descriptors: {role_id: {0..4: descriptor}}

The universal schema enables future roles to add only their level_descriptors
without duplicating domain metadata.

Run:
    python scripts/universalize_domains.py
    python scripts/universalize_domains.py --dry-run
"""

import argparse
import json
import sys
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent / "content"

# Preferred source role for the universal description field (most complete baseline).
_DESCRIPTION_SOURCE_ROLE = "rm"


def universalize(domains: dict) -> dict:
    """Convert role-scoped domains dict to universal domain schema."""
    # Group entries by domain_id
    by_domain: dict[str, list[dict]] = {}
    for entry in domains.values():
        did = entry["domain_id"]
        by_domain.setdefault(did, []).append(entry)

    universal: dict[str, dict] = {}

    # Domain display order (matches the hexagon model)
    domain_order = [
        "responsible_ai",
        "strategic_prompting",
        "critical_eval",
        "data_decision",
        "relationship_intel",
        "augmented_comm",
    ]

    for domain_id in domain_order:
        entries = by_domain.get(domain_id, [])
        if not entries:
            continue

        # Pick the description from the preferred source role, fall back to first entry
        desc_entry = next(
            (e for e in entries if e.get("role_id") == _DESCRIPTION_SOURCE_ROLE),
            entries[0],
        )

        # Level labels are identical across roles — take from any entry
        level_labels = {
            str(i): desc_entry[f"level_{i}_label"]
            for i in range(5)
            if f"level_{i}_label" in desc_entry
        }

        # Collect per-role level descriptors
        level_descriptors: dict[str, dict[str, str]] = {}
        for entry in sorted(entries, key=lambda e: e.get("role_id", "")):
            role_id = entry.get("role_id", "unknown")
            level_descriptors[role_id] = {
                str(i): entry[f"level_{i}_descriptor"]
                for i in range(5)
                if f"level_{i}_descriptor" in entry
            }

        universal[domain_id] = {
            "domain_id": domain_id,
            "title": desc_entry["title"],
            "description": desc_entry["description"],
            "level_labels": level_labels,
            "level_descriptors": level_descriptors,
        }

    return universal


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print output; do not write file")
    args = parser.parse_args()

    src = CONTENT_DIR / "domains.json"
    if not src.exists():
        sys.exit(f"ERROR: {src} not found")

    domains = json.loads(src.read_text(encoding="utf-8"))
    universal = universalize(domains)

    if args.dry_run:
        print(json.dumps(universal, indent=2, ensure_ascii=False))
        print(f"\n--- {len(universal)} universal domains (dry run, not written) ---")
    else:
        out = CONTENT_DIR / "domains_universal.json"
        out.write_text(json.dumps(universal, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {len(universal)} universal domains to {out}")
        for domain_id, d in universal.items():
            roles = list(d["level_descriptors"].keys())
            print(f"  {domain_id}: {len(roles)} role variants ({', '.join(roles)})")


if __name__ == "__main__":
    main()
