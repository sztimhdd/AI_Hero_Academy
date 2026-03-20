"""
utils/i18n.py — Language utilities for AI Hero Academy.

Loads flat JSON translation files from content/i18n/.
Priority fallback: requested lang → English → key itself (never crashes).
"""

import json
from pathlib import Path

import streamlit as st

SUPPORTED_LANGS: dict[str, str] = {"en": "English", "zh": "中文"}

_I18N_DIR = Path(__file__).parent.parent / "content" / "i18n"

_TRANSLATIONS: dict[str, dict[str, str]] = {}


def _load() -> None:
    for lang in SUPPORTED_LANGS:
        path = _I18N_DIR / f"{lang}.json"
        try:
            with open(path, encoding="utf-8") as f:
                _TRANSLATIONS[lang] = json.load(f)
        except Exception:
            _TRANSLATIONS[lang] = {}


_load()


def t(key: str, lang: str = "en") -> str:
    """Return translated string for key+lang.

    Fallback chain: lang → en → key itself.
    Never raises.
    """
    try:
        val = _TRANSLATIONS.get(lang, {}).get(key)
        if val is not None:
            return val
        val = _TRANSLATIONS.get("en", {}).get(key)
        if val is not None:
            return val
    except Exception:
        pass
    return key


def detect_browser_lang() -> str:
    """Detect preferred language from the browser Accept-Language header.

    Returns "zh" if the header starts with "zh" (covers zh-CN, zh-TW, zh-HK).
    Returns "en" for everything else, including on error.
    Requires Streamlit ≥ 1.37 for st.context.headers.
    """
    try:
        accept = st.context.headers.get("Accept-Language", "") or ""
        if accept.strip().lower().startswith("zh"):
            return "zh"
    except Exception:
        pass
    return "en"
