"""
Course Module page — Reading / Practice (AI Coach) / Evaluation / Results.

Sub-views controlled by st.session_state["active_submodule"]:
  overview | reading | practice | evaluation | results
"""

import json
import uuid
from datetime import datetime

import streamlit as st

from utils.auth import get_user_email
from utils.db import (
    get_profile, get_progress, get_all_progress, get_progress_by_seq, get_latest_diagnostic,
    save_coach_session, update_progress, unlock_progress, save_gap_map, create_progress,
)
from google.cloud.firestore import SERVER_TIMESTAMP
from utils.content import get_course, get_reading, get_scenario, get_eval_items, get_domain_descriptions, get_reading_structured, get_atomic_modules, EVAL_ITEMS
from utils.path_assembler import fill_scenario as _fill_scenario
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
from utils.i18n import t

st.set_page_config(
    page_title="Course Module | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

MAX_TASK_TURNS = 3
MAX_TOTAL_TURNS = 15
MAX_USER_INPUT_CHARS = 2000

# Appended to the coach system prompt for open-ended tasks.
# Instructs the coach to emit [ADVANCE] at the end of its reply when
# the learner has clearly demonstrated mastery of the task objective.
_OPEN_TASK_MASTERY_ADDENDUM = (
    "\n\n## MASTERY SIGNAL\n"
    "If the learner's last response clearly and completely addresses the task objective, "
    "append [ADVANCE] on a new line at the very end of your reply — after all other text. "
    "Do NOT mention, explain, or reference [ADVANCE] to the learner. "
    "Only emit [ADVANCE] when mastery is genuinely demonstrated; "
    "if the answer is partial or vague, continue with a follow-up question instead."
)

user_email = get_user_email()

# ── Guards ────────────────────────────────────────────────────────────────────
profile = get_profile(user_email)
if not profile:
    st.switch_page("pages/00_Welcome.py")

course_id = st.session_state.get("active_course_id")
active_atom_id = st.session_state.get("active_atom_id")
if not course_id and not active_atom_id:
    st.switch_page("pages/03_Home.py")

active_sub = st.session_state.get("active_submodule", "overview")

_lang = st.session_state.get("lang", "en")

# Profile-based lang override (runs once per session after profile load)
if not st.session_state.get("_lang_from_profile") and profile and profile.get("lang") in ("en", "zh"):
    st.session_state["lang"] = profile["lang"]
    st.session_state["_lang_from_profile"] = True
    _lang = profile["lang"]


# ── Data loaders ──────────────────────────────────────────────────────────────
def load_progress(cid: str):
    return get_progress(user_email, cid)


def load_all_progress() -> list:
    _rows = get_all_progress(user_email)
    result = []
    for _row in _rows:
        _course = get_course(_row["course_id"], lang=_lang)
        result.append({**_row, "primary_domain": _course["primary_domain"], "title": _course["title"]})
    return result


def load_next_module_title(current_seq: int):
    nxt = get_progress_by_seq(user_email, current_seq + 1)
    if nxt:
        return get_course(nxt["course_id"], lang=_lang)["title"]
    return None


def do_complete_practice(progress_id: str, messages: list, total_turns: int):
    """Write coach session + mark practice complete, then navigate to evaluation."""
    with st.spinner(t("module.saving_practice", st.session_state.get("lang", "en"))):
        try:
            session_id = str(uuid.uuid4())
            started_at = st.session_state.pop("practice_started_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            conv_json = json.dumps(messages, ensure_ascii=False)
            save_coach_session(session_id, user_email, course_id, started_at, total_turns, conv_json)
            update_progress(user_email, course_id, practice_completed_at=SERVER_TIMESTAMP)
        except Exception as e:
            st.error(t("module.save_practice_error", st.session_state.get("lang", "en")) + f"\n\n_{e}_")
            st.stop()

    for k in ["coach_messages_by_task", "mcq_answered_by_task", "practice_task_idx", "practice_turns", "task_turn_counts"]:
        st.session_state.pop(k, None)
    st.session_state["eval_item_index"] = 0
    st.session_state["eval_responses"] = []
    st.session_state["active_submodule"] = "evaluation"
    st.rerun()


# ── Load content ──────────────────────────────────────────────────────────────
_eval_auto_complete = False  # True when atom has no eval items → skip eval, auto-mark done

if active_atom_id:
    # ── Atom path: build content variables from atom structure ────────────────
    _atoms_map = {a["atom_id"]: a for a in get_atomic_modules()}
    _atom = _atoms_map.get(active_atom_id)
    if _atom is None:
        # Atom removed from content; fall back to legacy course_id path
        active_atom_id = None
    else:
        # Intake profile for scenario filling
        _intake_raw = profile.get("intake_profile") if profile else None
        try:
            _intake = json.loads(_intake_raw) if _intake_raw else {}
        except Exception:
            _intake = {}

        # Effective course_id for Firestore progress writes
        _source_ids = _atom.get("source_course_ids") or []
        _eff_course_id = _source_ids[0] if _source_ids else active_atom_id
        course_id = _eff_course_id

        # course dict — same keys used by the rendering code
        course = {
            "title": _atom.get("title", active_atom_id),
            "tagline": "",
            "primary_domain": _atom.get("domain", ""),
        }

        # reading dict — atom["reading"] uses same keys (concept_text, good_example, anti_pattern, takeaway)
        reading = _atom.get("reading") or {}

        # scenario dict — map atom practice structure to legacy expected format
        _practice = _atom.get("practice") or {}
        _task_templates = _practice.get("task_templates") or []
        _role_text = _intake.get("role_text") or "professional"
        _coach_prompt = (
            (_practice.get("coach_system_prompt_template") or "")
            .replace("{role}", _role_text)
            .replace("{organisation}", "your organization")
            .replace("{scenario_name}", _atom.get("title") or "the module")
        )
        scenario = {
            "scenario_text": _fill_scenario(_atom, _intake, _lang),
            "task_1_text": _task_templates[0]["text_template"] if len(_task_templates) > 0 else "",
            "task_2_text": _task_templates[1]["text_template"] if len(_task_templates) > 1 else "",
            "task_3_text": _task_templates[2]["text_template"] if len(_task_templates) > 2 else "",
            "task_4_text": _task_templates[3]["text_template"] if len(_task_templates) > 3 else "",
            "coach_system_prompt": _coach_prompt,
            "task_modes": [tt.get("task_mode", "open") for tt in _task_templates],
            "task_mcq_options": [tt.get("mcq_options") for tt in _task_templates],
        }

        # eval_items: try source_course_ids[0], then domain fallback, then skip
        eval_items = []
        if _source_ids:
            try:
                eval_items = get_eval_items(_source_ids[0], lang=_lang)
            except (KeyError, Exception):
                eval_items = []
        if not eval_items:
            _atom_domain = _atom.get("domain", "")
            _fallback_cid = next(
                (cid for cid in EVAL_ITEMS.keys() if _atom_domain in cid),
                None,
            )
            if _fallback_cid:
                eval_items = list(EVAL_ITEMS[_fallback_cid])
            else:
                eval_items = []
                _eval_auto_complete = True

        # progress: load by effective course_id; auto-create if missing (atom user's first visit)
        progress = load_progress(course_id)
        if progress is None:
            try:
                create_progress(user_email, course_id, seq=1, is_locked=False)
                progress = load_progress(course_id)
            except Exception:
                pass

if not active_atom_id:
    # ── Legacy course path ────────────────────────────────────────────────────
    if not course_id:
        st.switch_page("pages/03_Home.py")
    try:
        course = get_course(course_id, lang=_lang)
        reading = get_reading(course_id, lang=_lang)
        scenario = get_scenario(course_id, lang=_lang)
        eval_items = get_eval_items(course_id, lang=_lang)
        progress = load_progress(course_id)
    except KeyError as e:
        st.error(t("module.content_not_found_error", _lang).format(id=e))
        st.stop()
    except Exception as e:
        st.error(t("module.load_error", _lang) + f"\n\n_{e}_")
        st.stop()

if not course or not progress:
    st.error(t("module.module_not_found_error", _lang))
    if st.button(t("module.home_btn", _lang)):
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
    user_email=user_email,
    lang=_lang,
)


# ── Breadcrumb ────────────────────────────────────────────────────────────────
_bc_home_col, _bc_info_col = st.columns([2, 10])
with _bc_home_col:
    if st.button(t("module.back_btn", _lang), key="bc_home", use_container_width=True):
        st.switch_page("pages/03_Home.py")
with _bc_info_col:
    st.markdown(
        f'<div style="font-family:\'Inter\',sans-serif; font-size:0.75rem; color:#8990A8; padding-top:0.65rem">'
        f'{t("module.breadcrumb", _lang).format(n=seq_order, title=course_title)}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Reading section template renderers ────────────────────────────────────────

def _render_concept(rs: dict) -> None:
    """Renders concept_text_structured as an acronym card grid."""
    st.caption(rs.get("framework_acronym", ""))
    if rs.get("intro"):
        st.markdown(rs["intro"])

    cards = rs.get("cards", [])
    LETTER_ICONS = ["🔵", "🟣", "🔴", "🟢", "🟡", "🟠"]
    if cards:
        cols = st.columns(2)
        for i, card in enumerate(cards):
            with cols[i % 2]:
                with st.container(border=True):
                    icon = LETTER_ICONS[i % len(LETTER_ICONS)]
                    st.markdown(f"**{icon} {card['letter']} — {card['title']}**")
                    st.markdown(card["body"])

    if rs.get("guardrails"):
        items = "\n".join(f"- {g}" for g in rs["guardrails"])
        st.info(f"**Essential guardrails**\n\n{items}")


def _render_good_example(rs: dict) -> None:
    """Renders good_example_structured as a Before/After comparison."""
    if rs.get("scenario"):
        with st.container(border=True):
            st.caption("📋 Scenario")
            st.markdown(rs["scenario"])

    col_b, col_a = st.columns(2)
    with col_b:
        st.caption("❌ Before")
        with st.container(border=True):
            st.code(rs.get("before_prompt", ""), language=None)
            if rs.get("before_issue"):
                st.caption(f"⚠️ {rs['before_issue']}")
    with col_a:
        st.caption("✅ After")
        with st.container(border=True):
            st.code(rs.get("after_prompt", ""), language=None)
            if rs.get("after_benefit"):
                st.caption(f"✓ {rs['after_benefit']}")

    if rs.get("outcome"):
        st.success(rs["outcome"])


def _render_anti_pattern(rs: dict) -> None:
    """Renders anti_pattern_structured as an incident report with cascade chain."""
    if rs.get("failure_scenario"):
        with st.container(border=True):
            st.caption("⚠️ What went wrong")
            st.markdown(rs["failure_scenario"])

    chain = rs.get("chain", [])
    if chain:
        st.markdown("**The cascade:**")
        for i, step in enumerate(chain, 1):
            st.markdown(f"{i}. {step}")

    if rs.get("root_lesson"):
        st.error(f"**Root lesson:** {rs['root_lesson']}")


def _render_takeaway(rs: dict) -> None:
    """Renders takeaway_structured as a focal card with two action points."""
    if rs.get("statement"):
        st.markdown(f"## {rs['statement']}")
        st.divider()

    a1 = rs.get("action_1", {})
    a2 = rs.get("action_2", {})
    if a1 or a2:
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown(f"**{a1.get('title', '')}**")
                st.markdown(a1.get("body", ""))
        with col2:
            with st.container(border=True):
                st.markdown(f"**{a2.get('title', '')}**")
                st.markdown(a2.get("body", ""))


# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if active_sub == "overview":
    st.markdown(
        f'<div class="question-counter">{t("module.overview_counter", _lang).format(n=seq_order)}</div>',
        unsafe_allow_html=True,
    )
    st.title(course_title)
    st.markdown(
        f'<div style="font-family:\'Inter\',sans-serif; font-size:1rem; '
        f'color:#8990A8; margin-bottom:2rem">{course.get("tagline", "")}</div>',
        unsafe_allow_html=True,
    )

    def _step(done: bool, is_current: bool) -> str:
        return "done" if done else ("current" if is_current else "pending")

    step_progress_strip([
        {"label": t("module.read_step_label", _lang),     "state": _step(reading_done,  not reading_done)},
        {"label": t("module.practice_step_label", _lang), "state": _step(practice_done, reading_done and not practice_done)},
        {"label": t("module.quiz_step_label", _lang),     "state": _step(eval_done,     practice_done and not eval_done)},
    ])

    with st.expander(t("module.about_expander", _lang), expanded=False):
        domain_display = DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain)
        st.caption(t("module.about_domain", _lang).format(domain=domain_display))
        st.markdown(t("module.about_table_md", _lang))

    if eval_done:
        if st.button(t("module.review_results_btn", _lang), type="primary"):
            st.session_state["active_submodule"] = "results"
            st.rerun()
    elif practice_done:
        if st.button(t("module.take_quiz_btn", _lang), type="primary"):
            st.session_state["active_submodule"] = "evaluation"
            st.rerun()
    elif reading_done:
        if st.button(t("module.continue_practice_btn", _lang), type="primary"):
            st.session_state["active_submodule"] = "practice"
            st.rerun()
    else:
        if st.button(t("module.start_reading_btn", _lang), type="primary"):
            st.session_state["active_submodule"] = "reading"
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# READING
# ═══════════════════════════════════════════════════════════════════════════════
elif active_sub == "reading":
    if "reading_section_idx" not in st.session_state:
        st.session_state.reading_section_idx = 0

    st.title(course_title)
    step_progress_strip([
        {"label": t("module.read_step_label", _lang),     "state": "current"},
        {"label": t("module.practice_step_label", _lang), "state": "pending"},
        {"label": t("module.quiz_step_label", _lang),     "state": "pending"},
    ])

    if not reading:
        st.warning(t("module.reading_not_available", _lang))
        if st.button(t("module.back_btn_sm", _lang)):
            st.session_state["active_submodule"] = "overview"
            st.rerun()
        st.stop()

    # Internal English keys used for session state and section lookup (never translated)
    _SECTION_LABELS = ["Concept", "Example", "Pitfall", "Takeaway"]
    # Display labels: translated for UI only
    _SECTION_DISPLAY = [
        t("module.section_concept", _lang),
        t("module.section_example", _lang),
        t("module.section_pitfall", _lang),
        t("module.section_takeaway", _lang),
    ]

    # Apply pending navigation from Prev/Next buttons BEFORE the widget renders
    if "_reading_nav_target" in st.session_state:
        st.session_state["reading_section_ctrl"] = st.session_state.pop("_reading_nav_target")
    elif "reading_section_ctrl" not in st.session_state:
        st.session_state["reading_section_ctrl"] = _SECTION_LABELS[0]

    current_section = st.session_state["reading_section_ctrl"]
    section_idx = _SECTION_LABELS.index(current_section) if current_section in _SECTION_LABELS else 0

    reading_s = get_reading_structured(course_id)

    _, content_col, _ = st.columns([1, 4, 1])
    with content_col:
        if section_idx == 0:
            rs = reading_s.get("concept_text_structured") if reading_s else None
            if rs:
                _render_concept(rs)
            elif reading.get("concept_text"):
                with st.container(border=True):
                    st.markdown(reading["concept_text"])
        elif section_idx == 1:
            rs = reading_s.get("good_example_structured") if reading_s else None
            if rs:
                _render_good_example(rs)
            elif reading.get("good_example"):
                st.success(f"**Good example** — {reading['good_example']}")
        elif section_idx == 2:
            rs = reading_s.get("anti_pattern_structured") if reading_s else None
            if rs:
                _render_anti_pattern(rs)
            elif reading.get("anti_pattern"):
                st.warning(f"**Common mistake** — {reading['anti_pattern']}")
        elif section_idx == 3:
            rs = reading_s.get("takeaway_structured") if reading_s else None
            if rs:
                _render_takeaway(rs)
            elif reading.get("takeaway"):
                st.info(f"**Key takeaway** — {reading['takeaway']}")
            # Milestone flair — balloons fire once per reading session
            _celebrate_key = f"reading_takeaway_celebrated_{course_id}"
            if not st.session_state.get(_celebrate_key):
                st.balloons()
                st.session_state[_celebrate_key] = True
            st.success(t("module.reading_complete_msg", _lang))

    # ── Section navigation: Previous / pill selector / Next / Complete Reading ──
    st.divider()
    _rn_prev, _rn_ctrl, _rn_next = st.columns([1, 4, 1])
    with _rn_ctrl:
        # options= uses translated display labels; session state stores English internal key via index
        _selected_display = st.segmented_control(
            "Reading section",
            options=_SECTION_DISPLAY,
            default=_SECTION_DISPLAY[section_idx],
            key="reading_section_ctrl_display",
            label_visibility="collapsed",
        )
        # Keep internal key in sync
        if _selected_display and _selected_display in _SECTION_DISPLAY:
            _new_internal = _SECTION_LABELS[_SECTION_DISPLAY.index(_selected_display)]
            if _new_internal != st.session_state.get("reading_section_ctrl"):
                st.session_state["reading_section_ctrl"] = _new_internal
                st.rerun()
    with _rn_prev:
        if section_idx > 0:
            if st.button(f"← {_SECTION_DISPLAY[section_idx - 1]}", use_container_width=True):
                st.session_state["_reading_nav_target"] = _SECTION_LABELS[section_idx - 1]
                st.rerun()
    with _rn_next:
        if section_idx < len(_SECTION_LABELS) - 1:
            if st.button(f"{_SECTION_DISPLAY[section_idx + 1]} →", type="primary", use_container_width=True):
                st.session_state["_reading_nav_target"] = _SECTION_LABELS[section_idx + 1]
                st.rerun()
        else:
            if st.button(t("module.complete_reading_btn", _lang), key="r_complete", type="primary", use_container_width=True):
                try:
                    if not reading_done:
                        update_progress(user_email, course_id, reading_completed_at=SERVER_TIMESTAMP)
                except Exception as e:
                    st.error(f"Could not save progress.\n\n_{e}_")
                    st.stop()
                for k in ("reading_section_idx", "reading_section_ctrl",
                          f"reading_takeaway_celebrated_{course_id}"):
                    st.session_state.pop(k, None)
                st.session_state.update({
                    "coach_messages_by_task": {0: [], 1: [], 2: [], 3: []},
                    "mcq_answered_by_task": {},
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
    if "coach_messages_by_task" not in st.session_state:
        st.session_state["coach_messages_by_task"] = {0: [], 1: [], 2: [], 3: []}
    if "mcq_answered_by_task" not in st.session_state:
        st.session_state["mcq_answered_by_task"] = {}
    if "practice_task_idx" not in st.session_state:
        st.session_state["practice_task_idx"] = 0
    if "practice_turns" not in st.session_state:
        st.session_state["practice_turns"] = 0
    if "task_turn_counts" not in st.session_state:
        st.session_state["task_turn_counts"] = {0: 0, 1: 0, 2: 0, 3: 0}

    task_idx: int = st.session_state["practice_task_idx"]
    total_turns: int = st.session_state["practice_turns"]
    task_turns: dict = st.session_state["task_turn_counts"]
    msgs_by_task: dict = st.session_state["coach_messages_by_task"]
    messages: list = msgs_by_task.get(task_idx, [])

    def _all_messages() -> list:
        """Flatten all per-task message lists in order for persistence."""
        result = []
        for i in range(4):
            result.extend(msgs_by_task.get(i, []))
        return result

    if not scenario:
        st.warning(t("module.practice_not_available", _lang))
        if st.button(t("module.back_btn_sm", _lang)):
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
    task_modes = scenario.get("task_modes", ["open", "open", "open", "open"])
    task_mcq_options = scenario.get("task_mcq_options", [None, None, None, None])

    st.title(course_title)
    step_progress_strip([
        {"label": t("module.read_step_label", _lang),     "state": "done"},
        {"label": t("module.practice_step_label", _lang), "state": "current"},
        {"label": t("module.quiz_step_label", _lang),     "state": "pending"},
    ])

    st.error(t("module.practice_warning", _lang))

    scenario_html = (scenario.get("scenario_text") or "").replace("\n", "<br>")
    with st.expander(t("module.scenario_expander", _lang), expanded=(len(messages) == 0)):
        st.markdown(f'<div class="scenario-box">{scenario_html}</div>', unsafe_allow_html=True)

    # Turn limit reached
    if total_turns >= MAX_TOTAL_TURNS:
        st.markdown(
            f'<div class="aha-card-warning">'
            f'<strong>{t("module.limit_reached_strong", _lang)}</strong><br>'
            f'<span style="font-size:0.88rem; color:#8990A8">{t("module.limit_reached_sub", _lang)}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("module.go_quiz_btn", _lang), type="primary"):
            do_complete_practice(progress_id, _all_messages(), total_turns)
        st.stop()

    # All 4 tasks done
    if task_idx >= 4:
        st.success(t("module.all_tasks_done", _lang))
        if st.button(t("module.complete_practice_btn", _lang), type="primary"):
            do_complete_practice(progress_id, _all_messages(), total_turns)
        st.stop()

    current_task_text = tasks[task_idx]
    current_task_turns = int(task_turns.get(task_idx, 0))
    current_task_mode = task_modes[task_idx] if task_idx < len(task_modes) else "open"
    current_mcq_options = task_mcq_options[task_idx] if task_idx < len(task_mcq_options) else None

    task_steps = [
        {"label": t("module.task_label", _lang).format(n=_t + 1), "state": ("done" if _t < task_idx else ("current" if _t == task_idx else "pending"))}
        for _t in range(4)
    ]
    step_progress_strip(task_steps)

    section_header(t("module.task_header", _lang).format(n=task_idx + 1))
    st.markdown(f'<div class="question-text">{current_task_text}</div>', unsafe_allow_html=True)

    def _advance_task():
        new_tt = dict(task_turns)
        new_tt[task_idx + 1] = 0
        st.session_state["practice_task_idx"] = task_idx + 1
        st.session_state["task_turn_counts"] = new_tt
        st.rerun()

    # ── MCQ TASK (Tasks 2–4 when task_mode = "mcq") ─────────────────────────────
    if current_task_mode == "mcq" and current_mcq_options:
        mcq_answered = st.session_state["mcq_answered_by_task"].get(task_idx)

        if not mcq_answered:
            # Show option buttons in columns — no chat input
            cols = st.columns(len(current_mcq_options))
            for i, opt in enumerate(current_mcq_options):
                with cols[i]:
                    if st.button(opt["label"], key=f"mcq_{task_idx}_{i}"):
                        chosen = opt["label"]
                        is_best = opt.get("is_best", False)
                        best_label = next((o["label"] for o in current_mcq_options if o.get("is_best")), chosen)
                        correctness_note = (
                            "Their choice is the best answer."
                            if is_best
                            else f"Their choice is not the strongest answer. The best answer is: \"{best_label}\"."
                        )
                        if task_idx >= 3:
                            mcq_addendum = (
                                "\n\n## MCQ FEEDBACK MODE — FINAL TASK\n"
                                f"The learner selected: \"{chosen}\". {correctness_note} "
                                "This is the LAST task of this practice session. "
                                "Respond in 2–3 sentences: briefly affirm what they got right (or correct the key misconception), "
                                "then close with an encouraging statement acknowledging they have completed the practice. "
                                "Do NOT ask a follow-up question. Do NOT invite further discussion. "
                                "Do NOT cite specific numbers, percentages, or statistics unless they appear verbatim in the scenario text."
                            )
                        else:
                            mcq_addendum = (
                                "\n\n## MCQ FEEDBACK MODE\n"
                                f"The learner selected: \"{chosen}\". {correctness_note} "
                                "Respond in 2 sentences maximum: acknowledge what their choice gets right (or where it falls short), "
                                "and state the single most important insight they should take away. "
                                "Do NOT ask a follow-up question. "
                                "Do NOT cite specific numbers, percentages, or statistics unless they appear verbatim in the scenario text."
                            )
                        mcq_coach_prompt = coach_prompt + mcq_addendum
                        try:
                            with st.spinner(t("module.coach_thinking", _lang)):
                                feedback = coach_response(
                                    system_prompt=mcq_coach_prompt,
                                    conversation=[],
                                    user_input=chosen,
                                    user_email=user_email,
                                    lang=_lang,
                                )
                        except Exception as e:
                            st.error(t("module.coach_unavailable", _lang) + f"\n\n_{e}_")
                            st.stop()
                        updated_by_task = dict(msgs_by_task)
                        updated_by_task[task_idx] = [
                            {"role": "user", "content": chosen},
                            {"role": "assistant", "content": feedback},
                        ]
                        st.session_state["coach_messages_by_task"] = updated_by_task
                        answered = dict(st.session_state["mcq_answered_by_task"])
                        answered[task_idx] = chosen
                        st.session_state["mcq_answered_by_task"] = answered
                        st.session_state["practice_turns"] = total_turns + 1
                        st.rerun()
        else:
            # Show disabled MCQ buttons with ✅/❌ correctness signal
            answered_label = mcq_answered
            cols = st.columns(len(current_mcq_options))
            for i, opt in enumerate(current_mcq_options):
                with cols[i]:
                    if opt.get("is_best"):
                        display_label = f"✅ {opt['label']}"
                    elif opt["label"] == answered_label:
                        display_label = f"❌ {opt['label']}"
                    else:
                        display_label = opt["label"]
                    st.button(display_label, key=f"mcq_done_{task_idx}_{i}", disabled=True)
            # Show the recorded exchange then the advance CTA
            for msg in messages:
                with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else None):
                    st.markdown(msg["content"])
            if task_idx < 3:
                if st.button(t("module.next_task_btn", _lang), key=f"mcq_next_{task_idx}", type="primary"):
                    _advance_task()
            else:
                if st.button(t("module.complete_practice_btn", _lang), key="mcq_complete", type="primary"):
                    do_complete_practice(progress_id, _all_messages(), total_turns)

    # ── OPEN TASK (Task 1, or fallback for tasks missing mcq_options) ────────────
    else:
        # Task turn limit — render ABOVE chat history so CTA is always visible (UX-P2)
        effective_limit = MAX_TASK_TURNS + st.session_state.get(f"task_extra_{task_idx}", 0) * 3
        if current_task_turns >= effective_limit:
            st.warning(t("module.task_limit_warning", _lang))
            col_cont, col_next = st.columns(2)
            with col_cont:
                if st.button(t("module.continue_turns_btn", _lang), key=f"cont_{task_idx}"):
                    st.session_state[f"task_extra_{task_idx}"] = st.session_state.get(f"task_extra_{task_idx}", 0) + 1
                    st.rerun()
            with col_next:
                # UI-1: correct label on last task
                next_label = t("module.complete_practice_btn", _lang) if task_idx >= 3 else t("module.next_task_btn", _lang)
                if st.button(next_label, key=f"next_{task_idx}", type="primary"):
                    if task_idx >= 3:
                        do_complete_practice(progress_id, _all_messages(), total_turns)
                    else:
                        _advance_task()
            # Chat history rendered below CTA so learner can review context
            for msg in messages:
                with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else None):
                    st.markdown(msg["content"])
            st.stop()

        # Chat history — current task only (UX-P1)
        for msg in messages:
            with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])

        st.caption(t("module.turn_counter", _lang).format(n=total_turns, max=MAX_TOTAL_TURNS))

        # Determine if we're waiting for user input
        last_role = messages[-1]["role"] if messages else None
        waiting_for_user = last_role != "user"

        if not waiting_for_user:
            # Coach just replied — show primary CTA
            if task_idx < 3:
                if st.button(t("module.next_task_btn", _lang), key="p_next", type="primary"):
                    new_tt = dict(task_turns)
                    new_tt[task_idx + 1] = 0
                    st.session_state["practice_task_idx"] = task_idx + 1
                    st.session_state["task_turn_counts"] = new_tt
                    st.rerun()
            else:
                if st.button(t("module.complete_practice_btn", _lang), key="p_complete_final", type="primary"):
                    do_complete_practice(progress_id, _all_messages(), total_turns)

        # Secondary actions — always accessible via popover
        with st.popover(t("module.more_options_btn", _lang)):
            if waiting_for_user and task_idx < 3:
                if st.button(t("module.skip_task_btn", _lang), key="p_skip_pop"):
                    new_tt = dict(task_turns)
                    new_tt[task_idx + 1] = 0
                    st.session_state["practice_task_idx"] = task_idx + 1
                    st.session_state["task_turn_counts"] = new_tt
                    st.rerun()
            if task_idx < 3:
                if st.button(t("module.complete_early_btn", _lang), key="p_early_pop"):
                    do_complete_practice(progress_id, _all_messages(), total_turns)

        # Native chat input pinned to page bottom (only rendered when waiting for user)
        if waiting_for_user:
            if user_input := st.chat_input(t("module.chat_placeholder", _lang), key=f"p_input_{task_idx}_{current_task_turns}"):
                if len(user_input) > MAX_USER_INPUT_CHARS:
                    st.warning(f"Your message was trimmed to {MAX_USER_INPUT_CHARS} characters.")
                    user_input = user_input[:MAX_USER_INPUT_CHARS]
                # Immediately show the user message — don't wait for AI to reply
                with st.chat_message("user"):
                    st.markdown(user_input.strip())

                try:
                    with st.chat_message("assistant", avatar="🤖"):
                        with st.spinner(t("module.coach_thinking", _lang)):
                            reply = coach_response(
                                system_prompt=coach_prompt + _OPEN_TASK_MASTERY_ADDENDUM,
                                conversation=messages,
                                user_input=user_input.strip(),
                                user_email=user_email,
                                lang=_lang,
                            )
                        # Strip the mastery signal before displaying
                        auto_advance = "[ADVANCE]" in reply
                        reply_clean = reply.replace("[ADVANCE]", "").strip()
                        st.markdown(reply_clean)
                except Exception as e:
                    st.error(t("module.coach_unavailable", _lang) + f"\n\n_{e}_")
                    st.stop()

                new_tt = dict(task_turns)
                new_tt[task_idx] = current_task_turns + 1
                updated_task_msgs = messages + [
                    {"role": "user", "content": user_input.strip()},
                    {"role": "assistant", "content": reply_clean},
                ]
                updated_by_task = dict(msgs_by_task)
                updated_by_task[task_idx] = updated_task_msgs
                st.session_state["coach_messages_by_task"] = updated_by_task
                st.session_state["practice_turns"] = total_turns + 1
                st.session_state["task_turn_counts"] = new_tt

                # LG-1: auto-advance when coach signals mastery
                if auto_advance:
                    if task_idx >= 3:
                        do_complete_practice(progress_id, _all_messages(), total_turns + 1)
                    else:
                        _advance_task()
                else:
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
elif active_sub == "evaluation":
    # Atom path with no eval items: auto-mark complete with score 0, go to results
    if _eval_auto_complete:
        try:
            update_progress(
                user_email, course_id,
                evaluation_completed_at=SERVER_TIMESTAMP,
                evaluation_score=0,
                domain_score_after=None,
            )
        except Exception:
            pass
        st.session_state["active_submodule"] = "results"
        st.rerun()

    if "eval_item_index" not in st.session_state:
        st.session_state["eval_item_index"] = 0
    if "eval_responses" not in st.session_state:
        st.session_state["eval_responses"] = []

    eval_idx: int = st.session_state["eval_item_index"]
    EVAL_TOTAL = len(eval_items)

    def complete_evaluation(responses: list):
        with st.spinner(t("module.quiz_spinner_scoring", _lang)):
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
                scores = score_evaluation(payload, user_email=user_email, lang=_lang)
                eval_score = float(scores.get("overall_score", 0.0))
                domain_score_after = float(
                    scores.get("domain_scores", {}).get(primary_domain, eval_score)
                )
            except Exception as e:
                st.error(t("module.quiz_error_scoring", _lang) + f"\n\n_{e}_")
                st.stop()

        with st.spinner(t("module.quiz_spinner_profile", _lang)):
            try:
                update_progress(
                    user_email, course_id,
                    evaluation_score=eval_score,
                    evaluation_completed_at=SERVER_TIMESTAMP,
                    domain_score_after=domain_score_after,
                )
                unlock_progress(user_email, seq_order + 1)
            except Exception as e:
                st.error(t("module.quiz_error_save", _lang) + f"\n\n_{e}_")
                st.stop()

        with st.spinner(t("module.quiz_spinner_gap_map", _lang)):
            try:
                diag_row = get_latest_diagnostic(user_email)
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
                    domain_descriptions=get_domain_descriptions(st.session_state.get("role_id", "rm"), lang=_lang),
                    user_email=user_email,
                    source_type="evaluation",
                    lang=_lang,
                )
                gm_id = str(uuid.uuid4())
                save_gap_map(gm_id, user_email, "evaluation", progress_id, json.dumps(gap_bullets, ensure_ascii=False))
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
                lang=_lang,
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

    st.title(t("module.quiz_title", _lang).format(title=course_title))
    st.caption(t("module.quiz_counter", _lang).format(n=min(eval_idx + 1, EVAL_TOTAL), total=EVAL_TOTAL))
    step_progress_strip([
        {"label": t("module.read_step_label", _lang),     "state": "done"},
        {"label": t("module.practice_step_label", _lang), "state": "done"},
        {"label": t("module.quiz_step_label", _lang),     "state": "current"},
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

    st.caption(f"📍 {DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain).upper()}")

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

        btn_label = t("module.eval_submit_quiz_btn", _lang) if is_last else t("module.eval_next_btn", _lang)
        if st.button(btn_label, disabled=(selected is None), key=f"eb_{item_id}", type="primary"):
            st.session_state["eval_responses"].append({
                "item_id": item_id,
                "response": opt_keys[opt_labels.index(selected)],
            })
            st.session_state["eval_item_index"] += 1
            st.rerun()

    elif item_type == "performance_task":
        if scenario_text:
            st.caption(t("module.eval_scenario_label", _lang))
            st.markdown(f'<div class="scenario-box">{scenario_text}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="question-text">{question_text}</div>', unsafe_allow_html=True)
        user_text = st.text_area(
            "Response:",
            key=f"ep_{item_id}",
            height=160,
            placeholder=t("module.eval_response_placeholder", _lang),
            label_visibility="collapsed",
        )
        if st.button(t("module.eval_submit_quiz_btn", _lang), disabled=not (user_text or "").strip(), key=f"eb_{item_id}", type="primary"):
            response_text = user_text.strip()
            if len(response_text) > MAX_USER_INPUT_CHARS:
                st.warning(f"Your response was trimmed to {MAX_USER_INPUT_CHARS} characters.")
                response_text = response_text[:MAX_USER_INPUT_CHARS]
            st.session_state["eval_responses"].append({
                "item_id": item_id,
                "response": response_text,
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

    # Fetch diagnostic baseline for score delta (cached in session state)
    if "module_result_diag_baseline" not in st.session_state:
        try:
            diag_row = get_latest_diagnostic(user_email)
            diag_domain_scores = {}
            if diag_row:
                try:
                    diag_domain_scores = json.loads(diag_row.get("domain_scores") or "{}")
                except Exception:
                    pass
            st.session_state["module_result_diag_baseline"] = diag_domain_scores.get(primary_domain)
        except Exception:
            st.session_state["module_result_diag_baseline"] = None
    diag_baseline = st.session_state["module_result_diag_baseline"]

    st.title(t("module.results_title", _lang))
    step_progress_strip([
        {"label": t("module.read_step_label", _lang),     "state": "done"},
        {"label": t("module.practice_step_label", _lang), "state": "done"},
        {"label": t("module.quiz_step_label", _lang),     "state": "done"},
    ])

    try:
        rs = float(result_score or 0)
    except (TypeError, ValueError):
        rs = 0.0

    delta_str = None
    if diag_baseline is not None:
        try:
            delta_val = rs - float(diag_baseline)
            delta_str = t("module.results_delta", _lang).format(delta=f"{delta_val:+.1f}")
        except (TypeError, ValueError):
            pass

    st.metric(label=course_title, value=f"{rs:.1f} / 4.0", delta=delta_str)

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
        with st.container(border=True):
            st.caption(t("module.results_coach_note_label", _lang))
            st.markdown(coach_note)

    st.success(t("module.results_updated_success", _lang))

    all_prog = load_all_progress()
    next_module = next(
        (r for r in all_prog if int(r.get("module_sequence_order", 0)) == seq_order + 1),
        None,
    )
    all_complete = all(r.get("evaluation_completed_at") for r in all_prog)

    col_a, col_b = st.columns(2)
    with col_a:
        if not all_complete:
            if st.button(t("module.results_view_profile_btn", _lang), use_container_width=True, type="secondary"):
                st.switch_page("pages/02_Skills_Profile.py")
    with col_b:
        if all_complete:
            if st.button(t("module.results_final_profile_btn", _lang), use_container_width=True, type="primary"):
                st.switch_page("pages/02_Skills_Profile.py")
        elif next_module:
            if st.button(t("module.results_start_next_btn", _lang).format(n=seq_order + 1), use_container_width=True, type="primary"):
                st.session_state.update({
                    "active_course_id": next_module["course_id"],
                    "active_submodule": "overview",
                })
                for k in ["module_result_score", "module_result_domain_score", "module_result_coach_note"]:
                    st.session_state.pop(k, None)
                st.rerun()
