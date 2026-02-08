from fastapi import APIRouter

from app.api.users import router as user_router

router = APIRouter(prefix="/api")
router.include_router(user_router)
