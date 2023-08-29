from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    validator,
    Extra,
)

NAME_PROJECT_ERROR = 'Имя проекта не может быть пустым!'


class Base(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1


class CharityProjectCreate(Base):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    @validator('name')
    def check_name(cls, name):
        if name is None:
            raise ValueError(NAME_PROJECT_ERROR)
        return name


class CharityProjectUpdate(Base):

    class Config:
        extra = Extra.forbid


class CharityProjectDB(Base):
    id: int
    invested_amount: int
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
