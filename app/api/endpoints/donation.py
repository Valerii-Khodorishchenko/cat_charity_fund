from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationUserResponse
)
from app.crud.donation import donation_crud


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.

    Возвращает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationUserResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_multi(session, user)


@router.post(
    '/',
    response_model=DonationUserResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Сделать пожертвование."""
    return await donation_crud.create(donation, session, user)
