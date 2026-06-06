from typing import Optional

from pydantic import BaseModel


class CertificateFields(BaseModel):
    candidate_name: Optional[str] = None
    course_name: Optional[str] = None
    issue_date: Optional[str] = None
    organization: Optional[str] = None


class CertificateMetadata(BaseModel):
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    author: Optional[str] = None


class CertificateVerificationFactors(BaseModel):
    logo_present: bool
    logo_match_official: Optional[bool] = None
    signature_present: bool
    signature_suspicious: bool
    metadata_valid: bool
    resume_consistency: Optional[bool] = None


class CertificateVerificationResult(BaseModel):
    filename: str
    fields: CertificateFields
    metadata: CertificateMetadata
    factors: CertificateVerificationFactors
    score: int
    details: dict
