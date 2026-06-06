from typing import Dict, Optional

from app.engines.credential_engine.certificate_parser import (
    compute_resume_consistency,
    detect_logo,
    detect_signature,
    parse_certificate_fields,
)
from app.engines.credential_engine.metadata_checker import extract_pdf_metadata
from app.services.pdf_service import extract_pdf_image_count


def compute_certificate_authenticity_score(
    fields: Dict[str, Optional[str]],
    metadata: Dict[str, Optional[str]],
    logo_info: Dict[str, Optional[bool]],
    signature_info: Dict[str, bool],
    resume_consistency: Optional[bool],
) -> int:
    score = 30

    if fields.get("candidate_name"):
        score += 10
    if fields.get("course_name"):
        score += 5
    if fields.get("issue_date"):
        score += 5
    if fields.get("organization"):
        score += 5

    if metadata.get("creation_date"):
        score += 5
    if metadata.get("modification_date"):
        score += 5
    if metadata.get("author"):
        score += 5

    if logo_info.get("logo_present"):
        score += 10
    if logo_info.get("logo_match_official"):
        score += 10

    if signature_info.get("signature_present"):
        score += 10
    if not signature_info.get("signature_suspicious"):
        score += 5

    if resume_consistency is True:
        score += 15
    elif resume_consistency is False:
        score -= 10

    return max(0, min(score, 100))


def analyze_certificate(file_path: str, extracted_text: str, resume_text: Optional[str] = None) -> Dict[str, object]:
    fields = parse_certificate_fields(extracted_text)
    image_count = extract_pdf_image_count(file_path)
    logo_info = detect_logo(extracted_text, image_count, fields.get("organization"))
    signature_info = detect_signature(extracted_text, image_count)
    resume_consistency = compute_resume_consistency(fields, resume_text)
    metadata = extract_pdf_metadata(file_path)
    metadata_valid = bool(metadata.get("creation_date") and metadata.get("modification_date"))
    score = compute_certificate_authenticity_score(fields, metadata, logo_info, signature_info, resume_consistency)

    return {
        "fields": fields,
        "metadata": metadata,
        "factors": {
            "logo_present": logo_info["logo_present"],
            "logo_match_official": logo_info.get("logo_match_official"),
            "signature_present": signature_info["signature_present"],
            "signature_suspicious": signature_info["signature_suspicious"],
            "metadata_valid": metadata_valid,
            "resume_consistency": resume_consistency,
        },
        "score": score,
        "details": {
            "image_count": image_count,
            "extracted_text_length": len(extracted_text or ""),
            "resume_text_provided": bool(resume_text),
        },
    }
