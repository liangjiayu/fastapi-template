from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from loguru import logger

from app.api import router
from app.core.config import settings
from app.core.database import engine, init_db
from app.core.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("Starting up...")
	# SQLite 自动建表；PostgreSQL 应通过迁移工具管理表结构
	if settings.DB_ENGINE == "sqlite":
		await init_db()
	yield
	logger.info("Shutting down...")
	await engine.dispose()


# 用路由函数名作为 OpenAPI operationId，方便客户端代码生成
def custom_generate_unique_id(route: APIRoute) -> str:
	return route.name


def init_app() -> FastAPI:
	app = FastAPI(
		title=settings.APP_TITLE,
		description=settings.APP_DESCRIPTION,
		lifespan=lifespan,
		generate_unique_id_function=custom_generate_unique_id,
	)
	register_exception_handlers(app)
	app.include_router(router)

	# 自定义 OpenAPI schema：移除 FastAPI 默认的 422 响应和校验相关 schema，
	def custom_openapi():
		if app.openapi_schema:
			return app.openapi_schema
		openapi_schema = get_openapi(
			title=app.title,
			version=app.version,
			description=app.description,
			routes=app.routes,
		)
		for path in openapi_schema["paths"].values():
			for method in path.values():
				method.get("responses", {}).pop("422", None)
		schemas = openapi_schema.get("components", {}).get("schemas", {})
		schemas.pop("HTTPValidationError", None)
		schemas.pop("ValidationError", None)
		app.openapi_schema = openapi_schema
		return openapi_schema

	app.openapi = custom_openapi
	return app
