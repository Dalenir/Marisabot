import psycopg2
from bata import all_data
import os


async def data_getter(query):
    try:
        conn = all_data().get_postg()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        conn.close()
        return data
    except Exception as error:
        print(error)
        return False


async def answer_writer(points, user):
    quer = f"""CREATE table IF NOT EXISTS public.stats (id serial, time timestamp, points int, user_id int);
            INSERT into public.stats (time, points, user_id) values
            (current_timestamp, {int(points)}, {user}) returning 
            (select points from public.stats where user_id = {user} order by id desc limit 1) as before,
            (SELECT lag(points, 1) over (order by id asc) from public.stats
            WHERE user_id = {user} order by id desc limit 1) as long_before;
            """
    old_points = (await data_getter(quer))[0]
    print(old_points)
    return old_points


async def base_sentiency(points, old_points):
    answer = str()
    previous_points, more_older_points = old_points
    if points > previous_points and points > 0:
        pass


async def time_watcher():
    print('a')
    quer = 'SELECT time from public.stats ORDER BY id asc limit 1'
    return await data_getter(quer)
