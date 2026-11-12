from langchain_groq import ChatGroq
from app.core.config import settings

def get_fast_llm() -> ChatGroq:
    """Returns a fast, cheap LLM for classification and summarization."""
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL_FAST, # defaults to llama-3.1-8b-instant
        temperature=0.0,
        max_tokens=500,
    )