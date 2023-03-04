import logging
from typing import Any

import psycopg2

from bata import AllData
from marisa_log.scribe import witch_error
from aiogram.types import User


async def data_getter(query, return_value: bool = True) -> Any:
    try:
        conn = AllData().get_postg()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if return_value:
                    data = cur.fetchall()
        conn.close()
        if return_value and data:
            return data
    except psycopg2.Error as error:
        await witch_error(error, __file__)
        return False


async def answer_writer(points, user):
    quer = f"""CREATE table IF NOT EXISTS public.stats (id serial not null constraint stats_pk primary key,
            time timestamp, points int, user_id bigint);
            INSERT into public.stats (time, points, user_id) values
            (current_timestamp, {int(points)}, {user});
            """
    if await data_getter(quer, return_value=False) is not None:
        raise psycopg2.Error


async def time_watcher():
    quer = 'SELECT time from public.stats ORDER BY id limit 1'
    data = await data_getter(quer)
    if data:
        logging.info(f'Base time is here: {data}\nBot is sending messages every 12h from this time')
        return data[0][0]
    else:
        logging.warning('Base time is not here! Atleast one user must complete starting dialog!')
        return False


async def redis_get(key):
    return AllData().get_data_red().get(key)

async def redis_list(key):
    return AllData().get_data_red().lrange(key, start=0, end=-1)

async def redis_add_to_list(key, value):
    return AllData().get_data_red().lpush(key, value)


async def redis_set(key, value):
    try:
        return AllData().get_data_red().set(key, value)
    except Exception as error:
        await witch_error(error, __file__)


class BadGuest(Exception):
    def __init__(self, error_text):
        super().__init__(error_text)


class WitchGuest:
    def __init__(self, telegram_id: int | None = None):
        self.id = telegram_id
        self.full_name = None
        self.username = None
        self.mood_diary_concern = None
        self.everyday_task_concern = None

    async def get_user(self):
        q = f'SELECT username, fullname, mood_concern, tasks_concern FROM public.users WHERE t_id = {self.id}'
        userdata = await data_getter(q)
        if userdata:
            self.username = userdata[0][0]
            self.full_name = userdata[0][1]
            self.mood_diary_concern = userdata[0][2]
            self.everyday_task_concern = userdata[0][3]
            return self
        else:
            raise BadGuest('Guest with given id is not found')

    async def save_answer(self, points):
        q = f"""INSERT into public.stats (time, points, user_id) values
         (current_timestamp, {int(points)}, {self.id});
            """
        await data_getter(q, return_value=False)

    async def switch_mood_diary(self):
        if self.mood_diary_concern is None:
            await self.get_user()
        self.mood_diary_concern = False if self.mood_diary_concern else True
        q = f"""
            UPDATE public.users SET mood_concern = {self.mood_diary_concern} WHERE t_id = {self.id}
                """
        await data_getter(q, return_value=False)

    async def switch_everyday_tasks(self):
        if self.everyday_task_concern is None:
            await self.get_user()
        self.everyday_task_concern = False if self.everyday_task_concern else True
        q = f"""
            UPDATE public.users SET mood_concern = {self.everyday_task_concern} WHERE t_id = {self.id}
                """
        await data_getter(q, return_value=False)

    async def create(self, user: User):
        self.id = user.id
        try:
            await self.get_user()
        except BadGuest:
            q = f"INSERT INTO public.users(t_id, username, fullname) VALUES " \
                f"({user.id}, '{user.username}', '{user.full_name}')"
            await data_getter(q, return_value=False)
        return await self.get_user()

    async def get_old_points(self):
        quer = f"SELECT points, lag(points, 1) over (ORDER BY time) " \
               f"from stats where user_id = {self.id} order by time desc limit 1"
        old_points = await data_getter(quer, return_value=True)
        return old_points
