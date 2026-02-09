import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationUpdate


class ConversationRepository:
	@staticmethod
	async def get_by_id(db: AsyncSession, conversation_id: uuid.UUID) -> Conversation | None:
		return await db.get(Conversation, conversation_id)

	@staticmethod
	async def get_list(
		db: AsyncSession, user_id: str | None = None, skip: int = 0, limit: int = 100
	) -> list[Conversation]:
		stmt = select(Conversation)
		if user_id is not None:
			stmt = stmt.where(Conversation.user_id == user_id)
		result = await db.execute(
			stmt.order_by(Conversation.updated_at.desc()).offset(skip).limit(limit)
		)
		return list(result.scalars().all())

	@staticmethod
	async def create(db: AsyncSession, conversation_in: ConversationCreate) -> Conversation:
		conversation = Conversation(**conversation_in.model_dump())
		db.add(conversation)
		await db.commit()
		await db.refresh(conversation)
		return conversation

	@staticmethod
	async def update(
		db: AsyncSession, conversation: Conversation, conversation_in: ConversationUpdate
	) -> Conversation:
		for key, value in conversation_in.model_dump(exclude_unset=True).items():
			setattr(conversation, key, value)
		await db.commit()
		await db.refresh(conversation)
		return conversation

	@staticmethod
	async def delete(db: AsyncSession, conversation: Conversation) -> None:
		await db.delete(conversation)
		await db.commit()
