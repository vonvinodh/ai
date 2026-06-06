from fastapi import APIRouter, Form
from typing import Optional

from app.engines.timeline_engine.timeline_builder import (
    build_academic_timeline,
    build_experience_timeline,
    build_certificate_timeline,
)
from app.engines.timeline_engine.contradiction_detector import (
    detect_overlapping_experiences,
    detect_skill_evolution_gaps,
    detect_timeline_inconsistencies,
)
from app.engines.timeline_engine.consistency_score import compute_timeline_trust_score

router = APIRouter()


@router.post("/verify")
async def verify_timeline_consistency(
    education_json: Optional[str] = Form(None),
    experience_json: Optional[str] = Form(None),
    certificates_json: Optional[str] = Form(None),
    claimed_skills: Optional[str] = Form(None),
):
    """Verify timeline consistency across education, experience, and certificates."""
    import json
    
    try:
        education_list = json.loads(education_json or "[]")
        experience_list = json.loads(experience_json or "[]")
        certificates_list = json.loads(certificates_json or "[]")
        skills_list = [s.strip() for s in (claimed_skills or "").split(",") if s.strip()]
    except json.JSONDecodeError as e:
        return {
            "error": f"Invalid JSON in request: {str(e)}",
            "academic_events": 0,
            "experience_events": 0,
            "certificate_events": 0,
            "overlaps_detected": False,
            "skill_gaps_detected": False,
            "inconsistencies_detected": False,
            "timeline_trust_score": 0,
            "gaps": [],
            "overlaps": [],
        }
    
    try:
        academic_timeline = build_academic_timeline(education_list)
        experience_timeline = build_experience_timeline(experience_list)
        certificate_timeline = build_certificate_timeline(certificates_list)
        combined_timeline = sorted(academic_timeline + experience_timeline + certificate_timeline, key=lambda x: x["date"])
        
        contradictions = detect_overlapping_experiences(experience_timeline)
        skill_gaps = detect_skill_evolution_gaps(skills_list, combined_timeline)
        inconsistencies = detect_timeline_inconsistencies(combined_timeline)
        
        trust_score = compute_timeline_trust_score(
            academic_timeline,
            experience_timeline,
            certificate_timeline,
            contradictions,
            skill_gaps,
            inconsistencies,
        )
        
        return {
            "academic_events": len(academic_timeline),
            "experience_events": len(experience_timeline),
            "certificate_events": len(certificate_timeline),
            "overlaps_detected": contradictions.get("overlaps_detected"),
            "skill_gaps_detected": skill_gaps.get("gaps_detected"),
            "inconsistencies_detected": inconsistencies.get("inconsistencies_detected"),
            "timeline_trust_score": trust_score,
            "gaps": skill_gaps.get("gaps", []),
            "overlaps": contradictions.get("overlaps", []),
        }
    except Exception as e:
        return {
            "error": f"Error processing timeline data: {str(e)}",
            "academic_events": 0,
            "experience_events": 0,
            "certificate_events": 0,
            "overlaps_detected": False,
            "skill_gaps_detected": False,
            "inconsistencies_detected": False,
            "timeline_trust_score": 0,
            "gaps": [],
            "overlaps": [],
        }
