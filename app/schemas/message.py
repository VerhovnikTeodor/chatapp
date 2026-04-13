from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AttachmentMediaType(str, Enum):
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_WEBP = "image/webp"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class MessageAttachmentBase(BaseModel):
    url: str
    mediaType: AttachmentMediaType


class MessageAttachmentCreate(MessageAttachmentBase):
    pass


class MessageAttachmentUpdate(BaseModel):
    url: Optional[str] = None
    mediaType: Optional[AttachmentMediaType] = None


class MessageAttachment(MessageAttachmentBase):
    id: str
    messageId: str

    model_config = ConfigDict(from_attributes=True)


class MessageBase(BaseModel):
    content: Optional[str] = None
    userId: str
    chatId: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    userId: Optional[str] = None
    chatId: Optional[str] = None


class Message(MessageBase):
    id: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    attachments: list[MessageAttachment] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
