from sqlalchemy.orm import Session
from app.models.friends import Friend
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
    return db.query(Friend).filter((Friend.userId == user_id) | (Friend.friendId == user_id)).all()


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

    update_data = payload.model_dump(exclude_unset=True)

    next_user_id = update_data.get("userId", db_friendship.userId)
    next_friend_id = update_data.get("friendId", db_friendship.friendId)
    normalized_user_id, normalized_friend_id = _normalize_friend_pair(next_user_id, next_friend_id)

    db_friendship.userId = normalized_user_id
    db_friendship.friendId = normalized_friend_id

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
