from pydantic import BaseModel, Field


class UserBase(BaseModel):
	username: str = Field(description="用户名，唯一")
	email: str = Field(description="邮箱，唯一")


class UserCreate(UserBase):
	pass


class UserUpdate(BaseModel):
	username: str | None = Field(None, description="用户名，唯一")
	email: str | None = Field(None, description="邮箱，唯一")


class UserOut(UserBase):
	id: int = Field(description="用户 ID")

	model_config = {"from_attributes": True}
