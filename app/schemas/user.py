from pydantic import BaseModel


class UserBase(BaseModel):
	username: str
	email: str


class UserCreate(UserBase):
	pass


class UserUpdate(BaseModel):
	username: str | None = None
	email: str | None = None


class UserOut(UserBase):
	id: int

	model_config = {"from_attributes": True}
