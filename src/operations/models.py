from sqlalchemy import CheckConstraint, Numeric, Column, Integer, String, Enum, Text, Table, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class TransferHistory(Base):

    __tablename__ = "transfer_history"

    id = Column(Integer, primary_key=True, index=True)
    receipt_number = Column(String(11), unique=True, nullable=False)
    user_sender = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_receiver = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_sender = Column(String(16), nullable=False)
    transfer_amount = Column(Numeric(10, 2), nullable=False)
    transfer_date = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint('LENGTH(receipt_number) = 11'),
    )