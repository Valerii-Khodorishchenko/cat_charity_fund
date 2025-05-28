from datetime import datetime, timedelta, timezone

from sqlalchemy import CheckConstraint, Column, Boolean, DateTime, Integer
from sqlalchemy.orm import declared_attr

from app.core.db import Base


class Investment(Base):
    __abstract__ = True
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0, nullable=False,)
    full_amount = Column(Integer, nullable=False,)
    create_date = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc) - timedelta(seconds=0.1)
    )
    close_date = Column(DateTime)

    @declared_attr
    def __table_args__(cls):
        return (
            CheckConstraint(
                'full_amount > 0',
                name='check_full_amount_positive'
            ),
            CheckConstraint(
                'invested_amount >= 0',
                name='check_invested_amount_non_negative'
            ),
            CheckConstraint(
                'invested_amount <= full_amount',
                name='check_invested_not_exceed_full'
            ),
            CheckConstraint(
                'close_date IS NULL OR close_date >= create_date',
                name='check_close_date_after_create'
            ),
        )

    def __repr__(self):
        return f'{self.__class__.__name__} id: {self.id}'
