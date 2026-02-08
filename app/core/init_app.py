from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from settings import settings
from core.database import engine, Base
from api.v1.users import router as user_router

# 导入模型确保 Base 能识别到表结构
from models.user import User


async def init_db():
    """初始化数据库表"""
    try:
        logger.info(f"正在初始化数据库表 ({settings.DB_ENGINE})...")
        async with engine.begin() as conn:
            # 在异步引擎中执行同步的 create_all
            await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表初始化成功.")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. 启动时：初始化数据库
    await init_db()
    logger.info("应用启动成功.")
    yield
    # 2. 关闭时：释放连接池
    await engine.dispose()
    logger.info("数据库连接池已释放.")


def init_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan,
    )

    # 注册路由
    app.include_router(user_router, prefix="/api/v1")

    return app
