import os

import pytest
from aiogram.types import User

from DBs import DBuse
from DBs.DBuse import WitchGuest, BadGuest, data_getter
from bata import AllData
from functions.daily_mood import WitchyMood

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

    @pytest.fixture(scope="class", params=[(7000, 'Testing', 'Ultra'),
                                           (921348903, '', '')],
                    ids=['Valid user', 'User with empty username and fullname'])
    async def ind_pos_test_db_data(self, request):
        q = f"INSERT INTO public.users(t_id, username, fullname) VALUES ({request.param[0]}, '{request.param[1]}'," \
            f" '{request.param[2]}')"
        await data_getter(q, return_value=False)
        return request.param

    async def test_get_negative(self, test_negative_id):
        try:
            await WitchGuest(test_negative_id).get_user()
        except BadGuest:
            pass
        else:
            raise Exception('Not valid guest, but no Bad Guest Exeption!')

    async def test_get_positive(self, ind_pos_test_db_data):
        guest = await WitchGuest(ind_pos_test_db_data[0]).get_user()
        assert guest.full_name == ind_pos_test_db_data[2]
        assert guest.username == ind_pos_test_db_data[1]

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

    async def test_mood_switch(self, ind_pos_test_db_data):
        guest = await WitchGuest(ind_pos_test_db_data[0]).get_user()
        assert not guest.mood_diary_concern
        await guest.switch_mood_diary()
        assert guest.mood_diary_concern
        await guest.switch_mood_diary()
        assert not guest.mood_diary_concern

    async def test_concern_switch(self, ind_pos_test_db_data):
        guest = await WitchGuest(ind_pos_test_db_data[0]).get_user()
        assert not guest.everyday_task_concern
        await guest.switch_everyday_tasks()
        assert guest.everyday_task_concern
        await guest.switch_everyday_tasks()
        assert not guest.everyday_task_concern


class TestDailyMood:
    @pytest.fixture(scope='class', autouse=True)
    def test_data(self):
        return ((int(os.getenv('TEST_USER_ID')), 'A', 'A', True, False), (1, 'B', 'B', True, False),
                (1, 'C', 'C', True, False), (1, 'D', 'D', True, False), (1, 'E', 'E', True, False),
                (1, 'F', 'F', True, False))

    @pytest.fixture(scope='class', autouse=True)
    async def fill_base(self, test_data):
        await data_getter(f"INSERT INTO public.users values ({'), ('.join(test_data)})")

    async def test_witchy_mood_create(self):
        mood = WitchyMood()
        assert not mood.concern_list
        await mood.fill_concern_list()
        assert len(mood.concern_list) == 6
