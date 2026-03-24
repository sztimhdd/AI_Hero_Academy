# Phase 6 — Profile Import & Onboarding Acceleration

> Status: **PLANNED** — ready to start after Phase 5 UAT passes (now cleared)
> Last updated: 2026-03-24 (rev 2 — LinkedIn URL via Gemini Search Grounding + BYOW placeholders)

---

## Context & What's Already Done

**Phase 5 complete (2026-03-24):** BYOW diagnostic live. Intake parse extracts 6 fields
from free-text input. 9/9 G7 UAT checks pass. Any role, any JD → valid 7-module path.

**The problem Phase 6 solves:**
Phase 5 works, but the intake step still requires the user to type or paste a paragraph
about their role. For someone with a LinkedIn profile open, this is unnecessary friction.
Phase 6 adds zero-typing fast paths and removes the blank-page anxiety on the diagnostic.

---

## LinkedIn API Reality Check (confirmed 2025)

Standard LinkedIn OAuth (`openid profile email`) returns **name + email + photo only**.
Full profile data (positions, skills, industry) requires LinkedIn partner-tier API access.
Not viable for a ~100-user internal corporate tool.

**What actually works instead:**

Brave search and Gemini's **Google Search grounding** both retrieve the same public
LinkedIn snippet that search engines index — headline, company, and ~150 chars of About.
That's enough to populate `role_text`, `org_type`, `industry`, `seniority`, and seed
`magic_wish`. Tested live: `site:linkedin.com/in/haihu` returned:

> *"Senior Enterprise Architect @ Export Development Canada | Leading Generative AI
> Initiatives | designing Canada's first Generative AI Governance Model..."*

Gemini Search Grounding is the **cleanest implementation path** — it uses the
`GEMINI_API_KEY` already configured in the app, no additional credentials required.

---

## What Phase 6 Builds

### Three import paths — user picks the fastest

```
Option A (paste URL):   LinkedIn URL → Gemini Search Grounding → Q1 pre-populated
Option B (upload file): PDF / DOCX / TXT → text extraction → Q1 pre-populated
Option C (manual):      Type directly — unchanged from Phase 5 (always available)
```

All three produce the same `intake_profile` shape via the existing `intake_parse` LLM call.

### BYOW diagnostic placeholders

Each of the 6 BYOW diagnostic questions gets an example placeholder that models
the depth of answer expected — removes blank-page anxiety without leading the user.

---

## Implementation Tasks

### 6.1 — LinkedIn URL import (primary fast path)

**Where:** `pages/00_Welcome.py`, above the Q1 text area.

```python
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
        st.rerun()
    else:
        st.warning(t("welcome.li_import_failed", _lang))
```

**New helper function** in `pages/00_Welcome.py` (or `utils/linkedin_import.py`):

```python
def _fetch_linkedin_via_gemini(url: str) -> str:
    """
    Use Gemini with Google Search Grounding to retrieve public LinkedIn profile data.
    Returns a plain-text summary suitable for the Q1 intake text area.
    Returns "" on any failure — never raises.
    """
    try:
        from google import genai
        from google.genai import types as genai_types

        client = genai.Client()
        prompt = (
            f"Find the professional profile at: {url}\n"
            "Return a plain text summary (3-5 sentences) covering: "
            "current job title, employer, industry, key responsibilities, "
            "and any notable AI or technology focus. "
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
        return response.text.strip()[:1000]
    except Exception:
        return ""
```

**Why Gemini Search Grounding over direct Brave API call:**
- No additional API key — reuses existing `GEMINI_API_KEY`
- Gemini formats the extracted data as clean prose, ready for `intake_parse`
- Same underlying data source (Google's index of LinkedIn public profiles)
- Graceful — if Grounding can't find the profile, returns empty string and falls through to manual entry

---

### 6.2 — File upload (secondary fast path)

Add `st.file_uploader` below the LinkedIn URL field. Accepted: `.pdf`, `.txt`, `.docx`.

```python
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
        st.rerun()
    else:
        st.warning(t("welcome.import_extract_failed", _lang))
```

---

### 6.3 — Text extraction utility (`utils/doc_extract.py`)

New file. Handles `.pdf` (pypdf), `.txt` (raw decode), `.docx` (python-docx).
Always returns string, never raises. Truncates to 1000 chars.

**New dependencies** (add to `requirements.txt`):
- `pypdf>=4.0`
- `python-docx>=1.0`

---

### 6.4 — LinkedIn "How to import PDF" helper expander

Below the file uploader. Static text, zero engineering risk:

```
▶ Prefer to import from LinkedIn? (3 steps)
   1. Go to your LinkedIn profile page
   2. Click More → Save to PDF
   3. Upload the PDF using the button above
```

---

### 6.5 — BYOW diagnostic placeholders (`content/diagnostic_prompts.json`)

Add `placeholder_text` and `placeholder_text_zh` to each of the 6 prompts.
These render as greyed example text in the `st.text_area` — disappear when user types.
Each placeholder models the depth and format of a good answer without leading the user.

```json
[
  {
    "item_id": "byow_responsible_ai_1",
    "domain_id": "responsible_ai",
    "sequence": 1,
    "prompt_text": "...",
    "placeholder_text": "e.g. Last month I needed to summarise a client's financial profile for a proposal. I wasn't sure which AI tool was approved for that data, so I checked our tool policy first and used Copilot within M365 rather than a public chatbot — the client details never left our environment.",
    "placeholder_text_zh": "例如：上个月我需要为提案总结一位客户的财务状况。我不确定哪款AI工具可用于此类数据，于是先查阅了我们的工具使用政策，选择在M365中使用Copilot而非公共聊天工具，确保客户信息不离开我们的系统。"
  },
  {
    "item_id": "byow_strategic_prompting_1",
    "domain_id": "strategic_prompting",
    "sequence": 2,
    "prompt_text": "...",
    "placeholder_text": "e.g. I write weekly status reports. I'd type: 'Summarise these 5 bullet points into a 3-paragraph executive update for a non-technical audience. Lead with the most important risk. Keep it under 200 words and use plain language.' Then I review the draft and adjust the tone.",
    "placeholder_text_zh": "例如：我每周都要撰写状态报告。我会输入："将以下5个要点总结为面向非技术受众的3段执行摘要，以最重要的风险开头，不超过200字，使用简明语言。"然后审阅草稿并调整语气。"
  },
  {
    "item_id": "byow_critical_eval_1",
    "domain_id": "critical_eval",
    "sequence": 3,
    "prompt_text": "...",
    "placeholder_text": "e.g. I'd cross-check every specific number or fact against the source document, search online for any claims I can't immediately verify, and flag anything uncertain for a colleague to review before the report goes out. I never submit AI-generated text about a client without a second set of eyes.",
    "placeholder_text_zh": "例如：我会对照原始文档逐一核查每个具体数字或事实，在线搜索无法立即确认的说法，并将所有不确定内容标记出来请同事审查，再提交报告。涉及客户的AI生成内容，我从不独自定稿。"
  },
  {
    "item_id": "byow_data_decision_1",
    "domain_id": "data_decision",
    "sequence": 4,
    "prompt_text": "...",
    "placeholder_text": "e.g. I had 12 vendor responses to compare for a procurement decision. I'd paste the key evaluation criteria and ask AI to score each vendor against them, flag missing information, and produce a comparison table. Then I'd verify the top 3 manually before writing my recommendation.",
    "placeholder_text_zh": "例如：我曾需要比较12份供应商回复以支持采购决策。我会粘贴关键评估标准，让AI对每家供应商打分、标记缺失信息并生成对比表格，再手动核实前3名后撰写建议报告。"
  },
  {
    "item_id": "byow_relationship_intel_1",
    "domain_id": "relationship_intel",
    "sequence": 5,
    "prompt_text": "...",
    "placeholder_text": "e.g. Before a quarterly review with a major client, I'd ask AI to summarise their recent news and any industry developments that might affect them, generate 3 questions they're likely to raise about our service, and draft talking points I could adapt. I'd review everything before the call.",
    "placeholder_text_zh": "例如：在与重要客户进行季度回顾前，我会让AI总结他们的近期动态及可能影响他们的行业变化，列出他们可能提出的3个问题，并起草我可以调整的发言要点，然后在会议前审阅所有内容。"
  },
  {
    "item_id": "byow_augmented_comm_1",
    "domain_id": "augmented_comm",
    "sequence": 6,
    "prompt_text": "...",
    "placeholder_text": "e.g. I write briefing notes for senior leadership. I'd draft the key points myself, then ask AI to restructure it into executive summary format, tighten the language, and flag anything that sounds too technical. I always do a final read to make sure the tone matches our audience.",
    "placeholder_text_zh": "例如：我负责为高层领导撰写简报。我会先自己整理要点，再让AI将其重组为执行摘要格式、精简语言并标记过于技术性的表述。最后我会通读一遍，确保语气符合受众预期。"
  }
]
```

**In `pages/01_Diagnostic.py`**, update the `st.text_area` call to use the placeholder:

```python
val = st.text_area(
    prompt["prompt_text"] if _lang == "en" else prompt.get("prompt_text_zh", prompt["prompt_text"]),
    placeholder=prompt.get(f"placeholder_text{'_zh' if _lang == 'zh' else ''}", ""),
    key=f"byow_{prompt['item_id']}",
    max_chars=500,
    help="Aim for 3–5 sentences.",
)
```

---

### 6.6 — i18n keys

Add to `content/i18n/en.json` and `content/i18n/zh.json`:

```json
"welcome.li_url_label":      "Import from LinkedIn (paste your profile URL)",
"welcome.li_import_btn":     "Import →",
"welcome.li_spinner":        "Looking up your profile...",
"welcome.li_import_failed":  "Couldn't retrieve profile — please paste your details below instead.",
"welcome.import_label":      "Or upload a file (PDF, Word, or text)",
"welcome.import_help":       "LinkedIn export, CV, resume, or job description",
"welcome.import_extract_failed": "Could not extract text — please paste your details below instead.",
"welcome.import_linkedin":   "How to import from LinkedIn as PDF",
"welcome.import_step_1":     "Go to your LinkedIn profile page",
"welcome.import_step_2":     "Click More → Save to PDF",
"welcome.import_step_3":     "Upload the PDF using the button above"
```

---

### 6.7 — UAT (Group G8)

| # | Check | Grader | Pass Criterion |
|---|-------|--------|----------------|
| G8.1 | LinkedIn URL field + Import button renders | snapshot | Text input + button visible above Q1 |
| G8.2 | Paste LinkedIn URL → Q1 pre-populated | snapshot | Q1 filled with profile summary after ~3s |
| G8.3 | File uploader renders below URL field | snapshot | Upload widget visible |
| G8.4 | Upload a TXT file → Q1 pre-populated | snapshot | Q1 filled with extracted content |
| G8.5 | Q1 editable after import before submitting | manual | Edit text → submit → parsed correctly |
| G8.6 | LinkedIn PDF expander shows 3 steps | snapshot | Expander with 3 steps visible |
| G8.7 | BYOW placeholders visible on diagnostic page | snapshot | Grey example text in all 6 text areas |
| G8.8 | Placeholders disappear when user types | manual | Click into field → type → placeholder gone |
| G8.9 | Manual entry (no import) still works — regression | manual | Skip import, type Q1, submit → same flow |
| G8.10 | No console errors throughout | code | `browser_console_messages` clean |

---

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | LinkedIn URL → Gemini Search Grounding → Q1 pre-populated | 🔜 |
| 2 | File upload (pdf/txt/docx) → text extraction → Q1 pre-populated | 🔜 |
| 3 | Q1 pre-populated text is editable before submit | 🔜 |
| 4 | LinkedIn PDF export expander visible with 3-step instructions | 🔜 |
| 5 | All 6 BYOW prompts have `placeholder_text` in en + zh | 🔜 |
| 6 | Placeholders render in `st.text_area` on diagnostic page | 🔜 |
| 7 | Manual text entry unchanged — regression pass | 🔜 |
| 8 | `pypdf` and `python-docx` added to `requirements.txt` | 🔜 |
| 9 | i18n keys added to en.json and zh.json | 🔜 |
| 10 | G8 UAT 10/10 pass | 🔜 |

---

## New Files

- `utils/doc_extract.py` — text extraction from pdf/txt/docx
- `utils/linkedin_import.py` (optional) — `_fetch_linkedin_via_gemini()` helper

## Modified Files

- `pages/00_Welcome.py` — LinkedIn URL field + file uploader + helper expander
- `pages/01_Diagnostic.py` — add `placeholder` param to `st.text_area` calls
- `content/diagnostic_prompts.json` — add `placeholder_text` + `placeholder_text_zh` to all 6 prompts
- `requirements.txt` — add `pypdf`, `python-docx`
- `content/i18n/en.json` — 10 new keys
- `content/i18n/zh.json` — 10 new keys (ZH translations)

## Non-Goals for Phase 6

- LinkedIn OAuth / API integration (standard scopes provide name only)
- LinkedIn as authentication mechanism (GCP IAP handles auth)
- Full CV structured parsing (LLM handles field extraction from raw text)
- Multi-file upload

---

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Gemini Search Grounding returns empty for private LinkedIn profiles | Medium | `if not _li_text: st.warning(...)` fallback to manual entry |
| Google Search Grounding not available in all Gemini deployment configs | Low | Try/except — falls back silently; file upload still available |
| `pypdf` can't extract text from scanned/image PDFs | Medium | Graceful fallback message; never block submission |
| LinkedIn changes public profile snippet content visible to Google | Low | LLM extraction is format-agnostic |
