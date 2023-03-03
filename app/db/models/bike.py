import enum

from sqlalchemy import (Column, VARCHAR, Integer, UniqueConstraint,
                        CheckConstraint, ForeignKey, Enum,)
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class BikeModel(Base):
    id = Column(Integer, primary_key=True)
    brand = Column(VARCHAR(50))
    model = Column(VARCHAR(50), unique=True, index=True)
    engine_capacity = Column(Integer)

    bikes = relationship('Bike', back_populates='model')
    __table_args__ = (
        UniqueConstraint(
            'brand',
            'model',
            name='_brand_model_uc'
        ),
        CheckConstraint(
            engine_capacity > 0, name='check_engine_capacity_positive'
        )
                     )


class Bike(Base):
    number = Column(VARCHAR(12), primary_key=True, unique=True)
    model_id = Column(
        Integer,
        ForeignKey('bikemodels.id', ondelete="CASCADE"),
        nullable=False
    )
    color = Column(VARCHAR(50))
    born_year = Column(Integer)
    mileage = Column(Integer, default=0)
    photo = Column(VARCHAR(250))

    class BikeStatus(enum.Enum):
        available = 'available'
        unavailable = 'unavailable'

    status = Column(Enum(BikeStatus), default=BikeStatus.available)

    cost_per_day = Column(Integer)
    model = relationship('BikeModel', back_populates="bikes", lazy=True)
    orders = relationship('Order', back_populates='bike')
    __table_args__ = (
        CheckConstraint(
            born_year > 0, name='check_born_year_positive'
        ),
        CheckConstraint(
            mileage >= 0, name='check_mileage_positive'
        ),
        CheckConstraint(
            cost_per_day > 0, name='check_cost_per_day_positive'
        ),
    )
