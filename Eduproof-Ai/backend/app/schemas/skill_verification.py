from typing import List, Dict, Optional
from pydantic import BaseModel


class MCQQuestion(BaseModel):
    question: str
    options: List[str]
    correct: int
    difficulty: str


class CodingChallenge(BaseModel):
    title: str
    description: str
    difficulty: str
    test_cases: Optional[List[Dict[str, object]]]


class SkillTestResult(BaseModel):
    skill: str
    mcq_score: Optional[int]
    coding_score: Optional[int]
    viva_score: Optional[int]
    skill_authenticity_score: int
    tests_completed: int
    github_verified: bool
