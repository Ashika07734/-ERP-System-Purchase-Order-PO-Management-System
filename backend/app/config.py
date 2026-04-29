from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GroceryERP API"
    api_prefix: str = "/api/v1"
    debug: bool = True
    enable_scheduler: bool = False

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/groceryerp"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    cors_origins: str = "*"

    oauth_google_client_id: str | None = None
    oauth_google_client_secret: str | None = None

    ai_provider: str = "openai"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
