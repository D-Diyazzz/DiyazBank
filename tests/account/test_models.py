import asyncio
import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime, date

from src.database import engine, Base, async_session_maker
from src.account.models import User, Account, Card, CardType


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


# @pytest_asyncio.fixture
# async def init_objects(session):
#     user = User(firstname='Name', lastname='Name', phone_number='1234567890', hash_password='password', 
#                 hash_pincode='1234', date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(), address='Manasa', 
#                 registration_date=datetime.strptime('2022-04-28T15:30:00', '%Y-%m-%dT%H:%M:%S'), iin='123456789012')
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)

#     account = Account(user_id=user.id)
#     session.add(account)
#     await session.commit()
#     await session.refresh(account)

#     card = Card(account_id=account.id, number="1234567890123456", cvv="111", card_type=CardType.DIYAZ_GOLD)
#     session.add(card)
#     await session.commit()

#     await session.refresh(card)

#     return user, account, card

@pytest_asyncio.fixture
async def init_user(session):
    user = User(firstname='Name', lastname='Name', phone_number='1234567890', hash_password='password', 
                hash_pincode='1234', date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(), address='Manasa', 
                registration_date=datetime.strptime('2022-04-28T15:30:00', '%Y-%m-%dT%H:%M:%S'), iin='123456789012')
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@pytest_asyncio.fixture
async def init_account(session, init_user):
    account = Account(user_id=init_user.id)
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account


class TestUserModel():

    @pytest.mark.asyncio
    async def test_add_user(self, session, init_user):

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
    async def test_add_user_duplicate_phone_number(self, session, init_user):
        with pytest.raises(IntegrityError):
            user = User(firstname='Name', lastname='Name', phone_number='1234567890', hash_password='password',
                        hash_pincode='1234', date_of_birth=date(2001, 1, 1), address='Manasa',
                        registration_date=datetime(2022, 4, 28, 15, 30), iin='111111111111')
            session.add(user)
            await session.commit()


    @pytest.mark.asyncio
    async def test_add_user_duplicate_iin(self, session, init_user):
        with pytest.raises(IntegrityError) as error:
            user = User(firstname='Name', lastname='Name', phone_number='5555555555', hash_password='password',
                        hash_pincode='1234', date_of_birth=date(1990, 1, 1), address='Manasa',
                        registration_date=datetime(2022, 4, 28, 15, 30), iin='123456789012')
            session.add(user)
            await session.commit()

        assert f'Key (iin)=({user.iin}) already exists.' in str(error.value)

    @pytest.mark.asyncio
    async def test_add_user_without_firstname(self, session, init_user):
        with pytest.raises(IntegrityError) as error:
            user = User(lastname='Name', phone_number='5555555555', hash_password='password',
                            hash_pincode='1234', date_of_birth=date(1990, 1, 1), address='Manasa',
                            registration_date=datetime(2022, 4, 28, 15, 30), iin='123456789012')
            session.add(user)
            await session.commit()

        assert 'null value in column "firstname" of relation "users" violates not-null constraint' in str(error.value)


# class TestAccountModel():

#     @pytest.mark.asyncio
#     async def test_add_account(self, session, init_user, init_account):
        # result = await session.execute(select(Account).where(Account.user_id==init_user.id))
        # account = result.one()[0]
        # assert account.bonuses == 0
        # assert account.user_id == init_user.id
       