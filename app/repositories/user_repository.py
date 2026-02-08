from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
	@staticmethod
	async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
		return await db.get(User, user_id)

	@staticmethod
	async def get_by_username(db: AsyncSession, username: str) -> User | None:
		result = await db.execute(select(User).where(User.username == username))
		return result.scalars().first()

	@staticmethod
	async def get_list(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
		result = await db.execute(select(User).offset(skip).limit(limit))
		return list(result.scalars().all())

	@staticmethod
	async def create(db: AsyncSession, user_in: UserCreate) -> User:
		user = User(**user_in.model_dump())
		db.add(user)
		await db.commit()
		await db.refresh(user)
		return user

	@staticmethod
	async def update(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
		for key, value in user_in.model_dump(exclude_unset=True).items():
			setattr(user, key, value)
		await db.commit()
		await db.refresh(user)
		return user

	@staticmethod
	async def delete(db: AsyncSession, user: User) -> None:
		await db.delete(user)
		await db.commit()
