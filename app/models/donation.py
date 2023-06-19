# app\models\donation.py

from sqlalchemy import (
    Column, Text,
    Integer, Boolean, DateTime,
)
#    ForeignKey
from app.core.db import Base

#    user_id = Column(Integer, ForeignKey('user.id'))


class Donation(Base):
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    close_date = Column(DateTime)
