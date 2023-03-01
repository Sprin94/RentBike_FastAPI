from sqlalchemy import Boolean, Integer
from sqlalchemy import Column
from sqlalchemy import String, VARCHAR, Date
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(VARCHAR(50), nullable=True)
    surname = Column(VARCHAR(50), nullable=True)
    birth_day = Column(Date, nullable=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    orders = relationship('Order', back_populates='tenant')
