from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select

from src.database import get_async_session as get_session
from src.account.repository import *
from src.auth.jwt import get_user_id
from src.account import schemas


router = APIRouter(
    tags=["Account"],
    prefix="/api/v1"
)


@router.get("/user")
async def get_user_info(session: AsyncSession = Depends(get_session), user_id = Depends(get_user_id)):
    user_repo = UserRepository(session)

    user = await user_repo.get_by_id(user_id)

    user_out = schemas.UserRead(**user.__dict__)
    return user_out

@router.put("/user")
async def update_user_info(user_update: UserUpdate, session: AsyncSession = Depends(get_session), user_id = Depends(get_user_id)):
    user_repo = UserRepository(session)
   
    await user_repo.update(user_update, user_id)
    user = await user_repo.get_by_id(user_id)

    user_out = schemas.UserRead(**user.__dict__)
    return user_out

@router.get("/account")
async def get_account_info(session: AsyncSession = Depends(get_session), user_id = Depends(get_user_id)):
    account_repo = AccountRepository(session)
    card_repo = CardRepository(session)

    account = await account_repo.get_by_user_id(user_id)
    cards = await card_repo.get_all(account.id)
    cards_list = [schemas.CardRead(**i[0].__dict__) for i in cards]
    
    account_out = schemas.AccountRead(bonuses=account.bonuses, user_id=account.user_id, cards=cards_list)

    return account_out


@router.post("/card")
async def create_card(card: CardCreate, session: AsyncSession = Depends(get_session), user_id = Depends(get_user_id)):
    card_repo = CardRepository(session)
    account_repo = AccountRepository(session)

    account = await account_repo.get_by_user_id(user_id)
    card = await card_repo.add(card, account.id)
    card_out = schemas.CardRead(**card.__dict__)

    return card_out