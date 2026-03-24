# Phase 6 Kickstarter — Profile Import & Onboarding Acceleration

> Paste this entire prompt into a new Claude Code session to implement Phase 6.

---

## Mission

Add a zero-typing fast path to the Welcome page intake form. Users can upload a PDF,
Word doc, or text file (LinkedIn export, CV, job description) and have Q1 pre-populated
automatically. Manual text entry still works — this is additive, not a replacement.

Full plan: `plans/phase6-profile-import-plan.md`. Read it before starting.

**Key context:** LinkedIn OAuth was considered and rejected — standard LinkedIn API
provides only name/email, not job title or work history. File upload + existing LLM
`intake_parse` achieves the same goal with no API credentials required.

---

## Key Files to Read First

1. `plans/phase6-profile-import-plan.md` — full plan, acceptance criteria, risk table
2. `pages/00_Welcome.py` — read the full file; understand the intake form structure (~line 302)
3. `requirements.txt` — check current dependencies before adding new ones
4. `content/i18n/en.json` — find where to add the 4 new keys
5. `content/i18n/zh.json` — same

---

## Step 1 — Add `pypdf` and `python-docx` to `requirements.txt`

Read `requirements.txt` first. Add:

```
pypdf>=4.0
python-docx>=1.0
```

Verify they install cleanly:

```bash
.venv/Scripts/pip install pypdf python-docx
```

---

## Step 2 — Create `utils/doc_extract.py`

New file. Single public function:

```python
"""
utils/doc_extract.py — Extract plain text from uploaded files for intake pre-population.

Supports: .pdf (pypdf), .txt (raw decode), .docx (python-docx).
Always returns a plain string, never raises — returns "" on any failure.
Truncates to max_chars to match Welcome page Q1 limit.
"""
from __future__ import annotations

MAX_CHARS = 1000


def extract_text(file, max_chars: int = MAX_CHARS) -> str:
    """
    Extract plain text from a Streamlit UploadedFile object.

    Args:
        file: streamlit.runtime.uploaded_file_manager.UploadedFile
        max_chars: truncate output to this length (default 1000, matches Q1 max_chars)

    Returns:
        Extracted text string, truncated to max_chars. Empty string on failure.
    """
    try:
        name = getattr(file, "name", "") or ""
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""

        if ext == "txt":
            text = file.read().decode("utf-8", errors="replace")

        elif ext == "pdf":
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(file.read()))
            parts = []
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
            text = "\n".join(parts)

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

Test it locally:

```bash
.venv/Scripts/python -c "
from utils.doc_extract import extract_text
# Quick sanity — pass a fake object, expect empty string
class FakeFile:
    name = 'test.xyz'
    def read(self): return b'hello'
print(repr(extract_text(FakeFile())))  # expect ''
print('import OK')
"
```

---

## Step 3 — Update `pages/00_Welcome.py`

**Read the full file first.**

### 3a — Add import at top

```python
from utils.doc_extract import extract_text as _extract_file_text
```

### 3b — Add file uploader ABOVE the Q1 text_area block (~line 302)

Find the comment `# ── Intake form ───` and insert before the `st.text_area` call:

```python
# ── Profile import (optional fast path) ───────────────────────────────────────
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

**Important:** The `st.file_uploader` key `"welcome_import"` must be different from
all existing keys. The `st.rerun()` after a successful extract causes the page to
rerender with `welcome_q1` pre-populated in the text_area below.

### 3c — No changes needed to Q1 text_area, submit button, or LLM parse

The Q1 text area already reads from `st.session_state["welcome_q1"]` via its `key`
parameter. Pre-populating the session state key is sufficient. Everything downstream
(LLM parse, profile creation, diagnostic redirect) is unchanged.

---

## Step 4 — Add i18n keys

### `content/i18n/en.json`

Read the file, find a logical location (near other `welcome.*` keys), add:

```json
"welcome.import_label": "Import your profile (optional)",
"welcome.import_help": "Upload a PDF, Word doc, or text file — LinkedIn export, CV, or job description",
"welcome.import_extract_failed": "Could not extract text from this file — please paste your details below instead.",
"welcome.import_linkedin": "How to import from LinkedIn",
"welcome.import_step_1": "Go to your LinkedIn profile page",
"welcome.import_step_2": "Click More → Save to PDF",
"welcome.import_step_3": "Upload the downloaded PDF above"
```

### `content/i18n/zh.json`

Add Chinese equivalents. Use professional Simplified Chinese register:

```json
"welcome.import_label": "导入您的档案（可选）",
"welcome.import_help": "上传 PDF、Word 文档或文本文件 — 支持 LinkedIn 导出、简历或职位描述",
"welcome.import_extract_failed": "无法从此文件中提取文本，请在下方手动填写您的信息。",
"welcome.import_linkedin": "如何从 LinkedIn 导入",
"welcome.import_step_1": "打开您的 LinkedIn 个人主页",
"welcome.import_step_2": "点击"更多" → "保存为 PDF"",
"welcome.import_step_3": "上传下载的 PDF 文件"
```

---

## Step 5 — UAT (Group G8)

Ensure the app is running:

```bash
bash run_uat.sh
```

Reset UAT user first:

```bash
python scripts/reset_uat_user.py
```

Use Playwright MCP tools directly in main session (never sub-agents):

```python
mcp__playwright__browser_navigate(url="http://localhost:8501")
```

**G8 test group (7 checks):**

| # | Check | Method |
|---|-------|--------|
| G8.1 | File uploader widget appears above Q1 | `browser_snapshot` — find upload widget |
| G8.2 | Upload a `.txt` file → Q1 pre-populated | Create temp txt file, `browser_file_upload`, check Q1 |
| G8.3 | Upload a PDF → Q1 pre-populated | Use any small PDF |
| G8.4 | Q1 text editable after upload | `browser_type` into Q1 after upload |
| G8.5 | LinkedIn "How to import" expander shows 3 steps | Click expander, `browser_snapshot` |
| G8.6 | Manual entry (no upload) → full flow completes | Skip upload, type Q1, submit |
| G8.7 | No console errors | `browser_console_messages` |

Create a temp test file for G8.2:

```bash
python -c "
with open('tmp_test_profile.txt', 'w') as f:
    f.write('Senior Underwriter at Export Development Canada. I assess counterparty creditworthiness for credit insurance policies, structure coverage terms, and manage client relationships with Canadian exporters.')
"
```

---

## Done When

- `utils/doc_extract.py` exists and handles pdf/txt/docx
- `pypdf` and `python-docx` in `requirements.txt`
- File uploader appears on Welcome page above Q1
- Upload pre-populates Q1 session state and reruns
- LinkedIn expander shows 3-step instructions
- 7 i18n keys added to en.json and zh.json
- G8 UAT 7/7 pass
- `pytest` still passing (no regressions)

---

## Key Constraints

- `extract_text()` MUST never raise — always return string (empty on failure)
- `st.rerun()` is the correct Streamlit pattern to refresh after session state write
- Do NOT change the LLM `intake_parse` prompt or downstream flow — only Q1 pre-population changes
- File uploader key must not conflict with existing session state keys
- All Playwright MCP calls in main session — never delegate to sub-agents
- `/compact` after Step 2 (before touching 00_Welcome.py)
