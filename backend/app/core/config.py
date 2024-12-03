from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database Settings
    DATABASE_URL: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # CORS Settings
    CORS_ORIGINS: str

    # API Settings
    GROK_API_KEY: str
    GROK_API_BASE: str

    # Logging Settings
    LOG_LEVEL: str
    LOG_FILE: str
    LOG_MAX_SIZE: int
    LOG_BACKUP_COUNT: int
    LOG_FORMAT: str

    @property
    def cors_origins(self) -> List[str]:
        """将字符串转换为列表"""
        return self.CORS_ORIGINS.split(",")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 