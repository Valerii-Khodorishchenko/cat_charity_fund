from typing import Optional

from sqlalchemy import func, select
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

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[dict[str, str]]:
        days_passed = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)
        )
        projects = (await session.execute(
            select(
                CharityProject.name,
                days_passed,
                CharityProject.description
            ).where(
                CharityProject.fully_invested
            ).order_by(days_passed)
        )).all()
        return [
            {'name': name, 'days': str(int(days)), 'description': description}
            for name, days, description in projects
        ]


charity_project_crud = CharityProjectCRUD(CharityProject)
