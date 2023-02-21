from datetime import datetime

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime


@as_declarative
class Base:
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
