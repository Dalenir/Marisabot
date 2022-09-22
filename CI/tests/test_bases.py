import os

import pytest
from aiogram.types import User

from DBs import DBuse
from DBs.DBuse import WitchGuest, BadGuest, data_getter
from bata import AllData

data = AllData()
pytestmark = pytest.mark.anyio


@pytest.fixture(scope='module')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='module', autouse=True)
async def db_restore(anyio_backend):
    yield
    print('SETUP TESTS')
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    with open(f'{path}/databases/postgres/init.sql') as file:
        sqlFile = file.read()
    sqlCommands = sqlFile.split(';')
    await data_getter('DROP TABLE IF EXISTS stats CASCADE;'
                      'DROP TABLE IF EXISTS users CASCADE ;'
                      'DROP TABLE IF EXISTS everyday_tasks CASCADE;', return_value=False)
    for sqlcommand in sqlCommands:
        await data_getter(sqlcommand, return_value=False)


class TestDBs:

    async def test_time_warning(self):
        assert await DBuse.time_watcher() is False

    async def test_add_answer(self):
        await DBuse.answer_writer(5, 666)

    async def test_time(self):
        assert await DBuse.time_watcher() is not False

    async def test_no_time(self):
        assert await DBuse.get_old_points(666) is not False

    async def test_redis_zero_connect(self):
        assert data.get_red().set('1', '1') is not False

    async def test_redis_set(self):
        await DBuse.redis_set('key', 'WITCHY WITCH')

    async def test_redis_set_negative(self):
        try:
            assert await DBuse.redis_set({'1': '1'}, {1, 1})
        except Exception as ex:
            print(ex)
        else:
            raise Exception('NO EXEPTION IN REDIS SET')

    async def test_redis_get(self):
        assert await DBuse.redis_get('key') == 'WITCHY WITCH'


class TestWitchGuest:

    @pytest.fixture(scope="function", params=[None, 60000],
                    ids=['None', 'Not valid id'])
    def test_negative_id(self, request):
        return request.param

    async def test_get_negative(self, test_negative_id):
        try:
            await WitchGuest(test_negative_id).get_user()
        except BadGuest:
            pass
        else:
            raise Exception('Not valid guest, but no Bad Guest Exeption!')

    async def test_get_positive(self):
        q = "INSERT INTO public.users(t_id, username, fullname) VALUES (7000, 'Testing', 'Ultra')"
        await data_getter(q, return_value=False)
        guest = await WitchGuest(7000).get_user()
        assert guest.full_name == 'Ultra'
        assert guest.username == 'Testing'

    async def test_create(self):
        user = User(
            id=123123,
            is_bot=False,
            first_name='Tester',
            last_name='Shmester',
            username='tesinguser51'
        )
        new_guest = await WitchGuest().create(user)
        assert new_guest.full_name == 'Tester Shmester'
        assert new_guest.id == 123123
