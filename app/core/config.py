from functools import cached_property

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)

	# 应用配置
	APP_ENV: str = "development"
	APP_TITLE: str = "FastAPI Project"
	APP_DESCRIPTION: str = "A modern FastAPI project structure"
	DEBUG: bool = True

	# 数据库配置
	DB_ENGINE: str = "sqlite"  # "sqlite" | "postgres"
	DB_NAME: str = "fastapi_db"
	DB_HOST: str = "localhost"
	DB_PORT: int = 5432
	DB_USER: str = "postgres"
	DB_PASSWORD: str = ""

	# 日志配置
	LOG_LEVEL: str = "INFO"
	LOG_FILE_ENABLED: bool = True
	LOG_FILE_ROTATION: str = "1 day"
	LOG_FILE_RETENTION: str = "7 days"

	@computed_field
	@cached_property
	def DATABASE_URL(self) -> str:
		if self.DB_ENGINE == "postgres":
			return (
				f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
			)
		return f"sqlite+aiosqlite:///./{self.DB_NAME}.db"

	@computed_field
	@cached_property
	def DATABASE_ENGINE_OPTIONS(self) -> dict:
		"""根据数据库类型返回对应的引擎参数"""
		if self.DB_ENGINE == "postgres":
			return {
				"echo": self.DEBUG,
				"pool_size": 5,
				"max_overflow": 10,
				"pool_recycle": 3600,
				"pool_pre_ping": True,
			}
		return {
			"echo": self.DEBUG,
		}


settings = Settings()
