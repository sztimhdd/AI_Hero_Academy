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

/* Hide default Streamlit header/toolbar */
header[data-testid="stHeader"] {{ display: none !important; }}
.stToolbar {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}

/* ─── SIDEBAR ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] > div {{
  background-color: var(--bg-surface) !important;
  border-right: 1px solid var(--border) !important;
}}

section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {{
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}}

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
.stButton > button {{
  background: var(--cyan) !important;
  color: var(--bg-primary) !important;
  border: none !important;
  border-radius: 6px !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.04em !important;
  padding: 0.55rem 1.4rem !important;
  transition: all 0.15s ease !important;
  cursor: pointer !important;
}}
.stButton > button:hover {{
  background: #00B8CA !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(0, 212, 232, 0.25) !important;
}}
.stButton > button:disabled {{
  background: var(--bg-elevated) !important;
  color: var(--text-faint) !important;
  cursor: not-allowed !important;
  transform: none !important;
  box-shadow: none !important;
}}

/* Secondary button variant (applied via st.markdown wrapping) */
.btn-secondary > button,
button.btn-secondary {{
  background: transparent !important;
  color: var(--cyan) !important;
  border: 1px solid var(--border) !important;
}}
.btn-secondary > button:hover {{
  background: rgba(0,212,232,0.08) !important;
  border-color: var(--cyan) !important;
}}

/* ─── INPUTS ───────────────────────────────────────────────── */
.stTextInput > div > input,
.stTextArea > div > textarea,
.stSelectbox > div > div {{
  background-color: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.9rem !important;
}}
.stTextInput > div > input:focus,
.stTextArea > div > textarea:focus {{
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 2px rgba(0,212,232,0.15) !important;
  outline: none !important;
}}

/* Select box */
.stSelectbox > div > div[data-baseweb="select"] > div {{
  background-color: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}}

/* ─── RADIO BUTTONS ────────────────────────────────────────── */
.stRadio > div {{
  gap: 0.4rem !important;
}}
.stRadio label {{
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  padding: 0.7rem 1rem !important;
  cursor: pointer !important;
  transition: all 0.12s ease !important;
  display: flex !important;
  align-items: flex-start !important;
  gap: 0.6rem !important;
  color: var(--text) !important;
}}
.stRadio label:hover {{
  border-color: var(--cyan) !important;
  background: rgba(0,212,232,0.05) !important;
}}
.stRadio label[data-checked="true"] {{
  border-color: var(--cyan) !important;
  background: rgba(0,212,232,0.1) !important;
}}

/* ─── PROGRESS BAR ─────────────────────────────────────────── */
.stProgress > div > div > div {{
  background-color: var(--bg-elevated) !important;
  border-radius: 4px !important;
  height: 6px !important;
}}
.stProgress > div > div > div > div {{
  background: linear-gradient(90deg, var(--cyan), #0099AA) !important;
  border-radius: 4px !important;
}}

/* ─── DIVIDER ──────────────────────────────────────────────── */
hr {{
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 1.5rem 0 !important;
}}

/* ─── METRICS ──────────────────────────────────────────────── */
[data-testid="stMetric"] {{
  background: var(--bg-surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 1rem 1.2rem !important;
}}
[data-testid="stMetricLabel"] span {{
  color: var(--text-muted) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.75rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
}}
[data-testid="stMetricValue"] {{
  color: var(--text) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 2rem !important;
}}

/* ─── INFO / WARNING / ERROR ────────────────────────────────── */
.stAlert {{
  border-radius: 6px !important;
  border: 1px solid !important;
  background-color: var(--bg-elevated) !important;
  font-size: 0.88rem !important;
}}
div[data-testid="stInfo"] {{
  border-color: var(--cyan) !important;
  background: rgba(0,212,232,0.08) !important;
  color: var(--text) !important;
}}
div[data-testid="stSuccess"] {{
  border-color: var(--green) !important;
  background: rgba(41,204,106,0.08) !important;
  color: var(--text) !important;
}}
div[data-testid="stWarning"] {{
  border-color: var(--amber) !important;
  background: rgba(245,166,35,0.08) !important;
  color: var(--text) !important;
}}
div[data-testid="stError"] {{
  border-color: var(--red) !important;
  background: rgba(232,69,90,0.08) !important;
  color: var(--text) !important;
}}

/* ─── SPINNER / LOADING ─────────────────────────────────────── */
.stSpinner > div {{
  border-top-color: var(--cyan) !important;
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
.score-bar-container {{
  margin: 0.6rem 0;
}}
.score-bar-header {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.35rem;
}}
.score-bar-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  color: var(--text);
  font-weight: 500;
}}
.score-bar-value {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.85rem;
  color: var(--text-muted);
}}
.score-bar-track {{
  width: 100%;
  height: 8px;
  background: var(--bg-elevated);
  border-radius: 4px;
  overflow: hidden;
}}
.score-bar-fill {{
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}}
.score-bar-fill.danger  {{ background: var(--red); }}
.score-bar-fill.warning {{ background: var(--amber); }}
.score-bar-fill.success {{ background: var(--green); }}

/* ─── MODULE CARD ──────────────────────────────────────────── */
.module-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}}
.module-card.active {{
  border-color: var(--cyan);
  background: linear-gradient(135deg, rgba(0,212,232,0.06), var(--bg-surface));
}}
.module-card.completed {{
  border-color: var(--green);
  background: linear-gradient(135deg, rgba(41,204,106,0.05), var(--bg-surface));
}}
.module-card.locked {{
  opacity: 0.5;
}}

/* ─── MODULE CARD + ACTION BUTTON ATTACHMENT ────────────────
   Active and completed cards have a Streamlit button rendered
   immediately below their HTML block. These rules remove the
   visual gap so the button reads as the card's footer CTA.    */
.element-container:has(.module-card.active) .module-card.active,
.element-container:has(.module-card.completed) .module-card.completed {{
  border-bottom-left-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
  border-bottom: none !important;
  margin-bottom: 0 !important;
  padding-bottom: 1rem !important;
}}
.element-container:has(.module-card.active) + .element-container [data-testid="stButton"] > button {{
  border-top-left-radius: 0 !important;
  border-top-right-radius: 0 !important;
  border-top: 1px solid var(--cyan) !important;
  margin-top: 0 !important;
  width: 100% !important;
}}
.element-container:has(.module-card.completed) + .element-container [data-testid="stButton"] > button {{
  border-top-left-radius: 0 !important;
  border-top-right-radius: 0 !important;
  border-top: 1px solid var(--green) !important;
  margin-top: 0 !important;
  width: 100% !important;
}}
.module-number {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem;
  color: var(--text-faint);
  min-width: 2rem;
}}
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
.coach-header {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.6rem;
}}
.coach-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--cyan);
}}
.coach-message {{
  background: var(--bg-elevated);
  border: 1px solid rgba(0,212,232,0.2);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  font-size: 0.9rem;
  line-height: 1.65;
  color: var(--text);
  margin-bottom: 0.8rem;
}}
.turn-counter {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-faint);
  text-align: right;
}}

/* ─── READING CONTENT BLOCKS ────────────────────────────────── */
.reading-concept {{
  line-height: 1.8;
  font-size: 0.95rem;
  color: var(--text);
  margin-bottom: 1.5rem;
}}
.reading-example-box {{
  background: rgba(41,204,106,0.06);
  border: 1px solid rgba(41,204,106,0.25);
  border-left: 3px solid var(--green);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.2rem;
}}
.reading-example-box .box-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--green);
  margin-bottom: 0.5rem;
}}
.reading-antipattern-box {{
  background: rgba(232,69,90,0.06);
  border: 1px solid rgba(232,69,90,0.25);
  border-left: 3px solid var(--red);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.2rem;
}}
.reading-antipattern-box .box-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--red);
  margin-bottom: 0.5rem;
}}
.reading-takeaway-box {{
  background: rgba(0,212,232,0.06);
  border: 1px solid rgba(0,212,232,0.25);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.2rem;
}}
.reading-takeaway-box .box-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--cyan);
  margin-bottom: 0.5rem;
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
.score-hero {{
  text-align: center;
  padding: 2rem 0 1rem;
}}
.score-hero-number {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 4rem;
  font-weight: 500;
  color: var(--cyan);
  line-height: 1;
}}
.score-hero-denom {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.5rem;
  color: var(--text-faint);
}}
.score-hero-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-top: 0.4rem;
}}

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
.result-score-box {{
  background: linear-gradient(135deg, rgba(0,212,232,0.08), var(--bg-surface));
  border: 1px solid rgba(0,212,232,0.3);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
}}

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

/* ─── CHAT BUBBLE ───────────────────────────────────────────── */
.chat-bubble-user {{
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 8px 8px 2px 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--text);
  max-width: 85%;
  margin-left: auto;
}}
.chat-bubble-coach {{
  background: rgba(0,212,232,0.06);
  border: 1px solid rgba(0,212,232,0.15);
  border-radius: 8px 8px 8px 2px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--text);
  max-width: 85%;
}}
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


def score_bar(label: str, score: float, max_score: float = 4.0, color_class: str = "success"):
    """Render a labelled score progress bar."""
    pct = min(100, int(score / max_score * 100))
    st.markdown(f"""
<div class="score-bar-container">
  <div class="score-bar-header">
    <span class="score-bar-label">{label}</span>
    <span class="score-bar-value">{score:.1f} / {max_score:.1f}</span>
  </div>
  <div class="score-bar-track">
    <div class="score-bar-fill {color_class}" style="width:{pct}%"></div>
  </div>
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
