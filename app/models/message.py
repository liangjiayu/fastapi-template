import uuid
from datetime import datetime

from sqlalchemy import JSON, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Message(Base):
	__tablename__ = "messages"

	id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
	conversation_id: Mapped[uuid.UUID] = mapped_column(
		ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
	)
	role: Mapped[str] = mapped_column(String(20), nullable=False)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	status: Mapped[str] = mapped_column(String(20), default="success")
	extra_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())

	conversation = relationship("Conversation", back_populates="messages")
