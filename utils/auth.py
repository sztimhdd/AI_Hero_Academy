import os


def get_user_email() -> str:
    """
    Returns the authenticated user's email address.
    In demo mode, returns the virtual email for the active persona.
    In Databricks Apps, injected as DATABRICKS_USER_EMAIL env var.
    Falls back to DEV_USER_EMAIL for local development.
    """
    try:
        import streamlit as st
        if st.session_state.get("demo_mode"):
            demo_id = st.session_state.get("demo_profile_id", "3a")
            from utils.demo import DEMO_PROFILES
            return DEMO_PROFILES[demo_id]["email"]
    except Exception:
        pass

    email = os.environ.get("DATABRICKS_USER_EMAIL")
    if not email:
        email = os.environ.get("DEV_USER_EMAIL", "dev@example.com")
    return email
