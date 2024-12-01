import os
import logging
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    GROK_API_KEY: str
    GROK_API_BASE: str
    
    # Database Configuration
    DATABASE_URL: str
    
    # CORS Configuration
    CORS_ORIGINS: str
    
    # Logging Configuration
    LOG_LEVEL: str
    LOG_FILE: str
    LOG_MAX_SIZE: int
    LOG_BACKUP_COUNT: int
    LOG_FORMAT: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_log_level(self) -> int:
        """获取日志级别"""
        return getattr(logging, self.LOG_LEVEL.upper())

settings = Settings() 