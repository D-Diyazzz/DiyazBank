from sqlalchemy import Boolean, Column, Integer, String, Float, Text, Table, Date, DateTime

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