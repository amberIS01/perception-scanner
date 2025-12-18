from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "Perception Scanner"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: str = "http://localhost:5173"

    # Review fetching
    default_review_count: int = Field(default=100, ge=1, le=1000)
    max_review_count: int = Field(default=1000, ge=1, le=5000)

    # Google Play Store
    google_play_language: str = "en"
    google_play_country: str = "us"

    # iOS App Store
    ios_app_store_country: str = "us"

    # YouTube Data API v3
    youtube_api_key: Optional[str] = None

    # Product Hunt API
    product_hunt_api_token: Optional[str] = None

    # Reddit
    reddit_user_agent: str = "PerceptionScanner/1.0"

    # Request settings
    request_timeout: int = 30

    # Database
    database_url: str = "sqlite:///./perception_scanner.db"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
