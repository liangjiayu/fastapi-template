import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository):
	model = Message

	@staticmethod
	async def get_list_by_conversation_id(
		db: AsyncSession, conversation_id: uuid.UUID, offset: int = 0, limit: int = 100
	) -> list[Message]:
		result = await db.execute(
			select(Message)
			.where(Message.conversation_id == conversation_id)
			.order_by(Message.created_at.asc())
			.offset(offset)
			.limit(limit)
		)
		return list(result.scalars().all())

	@staticmethod
	async def get_count_by_conversation_id(db: AsyncSession, conversation_id: uuid.UUID) -> int:
		result = await db.execute(
			select(func.count()).select_from(Message).where(Message.conversation_id == conversation_id)
		)
		return result.scalar_one()
