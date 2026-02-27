"""
Welcome page — shown to users with no profile record.
Handles role selection and profile creation.
"""

import streamlit as st
import uuid
import os
from utils.auth import get_user_email
from utils.db import execute, query_one, escape
from utils.styles import inject_global_css
from utils.content import ROLES

st.set_page_config(
    page_title="Welcome | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()

user_email = get_user_email()

# Guard: if user already has a profile, route to the correct page for their state
existing = query_one(
    "SELECT role_id FROM users WHERE user_email = ?",
    [user_email],
)
if existing:
    st.session_state["user_email"] = user_email
    session = query_one(
        "SELECT session_id FROM diagnostic_sessions "
        "WHERE user_email = ? AND completed_at IS NOT NULL "
        "ORDER BY completed_at DESC LIMIT 1",
        [user_email],
    )
    if not session:
        st.session_state["user_state"] = "needs_diagnostic"
        st.switch_page("pages/01_Diagnostic.py")
    progress = query_one(
        "SELECT progress_id FROM training_progress "
        "WHERE user_email = ? LIMIT 1",
        [user_email],
    )
    if not progress:
        st.session_state["user_state"] = "needs_course"
        st.switch_page("pages/02_Skills_Profile.py")
    st.session_state["user_state"] = "in_training"
    st.switch_page("pages/03_Home.py")


# ── Brand mark ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="aha-brand" style="margin-bottom: 3rem;">
  <div class="aha-brand-icon">⚡</div>
  <div class="aha-brand-name">AI <span>Hero</span> Academy</div>
</div>
""", unsafe_allow_html=True)

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="welcome-hero">
  <div class="welcome-eyebrow">AI Hero Academy · Skills Training</div>
  <div class="welcome-headline">
    Master the AI skills<br>that matter for <em>your</em> job.
  </div>
  <div class="welcome-body">
    This is not a course about AI.<br>
    It is practice <strong>using AI</strong> for your actual work — through real scenarios,
    hands-on experiments, and AI coaching grounded in your role.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Value props ────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
<div class="aha-card">
  <div style="font-size:1.5rem; margin-bottom:0.6rem">🎯</div>
  <div style="font-family:'Inter',sans-serif; font-weight:600; font-size:0.9rem; color:#EDF0F7; margin-bottom:0.4rem">
    Diagnose your gaps
  </div>
  <div style="font-family:'Inter',sans-serif; font-size:0.82rem; color:#8990A8; line-height:1.6">
    A 5-minute diagnostic reveals exactly where you stand across 4 AI skill domains.
  </div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="aha-card">
  <div style="font-size:1.5rem; margin-bottom:0.6rem">🗺️</div>
  <div style="font-family:'Inter',sans-serif; font-weight:600; font-size:0.9rem; color:#EDF0F7; margin-bottom:0.4rem">
    Get a personalised path
  </div>
  <div style="font-family:'Inter',sans-serif; font-size:0.82rem; color:#8990A8; line-height:1.6">
    Your training sequence is built around your gaps — not a generic curriculum.
  </div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="aha-card">
  <div style="font-size:1.5rem; margin-bottom:0.6rem">🤖</div>
  <div style="font-family:'Inter',sans-serif; font-weight:600; font-size:0.9rem; color:#EDF0F7; margin-bottom:0.4rem">
    Learn by doing
  </div>
  <div style="font-family:'Inter',sans-serif; font-size:0.82rem; color:#8990A8; line-height:1.6">
    Real scenarios. An AI coach that responds to your actual answers. No passive videos.
  </div>
</div>
""", unsafe_allow_html=True)


# ── Role selection + CTA ──────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:480px">
  <div style="font-family:'Inter',sans-serif; font-size:0.8rem; font-weight:600;
              text-transform:uppercase; letter-spacing:0.08em; color:#8990A8;
              margin-bottom:0.6rem">
    Your Role
  </div>
</div>
""", unsafe_allow_html=True)

# Build role options from content — {title: role_id}, ordered by roles.json insertion order
_role_map = {v["title"]: k for k, v in ROLES.items()}
_available_roles = list(_role_map.keys())
_derived_name = user_email.split("@")[0].replace(".", " ").title()

col_sel, col_btn = st.columns([2, 1], gap="medium")

with col_sel:
    # CX8: show a role card when there is only one role; use selectbox when multiple roles exist
    if len(_available_roles) == 1:
        st.info(f"Your role: **{_available_roles[0]}**")
        selected_role = _available_roles[0]
    else:
        selected_role = st.selectbox(
            "Select your role",
            options=["— Select your role —"] + _available_roles,
            label_visibility="collapsed",
            key="welcome_role",
        )

    # CX7: show derived display name with an editable override
    display_name_val = st.text_input(
        "Display name",
        value=_derived_name,
        key="welcome_display_name",
        help="This is how you will be greeted throughout the app. Edit if needed.",
    )

role_selected = selected_role not in ("— Select your role —",)

with col_btn:
    if st.button(
        "Start My Diagnostic →",
        disabled=not role_selected,
        use_container_width=True,
        type="primary",
    ):
        with st.spinner("Setting up your profile..."):
            try:
                display_name = display_name_val.strip() if display_name_val.strip() else _derived_name
                role_id = _role_map.get(selected_role, "rm")
                execute(
                    "INSERT INTO users "
                    "(user_email, display_name, role_id) "
                    "VALUES (?, ?, ?)",
                    [user_email, display_name, role_id]
                )
                st.session_state["user_email"] = user_email
                st.session_state["user_state"] = "needs_diagnostic"
                st.switch_page("pages/01_Diagnostic.py")
            except Exception as err:
                st.error(f"Could not create your profile. Please refresh and try again.\n\n_{err}_")


# ── Footer note ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.78rem; color:#8990A8;
            border-top:1px solid #2A2F3E; padding-top:1.2rem; max-width:540px">
  Your scores and practice conversations are visible only to you.
  No manager dashboard. No rankings. Just your growth.
</div>
""", unsafe_allow_html=True)
