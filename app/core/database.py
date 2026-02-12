from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, **settings.DATABASE_ENGINE_OPTIONS)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
	pass


async def get_db() -> AsyncGenerator[AsyncSession]:
	async with AsyncSessionLocal() as session:
		try:
			yield session
		finally:
			await session.close()


# 依赖注入类型别名，路由中直接用 db: DB 即可获取数据库会话
DB = Annotated[AsyncSession, Depends(get_db)]
