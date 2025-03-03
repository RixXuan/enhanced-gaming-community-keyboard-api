from datetime import datetime
from typing import List, Optional
from beanie import Document
from pydantic import Field

class DiscordAccount(Document):
    discord_id: str
    username: str
    discriminator: str
    avatar: Optional[str] = None
    access_token: str
    refresh_token: str
    token_expires_at: datetime
    
    class Settings:
        name = "discord_accounts"
        indexes = [
            "discord_id",
        ]

class DiscordChannel(Document):
    channel_id: str
    server_id: str
    name: str
    type: str
    position: int = 0
    deep_link: str
    last_accessed: Optional[datetime] = None
    
    class Settings:
        name = "discord_channels"
        indexes = [
            "channel_id",
            "server_id",
        ]

class DiscordServer(Document):
    server_id: str
    name: str
    icon: Optional[str] = None
    channels: List[DiscordChannel] = []
    
    class Settings:
        name = "discord_servers"
        indexes = [
            "server_id",
        ]