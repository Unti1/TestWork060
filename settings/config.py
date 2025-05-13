from pathlib import Path

from fastapi.exceptions import HTTPException
from fastapi import Security
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis
from fastapi.security import APIKeyHeader


class Settings(BaseSettings):
    ROOT_PATH: Path = Path(__file__).parent.parent
    MEDIA_PATH: Path = ROOT_PATH / "static" / "media"

    # database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    TEST_DB_NAME: str

    DATABASE_SQLITE: str = "sqlite+aiosqlite:///data/db.sqlite3"

    REDIS_DB: int
    REDIS_HOST: str
    REDIS_PORT: int

    DTFORMAT: str = "%Y-%m-%d-T%H:%M:%S"

    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env", env_file_encoding="utf-8"
    )

    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_test_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"


settings = Settings()


# Redis клиент
redis_client = redis.Redis.from_url(settings.get_redis_url())

# API Key аутентификация
api_key_header = APIKeyHeader(name="Authorization")

def api_key_auth(api_key: str = Security(api_key_header)):
    if api_key != f"ApiKey {settings.API_KEY}":
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return api_key
