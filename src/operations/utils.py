from fastapi import HTTPException


def validate_amount_to_balance_replenishment(amount: float):
    if amount <=0:
        raise HTTPException(status_code=422, detail="Amout to balance replenishment must not be less than 0")
    
    return amount