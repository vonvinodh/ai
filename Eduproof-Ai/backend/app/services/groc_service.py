import json
import re
import urllib.request
import urllib.error
from app.core.settings import GROC_API_KEY, GROC_API_URL, GROC_MODEL

DEFAULT_GROC_URL = "https://api.x.ai/v1/responses"


def _call_groc(prompt: str) -> dict:
    if not GROC_API_KEY:
        raise ValueError("GROC_API_KEY is not configured.")

    endpoint = GROC_API_URL or DEFAULT_GROC_URL
    payload = json.dumps({
        "model": GROC_MODEL,
        "input": [
            {"role": "system", "content": "You are Grok, a highly intelligent, helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
    }).encode("utf-8")

    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROC_API_KEY}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace") if e.fp is not None else ""
        raise RuntimeError(f"GROC HTTPError {e.code}: {body or e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"GROC URL error: {e.reason}") from e


def analyze_resume(text: str) -> dict:
    try:
        prompt = f"""
Extract:
Name
Skills
Education
Return ONLY valid JSON.

Resume:
{text[:2000]}
"""

        response = _call_groc(prompt)
        response_text = None

        if isinstance(response, dict):
            if "output" in response and isinstance(response["output"], list) and response["output"]:
                first_output = response["output"][0]
                if isinstance(first_output, dict) and "content" in first_output:
                    for item in first_output["content"]:
                        if isinstance(item, dict) and item.get("type") in {"output_text", "text"}:
                            response_text = item.get("text") or item.get("content")
                            break
                if response_text is None:
                    response_text = first_output.get("text") or first_output.get("output_text")
            if not response_text:
                response_text = response.get("output_text") or response.get("result") or response.get("text")
            if response_text is None:
                return {
                    "status": "failed",
                    "error": "GROC response did not include text output",
                    "raw_response": response,
                }
        else:
            response_text = str(response)

        clean_text = re.sub(r"```json", "", response_text, flags=re.IGNORECASE)
        clean_text = re.sub(r"```", "", clean_text)
        clean_text = clean_text.strip()

        return json.loads(clean_text)
    except Exception as e:
        return {
            "status": "failed",
            "error": f"{type(e).__name__}: {e}",
        }
