from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, User, UserLogin, LoginResponse
from app.services.user_service import get_all_users, login_user, register_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = register_user(db=db, user=user)
    except ValueError as e:
        raise _error(400, "REGISTER_INVALID", str(e))
    except Exception:
        logger.exception("Register failed")
        raise _error(500, "REGISTER_FAILED", "Napaka pri registraciji uporabnika")
    if db_user is None:
        raise _error(400, "REGISTER_DUPLICATE", "Email ali username že obstaja")
    return db_user

@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        request = login_user(db=db, email=payload.email, entered_password=payload.password)
    except Exception:
        logger.exception("Login failed")
        raise _error(500, "LOGIN_FAILED", "Napaka pri prijavi")
    if request is None:
        raise _error(400, "LOGIN_INVALID", "Napačen email ali geslo")
    return LoginResponse(success=True)

@router.get("/users", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    try:
        return get_all_users(db=db)
    except Exception:
        logger.exception("Get users failed")
        raise _error(500, "USERS_FETCH_FAILED", "Napaka pri pridobivanju uporabnikov")