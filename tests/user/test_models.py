import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import engine, Base


@pytest_asyncio.fixture
async def async_setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with engine.dispose() as conn:
        await conn.run_sync(Base.metadata.drop_all)


