from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.database import get_db
from models.user import User
from schemas.user import UserCreate, UserOut
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing_user = await repo.get_user_by_username(user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already registered"
        )
    return await repo.create_user(user_in)


@router.get("/", response_model=List[UserOut])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return await repo.get_users(skip, limit)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    db_user = await repo.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    db_user = await repo.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return await repo.update_user(db_user, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    db_user = await repo.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await repo.delete_user(db_user)
    return None
