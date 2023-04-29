from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc


from src.database import get_async_session as get_session
from src.account.repository import *
from src.auth.jwt import get_user_id
from src.operations.utils import *


router = APIRouter(
    tags=["Operations"],
    prefix="/api/v1"
)


@router.patch("/balance_replenishment")
async def balance_replenishment(number_card: str, amount: float, session: AsyncSession = Depends(get_session)):
    card_repo = CardRepository(session)
    amount = validate_amount_to_balance_replenishment(amount)
    try:
        card = await card_repo.get_by_number(number_card)

    except exc.NoResultFound as error:
        raise HTTPException(status_code=404, detail="Card not found")
    await card_repo.update(amount, card.id)

    return{"message": "Balance successfully replenished"}

