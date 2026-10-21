"""Server-only configuration; startup works without AI credentials."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def integer(name: str, default: int, low: int, high: int) -> int:
    value = int(os.getenv(name, str(default)))
    if not low <= value <= high:
        raise ValueError(f"{name} must be between {low} and {high}")
    return value


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Groq SDK 1.x appends /openai/v1 itself. OpenAI-compatible clients instead
# require https://api.groq.com/openai/v1 as their base URL.
GROQ_BASE_URL = "https://api.groq.com"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
AI_TIMEOUT = integer("AI_TIMEOUT", 30, 1, 120)
CHAT_TIMEOUT = integer("CHAT_TIMEOUT", 120, 5, 300)
AI_MAX_TOKENS = integer("AI_MAX_TOKENS", 2048, 256, 8192)
AI_CONCURRENCY = integer("AI_CONCURRENCY", 2, 1, 10)
CHAT_REQUESTS_PER_MINUTE = integer("CHAT_REQUESTS_PER_MINUTE", 10, 1, 100)
MAX_MESSAGE_LENGTH = 4000
MAX_BODY_BYTES = 24000
MAX_HISTORY_MESSAGES = 12
MAX_HISTORY_CHARS = 16000
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{(ROOT / 'scout.db').as_posix()}")
ALLOWED_ORIGINS = [
    s.strip()
    for s in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if s.strip()
]
SESSION_SECRET = os.getenv("SESSION_SECRET", "")
SECURE_COOKIES = os.getenv("SECURE_COOKIES", "false").lower() == "true"
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
SERPER_URL = "https://google.serper.dev/search"
SEARCH_TIMEOUT = 10
# Optional legacy semantic index: Groq has no embedding endpoint.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
