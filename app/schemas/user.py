from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)