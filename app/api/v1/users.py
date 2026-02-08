from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.database import get_db
from models.user import User
from schemas.user import UserCreate, UserOut  # 假设你已定义这些 Pydantic 模型

router = APIRouter(prefix="/users", tags=["Users"])


# 1. Create - 创建用户
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 检查用户是否已存在 (最简逻辑)
    new_user = User(**user_in.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# 2. Read All - 获取用户列表
@router.get("/", response_model=List[UserOut])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


# 3. Read One - 获取特定用户
@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 4. Update - 更新用户 (简单更新名称)
@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int, user_in: UserCreate, db: AsyncSession = Depends(get_db)
):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 动态更新字段
    for key, value in user_in.model_dump().items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


# 5. Delete - 删除用户
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()
    return None
