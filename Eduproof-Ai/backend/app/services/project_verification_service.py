from typing import Dict, Optional, List
import re


def verify_project_claims(deployment_links: list[str] = None, github_links: list[str] = None) -> Dict[str, object]:
    """
    Verify project deployment links and source code availability.
    """
    if not deployment_links:
        deployment_links = []
    if not github_links:
        github_links = []

    findings: Dict[str, object] = {
        "deployment_links_valid": [],
        "github_links_valid": [],
        "deployment_confidence": 0,
        "source_code_confidence": 0,
    }

    url_pattern = re.compile(r"https?://[^\s]+", re.IGNORECASE)

    for link in deployment_links:
        if url_pattern.match(link):
            findings["deployment_links_valid"].append(link)
            findings["deployment_confidence"] += 25

    for link in github_links:
        if "github.com" in link.lower() and url_pattern.match(link):
            findings["github_links_valid"].append(link)
            findings["source_code_confidence"] += 25

    findings["deployment_confidence"] = min(100, findings["deployment_confidence"])
    findings["source_code_confidence"] = min(100, findings["source_code_confidence"])

    return findings
