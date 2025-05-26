from typing import List, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import DonationCreate
from datetime import datetime, timezone

from app.schemas.charity_project import CharityProjectCreate
from app.models import CharityProject, Donation


def transfer(
    source: Union[CharityProject, Donation],
    recipient: Union[CharityProject, Donation]
) -> None:
    transfer_amount = min(
        recipient.full_amount - recipient.invested_amount,
        source.full_amount - source.invested_amount
    )
    source.invested_amount += transfer_amount
    recipient.invested_amount += transfer_amount


def update_fund(
    fund: Union[CharityProject, Donation]
) -> None:
    if fund.invested_amount == fund.full_amount:
        fund.fully_invested = True
        fund.close_date = datetime.now(timezone.utc)


async def get_recipients_to_invest(
        model: Union[Type[CharityProject], Type[Donation]],
        session: AsyncSession
) -> Union[List[CharityProject], List[Donation]]:
    recipients = await session.scalars(
        select(model).where(model.fully_invested == 0)
    )
    return recipients.all()


async def invest_funds(
        source: Union[CharityProject, Donation],
        session: AsyncSession
) -> Union[CharityProjectCreate, DonationCreate]:
    source.invested_amount = 0
    model = Donation if isinstance(source, CharityProject) else CharityProject
    recipients = await get_recipients_to_invest(model, session)
    for recipient in recipients:
        if source.fully_invested:
            break
        transfer(source, recipient)
        update_fund(source)
        update_fund(recipient)
        session.add(recipient)
    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source
