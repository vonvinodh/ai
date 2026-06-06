from fastapi import APIRouter, Form
from typing import Optional
import json

from app.engines.trust_graph_engine.graph_builder import build_trust_graph
from app.engines.trust_graph_engine.graph_score import detect_fraud_patterns, detect_skill_inflation, compute_graph_trust_score
from app.engines.explainability_engine.fraud_explainer import calculate_fraud_probability, explain_fraud_signals, generate_evidence_breakdown
from app.engines.explainability_engine.reason_generator import generate_score_explanations
from app.engines.explainability_engine.recommendation_engine import generate_hiring_recommendation

router = APIRouter()


@router.post("/analyze")
async def analyze_fraud_risk(
    candidate_name: str = Form(...),
    skills_json: str = Form(...),
    projects_json: str = Form(...),
    certificates_json: str = Form(...),
    evidence_json: str = Form(None),
    timeline_json: str = Form(None),
    experience_years: float = Form(0),
):
    """Comprehensive fraud risk analysis."""
    
    skills = json.loads(skills_json or "[]")
    projects = json.loads(projects_json or "[]")
    certificates = json.loads(certificates_json or "[]")
    evidence = json.loads(evidence_json or "{}")
    timeline = json.loads(timeline_json or "{}")
    
    # Build trust graph
    graph = build_trust_graph(candidate_name, skills, projects, certificates, evidence)
    
    # Extract evidence gaps
    evidence_gaps = []
    if evidence.get("github_verification", {}).get("total_repos", 0) == 0:
        evidence_gaps.append("No GitHub projects found")
    
    # Detect patterns
    fraud_patterns = detect_fraud_patterns(graph, evidence_gaps, timeline.get("overlaps", []))
    graph_trust = compute_graph_trust_score(graph, fraud_patterns, {"inflation_score": 0, "fraud_signals": []})
    
    # Skill inflation
    skill_evidence = {}
    for skill in skills:
        skill_evidence[skill] = {"confidence": 50}
    
    skill_inflation = detect_skill_inflation(skill_evidence, experience_years)
    
    # Fraud probability
    fraud_prob = calculate_fraud_probability(
        identity_confidence=70,
        graph_trust=graph_trust,
        anomaly_score=fraud_patterns.get("anomaly_score", 0),
        evidence_gaps=len(evidence_gaps),
    )
    
    explanations = explain_fraud_signals(fraud_patterns, skill_inflation)
    evidence_breakdown = generate_evidence_breakdown(evidence)
    
    reason_explanations = generate_score_explanations({
        "profile_coherence": 70,
        "evidence_confidence": evidence.get("evidence_confidence_score", 0),
        "timeline_trust": timeline.get("timeline_trust_score", 70),
    })
    
    recommendation = generate_hiring_recommendation(
        fraud_probability=fraud_prob.get("fraud_probability", 0),
        identity_confidence=70,
        evidence_verified=len([s for s in skills if skill_evidence.get(s, {}).get("confidence", 0) > 50]),
    )
    
    return {
        "candidate_name": candidate_name,
        "fraud_risk": fraud_prob,
        "fraud_signals": explanations,
        "evidence_breakdown": evidence_breakdown,
        "reasoning": reason_explanations,
        "hiring_recommendation": recommendation,
        "trust_graph": {
            "total_nodes": graph.get("total_nodes"),
            "total_edges": graph.get("total_edges"),
        },
    }
