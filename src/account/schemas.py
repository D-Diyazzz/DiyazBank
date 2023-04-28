from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime




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


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    pincode: Optional[int] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    iin: Optional[str] = None

    class Config:
        orm_mode = True
