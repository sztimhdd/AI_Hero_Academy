"""
Course Module page — Reading / Practice (AI Coach) / Evaluation / Results.

Sub-views controlled by st.session_state["active_submodule"]:
  overview | reading | practice | evaluation | results
"""

import re
import json
import uuid
import os
from datetime import datetime

import streamlit as st

from utils.auth import get_user_email
from utils.db import execute, query_one
from utils.content import get_course, get_reading, get_scenario, get_eval_items, get_domain_descriptions
from utils.ai import (
    coach_response,
    score_evaluation,
    generate_gap_map,
    generate_module_coach_note,
)
from utils.scoring import (
    DOMAIN_DISPLAY_NAMES,
    parse_options,
    parse_rubric,
    compute_current_domain_scores,
)
from utils.styles import inject_global_css, section_header, step_progress_strip, render_sidebar

st.set_page_config(
    page_title="Course Module | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

CATALOG = os.environ.get("UC_CATALOG", "mdlg_ai_shared")
MAX_TASK_TURNS = 3
MAX_TOTAL_TURNS = 15

user_email = get_user_email()

# ── Guards ────────────────────────────────────────────────────────────────────
profile = query_one(
    f"SELECT display_name FROM {CATALOG}.learner.user_profiles WHERE user_email = ?",
    [user_email],
)
if not profile:
    st.switch_page("pages/00_Welcome.py")

course_id = st.session_state.get("active_course_id")
if not course_id:
    st.switch_page("pages/03_Home.py")

active_sub = st.session_state.get("active_submodule", "overview")


# ── Data loaders ──────────────────────────────────────────────────────────────
def load_progress(cid: str):
    return query_one(
        f"SELECT progress_id, module_sequence_order, is_locked, "
        f"reading_completed_at, practice_completed_at, "
        f"evaluation_completed_at, evaluation_score "
        f"FROM {CATALOG}.learner.training_progress "
        f"WHERE user_email = ? AND course_id = ?",
        [user_email, cid],
    )


def load_all_progress() -> list:
    _rows = execute(
        f"SELECT course_id, module_sequence_order, is_locked, evaluation_completed_at, domain_score_after "
        f"FROM {CATALOG}.learner.training_progress "
        f"WHERE user_email = ? ORDER BY module_sequence_order",
        [user_email],
    )
    result = []
    for _row in _rows:
        _course = get_course(_row["course_id"])
        result.append({**_row, "primary_domain": _course["primary_domain"], "title": _course["title"]})
    return result


def load_next_module_title(current_seq: int):
    nxt = query_one(
        f"SELECT course_id FROM {CATALOG}.learner.training_progress "
        f"WHERE user_email = ? AND module_sequence_order = ?",
        [user_email, current_seq + 1],
    )
    if nxt:
        return get_course(nxt["course_id"])["title"]
    return None


def do_complete_practice(progress_id: str, messages: list, total_turns: int):
    """Write coach session + mark practice complete, then navigate to evaluation."""
    with st.spinner("Saving practice session..."):
        try:
            session_id = str(uuid.uuid4())
            started_at = st.session_state.pop("practice_started_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            conv_json = json.dumps(messages, ensure_ascii=False)
            execute(
                f"INSERT INTO {CATALOG}.learner.coach_sessions "
                f"(session_id, user_email, course_id, started_at, completed_at, turn_count, conversation_json) "
                f"VALUES (?, ?, ?, CAST(? AS TIMESTAMP), current_timestamp(), ?, ?)",
                [session_id, user_email, course_id, started_at, total_turns, conv_json],
            )
            execute(
                f"UPDATE {CATALOG}.learner.training_progress "
                f"SET practice_completed_at = current_timestamp() "
                f"WHERE progress_id = ?",
                [progress_id],
            )
        except Exception as e:
            st.error(f"Could not save practice session. Please try again.\n\n_{e}_")
            st.stop()

    for k in ["coach_messages", "practice_task_idx", "practice_turns", "task_turn_counts"]:
        st.session_state.pop(k, None)
    st.session_state["eval_item_index"] = 0
    st.session_state["eval_responses"] = []
    st.session_state["active_submodule"] = "evaluation"
    st.rerun()


# ── Load content ──────────────────────────────────────────────────────────────
try:
    course = get_course(course_id)
    reading = get_reading(course_id)
    scenario = get_scenario(course_id)
    eval_items = get_eval_items(course_id)
    progress = load_progress(course_id)
except KeyError as e:
    st.error(f"Content not found for course: {e}. Please contact your administrator.")
    st.stop()
except Exception as e:
    st.error(f"Unable to load module content. Please refresh.\n\n_{e}_")
    st.stop()

if not course or not progress:
    st.error("Module not found.")
    if st.button("← Home"):
        st.switch_page("pages/03_Home.py")
    st.stop()

seq_order = int(progress.get("module_sequence_order", 1))
reading_done = bool(progress.get("reading_completed_at"))
practice_done = bool(progress.get("practice_completed_at"))
eval_done = bool(progress.get("evaluation_completed_at"))
course_title = course.get("title", "Module")
primary_domain = course.get("primary_domain", "")
progress_id = progress.get("progress_id", "")


# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar(
    "course_module",
    has_course=True,
    active_course_id=course_id,
    module_context={
        "seq_order": seq_order,
        "course_title": course_title,
        "domain_display": DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain),
    },
)


# ── Breadcrumb ────────────────────────────────────────────────────────────────
_sub_labels = {"reading": "Reading", "practice": "Practice", "evaluation": "Quiz", "results": "Results"}
_bc_home_col, _bc_info_col = st.columns([2, 10])
with _bc_home_col:
    if st.button("← My Training", key="bc_home", use_container_width=True):
        st.switch_page("pages/03_Home.py")
with _bc_info_col:
    _sub_text = f" / {_sub_labels[active_sub]}" if active_sub in _sub_labels else ""
    st.markdown(
        f'<div style="font-family:\'Inter\',sans-serif; font-size:0.75rem; color:#8990A8; padding-top:0.65rem">'
        f'Module {seq_order}: {course_title}{_sub_text}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if active_sub == "overview":
    st.markdown(f'<div class="question-counter">Module {seq_order} of 5</div>', unsafe_allow_html=True)
    st.title(course_title)
    st.markdown(
        f'<div style="font-family:\'Inter\',sans-serif; font-size:1rem; '
        f'color:#8990A8; margin-bottom:2rem">{course.get("tagline", "")}</div>',
        unsafe_allow_html=True,
    )

    def _step(done: bool, is_current: bool) -> str:
        return "done" if done else ("current" if is_current else "pending")

    step_progress_strip([
        {"label": "Read",     "state": _step(reading_done,  not reading_done)},
        {"label": "Practice", "state": _step(practice_done, reading_done and not practice_done)},
        {"label": "Quiz",     "state": _step(eval_done,     practice_done and not eval_done)},
    ])

    if eval_done:
        if st.button("Review Results →", type="primary"):
            st.session_state["active_submodule"] = "results"
            st.rerun()
    elif practice_done:
        if st.button("Take Quiz →", type="primary"):
            st.session_state["active_submodule"] = "evaluation"
            st.rerun()
    elif reading_done:
        if st.button("Continue Practice →", type="primary"):
            st.session_state["active_submodule"] = "practice"
            st.rerun()
    else:
        if st.button("Start Reading →", type="primary"):
            st.session_state["active_submodule"] = "reading"
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# READING
# ═══════════════════════════════════════════════════════════════════════════════
elif active_sub == "reading":
    st.markdown(f'<div class="question-counter">Module {seq_order} · Reading</div>', unsafe_allow_html=True)
    st.title(course_title)
    step_progress_strip([
        {"label": "Read", "state": "current"},
        {"label": "Practice", "state": "pending"},
        {"label": "Quiz", "state": "pending"},
    ])

    if not reading:
        st.warning("Reading content is not available yet.")
        if st.button("← Back"):
            st.session_state["active_submodule"] = "overview"
            st.rerun()
        st.stop()

    def _md(text: str) -> str:
        t = (text or "").replace("\n", "<br>")
        return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', t)

    section_header("CONCEPT")
    st.markdown(f'<div class="reading-concept">{_md(reading.get("concept_text",""))}</div>', unsafe_allow_html=True)

    if reading.get("good_example"):
        st.success(f"**Good Example**\n\n{reading['good_example']}")

    if reading.get("anti_pattern"):
        st.error(f"**Common Mistake**\n\n{reading['anti_pattern']}")

    if reading.get("takeaway"):
        st.info(f"**Key Takeaway**\n\n{reading['takeaway']}")

    col_back, col_cta = st.columns([1, 2])
    with col_back:
        if st.button("← Overview"):
            st.session_state["active_submodule"] = "overview"
            st.rerun()
    with col_cta:
        if st.button("I've read this — Start Practice →", use_container_width=True, type="primary"):
            try:
                execute(
                    f"UPDATE {CATALOG}.learner.training_progress "
                    f"SET reading_completed_at = current_timestamp() "
                    f"WHERE progress_id = ? AND reading_completed_at IS NULL",
                    [progress_id],
                )
            except Exception as e:
                st.error(f"Could not save progress.\n\n_{e}_")
                st.stop()
            st.session_state.update({
                "coach_messages": [],
                "practice_task_idx": 0,
                "practice_turns": 0,
                "task_turn_counts": {0: 0, 1: 0, 2: 0, 3: 0},
                "practice_started_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "active_submodule": "practice",
            })
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PRACTICE
# ═══════════════════════════════════════════════════════════════════════════════
elif active_sub == "practice":
    if "coach_messages" not in st.session_state:
        st.session_state["coach_messages"] = []
    if "practice_task_idx" not in st.session_state:
        st.session_state["practice_task_idx"] = 0
    if "practice_turns" not in st.session_state:
        st.session_state["practice_turns"] = 0
    if "task_turn_counts" not in st.session_state:
        st.session_state["task_turn_counts"] = {0: 0, 1: 0, 2: 0, 3: 0}

    task_idx: int = st.session_state["practice_task_idx"]
    total_turns: int = st.session_state["practice_turns"]
    task_turns: dict = st.session_state["task_turn_counts"]
    messages: list = st.session_state["coach_messages"]

    if not scenario:
        st.warning("Practice scenario not available.")
        if st.button("← Back"):
            st.session_state["active_submodule"] = "overview"
            st.rerun()
        st.stop()

    tasks = [
        scenario.get("task_1_text", ""),
        scenario.get("task_2_text", ""),
        scenario.get("task_3_text", ""),
        scenario.get("task_4_text", ""),
    ]
    coach_prompt = scenario.get("coach_system_prompt", "")

    st.markdown(f'<div class="question-counter">Module {seq_order} · Practice</div>', unsafe_allow_html=True)
    st.title(course_title)
    step_progress_strip([
        {"label": "Read", "state": "done"},
        {"label": "Practice", "state": "current"},
        {"label": "Quiz", "state": "pending"},
    ])

    st.warning(
        "⚠️ Navigating away via the sidebar or breadcrumb will end your session "
        "without saving your practice conversation."
    )

    section_header("SCENARIO")
    scenario_html = (scenario.get("scenario_text") or "").replace("\n", "<br>")
    st.markdown(f'<div class="scenario-box">{scenario_html}</div>', unsafe_allow_html=True)

    # Turn limit reached
    if total_turns >= MAX_TOTAL_TURNS:
        st.markdown("""
<div class="aha-card-warning">
  <strong>Practice limit reached.</strong><br>
  <span style="font-size:0.88rem; color:#8990A8">
    You've used all 15 coach turns. Time to take the quiz.
  </span>
</div>
""", unsafe_allow_html=True)
        if st.button("Go to Quiz →", type="primary"):
            do_complete_practice(progress_id, messages, total_turns)
        st.stop()

    # All 4 tasks done
    if task_idx >= 4:
        st.success("You've completed all 4 practice tasks!")
        if st.button("Complete Practice →", type="primary"):
            do_complete_practice(progress_id, messages, total_turns)
        st.stop()

    current_task_text = tasks[task_idx]
    current_task_turns = int(task_turns.get(task_idx, 0))

    section_header(f"TASK {task_idx + 1} OF 4")
    st.markdown(f'<div class="question-text">{current_task_text}</div>', unsafe_allow_html=True)

    # Chat history — native Streamlit chat components (NX1)
    for msg in messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    st.caption(f"Turn {total_turns} of {MAX_TOTAL_TURNS}")

    # Task turn limit — offer Continue or advance (P1)
    def _advance_task():
        new_tt = dict(task_turns)
        new_tt[task_idx + 1] = 0
        st.session_state["practice_task_idx"] = task_idx + 1
        st.session_state["task_turn_counts"] = new_tt
        st.rerun()

    effective_limit = MAX_TASK_TURNS + st.session_state.get(f"task_extra_{task_idx}", 0) * 3
    if current_task_turns >= effective_limit:
        st.info("You've reached the turn limit for this task.")
        col_cont, col_next = st.columns(2)
        with col_cont:
            if st.button("Continue (3 more turns) →", key=f"cont_{task_idx}"):
                st.session_state[f"task_extra_{task_idx}"] = st.session_state.get(f"task_extra_{task_idx}", 0) + 1
                st.rerun()
        with col_next:
            if st.button("Next Task →", key=f"next_{task_idx}", type="primary"):
                _advance_task()
        st.stop()

    # Determine if we're waiting for user input
    last_role = messages[-1]["role"] if messages else None
    waiting_for_user = last_role != "user"

    if not waiting_for_user:
        # Coach just replied — show navigation buttons
        col_nxt, col_done = st.columns([1, 1])
        with col_nxt:
            if task_idx < 3:
                if st.button("Next Task →", key="p_next", type="primary"):
                    new_tt = dict(task_turns)
                    new_tt[task_idx + 1] = 0
                    st.session_state["practice_task_idx"] = task_idx + 1
                    st.session_state["task_turn_counts"] = new_tt
                    st.rerun()
            else:
                if st.button("Complete Practice →", key="p_complete_final", type="primary"):
                    do_complete_practice(progress_id, messages, total_turns)
        with col_done:
            if task_idx < 3:
                if st.button("Complete Practice Early →", key="p_complete_early"):
                    do_complete_practice(progress_id, messages, total_turns)
    else:
        # Waiting for user — show skip option
        if st.button("Skip this task →", use_container_width=False, key="p_skip"):
            new_tt = dict(task_turns)
            new_tt[task_idx + 1] = 0
            st.session_state["practice_task_idx"] = task_idx + 1
            st.session_state["task_turn_counts"] = new_tt
            st.rerun()

    # Native chat input pinned to page bottom (only rendered when waiting for user)
    if waiting_for_user:
        if user_input := st.chat_input("Your response...", key=f"p_input_{task_idx}_{current_task_turns}"):
            with st.spinner("Coach is thinking..."):
                try:
                    reply = coach_response(
                        system_prompt=coach_prompt,
                        conversation=messages,
                        user_input=user_input.strip(),
                        user_email=user_email,
                    )
                except Exception as e:
                    st.error(f"Coach unavailable. Please try again.\n\n_{e}_")
                    st.stop()

            new_tt = dict(task_turns)
            new_tt[task_idx] = current_task_turns + 1
            st.session_state["coach_messages"] = messages + [
                {"role": "user", "content": user_input.strip()},
                {"role": "assistant", "content": reply},
            ]
            st.session_state["practice_turns"] = total_turns + 1
            st.session_state["task_turn_counts"] = new_tt
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
elif active_sub == "evaluation":
    if "eval_item_index" not in st.session_state:
        st.session_state["eval_item_index"] = 0
    if "eval_responses" not in st.session_state:
        st.session_state["eval_responses"] = []

    eval_idx: int = st.session_state["eval_item_index"]
    EVAL_TOTAL = len(eval_items)

    def complete_evaluation(responses: list):
        with st.spinner("Scoring your quiz responses..."):
            try:
                payload = []
                for r in responses:
                    item = next((i for i in eval_items if i["item_id"] == r["item_id"]), None)
                    if not item:
                        continue
                    rubric = parse_rubric(item.get("scoring_rubric") or "{}")
                    payload.append({
                        "item_id": r["item_id"],
                        "domain_id": primary_domain,
                        "item_type": item["item_type"],
                        "response": r["response"],
                        "correct_option": item.get("correct_option"),
                        "scoring_rubric": rubric,
                    })
                scores = score_evaluation(payload, user_email=user_email)
                eval_score = float(scores.get("overall_score", 0.0))
                domain_score_after = float(
                    scores.get("domain_scores", {}).get(primary_domain, eval_score)
                )
            except Exception as e:
                st.error(f"Issue scoring quiz. Please refresh and retry.\n\n_{e}_")
                st.stop()

        with st.spinner("Updating skills profile..."):
            try:
                execute(
                    f"UPDATE {CATALOG}.learner.training_progress "
                    f"SET evaluation_score = ?, "
                    f"    evaluation_completed_at = current_timestamp(), "
                    f"    domain_score_after = ? "
                    f"WHERE progress_id = ?",
                    [eval_score, domain_score_after, progress_id],
                )
                execute(
                    f"UPDATE {CATALOG}.learner.training_progress "
                    f"SET is_locked = false "
                    f"WHERE user_email = ? AND module_sequence_order = ?",
                    [user_email, seq_order + 1],
                )
            except Exception as e:
                st.error(f"Could not save quiz results.\n\n_{e}_")
                st.stop()

        with st.spinner("Generating updated gap map..."):
            try:
                diag_row = query_one(
                    f"SELECT domain_scores FROM {CATALOG}.learner.diagnostic_sessions "
                    f"WHERE user_email = ? AND completed_at IS NOT NULL "
                    f"ORDER BY completed_at DESC LIMIT 1",
                    [user_email],
                )
                try:
                    diag_domain_scores_gm = json.loads(diag_row.get("domain_scores") or "{}") if diag_row else {}
                except Exception:
                    diag_domain_scores_gm = {}
                # Build full merged eval domain scores across all completed modules (M5)
                eval_domain_scores_gm = []
                for _row in load_all_progress():
                    if _row.get("evaluation_completed_at") and _row.get("domain_score_after") is not None:
                        _domain = _row.get("primary_domain")
                        if _domain:
                            try:
                                eval_domain_scores_gm.append({_domain: float(_row["domain_score_after"])})
                            except (TypeError, ValueError):
                                pass
                merged_scores = compute_current_domain_scores(diag_domain_scores_gm, eval_domain_scores_gm)
                gap_bullets = generate_gap_map(
                    domain_scores=merged_scores,
                    domain_descriptions=get_domain_descriptions(st.session_state.get("role_id", "rm")),
                    user_email=user_email,
                    source_type="evaluation",
                )
                gm_id = str(uuid.uuid4())
                execute(
                    f"INSERT INTO {CATALOG}.learner.gap_maps "
                    f"(gap_map_id, user_email, source_type, source_id, bullets, generated_at) "
                    f"VALUES (?, ?, 'evaluation', ?, ?, current_timestamp())",
                    [gm_id, user_email, progress_id, json.dumps(gap_bullets, ensure_ascii=False)],
                )
            except Exception:
                pass

        coach_note = ""
        try:
            coach_note = generate_module_coach_note(
                module_title=course_title,
                evaluation_score=eval_score,
                domain_scores={primary_domain: domain_score_after},
                next_module_title=load_next_module_title(seq_order),
                user_email=user_email,
            )
        except Exception:
            pass

        st.session_state.update({
            "module_result_score": eval_score,
            "module_result_domain_score": domain_score_after,
            "module_result_coach_note": coach_note,
            "active_submodule": "results",
        })
        for k in ["eval_item_index", "eval_responses"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown(
        f'<div class="question-counter">Module {seq_order} · Quiz · '
        f'Question {min(eval_idx + 1, EVAL_TOTAL)} of {EVAL_TOTAL}</div>',
        unsafe_allow_html=True,
    )
    st.title(f"Quiz: {course_title}")
    step_progress_strip([
        {"label": "Read", "state": "done"},
        {"label": "Practice", "state": "done"},
        {"label": "Quiz", "state": "current"},
    ])
    st.progress(eval_idx / EVAL_TOTAL if EVAL_TOTAL > 0 else 0)

    if eval_idx >= EVAL_TOTAL:
        complete_evaluation(st.session_state["eval_responses"])
        st.stop()

    item = eval_items[eval_idx]
    item_id = item["item_id"]
    item_type = item["item_type"]
    question_text = item.get("question_text", "")
    scenario_text = item.get("scenario_text") or ""
    is_last = eval_idx == EVAL_TOTAL - 1

    st.markdown(
        f'<div class="domain-tag-inline">{DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain)}</div>',
        unsafe_allow_html=True,
    )

    if item_type == "mcq":
        if scenario_text:
            st.markdown(f'<div class="scenario-box">{scenario_text}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{question_text}</div>', unsafe_allow_html=True)

        options = parse_options(item.get("options") or "[]")
        opt_labels = [f"{o['label']}. {o['text']}" for o in options]
        opt_keys = [o["label"] for o in options]

        selected = st.radio(
            "Answer:",
            options=opt_labels,
            key=f"eq_{item_id}",
            index=None,
            label_visibility="collapsed",
        )

        btn_label = "Submit Quiz →" if is_last else "Next →"
        if st.button(btn_label, disabled=(selected is None), key=f"eb_{item_id}", type="primary"):
            st.session_state["eval_responses"].append({
                "item_id": item_id,
                "response": opt_keys[opt_labels.index(selected)],
            })
            st.session_state["eval_item_index"] += 1
            st.rerun()

    elif item_type == "performance_task":
        if scenario_text:
            st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.78rem; font-weight:700;
            text-transform:uppercase; letter-spacing:0.08em; color:#8990A8; margin-bottom:0.4rem">
  Scenario
</div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="scenario-box">{scenario_text}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="question-text">{question_text}</div>', unsafe_allow_html=True)
        user_text = st.text_area(
            "Response:",
            key=f"ep_{item_id}",
            height=160,
            placeholder="Write your response here...",
            label_visibility="collapsed",
        )
        if st.button("Submit Quiz →", disabled=not (user_text or "").strip(), key=f"eb_{item_id}", type="primary"):
            st.session_state["eval_responses"].append({
                "item_id": item_id,
                "response": user_text.strip(),
            })
            st.session_state["eval_item_index"] += 1
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
elif active_sub == "results":
    result_score = st.session_state.get("module_result_score")
    result_domain_score = st.session_state.get("module_result_domain_score")
    coach_note = st.session_state.get("module_result_coach_note", "")

    if result_score is None:
        # Use the progress already loaded at page start (avoids a redundant DB round-trip)
        if progress:
            try:
                result_score = float(progress.get("evaluation_score") or 0)
            except (TypeError, ValueError):
                result_score = 0.0
            try:
                result_domain_score = float(progress.get("domain_score_after") or result_score)
            except (TypeError, ValueError):
                result_domain_score = result_score
        else:
            result_domain_score = result_score

    st.markdown(f'<div class="question-counter">Module {seq_order} · Complete</div>', unsafe_allow_html=True)
    st.title("Module Complete!")
    step_progress_strip([
        {"label": "Read", "state": "done"},
        {"label": "Practice", "state": "done"},
        {"label": "Quiz", "state": "done"},
    ])

    try:
        rs = float(result_score or 0)
    except (TypeError, ValueError):
        rs = 0.0

    color_hex = "#29CC6A" if rs >= 2.5 else ("#F5A623" if rs >= 1.5 else "#E8455A")

    st.metric(label=course_title, value=f"{rs:.1f} / 4.0")

    if result_domain_score is not None:
        try:
            ds = float(result_domain_score)
        except (TypeError, ValueError):
            ds = 0.0
        col_lbl, col_val = st.columns([4, 1])
        with col_lbl:
            st.caption(DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain))
            st.progress(max(0.0, min(1.0, ds / 4.0)))
        with col_val:
            st.caption(f"{ds:.1f} / 4.0")

    if coach_note:
        st.markdown(f"""
<div class="aha-card-accent">
  <div class="coach-header"><span>🤖</span><span class="coach-label">AI Coach Note</span></div>
  <div style="font-family:'Inter',sans-serif; font-size:0.92rem; line-height:1.65; color:#EDF0F7">
    {coach_note}
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.82rem; color:#8990A8;
            margin:0.5rem 0 1.5rem">✓ Your skills profile has been updated.</div>
""", unsafe_allow_html=True)

    all_prog = load_all_progress()
    next_module = next(
        (r for r in all_prog if int(r.get("module_sequence_order", 0)) == seq_order + 1),
        None,
    )
    all_complete = all(r.get("evaluation_completed_at") for r in all_prog)

    col_a, col_b = st.columns(2)
    with col_a:
        if not all_complete:
            if st.button("View Updated Skills Profile →", use_container_width=True, type="secondary"):
                st.switch_page("pages/02_Skills_Profile.py")
    with col_b:
        if all_complete:
            if st.button("🏆  View Final Skills Profile →", use_container_width=True, type="primary"):
                st.switch_page("pages/02_Skills_Profile.py")
        elif next_module:
            if st.button(f"Start Module {seq_order + 1} →", use_container_width=True, type="primary"):
                st.session_state.update({
                    "active_course_id": next_module["course_id"],
                    "active_submodule": "overview",
                })
                for k in ["module_result_score", "module_result_domain_score", "module_result_coach_note"]:
                    st.session_state.pop(k, None)
                st.rerun()
