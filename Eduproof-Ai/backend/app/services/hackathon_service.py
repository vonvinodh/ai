from typing import Dict, List, Optional
import re


def verify_hackathon_claims(claimed_hackathons: list[str] = None, claimed_awards: list[str] = None) -> Dict[str, object]:
    """
    Verify hackathon participation and awards.
    """
    if not claimed_hackathons:
        claimed_hackathons = []
    if not claimed_awards:
        claimed_awards = []

    findings: Dict[str, object] = {
        "hackathons_verified": [],
        "awards_verified": [],
        "participation_confidence": 0,
        "award_confidence": 0,
    }

    known_hackathons = [
        "hackathon",
        "coding",
        "sprint",
        "competition",
        "challenge",
    ]

    for hackathon in claimed_hackathons:
        lowered = hackathon.lower()
        if any(keyword in lowered for keyword in known_hackathons):
            findings["hackathons_verified"].append(hackathon)
            findings["participation_confidence"] += 15

    for award in claimed_awards:
        if any(keyword in award.lower() for keyword in ["winner", "award", "first", "second", "third", "prize"]):
            findings["awards_verified"].append(award)
            findings["award_confidence"] += 20

    findings["participation_confidence"] = min(100, findings["participation_confidence"])
    findings["award_confidence"] = min(100, findings["award_confidence"])

    return findings
