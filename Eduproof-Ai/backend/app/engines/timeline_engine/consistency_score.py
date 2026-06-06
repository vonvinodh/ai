from typing import Dict, Optional


def compute_timeline_trust_score(
    academic_timeline: list = None,
    experience_timeline: list = None,
    certificate_timeline: list = None,
    contradictions: Dict[str, object] = None,
    skill_gaps: Dict[str, object] = None,
    inconsistencies: Dict[str, object] = None,
) -> int:
    """Compute overall timeline trust score (0-100)."""
    score = 70
    
    if not academic_timeline:
        academic_timeline = []
    if not experience_timeline:
        experience_timeline = []
    if not certificate_timeline:
        certificate_timeline = []
    if not contradictions:
        contradictions = {}
    if not skill_gaps:
        skill_gaps = {}
    if not inconsistencies:
        inconsistencies = {}
    
    if academic_timeline:
        score += 10
    if experience_timeline:
        score += 10
    if certificate_timeline:
        score += 10
    
    if contradictions.get("overlaps_detected"):
        score -= 20
    
    if skill_gaps.get("gaps_detected"):
        gap_count = len(skill_gaps.get("gaps", []))
        score -= min(15, gap_count * 3)
    
    if inconsistencies.get("inconsistencies_detected"):
        score -= 15
    
    return max(0, min(100, score))
