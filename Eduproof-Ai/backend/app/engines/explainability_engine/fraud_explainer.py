from typing import Dict, List, Optional


def calculate_fraud_probability(
    identity_confidence: int,
    graph_trust: int,
    anomaly_score: int,
    evidence_gaps: int,
) -> Dict[str, object]:
    """Calculate probability of fraudulent profile."""
    
    fraud_risk_score = 100 - ((identity_confidence * 0.3) + (graph_trust * 0.3) + ((100 - anomaly_score) * 0.2) + ((100 - min(100, evidence_gaps * 5)) * 0.2))
    
    return {
        "fraud_probability": max(0, min(100, int(fraud_risk_score))),
        "risk_level": "high" if fraud_risk_score > 70 else "medium" if fraud_risk_score > 40 else "low",
    }


def explain_fraud_signals(fraud_patterns: Dict[str, object], skill_inflation: Dict[str, object]) -> List[str]:
    """Generate explanations for fraud signals detected."""
    
    explanations = []
    
    for signal in fraud_patterns.get("fraud_indicators", []):
        explanations.append(f"⚠️ {signal}")
    
    for signal in skill_inflation.get("inflation_signals", []):
        explanations.append(f"📈 {signal}")
    
    return explanations


def generate_evidence_breakdown(evidence_data: Dict[str, object]) -> Dict[str, object]:
    """Generate detailed evidence breakdown."""
    
    breakdown = {
        "verified_sources": {
            "github": evidence_data.get("github_verification", {}).get("total_repos", 0),
            "linkedin": 1 if evidence_data.get("linkedin_verification", {}).get("linkedin_url_valid") else 0,
            "projects": len(evidence_data.get("project_verification", {}).get("deployment_links_valid", [])),
            "certificates": evidence_data.get("linkedin_verification", {}).get("skills_verified", []),
        },
        "verification_summary": "Profile evidence from multiple trusted sources" if evidence_data.get("github_verification", {}).get("total_repos", 0) > 0 else "Limited external verification",
    }
    
    return breakdown
