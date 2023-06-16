# app\schemas\charity_project.py
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic import conint


class CharityProject(BaseModel):
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = datetime.now()
    close_date: datetime = None


class CreateCharityProject(CharityProject):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = conint(gt=0)


class CharityProjectUpdate(CreateCharityProject):
    pass


class CharityProjectDB(CreateCharityProject):
    id: int

    class Config:
        orm_mode = True
