"""
Home page — course progress dashboard.
Shown to users who have a course created (in_training or completed state).
"""

import streamlit as st
import json
import os
from datetime import datetime

from utils.auth import get_user_email
from utils.db import execute, query_one
from utils.scoring import (
    DOMAIN_DISPLAY_NAMES, get_level_label, get_score_color,
    calculate_overall_score, compute_current_domain_scores,
)
from utils.styles import inject_global_css, section_header, render_sidebar
from utils.content import get_course

st.set_page_config(
    page_title="My Training | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")
user_email = get_user_email()

# ── Guards ────────────────────────────────────────────────────────────────────
profile = query_one(
    f"SELECT display_name, role_id FROM {CATALOG}.learner.user_profiles "
    f"WHERE user_email = ?",
    [user_email],
)
if not profile:
    st.switch_page("pages/00_Welcome.py")

diag = query_one(
    f"SELECT session_id, domain_scores, overall_score, completed_at "
    f"FROM {CATALOG}.learner.diagnostic_sessions "
    f"WHERE user_email = ? AND completed_at IS NOT NULL "
    f"ORDER BY completed_at DESC LIMIT 1",
    [user_email],
)
if not diag:
    st.switch_page("pages/01_Diagnostic.py")

_raw_progress = execute(
    f"SELECT progress_id, course_id, module_sequence_order, "
    f"is_locked, reading_completed_at, practice_completed_at, "
    f"evaluation_completed_at, evaluation_score, domain_score_after "
    f"FROM {CATALOG}.learner.training_progress "
    f"WHERE user_email = ? "
    f"ORDER BY module_sequence_order",
    [user_email],
)
if not _raw_progress:
    st.switch_page("pages/02_Skills_Profile.py")

progress_rows = []
for _row in _raw_progress:
    _course = get_course(_row["course_id"])
    progress_rows.append({**_row, "course_title": _course["title"], "primary_domain": _course["primary_domain"]})


# ── Derive current domain scores ──────────────────────────────────────────────
try:
    diag_domain_scores = json.loads(diag.get("domain_scores") or "{}")
except (json.JSONDecodeError, TypeError):
    diag_domain_scores = {}

# Build eval_domain_scores list from completed evaluations
eval_domain_scores_home = []
for row in progress_rows:
    if row.get("evaluation_completed_at") and row.get("domain_score_after") is not None:
        domain = row.get("primary_domain")
        if domain:
            try:
                eval_domain_scores_home.append({domain: float(row["domain_score_after"])})
            except (TypeError, ValueError):
                pass

# Build current domain scores with equal-weight per item (TDD §8)
current_domain_scores = compute_current_domain_scores(diag_domain_scores, eval_domain_scores_home)

overall = calculate_overall_score(current_domain_scores)
level_label = get_level_label(overall)
display_name = profile.get("display_name", user_email.split("@")[0].title())

# ── Trend indicator: current composite score vs diagnostic baseline ────────────
try:
    diag_overall = float(diag.get("overall_score") or 0)
except (TypeError, ValueError):
    diag_overall = overall

diff = overall - diag_overall
if diff > 0.1:
    trend_arrow, trend_color = "↑", "#29CC6A"
elif diff < -0.1:
    trend_arrow, trend_color = "↓", "#E8455A"
else:
    trend_arrow, trend_color = "→", "#8990A8"

# ── Last updated: most recent activity across diagnostic + evaluations ─────────
def _parse_ts(val):
    if val is None:
        return None
    if hasattr(val, "year"):
        return val
    try:
        return datetime.strptime(str(val)[:19].replace("T", " "), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

last_updated = _parse_ts(diag.get("completed_at"))
for _r in progress_rows:
    _eval_at = _parse_ts(_r.get("evaluation_completed_at"))
    if _eval_at and (last_updated is None or _eval_at > last_updated):
        last_updated = _eval_at

last_updated_str = (
    last_updated.strftime("%b %d, %Y").replace(" 0", " ")
    if last_updated else None
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar("home", has_course=True, progress_rows=progress_rows)


# ── Greeting ──────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="font-family:\'DM Serif Display\',serif; font-size:2rem; '
    f'color:#EDF0F7; margin-bottom:0.2rem">Welcome back, {display_name}.</div>',
    unsafe_allow_html=True,
)

# ── Summary card ──────────────────────────────────────────────────────────────
completed_count = sum(1 for r in progress_rows if r.get("evaluation_completed_at"))
total_modules = len(progress_rows)

col_card, col_spacer = st.columns([3, 2])
with col_card:
    color_class = get_score_color(overall)
    color_hex = {"danger": "#E8455A", "warning": "#F5A623", "success": "#29CC6A"}.get(color_class, "#00D4E8")
    last_updated_html = (
        f'<div style="font-family:\'Inter\',sans-serif; font-size:0.72rem; '
        f'color:#8990A8; margin-top:0.5rem">Last updated: {last_updated_str}</div>'
        if last_updated_str else ""
    )
    st.markdown(f"""
<div class="aha-card" style="display:flex; gap:2rem; align-items:center">
  <div>
    <div style="display:flex; align-items:baseline; gap:0.35rem">
      <div style="font-family:'IBM Plex Mono',monospace; font-size:2.2rem;
                  color:{color_hex}; line-height:1">{overall:.1f}</div>
      <div style="font-size:1.3rem; color:{trend_color}; line-height:1">{trend_arrow}</div>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem;
                color:#8990A8">/ 4.0</div>
    <div style="font-family:'Inter',sans-serif; font-size:0.72rem; font-weight:600;
                text-transform:uppercase; letter-spacing:0.08em; color:#8990A8;
                margin-top:0.25rem">{level_label}</div>
  </div>
  <div style="flex:1; border-left:1px solid #2A2F3E; padding-left:1.5rem">
    <div style="font-family:'Inter',sans-serif; font-size:0.82rem; color:#8990A8;
                margin-bottom:0.5rem">
      {completed_count} of {total_modules} modules complete
    </div>
    <div style="background:#1E2330; border-radius:4px; height:6px; overflow:hidden">
      <div style="height:100%; width:{int(completed_count/total_modules*100)}%;
                  background:linear-gradient(90deg,#00D4E8,#0099AA);
                  border-radius:4px; transition:width 0.5s ease"></div>
    </div>
    {last_updated_html}
  </div>
</div>
""", unsafe_allow_html=True)
    if st.button("→  View Full Skills Profile", use_container_width=False, key="view_profile_btn", type="primary"):
        st.switch_page("pages/02_Skills_Profile.py")

# ── Course progress ────────────────────────────────────────────────────────────
section_header("MY TRAINING COURSE")


def _badge(label, state):
    return f'<span class="sub-badge {state}">{label}</span>'


for row in progress_rows:
    seq = int(row.get("module_sequence_order", 0))
    title = row.get("course_title", f"Module {seq}")
    domain = row.get("primary_domain", "")
    domain_display = DOMAIN_DISPLAY_NAMES.get(domain, domain)
    is_locked = str(row.get("is_locked", "true")).lower() == "true"
    reading_done = bool(row.get("reading_completed_at"))
    practice_done = bool(row.get("practice_completed_at"))
    eval_done = bool(row.get("evaluation_completed_at"))
    eval_score = row.get("evaluation_score")
    course_id = row.get("course_id", "")

    # Determine state
    if is_locked:
        card_state = "locked"
    elif eval_done:
        card_state = "completed"
    else:
        card_state = "active"

    # Sub-module badge states
    if card_state == "completed":
        r_state, p_state, q_state = "done", "done", "done"
    elif card_state == "active":
        if not reading_done:
            r_state, p_state, q_state = "current", "pending", "pending"
        elif not practice_done:
            r_state, p_state, q_state = "done", "current", "pending"
        else:
            r_state, p_state, q_state = "done", "done", "current"
    else:
        r_state, p_state, q_state = "pending", "pending", "pending"

    num_color = "#00D4E8" if card_state == "active" else ("#29CC6A" if card_state == "completed" else "#8990A8")
    opacity = "opacity:0.5;" if is_locked else ""

    with st.container(border=True):
        col_num, col_body, col_score = st.columns([1, 7, 2])
        with col_num:
            st.markdown(
                f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.9rem;'
                f'font-weight:700;color:{num_color};padding-top:0.3rem;{opacity}">'
                f'{str(seq).zfill(2)}</div>',
                unsafe_allow_html=True,
            )
        with col_body:
            lock_icon = "🔒 " if is_locked else ""
            st.markdown(
                f'<div style="{opacity}">'
                f'<div class="module-title">{lock_icon}{title}</div>'
                f'<div style="margin-top:0.3rem"><span class="module-domain-tag">{domain_display}</span></div>'
                f'<div class="sub-strip">{_badge("Read", r_state)}{_badge("Practice", p_state)}{_badge("Quiz", q_state)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_score:
            if card_state == "completed" and eval_score is not None:
                try:
                    st.markdown(
                        f'<div style="text-align:right;font-family:\'IBM Plex Mono\',monospace;'
                        f'font-size:0.82rem;color:#29CC6A">{float(eval_score):.1f} / 4.0</div>',
                        unsafe_allow_html=True,
                    )
                except (TypeError, ValueError):
                    pass

        if card_state == "active":
            if not reading_done:
                btn_label = f"Start Module {seq} →"
            elif not practice_done:
                btn_label = f"Continue Practice →"
            else:
                btn_label = f"Take Quiz →"
            if st.button(btn_label, key=f"module_btn_{seq}", use_container_width=True, type="primary"):
                st.session_state["active_course_id"] = course_id
                if not reading_done:
                    st.session_state["active_submodule"] = "reading"
                elif not practice_done:
                    st.session_state["active_submodule"] = "practice"
                else:
                    st.session_state["active_submodule"] = "evaluation"
                st.switch_page("pages/04_Course_Module.py")
        elif card_state == "completed":
            if st.button(f"Review Module {seq}", key=f"module_btn_{seq}", type="secondary", use_container_width=True):
                st.session_state["active_course_id"] = course_id
                # Jump directly to results if fully complete; overview otherwise (UI2)
                all_done = (
                    row.get("reading_completed_at")
                    and row.get("practice_completed_at")
                    and row.get("evaluation_completed_at")
                )
                st.session_state["active_submodule"] = "results" if all_done else "overview"
                st.switch_page("pages/04_Course_Module.py")

