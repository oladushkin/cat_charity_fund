# app\models\charity_project.py

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


class CharityProject(Base):
    """Модель проектов"""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0)
    close_date = Column(DateTime)
