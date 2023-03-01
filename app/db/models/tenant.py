import enum

from sqlalchemy import (Column, VARCHAR, Integer, Date)
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Tenant(Base):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(VARCHAR(50), nullable=False)
    surname = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(150), nullable=False)
    birth_day = Column(Date, nullable=False)
