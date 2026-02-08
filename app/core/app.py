from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api import router
from app.core.config import settings
from app.core.database import engine, init_db
from app.core.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("Starting up...")
	if settings.APP_ENV == "development":
		await init_db()
	yield
	logger.info("Shutting down...")
	await engine.dispose()


def init_app() -> FastAPI:
	app = FastAPI(
		title=settings.APP_TITLE,
		description=settings.APP_DESCRIPTION,
		lifespan=lifespan,
	)
	register_exception_handlers(app)
	app.include_router(router)
	return app
