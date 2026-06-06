from typing import List, Dict, Optional
from pydantic import BaseModel


class AcademicProfile(BaseModel):
    candidate_name: str
    profile_completeness: int
    skill_count: int
    project_count: int
    certificate_count: int


class DigitalTwin(BaseModel):
    candidate_id: str
    candidate_name: str
    profile: AcademicProfile
    github_repos: int
    verified_skills: int
    twin_completeness: int


class SkillEvidence(BaseModel):
    skill: str
    github_evidence: List[str]
    projects: List[str]
    certificates: List[str]
    confidence: int
