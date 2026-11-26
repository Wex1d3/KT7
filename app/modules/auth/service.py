from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

def register_user(data: UserCreate, db: Session) -> User:
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(email: str, password: str, db: Session) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return create_access_token(str(user.id))
