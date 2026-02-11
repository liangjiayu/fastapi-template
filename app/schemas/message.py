import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
	system = "system"
	user = "user"
	assistant = "assistant"


class MessageStatus(StrEnum):
	processing = "processing"
	success = "success"
	error = "error"


class MessageBase(BaseModel):
	role: MessageRole = Field(description="消息角色：system / user / assistant")
	content: str = Field(description="消息内容")
	extra_data: dict | None = Field(None, description="扩展数据，如思考过程、token 用量等")


class MessageCreate(MessageBase):
	conversation_id: uuid.UUID = Field(description="所属会话 ID")
	status: MessageStatus = Field(MessageStatus.success, description="消息状态：processing / success / error")


class MessageUpdate(BaseModel):
	content: str | None = Field(None, description="消息内容")
	status: MessageStatus | None = Field(None, description="消息状态：processing / success / error")
	extra_data: dict | None = Field(None, description="扩展数据，如思考过程、token 用量等")


class MessageOut(MessageBase):
	id: uuid.UUID = Field(description="消息 ID")
	conversation_id: uuid.UUID = Field(description="所属会话 ID")
	status: MessageStatus = Field(description="消息状态：processing / success / error")
	created_at: datetime = Field(description="创建时间")

	model_config = {"from_attributes": True}
