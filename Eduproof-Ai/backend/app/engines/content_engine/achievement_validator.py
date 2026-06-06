import re
from typing import Dict, List

UNREALISTIC_KEYWORDS = [
    "world-class",
    "industry-leading",
    "best ever",
    "unprecedented",
    "perfect",
    "100%",
    "first-ever",
    "revolutionized",
    "unmatched",
    "unrivaled",
    "game-changing",
    "never before",
]


def validate_achievements(text: str) -> Dict[str, object]:
    lowered = text.lower()
    findings: List[str] = []

    for keyword in UNREALISTIC_KEYWORDS:
        if keyword in lowered:
            findings.append(keyword)

    high_boosts = re.findall(r"(\d+)%", text)
    for boost in high_boosts:
        try:
            value = int(boost)
            if value > 300:
                findings.append(f"unrealistic percent increase: {value}%")
        except ValueError:
            continue

    return {
        "unrealistic_claims": bool(findings),
        "flags": findings,
    }
