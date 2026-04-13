from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):
    name: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    name: Optional[str] = None


class Chat(ChatBase):
    id: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
