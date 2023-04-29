from sqlalchemy import Numeric, Column, Integer, String, Enum, Text, Table, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from src.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    phone_number = Column(String(12), nullable=True, unique=True)
    hash_password = Column(Text, nullable=False)
    hash_pincode = Column(Text, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String(200))
    registration_date= Column(DateTime)
    iin = Column(String(12), unique=True)

    account = relationship("Account", back_populates="user")


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    bonuses = Column(Numeric(10, 2), default=0)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="account")
    card = relationship("Card", back_populates="account")
    credit = relationship("Credit", back_populates='account')
    deposit = relationship("Deposit", back_populates='account')

class CardType(PyEnum):
    DIYAZ_GOLD = "Diyaz Gold"
    DIYAZ_BONUS = "Diyaz Bonus"


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    number = Column(String(16), unique=True, nullable=False)
    cvv = Column(String(3), nullable=False)
    balance = Column(Numeric(10, 2), default=0)
    card_type = Column(Enum(CardType), nullable=False)
    
    account = relationship("Account", back_populates="card")


class Credit(Base):
    __tablename__ = "credit"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    amount = Column(Numeric(10, 2), nullable=False)
    remain_to_pay = Column(Numeric(10, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    interest_rate = Column(Numeric(5, 2), default=1.0)

    account = relationship("Account", back_populates="credit")


class Deposit(Base):
    __tablename__ = "deposit"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    interest_rate = Column(Numeric(5, 2), default=1.141)
    balance = Column(Numeric(10, 2), default=0)
    start_date = Column(Date, nullable=False)

    account = relationship("Account", back_populates="deposit")
