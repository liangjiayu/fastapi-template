import uuid

from fastapi import APIRouter

from app.core.database import DB
from app.schemas.message import MessageCreate, MessageOut, MessageUpdate
from app.schemas.response import ApiResponse, PageData
from app.services import message_service

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=ApiResponse[MessageOut])
async def create_message(message_in: MessageCreate, db: DB):
	message = await message_service.create_message(db, message_in)
	return ApiResponse.ok(data=message)


@router.get("/conversation/{conversation_id}", response_model=ApiResponse[PageData[MessageOut]])
async def get_messages(conversation_id: uuid.UUID, page: int = 1, page_size: int = 20, db: DB = None):
	result = await message_service.get_messages(db, conversation_id, page, page_size)
	return ApiResponse.page(**result)


@router.get("/{message_id}", response_model=ApiResponse[MessageOut])
async def get_message(message_id: uuid.UUID, db: DB):
	message = await message_service.get_message(db, message_id)
	return ApiResponse.ok(data=message)


@router.put("/{message_id}", response_model=ApiResponse[MessageOut])
async def update_message(message_id: uuid.UUID, message_in: MessageUpdate, db: DB):
	message = await message_service.update_message(db, message_id, message_in)
	return ApiResponse.ok(data=message)


@router.delete("/{message_id}", response_model=ApiResponse[None])
async def delete_message(message_id: uuid.UUID, db: DB):
	await message_service.delete_message(db, message_id)
	return ApiResponse.ok()
