import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CivicShield"
    # Fallback to local SQLite if DATABASE_URL is not set or empty
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./civicshield.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "7d4b47e44a9561081691230cd8325a7a9228d73b64c02932b132e01dfb003a27")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    AI_MODEL_PATH: str = "./app/ai/models"

    class Config:
        env_file = ".env"

settings = Settings()
