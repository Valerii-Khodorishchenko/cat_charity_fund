from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_project,
    check_exist_invested_amount,
    check_fully_invested,
    check_fully_amount,
    get_project_or_404
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.crud import charity_project_crud, donation_crud
from app.services.investment import invest_funds


router = APIRouter()


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект.
    """
    await check_name_project(project.name, session)
    project = await charity_project_crud.create(project, session)
    session.add_all(invest_funds(
        project,
        await donation_crud.get_not_fully_invested(session)
    ))
    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть.
    """
    project = await get_project_or_404('id', project_id, session)
    check_fully_invested(project)
    check_exist_invested_amount(project)
    return await charity_project_crud.delete(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        changes: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await get_project_or_404('id', project_id, session)
    check_fully_invested(project)
    if project.name != changes.name:
        await check_name_project(changes.name, session)
    if changes.full_amount:
        check_fully_amount(project, changes)
    return await charity_project_crud.update(project, changes, session)
