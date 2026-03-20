"""
Skills Profile page.
Shows domain scores, gap map, assessment history.
Allows retake diagnostic and build/view course.
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go

from utils.auth import get_user_email
from utils.db import (
    get_profile, get_latest_diagnostic, get_all_diagnostics,
    get_latest_gap_map, get_all_progress, create_progress,
)
from utils.scoring import (
    DOMAIN_DISPLAY_NAMES, DOMAIN_IDS,
    get_level_label, calculate_overall_score,
    compute_current_domain_scores,
)
from utils.sequencing import compute_module_sequence
from utils.styles import inject_global_css, section_header, render_sidebar
from utils.content import get_course
from utils.i18n import t

st.set_page_config(
    page_title="Skills Profile | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

user_email = get_user_email()

# ── Guard: must have completed diagnostic ─────────────────────────────────────
profile = get_profile(user_email)
if not profile:
    st.switch_page("pages/00_Welcome.py")


# ── Load data ─────────────────────────────────────────────────────────────────
def load_latest_diagnostic():
    return get_latest_diagnostic(user_email)

def load_all_diagnostics():
    return get_all_diagnostics(user_email)

def load_latest_gap_map():
    return get_latest_gap_map(user_email)

def load_training_progress():
    return get_all_progress(user_email)

def load_eval_domain_scores(progress_rows):
    """Build a list of {domain_id: score} dicts from completed evaluations."""
    result = []
    for r in progress_rows:
        if r.get("evaluation_completed_at") and r.get("domain_score_after") is not None:
            try:
                course = get_course(r["course_id"])
                domain = course["primary_domain"]
                result.append({domain: float(r["domain_score_after"])})
            except (KeyError, TypeError, ValueError):
                pass
    return result


_lang = st.session_state.get("lang", "en")

# Profile-based lang override (runs once per session after profile load)
if not st.session_state.get("_lang_from_profile") and profile and profile.get("lang") in ("en", "zh"):
    st.session_state["lang"] = profile["lang"]
    st.session_state["_lang_from_profile"] = True
    _lang = profile["lang"]

try:
    latest_diag = load_latest_diagnostic()
    all_diags = load_all_diagnostics()
    gap_map_row = load_latest_gap_map()
    progress_rows = load_training_progress()
    eval_domain_scores = load_eval_domain_scores(progress_rows)
except Exception as e:
    st.error(t("profile.error_load", _lang) + f"\n\n_{e}_")
    st.stop()

if not latest_diag:
    st.info(t("profile.no_diag_info", _lang))
    if st.button(t("profile.take_diag_btn", _lang), type="primary"):
        st.switch_page("pages/01_Diagnostic.py")
    st.stop()

# Parse domain scores
try:
    diag_domain_scores = json.loads(latest_diag.get("domain_scores") or "{}")
except (json.JSONDecodeError, TypeError):
    diag_domain_scores = {}

# Build current domain scores with equal-weight per item (TDD §8)
current_domain_scores = compute_current_domain_scores(diag_domain_scores, eval_domain_scores)

overall = calculate_overall_score(current_domain_scores)
level_label = get_level_label(overall)
has_course = len(progress_rows) > 0
assessed_date = str(latest_diag.get("completed_at", ""))[:10] if latest_diag else "—"

display_name = profile.get("display_name", user_email.split("@")[0].title())

# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar("skills_profile", has_course=has_course, progress_rows=progress_rows,
               user_email=user_email, lang=_lang)


# ── Page header ───────────────────────────────────────────────────────────────
_role_id = profile.get("role_id", "rm")
from utils.content import ROLES as _ROLES
_role_title = _ROLES.get(_role_id, {}).get("title", _role_id.upper())

col_h, col_date = st.columns([4, 1])
with col_h:
    st.title(t("profile.title", _lang))
    st.markdown(
        f'<div style="font-family:\'Inter\',sans-serif; font-size:0.85rem; color:#8990A8">'
        f'{t("profile.role_label", _lang).format(role=_role_title)}</div>',
        unsafe_allow_html=True,
    )
with col_date:
    st.markdown(
        f'<div style="font-family:\'IBM Plex Mono\',monospace; font-size:0.75rem; '
        f'color:#8990A8; text-align:right; margin-top:1.2rem">{t("profile.last_assessed_label", _lang)}<br>{assessed_date}</div>',
        unsafe_allow_html=True,
    )

# ── Overall score hero + domain scores ────────────────────────────────────────
col_score, col_domains = st.columns([2, 3])
with col_score:
    st.metric(label=level_label, value=f"{overall:.1f} / 4.0")

with col_domains:
    section_header(t("profile.domain_scores_header", _lang))
    # Shortened axis labels — full names overflow on a 6-axis radar
    _short_names = {
        "responsible_ai":      "Resp. AI",
        "strategic_prompting": "Prompting",
        "critical_eval":       "Crit. Eval",
        "relationship_intel":  "Rel. Intel",
        "data_decision":       "Data Dec.",
        "augmented_comm":      "Comm.",
    }
    _cats = [_short_names.get(d, d) for d in DOMAIN_IDS]
    _vals = []
    for _d in DOMAIN_IDS:
        try:
            _vals.append(float(current_domain_scores.get(_d, 0.0)))
        except (TypeError, ValueError):
            _vals.append(0.0)
    # Close the polygon by repeating first point
    _fig = go.Figure(go.Scatterpolar(
        r=_vals + [_vals[0]],
        theta=_cats + [_cats[0]],
        fill="toself",
        fillcolor="rgba(0,212,232,0.12)",
        line=dict(color="#00D4E8", width=2),
        mode="lines+markers",
        marker=dict(color="#00D4E8", size=6),
    ))
    _fig.update_layout(
        polar=dict(
            bgcolor="#161A22",
            gridshape="linear",
            angularaxis=dict(
                tickfont=dict(color="#8990A8", size=11, family="Inter, sans-serif"),
                linecolor="#2A2F3E",
                gridcolor="#2A2F3E",
            ),
            radialaxis=dict(
                range=[0, 4],
                tickvals=[1, 2, 3, 4],
                showticklabels=False,
                linecolor="#2A2F3E",
                gridcolor="#2A2F3E",
            ),
        ),
        paper_bgcolor="#0D0F14",
        margin=dict(l=40, r=40, t=20, b=20),
        height=320,
        showlegend=False,
    )
    st.plotly_chart(_fig, use_container_width=True, config={"displayModeBar": False})

# ── Gap Map ───────────────────────────────────────────────────────────────────
section_header(t("profile.gap_map_header", _lang))

if gap_map_row:
    try:
        bullets = json.loads(gap_map_row.get("bullets") or "[]")
    except (json.JSONDecodeError, TypeError):
        bullets = []

    if bullets:
        # Build all HTML in one st.markdown() call — splitting across multiple calls causes
        # Streamlit to auto-close the opening <div> immediately, leaving an empty card box.
        parts = ['<div class="aha-card">']
        parts.append(
            '<div style="display:flex; gap:1.25rem; margin-bottom:1rem; font-family:\'Inter\',sans-serif;'
            ' font-size:0.72rem; color:#8990A8; text-transform:uppercase; letter-spacing:0.06em">'
            f'<span><span class="gap-priority-dot high" style="display:inline-block; vertical-align:middle; margin-right:0.35rem"></span>{t("profile.gap_priority_critical", _lang)}</span>'
            f'<span><span class="gap-priority-dot medium" style="display:inline-block; vertical-align:middle; margin-right:0.35rem"></span>{t("profile.gap_priority_needs", _lang)}</span>'
            f'<span><span class="gap-priority-dot low" style="display:inline-block; vertical-align:middle; margin-right:0.35rem"></span>{t("profile.gap_priority_on_track", _lang)}</span>'
            '</div>'
        )
        for b in sorted([b for b in bullets if isinstance(b, dict)], key=lambda x: x.get("priority", 99)):
            domain_id = b.get("domain_id", "")
            domain_score = current_domain_scores.get(domain_id, 0.0)
            try:
                domain_score = float(domain_score)
            except (TypeError, ValueError):
                domain_score = 0.0
            dot_class = "high" if domain_score < 1.5 else ("medium" if domain_score < 2.5 else "low")
            domain_name_display = DOMAIN_DISPLAY_NAMES.get(domain_id, domain_id)
            bullet_text = b.get("bullet", "")
            parts.append(
                f'<div class="gap-bullet">'
                f'<div class="gap-priority-dot {dot_class}"></div>'
                f'<div><div class="gap-domain-name">{domain_name_display}</div>'
                f'<div class="gap-bullet-text">{bullet_text}</div></div>'
                f'</div>'
            )
        parts.append('</div>')
        st.markdown("".join(parts), unsafe_allow_html=True)
    else:
        st.info(t("profile.gap_generating_info", _lang))
else:
    st.markdown(
        f'<div class="aha-card-accent"><div style="font-size:0.88rem; color:#8990A8">'
        f'{t("profile.gap_generating_card", _lang)}</div></div>',
        unsafe_allow_html=True,
    )

# ── Assessment History ─────────────────────────────────────────────────────────
if len(all_diags) > 0:
    section_header(t("profile.history_header", _lang))
    rows = []
    for diag in all_diags:
        date_str = str(diag.get("completed_at", ""))[:10]
        ov = float(diag.get("overall_score") or 0)
        try:
            ds = json.loads(diag.get("domain_scores") or "{}")
        except (json.JSONDecodeError, TypeError):
            ds = {}
        rows.append({
            "Date": date_str,
            "Overall": round(ov, 1),
            "Resp. AI": round(float(ds.get("responsible_ai", 0)), 1),
            "Prompting": round(float(ds.get("strategic_prompting", 0)), 1),
            "Crit. Eval": round(float(ds.get("critical_eval", 0)), 1),
            "Rel. Intel": round(float(ds.get("relationship_intel", 0)), 1),
            "Data Dec.": round(float(ds.get("data_decision", 0)), 1),
            "Comm.": round(float(ds.get("augmented_comm", 0)), 1),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ── Action buttons ─────────────────────────────────────────────────────────────
section_header(t("profile.actions_header", _lang))
col_a, col_b = st.columns([1, 1])

with col_a:
    if st.button(t("profile.retake_btn", _lang), use_container_width=True):
        # Clear any lingering diagnostic session state
        for k in ["diag_item_index", "diag_responses", "diag_session_started", "diag_started"]:
            st.session_state.pop(k, None)
        st.switch_page("pages/01_Diagnostic.py")

with col_b:
    if not has_course:
        if st.button(t("profile.build_course_btn", _lang), use_container_width=True, type="primary"):
            with st.spinner(t("profile.spinner_course", _lang)):
                try:
                    sequence = compute_module_sequence(current_domain_scores, role_id=profile["role_id"])
                    for i, course_id in enumerate(sequence):
                        create_progress(user_email, course_id, i + 1, is_locked=(i > 0))
                    st.session_state["user_state"] = "in_training"
                    st.switch_page("pages/03_Home.py")
                except Exception as e:
                    st.error(t("profile.error_course", _lang) + f"\n\n_{e}_")
    else:
        if st.button(t("profile.view_course_btn", _lang), use_container_width=True, type="primary"):
            st.switch_page("pages/03_Home.py")
