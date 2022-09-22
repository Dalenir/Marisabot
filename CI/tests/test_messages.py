import os

import pytest
from aiogram import Bot, Dispatcher

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from aiogram.exceptions import TelegramBadRequest

from CI import test_hand
from CI.Updates import fake_message_update, fake_callback_update
from DBs.DBuse import data_getter
from bata import AllData
from handlers import main_hand
from handlers.main_hand import marisa_awaikens
from states import MarisaStates

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
            await marisa_awaikens(bot=bot, users_list=[os.getenv('TEST_USER_ID')])
