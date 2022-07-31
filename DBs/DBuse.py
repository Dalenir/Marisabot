import logging
from typing import Any

from bata import AllData
from marisa_log.scribe import witch_error


async def data_getter(query, return_value: bool = True) -> Any:
    try:
        conn = AllData().get_postg()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if return_value:
                    data = cur.fetchall()
        conn.close()
        if return_value:
            return data
    except Exception as error:
        await witch_error(error, __file__)
        return False


async def answer_writer(points, user):
    quer = f"""CREATE table IF NOT EXISTS public.stats (id serial not null constraint stats_pk primary key,
            time timestamp, points int, user_id bigint);
            INSERT into public.stats (time, points, user_id) values
            (current_timestamp, {int(points)}, {user});
            """
    await data_getter(quer, return_value=False)


async def time_watcher():
    quer = 'SELECT time from public.stats ORDER BY id limit 1'
    data = await data_getter(quer)
    if data:
        logging.info(f'Base time is here: {data}\nBot is sending messages every 12h from this time')
        return data[0][0]
    else:
        logging.warning(f'Base time is not here! Atleast one user must complete starting dialog!')
        return False


async def get_old_points(t_id: int):
    quer = f"SELECT points, lag(points, 1) over (ORDER BY time asc) " \
           f"from stats where user_id = {t_id} order by time desc limit 1"
    old_points = await data_getter(quer, return_value=True)
    print(old_points)
    return old_points
