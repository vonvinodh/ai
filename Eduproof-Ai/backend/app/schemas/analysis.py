from typing import List, Optional

from pydantic import BaseModel


class AIDetection(BaseModel):
    ai_generated: bool
    template_generated: bool
    ai_keyword_count: int
    template_phrase_count: int
    generic_pattern_count: int


class BuzzwordAnalysis(BaseModel):
    buzzword_count: int
    excessive: bool
    matches: List[str]


class AchievementValidation(BaseModel):
    unrealistic_claims: bool
    flags: List[str]


class SimilarityAnalysis(BaseModel):
    portfolio_text_similarity: Optional[float]
    github_similarity: Optional[float]
    project_plagiarism: bool
    project_plagiarism_reasons: List[str]


class ContentAnalysisResult(BaseModel):
    ai_detection: AIDetection
    buzzword_analysis: BuzzwordAnalysis
    achievement_validation: AchievementValidation
    similarity: SimilarityAnalysis
    content_authenticity_score: int
