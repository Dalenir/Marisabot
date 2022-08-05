import os

import psycopg2
from aiogram import Bot
from redis import from_url


class AllData:
    def __init__(self):
        self.redis_url = 'redis://Witch_garden:2769'
        self.bot_token = os.getenv('BOT_TOKEN')
        self.master = (459509035, 319736241)

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
        return from_url('redis://Witch_garden:2769/1', decode_responses=True)
