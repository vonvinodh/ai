from fastapi import APIRouter, Form
from typing import List, Optional

from app.engines.evidence_engine.evidence_score import compute_evidence_confidence_score
from app.engines.evidence_engine.skill_mapper import map_skills_to_github
from app.services.github_service import fetch_github_repos, calculate_github_contributions
from app.services.linkedin_service import verify_linkedin_claims
from app.services.research_service import verify_research_claims
from app.services.hackathon_service import verify_hackathon_claims
from app.services.project_verification_service import verify_project_claims

router = APIRouter()


@router.post("/verify")
async def verify_evidence(
    github_url: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    claimed_skills: Optional[str] = Form(None),
    claimed_papers: Optional[str] = Form(None),
    scholar_profile: Optional[str] = Form(None),
    claimed_hackathons: Optional[str] = Form(None),
    claimed_awards: Optional[str] = Form(None),
    deployment_links: Optional[str] = Form(None),
    github_project_links: Optional[str] = Form(None),
):
    """Comprehensive evidence verification across multiple sources."""

    github_repos = fetch_github_repos(github_url) if github_url else None
    github_verification = calculate_github_contributions(github_repos)
    languages = github_verification.get("languages", [])

    claimed_skills_list = [s.strip() for s in claimed_skills.split(",") if s.strip()] if claimed_skills else []
    skill_mapping = map_skills_to_github(claimed_skills_list, languages)

    education = {}
    experience = {}
    linkedin_verification = verify_linkedin_claims(linkedin_url, claimed_skills_list, education, experience)

    claimed_papers_list = [p.strip() for p in claimed_papers.split(",") if p.strip()] if claimed_papers else []
    research_verification = verify_research_claims(claimed_papers_list, None, scholar_profile)

    hackathons_list = [h.strip() for h in claimed_hackathons.split(",") if h.strip()] if claimed_hackathons else []
    awards_list = [a.strip() for a in claimed_awards.split(",") if a.strip()] if claimed_awards else []
    hackathon_verification = verify_hackathon_claims(hackathons_list, awards_list)

    deployment_list = [d.strip() for d in deployment_links.split(",") if d.strip()] if deployment_links else []
    github_links_list = [g.strip() for g in github_project_links.split(",") if g.strip()] if github_project_links else []
    project_verification = verify_project_claims(deployment_list, github_links_list)

    evidence_data = {
        "github_verification": github_verification,
        "skill_mapping": skill_mapping,
        "linkedin_verification": linkedin_verification,
        "research_verification": research_verification,
        "hackathon_verification": hackathon_verification,
        "project_verification": project_verification,
    }

    confidence_result = compute_evidence_confidence_score(evidence_data)

    return {
        "github_verification": github_verification,
        "skill_mapping": skill_mapping,
        "linkedin_verification": linkedin_verification,
        "research_verification": research_verification,
        "hackathon_verification": hackathon_verification,
        "project_verification": project_verification,
        "evidence_confidence_score": confidence_result["confidence_score"],
        "verified_components": confidence_result["verified_components"],
    }
