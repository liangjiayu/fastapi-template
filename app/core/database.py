from collections.abc import AsyncGenerator

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


async def init_db() -> None:
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
