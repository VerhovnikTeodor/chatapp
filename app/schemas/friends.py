from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FriendshipStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    blocked = "blocked"


class FriendBase(BaseModel):
    userId: str
    friendId: str


class FriendCreate(FriendBase):
    pass


class FriendUpdate(BaseModel):
    status: FriendshipStatus


class FriendStatusUpdate(BaseModel):
    status: FriendshipStatus


class Friend(FriendBase):
    id: str
    status: FriendshipStatus
    respondedAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
