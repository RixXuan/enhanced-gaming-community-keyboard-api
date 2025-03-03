from typing import List, Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FlorisBoard Enhancement API"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "florisboard_db"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Discord
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI: str
    DISCORD_API_BASE: str = "https://discord.com/api/v10"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()