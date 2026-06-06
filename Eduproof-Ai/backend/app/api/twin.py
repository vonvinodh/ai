from fastapi import APIRouter, Form
from typing import Optional
import json

from app.engines.digital_twin_engine.profile_builder import build_academic_profile, analyze_profile_coherence
from app.engines.digital_twin_engine.twin_generator import generate_digital_twin, link_skills_to_evidence
from app.engines.digital_twin_engine.identity_score import compute_identity_confidence_score

router = APIRouter()


@router.post("/generate")
async def generate_digital_twin(
    candidate_name: str = Form(...),
    skills_json: str = Form(...),
    projects_json: str = Form(...),
    certificates_json: str = Form(...),
    education_json: str = Form(...),
    experience_json: str = Form(...),
    evidence_json: str = Form(None),
    timeline_json: str = Form(None),
):
    """Generate complete digital academic twin."""
    
    skills = json.loads(skills_json or "[]")
    projects = json.loads(projects_json or "[]")
    certificates = json.loads(certificates_json or "[]")
    education = json.loads(education_json or "[]")
    experience = json.loads(experience_json or "[]")
    evidence = json.loads(evidence_json or "{}")
    timeline = json.loads(timeline_json or "{}")
    
    profile = build_academic_profile(candidate_name, skills, projects, certificates, education, experience)
    coherence = analyze_profile_coherence(profile)
    
    github_langs = evidence.get("github_verification", {}).get("languages", [])
    skill_links = link_skills_to_evidence(skills, github_langs, projects, certificates)
    
    twin = generate_digital_twin(f"student_{candidate_name.replace(' ', '_')}", profile, evidence, timeline)
    
    evidence_conf = evidence.get("evidence_confidence_score", 0)
    timeline_trust = timeline.get("timeline_trust_score", 70)
    skill_coverage = skill_links.get("fully_supported_skills", 0) / max(1, len(skills))
    
    identity_score = compute_identity_confidence_score(
        profile_coherence=coherence.get("profile_coherence_score", 70),
        evidence_confidence=evidence_conf,
        timeline_trust=timeline_trust,
        skill_coverage=skill_coverage,
    )
    
    return {
        "digital_twin": twin,
        "profile_analysis": {
            "completeness": profile.get("profile_completeness"),
            "coherence_score": coherence.get("profile_coherence_score"),
            "gaps": coherence.get("gaps"),
        },
        "skill_evidence_analysis": skill_links,
        "identity_confidence_score": identity_score.get("identity_confidence_score"),
    }
