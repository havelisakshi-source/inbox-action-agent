from functools import lru_cache
from typing import Literal, Annotated
import json

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "Inbox Action Agent"
    ENVIRONMENT: Literal["development", "production", "test"] = "development"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"
    
    # NoDecode prevents Pydantic from trying to parse this as JSON automatically
    CORS_ORIGINS: Annotated[list[str], NoDecode] = ["http://localhost:5173"]

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TOKEN_ENCRYPTION_KEY: str

    DATABASE_URL: str

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/google/callback"
    
    GMAIL_SCOPES: Annotated[list[str], NoDecode] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.compose",
    ]

    LLM_PROVIDER: Literal["groq", "openai"] = "groq"
    GROQ_API_KEY: str = ""
    # Updated to active, working models
    GROQ_MODEL_FAST: str = "openai/gpt-oss-20b"
    GROQ_MODEL_REASONING: str = "openai/gpt-oss-120b"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_FAST: str = "gpt-4o-mini"
    OPENAI_MODEL_REASONING: str = "gpt-4o"
    LLM_MAX_TOKENS_PER_EMAIL: int = 2000
    LLM_TIMEOUT_SECONDS: int = 45

    AGENT_MAX_RETRIES: int = 2
    AGENT_TIMEOUT_SECONDS: int = 120
    AGENT_RECURSION_LIMIT: int = 25
    AUTO_APPROVE_LOW_RISK: bool = True

    MOCK_GMAIL: bool = False
    MOCK_LLM: bool = False
    LOG_LEVEL: str = "INFO"

    @field_validator("CORS_ORIGINS", "GMAIL_SCOPES", mode="before")
    @classmethod
    def _parse_list(cls, v):
        if isinstance(v, str):
            v = v.strip()
            # If it's a wildcard
            if v == "*":
                return ["*"]
            # If it's a JSON array string (like ["url1", "url2"])
            if v.startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Otherwise, treat it as a comma-separated string (like "url1,url2")
            return [x.strip() for x in v.split(",") if x.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()