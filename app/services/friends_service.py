from datetime import datetime, timezone

from sqlalchemy.orm import Session
from app.models.friends import Friend, FriendshipStatus
from app.schemas.friends import FriendCreate, FriendUpdate
from sqlalchemy.exc import IntegrityError
import uuid


def _normalize_friend_pair(user_id: str, friend_id: str) -> tuple[str, str]:
    if user_id == friend_id:
        raise ValueError("User cannot be friend with self")
    return (user_id, friend_id) if user_id < friend_id else (friend_id, user_id)


def get_friendships(db: Session):
    return db.query(Friend).all()


def get_friendship_by_id(db: Session, friendship_id: str):
    return db.query(Friend).filter(Friend.id == friendship_id).first()


def get_user_friendships(db: Session, user_id: str):
    return (
        db.query(Friend)
        .filter(
            ((Friend.userId == user_id) | (Friend.friendId == user_id))
            & (Friend.status == FriendshipStatus.accepted)
        )
        .all()
    )


def get_user_friend_requests(db: Session, user_id: str):
    return (
        db.query(Friend)
        .filter(Friend.friendId == user_id, Friend.status == FriendshipStatus.pending)
        .all()
    )


def create_friendship(db: Session, payload: FriendCreate):
    user_id, friend_id = _normalize_friend_pair(payload.userId, payload.friendId)

    existing = (
        db.query(Friend)
        .filter(Friend.userId == user_id, Friend.friendId == friend_id)
        .first()
    )
    if existing:
        return existing

    new_friendship = Friend(
        id=str(uuid.uuid4()),
        userId=user_id,
        friendId=friend_id,
        status=FriendshipStatus.pending,
    )
    db.add(new_friendship)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None

    db.refresh(new_friendship)
    return new_friendship


def update_friendship(db: Session, friendship_id: str, payload: FriendUpdate):
    db_friendship = get_friendship_by_id(db, friendship_id)
    if not db_friendship:
        return None

    if db_friendship.status != payload.status:
        db_friendship.status = payload.status
        if payload.status in {
            FriendshipStatus.accepted,
            FriendshipStatus.rejected,
            FriendshipStatus.blocked,
        }:
            db_friendship.respondedAt = datetime.now(timezone.utc)
        else:
            db_friendship.respondedAt = None

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None

    db.refresh(db_friendship)
    return db_friendship


def delete_friendship(db: Session, friendship_id: str):
    db_friendship = get_friendship_by_id(db, friendship_id)
    if not db_friendship:
        return None

    db.delete(db_friendship)
    db.commit()
    return db_friendship


def respond_to_friend_request(db: Session, friendship_id: str, status: FriendshipStatus):
    if status not in {FriendshipStatus.accepted, FriendshipStatus.rejected, FriendshipStatus.blocked}:
        raise ValueError("Invalid friend request response status")

    db_friendship = get_friendship_by_id(db, friendship_id)
    if not db_friendship:
        return None

    db_friendship.status = status
    db_friendship.respondedAt = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_friendship)
    return db_friendship
