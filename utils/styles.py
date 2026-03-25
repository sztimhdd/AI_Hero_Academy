"""
Shared visual design system for AI Hero Academy.

Aesthetic direction: Deep-space command centre — dark obsidian backgrounds,
electric cyan/amber accents, JetBrains Mono for data, DM Serif Display for
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
    "text_secondary":"#8990A8",   # body copy, card text, sub-headings
    "text_muted":    "#6B7280",   # secondary labels, helper text
    "text_faint":    "#4B5268",   # citations, source labels, footnotes
    # Signal grammar — AI-generated content accent
    "accent_indigo":        "#6366F1",
    "accent_indigo_glow":   "rgba(99,102,241,0.12)",
    "accent_indigo_border": "rgba(99,102,241,0.30)",
}


def inject_global_css():
    """Inject the full design system CSS once per page."""
    st.markdown(f"""
<style>
/* ─── RESET & ROOT ─────────────────────────────────────────── */
/* Fonts loaded natively via .streamlit/config.toml (Streamlit 1.55+):
   Inter (body), DM Serif Display (heading), JetBrains Mono (code) */
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
  --text-faint:   {COLORS['text_faint']};
  --indigo:        {COLORS['accent_indigo']};
  --indigo-glow:   {COLORS['accent_indigo_glow']};
  --indigo-border: {COLORS['accent_indigo_border']};
  --accent_green:  {COLORS['accent_green']};
  --accent_red:    {COLORS['accent_red']};
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
   as literal "keyboard_double_arrow_left" on hover (NAV2).
   Confirmed via UAT: actual testid is stSidebarCollapseButton (not collapsedControl). */
[data-testid="stSidebarCollapseButton"] {{ display: none !important; }}

/* ─── MAIN CONTENT AREA ────────────────────────────────────── */
/* Streamlit 1.54 wraps .block-container in [data-testid="stMain"], a
   column-flex with align-items: center. Without a width override, a
   max-width cap causes the container to be CENTERED in the main area,
   producing a large gap between the sidebar and content on wide displays.
   Fix: width: 100% fills the available space on narrow screens; on wide
   screens max-width kicks in and align-self: flex-start pins it to the
   left edge of stMain (no centering gap). */
.block-container {{
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
  max-width: 1400px !important;
  width: 100% !important;
  align-self: flex-start !important;
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
  font-family: 'JetBrains Mono', monospace !important;
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
/* Streamlit 1.40+ renders expanders as <details data-testid="stExpander">.
   The old .streamlit-expanderHeader / .streamlit-expanderContent class
   selectors are gone as of Streamlit 1.40 and have no effect.
   E2E confirmed: container = [data-testid="stExpander"], header = summary. */
[data-testid="stExpander"] summary {{
  background-color: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--text) !important;
}}
[data-testid="stExpander"] > div {{
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
  font-family: 'JetBrains Mono', monospace;
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
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  color: var(--text);
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
  font-family: 'JetBrains Mono', monospace;
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
  font-family: 'JetBrains Mono', monospace;
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
  font-family: 'JetBrains Mono', monospace;
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
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-faint);
}}
.step-circle.done    {{ border-color: var(--cyan); background: var(--cyan); color: #0D0F14; }}
.step-circle.done::after {{ content: '✓'; font-size: 0.6rem; }}
.step-circle.current {{ border-color: var(--cyan); background: var(--cyan); color: #0D0F14; box-shadow: 0 0 0 3px rgba(0,212,232,0.25); }}
.step-circle.pending {{ background: transparent; border: 2px solid var(--border); color: var(--text-faint); }}
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

/* ── Signal grammar ─────────────────────────────── */
.ai-card {{
  background: var(--indigo-glow);
  border-left: 3px solid var(--indigo-border);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
}}
.ai-card-label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--indigo);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}}

/* ── Reading content cards ───────────────────────── */
.read-concept-card {{ background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.6rem; }}
.read-principle-callout {{ background: var(--bg-elevated); border-left: 3px solid var(--indigo); border-radius: 0 6px 6px 0; padding: 0.9rem 1.1rem; margin-top: 1rem; font-size: 0.88rem; color: var(--text); }}
.read-split {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.8rem; }}
.read-split-bad  {{ background: rgba(232,69,90,0.08); border: 1px solid rgba(232,69,90,0.25); border-radius: 8px; padding: 1rem; }}
.read-split-good {{ background: rgba(41,204,106,0.08); border: 1px solid rgba(41,204,106,0.25); border-radius: 8px; padding: 1rem; }}
.read-split-label {{ font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }}
.read-pitfall-card {{ background: rgba(232,69,90,0.06); border-left: 3px solid var(--red); border-radius: 0 8px 8px 0; padding: 1.2rem 1.4rem; }}
.read-takeaway-card {{ background: rgba(0,212,232,0.07); border: 1px solid rgba(0,212,232,0.25); border-radius: 12px; padding: 1.4rem; text-align: center; }}

/* ── Chat bubbles ────────────────────────────────── */
.chat-user-bubble {{
  margin-left: auto; max-width: 78%;
  background: var(--bg-elevated); border: 1px solid var(--border);
  border-radius: 16px 16px 4px 16px; padding: 0.75rem 1rem;
  font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text);
}}
.chat-coach-bubble {{
  max-width: 88%;
  background: var(--indigo-glow); border-left: 3px solid var(--indigo-border);
  border-radius: 4px 16px 16px 16px; padding: 0.75rem 1rem;
  font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text);
}}
.chat-coach-label {{
  font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
  color: var(--indigo); text-transform: uppercase;
  letter-spacing: 0.1em; margin-bottom: 0.4rem;
}}

/* ── MCQ option cards ────────────────────────────── */
.mcq-option {{
  border: 1px solid var(--border); border-radius: 8px;
  padding: 0.85rem 1.1rem; margin-bottom: 0.5rem;
  cursor: pointer; transition: border-color 150ms ease-out, background 150ms ease-out;
  font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text);
}}
.mcq-option:hover {{ border-color: var(--cyan); background: rgba(0,212,232,0.06); }}
.mcq-option.selected {{ border-color: var(--cyan); background: rgba(0,212,232,0.10); }}

/* ── Eval top progress rail ──────────────────────── */
.eval-progress-rail-track {{
  position: fixed; top: 0; left: 0; right: 0; height: 3px;
  background: var(--border); z-index: 999;
}}
.eval-progress-rail-fill {{
  height: 100%; background: var(--cyan);
  transition: width 400ms ease;
  box-shadow: 0 0 8px rgba(0,212,232,0.5);
}}

/* ── Score card ──────────────────────────────────── */
.score-card {{ text-align: center; padding: 2rem 0 1.5rem; }}
.score-number {{ font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; font-weight: 500; color: var(--cyan); line-height: 1; }}
.score-level {{ font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--cyan); margin-top: 0.4rem; }}
.score-delta-pos {{ font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent_green); margin-top: 0.3rem; }}
.score-delta-neg {{ font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent_red); margin-top: 0.3rem; }}

/* ── Themed progress bar ─────────────────────────── */
.themed-progress-track {{ background: var(--bg-elevated); border-radius: 4px; height: 6px; overflow: hidden; margin: 0.4rem 0; }}
.themed-progress-fill  {{ height: 100%; background: linear-gradient(90deg, var(--cyan), #0099AA); border-radius: 4px; transition: width 0.5s ease; }}

/* ── Domain tag pill ─────────────────────────────── */
.domain-tag-pill {{
  display: inline-block; font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--cyan); background: rgba(0,212,232,0.08);
  border: 1px solid rgba(0,212,232,0.2); border-radius: 4px;
  padding: 0.2rem 0.6rem; margin-bottom: 1rem;
}}

/* ── Global accessibility ────────────────────────── */
html {{ scroll-behavior: smooth; }}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
}}



/* ─── SEGMENTED CONTROL CENTERING ──────────────────────────── */
/* stVerticalBlock is a column-flex; stElementContainer children
   default to align-self: flex-start (shrink-wrap width).
   Target the specific widget via its session-state key class. */
.st-key-reading_section_ctrl {{
  align-self: center;
}}

/* ─── CODE BLOCK WRAPPING ──────────────────────────────────── */
/* st.code() renders inside .stCode > pre; override pre's default
   white-space:pre so long prompt examples wrap in the reading pane.
   word-break / overflow-wrap are omitted — Streamlit 1.50+ applies
   these at the container level natively. */
.stCode pre,
.stCode code {{
  white-space: pre-wrap !important;
}}
</style>
""", unsafe_allow_html=True)

    # Detect ?demo=true on ANY page URL and initialize demo mode session state.
    # Works on deployed app and locally — not gated by LOCAL_UAT.
    if (
        st.query_params.get("demo") == "true"
        and not st.session_state.get("demo_mode")
    ):
        from utils.demo import DEMO_PROFILES, DEFAULT_PROFILE, ensure_demo_seeded
        profile_id = st.query_params.get("profile", DEFAULT_PROFILE)
        if profile_id not in DEMO_PROFILES:
            profile_id = DEFAULT_PROFILE
        st.session_state["demo_mode"] = True
        st.session_state["demo_profile_id"] = profile_id
        ensure_demo_seeded(profile_id)
        for key in ["user_email", "user_state", "role_id"]:
            st.session_state.pop(key, None)
        st.rerun()

    if os.environ.get("LOCAL_UAT") == "true":
        _uat_email = os.environ.get("DEV_USER_EMAIL", "dev@example.com")
        st.sidebar.markdown(
            f"""<div style="background:rgba(245,166,35,0.10);border:1px solid #F5A623;"""
            f"""border-radius:6px;padding:0.5rem 0.75rem;font-family:'JetBrains Mono',"""
            f"""monospace;font-size:0.72rem;color:#F5A623;margin-bottom:0.5rem;">"""
            f"""⚠ UAT MODE<br>"""
            f"""<span style="color:#8990A8;font-size:0.68rem;">{_uat_email}</span>"""
            f"""</div>""",
            unsafe_allow_html=True,
        )

    if st.session_state.get("demo_mode"):
        from utils.demo import DEMO_PROFILES, DEFAULT_PROFILE, ensure_demo_seeded
        with st.sidebar:
            st.markdown("**🎭 Demo Mode**")
            profile_labels = {pid: p["label"] for pid, p in DEMO_PROFILES.items()}
            current_id = st.session_state.get("demo_profile_id", DEFAULT_PROFILE)
            selected_label = st.selectbox(
                "Demo profile",
                options=list(profile_labels.values()),
                index=list(profile_labels.keys()).index(current_id),
                key="demo_profile_select",
                label_visibility="collapsed",
            )
            selected_id = next(k for k, v in profile_labels.items() if v == selected_label)
            if selected_id != current_id:
                ensure_demo_seeded(selected_id)
                keys_to_clear = [
                    k for k in st.session_state
                    if k not in ("demo_mode", "demo_profile_id", "demo_profile_select")
                ]
                for k in keys_to_clear:
                    del st.session_state[k]
                st.session_state["demo_profile_id"] = selected_id
                st.rerun()
            st.divider()

    # ── Language initialisation (browser detection on first load) ─────────────
    if "lang" not in st.session_state:
        from utils.i18n import detect_browser_lang
        st.session_state["lang"] = detect_browser_lang()


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
    user_email: str = None,
    lang: str = None,
):
    """
    Render consistent sidebar navigation on all post-diagnostic pages (NAV1).

    active_page: "home" | "skills_profile" | "course_module"
    has_course:  True if the user has training_progress rows
    progress_rows: list of progress dicts (needed for CX3 My Course navigation)
    active_course_id: current course_id (Course Module only)
    module_context: {"seq_order": int, "course_title": str, "domain_display": str}
                    — rendered as a context block on Course Module only
    user_email: if provided, show language toggle (omit on Welcome page)
    lang: current language code; defaults to st.session_state["lang"] or "en"
    """
    from utils.i18n import t, SUPPORTED_LANGS
    if lang is None:
        lang = st.session_state.get("lang", "en")

    with st.sidebar:
        st.markdown("""
<div style="padding:1rem 0.5rem">
  <div class="aha-brand">
    <div class="aha-brand-icon" style="width:28px;height:28px;display:flex;align-items:center;justify-content:center"><svg width="16" height="16" viewBox="0 0 24 24" fill="var(--cyan)"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
    <div class="aha-brand-name" style="font-size:0.95rem">AI <span>Hero</span> Academy</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("---")

        if st.button(t("nav.my_training", lang), use_container_width=True, disabled=(active_page == "home")):
            st.switch_page("pages/03_Home.py")

        if st.button(t("nav.skills_profile", lang), use_container_width=True, disabled=(active_page == "skills_profile")):
            st.switch_page("pages/02_Skills_Profile.py")

        if has_course:
            if st.button(t("nav.my_course", lang), use_container_width=True, disabled=(active_page == "course_module")):
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
                f' color:#8990A8; margin-bottom:0.5rem">{t("nav.module_label", lang).format(n=seq)}</div>'
                f'<div style="color:#EDF0F7; line-height:1.4; margin-bottom:0.8rem">{title}</div>'
                f'<div class="module-domain-tag">{domain_display}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # ── Language toggle (only when user has a profile) ────────────────────
        if user_email:
            st.divider()
            lang_options = list(SUPPORTED_LANGS.keys())
            lang_labels = list(SUPPORTED_LANGS.values())
            current_lang = st.session_state.get("lang", "en")
            selected_idx = lang_options.index(current_lang) if current_lang in lang_options else 0
            selected_label = st.selectbox(
                t("nav.language_toggle", lang),
                options=lang_labels,
                index=selected_idx,
                key="lang_toggle",
                label_visibility="collapsed",
            )
            selected_lang = lang_options[lang_labels.index(selected_label)]
            if selected_lang != current_lang:
                st.session_state["lang"] = selected_lang
                st.session_state["_lang_from_profile"] = True
                try:
                    from utils.db import update_profile_lang
                    update_profile_lang(user_email, selected_lang)
                except Exception:
                    pass
                st.rerun()


def render_lang_sidebar(user_email: str = None, lang: str = "en") -> None:
    """
    Render a minimal sidebar with just the language toggle.
    Used on Welcome and Diagnostic pages where full nav is not needed.
    """
    from utils.i18n import t, SUPPORTED_LANGS
    with st.sidebar:
        st.markdown("""
<div style="padding:1rem 0.5rem">
  <div class="aha-brand">
    <div class="aha-brand-icon" style="width:28px;height:28px;display:flex;align-items:center;justify-content:center"><svg width="16" height="16" viewBox="0 0 24 24" fill="var(--cyan)"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
    <div class="aha-brand-name" style="font-size:0.95rem">AI <span>Hero</span> Academy</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("---")
        lang_options = list(SUPPORTED_LANGS.keys())
        lang_labels = list(SUPPORTED_LANGS.values())
        current_lang = st.session_state.get("lang", "en")
        selected_idx = lang_options.index(current_lang) if current_lang in lang_options else 0
        selected_label = st.selectbox(
            t("nav.language_toggle", lang),
            options=lang_labels,
            index=selected_idx,
            key="lang_toggle_minimal",
            label_visibility="collapsed",
        )
        selected_lang = lang_options[lang_labels.index(selected_label)]
        if selected_lang != current_lang:
            st.session_state["lang"] = selected_lang
            if user_email:
                try:
                    from utils.db import update_profile_lang
                    update_profile_lang(user_email, selected_lang)
                except Exception:
                    pass
            st.rerun()
