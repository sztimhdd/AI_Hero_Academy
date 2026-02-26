"""
Shared visual design system for AI Hero Academy.

Aesthetic direction: Deep-space command centre — dark obsidian backgrounds,
electric cyan/amber accents, IBM Plex Mono for data, DM Serif Display for
editorial headings. Feels like an internal dashboard built for professionals
who take their craft seriously.
"""

import os
import streamlit as st

# Colour tokens used in inline Python formatting strings
COLORS = {
    "bg_primary":    "#0D0F14",   # near-black
    "bg_surface":    "#161A22",   # card surface
    "bg_elevated":   "#1E2330",   # raised card / input area
    "border":        "#2A2F3E",   # subtle dividers
    "accent_cyan":   "#00D4E8",   # primary action / highlight
    "accent_amber":  "#F5A623",   # warning / quick-win
    "accent_red":    "#E8455A",   # danger / gap
    "accent_green":  "#29CC6A",   # success / complete
    "text_primary":  "#EDF0F7",   # main text
    "text_secondary":"#8990A8",   # muted text
    "text_muted":    "#8990A8",   # faint text — #545B70 fails WCAG AA (3:1); minimum passing is #8990A8 (6.6:1)
}


def inject_global_css():
    """Inject the full design system CSS once per page."""
    st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
/* ─── RESET & ROOT ─────────────────────────────────────────── */
:root {{
  --bg-primary:   {COLORS['bg_primary']};
  --bg-surface:   {COLORS['bg_surface']};
  --bg-elevated:  {COLORS['bg_elevated']};
  --border:       {COLORS['border']};
  --cyan:         {COLORS['accent_cyan']};
  --amber:        {COLORS['accent_amber']};
  --red:          {COLORS['accent_red']};
  --green:        {COLORS['accent_green']};
  --text:         {COLORS['text_primary']};
  --text-muted:   {COLORS['text_secondary']};
  --text-faint:   {COLORS['text_muted']};
}}

/* ─── STREAMLIT GLOBAL OVERRIDES ───────────────────────────── */
.stApp {{
  background-color: var(--bg-primary) !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}}

/* Hide default Streamlit header/toolbar
   Note: header[data-testid="stHeader"] has no stable public class alternative in
   Streamlit's CSS API; data-testid is the documented community approach. */
header[data-testid="stHeader"] {{ display: none !important; }}
.stToolbar {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}

/* ─── SIDEBAR ──────────────────────────────────────────────── */
/* Use .stSidebar class — stable across Streamlit versions; avoids data-testid.
   Background also set via config.toml [theme] secondaryBackgroundColor. */
section.stSidebar > div {{
  background-color: var(--bg-surface) !important;
  border-right: 1px solid var(--border) !important;
}}

section.stSidebar .stRadio label,
section.stSidebar p,
section.stSidebar span {{
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}}

/* Hide Streamlit's built-in sidebar collapse toggle — sidebar is always expanded
   and the Material Icons font is not loaded, causing icon text to bleed through
   as literal "keyboard_double_arrow_left" on hover (NAV2). */
[data-testid="collapsedControl"] {{ display: none !important; }}

/* ─── MAIN CONTENT AREA ────────────────────────────────────── */
/* Leave Streamlit's native max-width (readable-content width) alone.
   Only adjust vertical padding. */
.block-container {{
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
}}

/* ─── TYPOGRAPHY ───────────────────────────────────────────── */
h1 {{
  font-family: 'DM Serif Display', serif !important;
  font-size: 2.6rem !important;
  font-weight: 400 !important;
  color: var(--text) !important;
  letter-spacing: -0.02em !important;
  line-height: 1.15 !important;
}}
h2 {{
  font-family: 'DM Serif Display', serif !important;
  font-size: 1.7rem !important;
  font-weight: 400 !important;
  color: var(--text) !important;
  letter-spacing: -0.01em !important;
}}
h3 {{
  font-family: 'Inter', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  color: var(--text-muted) !important;
}}
p, li, .stMarkdown p {{
  color: var(--text) !important;
  font-size: 0.95rem !important;
  line-height: 1.65 !important;
}}

/* ─── BUTTONS ──────────────────────────────────────────────── */
/* Primary buttons: styled via config.toml [theme] primaryColor = "#00D4E8"
   Secondary buttons: explicit override required — primaryColor bleeds into all
   button types without it (NX2). Disabled state: handled natively by disabled=True. */
.stButton > button {{
  border-radius: 6px !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.04em !important;
  padding: 0.55rem 1.4rem !important;
  transition: all 0.15s ease !important;
}}

/* Secondary buttons — neutral to distinguish from primary CTA.
   data-testid="stBaseButton-secondary" is the documented community selector for
   secondary button containers; Streamlit has no stable public class for primary/
   secondary variants (same rationale as NX10, stInfo, stSuccess in this file). */
[data-testid="stBaseButton-secondary"] button {{
  background-color: transparent !important;
  color: {COLORS['text_primary']} !important;
  border: 1px solid {COLORS['border']} !important;
}}
[data-testid="stBaseButton-secondary"] button:hover {{
  background-color: {COLORS['bg_elevated']} !important;
  border-color: {COLORS['text_secondary']} !important;
}}

/* ─── INPUTS ───────────────────────────────────────────────── */
/* Resolved hex values used (not var()) to avoid Streamlit JS "Invalid color" warnings */
.stTextInput > div > input,
.stTextArea > div > textarea,
.stSelectbox > div > div {{
  background-color: {COLORS['bg_elevated']} !important;
  border: 1px solid {COLORS['border']} !important;
  border-radius: 6px !important;
  color: {COLORS['text_primary']} !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.9rem !important;
}}
.stTextInput > div > input:focus,
.stTextArea > div > textarea:focus {{
  border-color: {COLORS['accent_cyan']} !important;
  box-shadow: 0 0 0 2px rgba(0,212,232,0.15) !important;
  outline: none !important;
}}

/* Select box */
.stSelectbox > div > div[data-baseweb="select"] > div {{
  background-color: {COLORS['bg_elevated']} !important;
  border: 1px solid {COLORS['border']} !important;
  color: {COLORS['text_primary']} !important;
}}

/* ─── RADIO BUTTONS ────────────────────────────────────────── */
/* Resolved hex values (not var()) to avoid Streamlit JS "Invalid color" warnings */
.stRadio > div {{
  gap: 0.4rem !important;
}}
.stRadio label {{
  background: {COLORS['bg_elevated']} !important;
  border: 1px solid {COLORS['border']} !important;
  border-radius: 6px !important;
  padding: 0.7rem 1rem !important;
  cursor: pointer !important;
  transition: all 0.12s ease !important;
  display: flex !important;
  align-items: flex-start !important;
  gap: 0.6rem !important;
  color: {COLORS['text_primary']} !important;
}}
.stRadio label:hover {{
  border-color: {COLORS['accent_cyan']} !important;
  background: rgba(0,212,232,0.05) !important;
}}
.stRadio label[data-checked="true"] {{
  border-color: {COLORS['accent_cyan']} !important;
  background: rgba(0,212,232,0.1) !important;
}}

/* ─── PROGRESS BAR ─────────────────────────────────────────── */
/* Resolved hex values (not var()) to avoid Streamlit JS "Invalid color" warnings */
.stProgress > div > div > div {{
  background-color: {COLORS['bg_elevated']} !important;
  border-radius: 4px !important;
  height: 6px !important;
}}
.stProgress > div > div > div > div {{
  background: linear-gradient(90deg, {COLORS['accent_cyan']}, #0099AA) !important;
  border-radius: 4px !important;
}}

/* ─── DIVIDER ──────────────────────────────────────────────── */
/* Resolved hex (not var()) to avoid Streamlit JS "Invalid color" warnings */
hr {{
  border: none !important;
  border-top: 1px solid {COLORS['border']} !important;
  margin: 1.5rem 0 !important;
}}

/* ─── METRICS ──────────────────────────────────────────────── */
/* Use .stMetric / .stMetricLabel / .stMetricValue class names — stable in
   Streamlit ≥1.20; avoids data-testid for these elements.
   Resolved hex (not var()) to avoid Streamlit JS "Invalid color" warnings. */
.stMetric {{
  background: {COLORS['bg_surface']} !important;
  border: 1px solid {COLORS['border']} !important;
  border-radius: 8px !important;
  padding: 1rem 1.2rem !important;
}}
.stMetricLabel span {{
  color: {COLORS['text_secondary']} !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.75rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
}}
.stMetricValue {{
  color: {COLORS['text_primary']} !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 2rem !important;
}}

/* ─── INFO / WARNING / ERROR ────────────────────────────────── */
/* .stAlert covers all alert types generically.
   Per-variant colours use data-testid because Streamlit does not expose stable
   public class names for individual alert types (info/warning/error/success).
   This is the documented community approach; see NX10 in Issues.md.
   Resolved hex (not var()) to avoid Streamlit JS "Invalid color" warnings. */
.stAlert {{
  border-radius: 6px !important;
  border: 1px solid !important;
  background-color: {COLORS['bg_elevated']} !important;
  font-size: 0.88rem !important;
}}
div[data-testid="stInfo"] {{
  border-color: {COLORS['accent_cyan']} !important;
  background: rgba(0,212,232,0.08) !important;
  color: {COLORS['text_primary']} !important;
}}
div[data-testid="stSuccess"] {{
  border-color: {COLORS['accent_green']} !important;
  background: rgba(41,204,106,0.08) !important;
  color: {COLORS['text_primary']} !important;
}}
div[data-testid="stWarning"] {{
  border-color: {COLORS['accent_amber']} !important;
  background: rgba(245,166,35,0.08) !important;
  color: {COLORS['text_primary']} !important;
}}
div[data-testid="stError"] {{
  border-color: {COLORS['accent_red']} !important;
  background: rgba(232,69,90,0.08) !important;
  color: {COLORS['text_primary']} !important;
}}

/* ─── SPINNER / LOADING ─────────────────────────────────────── */
/* Resolved hex (not var()) to avoid Streamlit JS "Invalid color" warnings */
.stSpinner > div {{
  border-top-color: {COLORS['accent_cyan']} !important;
}}

/* ─── EXPANDER ─────────────────────────────────────────────── */
.streamlit-expanderHeader {{
  background-color: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--text) !important;
}}
.streamlit-expanderContent {{
  background-color: var(--bg-surface) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
}}

/* ─── CARD COMPONENT ───────────────────────────────────────── */
.aha-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
}}
.aha-card-elevated {{
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
}}
.aha-card-accent {{
  background: var(--bg-surface);
  border: 1px solid var(--cyan);
  border-left: 3px solid var(--cyan);
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
}}
.aha-card-warning {{
  background: var(--bg-surface);
  border: 1px solid var(--amber);
  border-left: 3px solid var(--amber);
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
}}
.aha-card-danger {{
  background: var(--bg-surface);
  border: 1px solid var(--red);
  border-left: 3px solid var(--red);
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
}}
.aha-card-success {{
  background: var(--bg-surface);
  border: 1px solid var(--green);
  border-left: 3px solid var(--green);
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
}}

/* ─── SCORE BAR COMPONENT ──────────────────────────────────── */
/* score_bar() replaced by st.progress() + st.columns (NX5 resolved) */

/* ─── MODULE CARD ──────────────────────────────────────────── */
/* module-card HTML replaced by st.container(border=True) (NX10/NX11 resolved).
   Inner content still uses module-title, module-domain-tag, sub-strip, sub-badge. */
.module-title {{
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
}}
.module-domain-tag {{
  display: inline-block;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 0.7rem;
  font-family: 'Inter', sans-serif;
  color: var(--text-muted);
  padding: 0.15rem 0.5rem;
  margin-right: 0.3rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

/* ─── SUBMODULE STATUS STRIP ────────────────────────────────── */
.sub-strip {{
  display: flex;
  gap: 0.3rem;
  align-items: center;
  margin-top: 0.5rem;
  margin-bottom: 0.75rem;   /* UI1: separates badge strip from action button below */
}}
.sub-badge {{
  font-size: 0.72rem;
  font-family: 'Inter', sans-serif;
  padding: 0.2rem 0.55rem;
  border-radius: 12px;
  font-weight: 500;
}}
.sub-badge.done    {{ background: rgba(41,204,106,0.15); color: var(--green); }}
.sub-badge.current {{ background: rgba(0,212,232,0.15);  color: var(--cyan);  }}
.sub-badge.pending {{ background: var(--bg-elevated);    color: var(--text-faint); }}

/* ─── DIAGNOSTIC / QUIZ QUESTION AREA ──────────────────────── */
.question-counter {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.78rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.25rem;
}}
.domain-tag-inline {{
  display: inline-block;
  background: rgba(0,212,232,0.1);
  border: 1px solid rgba(0,212,232,0.3);
  color: var(--cyan);
  font-size: 0.7rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  display: inline-block;
}}
.question-text {{
  font-family: 'Inter', sans-serif;
  font-size: 1.05rem;
  font-weight: 500;
  color: var(--text);
  line-height: 1.5;
  margin-bottom: 1.2rem;
}}
.scenario-box {{
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  font-size: 0.88rem;
  line-height: 1.65;
  color: var(--text);
  margin-bottom: 1.2rem;
  font-family: 'Inter', sans-serif;
}}
.scenario-box pre {{
  white-space: pre-wrap;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.82rem;
  color: var(--text);
}}

/* ─── COACH PANEL ──────────────────────────────────────────── */
/* Chat UI now uses st.chat_message() native components (NX1 resolved).
   Coach label still used in Results sub-view coach note. */
.coach-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--cyan);
}}

/* ─── READING CONTENT BLOCKS ────────────────────────────────── */
/* reading-example-box, reading-antipattern-box, reading-takeaway-box replaced
   by st.success(), st.error(), st.info() (NX9 resolved) */
.reading-concept {{
  line-height: 1.8;
  font-size: 0.95rem;
  color: var(--text);
  margin-bottom: 1.5rem;
}}

/* ─── GAP MAP BULLETS ──────────────────────────────────────── */
.gap-bullet {{
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  padding: 0.7rem 0;
  border-bottom: 1px solid var(--border);
}}
.gap-bullet:last-child {{ border-bottom: none; }}
.gap-priority-dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 0.35rem;
  flex-shrink: 0;
}}
.gap-priority-dot.high    {{ background: var(--red); }}
.gap-priority-dot.medium  {{ background: var(--amber); }}
.gap-priority-dot.low     {{ background: var(--green); }}
.gap-domain-name {{
  font-weight: 600;
  font-size: 0.82rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 0.2rem;
}}
.gap-bullet-text {{
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--text);
}}

/* ─── HISTORY TABLE ────────────────────────────────────────── */
table {{
  width: 100%;
  border-collapse: collapse;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
}}
th {{
  background: var(--bg-elevated);
  color: var(--text-muted);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  font-weight: 600;
  padding: 0.65rem 0.9rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}}
td {{
  padding: 0.65rem 0.9rem;
  color: var(--text);
  border-bottom: 1px solid var(--border);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.82rem;
}}
tr:last-child td {{ border-bottom: none; }}

/* ─── PAGE SECTION HEADERS ──────────────────────────────────── */
.section-header {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 2rem 0 1rem;
}}
.section-header-line {{
  flex: 1;
  height: 1px;
  background: var(--border);
}}
.section-header-text {{
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-faint);
  white-space: nowrap;
}}

/* ─── OVERALL SCORE DISPLAY ─────────────────────────────────── */
/* score-hero replaced by st.metric() (NX4 resolved) */

/* ─── LOGO / BRAND MARK ─────────────────────────────────────── */
.aha-brand {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.25rem;
}}
.aha-brand-icon {{
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--cyan), #0066AA);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}}
.aha-brand-name {{
  font-family: 'DM Serif Display', serif;
  font-size: 1.2rem;
  color: var(--text);
  letter-spacing: -0.01em;
}}
.aha-brand-name span {{
  color: var(--cyan);
}}

/* ─── WELCOME HERO ──────────────────────────────────────────── */
.welcome-hero {{
  padding: 3rem 0 2rem;
}}
.welcome-eyebrow {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--cyan);
  margin-bottom: 1rem;
}}
.welcome-headline {{
  font-family: 'DM Serif Display', serif;
  font-size: 3.2rem;
  line-height: 1.1;
  color: var(--text);
  letter-spacing: -0.02em;
  margin-bottom: 1.2rem;
}}
.welcome-headline em {{
  font-style: italic;
  color: var(--cyan);
}}
.welcome-body {{
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-muted);
  max-width: 540px;
  margin-bottom: 2rem;
}}

/* ─── RESULT SCORE BOX ──────────────────────────────────────── */
/* result-score-box replaced by st.metric() (NX4 resolved) */

/* ─── TASK INDICATOR ────────────────────────────────────────── */
.task-indicator {{
  display: inline-block;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-muted);
  padding: 0.2rem 0.55rem;
  margin-bottom: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}

/* ─── STEP PROGRESS STRIP ───────────────────────────────────── */
.step-strip {{
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 2rem;
}}
.step-item {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  flex: 1;
}}
.step-circle {{
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--bg-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-faint);
}}
.step-circle.done    {{ border-color: var(--green); background: rgba(41,204,106,0.15); color: var(--green); }}
.step-circle.current {{ border-color: var(--cyan);  background: rgba(0,212,232,0.15);  color: var(--cyan); }}
.step-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.68rem;
  color: var(--text-faint);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}
.step-label.current {{ color: var(--cyan); }}
.step-connector {{
  flex: 1;
  height: 1px;
  background: var(--border);
  margin-top: -1.2rem;
}}

/* Chat bubbles removed — replaced with st.chat_message() (NX1 resolved) */
</style>
""", unsafe_allow_html=True)

    if os.environ.get("LOCAL_UAT") == "true":
        _uat_email = os.environ.get("DEV_USER_EMAIL", "dev@example.com")
        st.sidebar.markdown(
            f"""<div style="background:rgba(245,166,35,0.10);border:1px solid #F5A623;"""
            f"""border-radius:6px;padding:0.5rem 0.75rem;font-family:'IBM Plex Mono',"""
            f"""monospace;font-size:0.72rem;color:#F5A623;margin-bottom:0.5rem;">"""
            f"""⚠ UAT MODE<br>"""
            f"""<span style="color:#8990A8;font-size:0.68rem;">{_uat_email}</span>"""
            f"""</div>""",
            unsafe_allow_html=True,
        )


def section_header(label: str):
    """Render a divider with a centred label."""
    st.markdown(f"""
<div class="section-header">
  <div class="section-header-line"></div>
  <div class="section-header-text">{label}</div>
  <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)



def step_progress_strip(steps: list[dict]):
    """
    steps: [{"label": str, "state": "done"|"current"|"pending"}, ...]
    """
    parts = []
    for i, step in enumerate(steps):
        state = step["state"]
        icon = "✓" if state == "done" else str(i + 1)
        parts.append(f"""
  <div class="step-item">
    <div class="step-circle {state}">{icon}</div>
    <div class="step-label {state if state != 'pending' else ''}">{step['label']}</div>
  </div>
""")
        if i < len(steps) - 1:
            parts.append('<div class="step-connector"></div>')
    st.markdown(f'<div class="step-strip">{"".join(parts)}</div>', unsafe_allow_html=True)


def render_sidebar(
    active_page: str,
    has_course: bool = False,
    progress_rows: list = None,
    active_course_id: str = None,
    module_context: dict = None,
):
    """
    Render consistent sidebar navigation on all post-diagnostic pages (NAV1).

    active_page: "home" | "skills_profile" | "course_module"
    has_course:  True if the user has training_progress rows
    progress_rows: list of progress dicts (needed for CX3 My Course navigation)
    active_course_id: current course_id (Course Module only)
    module_context: {"seq_order": int, "course_title": str, "domain_display": str}
                    — rendered as a context block on Course Module only
    """
    with st.sidebar:
        st.markdown("""
<div style="padding:1rem 0.5rem">
  <div class="aha-brand">
    <div class="aha-brand-icon" style="width:28px;height:28px;font-size:0.9rem">⚡</div>
    <div class="aha-brand-name" style="font-size:0.95rem">AI <span>Hero</span> Academy</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("---")

        if st.button("🏠  My Training", use_container_width=True, disabled=(active_page == "home")):
            st.switch_page("pages/03_Home.py")

        if st.button("🏅  Skills Profile", use_container_width=True, disabled=(active_page == "skills_profile")):
            st.switch_page("pages/02_Skills_Profile.py")

        if has_course:
            if st.button("📚  My Course", use_container_width=True, disabled=(active_page == "course_module")):
                # CX3: find the active (unlocked, incomplete) module to navigate directly to it
                if progress_rows:
                    _active = next(
                        (r for r in progress_rows
                         if str(r.get("is_locked", "true")).lower() == "false"
                         and not r.get("evaluation_completed_at")),
                        progress_rows[0] if progress_rows else None,
                    )
                    if _active:
                        st.session_state["active_course_id"] = _active["course_id"]
                        st.session_state["active_submodule"] = "overview"
                st.switch_page("pages/04_Course_Module.py")

        # Module context block — rendered on Course Module only
        if active_page == "course_module" and active_course_id and module_context:
            seq = module_context.get("seq_order", "")
            title = module_context.get("course_title", "")
            domain_display = module_context.get("domain_display", "")
            st.markdown(
                f'<div style="padding:1rem 0.5rem; font-family:\'Inter\',sans-serif;'
                f' font-size:0.75rem; color:#8990A8">'
                f'<div style="font-weight:600; text-transform:uppercase; letter-spacing:0.08em;'
                f' color:#8990A8; margin-bottom:0.5rem">Module {seq}</div>'
                f'<div style="color:#EDF0F7; line-height:1.4; margin-bottom:0.8rem">{title}</div>'
                f'<div class="module-domain-tag">{domain_display}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
