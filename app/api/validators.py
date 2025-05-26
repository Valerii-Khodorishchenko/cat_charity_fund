from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


ERROR_MESSAGE_PROJECT_NAME_EXIST = 'Имя проекта должно быть уникальным.'
ERROR_MESSAGE_PROJECT_NOT_EXIST = 'Проект не найден.'
ERROR_MESSAGE_PROJECT_FULLY_INVESTED = (
    'Нельзя изменять полностью проинвестированые проекты'
)
ERROR_MESSAGE_PROJECT_FULLY_AMOUNT = (
    'Полная сумма инвестиций должна быть больше уже инвестируемых средств'
)
ERROR_MESSAGE_INVESTED_PROJECT = 'Нельзя удалить проект с инвестицией'


async def check_name_project(
        name_project: str,
        session: AsyncSession
) -> None:
    project = await charity_project_crud.get_project(
        'name', name_project, session
    )
    if project is not None:
        raise HTTPException(
            status_code=400,
            detail=ERROR_MESSAGE_PROJECT_NAME_EXIST,
        )


async def get_project_or_404(
        attr_name: str,
        attr_volume: str,
        session: AsyncSession
):
    project = await charity_project_crud.get_project(
        attr_name, attr_volume, session
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGE_PROJECT_NAME_EXIST,
        )
    return project


async def check_fully_invested(
        project: CharityProject,
):
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=ERROR_MESSAGE_PROJECT_FULLY_INVESTED,
        )


async def check_fully_amount(
        project: CharityProject,
        changes: CharityProjectUpdate,
):
    if project.invested_amount > changes.full_amount:
        raise HTTPException(
            status_code=422,
            detail=ERROR_MESSAGE_PROJECT_FULLY_AMOUNT,
        )


async def check_exist_invested_amount(
        project: CharityProject
):
    if project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=ERROR_MESSAGE_INVESTED_PROJECT
        )
