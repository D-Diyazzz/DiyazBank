import random
from fastapi import HTTPException
from passlib.context import CryptContext

from src.account import models
from src.operations import schemas


def validate_amount_to_balance_replenishment(amount: float):
    if amount <=0:
        raise HTTPException(status_code=422, detail="Amout to balance replenishment must not be less than 0 or equal to 0")
    
    return amount


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_pincode(plain_pincode: str, hashed_pincode: str) -> bool:
    return pwd_context.verify(plain_pincode, hashed_pincode)


def validate_data_for_transfer(
        user: models.User, 
        account: models.Account, 
        card: models.Card,  
        transfer_data: schemas.TransferCreate
        ):
    
    if(user.phone_number == transfer_data.receiver_phone):
        raise HTTPException(status_code=400, detail=f"transfer to this card is not possible")
    if(card.account_id != account.id):
        raise HTTPException(status_code=404, detail="Card not found")
    if(card.balance < transfer_data.amount):
        raise HTTPException(status_code=400, detail="Not enough money")
    if(transfer_data.amount <= 0):
        raise HTTPException(status_code=422, detail="Amout of money to transfer must not be less than 0 or equal to 0")
    if not verify_pincode(str(transfer_data.pincode), user.hash_pincode):
        raise HTTPException(status_code=401, detail="Invalid pincode")
    
    
def generate_receipt_number():
    number = [str(random.randint(0, 9)) for _ in range(11)]
    return "".join(number)