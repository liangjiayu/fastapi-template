from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)

	APP_TITLE: str = "FastAPI Project"
	APP_DESCRIPTION: str = "A modern FastAPI project structure"
	DEBUG: bool = True

	DB_ENGINE: str = "sqlite"  # "sqlite" | "postgres"

	DB_HOST: str = "localhost"
	DB_PORT: int = 5432
	DB_USER: str = "postgres"
	DB_PASSWORD: str = ""
	DB_NAME: str = "fastapi_db"

	@computed_field
	@cached_property
	def DATABASE_URL(self) -> str:
		if self.DB_ENGINE == "postgres":
			return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
		return "sqlite+aiosqlite:///./test.db"


settings = Settings()
