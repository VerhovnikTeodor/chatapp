from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FriendBase(BaseModel):
    userId: str
    friendId: str


class FriendCreate(FriendBase):
    pass


class FriendUpdate(BaseModel):
    userId: Optional[str] = None
    friendId: Optional[str] = None


class Friend(FriendBase):
    id: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
