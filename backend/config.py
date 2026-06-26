from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = "scout"
MODEL_NAME = "gemini-2.5-flash"

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is missing.")