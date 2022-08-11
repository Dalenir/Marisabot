import unittest

import psycopg2
import pytest

from DBs import DBuse
from bata import AllData

data = AllData()


@pytest.mark.asyncio
class TestDBs:

    async def test_time_warning(self):
        await DBuse.data_getter('DROP TABLE IF EXISTS public.stats', return_value=False)
        assert await DBuse.time_watcher() is False

    async def test_add_answer(self):
        await DBuse.answer_writer(5, 666)

    async def test_time(self):
        assert await DBuse.time_watcher() is not False

    async def test_add_answer_negative(self):
        try:
            await DBuse.answer_writer(5, 'MARISA')
        except psycopg2.Error:
            pass

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


if __name__ == '__main__':
    unittest.main()
