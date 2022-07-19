from aiogram import Bot
import psycopg2
from redis import from_url
import pymongo


class all_data():
    def __init__(self):
        self.redis_url = 'redis://:dZ9rnNNXZtps3wkjz8PcQJEVMTJWx2LqtjcAQzuclJ1zYcDiXGTobChpsUnZ8JJGgWiLCIL@127.0.0.1:6379'
        self.bot_token = '5566375516:AAF60vyfpAIJKSrnvSLToKlUO_ypqYltekc'
        self.timetime = None
        self.master = (319736241, 319736241)

    def get_bot(self):
        return Bot(self.bot_token, parse_mode="HTML")

    def get_postg(self):
        return psycopg2.connect(database="postgres", user="postgres", password="baka", host="localhost", port=5432)

    def get_red(self):
        return from_url(self.redis_url, decode_responses=True)

    def get_data_red(self):
        return from_url('redis://nobaka@localhost:6379/1', decode_responses=True)



#Settings:

Check_tickets = False