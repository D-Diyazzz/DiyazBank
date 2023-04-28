import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, Header

from src import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data_to_encode: dict, expires_delta: timedelta | None = None
):
    to_encode = data_to_encode.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(config.SECRET_KEY), algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_user_id(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        token_type, access_token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Authorization error")
        
        try:
            data = jwt.decode(access_token, str(config.SECRET_KEY), algorithms=config.ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Authorization error")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Authorization error")

        return data['id']
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Authorization error")
