from decimal import Decimal
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc


from src.database import get_async_session as get_session
from src.account.repository import *
from src.operations.repositry import *
from src.auth.jwt import get_user_id
from src.operations import schemas
from src.operations.utils import *
from src.operations import service


router = APIRouter(
    tags=["Operations"],
    prefix="/api/v1"
)


@router.patch("/balance_replenishment")
async def balance_replenishment(number_card: str, amount: float, session: AsyncSession = Depends(get_session)):
    card_repo = CardRepository(session)
    amount = validate_amount_to_balance_replenishment(amount)
    await service.balance_replenishment(number_card, amount, session, card_repo)

    return{"message": "Balance successfully replenished"}


@router.post("/transfer")
async def transfer(transfer_data: schemas.TransferCreate, session: AsyncSession = Depends(get_session), user_id = Depends(get_user_id)):
    user_repo = UserRepository(session)
    card_repo = CardRepository(session)
    account_repo = AccountRepository(session)

    user = await user_repo.get_by_id(user_id)
    account= await account_repo.get_by_user_id(user_id)
    try:
        card = await card_repo.get_by_number(transfer_data.number_card)
    except exc.NoResultFound as error:
        raise HTTPException(status_code=404, detail="Card not found")

    validate_data_for_transfer(user, account, card, transfer_data)

    transfer_history = await service.perform_transfer(user, card, transfer_data, user_repo, card_repo, account_repo, session)

    return{"message": "Transfer successful", "transfer": transfer_history}


@router.get("/transfer_history")
async def get_transfer_history(session: AsyncSession = Depends(get_session), user_id = Depends(get_user_id)):
    transfer_history_repo = TranserHistoryRepositry(session)
    transfer_histories = await transfer_history_repo.get_all(user_id)
    print(transfer_histories)
    transfer_history_list = [schemas.TransferHistoryRead(**i[0].__dict__) for i in transfer_histories]

    return {"transfers": transfer_history_list}