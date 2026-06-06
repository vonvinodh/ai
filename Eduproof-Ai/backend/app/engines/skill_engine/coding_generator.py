from typing import Dict, List


CODING_CHALLENGES = {
    "python": [
        {
            "title": "Fibonacci Sequence",
            "description": "Write a function that returns the first n Fibonacci numbers.",
            "test_cases": [
                {"input": 5, "output": [0, 1, 1, 2, 3]},
                {"input": 1, "output": [0]},
            ],
            "difficulty": "easy",
        },
        {
            "title": "Prime Checker",
            "description": "Write a function that checks if a number is prime.",
            "test_cases": [
                {"input": 17, "output": True},
                {"input": 4, "output": False},
            ],
            "difficulty": "easy",
        },
        {
            "title": "Reverse String with Recursion",
            "description": "Reverse a string using recursion.",
            "difficulty": "medium",
        },
    ],
    "javascript": [
        {
            "title": "Array Sum",
            "description": "Write a function that sums all numbers in an array.",
            "test_cases": [
                {"input": [1, 2, 3], "output": 6},
                {"input": [10, 20], "output": 30},
            ],
            "difficulty": "easy",
        },
    ],
}


def generate_coding_challenges(skill: str, difficulty: str = "easy", count: int = 2) -> List[Dict[str, object]]:
    """Generate coding challenges for a skill."""
    skill_lower = skill.lower()
    
    if skill_lower not in CODING_CHALLENGES:
        return []
    
    challenges = CODING_CHALLENGES[skill_lower]
    
    if difficulty != "mixed":
        challenges = [c for c in challenges if c.get("difficulty") == difficulty]
    
    return challenges[:count]
