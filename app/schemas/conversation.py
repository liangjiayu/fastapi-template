import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ConversationBase(BaseModel):
	title: str | None = Field(None, description="会话标题")
	model_name: str | None = Field(None, description="模型名称")
	extra_data: dict | None = Field(None, description="扩展数据，如模型配置 temperature、top_p 等")


class ConversationCreate(ConversationBase):
	user_id: str = Field(description="用户标识")


class ConversationUpdate(BaseModel):
	title: str | None = Field(None, description="会话标题")
	model_name: str | None = Field(None, description="模型名称")
	extra_data: dict | None = Field(None, description="扩展数据，如模型配置 temperature、top_p 等")


class ConversationOut(ConversationBase):
	id: uuid.UUID = Field(description="会话 ID")
	user_id: str = Field(description="用户标识")
	created_at: datetime = Field(description="创建时间")
	updated_at: datetime = Field(description="更新时间")

	model_config = {"from_attributes": True}
