# app\schemas\shema.py

from datetime import datetime
from pydantic import BaseModel, Field


class BaseShema(BaseModel):
    full_amount: int = Field(..., gt=0)
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime = None