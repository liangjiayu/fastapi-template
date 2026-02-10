from typing import Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class BaseRepository[T: Base]:
	model: type[T]

	@classmethod
	async def get_by_id(cls, db: AsyncSession, id: Any) -> T | None:
		return await db.get(cls.model, id)

	@classmethod
	async def create(cls, db: AsyncSession, create_in: BaseModel) -> T:
		obj = cls.model(**create_in.model_dump())
		db.add(obj)
		await db.commit()
		await db.refresh(obj)
		return obj

	@classmethod
	async def update(cls, db: AsyncSession, obj: T, update_in: BaseModel) -> T:
		for key, value in update_in.model_dump(exclude_unset=True).items():
			setattr(obj, key, value)
		await db.commit()
		await db.refresh(obj)
		return obj

	@classmethod
	async def delete(cls, db: AsyncSession, obj: T) -> None:
		await db.delete(obj)
		await db.commit()
