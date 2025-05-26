
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
        project = await session.scalars(
            select(CharityProject).where(attr == attr_value)
        )
        return project.first()

    async def update(
            self,
            project: CharityProject,
            changes: CharityProjectUpdate,
            session: AsyncSession
    ) -> CharityProject:
        update_data = changes.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    async def delete(
            self,
            project: CharityProject,
            session: AsyncSession
    ) -> CharityProject:
        await session.delete(project)
        await session.commit()
        return project


charity_project_crud = CharityProjectCRUD(CharityProject)
