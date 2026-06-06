from difflib import SequenceMatcher
import re
from typing import Dict, Optional

from app.services.github_service import fetch_github_repo_descriptions


def _similarity_ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0

    a_norm = re.sub(r"\s+", " ", a.strip().lower())
    b_norm = re.sub(r"\s+", " ", b.strip().lower())
    return SequenceMatcher(None, a_norm, b_norm).ratio()


def compare_portfolio_similarity(resume_text: str, portfolio_text: Optional[str], github_url: Optional[str]) -> Dict[str, object]:
    result: Dict[str, object] = {
        "portfolio_text_similarity": None,
        "github_similarity": None,
        "project_plagiarism": False,
        "project_plagiarism_reasons": [],
    }

    if portfolio_text:
        result["portfolio_text_similarity"] = _similarity_ratio(resume_text, portfolio_text)

    if github_url:
        github_text = fetch_github_repo_descriptions(github_url)
        if github_text:
            ratio = _similarity_ratio(resume_text, github_text)
            result["github_similarity"] = ratio
            if ratio >= 0.4:
                result["project_plagiarism"] = True
                result["project_plagiarism_reasons"].append(
                    "Resume appears closely matched to GitHub repo names/descriptions"
                )

    if portfolio_text and result.get("portfolio_text_similarity") is not None and result["portfolio_text_similarity"] >= 0.6:
        result["project_plagiarism"] = True
        result["project_plagiarism_reasons"].append(
            "Resume content is highly similar to existing portfolio text"
        )

    return result
