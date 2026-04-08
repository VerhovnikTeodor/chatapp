from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, User
from app.services.user_service import get_all_users, login_user, register_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = register_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Register failed")
        raise HTTPException(status_code=500, detail="Napaka pri registraciji uporabnika")
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email ali username že obstaja")
    return db_user

@router.post("/login")
def login(password: str, email: str, db: Session = Depends(get_db)):
    try:
        request = login_user(db=db, email=email, entered_password=password)
    except Exception:
        logger.exception("Login failed")
        raise HTTPException(status_code=500, detail="Napaka pri prijavi")
    if request is None:
        raise HTTPException(status_code=400, detail="Napačen email ali geslo")
    return True

@router.get("/users", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    try:
        return get_all_users(db=db)
    except Exception:
        logger.exception("Get users failed")
        raise HTTPException(status_code=500, detail="Napaka pri pridobivanju uporabnikov")