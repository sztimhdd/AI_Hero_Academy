"""
Diagnostic page — 6 open-ended BYOW (Bring Your Own Work) prompts, one per domain.
No role gating. All 6 rendered at once; submit enabled when every response ≥ 20 chars.
On submission, triggers AI scoring + gap map generation + path assembly.
No partial saves.
"""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

from utils.auth import get_user_email
from utils.db import (
    get_profile,
    get_latest_diagnostic,
    save_diagnostic,
    save_gap_map,
    save_assembled_path,
)
from utils.ai import score_byow_diagnostic, generate_gap_map
from utils.path_assembler import assemble_path
from utils.content import get_atomic_modules, get_domain_descriptions
from utils.styles import inject_global_css, render_lang_sidebar
from utils.i18n import t

st.set_page_config(
    page_title="Diagnostic | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto",
)

inject_global_css()

user_email = get_user_email()

# ── Guard: must have a profile ────────────────────────────────────────────────
profile = get_profile(user_email)
if not profile:
    st.switch_page("pages/00_Welcome.py")

# Check for prior completed diagnostic — used to show exit navigation (CX1)
_prior_diag = get_latest_diagnostic(user_email)
_can_exit = bool(_prior_diag)

# ── Language toggle in sidebar ────────────────────────────────────────────────
_lang = st.session_state.get("lang", "en")
render_lang_sidebar(user_email=user_email, lang=_lang)

# domain_descriptions needed for gap map generation
role_id: str = profile["role_id"] if profile else "universal"
domain_descriptions = get_domain_descriptions(role_id, lang=_lang)

# ── Load BYOW prompts ─────────────────────────────────────────────────────────
_PROMPTS_PATH = Path("content/diagnostic_prompts.json")
byow_prompts = json.loads(_PROMPTS_PATH.read_text(encoding="utf-8"))

# ── Session state init ────────────────────────────────────────────────────────
if "diag_session_started" not in st.session_state:
    st.session_state["diag_session_started"] = str(uuid.uuid4())
    st.session_state["diag_started_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# ── Brand header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="aha-brand" style="margin-bottom:2rem">
  <div class="aha-brand-icon">⚡</div>
  <div class="aha-brand-name">AI <span>Hero</span> Academy</div>
</div>
""", unsafe_allow_html=True)

# ── Title row with optional exit ─────────────────────────────────────────────
col_title, col_exit = st.columns([5, 1])
with col_title:
    st.title(t("diag.title", _lang))
with col_exit:
    if _can_exit and st.button(t("diag.exit_btn", _lang), key="diag_exit", use_container_width=True):
        st.switch_page("pages/03_Home.py")

st.markdown(
    f'<div style="font-family:\'Inter\',sans-serif; font-size:0.85rem; color:#8990A8; '
    f'margin-bottom:2rem">{t("diag.byow_intro", _lang)}</div>',
    unsafe_allow_html=True,
)

# ── Completion handler ────────────────────────────────────────────────────────
def complete_diagnostic(responses: list[dict]) -> None:
    """Called after the user submits all 6 BYOW responses."""
    with st.spinner(t("diag.spinner_analysing", _lang)):
        try:
            scores = score_byow_diagnostic(responses, user_email=user_email, lang=_lang)
            item_scores = scores["item_scores"]
            domain_scores = scores["domain_scores"]
            overall_score = scores["overall_score"]
        except Exception as e:
            st.error(t("diag.error_scoring", _lang) + f"\n\n_{e}_")
            st.stop()

        session_id = st.session_state.get("diag_session_started", str(uuid.uuid4()))
        started_at = st.session_state.get("diag_started_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        resp_json = json.dumps({r["item_id"]: r["response_text"] for r in responses}, ensure_ascii=False)
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

    with st.spinner(t("diag.spinner_gap_map", _lang)):
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

    # ── Assemble personalised atom path ──────────────────────────────────────
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
    st.session_state.pop("diag_session_started", None)
    st.session_state.pop("diag_started_at", None)
    st.session_state["user_state"] = "needs_course"
    st.switch_page("pages/02_Skills_Profile.py")


# ── Render 6 BYOW prompts inside a form ──────────────────────────────────────
# st.form captures all field values at submission time, bypassing the Streamlit
# blur requirement that kept Submit disabled after the last textarea was filled.
responses: list[dict] = []

with st.form("byow_diagnostic_form"):
    for prompt in byow_prompts:
        prompt_label = prompt.get(f"prompt_text_{_lang}", prompt["prompt_text"])
        val = st.text_area(
            prompt_label,
            key=f"byow_{prompt['item_id']}",
            max_chars=500,
            help="Aim for 3–5 sentences." if _lang == "en" else "建议3-5句话。",
        )
        char_count = len((val or "").strip())
        st.markdown(
            f'<div style="font-family:\'IBM Plex Mono\',monospace; font-size:0.72rem; '
            f'color:#8990A8; margin-top:-0.75rem; margin-bottom:1rem">'
            f'{t("diag.char_counter", _lang).format(count=char_count)}</div>',
            unsafe_allow_html=True,
        )
        responses.append({
            "item_id": prompt["item_id"],
            "domain_id": prompt["domain_id"],
            "prompt_text": prompt["prompt_text"],
            "response_text": (val or "").strip(),
            "scoring_rubric": prompt["scoring_rubric"],
        })

    submitted = st.form_submit_button(t("diag.submit_btn", _lang), type="primary")

# ── Submit handler ────────────────────────────────────────────────────────────
if submitted:
    if any(len(r["response_text"]) < 20 for r in responses):
        st.warning(t("diag.min_chars_warning", _lang))
    else:
        complete_diagnostic(responses)
