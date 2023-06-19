# app\models\charity_project.py

from sqlalchemy import (
    Column, String, Text,
    Integer, Boolean, DateTime
)

from app.core.db import Base


class CharityProject(Base):
    """Модель проектов"""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    close_date = Column(DateTime)
