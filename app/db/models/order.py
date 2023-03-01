import enum
from uuid import uuid4

from sqlalchemy import (Column, UUID, VARCHAR, Integer, Date,
                        CheckConstraint, ForeignKey, Enum)
from sqlalchemy.orm import relationship
from app.db.models.base import Base


def gen_uuid_hex():
    return uuid4().hex


class Order(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=gen_uuid_hex)
    bike_number = Column(
        VARCHAR,
        ForeignKey('bikes.number', ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False
    )
    date_begin = Column(
        Date,
        nullable=False
    )
    date_end = Column(
        Date,
        nullable=False
    )

    class OrderStatus(enum.Enum):
        ACTIVE = 'active'
        COMPLETE = 'complete'
        RESERVATION = 'reservation'
        CANCELLED = 'cancelled'

    status = Column(Enum(OrderStatus), default=OrderStatus)

    bike = relationship('Bike', back_populates="orders")
    tenant = relationship('User', back_populates="orders", lazy=True)

    __table_args__ = (
        CheckConstraint(
            date_end > date_end, name='check_dates_positive'
        ),
    )
