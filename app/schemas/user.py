from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from app.schemas.discord import DiscordAccountResponse

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_superuser: bool
    discord_account: Optional[DiscordAccountResponse] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class UserInDB(UserResponse):
    hashed_password: str