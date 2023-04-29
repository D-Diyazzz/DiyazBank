from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum

from src.account.models import CardType


class UserRead(BaseModel):
    id: int
    firstname: str
    lastname: str
    phone_number: str
    date_of_birth: date
    address: Optional[str] = None
    registration_date: datetime
    iin: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    phone_number: str
    date_of_birth: Optional[date] = None
    password: str
    pincode: int


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    hash_password: Optional[str] = None
    hash_pincode: Optional[int] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    iin: Optional[str] = None

    class Config:
        orm_mode = True

    def get_non_null_fields(self):
        return {key: value for key, value in self.dict().items() if value is not None}


class AccountRead(BaseModel):
    bonuses: float
    user_id: int
    cards: Optional[list] = []
    credits: Optional[list] = []
    debit: Optional[list] = []

    class Config:
        orm_mode = True
    
class CardCreate(BaseModel):
    card_type: CardType


class CardRead(BaseModel):
    card_type: CardType
    number: str
    cvv: str

