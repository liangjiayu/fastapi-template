from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas.users import UserOut, UserCreate
from core.database import get_db
from services.user_service import create_user, get_users, get_user_by_username

# 1. 初始化路由器
# prefix: 该模块下所有接口都会带上 /users 前缀
# tags: 在 Swagger 文档中自动归类
router = APIRouter(prefix="/users", tags=["用户管理"])


# 2. 接口 A：用户注册 (POST)
@router.post("/", response_model=UserOut)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 第一步：检查用户名是否被占用
    existing_user = await get_user_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已被注册")

    # 第二步：调用 CRUD 执行写入
    return await create_user(db=db, user=user_in)


# 3. 接口 B：获取用户列表 (GET)
@router.get("/", response_model=List[UserOut])
async def list_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    users = await get_users(db, skip=skip, limit=limit)
    return users
