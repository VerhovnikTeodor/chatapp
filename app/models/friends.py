from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Friend(Base):
    __tablename__ = "friends"
    __table_args__ = (
        UniqueConstraint("userId", "friendId", name="uq_friend_pair"),
        CheckConstraint('"userId" <> "friendId"', name="ck_no_self_friend"),
    )

    id = Column(String, primary_key=True, index=True)
    userId = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    friendId = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", foreign_keys=[userId])
    friend = relationship("User", foreign_keys=[friendId])