import os
from functools import lru_cache

import psycopg2
from aiogram import Bot
from pydantic import BaseSettings, validator
from redis import from_url


class AllData:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.master = (459509035, 319736241)
        self.aitoken = os.getenv('AI_TOKEN')
        self.redis_pass = os.getenv('RED_PASS')
        self.redis_url = f'redis://:{self.redis_pass}@Witch_garden:2769'

    def get_bot(self):
        return Bot(self.bot_token, parse_mode="HTML")

    @staticmethod
    def get_postg():
        return psycopg2.connect(database="postgres", user="postgres", password=os.getenv('POSTGRES_PASSWORD'),
                                host="Witch_stash", port=5432)

    def get_red(self):
        return from_url(self.redis_url, decode_responses=True)

    @staticmethod
    def get_data_red():
        return from_url(f'redis://:{os.getenv("RED_PASS")}@Witch_garden:2769/1', decode_responses=False)


class NormalSettings(BaseSettings):
    AI_FULL_LIMIT: int
    AI_OUT_LIMIT: int
    AI_IN_LIMIT: int = None

    @validator("AI_IN_LIMIT", always=True)
    def create_in(cls, value, values):
        print(values)
        return values["AI_FULL_LIMIT"] - values["AI_OUT_LIMIT"]


@lru_cache()
def get_settings():
    return NormalSettings()

settings = get_settings()