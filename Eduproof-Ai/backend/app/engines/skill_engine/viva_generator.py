from typing import Dict, List


VIVA_QUESTIONS = {
    "python": [
        "Explain the difference between list and tuple in Python.",
        "What is the Global Interpreter Lock (GIL)?",
        "How does Python manage memory?",
        "What are decorators and how do they work?",
        "Explain list comprehensions with an example.",
    ],
    "javascript": [
        "What is the difference between var, let, and const?",
        "Explain closures with a real-world example.",
        "What is the event loop in JavaScript?",
        "How does async/await work?",
        "What is the difference between == and ===?",
    ],
    "java": [
        "What is the difference between abstract class and interface?",
        "Explain the concept of polymorphism.",
        "What are checked and unchecked exceptions?",
        "How does garbage collection work in Java?",
        "Explain the difference between HashMap and Hashtable.",
    ],
}


def generate_viva_questions(skill: str, count: int = 3) -> List[str]:
    """Generate viva/interview questions for a skill."""
    skill_lower = skill.lower()
    
    if skill_lower not in VIVA_QUESTIONS:
        return []
    
    questions = VIVA_QUESTIONS[skill_lower]
    return questions[:count]
