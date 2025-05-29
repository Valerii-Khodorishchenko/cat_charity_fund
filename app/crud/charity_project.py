from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate
)

from app.crud.base import CRUDBase


class CharityProjectCRUD(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    async def get_project(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        attr = getattr(CharityProject, attr_name)
        return (await session.scalars(
            select(CharityProject).where(attr == attr_value)
        )).first()


charity_project_crud = CharityProjectCRUD(CharityProject)
