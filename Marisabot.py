import asyncio
from asyncio import events
from datetime import datetime, timedelta

import aiohttp

import handlers
from DBuse import time_watcher
from bata import all_data
from aiogram import Dispatcher

from aiogram.dispatcher.fsm.storage.redis import RedisStorage

data = all_data()
bot = data.get_bot()
storage = RedisStorage.from_url(data.redis_url)
dp = Dispatcher(storage)


async def periodic(timet):
    a = datetime.strptime(timet.strftime('%H:%M'), '%H:%M')
    one_time = (a + timedelta(hours=12)).time()
    two_time = a.time()
    while True:
        time = datetime.strptime(datetime.now().time().strftime('%H:%M'), '%H:%M').time()
        if time == one_time or time == two_time:
            await handlers.marisa_awaikens(None, bot)
            await asyncio.sleep(120)
        await asyncio.sleep(0.5)


async def main():
    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")
    dp.include_router(handlers.router)
    if await time_watcher():
        asyncio.create_task(periodic(timet=(await time_watcher())[0][0]))
    session = aiohttp.ClientSession()
    await session.close()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
