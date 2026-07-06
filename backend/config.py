"""
Scout Configuration.

Central configuration for environment variables
and application constants.
"""

import os

from dotenv import load_dotenv

# ==========================================================
# Environment
# ==========================================================

load_dotenv()

# ==========================================================
# API Keys
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is not configured."
    )

if not SERPER_API_KEY:
    raise RuntimeError(
        "SERPER_API_KEY is not configured."
    )

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./scout.db",
)

# ==========================================================
# Search
# ==========================================================

SERPER_URL = "https://google.serper.dev/search"

SEARCH_TIMEOUT = 10

# ==========================================================
# Models
# ==========================================================

GEMINI_MODEL = "gemini-2.5-flash"