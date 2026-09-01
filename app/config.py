import os
from dotenv import load_dotenv

load_dotenv()

class Settngs:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"

    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")

    QDRANT_URL = os.getenv("QDRANT_CLUSTER_ENDPOINT")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = "enterprise_rag"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settngs()