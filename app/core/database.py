from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from settings import settings

# 从 settings 获取计算好的配置
db_setup = settings.db_config

# 创建异步引擎
engine = create_async_engine(
    db_setup["url"], echo=settings.DEBUG, **db_setup["engine_kwargs"]
)

# 创建异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# 声明式基类：所有 models/*.py 里的类都要继承它
class Base(DeclarativeBase):
    pass


# FastAPI 依赖注入项
async def get_db():
    """获取数据库异步连接会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
