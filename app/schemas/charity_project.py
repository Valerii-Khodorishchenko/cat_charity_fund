from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)
    invested_amount: Optional[int] = None
    create_date: Optional[datetime] = None
    close_date: Optional[datetime] = None
    fully_invested: Optional[bool] = None

    @validator(
        'invested_amount',
        'create_date',
        'close_date',
        'fully_invested',
        check_fields=False
    )
    def validate_forbidden_fields(cls, field):
        if field is not None:
            raise ValueError('Это поле нельзя изменять через API')
        return field


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
