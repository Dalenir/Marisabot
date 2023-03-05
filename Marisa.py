import asyncio
import warnings
import aiohttp
import pytz
from aiogram import Dispatcher
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from AllLogs.bot_logger import main_logger
from DBs.DBuse import time_watcher
from bata import AllData
from functions.daily_mood import WitchyMood
from handlers import main_hand, conv_hand, free_speach_hand
from marisa_log.scribe import witch_log

data = AllData()
bot = data.get_bot()
storage = RedisStorage.from_url(data.redis_url)
dp = Dispatcher(storage)


async def marisa_eyes():
    is_times = await time_watcher()
    if is_times:
        cron_concern_time = is_times.strftime('* %H/2 * * *')
        scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Moscow"))
        scheduler.add_job(WitchyMood().witch_concern, CronTrigger.from_crontab(cron_concern_time), [bot])
        scheduler.start()
    else:
        witch_log.warning('There is no records in table, sleep for 1h')
        await asyncio.sleep(3600)


async def main():
    main_logger.infolog.info('Logger is ready!')

    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")

    dp.include_router(main_hand.router)
    dp.include_router(conv_hand.router)
    dp.include_router(free_speach_hand.router)
    # asyncio.create_task(marisa_eyes())
    session = aiohttp.ClientSession()
    await session.close()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    warnings.simplefilter('ignore')
    asyncio.run(main())
