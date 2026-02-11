from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from loguru import logger

from app.api import router
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("Starting up...")
	# 数据库 schema 现在由 Alembic 迁移管理
	# 运行 "alembic upgrade head" 来初始化或更新数据库
	yield
	logger.info("Shutting down...")
	await engine.dispose()


# 用路由函数名作为 OpenAPI operationId，方便客户端代码生成
def custom_generate_unique_id(route: APIRoute) -> str:
	return route.name


def init_app() -> FastAPI:
	# 初始化日志系统（必须在最开始）
	setup_logging()

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
