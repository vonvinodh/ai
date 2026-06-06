from typing import Dict, List, Optional


def generate_digital_twin(
    candidate_id: str,
    profile: Dict[str, object],
    evidence_data: Dict[str, object],
    timeline_data: Dict[str, object],
) -> Dict[str, object]:
    """Generate complete digital academic twin."""
    
    twin = {
        "candidate_id": candidate_id,
        "candidate_name": profile.get("candidate_name"),
        "profile": profile,
        "evidence_summary": {
            "github_repos": evidence_data.get("github_verification", {}).get("total_repos", 0),
            "skill_mappings": len(evidence_data.get("skill_mapping", {}).get("mapped_skills", [])),
            "verified_projects": len(evidence_data.get("project_verification", {}).get("deployment_links_valid", [])),
            "hackathon_participations": len(evidence_data.get("hackathon_verification", {}).get("hackathons_verified", [])),
        },
        "timeline_summary": {
            "academic_events": timeline_data.get("academic_events", 0),
            "experience_events": timeline_data.get("experience_events", 0),
            "certificate_events": timeline_data.get("certificate_events", 0),
        },
        "twin_completeness": 0,
    }
    
    profile_complete = profile.get("profile_completeness", 0)
    evidence_count = sum(twin["evidence_summary"].values())
    timeline_count = sum(twin["timeline_summary"].values())
    
    twin["twin_completeness"] = int((profile_complete * 0.4) + (min(100, evidence_count * 10) * 0.3) + (min(100, timeline_count * 10) * 0.3))
    
    return twin


def link_skills_to_evidence(
    skills: List[str],
    github_languages: List[str],
    projects: List[Dict[str, str]],
    certificates: List[Dict[str, str]],
) -> Dict[str, object]:
    """Link each skill to supporting evidence."""
    
    skill_evidence_map = {}
    
    for skill in skills:
        skill_lower = skill.lower()
        evidence = {
            "skill": skill,
            "github_evidence": [],
            "projects": [],
            "certificates": [],
            "confidence": 0,
        }
        
        for lang in github_languages:
            if skill_lower in lang.lower() or lang.lower() in skill_lower:
                evidence["github_evidence"].append(lang)
        
        for project in projects:
            proj_str = str(project).lower()
            if skill_lower in proj_str:
                evidence["projects"].append(project)
        
        for cert in certificates:
            cert_str = str(cert).lower()
            if skill_lower in cert_str:
                evidence["certificates"].append(cert)
        
        total_evidence = len(evidence["github_evidence"]) + len(evidence["projects"]) + len(evidence["certificates"])
        evidence["confidence"] = min(100, total_evidence * 25)
        
        skill_evidence_map[skill] = evidence
    
    return {
        "skill_evidence_links": skill_evidence_map,
        "fully_supported_skills": len([s for s in skill_evidence_map.values() if s["confidence"] > 50]),
        "total_skills": len(skills),
    }
