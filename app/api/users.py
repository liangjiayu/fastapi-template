from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
	return await user_service.create_user(db, user_in)


@router.get("/", response_model=list[UserOut])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
	return await user_service.get_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
	return await user_service.get_user(db, user_id)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
	return await user_service.update_user(db, user_id, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
	await user_service.delete_user(db, user_id)
