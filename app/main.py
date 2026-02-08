from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api.users import router as user_router
from app.core.config import settings
from app.core.database import engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("Starting up...")
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
	app.include_router(user_router, prefix="/api")
	return app
