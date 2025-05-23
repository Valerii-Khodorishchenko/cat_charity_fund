from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.mixins import InvestmentMixin


class Donation(Base, InvestmentMixin):
    user_id = Column(Integer, ForeignKey('user.id', name='fk_user_order_id'))
    comment = Column(Text)
