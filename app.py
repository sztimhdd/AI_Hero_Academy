"""
AI Hero Academy — entry point and router.

On every page load:
1. Read user_email from auth context
2. Query Firestore to determine user state
3. Route to the appropriate page, or fall through to the main app nav
"""

import streamlit as st
from utils.auth import get_user_email
from utils.db import get_profile, get_latest_diagnostic, get_any_progress
from utils.styles import inject_global_css

st.set_page_config(
    page_title="AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()


def get_user_state(user_email: str) -> tuple[str, str | None]:
    """
    Returns (state, role_id) where state is one of:
    new_user | needs_diagnostic | needs_course | in_training
    role_id is None for new_user, otherwise the role from user_profiles.
    """
    profile = get_profile(user_email)
    if not profile:
        return "new_user", None

    role_id = profile["role_id"]

    session = get_latest_diagnostic(user_email)
    if not session:
        return "needs_diagnostic", role_id

    progress = get_any_progress(user_email)
    if not progress:
        return "needs_course", role_id

    return "in_training", role_id


# ── Initialise session state ──────────────────────────────────────────────────
if "user_email" not in st.session_state:
    try:
        user_email = get_user_email()
        state, role_id = get_user_state(user_email)
        st.session_state["user_email"] = user_email
        st.session_state["user_state"] = state
        st.session_state["role_id"] = role_id or "rm"
        # Override browser-detected lang with Firestore preference (returning users)
        if not st.session_state.get("_lang_from_profile"):
            profile = get_profile(user_email)
            if profile and profile.get("lang") in ("en", "zh"):
                st.session_state["lang"] = profile["lang"]
                st.session_state["_lang_from_profile"] = True
    except Exception as e:
        from utils.i18n import t
        _lang = st.session_state.get("lang", "en")
        st.error(t("app.db_error", _lang) + f"\n\n_{e}_")
        st.stop()

user_email: str = st.session_state["user_email"]
user_state: str = st.session_state.get("user_state", "new_user")

# ── Route new users and users who haven't completed diagnostic ─────────────────
PAGE_MAP = {
    "new_user":         "pages/00_Welcome.py",
    "needs_diagnostic": "pages/01_Diagnostic.py",
    "needs_course":     "pages/02_Skills_Profile.py",
}
if user_state in PAGE_MAP:
    st.switch_page(PAGE_MAP[user_state])

# ── Default landing for in_training / completed users ─────────────────────────
st.switch_page("pages/03_Home.py")
