from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.chat import chat_members
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    chats = relationship("Chat", secondary=chat_members, back_populates="users")
    messages = relationship("Message", back_populates  ="user")
    
    sent_friendships = relationship("Friend", foreign_keys="Friend.userId")
    received_friendships = relationship("Friend", foreign_keys="Friend.friendId")