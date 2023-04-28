import re
from fastapi import HTTPException


def validate_phone_number(phone_number):
    phone_number = phone_number.replace(" ", "")
    
    pattern = "^(\+7|8)[0-9]{9,11}$"
    match = re.match(pattern, phone_number)
    
    if match and match.group() == phone_number:
        return phone_number
    else:
        raise HTTPException(status_code=400, detail="Phone number validate error")