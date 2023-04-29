from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.operations import models
from src.operations import schemas


class TranserHistoryRepositry:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, id:int):
        rows = await self.session.execute(select(models.TransferHistory).where(or_(models.TransferHistory.user_sender == id, models.TransferHistory.user_receiver == id)))
        return rows.all()

    async def add(self, transfer_history: schemas.TransferHisotryCreate):
        
        transfer_history = models.TransferHistory(**transfer_history.__dict__)
        self.session.add(transfer_history)
        self.session.refresh(transfer_history)
        return transfer_history