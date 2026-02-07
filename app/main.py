from fastapi import FastAPI
from core.database import engine, Base
from api.users import router

# 1. 初始化 FastAPI 实例
app = FastAPI(
    title="My MVP API",
    description="这是一个基于 FastAPI + SQLAlchemy 2.0 的专业项目架构",
    version="1.0.0",
)


# 2. 自动化：启动时检查并创建数据库表
# 在正式生产环境中，通常会改用 Alembic 来管理，但 MVP 阶段这最快
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # 这一行会自动扫描 models.py 里所有的表结构并同步到 MySQL
        await conn.run_sync(Base.metadata.create_all)
    print("🚀 数据库同步完成，服务已就绪！")


# 3. 挂载各个模块的路由
# tags 参数是为了在文档中对接口进行物理分组
app.include_router(router)


# 4. 根路径欢迎接口 (用于健康检查)
@app.get("/", tags=["Root"])
async def root():
    return {"status": "ok", "message": "Welcome to my FastAPI system!"}
