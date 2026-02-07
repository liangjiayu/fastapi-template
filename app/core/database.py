from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# 拼接异步连接字符串
DATABASE_URL = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# 1. 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 开启后会在终端显示生成的 SQL 语句，初学者必备
    pool_pre_ping=True,  # 自动检测失效连接
)

# 2. 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# 3. 声明基类，供模型继承
Base = declarative_base()


# 4. 依赖注入函数：每个请求一个 Session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
