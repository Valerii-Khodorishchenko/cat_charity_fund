from datetime import datetime, timezone

from app.models import Investment


def invest_funds(
        target: Investment,
        sources: list[Investment],
) -> list[Investment]:
    update_sources = []
    for source in sources:
        if target.fully_invested:
            break
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for fund in source, target:
            fund.invested_amount += transfer_amount
            if fund.invested_amount == fund.full_amount:
                fund.fully_invested = True
                fund.close_date = datetime.now(timezone.utc)
        update_sources.append(source)
    return update_sources
