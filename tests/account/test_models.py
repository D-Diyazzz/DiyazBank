import asyncio
import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime, date

from src.database import engine, Base, async_session_maker
from src.account.models import User


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


@pytest_asyncio.fixture
async def session(async_setup_database):
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def init_user(session):
    user = User(firstname='Name', lastname='Name', phone_number='1234567890', hash_password='password', 
                hash_pincode='1234', date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(), address='Manasa', 
                registration_date=datetime.strptime('2022-04-28T15:30:00', '%Y-%m-%dT%H:%M:%S'), iin='123456789012')
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_add_user(session, init_user):

    result = await session.execute(select(User).where(User.phone_number=='1234567890'))
    user = result.scalar_one()
    assert user.firstname == 'Name'
    assert user.lastname == 'Name'
    assert user.phone_number == '1234567890'
    assert user.hash_password == 'password'
    assert user.hash_pincode == '1234'
    assert user.date_of_birth == date(1990, 1, 1)
    assert user.address == 'Manasa'
    assert user.registration_date == datetime(2022, 4, 28, 15, 30)
    assert user.iin == '123456789012'


@pytest.mark.asyncio
async def test_add_user_duplicate_phone_number(session, init_user):
    with pytest.raises(IntegrityError):
        user = User(firstname='Name', lastname='Name', phone_number='1234567890', hash_password='password',
                    hash_pincode='1234', date_of_birth=date(2001, 1, 1), address='Manasa',
                    registration_date=datetime(2022, 4, 28, 15, 30), iin='111111111111')
        session.add(user)
        await session.commit()


@pytest.mark.asyncio
async def test_add_user_duplicate_iin(session, init_user):
    with pytest.raises(IntegrityError) as error:
        user = User(firstname='Name', lastname='Name', phone_number='5555555555', hash_password='password',
                    hash_pincode='1234', date_of_birth=date(1990, 1, 1), address='Manasa',
                    registration_date=datetime(2022, 4, 28, 15, 30), iin='123456789012')
        session.add(user)
        await session.commit()

    assert 'Key (iin)=(123456789012) already exists.' in str(error.value)

@pytest.mark.asyncio
async def test_add_user_without_firstname(session):
    with pytest.raises(IntegrityError) as error:
        user = User(lastname='Name', phone_number='5555555555', hash_password='password',
                        hash_pincode='1234', date_of_birth=date(1990, 1, 1), address='Manasa',
                        registration_date=datetime(2022, 4, 28, 15, 30), iin='123456789012')
        session.add(user)
        await session.commit()

    assert 'null value in column "firstname" of relation "users" violates not-null constraint' in str(error.value)