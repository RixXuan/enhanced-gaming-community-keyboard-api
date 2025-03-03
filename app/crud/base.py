from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from beanie import Document
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD 对象带有默认的 CRUD 操作方法
        """
        self.model = model

    async def get(self, id: str) -> Optional[ModelType]:
        """
        通过 ID 获取对象
        """
        return await self.model.get(id)

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        获取多个对象
        """
        return await self.model.find().skip(skip).limit(limit).to_list()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建新对象
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        await db_obj.insert()
        return db_obj

    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新对象
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        await db_obj.save()
        return db_obj

    async def remove(self, *, id: str) -> Optional[ModelType]:
        """
        删除对象
        """
        db_obj = await self.get(id)
        if db_obj:
            await db_obj.delete()
        return db_obj