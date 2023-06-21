# app\schemas\charity_project.py
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, validator

from app.schemas.shema import BaseShema


class CharityProjectBase(BaseModel):
    name: Union[None, str] = Field(None, min_length=1, max_length=100)
    description: Union[None, str] = Field(None, min_length=1)
    full_amount: Union[None, int] = Field(None)

    class Config:
        extra = Extra.forbid


class CreateCharityProject(BaseShema):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Цель проекта не может быть пустым!')
        return value

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectDB(BaseModel):
    id: int
    name: str
    description: str
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
