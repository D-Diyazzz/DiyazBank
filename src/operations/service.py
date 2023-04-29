from sqlalchemy import exc
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from src.account import models
from src.operations import schemas
from src.account.repository import *

async def balance_replenishment(number_card: str, amount: float, session: AsyncSession, card_repo: CardRepository):
    try:
        card = await card_repo.get_by_number(number_card)

    except exc.NoResultFound as error:
        raise HTTPException(status_code=404, detail="Card not found")
    await card_repo.update(amount, card.id)
    await session.commit()


async def perform_transfer(
        card: models.Card,  
        transfer_data: schemas.TransferCreate,
        user_repo: UserRepository,
        card_repo: CardRepository,
        account_repo: AccountRepository,
        session: AsyncSession
        ):

    try:
        receiver_user = await user_repo.get_by_phone(transfer_data.receiver_phone)
        receiver_account = await account_repo.get_by_user_id(receiver_user.id)
        receiver_card = await card_repo.get_by_account_id(receiver_account.id)
    except exc.NoResultFound as error:
        raise HTTPException(status_code=404, detail=f"User with this phone={transfer_data.receiver_phone} not found")
 
    total_user_balance = card.balance - Decimal(transfer_data.amount)
    total_receiver_balance = receiver_card.balance + Decimal(transfer_data.amount)

    await card_repo.update(total_user_balance, card.id)
    await card_repo.update(total_receiver_balance, receiver_card.id)
    await session.commit()