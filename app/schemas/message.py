import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MessageRole(str, Enum):
	system = "system"
	user = "user"
	assistant = "assistant"


class MessageStatus(str, Enum):
	processing = "processing"
	success = "success"
	error = "error"


class MessageBase(BaseModel):
	role: MessageRole
	content: str
	extra_data: dict | None = None


class MessageCreate(MessageBase):
	conversation_id: uuid.UUID
	status: MessageStatus = MessageStatus.success


class MessageUpdate(BaseModel):
	content: str | None = None
	status: MessageStatus | None = None
	extra_data: dict | None = None


class MessageOut(MessageBase):
	id: uuid.UUID
	conversation_id: uuid.UUID
	status: MessageStatus
	created_at: datetime

	model_config = {"from_attributes": True}
