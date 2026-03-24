# Phase 6 Kickstarter — Profile Import & Onboarding Acceleration

> Paste this entire prompt into a new Claude Code session to implement Phase 6.

---

## Mission

Two things in one sprint:

1. **Zero-typing intake fast paths** — Users can paste a LinkedIn URL or upload a file
   (CV, PDF, DOCX) and have the Q1 intake field pre-populated automatically.
2. **BYOW diagnostic placeholders** — Each of the 6 open-ended diagnostic questions
   gets an example placeholder that shows users the expected depth of answer, removing
   blank-page anxiety.

Full plan: `plans/phase6-profile-import-plan.md`. Read it before starting.

**Key context:**
- LinkedIn OAuth rejected — standard API provides name only, not job title or experience.
- Primary fast path: LinkedIn URL → Gemini with Google Search Grounding → Q1 pre-populated.
  No extra API key needed — reuses the `GEMINI_API_KEY` already configured.
- Secondary fast path: file upload (PDF/DOCX/TXT) → text extraction → Q1 pre-populated.
- Placeholders are already written in `content/diagnostic_prompts.json` — just wire them
  into the `st.text_area` calls in `pages/01_Diagnostic.py`.

---

## Key Files to Read First

1. `plans/phase6-profile-import-plan.md` — full plan, all code snippets, acceptance criteria
2. `pages/00_Welcome.py` — full read; understand intake form structure (~line 302)
3. `pages/01_Diagnostic.py` — find the `st.text_area` calls in the BYOW loop
4. `content/diagnostic_prompts.json` — placeholders already added; read the schema
5. `requirements.txt` — check current deps before adding new ones
6. `content/i18n/en.json` — find where to insert the 10 new keys

---

## Step 1 — Wire BYOW placeholders into `pages/01_Diagnostic.py`

**Easiest step — do this first, verify it works, then move on.**

Read `pages/01_Diagnostic.py`. Find the loop that renders `st.text_area` for each prompt
(search for `byow_prompts`). The `diagnostic_prompts.json` file already has
`placeholder_text` and `placeholder_text_zh` fields. Update the `st.text_area` call:

```python
val = st.text_area(
    prompt["prompt_text"] if _lang == "en" else prompt.get("prompt_text_zh", prompt["prompt_text"]),
    placeholder=prompt.get(f"placeholder_text{'_zh' if _lang == 'zh' else ''}", ""),
    key=f"byow_{prompt['item_id']}",
    max_chars=500,
    help=t("diag.char_hint", _lang),   # add this i18n key: "Aim for 3–5 sentences."
)
```

Add `"diag.char_hint"` to `content/i18n/en.json` and `content/i18n/zh.json`:
```json
"diag.char_hint": "Aim for 3–5 sentences."
"diag.char_hint": "建议写3至5句话。"
```

Verify by running the app and checking that grey placeholder text appears in each question.

**→ /compact after Step 1**

---

## Step 2 — LinkedIn URL import (`pages/00_Welcome.py`)

**Read the full `pages/00_Welcome.py` first.**

### 2a — Add the Gemini Search Grounding helper

Add this function near the top of `pages/00_Welcome.py` (after imports):

```python
def _fetch_linkedin_via_gemini(url: str) -> str:
    """
    Retrieve public LinkedIn profile data using Gemini with Google Search Grounding.
    Returns plain text (name, title, company, responsibilities) for Q1 pre-population.
    Returns "" on any failure — never raises.
    """
    try:
        from google import genai
        from google.genai import types as genai_types

        client = genai.Client()
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
        return (response.text or "").strip()[:1000]
    except Exception:
        return ""
```

### 2b — Add LinkedIn URL field above Q1 text area

Find the `# ── Intake form ───` comment (~line 302). Insert BEFORE the `st.text_area`:

```python
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
        st.rerun()
    else:
        st.warning(t("welcome.li_import_failed", _lang))
```

### 2c — No other changes to Q1 or downstream flow

Q1 text area already reads from `st.session_state["welcome_q1"]` via its `key`.
Pre-populating session state + `st.rerun()` is sufficient.

---

## Step 3 — File upload (`pages/00_Welcome.py`)

### 3a — Add `pypdf` and `python-docx` to `requirements.txt`

```
pypdf>=4.0
python-docx>=1.0
```

Install locally:
```bash
.venv/Scripts/pip install pypdf python-docx
```

### 3b — Create `utils/doc_extract.py`

```python
"""
utils/doc_extract.py — Extract plain text from uploaded files for intake pre-population.
Supports .pdf (pypdf), .txt (raw decode), .docx (python-docx).
Always returns str, never raises. Truncates to max_chars.
"""
from __future__ import annotations

MAX_CHARS = 1000


def extract_text(file, max_chars: int = MAX_CHARS) -> str:
    try:
        name = getattr(file, "name", "") or ""
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""

        if ext == "txt":
            text = file.read().decode("utf-8", errors="replace")

        elif ext == "pdf":
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(file.read()))
            text = "\n".join(p.extract_text() or "" for p in reader.pages)

        elif ext == "docx":
            from docx import Document
            import io
            doc = Document(io.BytesIO(file.read()))
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

        else:
            return ""

        return text.strip()[:max_chars]
    except Exception:
        return ""
```

Quick sanity test:
```bash
.venv/Scripts/python -c "
from utils.doc_extract import extract_text
class F:
    name='x.xyz'
    def read(self): return b''
print(repr(extract_text(F())))  # expect ''
print('OK')
"
```

### 3c — Add file uploader below the LinkedIn URL field

```python
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
        st.rerun()
    else:
        st.warning(t("welcome.import_extract_failed", _lang))

with st.expander(t("welcome.import_linkedin", _lang), expanded=False):
    st.markdown(
        f"1. {t('welcome.import_step_1', _lang)}  \n"
        f"2. {t('welcome.import_step_2', _lang)}  \n"
        f"3. {t('welcome.import_step_3', _lang)}"
    )
```

**→ /compact after Step 3**

---

## Step 4 — Add i18n keys

Read `content/i18n/en.json`. Find the `welcome.*` block. Add all 10 new keys:

### `en.json`
```json
"welcome.li_url_label":          "Import from LinkedIn (paste your profile URL)",
"welcome.li_import_btn":         "Import →",
"welcome.li_spinner":            "Looking up your profile...",
"welcome.li_import_failed":      "Couldn't retrieve profile — please paste your details below instead.",
"welcome.import_or":             "or upload a file",
"welcome.import_label":          "Upload a file (PDF, Word, or text)",
"welcome.import_help":           "LinkedIn export, CV, resume, or job description",
"welcome.import_extract_failed": "Could not extract text — please paste your details below instead.",
"welcome.import_linkedin":       "How to import from LinkedIn as PDF (3 steps)",
"welcome.import_step_1":         "Go to your LinkedIn profile page",
"welcome.import_step_2":         "Click More → Save to PDF",
"welcome.import_step_3":         "Upload the PDF using the button above"
```

### `zh.json`
```json
"welcome.li_url_label":          "从 LinkedIn 导入（粘贴您的主页链接）",
"welcome.li_import_btn":         "导入 →",
"welcome.li_spinner":            "正在查询您的档案…",
"welcome.li_import_failed":      "无法获取档案，请在下方手动填写您的信息。",
"welcome.import_or":             "或上传文件",
"welcome.import_label":          "上传文件（PDF、Word 或文本）",
"welcome.import_help":           "支持 LinkedIn 导出文件、简历或职位描述",
"welcome.import_extract_failed": "无法从此文件提取文本，请在下方手动填写。",
"welcome.import_linkedin":       "如何从 LinkedIn 导出 PDF（3 步）",
"welcome.import_step_1":         "打开您的 LinkedIn 个人主页",
"welcome.import_step_2":         "点击"更多" → "保存为 PDF"",
"welcome.import_step_3":         "使用上方按钮上传 PDF 文件"
```

---

## Step 5 — UAT (Group G8, 10 checks)

```bash
python scripts/reset_uat_user.py
bash run_uat.sh
```

Playwright MCP in main session only (never sub-agents):

```python
mcp__playwright__browser_navigate(url="http://localhost:8501")
```

| # | Check | Method |
|---|-------|--------|
| G8.1 | LinkedIn URL field + Import button visible | `browser_snapshot` |
| G8.2 | Paste LinkedIn URL → Q1 pre-populated after spinner | Paste `https://www.linkedin.com/in/haihu/`, click Import |
| G8.3 | File uploader visible below URL field | `browser_snapshot` |
| G8.4 | Upload `.txt` → Q1 pre-populated | `browser_file_upload` with temp txt |
| G8.5 | Q1 editable after any import | `browser_type` into Q1, check value changes |
| G8.6 | LinkedIn PDF expander shows 3 steps | Click expander, `browser_snapshot` |
| G8.7 | BYOW diagnostic: placeholder text visible in all 6 fields | Navigate to diagnostic, `browser_snapshot` |
| G8.8 | Typing into a BYOW field removes placeholder | `browser_type` into field 1, check placeholder gone |
| G8.9 | Manual entry (no import) → full flow completes | Skip import, type Q1, complete diagnostic |
| G8.10 | No console errors throughout | `browser_console_messages` |

Create temp test file for G8.4:
```bash
python -c "
with open('tmp_test_profile.txt', 'w') as f:
    f.write('Senior Underwriter at Export Development Canada. I assess counterparty creditworthiness, structure credit insurance coverage, and manage client relationships with Canadian exporters across emerging markets.')
"
```

---

## Done When

- BYOW placeholder text renders in all 6 diagnostic questions (en + zh)
- LinkedIn URL → Gemini Search Grounding → Q1 pre-populated
- File upload (pdf/txt/docx) → text extraction → Q1 pre-populated
- LinkedIn PDF expander shows 3-step instructions
- `pypdf` + `python-docx` in `requirements.txt`
- 10 i18n keys + `diag.char_hint` in en.json + zh.json
- `pytest` all passing
- G8 UAT 10/10 pass

---

## Key Constraints

- `extract_text()` and `_fetch_linkedin_via_gemini()` MUST never raise — empty string on failure
- `st.rerun()` is the correct Streamlit pattern after `st.session_state` write
- Do NOT change `intake_parse` LLM prompt or anything downstream — only Q1 pre-population
- Gemini Search Grounding uses existing `GEMINI_API_KEY` — no new env vars
- All Playwright MCP calls in main session — never delegate to sub-agents
- `/compact` after Step 1 and after Step 3
