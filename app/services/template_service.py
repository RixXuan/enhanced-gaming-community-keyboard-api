from typing import List, Optional
from beanie.odm.operators.find.comparison import In

from app.models.template import Template
from app.models.user import User
from app.models.game import Game

class TemplateService:
    """模板管理服务"""
    
    @staticmethod
    async def get_templates_for_user(
        user_id: str,
        game_id: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Template]:
        """获取用户的模板列表"""
        query = Template.find(Template.owner.id == user_id)
        
        if game_id:
            query = query.find(Template.game.id == game_id)
        
        if category:
            query = query.find(Template.category == category)
        
        return await query.sort(-Template.updated_at).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def get_public_templates(
        game_id: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Template]:
        """获取公共模板列表"""
        query = Template.find(Template.is_public == True)
        
        if game_id:
            query = query.find(Template.game.id == game_id)
        
        if category:
            query = query.find(Template.category == category)
        
        return await query.sort(-Template.usage_count).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def get_templates_for_game(
        package_name: str,
        user_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Template]:
        """通过游戏包名获取模板"""
        game = await Game.find_one(Game.package_name == package_name)
        if not game:
            return []
        
        if user_id:
            # 获取用户的模板和流行的公共模板
            user_templates = await Template.find(
                Template.game.id == game.id,
                Template.owner.id == user_id
            ).to_list()
            
            # 公共模板数量
            public_limit = max(0, limit - len(user_templates))
            
            if public_limit > 0:
                # 排除用户已有的模板
                user_template_ids = [t.id for t in user_templates]
                public_templates = await Template.find(
                    Template.game.id == game.id,
                    Template.is_public == True,
                    ~In(Template.id, user_template_ids) if user_template_ids else {}
                ).sort(-Template.usage_count).limit(public_limit).to_list()
                
                return user_templates + public_templates
            return user_templates
        else:
            # 仅返回公共模板
            return await Template.find(
                Template.game.id == game.id,
                Template.is_public == True
            ).sort(-Template.usage_count).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def increment_usage_count(template_id: str) -> Optional[Template]:
        """增加模板使用次数"""
        template = await Template.get(template_id)
        if template:
            template.usage_count += 1
            await template.save()
        return template