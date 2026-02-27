"""
AI Hero Academy — entry point and router.

On every page load:
1. Read user_email from Databricks SSO context
2. Query Delta to determine user state
3. Route to the appropriate page, or fall through to the main app nav
"""

import streamlit as st
from utils.auth import get_user_email
from utils.db import query_one
from utils.styles import inject_global_css
import os

st.set_page_config(
    page_title="AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")


def get_user_state(user_email: str) -> tuple[str, str | None]:
    """
    Returns (state, role_id) where state is one of:
    new_user | needs_diagnostic | needs_course | in_training
    role_id is None for new_user, otherwise the role from user_profiles.
    """
    profile = query_one(
        f"SELECT role_id FROM {CATALOG}.learner.user_profiles WHERE user_email = ?",
        [user_email],
    )
    if not profile:
        return "new_user", None

    role_id = profile["role_id"]

    session = query_one(
        f"SELECT session_id FROM {CATALOG}.learner.diagnostic_sessions "
        f"WHERE user_email = ? AND completed_at IS NOT NULL "
        f"ORDER BY completed_at DESC LIMIT 1",
        [user_email],
    )
    if not session:
        return "needs_diagnostic", role_id

    progress = query_one(
        f"SELECT progress_id FROM {CATALOG}.learner.training_progress "
        f"WHERE user_email = ? LIMIT 1",
        [user_email],
    )
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
    except Exception as e:
        st.error(f"Unable to connect to the database. Please refresh.\n\n_{e}_")
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
