import asyncio
import unittest

import pytest

from Marisa import main
from handlers import main_hand


@pytest.mark.asyncio
class TestDoor:

    async def test_bot_door(self):
        try:
            await asyncio.wait_for(main(), 5)
        except asyncio.exceptions.TimeoutError:
            await main_hand.router.emit_shutdown()


if __name__ == '__main__':
    unittest.main()
