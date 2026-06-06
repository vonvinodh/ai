from typing import Dict, List, Optional


def build_academic_profile(
    candidate_name: str,
    skills: List[str],
    projects: List[Dict[str, str]],
    certificates: List[Dict[str, str]],
    education: List[Dict[str, str]],
    experience: List[Dict[str, str]],
) -> Dict[str, object]:
    """Build comprehensive academic profile."""
    
    profile = {
        "candidate_name": candidate_name,
        "profile_completeness": 0,
        "sections": {
            "skills": {
                "count": len(skills),
                "items": skills,
                "verified": 0,
            },
            "projects": {
                "count": len(projects),
                "items": projects,
                "verified": 0,
            },
            "certificates": {
                "count": len(certificates),
                "items": certificates,
                "verified": 0,
            },
            "education": {
                "count": len(education),
                "items": education,
            },
            "experience": {
                "count": len(experience),
                "items": experience,
            },
        },
    }
    
    total_items = len(skills) + len(projects) + len(certificates) + len(education) + len(experience)
    profile["profile_completeness"] = min(100, (total_items / 15) * 100)
    
    return profile


def analyze_profile_coherence(profile: Dict[str, object]) -> Dict[str, object]:
    """Analyze coherence of profile elements."""
    
    coherence_score = 70
    gaps = []
    
    sections = profile.get("sections", {})
    
    if sections.get("skills", {}).get("count", 0) == 0:
        gaps.append("No skills listed")
        coherence_score -= 15
    
    if sections.get("projects", {}).get("count", 0) == 0:
        gaps.append("No projects to support skills")
        coherence_score -= 10
    
    if sections.get("certificates", {}).get("count", 0) == 0:
        gaps.append("No certifications or credentials")
        coherence_score -= 5
    
    if sections.get("experience", {}).get("count", 0) == 0 and sections.get("education", {}).get("count", 0) > 0:
        gaps.append("Education but no work experience")
        coherence_score -= 5
    
    return {
        "profile_coherence_score": max(0, min(100, coherence_score)),
        "gaps": gaps,
    }
