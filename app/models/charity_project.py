# app\models\charity_project.py
from sqlalchemy import (
    Column, String, Text,
    Integer, Boolean, DateTime
)

from app.core.db import Base


class CharityProject(Base):
    """Модель проектов"""

    __tablename__ = 'charityproject'

    name = Column(String(100))
    description = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
