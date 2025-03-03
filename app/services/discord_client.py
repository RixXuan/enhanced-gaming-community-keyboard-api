import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.core.config import settings
from app.models.discord import DiscordAccount, DiscordServer, DiscordChannel

class DiscordClient:
    """Discord API 客户端服务"""
    
    @staticmethod
    async def exchange_code(code: str) -> Dict:
        """使用授权码交换访问令牌"""
        async with aiohttp.ClientSession() as session:
            data = {
                'client_id': settings.DISCORD_CLIENT_ID,
                'client_secret': settings.DISCORD_CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': settings.DISCORD_REDIRECT_URI,
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            async with session.post(
                f"{settings.DISCORD_API_BASE}/oauth2/token",
                data=data,
                headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to exchange code: {error_text}")
                return await response.json()
    
    @staticmethod
    async def get_user_info(access_token: str) -> Dict:
        """获取 Discord 用户信息"""
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {access_token}'}
            
            async with session.get(
                f"{settings.DISCORD_API_BASE}/users/@me",
                headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get user info: {error_text}")
                return await response.json()
    
    @staticmethod
    async def get_user_guilds(access_token: str) -> List[Dict]:
        """获取用户所在的服务器"""
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {access_token}'}
            
            async with session.get(
                f"{settings.DISCORD_API_BASE}/users/@me/guilds",
                headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get user guilds: {error_text}")
                return await response.json()
    
    @staticmethod
    async def get_guild_channels(access_token: str, guild_id: str) -> List[Dict]:
        """获取服务器频道"""
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {access_token}'}
            
            async with session.get(
                f"{settings.DISCORD_API_BASE}/guilds/{guild_id}/channels",
                headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get guild channels: {error_text}")
                return await response.json()
    
    @staticmethod
    def create_deep_link(server_id: str, channel_id: str) -> str:
        """创建 Discord 深度链接"""
        return f"discord://discord.com/channels/{server_id}/{channel_id}"
    
    @staticmethod
    async def refresh_discord_token(refresh_token: str) -> Dict:
        """刷新 Discord 访问令牌"""
        async with aiohttp.ClientSession() as session:
            data = {
                'client_id': settings.DISCORD_CLIENT_ID,
                'client_secret': settings.DISCORD_CLIENT_SECRET,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            async with session.post(
                f"{settings.DISCORD_API_BASE}/oauth2/token",
                data=data,
                headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to refresh token: {error_text}")
                return await response.json()