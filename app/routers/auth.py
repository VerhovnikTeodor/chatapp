from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, User
from app.services.user_service import create_user

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    return db_user
