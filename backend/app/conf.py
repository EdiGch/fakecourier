import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, validator

load_dotenv()


class Settings(BaseSettings):
    #########################
    # Basic module settings #
    #########################
    class Config:
        case_sensitive = True
        # env_file = os.environ.get("SETTINGS_ENV", ".env")

    SERVER_URL: str = os.getenv("SERVER_URL", "http://localhost")
    SERVER_PORT: int = os.getenv("SERVER_PORT", 8000)
    DATABASE_HOST: str = os.getenv("DB_HOST", "db")
    DATABASE_USER: str = os.getenv("DB_USER", "fake_courier")
    DATABASE_PASSWORD: str = os.getenv("DB_PASSWORD", "123456")
    DATABASE_NAME: str = os.getenv("DB_NAME", "fake_courier")
    DATABASE_PORT: str = os.getenv("DB_PORT", "5432")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URI_WITHOUT_DB: Optional[PostgresDsn] = None
    OPENAPI_URL: str = os.environ.get("OPENAPI_URL", "/openapi.json")
    PYTEST: bool = False
    DEBUG: bool = os.environ.get("DEBUG", False)
    HOST_URL: str = os.getenv("HOST_URL", "http://localhost")

    VERSION: str = os.getenv("VERSION", "0.1")

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            path=f"/{values.get('DATABASE_NAME') or ''}",
            port=values.get("DATABASE_PORT"),
        )

    @validator("SQLALCHEMY_DATABASE_URI_WITHOUT_DB", pre=True)
    def assemble_db_connection_db(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=values.get("DATABASE_PORT"),
        )


settings = Settings()
