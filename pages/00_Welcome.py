"""
Welcome page — shown to users with no profile record.
Handles role selection and profile creation.

For returning users the routing guard (lines below) immediately redirects
to the correct page for their state; only new/unregistered users see the
full executive demo page.
"""

import json
import streamlit as st
import uuid
from utils.auth import get_user_email
from utils.db import get_profile, get_latest_diagnostic, get_any_progress, create_profile
from utils.styles import inject_global_css, render_lang_sidebar
from utils.content import ROLES
from utils.i18n import t
from utils.ai import call_llm
import utils.welcome_zh as _wzh


def _fetch_linkedin_via_gemini(url: str) -> str:
    """
    Retrieve public LinkedIn profile data using Gemini with Google Search Grounding.
    Returns plain text (title, company, responsibilities) suitable for Q1 pre-population.
    Returns "" on any failure — never raises.
    """
    try:
        import os
        from google import genai
        from google.genai import types as genai_types

        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        prompt = (
            f"Find the professional profile at: {url}\n"
            "Return a plain text summary (3-5 sentences) covering: "
            "current job title, employer, industry, and key responsibilities. "
            "Do not include personal contact details. Plain text only, no markdown."
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                tools=[genai_types.Tool(
                    google_search=genai_types.GoogleSearch()
                )],
                temperature=0.1,
            ),
        )
        text = (response.text or "").strip()[:1000]
        # Treat model refusals as empty — they mean Search Grounding wasn't available
        _refusal_signals = ("i am sorry", "i don't have", "i cannot", "i'm unable", "unable to access")
        if any(text.lower().startswith(sig) for sig in _refusal_signals):
            return ""
        return text
    except Exception:
        return ""


st.set_page_config(
    page_title="Welcome | AI Hero Academy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto",
)

inject_global_css()

user_email = get_user_email()

# Language toggle available even before profile creation
render_lang_sidebar(user_email=None)
_lang = st.session_state.get("lang", "en")

# Guard: if user already has a profile, route to the correct page for their state
existing = get_profile(user_email)
if existing:
    st.session_state["user_email"] = user_email
    session = get_latest_diagnostic(user_email)
    if not session:
        st.session_state["user_state"] = "needs_diagnostic"
        st.switch_page("pages/01_Diagnostic.py")
    progress = get_any_progress(user_email)
    if not progress:
        st.session_state["user_state"] = "needs_course"
        st.switch_page("pages/02_Skills_Profile.py")
    st.session_state["user_state"] = "in_training"
    st.switch_page("pages/03_Home.py")


# ── Page-specific CSS ──────────────────────────────────────────────────────────
DEMO_CSS = """
<style>
/* ─── LAYOUT & TYPOGRAPHY ───────────────────────────────── */
.demo-hero {
  padding: 5rem 0 4rem;
  text-align: center;
}
.demo-eyebrow {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--cyan);
  margin-bottom: 1.2rem;
}
.demo-headline {
  font-family: 'DM Serif Display', serif;
  font-size: 2.8rem;
  line-height: 1.15;
  color: var(--text);
  margin-bottom: 1rem;
}
.demo-headline em {
  color: var(--cyan);
  font-style: normal;
}
.demo-subhead {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-muted);
  max-width: 560px;
  margin: 0 auto 2.4rem;
}
.demo-section-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.68rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--cyan);
  margin-bottom: 0.5rem;
}
.demo-section-heading {
  font-family: 'DM Serif Display', serif;
  font-size: 1.6rem;
  color: var(--text);
  margin-bottom: 0.4rem;
}
.demo-section-sub {
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 2rem;
  max-width: 540px;
}
.demo-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 3.5rem 0;
}
/* ─── STAT CARDS (Section 2) ────────────────────────────── */
.demo-stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.8rem 1.4rem;
  height: 100%;
}
.demo-stat-number {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 3rem;
  font-weight: 500;
  color: var(--cyan);
  line-height: 1;
  margin-bottom: 0.4rem;
}
.demo-stat-label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text);
  margin-bottom: 0.5rem;
}
.demo-stat-context {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.6;
}
.demo-stat-source {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-faint);
  margin-top: 0.8rem;
}
/* ─── EDC CALLOUT (Section 2) ───────────────────────────── */
.demo-edc-callout {
  background: var(--bg-elevated);
  border-left: 3px solid var(--cyan);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.4rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-style: italic;
  color: var(--text-muted);
  line-height: 1.7;
  margin-top: 1.4rem;
}
/* ─── LEARNING LOOP (Section 3) ─────────────────────────── */
.demo-stage-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.6rem 1.2rem;
  text-align: center;
  height: 100%;
}
.demo-stage-icon  { font-size: 1.8rem; margin-bottom: 0.7rem; }
.demo-stage-num   { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: var(--cyan); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.demo-stage-label { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.95rem; color: var(--text); margin-bottom: 0.5rem; }
.demo-stage-body  { font-family: 'Inter', sans-serif; font-size: 0.8rem; color: var(--text-muted); line-height: 1.6; }
.demo-loop-callout {
  background: var(--bg-elevated);
  border-left: 3px solid var(--cyan);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 1.6rem;
  max-width: 640px;
}
/* ─── SCREENSHOT TABS (Section 4) ───────────────────────── */
.demo-screenshot-caption {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
  padding: 0.7rem 0 0;
  max-width: 680px;
  margin: 0 auto;
}
/* ─── DIFFERENTIATOR CARDS (Section 5) ──────────────────── */
.demo-diff-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.6rem 1.4rem;
  height: 100%;
}
.demo-diff-icon     { font-size: 1.4rem; margin-bottom: 0.6rem; }
.demo-diff-headline { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.95rem; color: var(--text); margin-bottom: 0.5rem; }
.demo-diff-body     { font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-muted); line-height: 1.65; }
/* ─── DOMAIN PILLS (Section 6) ──────────────────────────── */
.demo-domain-pill {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.1rem 1rem;
  height: 100%;
}
.demo-domain-emoji  { font-size: 1.3rem; margin-bottom: 0.4rem; }
.demo-domain-label  { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.85rem; color: var(--text); margin-bottom: 0.25rem; }
.demo-domain-reframe { font-family: 'Inter', sans-serif; font-size: 0.78rem; color: var(--cyan); line-height: 1.5; }
.demo-attribution   { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: var(--text-faint); text-align: center; margin-top: 1rem; }
/* ─── MASTERY PROGRESSION (Section 6) ──────────────────── */
.demo-mastery-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 1.4rem 0 0.6rem;
}
.demo-mastery-pill {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-muted);
  white-space: nowrap;
}
.demo-mastery-pill.active {
  border-color: var(--amber);
  color: var(--text);
  background: var(--bg-surface);
}
.demo-mastery-arrow { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: var(--border); }
.demo-mastery-note  { font-family: 'Inter', sans-serif; font-size: 0.78rem; color: var(--text-faint); text-align: center; margin-top: 0.4rem; }
/* ─── GET STARTED (Section 7) ───────────────────────────── */
.demo-cta-header   { text-align: center; padding: 1rem 0 2rem; }
.demo-cta-headline { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: var(--text); margin-bottom: 0.5rem; }
.demo-cta-sub      { font-family: 'Inter', sans-serif; font-size: 0.88rem; color: var(--text-muted); line-height: 1.7; }
/* ─── PILOT NOTE (Section 7) ────────────────────────────── */
.demo-pilot-note {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-style: italic;
  color: var(--text-muted);
  border-left: 2px solid var(--border);
  padding: 0.5rem 0.8rem;
  margin-top: 1rem;
  line-height: 1.6;
}
/* ─── ROADMAP CARDS (Section 8) ─────────────────────────── */
.demo-roadmap-card  { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem; height: 100%; }
.demo-roadmap-badge { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: var(--amber); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
.demo-roadmap-title { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.88rem; color: var(--text); margin-bottom: 0.35rem; }
.demo-roadmap-body  { font-family: 'Inter', sans-serif; font-size: 0.78rem; color: var(--text-muted); line-height: 1.6; }
</style>
"""

st.markdown(DEMO_CSS, unsafe_allow_html=True)


# ── Section 1 — Hero ──────────────────────────────────────────────────────────
if _lang == "zh":
    _wzh.render_hero_zh()
else:
    st.markdown("""
<div class="demo-hero">
  <div class="demo-eyebrow">Internal · AI Skills Platform</div>
  <div class="demo-headline">
    Turn every employee into an<br><em>AI-powered</em> professional.
  </div>
  <div class="demo-subhead">
    Not another e-learning course.<br>
    A diagnostic engine + personalized path + live AI coaching,
    built specifically for each role — and ready for your entire team.
  </div>
</div>
""", unsafe_allow_html=True)

_role_map = {v["title"]: k for k, v in ROLES.items()}
_available_roles = list(_role_map.keys())
_derived_name = user_email.split("@")[0].replace(".", " ").title()

_AI_TOOL_OPTIONS = [
    "Microsoft Copilot (M365 — Word, Excel, Teams, Outlook)",
    "GitHub Copilot / Cursor (coding)",
    "ChatGPT (browser / API)",
    "Google Gemini",
    "Databricks AI / internal LLM tools",
    "AI features in enterprise software (Salesforce, ServiceNow, etc.)",
    "None yet — just getting started",
]

# ── Profile import — Option A: LinkedIn URL ───────────────────────────────────
_li_url = st.text_input(
    t("welcome.li_url_label", _lang),
    placeholder="https://www.linkedin.com/in/your-profile",
    key="welcome_li_url",
)
if st.button(t("welcome.li_import_btn", _lang), key="li_import") and _li_url.strip():
    with st.spinner(t("welcome.li_spinner", _lang)):
        _li_text = _fetch_linkedin_via_gemini(_li_url.strip())
    if _li_text:
        st.session_state["welcome_q1"] = _li_text
    else:
        st.warning(t("welcome.li_import_failed", _lang))

# ── Profile import — Option B: file upload ────────────────────────────────────
from utils.doc_extract import extract_text as _extract_file_text

st.markdown(f"— {t('welcome.import_or', _lang)} —")
_uploaded = st.file_uploader(
    t("welcome.import_label", _lang),
    type=["pdf", "txt", "docx"],
    help=t("welcome.import_help", _lang),
    key="welcome_import",
)
if _uploaded is not None:
    _extracted = _extract_file_text(_uploaded)
    if _extracted:
        st.session_state["welcome_q1"] = _extracted
    else:
        st.warning(t("welcome.import_extract_failed", _lang))

with st.expander(t("welcome.import_linkedin", _lang), expanded=False):
    st.markdown(
        f"1. {t('welcome.import_step_1', _lang)}  \n"
        f"2. {t('welcome.import_step_2', _lang)}  \n"
        f"3. {t('welcome.import_step_3', _lang)}"
    )

# ── Intake form ───────────────────────────────────────────────────────────────
_q1_text = st.text_area(
    t("welcome.q1_label", _lang),
    placeholder=t("welcome.q1_placeholder", _lang),
    height=200,
    max_chars=1000,
    key="welcome_q1",
)

_selected_tools = st.multiselect(
    t("welcome.q2_label", _lang),
    options=_AI_TOOL_OPTIONS,
    key="welcome_q2_tools",
)

# Advanced options (demo / admin) — keeps role selector accessible without cluttering main flow
with st.expander(t("welcome.advanced_options_label", _lang), expanded=False):
    if len(_available_roles) == 1:
        st.info(t("welcome.your_role_info", _lang).format(role=_available_roles[0]))
        _selected_role = _available_roles[0]
    else:
        _selected_role = st.selectbox(
            t("welcome.role_select_label", _lang),
            options=[t("welcome.role_placeholder", _lang)] + _available_roles,
            key="welcome_role",
        )
    _display_name_val = st.text_input(
        t("welcome.display_name_label", _lang),
        value=_derived_name,
        key="welcome_display_name",
        help=t("welcome.display_name_help", _lang),
    )

_adv_role_placeholder = t("welcome.role_placeholder", _lang)

if st.button(
    t("welcome.cta_btn", _lang),
    use_container_width=False,
    type="primary",
    key="hero_cta",
):
    if not _q1_text or not _q1_text.strip():
        st.error(t("welcome.error_q1_empty", _lang))
    else:
        with st.spinner(t("welcome.spinner_parse", _lang)):
            # ── LLM parse of Q1 → structured intake_profile ───────────────
            _parse_prompt = (
                "Extract structured information from this employee job description or self-description. "
                "Return ONLY valid JSON with exactly these keys:\n"
                "  role_text: job title in 3-5 words\n"
                "  daily_tasks: list of 4-5 specific task strings (verbs, e.g. 'review credit applications')\n"
                "  magic_wish: the primary AI benefit this person would want, one sentence\n"
                "  industry: industry or sector in 2-3 words (e.g. 'project finance', 'insurance', 'engineering')\n"
                "  org_type: type of organization in 3-5 words (e.g. 'financial Crown corporation')\n"
                "  seniority: one of: junior, mid, senior, executive"
            )
            try:
                _raw = call_llm(
                    messages=[
                        {"role": "system", "content": _parse_prompt},
                        {"role": "user", "content": _q1_text.strip()},
                    ],
                    temperature=0.1,
                    user_email=user_email,
                    call_type="intake_parse",
                )
                # Strip markdown fences if present
                _raw_clean = _raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                _parsed = json.loads(_raw_clean)
            except Exception:
                # Graceful fallback — never block profile creation on LLM failure
                _parsed = {
                    "role_text": _q1_text.strip()[:50],
                    "daily_tasks": [],
                    "magic_wish": _q1_text.strip()[:100],
                }
            _parsed["ai_tools"] = _selected_tools

            # ── role_id: use Advanced Options selection if provided; else "universal" ──
            _adv_sel = st.session_state.get("welcome_role", _adv_role_placeholder)
            _inferred_role_id = _role_map.get(_adv_sel, "universal")

            # ── Display name from advanced options or email prefix ─────────
            _adv_name = st.session_state.get("welcome_display_name", "").strip()
            _display_name = _adv_name if _adv_name else _derived_name

        with st.spinner(t("welcome.spinner_setup", _lang)):
            try:
                create_profile(
                    user_email,
                    _display_name,
                    _inferred_role_id,
                    lang=_lang,
                    intake_profile=_parsed,
                )
                st.session_state["user_email"] = user_email
                st.session_state["user_state"] = "needs_diagnostic"
                st.session_state["_lang_from_profile"] = True
                st.switch_page("pages/01_Diagnostic.py")
            except Exception as err:
                st.error(t("welcome.error_create_profile", _lang) + f"\n\n_{err}_")

st.markdown('<hr class="demo-divider">', unsafe_allow_html=True)


# ── Section 2 — The Challenge ─────────────────────────────────────────────────
if _lang == "zh":
    _wzh.render_challenge_zh()
else:
    st.markdown("""
<div class="demo-section-label">The Challenge</div>
<div class="demo-section-heading">Your people are already using AI. The question is whether they're using it well.</div>
<div class="demo-section-sub">Three data points that make the case.</div>
""", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3, gap="medium")

    with sc1:
        st.markdown("""
<div class="demo-stat-card">
  <div class="demo-stat-number">68%</div>
  <div class="demo-stat-label">want AI training more than job security</div>
  <div class="demo-stat-context">Your people are asking for this. AI skills are the top professional development priority across every function.</div>
  <div class="demo-stat-source">Predictive Index, 2025</div>
</div>
""", unsafe_allow_html=True)

    with sc2:
        st.markdown("""
<div class="demo-stat-card">
  <div class="demo-stat-number">3×</div>
  <div class="demo-stat-label">more AI usage than leaders expect</div>
  <div class="demo-stat-context">Shadow AI is rampant. Employees are already using tools leaders haven't approved — without guardrails or training.</div>
  <div class="demo-stat-source">McKinsey Superagency Report, 2025</div>
</div>
""", unsafe_allow_html=True)

    with sc3:
        st.markdown("""
<div class="demo-stat-card">
  <div class="demo-stat-number">48%</div>
  <div class="demo-stat-label">cite lack of training as the #1 adoption blocker</div>
  <div class="demo-stat-context">Training unlocks ROI. Without it, AI tools sit underused or get misused — both outcomes cost you.</div>
  <div class="demo-stat-source">McKinsey Superagency Report, 2025</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="demo-edc-callout">
  Across the organization, over 100 employees have already submitted AI use case requests.
  Meeting support, document summarization, and email drafting rank as the top three needs.
  This platform builds the skills to do them right — securely, consistently, at scale.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="demo-divider">', unsafe_allow_html=True)


# ── Section 3 — The Learning Loop ────────────────────────────────────────────
if _lang == "zh":
    _wzh.render_loop_zh()
else:
    st.markdown("""
<div class="demo-section-label">How It Works</div>
<div class="demo-section-heading">The Learning Loop</div>
<div class="demo-section-sub">Four stages. One continuous cycle. Completely personalized.</div>
""", unsafe_allow_html=True)

    lc1, lc2, lc3, lc4 = st.columns(4, gap="medium")

    with lc1:
        st.markdown("""
<div class="demo-stage-card">
  <div class="demo-stage-icon">🎯</div>
  <div class="demo-stage-num">Stage 01</div>
  <div class="demo-stage-label">Diagnose</div>
  <div class="demo-stage-body">6 open-ended questions scored by AI — no right answers, just your real work. Takes ~5 minutes. Reveals your skill level across all 6 domains.</div>
</div>
""", unsafe_allow_html=True)

    with lc2:
        st.markdown("""
<div class="demo-stage-card">
  <div class="demo-stage-icon">🗺️</div>
  <div class="demo-stage-num">Stage 02</div>
  <div class="demo-stage-label">Map Gaps</div>
  <div class="demo-stage-body">AI generates a personalized narrative gap map and sequences your training path.</div>
</div>
""", unsafe_allow_html=True)

    with lc3:
        st.markdown("""
<div class="demo-stage-card">
  <div class="demo-stage-icon">🤖</div>
  <div class="demo-stage-num">Stage 03</div>
  <div class="demo-stage-label">Train</div>
  <div class="demo-stage-body">Role-specific scenarios + live AI coach. You practice; the coach responds to YOUR answers.</div>
</div>
""", unsafe_allow_html=True)

    with lc4:
        st.markdown("""
<div class="demo-stage-card">
  <div class="demo-stage-icon">📊</div>
  <div class="demo-stage-num">Stage 04</div>
  <div class="demo-stage-label">Score & Track</div>
  <div class="demo-stage-body">Hexagon skill radar updates after each module. Watch your gaps close over time.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="demo-loop-callout">
  <strong>The path is yours.</strong> Module 1 unlocks immediately based on your biggest gap —
  not a fixed curriculum everyone follows in the same order.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="demo-divider">', unsafe_allow_html=True)


# ── Section 4 — Inside the Platform ──────────────────────────────────────────
if _lang == "zh":
    _wzh.render_tour_header_zh()
else:
    st.markdown("""
<div class="demo-section-label">Product Tour</div>
<div class="demo-section-heading">Inside the Platform</div>
<div class="demo-section-sub">Five views. One integrated experience.</div>
""", unsafe_allow_html=True)

import os as _os

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t("welcome.tab_diagnostic", _lang),
    t("welcome.tab_skills_profile", _lang),
    t("welcome.tab_course_module", _lang),
    t("welcome.tab_ai_coach", _lang),
    t("welcome.tab_results", _lang),
])

_BASE = _os.path.join(_os.path.dirname(__file__), "..", "assets", "screenshots")

if _lang == "zh":
    _captions = _wzh.CAPTIONS_ZH
else:
    _captions = [
        "Six open-ended questions based on your own work. No multiple choice — you describe how you'd actually use AI. Takes ~5 minutes. Scores all 6 domains simultaneously.",
        "Your hexagon radar shows exactly where you stand. The AI-generated gap map turns raw scores into plain-language priorities you can act on today.",
        "Each module opens with a reading section that explains the core framework — then immediately asks you to apply it to a realistic work scenario.",
        "The AI coach responds to what you actually wrote — not a scripted flow. It asks follow-up questions, flags weak reasoning, and models better approaches in real time.",
        "After each module, you get a score breakdown by rubric criterion and a personalized coach note. Your hexagon radar updates immediately.",
    ]

_screenshots = {
    tab1: ("demo_01_diagnostic.png",     "demo_01_diagnostic.gif",     _captions[0]),
    tab2: ("demo_02_skills_profile.png", "demo_02_skills_profile.gif", _captions[1]),
    tab3: ("demo_03_course_module.png",  "demo_03_course_module.gif",  _captions[2]),
    tab4: ("demo_04_ai_coach.png",       "demo_04_ai_coach.gif",       _captions[3]),
    tab5: ("demo_05_results.png",        "demo_05_results.gif",        _captions[4]),
}

for tab, (png_name, gif_name, caption) in _screenshots.items():
    with tab:
        asset_path = None
        is_gif = False
        if gif_name:
            gif_path = _os.path.join(_BASE, gif_name)
            if _os.path.exists(gif_path):
                asset_path = gif_path
                is_gif = True
        if asset_path is None:
            png_path = _os.path.join(_BASE, png_name)
            if _os.path.exists(png_path):
                asset_path = png_path
        if asset_path:
            if is_gif:
                import base64 as _b64
                with open(asset_path, "rb") as _f:
                    _data = _b64.b64encode(_f.read()).decode()
                st.markdown(
                    f'<img src="data:image/gif;base64,{_data}" style="width:100%;border-radius:8px;">',
                    unsafe_allow_html=True,
                )
            else:
                st.image(asset_path, use_container_width=True)
        else:
            st.info(f"Screenshot not yet captured: `{png_name}`")
        st.markdown(f'<div class="demo-screenshot-caption">{caption}</div>', unsafe_allow_html=True)

st.markdown('<hr class="demo-divider">', unsafe_allow_html=True)


# ── Section 5 — What Makes It Different ──────────────────────────────────────
if _lang == "zh":
    _wzh.render_differentiators_zh()
else:
    st.markdown("""
<div class="demo-section-label">Differentiators</div>
<div class="demo-section-heading">What Makes It Different</div>
<div class="demo-section-sub">Four decisions that separate this from generic e-learning.</div>
""", unsafe_allow_html=True)

    dc1, dc2, dc3, dc4 = st.columns(4, gap="medium")

    with dc1:
        st.markdown("""
<div class="demo-diff-card">
  <div class="demo-diff-icon">🎯</div>
  <div class="demo-diff-headline">Your role. Your scenarios.</div>
  <div class="demo-diff-body">Every practice task is built around real work situations for your specific role — RM, Underwriter, Analyst. No generic "write a prompt about dogs" exercises.</div>
</div>
""", unsafe_allow_html=True)

    with dc2:
        st.markdown("""
<div class="demo-diff-card">
  <div class="demo-diff-icon">🤖</div>
  <div class="demo-diff-headline">An AI coach that actually reads your answer.</div>
  <div class="demo-diff-body">The coach sees exactly what you wrote and responds with contextual feedback. It can't be fooled by a vague answer — it will push back.</div>
</div>
""", unsafe_allow_html=True)

    with dc3:
        st.markdown("""
<div class="demo-diff-card">
  <div class="demo-diff-icon">🗺️</div>
  <div class="demo-diff-headline">Your gaps drive the sequence.</div>
  <div class="demo-diff-body">The diagnostic scores 6 domains. Module 1 is the domain where you need the most help — not the one that comes first alphabetically.</div>
</div>
""", unsafe_allow_html=True)

    with dc4:
        st.markdown("""
<div class="demo-diff-card">
  <div class="demo-diff-icon">🔒</div>
  <div class="demo-diff-headline">Your data never leaves your workspace.</div>
  <div class="demo-diff-body">Hosted on GCP Cloud Run and served from your organization's environment. No data sent to third-party training platforms. No external user accounts.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="demo-divider">', unsafe_allow_html=True)


# ── Section 6 — The Skill Model ───────────────────────────────────────────────
if _lang == "zh":
    _wzh.render_skill_model_zh()
    _wzh.render_mastery_zh()
else:
    st.markdown("""
<div class="demo-section-label">Skill Model</div>
<div class="demo-section-heading">Six Domains. One Hexagon.</div>
<div class="demo-section-sub">Every domain is scored independently. The diagnostic tells you exactly where you sit on each axis.</div>
""", unsafe_allow_html=True)

    _DOMAINS = [
        ("🛡️", "Responsible AI",           "Protect your professional reputation"),
        ("⚡",  "Strategic Prompting",      "Your personal productivity superpower"),
        ("🔍",  "Critical Evaluation",      "Never be caught out by an AI error"),
        ("📊",  "Data & Decision",          "Generate insights in minutes, not hours"),
        ("🤝",  "Relationship Intelligence","Know every stakeholder better than anyone"),
        ("✍️",  "Augmented Communication",  "Deliver polished outputs 3× faster"),
    ]

    row1 = st.columns(3, gap="medium")
    row2 = st.columns(3, gap="medium")

    for i, (emoji, label, reframe) in enumerate(_DOMAINS):
        col = row1[i] if i < 3 else row2[i - 3]
        with col:
            st.markdown(f"""
<div class="demo-domain-pill">
  <div class="demo-domain-emoji">{emoji}</div>
  <div class="demo-domain-label">{label}</div>
  <div class="demo-domain-reframe">{reframe}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="demo-attribution">
  Aligned with the Alan Turing Institute's AI Skills Framework for Knowledge Workers (2024).
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="demo-mastery-row">
  <span class="demo-mastery-pill">Unaware</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">Explorer</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill active">Practitioner</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">Proficient</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">Champion</span>
</div>
<div class="demo-mastery-note">Every domain is scored independently. The diagnostic tells you exactly where you sit on each axis.</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="demo-divider">', unsafe_allow_html=True)


# ── Section 8 — What's Coming ─────────────────────────────────────────────────
if _lang == "zh":
    _wzh.render_roadmap_header_zh()
else:
    st.markdown("""
<div class="demo-section-label">Roadmap</div>
<div class="demo-section-heading">What's Coming</div>
<div class="demo-section-sub">This is version 1. Three roles are live today.<br>The roadmap below reflects what's already being built.</div>
""", unsafe_allow_html=True)

with st.expander(t("welcome.roadmap_expander", _lang), expanded=False):
    if _lang == "zh":
        _wzh.render_roadmap_content_zh()
    else:
        rc1, rc2 = st.columns(2, gap="medium")

        with rc1:
            st.markdown("""
<div class="demo-roadmap-card" style="margin-bottom:1rem">
  <div class="demo-roadmap-badge">🔜 Phase 1</div>
  <div class="demo-roadmap-title">More roles</div>
  <div class="demo-roadmap-body">PM, Engineer, Legal, Finance — same methodology, role-specific scenarios built on the same 6-domain skill model.</div>
</div>
""", unsafe_allow_html=True)
            st.markdown("""
<div class="demo-roadmap-card">
  <div class="demo-roadmap-badge">🔜 Phase 3+</div>
  <div class="demo-roadmap-title">Board-ready metrics</div>
  <div class="demo-roadmap-body">% workforce at Practitioner+ per domain; exportable for quarterly reporting and board packs.</div>
</div>
""", unsafe_allow_html=True)

        with rc2:
            st.markdown("""
<div class="demo-roadmap-card" style="margin-bottom:1rem">
  <div class="demo-roadmap-badge">🔜 Phase 3+</div>
  <div class="demo-roadmap-title">Org-level dashboard</div>
  <div class="demo-roadmap-body">Admin view: completion rates, average scores by department, skill gap heatmap across the workforce.</div>
</div>
""", unsafe_allow_html=True)
            st.markdown("""
<div class="demo-roadmap-card">
  <div class="demo-roadmap-badge">🔜 Phase 1+</div>
  <div class="demo-roadmap-title">Microsoft Copilot track</div>
  <div class="demo-roadmap-body">A dedicated module covering M365 Copilot — the tool most frequently requested by employees.</div>
</div>
""", unsafe_allow_html=True)
