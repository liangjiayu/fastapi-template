import uuid
from datetime import datetime

from sqlalchemy import JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Conversation(Base):
	__tablename__ = "conversations"

	id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
	user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
	title: Mapped[str | None] = mapped_column(String(255), nullable=True)
	model_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
	extra_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

	messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
