import os
import secrets
from typing import Any, Dict, Optional

from pydantic import (BaseSettings, PostgresDsn, validator)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Rental Bike'

    BASE_DIR: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    TEMPLATES_DIR: str = 'templates'
    MEDIA_DIR: str = 'media'
    DIRS = ('bikes_photo',)
    HOST: str = 'localhost'
    PORT: int = 80

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SMTP_USER: str
    SMTP_FROM: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls,
        v: Optional[str],
        values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
