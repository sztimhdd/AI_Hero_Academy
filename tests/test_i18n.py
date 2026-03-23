"""
Tests for i18n completeness — ensures every t() key used in pages/ exists
in both en.json and zh.json so missing keys never silently display as raw
key strings in production.
"""

import re
from pathlib import Path

import pytest

PAGES_DIR = Path(__file__).parent.parent / "pages"
I18N_DIR = Path(__file__).parent.parent / "content" / "i18n"

# Match t("key") but NOT .get("key"), dict["key"], or other patterns.
# Requires t( to be preceded by whitespace, (, comma, or start of line.
_T_CALL = re.compile(r'(?<![.\w])t\(\s*"([\w.]+)"')


def _collect_keys() -> set[str]:
    """Extract all t("key") literals from pages/*.py."""
    keys: set[str] = set()
    for py_file in PAGES_DIR.glob("*.py"):
        src = py_file.read_text(encoding="utf-8")
        keys.update(_T_CALL.findall(src))
    return keys


def _load_json(path: Path) -> dict:
    import json
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def en_keys():
    return set(_load_json(I18N_DIR / "en.json").keys())


@pytest.fixture(scope="module")
def zh_keys():
    return set(_load_json(I18N_DIR / "zh.json").keys())


@pytest.fixture(scope="module")
def used_keys():
    return _collect_keys()


def test_all_used_keys_in_en(used_keys, en_keys):
    missing = used_keys - en_keys
    assert not missing, (
        f"{len(missing)} t() key(s) missing from en.json:\n"
        + "\n".join(f"  {k}" for k in sorted(missing))
    )


def test_all_used_keys_in_zh(used_keys, zh_keys):
    missing = used_keys - zh_keys
    assert not missing, (
        f"{len(missing)} t() key(s) missing from zh.json:\n"
        + "\n".join(f"  {k}" for k in sorted(missing))
    )
