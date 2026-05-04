import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

# Model configuration — defaults to a fast, capable model on Groq
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to the .env file:\n"
        "  GROQ_API_KEY=gsk_...\n\n"
        "Get your free key at: https://console.groq.com/keys"
    )
