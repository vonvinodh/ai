import json
import urllib.request
import urllib.parse
from typing import Optional, Dict, List

from app.core.settings import GITHUB_TOKEN


def _make_github_request(url: str) -> Optional[dict]:
    request = urllib.request.Request(url, headers={"User-Agent": "EduProofAI"})
    if GITHUB_TOKEN:
        request.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except Exception:
        return None


def _normalize_github_url(url: str) -> Optional[str]:
    cleaned = url.strip().rstrip("/")
    if cleaned.startswith("https://github.com/"):
        path = cleaned[len("https://github.com/"):].strip("/")
        return path
    return None


def fetch_github_repos(github_url: str) -> Optional[List[Dict[str, object]]]:
    normalized = _normalize_github_url(github_url)
    if not normalized:
        return None

    parts = normalized.split("/")
    if len(parts) < 1:
        return None

    username = parts[0]
    api_url = f"https://api.github.com/users/{urllib.parse.quote(username)}/repos?per_page=100"
    data = _make_github_request(api_url)

    if not isinstance(data, list):
        return None

    return data


def extract_languages_from_repos(repos: Optional[List[Dict[str, object]]]) -> List[str]:
    if not repos:
        return []

    languages: Dict[str, int] = {}
    for repo in repos:
        language = repo.get("language")
        if language and isinstance(language, str):
            languages[language] = languages.get(language, 0) + 1

    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    return [lang[0] for lang in sorted_langs]


def calculate_github_contributions(repos: Optional[List[Dict[str, object]]]) -> Dict[str, object]:
    if not repos:
        return {
            "total_repos": 0,
            "total_stars": 0,
            "total_forks": 0,
            "primary_language": None,
            "languages": [],
        }

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos if isinstance(repo.get("stargazers_count"), int))
    total_forks = sum(repo.get("forks_count", 0) for repo in repos if isinstance(repo.get("forks_count"), int))
    languages = extract_languages_from_repos(repos)

    return {
        "total_repos": len(repos),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "primary_language": languages[0] if languages else None,
        "languages": languages,
    }


def fetch_github_repo_descriptions(github_url: str) -> Optional[str]:
    repos = fetch_github_repos(github_url)
    if not repos:
        return None

    descriptions = []
    for repo in repos:
        name = repo.get("name")
        description = repo.get("description")
        if name:
            descriptions.append(name)
        if description:
            descriptions.append(description)

    return "\n".join(descriptions) if descriptions else None
