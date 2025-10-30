import os
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")

MCP_SERVERS = {
    "playwright": {
        "url": os.getenv("MCP_PLAYWRIGHT_URL", "http://localhost:8931/mcp"),
        "transport": os.getenv("MCP_PLAYWRIGHT_TRANSPORT", "streamable_http"),
    }
}

if GEMINI_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
else:
    raise EnvironmentError("❌ Missing GEMINI_API_KEY in .env file")
