import re
from typing import Dict, Optional

from pypdf import PdfReader

PDF_DATE_RE = re.compile(r"^D:(\d{4})(\d{2})?(\d{2})?(\d{2})?(\d{2})?(\d{2})?")


def _parse_pdf_date(raw_date: Optional[str]) -> Optional[str]:
    if not raw_date:
        return None

    value = raw_date.strip()
    if value.startswith("D:"):
        value = value[2:]

    value = re.sub(r"[^0-9]", "", value)
    if len(value) < 8:
        return None

    year = value[0:4]
    month = value[4:6]
    day = value[6:8]
    hour = value[8:10] if len(value) >= 10 else "00"
    minute = value[10:12] if len(value) >= 12 else "00"
    second = value[12:14] if len(value) >= 14 else "00"

    return f"{year}-{month}-{day} {hour}:{minute}:{second}"


def extract_pdf_metadata(file_path: str) -> Dict[str, Optional[str]]:
    reader = PdfReader(file_path)
    raw_metadata = reader.metadata or {}

    creation_date = raw_metadata.get("/CreationDate") or raw_metadata.get("CreationDate")
    modification_date = raw_metadata.get("/ModDate") or raw_metadata.get("/ModificationDate")
    author = raw_metadata.get("/Author") or raw_metadata.get("Author")

    return {
        "creation_date": _parse_pdf_date(creation_date),
        "modification_date": _parse_pdf_date(modification_date),
        "author": author.strip() if isinstance(author, str) and author.strip() else None,
    }
