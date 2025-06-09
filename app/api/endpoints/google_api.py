from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

router = APIRouter()


@router.get(
    '/',
    response_model=dict[str, str],
    dependencies=[Depends(current_superuser)]
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """
    Только для суперюзеров.\n
    Только если в переменные окружения переданы переменные ключа доступа к
    сервисному аккаунту и email гугл-аккаунта
    (см. README.md Подключение отчёта в Google Sheets).\n
    Возвращает ссылку на таблицу с отчётом.
    """
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid,
        await charity_project_crud.get_projects_by_completion_rate(session),
        wrapper_services
    )
    return {
        'report_link':
        f'https://docs.google.com/spreadsheets/d/{spreadsheetid}'
    }
