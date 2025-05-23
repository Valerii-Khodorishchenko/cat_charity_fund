from datetime import datetime, timezone

from sqlalchemy import Column, Boolean, DateTime, Integer


class InvestmentMixin:
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0, nullable=False,)
    full_amount = Column(Integer, nullable=False,)
    create_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    close_date = Column(DateTime)
