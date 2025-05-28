from typing import List
from datetime import datetime, timezone

from app.models import Investment


async def invest_funds(
        target: Investment,
        sources: List[Investment],
) -> List[Investment]:
    update_sources = []
    for source in sources:
        if target.fully_invested:
            break
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        source.invested_amount += transfer_amount
        target.invested_amount += transfer_amount
        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = datetime.now(timezone.utc)
        update_sources.append(source)
        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now(timezone.utc)
        print(target.invested_amount)
    return update_sources
