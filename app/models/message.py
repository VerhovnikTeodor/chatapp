from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class AttachmentMediaType(str, enum.Enum):
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_WEBP = "image/webp"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    content = Column(String, nullable=True)
    userId = Column(String, ForeignKey("users.id"), nullable=False)
    chatId = Column(String, ForeignKey("chats.id"), nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")

class MessageAttachment(Base):
    __tablename__ = "message_attachments"

    id = Column(String, primary_key=True, index=True)
    messageId = Column(String, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    mediaType = Column(Enum(AttachmentMediaType, name="attachment_media_type"), nullable=False)

    message = relationship("Message", back_populates="attachments")