from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import LoginRequest
from app.core.secutiry import create_access_token
router = APIRouter()

@router.post("/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email або пароль"
        )
        
    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "message": "Успішний вхід",
        "token": access_token,
        "user_id": user.id
    }