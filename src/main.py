from fastapi import FastAPI

from src.database import engine, Base
from src.auth.router import router


app = FastAPI(
    title="DiyazBank"
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router)
