from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class DiscordAccountBase(BaseModel):
    discord_id: str
    username: str
    discriminator: str
    avatar: Optional[str] = None

class DiscordAccountCreate(DiscordAccountBase):
    access_token: str
    refresh_token: str
    token_expires_at: datetime

class DiscordAccountResponse(DiscordAccountBase):
    id: str
    
    class Config:
        orm_mode = True

class DiscordChannelBase(BaseModel):
    channel_id: str
    server_id: str
    name: str
    type: str
    position: int = 0
    deep_link: str

class DiscordChannelCreate(DiscordChannelBase):
    pass

class DiscordChannelResponse(DiscordChannelBase):
    id: str
    last_accessed: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class DiscordServerBase(BaseModel):
    server_id: str
    name: str
    icon: Optional[str] = None

class DiscordServerCreate(DiscordServerBase):
    channels: List[DiscordChannelCreate] = []

class DiscordServerResponse(DiscordServerBase):
    id: str
    channels: List[DiscordChannelResponse] = []
    
    class Config:
        orm_mode = True