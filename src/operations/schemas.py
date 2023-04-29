from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransferCreate(BaseModel):
    pincode: int
    number_card: str
    receiver_phone: str
    amount: float

class TransferHisotryCreate(BaseModel):
    receipt_number: Optional[str] = None
    user_sender: int
    user_receiver: int
    card_sender: int
    transfer_amount: float
    transfer_date: Optional[datetime] = None

class TransferHistoryRead(BaseModel):
    receipt_number: str
    user_sender: str
    user_receiver:str
    transfer_amount: float
    transfer_date: datetime

    class Config:
        orm_mode = True
