# app\schemas\charity_project.py
from typing import Optional
from pydantic import Field
from app.schemas.shema import BaseShema
from datetime import datetime


class CharityProjectBase(BaseShema):
    name: Optional[str]
    description: Optional[str]


class CreateCharityProject(CharityProjectBase):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)


class CharityProjectUpdate(CreateCharityProject):
    pass


class CharityProjectDB(CreateCharityProject):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
