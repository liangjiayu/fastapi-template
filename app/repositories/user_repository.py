from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
	model = User

	@classmethod
	async def get_by_username(cls, db: AsyncSession, username: str) -> User | None:
		result = await db.execute(select(User).where(User.username == username))
		return result.scalars().first()

	@classmethod
	async def get_list(cls, db: AsyncSession, offset: int = 0, limit: int = 100) -> list[User]:
		result = await db.execute(select(User).offset(offset).limit(limit))
		return list(result.scalars().all())

	@classmethod
	async def get_count(cls, db: AsyncSession) -> int:
		result = await db.execute(select(func.count()).select_from(User))
		return result.scalar_one()
