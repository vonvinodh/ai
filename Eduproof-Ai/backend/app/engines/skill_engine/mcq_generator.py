from typing import Dict, List, Optional


MCQ_TEMPLATES = {
    "python": [
        {
            "question": "What is the output of print(2 ** 3)?",
            "options": ["6", "8", "9", "2"],
            "correct": 1,
            "difficulty": "easy",
        },
        {
            "question": "Which of the following is a mutable data type in Python?",
            "options": ["tuple", "string", "list", "int"],
            "correct": 2,
            "difficulty": "easy",
        },
        {
            "question": "What does the 'lambda' keyword do in Python?",
            "options": ["Defines a class", "Creates an anonymous function", "Imports a module", "Declares a variable"],
            "correct": 1,
            "difficulty": "medium",
        },
    ],
    "javascript": [
        {
            "question": "What does 'typeof null' return in JavaScript?",
            "options": ["null", "object", "undefined", "NaN"],
            "correct": 1,
            "difficulty": "medium",
        },
        {
            "question": "Which of the following is NOT a JavaScript data type?",
            "options": ["string", "number", "boolean", "alphabet"],
            "correct": 3,
            "difficulty": "easy",
        },
    ],
    "java": [
        {
            "question": "What is the correct way to declare a string in Java?",
            "options": ["String str = 'hello';", "string str = 'hello';", "String str = \"hello\";", "var str = 'hello';"],
            "correct": 2,
            "difficulty": "easy",
        },
    ],
}


def generate_mcqs(skill: str, difficulty: str = "mixed", count: int = 3) -> List[Dict[str, object]]:
    """Generate MCQs for a given skill."""
    skill_lower = skill.lower()
    
    if skill_lower not in MCQ_TEMPLATES:
        return []
    
    available_mcqs = MCQ_TEMPLATES[skill_lower]
    
    if difficulty != "mixed":
        available_mcqs = [q for q in available_mcqs if q.get("difficulty") == difficulty]
    
    return available_mcqs[:count]
