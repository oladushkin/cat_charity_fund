# app\schemas\donation.py
from datetime import datetime
from typing import Optional
from app.schemas.shema import BaseShema


class DonationBase(BaseShema):
    comment: Optional[str] = None


class CreateDonationBase(DonationBase):
    pass


class DonationBaseDB(DonationBase):
    id: int
#   user_id: int
    create_date: datetime

    class Config:
        orm_mode = True
