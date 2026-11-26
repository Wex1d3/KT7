from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.modules.auth.schemas import UserCreate, UserOut
from app.modules.auth.service import register_user, authenticate_user
from app.modules.auth.models import User
from app.main_limiter import limiter

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return register_user(data, db)

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = authenticate_user(form.username, form.password, db)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user

@router.get("/admin-only")
def admin_only(user: User = Depends(require_admin)):
    return {"message": "Welcome, admin", "email": user.email}
