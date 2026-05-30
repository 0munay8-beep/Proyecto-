"""
Central configuration for the application
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Core
    app_name: str = "Bus Management System"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/bus_management"
    sqlalchemy_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 40

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    jwt_secret: str = "your-jwt-secret-change-in-production"

    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_cache_ttl: int = 3600

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Email
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_name: str = "Bus Management System"

    # Celery
    celery_broker_url: str = "redis://localhost:6379"
    celery_result_backend: str = "redis://localhost:6379"

    # ML Settings
    model_update_interval: int = 3600
    anomaly_threshold: float = 0.85
    forecast_days: int = 7
    cluster_numbers: int = 5

    # Maps
    map_default_lat: float = 10.3910
    map_default_lon: float = -75.4794
    map_default_zoom: int = 12
    geocoder_provider: str = "nominatim"

    # Optimization Algorithms
    genetic_algorithm_population: int = 100
    genetic_algorithm_generations: int = 50
    simulated_annealing_temp: float = 1000
    simulated_annealing_cooling_rate: float = 0.95

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()