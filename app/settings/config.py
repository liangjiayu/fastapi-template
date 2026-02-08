from typing import Any, Dict
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # 基础信息
    APP_TITLE: str = "FastAPI Project"
    APP_DESCRIPTION: str = "A modern FastAPI project structure"
    DEBUG: bool = True
    APP_ENV: str = "development"

    # 数据库配置
    DB_ENGINE: str = "postgres"  # "postgres" 或 "sqlite"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "secret"
    DB_NAME: str = "app_db"

    @computed_field
    @property
    def db_config(self) -> Dict[str, Any]:
        """封装数据库连接信息与引擎参数"""
        if self.DB_ENGINE == "sqlite":
            return {
                "url": "sqlite+aiosqlite:///./test.db",
                "engine_kwargs": {
                    "connect_args": {"check_same_thread": False},
                },
            }

        # PostgreSQL 配置
        return {
            "url": f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
            "engine_kwargs": {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": True,
            },
        }


settings = Settings()
