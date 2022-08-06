import unittest

import pytest

from DBs import DBuse


@pytest.mark.asyncio
class TestTime:

    async def test_no_time(self):
        assert await DBuse.time_watcher() is not False

    async def test_redis_connection(self):
        assert await DBuse.redis_get('key') is None

if __name__ == '__main__':
    unittest.main()
