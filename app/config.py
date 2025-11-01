"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./billing_system.db"
    
    # Email Configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SENDER_EMAIL: Optional[str] = None
    SENDER_PASSWORD: Optional[str] = None
    
    # Application
    APP_NAME: str = "Billing System API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Denominations (default shop denominations)
    DEFAULT_DENOMINATIONS: list = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
