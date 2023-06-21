# app\models\donation.py

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0)
    close_date = Column(DateTime)
