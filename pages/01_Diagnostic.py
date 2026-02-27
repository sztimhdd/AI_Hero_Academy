"""
Diagnostic page — 12-question assessment.
Supports MCQ, prompt_sandbox, and micro_task item types.
No partial saves. On completion, triggers AI scoring + gap map generation.
"""

import streamlit as st
import uuid
import json
import os
import sys
from datetime import datetime

from utils.auth import get_user_email
from utils.db import execute, query_one
from utils.ai import score_diagnostic, generate_gap_map
from utils.scoring import DOMAIN_DISPLAY_NAMES
from utils.styles import inject_global_css
from utils.content import get_diagnostic_items, get_domain_descriptions

st.set_page_config(
    page_title="Diagnostic | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()

user_email = get_user_email()

# ── Guard: must have a profile ────────────────────────────────────────────────
profile = query_one(
    "SELECT role_id FROM users WHERE user_email = ?",
    [user_email],
)
if not profile:
    st.switch_page("pages/00_Welcome.py")

role_id: str = profile["role_id"] if profile else st.session_state.get("role_id", "rm")

# Check for prior completed diagnostic — used to show exit navigation (CX1)
_prior_diag = query_one(
    "SELECT session_id FROM diagnostic_sessions "
    "WHERE user_email = ? AND completed_at IS NOT NULL LIMIT 1",
    [user_email],
)
_can_exit = bool(_prior_diag)

# ── Load diagnostic items (ordered) ──────────────────────────────────────────
items = get_diagnostic_items(role_id)
domain_descriptions = get_domain_descriptions(role_id)

TOTAL = len(items)

if TOTAL == 0:
    st.warning("No diagnostic questions found. The content database may not be seeded yet. Please contact your administrator.")
    st.stop()

# ── Session state init ────────────────────────────────────────────────────────
if "diag_item_index" not in st.session_state:
    st.session_state["diag_item_index"] = 0
if "diag_responses" not in st.session_state:
    st.session_state["diag_responses"] = []
if "diag_session_started" not in st.session_state:
    st.session_state["diag_session_started"] = str(uuid.uuid4())
    st.session_state["diag_started_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# ── Orientation screen (shown before Q1 on first load) ───────────────────────
if not st.session_state.get("diag_started"):
    st.markdown("""
<div class="aha-brand" style="margin-bottom:2rem">
  <div class="aha-brand-icon">⚡</div>
  <div class="aha-brand-name">AI <span>Hero</span> Academy</div>
</div>
""", unsafe_allow_html=True)
    st.title("AI Skills Diagnostic")
    st.markdown(
        '<div style="font-family:\'Inter\',sans-serif; font-size:0.85rem; color:#8990A8; margin-bottom:2rem">'
        'Before we build your personalised training course, we need to understand your current AI skill level.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"""
<div class="aha-card">
  <div style="display:flex; gap:2.5rem; flex-wrap:wrap; margin-bottom:1.25rem">
    <div style="text-align:center; min-width:80px">
      <div style="font-family:'IBM Plex Mono',monospace; font-size:1.8rem; font-weight:700; color:#E8E9EF">~5</div>
      <div style="font-family:'Inter',sans-serif; font-size:0.72rem; color:#8990A8; text-transform:uppercase; letter-spacing:0.08em">minutes</div>
    </div>
    <div style="text-align:center; min-width:80px">
      <div style="font-family:'IBM Plex Mono',monospace; font-size:1.8rem; font-weight:700; color:#E8E9EF">{TOTAL}</div>
      <div style="font-family:'Inter',sans-serif; font-size:0.72rem; color:#8990A8; text-transform:uppercase; letter-spacing:0.08em">questions</div>
    </div>
    <div style="text-align:center; min-width:80px">
      <div style="font-family:'IBM Plex Mono',monospace; font-size:1.8rem; font-weight:700; color:#E8E9EF">4</div>
      <div style="font-family:'Inter',sans-serif; font-size:0.72rem; color:#8990A8; text-transform:uppercase; letter-spacing:0.08em">skill domains</div>
    </div>
  </div>
  <div style="font-family:'Inter',sans-serif; font-size:0.85rem; color:#8990A8; line-height:1.6">
    Questions include <strong style="color:#E8E9EF">multiple choice</strong>,
    <strong style="color:#E8E9EF">written responses</strong>, and
    <strong style="color:#E8E9EF">short tasks</strong>.
    There are no right or wrong answers — your results shape your personalised training course.
  </div>
</div>
""", unsafe_allow_html=True)
    _orient_cols = st.columns([3, 1]) if _can_exit else [None]
    with (_orient_cols[0] if _can_exit else st.container()):
        if st.button("Start Assessment →", type="primary"):
            st.session_state["diag_started"] = True
            st.rerun()
    if _can_exit:
        with _orient_cols[1]:
            if st.button("← Exit", key="diag_exit_orient", use_container_width=True):
                st.switch_page("pages/03_Home.py")
    st.stop()

idx: int = st.session_state["diag_item_index"]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="aha-brand" style="margin-bottom:2rem">
  <div class="aha-brand-icon">⚡</div>
  <div class="aha-brand-name">AI <span>Hero</span> Academy</div>
</div>
""", unsafe_allow_html=True)

col_title, col_counter, col_exit = st.columns([4, 1, 1])
with col_title:
    st.title("Diagnostic")
with col_counter:
    st.markdown(
        f'<div class="question-counter" style="text-align:right; margin-top:1.4rem">'
        f'Question {min(idx + 1, TOTAL)} of {TOTAL}</div>',
        unsafe_allow_html=True,
    )
with col_exit:
    if st.button("← Exit", key="diag_exit_quiz", use_container_width=True):
        for k in ["diag_item_index", "diag_responses", "diag_session_started",
                  "diag_started_at", "diag_started"]:
            st.session_state.pop(k, None)
        st.switch_page("pages/03_Home.py")

# Progress bar
progress_pct = idx / TOTAL
st.progress(progress_pct)

# ── Scoring / completion handler ──────────────────────────────────────────────
def complete_diagnostic(responses: list[dict]):
    """Called after the final question is submitted."""
    with st.spinner("Analysing your responses — this takes about 20 seconds..."):
        try:
            # Build scoring payload
            scoring_payload = []
            for r in responses:
                item = next(i for i in items if i["item_id"] == r["item_id"])
                rubric = item["scoring_rubric"] if item["scoring_rubric"] else {}
                scoring_payload.append({
                    "item_id": r["item_id"],
                    "domain_id": item["domain_id"],
                    "item_type": item["item_type"],
                    "response": r["response"],
                    "correct_option": item.get("correct_option"),
                    "scoring_rubric": rubric,
                })

            scores = score_diagnostic(scoring_payload, user_email=user_email)
            item_scores = scores["item_scores"]
            domain_scores = scores["domain_scores"]
            overall_score = scores["overall_score"]

        except Exception as e:
            st.error(
                "We encountered an issue scoring your responses. "
                "Your answers are saved in this session. Please try again by refreshing.\n\n"
                f"_{e}_"
            )
            st.stop()

        # Write diagnostic session to Delta
        session_id = st.session_state.get("diag_session_started", str(uuid.uuid4()))
        started_at = st.session_state.get("diag_started_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        resp_json = json.dumps({r["item_id"]: r["response"] for r in responses}, ensure_ascii=False)
        item_scores_json = json.dumps(item_scores, ensure_ascii=False)
        domain_scores_json = json.dumps(domain_scores, ensure_ascii=False)
        try:
            execute(
                "INSERT INTO diagnostic_sessions "
                "(session_id, user_email, started_at, completed_at, responses, item_scores, domain_scores, overall_score) "
                f"VALUES (?, ?, CAST(? AS TIMESTAMP), current_timestamp(), ?, ?, ?, ?)",
                [session_id, user_email, started_at, resp_json, item_scores_json, domain_scores_json, overall_score],
            )
        except Exception as e:
            st.error(f"Could not save your results. Please try again.\n\n_{e}_")
            st.stop()

    with st.spinner("Building your personalised gap map..."):
        gap_bullets = []
        try:
            gap_bullets = generate_gap_map(
                domain_scores=domain_scores,
                domain_descriptions=domain_descriptions,
                user_email=user_email,
                source_type="diagnostic",
            )
        except Exception as _gap_err:
            # Non-fatal — Skills Profile shows fallback if gap map is missing
            print(f"[WARNING] gap_map generation failed after diagnostic: {_gap_err}", file=sys.stderr)
        if gap_bullets:
            try:
                gap_map_id = str(uuid.uuid4())
                bullets_json = json.dumps(gap_bullets, ensure_ascii=False)
                execute(
                    "INSERT INTO gap_maps "
                    "(gap_map_id, user_email, source_type, source_id, bullets, generated_at) "
                    f"VALUES (?, ?, 'diagnostic', ?, ?, current_timestamp())",
                    [gap_map_id, user_email, session_id, bullets_json],
                )
            except Exception as _db_err:
                print(f"[WARNING] gap_map write failed after diagnostic: {_db_err}", file=sys.stderr)

    # Clear diagnostic session state and navigate
    st.session_state.pop("diag_item_index", None)
    st.session_state.pop("diag_responses", None)
    st.session_state.pop("diag_session_started", None)
    st.session_state.pop("diag_started_at", None)
    st.session_state["user_state"] = "needs_course"
    st.switch_page("pages/02_Skills_Profile.py")


# ── Render current question ───────────────────────────────────────────────────
if idx >= TOTAL:
    complete_diagnostic(st.session_state["diag_responses"])
    st.stop()

item = items[idx]
item_id = item["item_id"]
domain_id = item["domain_id"]
item_type = item["item_type"]
question_text = item["question_text"] or ""
scenario_text = item["scenario_text"] or ""

domain_name = DOMAIN_DISPLAY_NAMES.get(domain_id, domain_id)
is_last = idx == TOTAL - 1

# Domain tag
st.markdown(
    f'<div class="domain-tag-inline">{domain_name}</div>',
    unsafe_allow_html=True,
)

# ── MCQ ────────────────────────────────────────────────────────────────────────
if item_type == "mcq":
    if scenario_text:
        st.markdown(
            f'<div class="scenario-box">{scenario_text}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f'<div class="question-text">{question_text}</div>', unsafe_allow_html=True)

    options = item["options"] if item["options"] else []

    opt_labels = [f"{o['label']}. {o['text']}" for o in options]
    opt_keys = [o["label"] for o in options]

    selected = st.radio(
        "Choose your answer:",
        options=opt_labels,
        key=f"mcq_{item_id}",
        label_visibility="collapsed",
        index=None,
    )

    btn_label = "Submit & Continue →" if is_last else "Next →"
    if st.button(btn_label, disabled=(selected is None), key=f"btn_{item_id}", type="primary"):
        chosen_idx = opt_labels.index(selected)
        chosen_label = opt_keys[chosen_idx]
        st.session_state["diag_responses"].append({
            "item_id": item_id,
            "response": chosen_label,
        })
        st.session_state["diag_item_index"] += 1
        st.rerun()

# ── Prompt Sandbox ────────────────────────────────────────────────────────────
elif item_type == "prompt_sandbox":
    st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.78rem; font-weight:700;
            text-transform:uppercase; letter-spacing:0.08em; color:#8990A8;
            margin-bottom:0.4rem">Scenario</div>
""", unsafe_allow_html=True)
    st.markdown(
        f'<div class="scenario-box">{scenario_text}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="question-text">{question_text}</div>', unsafe_allow_html=True)

    st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.8rem; color:#8990A8;
            margin-bottom:0.4rem">Write the prompt you would give Copilot:</div>
""", unsafe_allow_html=True)

    user_text = st.text_area(
        "Your prompt:",
        key=f"sandbox_{item_id}",
        height=140,
        placeholder="Write your prompt here. Aim for 3–8 sentences.",
        label_visibility="collapsed",
    )

    st.markdown(
        '<div style="font-family:\'IBM Plex Mono\',monospace; font-size:0.72rem; '
        'color:#8990A8; margin-top:0.3rem">Aim for 3–8 sentences</div>',
        unsafe_allow_html=True,
    )

    btn_label = "Submit →" if is_last else "Submit →"
    if st.button(btn_label, disabled=not (user_text or "").strip(), key=f"btn_{item_id}", type="primary"):
        st.session_state["diag_responses"].append({
            "item_id": item_id,
            "response": user_text.strip(),
        })
        st.session_state["diag_item_index"] += 1
        st.rerun()

# ── Micro Task ────────────────────────────────────────────────────────────────
elif item_type == "micro_task":
    st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.78rem; font-weight:700;
            text-transform:uppercase; letter-spacing:0.08em; color:#8990A8;
            margin-bottom:0.4rem">Review this content</div>
""", unsafe_allow_html=True)
    st.markdown(
        f'<div class="scenario-box"><pre>{scenario_text}</pre></div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="question-text">{question_text}</div>', unsafe_allow_html=True)

    user_text = st.text_area(
        "Your response:",
        key=f"microtask_{item_id}",
        height=120,
        placeholder="Type your response here...",
        label_visibility="collapsed",
    )

    btn_label = "Submit →"
    if st.button(btn_label, disabled=not (user_text or "").strip(), key=f"btn_{item_id}", type="primary"):
        st.session_state["diag_responses"].append({
            "item_id": item_id,
            "response": user_text.strip(),
        })
        st.session_state["diag_item_index"] += 1
        st.rerun()
