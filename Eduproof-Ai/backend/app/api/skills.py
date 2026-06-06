from fastapi import APIRouter, Form
from typing import Optional

from app.engines.skill_engine.mcq_generator import generate_mcqs
from app.engines.skill_engine.coding_generator import generate_coding_challenges
from app.engines.skill_engine.viva_generator import generate_viva_questions
from app.engines.skill_engine.skill_score import calculate_skill_confidence_score, AdaptiveDifficultySystem

router = APIRouter()


@router.post("/verify")
async def verify_skill(
    skill: str = Form(...),
    mcq_score: Optional[int] = Form(None),
    coding_score: Optional[int] = Form(None),
    viva_score: Optional[int] = Form(None),
    github_evidence: Optional[bool] = Form(False),
):
    """Verify skill through MCQs, coding challenges, and viva questions."""
    mcq_questions = generate_mcqs(skill, difficulty="mixed", count=3)
    coding_challenges = generate_coding_challenges(skill, difficulty="easy", count=2)
    viva_questions = generate_viva_questions(skill, count=3)
    
    confidence_result = calculate_skill_confidence_score(
        mcq_score=mcq_score,
        coding_score=coding_score,
        viva_score=viva_score,
        github_evidence=github_evidence,
    )
    
    return {
        "skill": skill,
        "mcq_questions": mcq_questions,
        "coding_challenges": coding_challenges,
        "viva_questions": viva_questions,
        "skill_authenticity_score": confidence_result["skill_authenticity_score"],
        "tests_completed": confidence_result["tests_completed"],
    }


@router.get("/adaptive-difficulty/{current_difficulty}/{performance_score}")
async def adjust_difficulty(current_difficulty: str, performance_score: int):
    """Adjust difficulty based on performance."""
    system = AdaptiveDifficultySystem(current_difficulty)
    new_difficulty = system.adjust_difficulty(performance_score)
    
    return {
        "current_difficulty": current_difficulty,
        "performance_score": performance_score,
        "new_difficulty": new_difficulty,
        "recommendation": f"Move to {new_difficulty} level",
    }
