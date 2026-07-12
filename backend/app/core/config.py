from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://ecosphere:ecosphere_pass@localhost:5432/ecosphere_db"
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
