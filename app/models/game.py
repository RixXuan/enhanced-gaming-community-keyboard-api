from beanie import Document
from typing import Optional, List
from pydantic import Field
from datetime import datetime

class Game(Document):
    name: str
    package_name: str  # Android 包名，用于识别
    icon_url: Optional[str] = None
    description: Optional[str] = None
    input_contexts: List[str] = []  # 匹配输入框的上下文特征
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "games"
        indexes = [
            "package_name",
        ]