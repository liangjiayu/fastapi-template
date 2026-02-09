import uuid

from fastapi import APIRouter

from app.core.database import DB
from app.schemas.conversation import ConversationCreate, ConversationOut, ConversationUpdate
from app.schemas.response import ApiResponse
from app.services import conversation_service

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("/", response_model=ApiResponse[ConversationOut])
async def create_conversation(conversation_in: ConversationCreate, db: DB):
	conversation = await conversation_service.create_conversation(db, conversation_in)
	return ApiResponse.ok(data=conversation)


@router.get("/", response_model=ApiResponse[list[ConversationOut]])
async def get_conversations(user_id: str | None = None, skip: int = 0, limit: int = 100, db: DB = None):
	conversations = await conversation_service.get_conversations(db, user_id, skip, limit)
	return ApiResponse.ok(data=conversations)


@router.get("/{conversation_id}", response_model=ApiResponse[ConversationOut])
async def get_conversation(conversation_id: uuid.UUID, db: DB):
	conversation = await conversation_service.get_conversation(db, conversation_id)
	return ApiResponse.ok(data=conversation)


@router.put("/{conversation_id}", response_model=ApiResponse[ConversationOut])
async def update_conversation(
	conversation_id: uuid.UUID, conversation_in: ConversationUpdate, db: DB
):
	conversation = await conversation_service.update_conversation(db, conversation_id, conversation_in)
	return ApiResponse.ok(data=conversation)


@router.delete("/{conversation_id}", response_model=ApiResponse[None])
async def delete_conversation(conversation_id: uuid.UUID, db: DB):
	await conversation_service.delete_conversation(db, conversation_id)
	return ApiResponse.ok()
