from typing import Optional, List
from app.crud.base import CRUDBase
from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate

class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]):
    async def get_by_package_name(self, *, package_name: str) -> Optional[Game]:
        return await Game.find_one(Game.package_name == package_name)

    async def get_all(self) -> List[Game]:
        return await Game.find().to_list()

game = CRUDGame(Game)