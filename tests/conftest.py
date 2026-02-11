import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import app

# 使用内存 SQLite 进行测试隔离
TEST_DATABASE_URL = "sqlite+aiosqlite:///"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_db():
	async with TestSessionLocal() as session:
		try:
			yield session
		finally:
			await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def setup_database():
	"""每个测试前建表，测试后删表，确保完全隔离"""
	async with test_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
	yield
	async with test_engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
	"""异步 HTTP 客户端，直接与 ASGI 应用通信"""
	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url="http://test") as ac:
		yield ac
