import uuid
from datetime import datetime

from pydantic import BaseModel


class ConversationBase(BaseModel):
	title: str | None = None
	model_name: str | None = None
	extra_data: dict | None = None


class ConversationCreate(ConversationBase):
	user_id: str


class ConversationUpdate(BaseModel):
	title: str | None = None
	model_name: str | None = None
	extra_data: dict | None = None


class ConversationOut(ConversationBase):
	id: uuid.UUID
	user_id: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}
