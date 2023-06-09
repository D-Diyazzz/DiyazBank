import abc
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.account import models
from src.account.schemas import *
from src.account.utils import *
from src.auth.jwt import get_password_hash


# class AbstractRepository(abc.ABC):

#     @abc.abstractclassmethod
#     def add(self, obj: )

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id:int):
        row = await self.session.execute(select(models.User).where(models.User.id == id))
        return row.one()[0]
    
    async def get_by_phone(self, phone:str):
        row = await self.session.execute(select(models.User).where(models.User.phone_number == phone))
        return row.one()[0]

    async def add(self, user: UserCreate):
        hash_pincode = get_password_hash(str(user.pincode))
        hash_password = get_password_hash(user.password)
        user = models.User(firstname=user.firstname, lastname=user.lastname,phone_number=user.phone_number,
                           date_of_birth=user.date_of_birth, hash_password=hash_password, 
                           hash_pincode=hash_pincode, registration_date=datetime.now())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update(self, user: UserUpdate, id):
        await self.session.execute(update(models.User).where(models.User.id == id).values(**user.get_non_null_fields()))

    async def delete(self, id):
        await self.session.execute(delete(models.User).where(models.User.id == id))


class AccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        

    async def get_by_user_id(self, id:int):
        row = await self.session.execute(select(models.Account).where(models.Account.user_id == id))
        return row.one()[0]
    
    async def delete(self, id):
        await self.session.execute(delete(models.Account).where(models.Account.id == id))
    

class CardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, id:int):
        rows = await self.session.execute(select(models.Card).where(models.Card.account_id == id))
        return rows.all()
    
    async def get_by_id(self, id:int):
        row = await self.session.execute(select(models.Card).where(models.Card.id == id))
        return row.one()[0]

    async def get_first_by_account_id(self, id:int):
        row = await self.session.execute(select(models.Card).where(models.Card.account_id == id))
        return row.one()[0]
    
    async def get_by_number(self, number:str):
        row = await self.session.execute(select(models.Card).where(models.Card.number == number))
        return row.one()[0]

    async def add(self, card: CardCreate, id: int):
        number = generate_number_for_card()
        cvv = generate_cvv_fo_card()
        card = models.Card(account_id=id, **card.__dict__, number=number, cvv=cvv)
        self.session.add(card)
        await self.session.commit()
        await self.session.refresh(card)
        return card
    
    async def update(self, balance: float, id):
        await self.session.execute(update(models.Card).where(models.Card.id == id).values(balance=balance))
        # await self.session.commit()

    async def delete(self, id):
        await self.sessoin.execute(delete(models.Card).where(models.Card.id == id))