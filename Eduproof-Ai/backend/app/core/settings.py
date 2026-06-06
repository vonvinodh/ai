from dotenv import load_dotenv
import os

load_dotenv()

GROC_API_KEY = os.getenv("GROC_API_KEY") or os.getenv("GEMINI_API_KEY")
GROC_API_URL = os.getenv("GROC_API_URL")
GROC_MODEL = os.getenv("GROC_MODEL") or "grok-4.3"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
