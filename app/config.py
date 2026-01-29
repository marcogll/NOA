from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "NOA - Networked Operational Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None

    # Evolution API
    EVOLUTION_API_URL: Optional[str] = None
    EVOLUTION_API_TOKEN: Optional[str] = None

    # Database
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "noa_db"
    DATABASE_URL: Optional[str] = None

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
