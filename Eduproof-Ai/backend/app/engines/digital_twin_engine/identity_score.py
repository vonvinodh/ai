from typing import Dict, Optional


def compute_identity_confidence_score(
    profile_coherence: int,
    evidence_confidence: int,
    timeline_trust: int,
    skill_coverage: float,
) -> Dict[str, object]:
    """Compute overall identity confidence score."""
    
    score = (profile_coherence * 0.25) + (evidence_confidence * 0.3) + (timeline_trust * 0.25) + (skill_coverage * 100 * 0.2)
    
    return {
        "identity_confidence_score": int(min(100, score)),
        "components": {
            "profile_coherence": profile_coherence,
            "evidence_confidence": evidence_confidence,
            "timeline_trust": timeline_trust,
            "skill_coverage_percent": skill_coverage * 100,
        },
    }
