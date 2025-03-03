from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_current_user
from app.models.user import User
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.services.template_service import TemplateService

router = APIRouter(prefix="/templates", tags=["templates"])

@router.get("/", response_model=List[TemplateResponse])
async def get_templates(
    game: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """获取用户的模板列表"""
    templates = await TemplateService.get_templates_for_user(
        user_id=str(current_user.id),
        game_id=game,
        category=category,
        skip=skip,
        limit=limit
    )
    return templates

@router.post("/", response_model=TemplateResponse)
async def create_template(
    template_in: TemplateCreate,
    current_user: User = Depends(get_current_user)
):
    """创建新模板"""
    template = Template(
        title=template_in.title,
        content=template_in.content,
        category=template_in.category,
        owner=current_user,
        tags=template_in.tags,
        is_public=template_in.is_public
    )
    
    if template_in.game_id:
        from app.models.game import Game
        game = await Game.get(template_in.game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        template.game = game
    
    await template.insert()
    return template

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str,
    current_user: User = Depends(get_current_user)
):
    """获取特定模板"""
    template = await Template.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # 检查权限
    if str(template.owner.id) != str(current_user.id) and not template.is_public:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return template

@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    template_in: TemplateUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新模板"""
    template = await Template.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # 检查权限
    if str(template.owner.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # 更新字段
    update_data = template_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(template, key, value)
    
    template.updated_at = datetime.utcnow()
    await template.save()
    return template

@router.delete("/{template_id}")
async def delete_template(
    template_id: str,
    current_user: User = Depends(get_current_user)
):
    """删除模板"""
    template = await Template.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # 检查权限
    if str(template.owner.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await template.delete()
    return {"success": True}

@router.get("/game/{package_name}", response_model=List[TemplateResponse])
async def get_templates_by_game(
    package_name: str,
    current_user: User = Depends(get_current_user)
):
    """通过游戏包名获取模板"""
    templates = await TemplateService.get_templates_for_game(
        package_name=package_name,
        user_id=str(current_user.id)
    )
    return templates