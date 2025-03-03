from datetime import datetime
from typing import Optional, List
from beanie import Document, Link
from pydantic import Field
from app.models.user import User
from app.models.game import Game

class Template(Document):
    title: str
    content: str
    category: str
    game: Optional[Link[Game]] = None
    owner: Link[User]
    usage_count: int = 0
    is_public: bool = False
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "templates"
        indexes = [
            "owner",
            "game",
            "category",
            "tags",
            "is_public",
        ]