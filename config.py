import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    config = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "GROQ_MODEL": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "WATCHMODE_API_KEY": os.getenv("WATCHMODE_API_KEY", ""),
        "INSTAGRAM_USERNAME": os.getenv("INSTAGRAM_USERNAME", ""),
        "INSTAGRAM_PASSWORD": os.getenv("INSTAGRAM_PASSWORD", ""),
        "USE_MOCK_DATA": os.getenv("USE_MOCK_DATA", "false").lower() == "true",
    }
    if not config["GROQ_API_KEY"] or not config["GROQ_API_KEY"].startswith("gsk_"):
        raise ValueError("❌ Установите GROQ_API_KEY в .env (формат gsk_...)")
    return config
