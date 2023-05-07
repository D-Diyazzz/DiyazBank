import asyncio
import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime, date

from src.database import engine, Base, async_session_maker
from src.account.models import User, Account, Card, CardType
from src.account.repository import *
from src.auth.jwt import verify_password


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(async_setup_database):
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def init_objects(session):
    user_create = UserCreate(firstname="Name", lastname="Name", phone_number="123456789011", date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
                             password="password", pincode="1234")
    user_repo = UserRepository(session)

    user = await user_repo.add(user_create)
    return user


@pytest.mark.asyncio
async def test_add_user_repository(session):
    user_create = UserCreate(firstname="Name", lastname="Name", phone_number="123456789011", date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
                             password="password", pincode="1234")
    user_repo = UserRepository(session)

    user = await user_repo.add(user_create)
    assert user.firstname == user_create.firstname
    assert user.lastname == user_create.lastname
    assert user.phone_number == user_create.phone_number
    assert user.date_of_birth == user_create.date_of_birth
    assert verify_password(user_create.password, user.hash_password) == True
    assert verify_password(str(user_create.pincode), user.hash_pincode) == True


@pytest.mark.asyncio
async def test_get_by_id_user_repository(session, init_objects):
    user_repo = UserRepository(session)
    user = init_objects

    user_by_id = await user_repo.get_by_id(user.id)
    assert user_by_id.id == user.id


@pytest.mark.asyncio
async def test_get_by_phone_user_repository(session, init_objects):
    user_repo = UserRepository(session)
    user = init_objects

    user_by_phone = await user_repo.get_by_phone(user.phone_number)
    assert user_by_phone.id == user.id
    assert user_by_phone.phone_number == user.phone_number


@pytest.mark.asyncio
async def test_update_user_repository(session, init_objects):
    user_repo = UserRepository(session)
    user = init_objects

    user_update = UserUpdate(firstname="UpdatedName", phone_number="110987654321")
    await user_repo.update(user_update, user.id)
    assert user.firstname == user_update.firstname
    assert user.phone_number == user_update.phone_number


@pytest.mark.asyncio
async def test_delete_user_repostory(session, init_objects):
    user_repo = UserRepository(session)
    user = init_objects

    await user_repo.delete(user.id)

    user = session.execute(select(models.User).where(models.User.id == user.id))
