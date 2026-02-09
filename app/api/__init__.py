from fastapi import APIRouter

from app.api.conversations import router as conversation_router
from app.api.messages import router as message_router
from app.api.users import router as user_router

router = APIRouter(prefix="/api")
router.include_router(user_router)
router.include_router(conversation_router)
router.include_router(message_router)
