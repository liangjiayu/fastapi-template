from fastapi import APIRouter

from app.core.database import DB
from app.schemas.response import ApiResponse
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=ApiResponse[UserOut])
async def create_user(user_in: UserCreate, db: DB):
	user = await user_service.create_user(db, user_in)
	return ApiResponse.ok(data=user)


@router.get("/", response_model=ApiResponse[list[UserOut]])
async def get_users(skip: int = 0, limit: int = 100, db: DB = None):
	users = await user_service.get_users(db, skip, limit)
	return ApiResponse.ok(data=users)


@router.get("/{user_id}", response_model=ApiResponse[UserOut])
async def get_user(user_id: int, db: DB):
	user = await user_service.get_user(db, user_id)
	return ApiResponse.ok(data=user)


@router.put("/{user_id}", response_model=ApiResponse[UserOut])
async def update_user(user_id: int, user_in: UserUpdate, db: DB):
	user = await user_service.update_user(db, user_id, user_in)
	return ApiResponse.ok(data=user)


@router.delete("/{user_id}", response_model=ApiResponse[None])
async def delete_user(user_id: int, db: DB):
	await user_service.delete_user(db, user_id)
	return ApiResponse.ok()
