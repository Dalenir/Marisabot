import unittest

import psycopg2
import pytest
from aiogram import Bot

from DBs import DBuse


@pytest.mark.asyncio
class TestTime:

    async def test_add_answer(self):
        await DBuse.answer_writer(5, 666)

    async def test_add_answer_negative(self):
        try:
            await DBuse.answer_writer(5, 'MARISA')
        except psycopg2.Error:
            pass

    async def test_no_time(self):
        assert await DBuse.time_watcher() is not False

    async def test_redis_set(self):
        await DBuse.redis_set('key', 'WITCHY WITCH')

    async def test_redis_get(self):
        assert await DBuse.redis_get('key') == 'WITCHY WITCH'


if __name__ == '__main__':
    unittest.main()
