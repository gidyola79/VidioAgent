from langchain_groq import ChatGroq
from app.core.config import settings

def get_llm(temperature: float = 0.7):
    """
    Returns a configured ChatGroq instance (Llama 3).
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")
    
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",  # Updated model (Dec 2024)
        temperature=temperature
    )
