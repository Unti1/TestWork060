from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped
from settings.database import Base


class Transaction(Base):
    user_id: Mapped[str] = Column(ForeignKey('users.id'))
    amount: Mapped[Decimal]
    currency: Mapped[str]
    timestamp = Mapped[datetime]
    