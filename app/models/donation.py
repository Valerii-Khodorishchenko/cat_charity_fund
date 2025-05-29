from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.investment import Investment


class Donation(Investment):
    user_id = Column(Integer, ForeignKey('user.id', name='fk_user_order_id'))
    comment = Column(Text)

    def __repr__(self):
        return f'{super().__repr__()}, {self.user_id=}, {self.comment=}'
