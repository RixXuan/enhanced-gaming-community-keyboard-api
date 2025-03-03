from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class GameBase(BaseModel):
    name: str
    package_name: str
    icon_url: Optional[str] = None
    description: Optional[str] = None
    input_contexts: List[str] = []

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    name: Optional[str] = None
    icon_url: Optional[str] = None
    description: Optional[str] = None
    input_contexts: Optional[List[str]] = None

class GameResponse(GameBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True