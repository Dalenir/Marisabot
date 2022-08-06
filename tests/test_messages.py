import asyncio
import os
import unittest

import pytest
from aiogram import Bot, Dispatcher

from CI import test_hand
from CI.Updates import test_message
from handlers import main_hand


@pytest.mark.asyncio
class TestMessages:

    async def test_start(self):
        bot = Bot(os.getenv('BOT_TOKEN'))
        dp = Dispatcher()
        dp.include_router(test_hand.router)
        result = await dp.feed_update(bot, test_message)
        assert result == 'Smoketesting wasv successfull'


if __name__ == '__main__':
    unittest.main()
