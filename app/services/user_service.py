from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from schemas.users import UserCreate


# 1. 根据用户名查询用户（用于判断用户是否已存在）
async def get_user_by_username(db: AsyncSession, username: str):
    # 执行异步查询：SELECT * FROM users WHERE username = :username
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


# 2. 创建用户逻辑
async def create_user(db: AsyncSession, user: UserCreate):
    # 关键步骤：目前我们先存明文，下一课加入密码哈希
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,  # 临时存放，待加密
    )

    # 将对象添加到 session
    db.add(db_user)
    # 提交到数据库
    await db.commit()
    # 刷新 db_user，以便获取数据库自动生成的 ID 和 created_at
    await db.refresh(db_user)

    return db_user


# 3. 获取用户列表（带分页功能）
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
