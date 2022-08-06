import unittest

import pytest

from DBs import DBuse


@pytest.mark.asyncio
class TestTime:

    async def test_no_time(self):
        assert await DBuse.time_watcher() is False


if __name__ == '__main__':
    unittest.main()
