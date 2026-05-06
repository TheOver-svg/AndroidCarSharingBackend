from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    
    class Config:
        from_attributes = True
        
class LoginRequest(BaseModel):
    email: str
    password: str