from typing import Dict, Optional


def compute_evidence_confidence_score(evidence_data: Dict[str, object]) -> int:
    """
    Compute overall evidence confidence from all verification sources.
    """
    score = 30
    components = []

    github_data = evidence_data.get("github_verification", {})
    if github_data.get("total_repos", 0) > 0:
        score += 15
        components.append("github_repos")
    if github_data.get("total_stars", 0) > 0:
        score += 10
        components.append("github_stars")

    skills_data = evidence_data.get("skill_mapping", {})
    skill_conf = skills_data.get("skill_confidence", 0)
    score += int(skill_conf * 20)
    if skill_conf > 0:
        components.append("skill_mapping")

    linkedin_data = evidence_data.get("linkedin_verification", {})
    if linkedin_data.get("linkedin_url_valid"):
        score += 10
        if linkedin_data.get("skills_verified"):
            score += 5
        components.append("linkedin")

    research_data = evidence_data.get("research_verification", {})
    if research_data.get("google_scholar_verified"):
        score += 10
        components.append("research")

    hackathon_data = evidence_data.get("hackathon_verification", {})
    if hackathon_data.get("hackathons_verified"):
        score += 10
        components.append("hackathons")
    if hackathon_data.get("awards_verified"):
        score += 10
        components.append("awards")

    project_data = evidence_data.get("project_verification", {})
    if project_data.get("deployment_links_valid"):
        score += 10
        components.append("deployment")
    if project_data.get("github_links_valid"):
        score += 10
        components.append("source_code")

    return {
        "confidence_score": min(100, score),
        "verified_components": components,
        "evidence_count": len(components),
    }
