from typing import List, Dict
from pydantic import BaseModel


class FraudSignal(BaseModel):
    signal: str
    severity: str
    category: str


class FraudAnalysis(BaseModel):
    fraud_probability: int
    risk_level: str
    fraud_signals: List[FraudSignal]
    skill_inflation_score: int
    anomaly_score: int


class HiringRecommendation(BaseModel):
    recommendation: str
    reason: str
    confidence_score: int
    fraud_probability: int
    next_steps: List[str]
