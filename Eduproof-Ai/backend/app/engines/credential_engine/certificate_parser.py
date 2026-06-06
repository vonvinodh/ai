import re
from typing import Dict, Optional

DATE_REGEX = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|"
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"[ .,/-]+\d{1,2},?[ .,/-]+\d{4})\b",
    re.IGNORECASE,
)

NAME_KEYWORDS = [
    "awarded to",
    "recipient",
    "student name",
    "name",
    "this certificate is awarded to",
    "this is to certify that",
    "certified to",
]

COURSE_KEYWORDS = [
    "course",
    "program",
    "certification in",
    "for successfully completing",
    "for the completion of",
    "of the",
    "qualification in",
]

ORGANIZATION_KEYWORDS = [
    "issued by",
    "organization",
    "institution",
    "school",
    "academy",
    "university",
    "college",
    "company",
    "provider",
]

DATE_KEYWORDS = [
    "issued on",
    "issue date",
    "date of issue",
    "dated",
    "date:",
    "issued:",
    "awarded on",
    "awarded date",
]

SIGNATURE_KEYWORDS = [
    "signature",
    "signed by",
    "authorized signature",
    "authorised signature",
    "signatory",
    "signature line",
]

LOGO_KEYWORDS = [
    "logo",
    "official seal",
    "seal",
    "emblem",
    "brand",
]


def _search_field(lines: list[str], keywords: list[str]) -> Optional[str]:
    for index, line in enumerate(lines):
        normalized = line.strip()
        lowered = normalized.lower()
        for keyword in keywords:
            if keyword in lowered:
                value = normalized[lowered.find(keyword) + len(keyword) :].strip(" :\t-–")
                if value:
                    return value
                if index + 1 < len(lines):
                    candidate = lines[index + 1].strip()
                    if candidate:
                        return candidate
    return None


def _extract_date_from_text(text: str) -> Optional[str]:
    match = DATE_REGEX.search(text)
    if match:
        return match.group(0).strip()
    return None


def _extract_candidate_name(lines: list[str], text: str) -> Optional[str]:
    name = _search_field(lines, NAME_KEYWORDS)
    if name:
        return name

    pattern = re.compile(
        r"(?:recipient|awarded to|this certificate is awarded to|this is to certify that|certified to|student name|name)[:\-–]?\s*(.+)",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None


def _extract_course_name(lines: list[str], text: str) -> Optional[str]:
    course = _search_field(lines, COURSE_KEYWORDS)
    if course:
        return course

    pattern = re.compile(
        r"(?:course|program|certification in|qualification in|for the completion of|for successfully completing|of the)[:\-–]?\s*(.+)",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None


def _extract_organization(lines: list[str], text: str) -> Optional[str]:
    organization = _search_field(lines, ORGANIZATION_KEYWORDS)
    if organization:
        return organization

    pattern = re.compile(
        r"(?:issued by|organization|institution|school|academy|university|college|company|provider)[:\-–]?\s*(.+)",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None


def _extract_issue_date(lines: list[str], text: str) -> Optional[str]:
    date_value = _search_field(lines, DATE_KEYWORDS)
    if date_value:
        date_match = DATE_REGEX.search(date_value)
        if date_match:
            return date_match.group(0).strip()

    return _extract_date_from_text(text)


def parse_certificate_fields(text: str) -> Dict[str, Optional[str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "candidate_name": _extract_candidate_name(lines, text),
        "course_name": _extract_course_name(lines, text),
        "issue_date": _extract_issue_date(lines, text),
        "organization": _extract_organization(lines, text),
    }


def detect_logo(text: str, image_count: int, organization: Optional[str]) -> Dict[str, Optional[bool]]:
    lowered = text.lower()
    logo_present = image_count > 0 or any(keyword in lowered for keyword in LOGO_KEYWORDS)
    logo_match_official: Optional[bool] = None
    if logo_present and organization:
        logo_match_official = organization.strip().lower() in lowered
    return {
        "logo_present": logo_present,
        "logo_match_official": logo_match_official,
    }


def detect_signature(text: str, image_count: int) -> Dict[str, bool]:
    lowered = text.lower()
    signature_text = any(keyword in lowered for keyword in SIGNATURE_KEYWORDS)
    signature_present = signature_text or image_count > 0
    signature_suspicious = signature_present and not signature_text
    return {
        "signature_present": signature_present,
        "signature_suspicious": signature_suspicious,
    }


def extract_resume_candidate_name(resume_text: str) -> Optional[str]:
    for line in resume_text.splitlines():
        candidate = line.strip()
        if candidate and len(candidate.split()) <= 5 and re.search(r"[A-Za-z]", candidate):
            normalized = candidate.replace("Resume", "", 1).strip()
            if normalized:
                return normalized
    return None


def compute_resume_consistency(fields: Dict[str, Optional[str]], resume_text: Optional[str]) -> Optional[bool]:
    if not resume_text:
        return None

    candidate_name = fields.get("candidate_name")
    course_name = fields.get("course_name")
    lower_resume = resume_text.lower()

    if candidate_name and candidate_name.lower() in lower_resume:
        return True
    if course_name and course_name.lower() in lower_resume:
        return True

    return False
