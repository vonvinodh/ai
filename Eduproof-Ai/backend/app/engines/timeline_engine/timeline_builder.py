from typing import Dict, List, Optional
from datetime import datetime


def parse_timeline_entry(date_str: Optional[str], event: str) -> Optional[Dict[str, object]]:
    """Parse a timeline entry with date and event."""
    if not date_str or not event:
        return None
    
    try:
        date_obj = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return {
            "date": date_obj,
            "event": event.strip(),
            "year": date_obj.year,
            "month": date_obj.month,
        }
    except ValueError:
        return None


def build_academic_timeline(education_list: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """Build academic timeline from education entries."""
    timeline = []
    
    for edu in education_list:
        start_date = edu.get("start_date")
        end_date = edu.get("end_date")
        degree = edu.get("degree", "")
        
        if start_date:
            start_entry = parse_timeline_entry(start_date, f"Started {degree}")
            if start_entry:
                timeline.append(start_entry)
        
        if end_date:
            end_entry = parse_timeline_entry(end_date, f"Completed {degree}")
            if end_entry:
                timeline.append(end_entry)
    
    return sorted(timeline, key=lambda x: x["date"])


def build_experience_timeline(experience_list: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """Build experience timeline from work entries."""
    timeline = []
    
    for exp in experience_list:
        start_date = exp.get("start_date")
        end_date = exp.get("end_date")
        title = exp.get("title", "")
        
        if start_date:
            start_entry = parse_timeline_entry(start_date, f"Started as {title}")
            if start_entry:
                timeline.append(start_entry)
        
        if end_date:
            end_entry = parse_timeline_entry(end_date, f"Ended {title}")
            if end_entry:
                timeline.append(end_entry)
    
    return sorted(timeline, key=lambda x: x["date"])


def build_certificate_timeline(certificates: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """Build certificate timeline from certificate entries."""
    timeline = []
    
    for cert in certificates:
        issue_date = cert.get("issue_date")
        name = cert.get("name", "")
        
        if issue_date:
            entry = parse_timeline_entry(issue_date, f"Obtained {name}")
            if entry:
                timeline.append(entry)
    
    return sorted(timeline, key=lambda x: x["date"])
