from typing import Dict, Optional


def verify_linkedin_claims(linkedin_url: str, claimed_skills: list[str], claimed_education: dict, claimed_experience: dict) -> Dict[str, object]:
    """
    Simulate LinkedIn verification. In production, this would use LinkedIn API.
    Returns confidence scores based on URL validity and pattern matching.
    """
    if not linkedin_url:
        return {
            "linkedin_url_valid": False,
            "skills_verified": [],
            "education_verified": False,
            "experience_verified": False,
            "overall_confidence": 0,
        }

    linkedin_valid = "linkedin.com/in/" in linkedin_url.lower()

    return {
        "linkedin_url_valid": linkedin_valid,
        "skills_verified": claimed_skills if linkedin_valid else [],
        "education_verified": bool(claimed_education and linkedin_valid),
        "experience_verified": bool(claimed_experience and linkedin_valid),
        "overall_confidence": 40 if linkedin_valid else 0,
    }
