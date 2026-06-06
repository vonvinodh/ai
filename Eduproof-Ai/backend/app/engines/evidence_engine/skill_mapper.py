from typing import Dict, List, Optional


def map_skills_to_github(claimed_skills: list[str] = None, github_languages: list[str] = None) -> Dict[str, object]:
    """
    Map claimed skills to GitHub language evidence.
    """
    if not claimed_skills:
        claimed_skills = []
    if not github_languages:
        github_languages = []

    skill_language_mapping = {
        "python": ["python"],
        "java": ["java"],
        "javascript": ["javascript", "js"],
        "typescript": ["typescript", "ts"],
        "react": ["javascript", "typescript"],
        "nodejs": ["javascript"],
        "golang": ["go"],
        "rust": ["rust"],
        "cpp": ["c++"],
        "csharp": ["c#"],
        "sql": ["sql"],
        "html": ["html"],
        "css": ["css"],
    }

    github_lower = [lang.lower() for lang in github_languages]
    mapped_skills = []
    unverified_skills = []

    for skill in claimed_skills:
        skill_lower = skill.lower()
        possible_langs = skill_language_mapping.get(skill_lower, [skill_lower])
        matched = any(lang.lower() in github_lower for lang in possible_langs)

        if matched:
            mapped_skills.append(skill)
        else:
            unverified_skills.append(skill)

    return {
        "claimed_skills": claimed_skills,
        "github_evidence": github_languages,
        "mapped_skills": mapped_skills,
        "unverified_skills": unverified_skills,
        "skill_confidence": len(mapped_skills) / len(claimed_skills) if claimed_skills else 0,
    }
