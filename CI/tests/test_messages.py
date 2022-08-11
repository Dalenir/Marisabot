import os
import unittest

import pytest
from aiogram import Bot, Dispatcher

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from aiogram.exceptions import TelegramBadRequest

from CI import test_hand
from CI.Updates import fake_message_update, fake_callback_update
from bata import AllData
from handlers import main_hand
from handlers.main_hand import marisa_awaikens
from states import MarisaStates


@pytest.mark.asyncio
class TestMessages:

    async def test_smoke(self):
        bot = Bot(os.getenv('BOT_TOKEN'))
        dp = Dispatcher()
        dp.include_router(test_hand.router)
        uppdate = fake_message_update('/smoke_test', int(os.getenv('TEST_CHANNEL_ID')), int(os.getenv('TEST_USER_ID')))
        assert await dp.feed_update(bot, uppdate) is True
        await dp.emit_shutdown()

    async def test_all_messages(self):
        bot = Bot(os.getenv('BOT_TOKEN'))
        storage = RedisStorage.from_url(AllData().redis_url)
        dp = main_hand.router.parent_router
        state = FSMContext(
            bot=bot,
            storage=storage,
            key=StorageKey(bot.id, int(os.getenv('TEST_USER_ID')), int(os.getenv('TEST_USER_ID')))
        )
        messages = ('/start', 'А ты точно Мариса?')
        for mes in messages:
            uppdate = fake_message_update(mes, int(os.getenv('TEST_USER_ID')),
                                          int(os.getenv('TEST_USER_ID')))
            await dp.feed_update(bot, uppdate)
        await state.clear()
        callbacks = ('1', '2', '3', '-1', '-2', '-3')
        for call in callbacks:
            await state.set_state(MarisaStates.start)
            uppdate = fake_callback_update(call, int(os.getenv('TEST_USER_ID')),
                                           int(os.getenv('TEST_USER_ID')))
            try:
                await dp.feed_update(bot, uppdate)
            except TelegramBadRequest:
                pass
        for call in callbacks:
            await state.set_state(MarisaStates.sleepmode)
            uppdate = fake_callback_update(call, int(os.getenv('TEST_USER_ID')),
                                           int(os.getenv('TEST_USER_ID')))
            await dp.feed_update(bot, uppdate)
            await marisa_awaikens(bot, users_list=[os.getenv('TEST_USER_ID')])


if __name__ == '__main__':
    unittest.main()
