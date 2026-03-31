"""
Home page — course progress dashboard.
Shown to users who have a course created (in_training or completed state).
"""

import streamlit as st
import json
from datetime import datetime

from utils.auth import get_user_email
from utils.db import get_profile, get_latest_diagnostic, get_all_progress, get_assembled_path
from utils.scoring import (
    DOMAIN_DISPLAY_NAMES, get_level_label, get_domain_display_name, get_score_color,
    calculate_overall_score, compute_current_domain_scores,
)
from utils.styles import inject_global_css, section_header, render_sidebar
from utils.content import get_course, get_atomic_modules
from utils.i18n import t

st.set_page_config(
    page_title="My Training | AI Hero Academy",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

user_email = get_user_email()

# ── Guards ────────────────────────────────────────────────────────────────────
profile = get_profile(user_email)
if not profile:
    st.switch_page("pages/00_Welcome.py")

diag = get_latest_diagnostic(user_email)
if not diag:
    st.switch_page("pages/01_Diagnostic.py")

_raw_progress = get_all_progress(user_email)
if not _raw_progress:
    st.switch_page("pages/02_Skills_Profile.py")

# Resolve lang early so content getters below can use it
_lang = st.session_state.get("lang", "en")
if not st.session_state.get("_lang_from_profile") and profile and profile.get("lang") in ("en", "zh"):
    st.session_state["lang"] = profile["lang"]
    st.session_state["_lang_from_profile"] = True
    _lang = profile["lang"]

progress_rows = []
for _row in _raw_progress:
    _course = get_course(_row["course_id"], lang=_lang)
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
level_label = get_level_label(overall, _lang)
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
render_sidebar("home", has_course=True, progress_rows=progress_rows,
               user_email=user_email, lang=_lang)


# ── Greeting ──────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="font-family:\'DM Serif Display\',serif; font-size:1.5rem; '
    f'color:#EDF0F7; margin-bottom:0.2rem">{t("home.greeting", _lang).format(name=display_name)}</div>',
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
        f'color:#8990A8; margin-top:0.5rem">{t("home.last_updated_label", _lang).format(date=last_updated_str)}</div>'
        if last_updated_str else ""
    )
    _modules_progress_str = t("home.modules_progress", _lang).format(done=completed_count, total=total_modules)
    st.markdown(f"""
<div class="aha-card" style="display:flex; gap:2rem; align-items:center">
  <div>
    <div style="display:flex; align-items:baseline; gap:0.35rem">
      <div style="font-family:'JetBrains Mono',monospace; font-size:2.2rem;
                  color:{color_hex}; line-height:1">{overall:.1f}</div>
      <div style="font-size:1.3rem; color:{trend_color}; line-height:1">{trend_arrow}</div>
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem;
                color:#8990A8">/ 4.0</div>
    <div style="font-family:'Inter',sans-serif; font-size:0.72rem; font-weight:600;
                text-transform:uppercase; letter-spacing:0.08em; color:#8990A8;
                margin-top:0.25rem">{level_label}</div>
  </div>
  <div style="flex:1; border-left:1px solid #2A2F3E; padding-left:1.5rem">
    <div style="font-family:'Inter',sans-serif; font-size:0.82rem; color:#8990A8;
                margin-bottom:0.5rem">
      {_modules_progress_str}
    </div>
    <div class="themed-progress-track">
      <div class="themed-progress-fill" style="width:{int(completed_count/total_modules*100)}%"></div>
    </div>
    {last_updated_html}
  </div>
</div>
""", unsafe_allow_html=True)
    if st.button(t("home.view_profile_btn", _lang), use_container_width=False, key="view_profile_btn", type="primary"):
        st.switch_page("pages/02_Skills_Profile.py")

# ── Assembled atom path (new-intake users) or legacy course list ──────────────
_assembled_path = get_assembled_path(user_email)

if _assembled_path:
    # ── Atom-path rendering ───────────────────────────────────────────────────
    _atoms_by_id = {
        a["atom_id"]: a
        for a in get_atomic_modules()
        if a.get("status") in ("canonical", "role-variant", "capstone")
    }
    # Build a lookup: source_course_id -> progress row
    _course_progress_map = {r.get("course_id", ""): r for r in _raw_progress}

    section_header(t("home.course_header", _lang))

    _SVG_LOCK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>'
    _SVG_CHECK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--accent_green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'

    def _badge(label, state):
        return f'<span class="sub-badge {state}">{label}</span>'

    for _atom_seq, _atom_id in enumerate(_assembled_path, start=1):
        _atom = _atoms_by_id.get(_atom_id)
        if _atom is None:
            continue  # atom removed from content — skip silently

        _atom_domain = _atom.get("domain", "")
        _atom_domain_display = get_domain_display_name(_atom_domain, _lang)
        _atom_minutes = _atom.get("estimated_minutes", 0)

        # Determine completion: any source_course_id with evaluation_completed_at
        _source_ids = _atom.get("source_course_ids") or []
        _atom_eval_done = any(
            bool(_course_progress_map.get(cid, {}).get("evaluation_completed_at"))
            for cid in _source_ids
        )
        _atom_reading_done = any(
            bool(_course_progress_map.get(cid, {}).get("reading_completed_at"))
            for cid in _source_ids
        )
        _atom_practice_done = any(
            bool(_course_progress_map.get(cid, {}).get("practice_completed_at"))
            for cid in _source_ids
        )

        if _atom_eval_done:
            _atom_card_state = "completed"
        else:
            _atom_card_state = "active"

        _num_color = "#00D4E8" if _atom_card_state == "active" else "#29CC6A"

        with st.container(border=True):
            _col_num, _col_body, _col_time = st.columns([1, 7, 2])
            with _col_num:
                st.markdown(
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.9rem;'
                    f'font-weight:700;color:{_num_color};padding-top:0.3rem">'
                    f'{str(_atom_seq).zfill(2)}</div>',
                    unsafe_allow_html=True,
                )
            with _col_body:
                _done_icon = f'{_SVG_CHECK} ' if _atom_card_state == "completed" else ""
                _r_state = "done" if _atom_reading_done else "current"
                _p_state = "done" if _atom_practice_done else ("current" if _atom_reading_done else "pending")
                _q_state = "done" if _atom_eval_done else ("current" if _atom_practice_done else "pending")
                st.markdown(
                    f'<div>'
                    f'<div class="module-title">{_done_icon}{_atom.get("title", _atom_id)}</div>'
                    f'<div style="margin-top:0.3rem"><span class="module-domain-tag">{_atom_domain_display}</span></div>'
                    f'<div class="sub-strip">'
                    f'{_badge(t("home.badge_read", _lang), _r_state)}'
                    f'{_badge(t("home.badge_practice", _lang), _p_state)}'
                    f'{_badge(t("home.badge_quiz", _lang), _q_state)}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with _col_time:
                if _atom_minutes:
                    st.markdown(
                        f'<div style="text-align:right;font-family:\'JetBrains Mono\',monospace;'
                        f'font-size:0.75rem;color:#8990A8">{_atom_minutes} min</div>',
                        unsafe_allow_html=True,
                    )

            if _atom_card_state == "active":
                if not _atom_reading_done:
                    _atom_btn_label = t("home.start_module_btn", _lang).format(n=_atom_seq)
                elif not _atom_practice_done:
                    _atom_btn_label = t("home.continue_practice_btn", _lang)
                else:
                    _atom_btn_label = t("home.take_quiz_btn", _lang)
                if st.button(_atom_btn_label, key=f"atom_btn_{_atom_id}", use_container_width=True, type="primary"):
                    st.session_state["active_atom_id"] = _atom_id
                    st.session_state.pop("active_course_id", None)
                    if not _atom_reading_done:
                        st.session_state["active_submodule"] = "overview"
                    elif not _atom_practice_done:
                        st.session_state["active_submodule"] = "practice"
                    else:
                        st.session_state["active_submodule"] = "evaluation"
                    st.switch_page("pages/04_Course_Module.py")
            elif _atom_card_state == "completed":
                if st.button(
                    t("home.review_module_btn", _lang).format(n=_atom_seq),
                    key=f"atom_btn_{_atom_id}",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state["active_atom_id"] = _atom_id
                    st.session_state.pop("active_course_id", None)
                    st.session_state["active_submodule"] = "results"
                    st.switch_page("pages/04_Course_Module.py")

else:
    # ── Legacy role-based course list ─────────────────────────────────────────
    section_header(t("home.course_header", _lang))

    _SVG_LOCK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>'
    _SVG_CHECK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--accent_green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'

    def _badge(label, state):
        return f'<span class="sub-badge {state}">{label}</span>'

    _read_label = t("home.badge_read", _lang)
    _practice_label = t("home.badge_practice", _lang)
    _quiz_label = t("home.badge_quiz", _lang)

    for row in progress_rows:
        seq = int(row.get("module_sequence_order", 0))
        title = row.get("course_title", f"Module {seq}")
        domain = row.get("primary_domain", "")
        domain_display = get_domain_display_name(domain, _lang)
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
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.9rem;'
                    f'font-weight:700;color:{num_color};padding-top:0.3rem;{opacity}">'
                    f'{str(seq).zfill(2)}</div>',
                    unsafe_allow_html=True,
                )
            with col_body:
                lock_icon = f'{_SVG_LOCK} ' if is_locked else ""
                _locked_hint_html = (
                    f'<div style="font-size:0.75rem;color:var(--text-faint);margin-top:0.2rem">'
                    f'{t("home.locked_hint", _lang).format(n=seq-1)}</div>'
                    if is_locked and seq > 1 else ""
                )
                st.markdown(
                    f'<div style="{opacity}">'
                    f'<div class="module-title">{lock_icon}{title}</div>'
                    f'{_locked_hint_html}'
                    f'<div style="margin-top:0.3rem"><span class="module-domain-tag">{domain_display}</span></div>'
                    f'<div class="sub-strip">{_badge(_read_label, r_state)}{_badge(_practice_label, p_state)}{_badge(_quiz_label, q_state)}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col_score:
                if card_state == "completed" and eval_score is not None:
                    try:
                        st.markdown(
                            f'<div style="text-align:right;font-family:\'JetBrains Mono\',monospace;'
                            f'font-size:0.82rem;color:#29CC6A">{float(eval_score):.1f} / 4.0</div>',
                            unsafe_allow_html=True,
                        )
                    except (TypeError, ValueError):
                        pass

            if card_state == "active":
                if not reading_done:
                    btn_label = t("home.start_module_btn", _lang).format(n=seq)
                elif not practice_done:
                    btn_label = t("home.continue_practice_btn", _lang)
                else:
                    btn_label = t("home.take_quiz_btn", _lang)
                if st.button(btn_label, key=f"module_btn_{seq}", use_container_width=True, type="primary"):
                    st.session_state["active_course_id"] = course_id
                    if not reading_done:
                        st.session_state["active_submodule"] = "overview"
                    elif not practice_done:
                        st.session_state["active_submodule"] = "practice"
                    else:
                        st.session_state["active_submodule"] = "evaluation"
                    st.switch_page("pages/04_Course_Module.py")
            elif card_state == "completed":
                if st.button(t("home.review_module_btn", _lang).format(n=seq), key=f"module_btn_{seq}", type="secondary", use_container_width=True):
                    st.session_state["active_course_id"] = course_id
                    # Jump directly to results if fully complete; overview otherwise (UI2)
                    all_done = (
                        row.get("reading_completed_at")
                        and row.get("practice_completed_at")
                        and row.get("evaluation_completed_at")
                    )
                    st.session_state["active_submodule"] = "results" if all_done else "overview"
                    st.switch_page("pages/04_Course_Module.py")

