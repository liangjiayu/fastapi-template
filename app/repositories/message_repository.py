import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate


class MessageRepository:
	@staticmethod
	async def get_by_id(db: AsyncSession, message_id: uuid.UUID) -> Message | None:
		return await db.get(Message, message_id)

	@staticmethod
	async def get_list_by_conversation_id(
		db: AsyncSession, conversation_id: uuid.UUID, skip: int = 0, limit: int = 100
	) -> list[Message]:
		result = await db.execute(
			select(Message)
			.where(Message.conversation_id == conversation_id)
			.order_by(Message.created_at.asc())
			.offset(skip)
			.limit(limit)
		)
		return list(result.scalars().all())

	@staticmethod
	async def create(db: AsyncSession, message_in: MessageCreate) -> Message:
		message = Message(**message_in.model_dump())
		db.add(message)
		await db.commit()
		await db.refresh(message)
		return message

	@staticmethod
	async def update(db: AsyncSession, message: Message, message_in: MessageUpdate) -> Message:
		for key, value in message_in.model_dump(exclude_unset=True).items():
			setattr(message, key, value)
		await db.commit()
		await db.refresh(message)
		return message

	@staticmethod
	async def delete(db: AsyncSession, message: Message) -> None:
		await db.delete(message)
		await db.commit()
