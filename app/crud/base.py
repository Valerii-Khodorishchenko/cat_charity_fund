from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User
from app.services.investment import invest_funds


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> List[ModelType]:
        query = select(self.model)
        if user is not None:
            query = query.where(self.model.user_id == user.id)
        db_objs = await session.scalars(query)
        return db_objs.all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        return await invest_funds(db_obj, session)
