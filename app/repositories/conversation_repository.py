from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository):
	model = Conversation

	@staticmethod
	async def get_list(
		db: AsyncSession, user_id: str | None = None, offset: int = 0, limit: int = 100
	) -> list[Conversation]:
		stmt = select(Conversation)
		if user_id is not None:
			stmt = stmt.where(Conversation.user_id == user_id)
		result = await db.execute(stmt.order_by(Conversation.updated_at.desc()).offset(offset).limit(limit))
		return list(result.scalars().all())

	@staticmethod
	async def get_count(db: AsyncSession, user_id: str | None = None) -> int:
		stmt = select(func.count()).select_from(Conversation)
		if user_id is not None:
			stmt = stmt.where(Conversation.user_id == user_id)
		result = await db.execute(stmt)
		return result.scalar_one()
