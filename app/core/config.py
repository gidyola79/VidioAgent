from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "VidioAgent"
    SECRET_KEY: str = "development_secret"
    
    # AI Providers
    GROQ_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    ELEVENLABS_API_KEY: str | None = None
    REPLICATE_API_TOKEN: str | None = None
    
    # Twilio
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_WHATSAPP_NUMBER: str | None = None
    
    # Database & Redis
    DATABASE_URL: str | None = None
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    # Optional base URL for building absolute links (used for CORS and media URLs)
    BASE_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
