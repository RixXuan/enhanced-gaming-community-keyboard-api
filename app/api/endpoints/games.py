from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, get_current_active_superuser
from app.crud.game import game
from app.models.game import Game
from app.models.user import User
from app.schemas.game import GameCreate, GameUpdate, GameResponse

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/", response_model=List[GameResponse])
async def read_games(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """
    获取所有支持的游戏
    """
    games = await game.get_multi(skip=skip, limit=limit)
    return games

@router.post("/", response_model=GameResponse)
async def create_game(
    game_in: GameCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """
    创建新游戏（需要管理员权限）
    """
    existing_game = await game.get_by_package_name(package_name=game_in.package_name)
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game with this package name already exists"
        )
    
    return await game.create(obj_in=game_in)

@router.get("/{game_id}", response_model=GameResponse)
async def read_game(
    game_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    通过 ID 获取特定游戏
    """
    found_game = await game.get(id=game_id)
    if not found_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return found_game

@router.put("/{game_id}", response_model=GameResponse)
async def update_game(
    game_id: str,
    game_in: GameUpdate,
    current_user: User = Depends(get_current_active_superuser)
):
    """
    更新游戏（需要管理员权限）
    """
    found_game = await game.get(id=game_id)
    if not found_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return await game.update(db_obj=found_game, obj_in=game_in)

@router.get("/package/{package_name}", response_model=GameResponse)
async def read_game_by_package(
    package_name: str,
    current_user: User = Depends(get_current_user)
):
    """
    通过包名获取游戏
    """
    found_game = await game.get_by_package_name(package_name=package_name)
    if not found_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return found_game

@router.post("/contexts")
async def report_game_context(
    package_name: str,
    context: str,
    current_user: User = Depends(get_current_user)
):
    """
    上报游戏上下文信息（用于改进识别）
    """
    found_game = await game.get_by_package_name(package_name=package_name)
    
    # 如果游戏不存在，创建记录（为将来的支持）
    if not found_game:
        found_game = await game.create(
            obj_in=GameCreate(
                name=f"Unknown Game ({package_name})",
                package_name=package_name,
                input_contexts=[context]
            )
        )
    # 如果游戏存在但上下文不在列表中，添加它
    elif context not in found_game.input_contexts:
        found_game.input_contexts.append(context)
        await found_game.save()
    
    return {"success": True, "game_id": str(found_game.id)}