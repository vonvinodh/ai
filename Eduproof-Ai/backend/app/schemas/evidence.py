from typing import List, Optional

from pydantic import BaseModel


class GitHubVerification(BaseModel):
    total_repos: int
    total_stars: int
    total_forks: int
    primary_language: Optional[str]
    languages: List[str]


class SkillMapping(BaseModel):
    claimed_skills: List[str]
    github_evidence: List[str]
    mapped_skills: List[str]
    unverified_skills: List[str]
    skill_confidence: float


class LinkedInVerification(BaseModel):
    linkedin_url_valid: bool
    skills_verified: List[str]
    education_verified: bool
    experience_verified: bool
    overall_confidence: int


class ResearchVerification(BaseModel):
    google_scholar_verified: bool
    researchgate_verified: bool
    papers_found: List[str]
    citation_count: int
    overall_confidence: int


class HackathonVerification(BaseModel):
    hackathons_verified: List[str]
    awards_verified: List[str]
    participation_confidence: int
    award_confidence: int


class ProjectVerification(BaseModel):
    deployment_links_valid: List[str]
    github_links_valid: List[str]
    deployment_confidence: int
    source_code_confidence: int


class EvidenceVerificationResult(BaseModel):
    github_verification: GitHubVerification
    skill_mapping: SkillMapping
    linkedin_verification: LinkedInVerification
    research_verification: ResearchVerification
    hackathon_verification: HackathonVerification
    project_verification: ProjectVerification
    overall_evidence_confidence: int
