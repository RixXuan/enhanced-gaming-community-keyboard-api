from datetime import datetime
from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field
from app.models.discord import DiscordAccount

class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    discord_account: Optional[DiscordAccount] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
        ]