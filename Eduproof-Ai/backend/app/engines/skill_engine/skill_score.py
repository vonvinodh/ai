from typing import Dict, Optional


def calculate_skill_confidence_score(
    mcq_score: Optional[int] = None,
    coding_score: Optional[int] = None,
    viva_score: Optional[int] = None,
    github_evidence: Optional[bool] = None,
) -> Dict[str, object]:
    """Calculate overall skill authenticity score."""
    score = 20
    completed_tests = 0
    
    if mcq_score is not None:
        score += mcq_score * 0.25
        completed_tests += 1
    
    if coding_score is not None:
        score += coding_score * 0.35
        completed_tests += 1
    
    if viva_score is not None:
        score += viva_score * 0.25
        completed_tests += 1
    
    if github_evidence:
        score += 15
    
    if completed_tests == 0:
        base_score = 0
    else:
        base_score = score
    
    return {
        "skill_authenticity_score": max(0, min(100, int(base_score))),
        "tests_completed": completed_tests,
        "mcq_score": mcq_score,
        "coding_score": coding_score,
        "viva_score": viva_score,
        "github_verified": github_evidence,
    }


class AdaptiveDifficultySystem:
    """Adaptive difficulty system that increases challenge based on performance."""
    
    def __init__(self, initial_difficulty: str = "easy"):
        self.current_difficulty = initial_difficulty
        self.difficulty_levels = ["easy", "medium", "hard", "expert"]
        self.current_index = self.difficulty_levels.index(initial_difficulty)
    
    def get_current_difficulty(self) -> str:
        return self.current_difficulty
    
    def adjust_difficulty(self, performance_score: int) -> str:
        """Adjust difficulty based on performance (0-100)."""
        if performance_score >= 85 and self.current_index < len(self.difficulty_levels) - 1:
            self.current_index += 1
            self.current_difficulty = self.difficulty_levels[self.current_index]
        elif performance_score < 50 and self.current_index > 0:
            self.current_index -= 1
            self.current_difficulty = self.difficulty_levels[self.current_index]
        
        return self.current_difficulty
