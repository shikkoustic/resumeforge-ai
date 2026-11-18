"""Getting resume text in, whether it arrives as a PDF or as pasted text."""
from __future__ import annotations

import io

from pypdf import PdfReader

MAX_PAGES = 5


class ResumeReadError(RuntimeError):
    pass


def pdf_to_text(file_bytes: bytes) -> str:
    """Extract plain text from an uploaded resume PDF.

    Raises ResumeReadError with a message meant for the user, because a scanned
    (image-only) resume is a real case and the app should say so rather than silently
    sending an empty string to the model.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
    except Exception as exc:  # pypdf raises several different errors
        raise ResumeReadError(f"That file could not be opened as a PDF ({exc}).") from exc

    if reader.is_encrypted:
        raise ResumeReadError(
            "That PDF is password protected. Please upload an unlocked copy, or paste the "
            "text instead."
        )

    pages = reader.pages[:MAX_PAGES]
    text = "\n".join((page.extract_text() or "") for page in pages).strip()

    if not text:
        raise ResumeReadError(
            "No text could be read from that PDF. It is most likely a scan or an image. "
            "Please paste the resume text instead."
        )
    return text
