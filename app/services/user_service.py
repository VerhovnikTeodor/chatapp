from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
import uuid
from sqlalchemy.exc import IntegrityError
import logging
import bcrypt



def register_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise ValueError("Email already registered")

    p = user.password.encode("utf-8")
    s = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(p, s).decode("utf-8")

    new_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        username=user.username,
        password=hashed_password,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )
    db.add(new_user)
    try:
        db.commit()
        logging.info(f"User registered successfully: {new_user.email}")
    except IntegrityError:
        db.rollback()
        return None

    db.refresh(new_user)
    return new_user

def login_user(db: Session, email: str, entered_password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    entered_password_bytes = entered_password.encode("utf-8")
    stored_hash = user.password if isinstance(user.password, (bytes, bytearray)) else user.password.encode("utf-8")

    if bcrypt.checkpw(entered_password_bytes, stored_hash):
        logging.info(f"Login uspešen: {user.email}")
        return user

    logging.warning(f"Login neuspešen: {user.email}")
    return None
    

def get_all_users(db: Session):
    return db.query(User).all()