from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "LegalEase"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    demo_mode: bool = True
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    frontend_backend_url: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
