import os
from pathlib import Path

from fastapi.exceptions import HTTPException
from fastapi import Header
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis


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


def api_key_auth(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="API Key required")
    if not authorization.startswith("ApiKey "):
        raise HTTPException(status_code=401, detail="Invalid API Key format")
    api_key = authorization.split(" ")[1]
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True


# Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)
