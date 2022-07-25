import unittest

import pytest

import DBuse


@pytest.mark.asyncio
class TestTime:

    async def test_no_time(self):
        assert await DBuse.time_watcher() is True


if __name__ == '__main__':
    unittest.main()
