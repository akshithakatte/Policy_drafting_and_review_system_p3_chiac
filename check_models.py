from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

try:
    models = client.models.list()
    print("Available Groq models:")
    for model in models.data:
        print(f"- {model.id}")
    print(f"\nActive model for this project: {LLM_MODEL}")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure GROQ_API_KEY is set correctly in the .env file.")
