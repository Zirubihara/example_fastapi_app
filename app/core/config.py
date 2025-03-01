import os
from logging import INFO, WARNING
from typing import Final, List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class BaseConfig:
    """Base configuration class with common settings."""

    # Database settings
    DATABASE_URL: Final = os.getenv("DATABASE_URL")
    DATABASE_POOL_SIZE: Final = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    DATABASE_MAX_OVERFLOW: Final = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))

    # Security settings
    SECRET_KEY: Final = os.getenv("SECRET_KEY")
    JWT_EXPIRATION_HOURS: Final = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    PASSWORD_MIN_LENGTH: Final = 8

    # Email settings
    ALLOWED_EMAIL_DOMAIN: Final = "@gmail.com"
    SMTP_HOST: Final = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: Final = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Final = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Final = os.getenv("SMTP_PASSWORD")

    # API settings
    API_VERSION: Final = "v1"
    API_PREFIX: Final = f"/api/{API_VERSION}"
    RATE_LIMIT_PER_MINUTE: Final = int(os.getenv("RATE_LIMIT", "60"))

    # Logging settings
    LOG_LEVEL: Final = INFO
    LOG_FORMAT: Final = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration settings."""
        required_settings = {
            "DATABASE_URL": cls.DATABASE_URL,
            "SECRET_KEY": cls.SECRET_KEY,
        }

        missing_settings = [
            key for key, value in required_settings.items() if not value
        ]

        if missing_settings:
            raise ValueError(
                f"Missing required configuration settings: {', '.join(missing_settings)}"
            )


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""

    DEBUG: Final = True
    TESTING: Final = False
    LOG_LEVEL: Final = INFO

    # Development-specific settings
    CORS_ORIGINS: Final = ["http://localhost:3000"]
    SWAGGER_UI_ENABLED: Final = True


class TestingConfig(BaseConfig):
    """Testing environment configuration."""

    DEBUG: Final = False
    TESTING: Final = True
    LOG_LEVEL: Final = WARNING

    # Test database settings
    DATABASE_URL: Final = "sqlite:///./test.db"

    # Test-specific settings
    CORS_ORIGINS: Final = ["http://localhost:3000"]
    SWAGGER_UI_ENABLED: Final = True


class ProductionConfig(BaseConfig):
    """Production environment configuration."""

    DEBUG: Final = False
    TESTING: Final = False
    LOG_LEVEL: Final = WARNING

    # Production-specific settings
    CORS_ORIGINS: Final = os.getenv("CORS_ORIGINS", "").split(",")
    SWAGGER_UI_ENABLED: Final = False

    # Override pool settings for production
    DATABASE_POOL_SIZE: Final = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: Final = int(os.getenv("DATABASE_MAX_OVERFLOW", "30"))


def get_config():
    """Get configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()

    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    config_class = configs.get(env, DevelopmentConfig)
    config_class.validate()
    return config_class


# Create configuration instance
Config = get_config()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Example App"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A FastAPI example application"
    API_V1_STR: str = "/api/v1"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"

settings = Settings()
