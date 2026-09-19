from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# Load variables from .env into the process environment.
# This is required because the provided AI provider factory
# reads LLM_PROVIDER and API keys using os.getenv().
load_dotenv()


class Settings(BaseSettings):
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://postgres:dev@localhost:5432/foodanalyzer"
    nutrition_cache_ttl_seconds: int = 86400
    max_image_size_mb: int = 5
    http_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()