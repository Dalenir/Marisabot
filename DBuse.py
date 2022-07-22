from typing import Any

from bata import all_data


async def data_getter(query, return_value: bool = True) -> Any:
    try:
        conn = all_data().get_postg()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if return_value:
                    data = cur.fetchall()
        conn.close()
        if return_value:
            return data
    except Exception as error:
        print(error)
        return False


async def answer_writer(points, user):
    old_points = 0
    quer = f"""CREATE table IF NOT EXISTS public.stats (id serial, time timestamp, points int, user_id bigint);
            INSERT into public.stats (time, points, user_id) values
            (current_timestamp, {int(points)}, {user});
            """
    data = await data_getter(quer, return_value=False)
    return old_points


async def base_sentiency(points, old_points):
    # answer = str()
    previous_points, more_older_points = old_points
    if points > previous_points and points > 0:
        pass


async def time_watcher():
    print('a')
    quer = 'SELECT time from public.stats ORDER BY id limit 1'
    return await data_getter(quer)
