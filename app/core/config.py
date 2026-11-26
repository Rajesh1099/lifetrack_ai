
from pathlib import Path  # Import Path to build the .env file path

from pydantic_settings import BaseSettings, SettingsConfigDict  # Import settings management classes

class Settings(BaseSettings):  # Define all application configuration settings
    APP_NAME: str  # Application name
    APP_ENV: str  # Application environment
    DEBUG: bool  # Enable or disable debug mode
    API_V1_PREFIX: str  # API version prefix
    
    BACKEND_BASE_URL: str  # Base URL used to construct backend links

    DB_HOST: str  # Database host
    DB_PORT: int  # Database port
    DB_NAME: str  # Database name
    DB_USER: str  # Database username
    DB_PASSWORD: str  # Database password

    SECRET_KEY: str  # Secret key used for JWT signing
    ALGORITHM: str  # JWT signing algorithm
    
    EMAIL_SECRET_KEY: str  # Secret key used only for email verification tokens

    SMTP_HOST: str  # SMTP server address
    SMTP_PORT: int  # SMTP server port
    SMTP_USERNAME: str  # Gmail email address used to send emails
    SMTP_PASSWORD: str  # Gmail app password
    SMTP_FROM_EMAIL: str  # Sender email address
    SMTP_FROM_NAME: str  # Sender display name

    model_config = SettingsConfigDict(  # Configure how settings are loaded
        env_file=Path(__file__).resolve().parents[2] / ".env",  # Load variables from backend/.env
        env_file_encoding="utf-8",  # Read the environment file as UTF-8
        extra="ignore"  # Ignore environment variables not declared above
    )

settings = Settings()  # Create the settings object
