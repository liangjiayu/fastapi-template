import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizException
from app.repositories.message_repository import MessageRepository
from app.schemas.message import MessageCreate, MessageUpdate
from app.services.conversation_service import get_conversation


async def create_message(db: AsyncSession, message_in: MessageCreate):
	await get_conversation(db, message_in.conversation_id)
	return await MessageRepository.create(db, message_in)


async def get_message(db: AsyncSession, message_id: uuid.UUID):
	message = await MessageRepository.get_by_id(db, message_id)
	if not message:
		raise BizException(code=404, msg="Message not found")
	return message


async def get_messages(db: AsyncSession, conversation_id: uuid.UUID, page: int = 1, page_size: int = 20):
	await get_conversation(db, conversation_id)
	offset = (page - 1) * page_size
	messages = await MessageRepository.get_list_by_conversation_id(db, conversation_id, offset, page_size)
	total = await MessageRepository.get_count_by_conversation_id(db, conversation_id)
	return {"list": messages, "total": total, "page": page, "page_size": page_size}


async def update_message(db: AsyncSession, message_id: uuid.UUID, message_in: MessageUpdate):
	message = await get_message(db, message_id)
	return await MessageRepository.update(db, message, message_in)


async def delete_message(db: AsyncSession, message_id: uuid.UUID):
	message = await get_message(db, message_id)
	await MessageRepository.delete(db, message)
