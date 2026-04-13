import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.friends import FriendCreate, FriendUpdate, Friend as FriendSchema
from app.services.friends_service import (
    get_friendships,
    get_friendship_by_id,
    get_user_friendships,
    create_friendship,
    update_friendship,
    delete_friendship,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


@router.get("/", response_model=list[FriendSchema])
def list_friendships(db: Session = Depends(get_db)):
    try:
        return get_friendships(db)
    except Exception:
        logger.exception("List friendships failed")
        raise _error(500, "FRIENDS_FETCH_FAILED", "Napaka pri pridobivanju prijateljstev")


@router.get("/{friendship_id}", response_model=FriendSchema)
def get_friendship(friendship_id: str, db: Session = Depends(get_db)):
    try:
        friendship = get_friendship_by_id(db, friendship_id)
    except Exception:
        logger.exception("Get friendship failed")
        raise _error(500, "FRIEND_FETCH_FAILED", "Napaka pri pridobivanju prijateljstva")

    if not friendship:
        raise _error(404, "FRIENDSHIP_NOT_FOUND", "Friendship not found")
    return friendship


@router.get("/user/{user_id}", response_model=list[FriendSchema])
def list_user_friendships(user_id: str, db: Session = Depends(get_db)):
    try:
        return get_user_friendships(db, user_id)
    except Exception:
        logger.exception("List user friendships failed")
        raise _error(500, "USER_FRIENDS_FETCH_FAILED", "Napaka pri pridobivanju uporabnikovih prijateljstev")


@router.post("/", response_model=FriendSchema)
def post_friendship(payload: FriendCreate, db: Session = Depends(get_db)):
    try:
        friendship = create_friendship(db, payload)
    except ValueError as exc:
        raise _error(400, "FRIENDSHIP_INVALID", str(exc))
    except Exception:
        logger.exception("Create friendship failed")
        raise _error(500, "FRIENDSHIP_CREATE_FAILED", "Napaka pri ustvarjanju prijateljstva")

    if friendship is None:
        raise _error(400, "FRIENDSHIP_CONFLICT", "Prijateljstvo že obstaja ali ni veljavno")
    return friendship


@router.put("/{friendship_id}", response_model=FriendSchema)
def put_friendship(friendship_id: str, payload: FriendUpdate, db: Session = Depends(get_db)):
    try:
        friendship = update_friendship(db, friendship_id, payload)
    except ValueError as exc:
        raise _error(400, "FRIENDSHIP_INVALID", str(exc))
    except Exception:
        logger.exception("Update friendship failed")
        raise _error(500, "FRIENDSHIP_UPDATE_FAILED", "Napaka pri posodobitvi prijateljstva")

    if friendship is None:
        raise _error(404, "FRIENDSHIP_NOT_FOUND", "Friendship not found ali konflikt")
    return friendship


@router.delete("/{friendship_id}", response_model=FriendSchema)
def remove_friendship(friendship_id: str, db: Session = Depends(get_db)):
    try:
        friendship = delete_friendship(db, friendship_id)
    except Exception:
        logger.exception("Delete friendship failed")
        raise _error(500, "FRIENDSHIP_DELETE_FAILED", "Napaka pri brisanju prijateljstva")

    if not friendship:
        raise _error(404, "FRIENDSHIP_NOT_FOUND", "Friendship not found")
    return friendship
