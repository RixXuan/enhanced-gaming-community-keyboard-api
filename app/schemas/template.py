from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.game import GameResponse

class TemplateBase(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str] = []
    is_public: bool = False

class TemplateCreate(TemplateBase):
    game_id: Optional[str] = None

class TemplateUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None

class TemplateResponse(TemplateBase):
    id: str
    game: Optional[GameResponse] = None
    owner_id: str
    usage_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True