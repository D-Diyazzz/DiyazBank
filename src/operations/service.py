from sqlalchemy import exc
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from src.account import models
from src.operations import schemas
from src.account.repository import *
from src.operations.repositry import *
from src.operations.utils import *

async def balance_replenishment(number_card: str, amount: float, session: AsyncSession, card_repo: CardRepository):
    try:
        card = await card_repo.get_by_number(number_card)

    except exc.NoResultFound as error:
        raise HTTPException(status_code=404, detail="Card not found")
    await card_repo.update(amount, card.id)
    await session.commit()


async def crete_history_of_transfer(transfer_history_create: schemas.TransferHisotryCreate, session: AsyncSession):
    transfer_history_repo = TranserHistoryRepositry(session)
    
    receip_number = generate_receipt_number()
    datetime_now = datetime.now()
    transfer_history_create.receipt_number = receip_number
    transfer_history_create.transfer_date = datetime_now
    try:
        transfer_history = await transfer_history_repo.add(transfer_history_create)
        return transfer_history
    except exc.IntegrityError:
        crete_history_of_transfer(transfer_history_create, session)

async def perform_transfer(
        user: models.User,
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
    
    transfer_history_create = schemas.TransferHisotryCreate(user_sender=user.id, user_receiver=receiver_user.id, card_sender=card.number, transfer_amount=transfer_data.amount)
    transder_history = await crete_history_of_transfer(transfer_history_create, session)
    transfer_history_read = schemas.TransferHistoryRead(
        receipt_number=transder_history.receipt_number, 
        user_sender=user.firstname+" "+user.lastname, 
        user_receiver=receiver_user.firstname+" "+receiver_user.lastname, 
        transfer_amount=transder_history.transfer_amount, 
        transfer_date=transder_history.transfer_date)

    total_user_balance = card.balance - Decimal(transfer_data.amount)
    total_receiver_balance = receiver_card.balance + Decimal(transfer_data.amount)

    await card_repo.update(total_user_balance, card.id)
    await card_repo.update(total_receiver_balance, receiver_card.id)
    await session.commit()

    return transfer_history_read