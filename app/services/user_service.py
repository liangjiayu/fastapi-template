from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizException
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


async def create_user(db: AsyncSession, user_in: UserCreate):
	existing = await UserRepository.get_by_username(db, user_in.username)
	if existing:
		raise BizException(code=400, msg="Username already exists")
	return await UserRepository.create(db, user_in)


async def get_user(db: AsyncSession, user_id: int):
	user = await UserRepository.get_by_id(db, user_id)
	if not user:
		raise BizException(code=404, msg="User not found")
	return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
	return await UserRepository.get_list(db, skip, limit)


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate):
	user = await get_user(db, user_id)
	return await UserRepository.update(db, user, user_in)


async def delete_user(db: AsyncSession, user_id: int):
	user = await get_user(db, user_id)
	await UserRepository.delete(db, user)
