from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from DBs.DBuse import redis_get


class AlcoveFilter(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        path = await redis_get('garden_path')
        print(path)
        if path is not None:
            return True
        else:
            return False
