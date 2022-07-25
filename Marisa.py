import asyncio
from datetime import datetime, timedelta
import aiohttp

import handlers
from DBuse import time_watcher
from bata import AllData
from aiogram import Dispatcher

from aiogram.dispatcher.fsm.storage.redis import RedisStorage

from marisa_log.scribe import witch_log

data = AllData()
bot = data.get_bot()
storage = RedisStorage.from_url(data.redis_url)
dp = Dispatcher(storage)


async def marisa_eyes():
    is_times = await time_watcher()
    if is_times:
        a = datetime.strptime(is_times.strftime('%H:%M'), '%H:%M')
        one_time = (a + timedelta(hours=12)).time()
        two_time = a.time()
        while True:
            time = datetime.strptime(datetime.now().time().strftime('%H:%M'), '%H:%M').time()
            if time == one_time or time == two_time:
                await handlers.marisa_awaikens(None, bot)
                await asyncio.sleep(120)
            await asyncio.sleep(0.5)
    else:
        witch_log.warning('There is no records in table, sleep for 1h')
        await asyncio.sleep(3600)


async def main():
    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")
    dp.include_router(handlers.router)
    asyncio.create_task(marisa_eyes())
    session = aiohttp.ClientSession()
    await session.close()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
