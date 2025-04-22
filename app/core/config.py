from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional, Union
import secrets
import os


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "HotLabel Publisher Management"
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", None)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "hotlabel_publishers"
    DATABASE_URI: Optional[str] = None
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if self.DATABASE_URI:
            return self.DATABASE_URI
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
