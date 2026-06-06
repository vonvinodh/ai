from typing import List, Optional
from pydantic import BaseModel


class TimelineEntry(BaseModel):
    date: str
    event: str
    year: int
    month: int


class AcademicTimeline(BaseModel):
    entries: List[TimelineEntry]
    duration_years: Optional[int]


class ExperienceTimeline(BaseModel):
    entries: List[TimelineEntry]
    total_experience_years: Optional[int]


class CertificateTimeline(BaseModel):
    entries: List[TimelineEntry]
    certificate_count: int


class TimelineConsistencyResult(BaseModel):
    academic_timeline: AcademicTimeline
    experience_timeline: ExperienceTimeline
    certificate_timeline: CertificateTimeline
    contradictions_detected: bool
    skill_gaps_detected: bool
    inconsistencies_detected: bool
    timeline_trust_score: int
