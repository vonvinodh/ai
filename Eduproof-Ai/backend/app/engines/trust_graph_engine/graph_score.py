from typing import Dict, List


def detect_fraud_patterns(
    graph_data: Dict[str, object],
    evidence_gaps: List[str],
    timeline_contradictions: List[str],
) -> Dict[str, object]:
    """Detect suspicious patterns in academic graph."""
    
    fraud_signals = []
    anomaly_score = 0
    
    # Check for isolated skill nodes (skills with no project/certificate support)
    skill_nodes = [n for n in graph_data.get("nodes", []) if n.get("type") == "skill"]
    for skill in skill_nodes:
        connected_edges = [e for e in graph_data.get("edges", []) if e.get("target") == skill["id"] or e.get("source") == skill["id"]]
        if len(connected_edges) == 1:  # Only connection to student
            fraud_signals.append(f"Unsupported skill: {skill.get('label')}")
            anomaly_score += 10
    
    # Check for certificate without project or experience
    cert_nodes = [n for n in graph_data.get("nodes", []) if n.get("type") == "certificate"]
    if len(cert_nodes) > 5 and len([n for n in graph_data.get("nodes", []) if n.get("type") == "project"]) == 0:
        fraud_signals.append("Multiple certificates but no projects")
        anomaly_score += 15
    
    # Evidence gaps
    for gap in (evidence_gaps or []):
        fraud_signals.append(f"Missing evidence: {gap}")
        anomaly_score += 5
    
    # Timeline contradictions
    for contradiction in (timeline_contradictions or []):
        fraud_signals.append(f"Timeline issue: {contradiction}")
        anomaly_score += 10
    
    return {
        "fraud_signals_detected": len(fraud_signals),
        "anomaly_score": min(100, anomaly_score),
        "fraud_indicators": fraud_signals,
        "fraud_risk": "high" if anomaly_score > 40 else "medium" if anomaly_score > 20 else "low",
    }


def detect_skill_inflation(
    skill_evidence_map: Dict[str, object],
    experience_years: float,
) -> Dict[str, object]:
    """Detect exaggerated or inflated skill claims."""
    
    inflation_signals = []
    inflation_score = 0
    
    unsupported_skills = [
        skill for skill, data in skill_evidence_map.items()
        if data.get("confidence", 0) == 0
    ]
    
    if unsupported_skills:
        inflation_signals.append(f"Completely unsupported skills: {len(unsupported_skills)}")
        inflation_score += 20
    
    # High claims with low experience
    if experience_years < 2:
        high_level_skills = sum(1 for skill in skill_evidence_map.keys() if "expert" in skill.lower() or "advanced" in skill.lower())
        if high_level_skills > 3:
            inflation_signals.append("Advanced claims with insufficient experience")
            inflation_score += 25
    
    return {
        "skill_inflation_detected": len(inflation_signals) > 0,
        "inflation_score": min(100, inflation_score),
        "inflation_signals": inflation_signals,
    }


def compute_graph_trust_score(
    graph_data: Dict[str, object],
    fraud_patterns: Dict[str, object],
    skill_inflation: Dict[str, object],
) -> int:
    """Compute overall graph-based trust score."""
    
    score = 80
    
    # Graph structure impact
    total_nodes = graph_data.get("total_nodes", 0)
    total_edges = graph_data.get("total_edges", 0)
    
    if total_nodes < 5:
        score -= 15
    if total_edges < 4:
        score -= 10
    
    # Fraud pattern impact
    score -= fraud_patterns.get("anomaly_score", 0)
    
    # Skill inflation impact
    score -= skill_inflation.get("inflation_score", 0)
    
    return max(0, min(100, score))
