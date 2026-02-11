import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizException
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import ConversationCreate, ConversationUpdate


async def create_conversation(db: AsyncSession, conversation_in: ConversationCreate):
	return await ConversationRepository.create(db, conversation_in)


async def get_conversation(db: AsyncSession, conversation_id: uuid.UUID):
	conversation = await ConversationRepository.get_by_id(db, conversation_id)
	if not conversation:
		raise BizException(code=404, msg="Conversation not found")
	return conversation


async def get_conversations(db: AsyncSession, user_id: str | None = None, page: int = 1, page_size: int = 20):
	offset = (page - 1) * page_size
	conversations = await ConversationRepository.get_list(db, user_id, offset, page_size)
	total = await ConversationRepository.get_count(db, user_id)
	return {"list": conversations, "total": total, "page": page, "page_size": page_size}


async def update_conversation(db: AsyncSession, conversation_id: uuid.UUID, conversation_in: ConversationUpdate):
	conversation = await get_conversation(db, conversation_id)
	return await ConversationRepository.update(db, conversation, conversation_in)


async def delete_conversation(db: AsyncSession, conversation_id: uuid.UUID):
	conversation = await get_conversation(db, conversation_id)
	await ConversationRepository.delete(db, conversation)
