from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_current_user
from app.models.user import User
from app.models.discord import DiscordServer, DiscordChannel
from app.schemas.discord import DiscordServerResponse, DiscordChannelResponse
from app.services.discord_client import DiscordClient

router = APIRouter(prefix="/discord", tags=["discord"])

@router.get("/servers", response_model=List[DiscordServerResponse])
async def get_discord_servers(
    current_user: User = Depends(get_current_user)
):
    """获取用户的 Discord 服务器列表"""
    if not current_user.discord_account:
        raise HTTPException(status_code=400, detail="Discord account not linked")
    
    # 检查令牌是否过期
    if current_user.discord_account.token_expires_at < datetime.utcnow():
        try:
            # 刷新令牌
            token_data = await DiscordClient.refresh_discord_token(
                current_user.discord_account.refresh_token
            )
            # 更新令牌
            current_user.discord_account.access_token = token_data["access_token"]
            current_user.discord_account.refresh_token = token_data["refresh_token"]
            current_user.discord_account.token_expires_at = datetime.utcnow() + timedelta(seconds=token_data["expires_in"])
            await current_user.save()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to refresh Discord token: {str(e)}")
    
    try:
        # 获取服务器列表
        guilds = await DiscordClient.get_user_guilds(current_user.discord_account.access_token)
        
        servers = []
        for guild in guilds:
            # 获取频道列表
            channels = await DiscordClient.get_guild_channels(
                current_user.discord_account.access_token,
                guild["id"]
            )
            
            # 过滤出文本频道
            text_channels = [
                DiscordChannel(
                    channel_id=channel["id"],
                    server_id=guild["id"],
                    name=channel["name"],
                    type=channel["type"],
                    position=channel.get("position", 0),
                    deep_link=DiscordClient.create_deep_link(guild["id"], channel["id"])
                )
                for channel in channels
                if channel["type"] == 0  # 0 表示文本频道
            ]
            
            server = DiscordServer(
                server_id=guild["id"],
                name=guild["name"],
                icon=guild.get("icon"),
                channels=text_channels
            )
            servers.append(server)
        
        return servers
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get Discord servers: {str(e)}")

@router.get("/deeplinks", response_model=List[DiscordChannelResponse])
async def get_discord_deeplinks(
    current_user: User = Depends(get_current_user),
    limit: int = 10
):
    """获取用户最近使用的 Discord 频道链接"""
    if not current_user.discord_account:
        raise HTTPException(status_code=400, detail="Discord account not linked")
    
    # 获取最近访问的频道
    channels = await DiscordChannel.find().sort(
        -DiscordChannel.last_accessed
    ).limit(limit).to_list()
    
    return channels

@router.post("/channel/access", response_model=DiscordChannelResponse)
async def record_channel_access(
    channel_id: str,
    current_user: User = Depends(get_current_user)
):
    """记录频道访问"""
    if not current_user.discord_account:
        raise HTTPException(status_code=400, detail="Discord account not linked")
    
    channel = await DiscordChannel.find_one(DiscordChannel.channel_id == channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # 更新访问时间
    channel.last_accessed = datetime.utcnow()
    await channel.save()
    
    return channel