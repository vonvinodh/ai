from typing import Dict


def generate_hiring_recommendation(
    fraud_probability: int,
    identity_confidence: int,
    evidence_verified: int,
) -> Dict[str, object]:
    """Generate hiring recommendation based on trust analysis."""
    
    if fraud_probability > 70:
        recommendation = "REJECT"
        reason = "High fraud probability detected. Profile shows multiple red flags."
    elif fraud_probability > 40:
        recommendation = "REVIEW"
        reason = "Medium fraud risk. Manual review recommended before proceeding."
    elif identity_confidence < 40:
        recommendation = "REVIEW"
        reason = "Insufficient evidence to verify claims. Additional information needed."
    else:
        recommendation = "SHORTLIST"
        reason = f"Candidate appears genuine with {identity_confidence}% confidence. Recommended for next round."
    
    return {
        "recommendation": recommendation,
        "reason": reason,
        "confidence_score": identity_confidence,
        "fraud_probability": fraud_probability,
        "next_steps": _get_next_steps(recommendation),
    }


def _get_next_steps(recommendation: str) -> list:
    """Get recommended next steps based on recommendation."""
    if recommendation == "SHORTLIST":
        return ["Schedule technical interview", "Review portfolio projects", "Reach out to candidate"]
    elif recommendation == "REVIEW":
        return ["Request additional certifications", "Verify GitHub profile", "Contact references"]
    else:
        return ["Archive application", "Update rejection reason", "Optionally provide feedback"]
