"""
utils/doc_extract.py — Extract plain text from uploaded files for Q1 intake pre-population.
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
