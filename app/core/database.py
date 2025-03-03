from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.user import User
from app.models.template import Template
from app.models.game import Game
from app.models.discord import DiscordServer, DiscordChannel

async def init_db():
    """初始化数据库连接"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[
            User,
            Template,
            Game,
            DiscordServer,
            DiscordChannel,
        ]
    )