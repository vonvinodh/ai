from typing import Dict, List, Optional
from datetime import datetime


def detect_overlapping_experiences(experience_timeline: List[Dict[str, object]]) -> Dict[str, object]:
    """Detect impossible overlapping experiences."""
    overlaps = []
    
    for i in range(len(experience_timeline)):
        for j in range(i + 1, len(experience_timeline)):
            entry1 = experience_timeline[i]
            entry2 = experience_timeline[j]
            
            if "Ended" in entry1.get("event", "") and "Started" in entry2.get("event", ""):
                date1 = entry1.get("date")
                date2 = entry2.get("date")
                
                if date1 and date2 and date1 > date2:
                    overlaps.append({
                        "event1": entry1.get("event"),
                        "event2": entry2.get("event"),
                        "date1": date1.isoformat(),
                        "date2": date2.isoformat(),
                    })
    
    return {
        "overlaps_detected": len(overlaps) > 0,
        "overlaps": overlaps,
    }


def detect_skill_evolution_gaps(claimed_skills: List[str], skill_timeline: List[Dict[str, object]]) -> Dict[str, object]:
    """Detect skills claimed without prior evidence."""
    gaps = []
    
    for skill in claimed_skills:
        skill_lower = skill.lower()
        skill_evidence = [event for event in skill_timeline if skill_lower in event.get("event", "").lower()]
        
        if not skill_evidence:
            gaps.append({
                "skill": skill,
                "reason": "No prior evidence of skill development",
            })
    
    return {
        "gaps_detected": len(gaps) > 0,
        "gaps": gaps,
    }


def detect_timeline_inconsistencies(combined_timeline: List[Dict[str, object]]) -> Dict[str, object]:
    """Detect general timeline inconsistencies."""
    inconsistencies = []
    
    for i in range(len(combined_timeline) - 1):
        current = combined_timeline[i]
        next_event = combined_timeline[i + 1]
        
        date1 = current.get("date")
        date2 = next_event.get("date")
        
        if date1 and date2 and date1 == date2:
            inconsistencies.append({
                "event1": current.get("event"),
                "event2": next_event.get("event"),
                "issue": "Same date for different events",
            })
    
    return {
        "inconsistencies_detected": len(inconsistencies) > 0,
        "inconsistencies": inconsistencies,
    }
