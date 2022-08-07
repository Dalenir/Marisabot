import asyncio
import os
import unittest

import pytest
from aiogram import Bot, Dispatcher

from CI import test_hand
from CI.Updates import test_message
from Marisa import main


@pytest.mark.asyncio
class TestMessages:

    async def test_start(self):
        bot = Bot(os.getenv('BOT_TOKEN'))
        dp = Dispatcher()
        dp.include_router(test_hand.router)
        result = await dp.feed_update(bot, test_message)
        assert result == 'Smoketesting was successfull'

    async def test_bot_door(self):
        try:
            await asyncio.wait_for(main(), 10)
        except asyncio.exceptions.TimeoutError:
            pass


if __name__ == '__main__':
    unittest.main()
