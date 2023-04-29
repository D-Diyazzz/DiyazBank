from fastapi import FastAPI

from src.database import engine, Base
from src.auth.router import router as AuthRouter
from src.account.router import router as AccountRounter
from src.operations.router import router as OperatoinRouter


app = FastAPI(
    title="DiyazBank",
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(AuthRouter)
app.include_router(AccountRounter)
app.include_router(OperatoinRouter)
