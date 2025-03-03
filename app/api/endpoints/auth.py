from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token
from app.crud.user import user
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.discord_client import DiscordClient
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 兼容的令牌登录
    """
    authenticated_user = await user.authenticate(email=form_data.username, password=form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active(authenticated_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=str(authenticated_user.id), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserResponse)
async def register_user(user_in: UserCreate):
    """
    创建新用户
    """
    existing_user = await user.get_by_email(email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = await user.create(obj_in=user_in)
    return new_user

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户
    """
    return current_user

@router.post("/discord/authorize")
async def discord_authorize():
    """
    生成 Discord 授权 URL
    """
    authorize_url = (
        f"{settings.DISCORD_API_BASE}/oauth2/authorize"
        f"?client_id={settings.DISCORD_CLIENT_ID}"
        f"&redirect_uri={settings.DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify%20guilds"
    )
    return {"authorize_url": authorize_url}

@router.get("/discord/callback", response_model=Token)
async def discord_callback(
    code: str,
    current_user: User = Depends(get_current_user)
):
    """
    处理 Discord 授权回调
    """
    try:
        # 交换授权码获取访问令牌
        token_data = await DiscordClient.exchange_code(code)
        
        # 获取 Discord 用户信息
        user_info = await DiscordClient.get_user_info(token_data["access_token"])
        
        # 创建 Discord 账号
        from app.models.discord import DiscordAccount
        discord_account = DiscordAccount(
            discord_id=user_info["id"],
            username=user_info["username"],
            discriminator=user_info["discriminator"],
            avatar=user_info.get("avatar"),
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            token_expires_at=datetime.utcnow() + timedelta(seconds=token_data["expires_in"])
        )
        
        # 更新用户的 Discord 账号
        current_user.discord_account = discord_account
        await current_user.save()
        
        # 返回相同的访问令牌
        return {
            "access_token": create_access_token(
                subject=str(current_user.id),
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            ),
            "token_type": "bearer",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to authenticate with Discord: {str(e)}"
        )