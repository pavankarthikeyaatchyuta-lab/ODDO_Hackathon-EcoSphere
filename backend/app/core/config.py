from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://neondb_owner:npg_EjnaB2r7HyzL@ep-divine-poetry-at2qm1gc-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"
    secret_key: str = "supersecretkey123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    ai_provider: str = "groq"
    groq_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434/v1"
    ai_model: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
