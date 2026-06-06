from typing import Dict, List


def generate_score_explanations(
    components: Dict[str, int],
    threshold: int = 50,
) -> Dict[str, List[str]]:
    """Generate detailed explanations for score components."""
    
    explanations = {
        "strengths": [],
        "weaknesses": [],
        "recommendations": [],
    }
    
    if components.get("profile_coherence", 0) >= threshold:
        explanations["strengths"].append("✓ Profile shows good internal consistency")
    else:
        explanations["weaknesses"].append("✗ Profile lacks coherence - gaps detected")
        explanations["recommendations"].append("Add missing sections (projects, certificates)")
    
    if components.get("evidence_confidence", 0) >= threshold:
        explanations["strengths"].append("✓ Multiple sources verify claimed skills")
    else:
        explanations["weaknesses"].append("✗ Limited external verification available")
        explanations["recommendations"].append("Link GitHub, LinkedIn, or deployment links")
    
    if components.get("timeline_trust", 0) >= threshold:
        explanations["strengths"].append("✓ Timeline is consistent and realistic")
    else:
        explanations["weaknesses"].append("✗ Timeline contains inconsistencies")
        explanations["recommendations"].append("Review and correct date discrepancies")
    
    return explanations
