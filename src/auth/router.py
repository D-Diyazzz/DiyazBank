from datetime import datetime
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select

from src.user import schemas, models
from src.auth.jwt import *
from src.database import get_async_session as get_session
from src.auth.utils import validate_phone_number
from src.auth.schemas import TokenOut, UserLogin


router = APIRouter(
    tags=["Auth"]
)


@router.post("/register")
async def register(data: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    user = models.User(
        firstname=data.firstname,
        lastname=data.lastname,
        phone_number=validate_phone_number(data.phone_number),
        date_of_birth=data.date_of_birth,
        hash_password =get_password_hash(data.password),
        hash_pincode=get_password_hash(str(data.pincode)),
        registration_date=datetime.now()
    )
    
    try:
        session.add(user)
        await session.commit()
        await session.flush()
        await session.refresh(user)
    except exc.IntegrityError as e:
        print(e)
        return {"Error": f'User with this phone number = "{user.phone_number}" exist'}
    print(type(user.registration_date))
    user_out = schemas.UserRead(**user.__dict__)
    return user_out


@router.post("/login")
async def login(response: Response, data: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        user_by_phone = await session.execute(select(models.User).where(models.User.phone_number==data.phone_number))
        user_by_phone = user_by_phone.one()[0]
    
        if not verify_password(data.password, user_by_phone.hash_password):
            raise HTTPException(status_code=401, detail="Authorization error")
    except exc.NoResultFound as e:
        raise HTTPException(status_code=401, detail="Authorization error")
    
    

    data_to_encode = {"id": user_by_phone.id}
    access_token = create_access_token(data_to_encode)
    refresh_token = create_access_token(data_to_encode, expires_delta=timedelta(minutes=1000))
    
    tokenOut = TokenOut(access_token=access_token, refresh_token=refresh_token)
    response.headers["Authorization"] = f'Bearer {access_token}'
    return tokenOut


@router.post("/refresh")
async def refresh(access_token: str, refresh_token: str, response: Response):
    try:
        data = jwt.decode(access_token, str(config.SECRET_KEY), algorithms=config.ALGORITHM)
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Authorization error")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authorization error")

    new_access_token = create_access_token(data)
    new_refresh_token = create_access_token(data, expires_delta=timedelta(minutes=1000))
    tokenOut = TokenOut(access_token=new_access_token, refresh_token=new_refresh_token)
    response.headers["Authorization"] = f'Bearer {new_access_token}'
    return tokenOut