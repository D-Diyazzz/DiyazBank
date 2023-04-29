from pydantic import BaseModel


class TransferCreate(BaseModel):
    pincode: int
    number_card: str
    receiver_phone: str
    amount: float
    