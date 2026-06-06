from typing import Dict, Optional, List

from app.engines.content_engine.achievement_validator import validate_achievements
from app.engines.content_engine.ai_detector import detect_ai_and_template
from app.engines.content_engine.similarity_checker import compare_portfolio_similarity

BUZZWORDS = [
    "innovative",
    "scalable",
    "dynamic",
    "ai-powered",
    "cutting-edge",
    "synergy",
    "growth-driven",
]


def detect_buzzwords(text: str) -> Dict[str, object]:
    lowered = text.lower()
    matches: List[str] = []

    for buzzword in BUZZWORDS:
        if buzzword in lowered:
            matches.append(buzzword)

    return {
        "buzzword_count": len(matches),
        "excessive": len(matches) >= 3,
        "matches": matches,
    }


def compute_content_authenticity_score(analysis: Dict[str, object]) -> int:
    score = 60
    ai = analysis["ai_detection"]
    buzzword = analysis["buzzword_analysis"]
    achievement = analysis["achievement_validation"]
    similarity = analysis["similarity"]

    if ai["ai_generated"]:
        score -= 25
    if ai["template_generated"]:
        score -= 15

    score -= min(15, buzzword["buzzword_count"] * 4)

    if achievement["unrealistic_claims"]:
        score -= 20

    github_similarity = similarity.get("github_similarity")
    portfolio_similarity = similarity.get("portfolio_text_similarity")
    if github_similarity is not None and github_similarity >= 0.4:
        score += 5
    if portfolio_similarity is not None and portfolio_similarity >= 0.6:
        score += 5

    if similarity.get("project_plagiarism"):
        score -= 25

    return max(0, min(100, score))


def analyze_resume_content(text: str, github_url: Optional[str] = None, portfolio_text: Optional[str] = None) -> Dict[str, object]:
    ai_detection = detect_ai_and_template(text)
    buzzword_analysis = detect_buzzwords(text)
    achievement_validation = validate_achievements(text)
    similarity = compare_portfolio_similarity(text, portfolio_text, github_url)

    score = compute_content_authenticity_score({
        "ai_detection": ai_detection,
        "buzzword_analysis": buzzword_analysis,
        "achievement_validation": achievement_validation,
        "similarity": similarity,
    })

    return {
        "ai_detection": ai_detection,
        "buzzword_analysis": buzzword_analysis,
        "achievement_validation": achievement_validation,
        "similarity": similarity,
        "content_authenticity_score": score,
    }
