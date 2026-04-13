from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


chat_members = Table(
    "chat_members",
    Base.metadata,
    Column("chat_id", String, ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    users = relationship("User", secondary=chat_members, back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
