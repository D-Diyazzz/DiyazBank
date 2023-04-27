from fastapi import FastAPI

from src.database import engine


app = FastAPI(
    title="DiyazBank"
)


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.create_all)


