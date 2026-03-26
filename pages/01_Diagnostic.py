"""
Diagnostic page — Hybrid 2-text + 4-MCQ one-question-at-a-time flow.

Architecture:
  Screen "entry"     — intro card with Begin button
  Screen "q1"        — text question (strategic_prompting)
  Screen "q2"        — text question (critical_eval)
  Screen "generating"— LLM generates 4 personalized MCQs
  Screens "mcq_0"..."mcq_3" — one MCQ per screen, auto-advance on click
  Screen "scoring"   — scores all responses, saves to Firestore, navigates away
"""

import json
import sys
import uuid
from datetime import datetime

import streamlit as st

from utils.auth import get_user_email
from utils.db import (
    get_profile,
    get_latest_diagnostic,
    save_diagnostic,
    save_gap_map,
    save_assembled_path,
)
from utils.ai import generate_diagnostic_mcqs, score_hybrid_diagnostic, generate_gap_map
from utils.path_assembler import assemble_path
from utils.content import get_atomic_modules, get_domain_descriptions
from utils.scoring import get_domain_display_name
from utils.styles import inject_global_css, render_lang_sidebar
from utils.i18n import t

st.set_page_config(
    page_title="Diagnostic | AI Hero Academy",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="auto",
)

inject_global_css()

user_email = get_user_email()

# ── Guard: must have a profile ─────────────────────────────────────────────────
profile = get_profile(user_email)
if not profile:
    st.switch_page("pages/00_Welcome.py")

# ── Language toggle in sidebar ─────────────────────────────────────────────────
_lang = st.session_state.get("lang", "en")
render_lang_sidebar(user_email=user_email, lang=_lang)

# ── Shared state ───────────────────────────────────────────────────────────────
role_id: str = profile["role_id"] if profile else "universal"
domain_descriptions = get_domain_descriptions(role_id, lang=_lang)

# ── Session state init (hybrid diagnostic state machine) ──────────────────────
if "diag_session_started" not in st.session_state:
    st.session_state["diag_session_started"] = str(uuid.uuid4())
    st.session_state["diag_started_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

if "diag_screen" not in st.session_state:
    st.session_state["diag_screen"] = "entry"
if "diag_q1_text" not in st.session_state:
    st.session_state["diag_q1_text"] = ""
if "diag_q2_text" not in st.session_state:
    st.session_state["diag_q2_text"] = ""
if "diag_mcqs" not in st.session_state:
    st.session_state["diag_mcqs"] = []
if "diag_mcq_answers" not in st.session_state:
    st.session_state["diag_mcq_answers"] = {}

# ── Can exit (prior diagnostic exists) ────────────────────────────────────────
_prior_diag = get_latest_diagnostic(user_email)
_can_exit = bool(_prior_diag)

# ── Brand header + optional exit ──────────────────────────────────────────────
col_brand, col_exit = st.columns([5, 1])
with col_brand:
    st.markdown(
        '<div class="aha-brand" style="margin-bottom:2rem">'
        '<div class="aha-brand-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="var(--cyan)">'
        '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>'
        '<div class="aha-brand-name">AI <span>Hero</span> Academy</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with col_exit:
    if _can_exit and st.button(t("diag.exit_btn", _lang), key="diag_exit", use_container_width=True):
        st.switch_page("pages/03_Home.py")


# ── Helpers ────────────────────────────────────────────────────────────────────
def _progress_pill(n: int, total: int = 6) -> str:
    return (
        f'<div class="domain-tag-pill" style="margin-bottom:1.2rem">'
        f'{n} of {total}</div>'
    )


# ── Completion handler ─────────────────────────────────────────────────────────
def _complete_diagnostic(domain_scores: dict, item_scores: dict, overall_score: float) -> None:
    session_id = st.session_state.get("diag_session_started", str(uuid.uuid4()))
    started_at = st.session_state.get("diag_started_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

    # Build responses dict for persistence
    resp_json = json.dumps({
        "q1": st.session_state.get("diag_q1_text", ""),
        "q2": st.session_state.get("diag_q2_text", ""),
        "mcq_answers": st.session_state.get("diag_mcq_answers", {}),
    }, ensure_ascii=False)
    item_scores_json = json.dumps(item_scores, ensure_ascii=False)
    domain_scores_json = json.dumps(domain_scores, ensure_ascii=False)

    try:
        save_diagnostic(
            session_id, user_email, started_at,
            resp_json, item_scores_json, domain_scores_json, overall_score,
        )
    except Exception as e:
        st.error(t("diag.error_save", _lang) + f"\n\n_{e}_")
        st.stop()

    # Gap map generation
    gap_bullets = []
    try:
        gap_bullets = generate_gap_map(
            domain_scores=domain_scores,
            domain_descriptions=domain_descriptions,
            user_email=user_email,
            source_type="diagnostic",
            lang=_lang,
        )
    except Exception as _gap_err:
        print(f"[WARNING] gap_map generation failed after diagnostic: {_gap_err}", file=sys.stderr)
    if gap_bullets:
        try:
            gap_map_id = str(uuid.uuid4())
            bullets_json = json.dumps(gap_bullets, ensure_ascii=False)
            save_gap_map(gap_map_id, user_email, "diagnostic", session_id, bullets_json)
        except Exception as _db_err:
            print(f"[WARNING] gap_map write failed after diagnostic: {_db_err}", file=sys.stderr)

    # Path assembly
    try:
        _intake_raw = profile.get("intake_profile") if profile else None
        _intake = json.loads(_intake_raw) if _intake_raw else None
        if _intake:
            _atoms = [
                a for a in get_atomic_modules()
                if a.get("status") in ("canonical", "role-variant")
            ]
            if _atoms:
                _path = assemble_path(_intake, domain_scores, _atoms)
                save_assembled_path(user_email, _path)
    except Exception as _path_err:
        print(f"[WARNING] path assembly failed after diagnostic: {_path_err}", file=sys.stderr)

    # Clear session state and navigate
    for k in ["diag_session_started", "diag_started_at", "diag_screen",
              "diag_q1_text", "diag_q2_text", "diag_mcqs", "diag_mcq_answers"]:
        st.session_state.pop(k, None)
    st.session_state["user_state"] = "needs_course"
    st.switch_page("pages/02_Skills_Profile.py")


# ── Screen renderers ───────────────────────────────────────────────────────────

def _render_entry():
    st.markdown(_progress_pill(0), unsafe_allow_html=True)
    st.markdown(
        f'<div class="score-card" style="padding:3rem 0 2rem">'
        f'<div style="font-family:\'DM Serif Display\',serif;font-size:2rem;color:var(--text)">'
        f'{t("diag.entry_headline", _lang)}</div>'
        f'<div style="font-size:0.9rem;color:var(--text-muted);margin-top:0.6rem">'
        f'{t("diag.entry_sub", _lang)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if st.button(t("diag.begin_btn", _lang), type="primary", use_container_width=False):
        st.session_state["diag_screen"] = "q1"
        st.rerun()


def _render_text_question(q_num: int):
    key = f"diag_q{q_num}_text"
    label_key = f"diag.q{q_num}_label"
    screen_next = "q2" if q_num == 1 else "generating"
    domain = "strategic_prompting" if q_num == 1 else "critical_eval"

    st.markdown(_progress_pill(q_num), unsafe_allow_html=True)

    st.markdown(
        f'<div class="domain-tag-pill">{get_domain_display_name(domain, _lang)}</div>',
        unsafe_allow_html=True,
    )

    val = st.text_area(
        t(label_key, _lang),
        value=st.session_state.get(key, ""),
        max_chars=300,
        height=120,
        key=f"diag_ta_q{q_num}",
    )
    st.session_state[key] = val or ""

    char_count = len((val or "").strip())
    counter_color = "var(--accent_green)" if char_count >= 30 else "var(--text-faint)"
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;'
        f'color:{counter_color};text-align:right;margin-top:-0.5rem">'
        f'{char_count} / 300 · {t("diag.char_hint_short", _lang)}</div>',
        unsafe_allow_html=True,
    )

    _valid = char_count >= 30
    col_back, col_next = st.columns([1, 3])
    with col_back:
        if q_num == 2 and st.button(t("diag.back_btn", _lang), use_container_width=True):
            st.session_state["diag_screen"] = "q1"
            st.rerun()
    with col_next:
        if st.button(
            t("diag.next_btn", _lang),
            disabled=not _valid,
            type="primary",
            use_container_width=True,
            key=f"diag_next_q{q_num}",
        ):
            st.session_state["diag_screen"] = screen_next
            st.rerun()


def _render_generating():
    st.markdown(_progress_pill(3), unsafe_allow_html=True)
    st.markdown(
        f'<div class="ai-card" style="text-align:center;padding:2.5rem 1.5rem">'
        f'<div class="ai-card-label" style="text-align:center">'
        f'{t("diag.generating_headline", _lang)}</div>'
        f'<div style="font-size:0.88rem;color:var(--text-muted);margin-top:0.8rem;line-height:1.7">'
        f'{t("diag.generating_sub", _lang)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.get("diag_mcqs"):
        with st.spinner(""):
            intake_raw = profile.get("intake_profile") if profile else None
            intake = json.loads(intake_raw) if intake_raw else {}
            mcqs = generate_diagnostic_mcqs(
                q1_text=st.session_state["diag_q1_text"],
                q2_text=st.session_state["diag_q2_text"],
                intake_profile=intake,
                user_email=user_email,
                lang=_lang,
            )
            st.session_state["diag_mcqs"] = mcqs

    st.session_state["diag_screen"] = "mcq_0"
    st.rerun()


def _render_mcq(idx: int):
    mcqs = st.session_state.get("diag_mcqs", [])
    if idx >= len(mcqs):
        st.session_state["diag_screen"] = "scoring"
        st.rerun()
        return

    mcq = mcqs[idx]
    screen_num = idx + 3
    st.markdown(_progress_pill(screen_num), unsafe_allow_html=True)

    st.markdown(
        f'<div class="domain-tag-pill">{get_domain_display_name(mcq["domain_id"], _lang)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="font-family:\'Inter\',sans-serif;font-size:1.05rem;font-weight:600;'
        f'color:var(--text);line-height:1.6;margin-bottom:1.2rem">'
        f'{mcq["question_text"]}</div>',
        unsafe_allow_html=True,
    )

    for option in mcq["options"]:
        if st.button(
            f'{option["label"]}.  {option["text"]}',
            key=f'mcq_{mcq["domain_id"]}_{option["label"]}',
            use_container_width=True,
        ):
            st.session_state["diag_mcq_answers"][mcq["domain_id"]] = option["score"]
            next_idx = idx + 1
            if next_idx < len(mcqs):
                st.session_state["diag_screen"] = f"mcq_{next_idx}"
            else:
                st.session_state["diag_screen"] = "scoring"
            st.rerun()


def _render_scoring():
    st.markdown(_progress_pill(6, 6), unsafe_allow_html=True)
    st.markdown(
        f'<div class="score-card" style="padding:2rem 0">'
        f'<div style="font-size:1.8rem;color:var(--accent_green)">✓</div>'
        f'<div style="font-family:\'Inter\',sans-serif;font-size:1rem;'
        f'color:var(--text);margin-top:0.6rem">{t("diag.all_done", _lang)}</div>'
        f'<div style="font-size:0.88rem;color:var(--text-muted);margin-top:0.3rem">'
        f'{t("diag.scoring_headline", _lang)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        intake_raw = profile.get("intake_profile") if profile else None
        intake = json.loads(intake_raw) if intake_raw else {}
        try:
            result = score_hybrid_diagnostic(
                q1_text=st.session_state["diag_q1_text"],
                q2_text=st.session_state["diag_q2_text"],
                mcq_answers=st.session_state["diag_mcq_answers"],
                intake_profile=intake,
                user_email=user_email,
                lang=_lang,
            )
        except Exception as e:
            st.error(t("diag.error_scoring", _lang) + f"\n\n_{e}_")
            st.stop()

    _complete_diagnostic(
        domain_scores=result["domain_scores"],
        item_scores=result["item_scores"],
        overall_score=result["overall_score"],
    )


# ── Screen router ──────────────────────────────────────────────────────────────
screen = st.session_state["diag_screen"]

if screen == "entry":
    _render_entry()
elif screen == "q1":
    _render_text_question(q_num=1)
elif screen == "q2":
    _render_text_question(q_num=2)
elif screen == "generating":
    _render_generating()
elif screen.startswith("mcq_"):
    try:
        idx = int(screen.split("_")[1])
        _render_mcq(idx)
    except (ValueError, IndexError):
        st.session_state["diag_screen"] = "scoring"
        st.rerun()
elif screen == "scoring":
    _render_scoring()
else:
    # Fallback to entry
    st.session_state["diag_screen"] = "entry"
    st.rerun()
