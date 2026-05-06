from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email вже існує!")
    
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user