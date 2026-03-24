# Phase 6 — Profile Import & Onboarding Acceleration

> Status: **PLANNED** — ready to start after Phase 5 UAT passes (now cleared)
> Last updated: 2026-03-24

---

## Context & What's Already Done

**Phase 5 complete (2026-03-24):** BYOW diagnostic live. Intake parse extracts 6 fields
from free-text input. 9/9 G7 UAT checks pass. Any role, any JD → valid 7-module path.

**The problem Phase 6 solves:**
Phase 5 works, but the intake step still requires the user to type or paste a paragraph
about their role. For someone with a CV or LinkedIn profile already open, this is
unnecessary friction. Phase 6 adds a zero-typing fast path.

---

## LinkedIn API Reality Check

**Original plan:** LinkedIn OAuth login → pre-populate intake_profile from profile data.

**What LinkedIn standard OAuth actually provides** (confirmed 2025):

| Scope | Data available |
|-------|---------------|
| `openid profile email` | name, email, profile photo, locale |
| `r_liteprofile` (deprecated) | same as above |
| Full positions/skills/industry | **Requires LinkedIn partner-tier API access** — not available to standard apps |

**Implication:** LinkedIn OAuth in standard form cannot pre-populate `role_text`,
`daily_tasks`, `industry`, or `org_type` — the fields that actually drive intake quality.
It can only pre-fill the display name. Not worth the OAuth infrastructure for that alone.

**Additional note:** The app uses GCP Identity-Aware Proxy for identity
(`GCP_USER_EMAIL`). LinkedIn as an authentication mechanism is redundant for a
corporate internal GCP app. Employees authenticate via Google; LinkedIn is a data source.

**Decision:** Reframe Phase 6 from "LinkedIn OAuth login" to
**"Profile Import — any source, zero typing."**

---

## What Phase 6 Builds

### The Fast Path

Replace the "paste text here" Q1 experience with a structured import flow:

```
Option A (one click):   Upload a file → LLM extracts → Q1 pre-populated
Option B (copy-paste):  Paste any document text → same extraction
Option C (manual):      Type directly — unchanged from Phase 5 (always available)
```

The user picks whichever is fastest for them. All three produce the same
`intake_profile` shape. No API credentials required.

**Supported import sources (all handled identically by the LLM extractor):**
- LinkedIn profile → Save to PDF → upload
- CV / resume (any format)
- Job description (copied from job board, email, intranet)
- Email signature + role description
- Plain text (Phase 5 fallback, still works)

---

## Implementation Tasks

### 6.1 — File upload in `pages/00_Welcome.py`

Add `st.file_uploader` above the Q1 text area. Accepted: `.pdf`, `.txt`, `.docx`.

```python
uploaded = st.file_uploader(
    t("welcome.import_label", _lang),
    type=["pdf", "txt", "docx"],
    help=t("welcome.import_help", _lang),
    key="welcome_import",
)
if uploaded:
    extracted_text = _extract_text(uploaded)
    st.session_state["welcome_q1"] = extracted_text[:1000]
    st.rerun()
```

When a file is uploaded, extract its text, write it into the Q1 session state key,
and rerun. The Q1 text area renders with the pre-populated content. User can edit
before submitting. Same LLM parse flow as Phase 5 — nothing downstream changes.

### 6.2 — Text extraction (`utils/doc_extract.py`)

New utility module. Thin wrappers around standard libraries:

```python
def extract_text(file: UploadedFile) -> str:
    """Extract plain text from pdf, txt, or docx upload. Max 1000 chars returned."""
```

| Format | Library | Notes |
|--------|---------|-------|
| `.txt` | built-in `read().decode()` | trivial |
| `.pdf` | `pypdf` (already in many Streamlit projects) | extract all page text |
| `.docx` | `python-docx` | extract paragraph text |

Output is truncated to 1000 chars (matches Q1 `max_chars`). No new LLM call —
the existing Phase 5 `intake_parse` LLM call handles all extraction.

**New dependencies** (add to `requirements.txt`):
- `pypdf>=4.0` — PDF text extraction
- `python-docx>=1.0` — Word doc text extraction

### 6.3 — LinkedIn "How to import" helper

No OAuth. No API credentials. A collapsible expander beneath the file uploader:

```
▶ How to import from LinkedIn (3 steps)
   1. Go to your LinkedIn profile page
   2. Click "More" → "Save to PDF"
   3. Upload the downloaded PDF above
```

This is a pure UX addition — one `st.expander` block with static text + an icon.
Zero engineering risk, immediate user value.

### 6.4 — i18n keys

Add to `content/i18n/en.json` and `content/i18n/zh.json`:

```json
"welcome.import_label":    "Import your profile (optional)",
"welcome.import_help":     "Upload a PDF, Word doc, or text file — LinkedIn export, CV, or job description",
"welcome.import_linkedin": "How to import from LinkedIn",
"welcome.import_step_1":   "Go to your LinkedIn profile",
"welcome.import_step_2":   "Click More → Save to PDF",
"welcome.import_step_3":   "Upload the PDF above"
```

### 6.5 — UAT (Group G8)

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| G8.1 | File uploader renders above Q1 | snapshot | Upload widget visible |
| G8.2 | Upload a TXT file → Q1 pre-populated | snapshot | Q1 text area filled with extracted content |
| G8.3 | Upload a PDF (LinkedIn export) → Q1 pre-populated | snapshot | Q1 filled, no error |
| G8.4 | User can edit Q1 after import before submitting | manual | Edit text → submit → parsed correctly |
| G8.5 | LinkedIn "How to import" expander renders | snapshot | Expander with 3 steps visible |
| G8.6 | Manual entry (no upload) still works — regression | manual | Skip upload, type Q1, submit → same flow |
| G8.7 | No console errors throughout | code | `browser_console_messages` clean |

---

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | File uploader accepts pdf/txt/docx, extracts text, pre-populates Q1 | 🔜 |
| 2 | Q1 pre-populated text is editable before submit | 🔜 |
| 3 | LinkedIn PDF export → valid intake_profile (role_text, industry populated) | 🔜 |
| 4 | LinkedIn "How to import" expander visible with 3-step instructions | 🔜 |
| 5 | Manual text entry (no upload) unchanged — regression pass | 🔜 |
| 6 | `pypdf` and `python-docx` added to `requirements.txt` | 🔜 |
| 7 | 4 i18n keys added to en.json and zh.json | 🔜 |
| 8 | G8 UAT 7/7 pass | 🔜 |

---

## New Files

- `utils/doc_extract.py` — text extraction from pdf/txt/docx

## Modified Files

- `pages/00_Welcome.py` — file uploader + LinkedIn helper expander
- `requirements.txt` — add `pypdf`, `python-docx`
- `content/i18n/en.json` — 4 new keys
- `content/i18n/zh.json` — 4 new keys (ZH translations)

## Non-Goals for Phase 6

- LinkedIn OAuth / API integration (standard API provides no useful profile data without partner access)
- LinkedIn as authentication mechanism (GCP IAP handles auth for corporate users)
- CV parsing beyond plain text extraction (no structured parsing, no field inference — LLM handles that)
- Multi-file upload (single file only)

---

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| `pypdf` can't extract text from scanned/image PDFs | Medium | Graceful fallback: show "Could not extract text — please paste manually"; never block submission |
| Uploaded file too large → slow extraction | Low | `max_upload_size` Streamlit config; truncate at 1000 chars before LLM call |
| `.docx` with complex formatting produces garbled text | Low | Paragraph-only extraction (no tables, headers); acceptable for CVs and LinkedIn exports |
| LinkedIn PDF export format changes | Low | LLM extraction is format-agnostic; no structured parsing |

---

## Why Not LinkedIn OAuth?

Documented here for future reference. LinkedIn partner-tier API (which unlocks
positions, skills, and work history) requires:

1. Applying for LinkedIn Marketing Developer Platform access
2. Agreeing to LinkedIn's partnership terms
3. Building and maintaining an OAuth flow

For an internal corporate tool with ~100 EDC users, this overhead is not justified
when a PDF upload achieves the same outcome in a single afternoon of engineering.

If EDC later scales to external users or LinkedIn offers richer standard API access,
the OAuth path remains viable — Phase 6's import infrastructure (text → LLM extract)
is identical regardless of how the text arrives.
