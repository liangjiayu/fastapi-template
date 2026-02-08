from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


async def create_user(db: AsyncSession, user_in: UserCreate):
	existing = await UserRepository.get_by_username(db, user_in.username)
	if existing:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Username already exists",
		)
	return await UserRepository.create(db, user_in)


async def get_user(db: AsyncSession, user_id: int):
	user = await UserRepository.get_by_id(db, user_id)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
	return await UserRepository.get_list(db, skip, limit)


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate):
	user = await get_user(db, user_id)
	return await UserRepository.update(db, user, user_in)


async def delete_user(db: AsyncSession, user_id: int):
	user = await get_user(db, user_id)
	await UserRepository.delete(db, user)
