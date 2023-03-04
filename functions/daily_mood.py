from datetime import datetime

from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from DBs.DBuse import data_getter, WitchGuest
from handlers.main_hand import all_points
from resources.bunch_of_variables import simple_answers


class WitchyMood:
    def __init__(self, custom_list: None | list[WitchGuest] = None):
        self.concern_list = custom_list if custom_list else list()

    async def fill_concern_list(self):
        users_ids = await data_getter("SELECT t_id from postgres.public.users where mood_concern = True")
        for user_id in users_ids:
            self.concern_list.append(await WitchGuest(user_id[0]).get_user())

    async def witch_concern(self, bot: Bot):
        print(datetime.now())
        if not self.concern_list:
            await self.fill_concern_list()

        nmarkup = InlineKeyboardBuilder()
        for points in all_points:
            nmarkup.button(text=str(points), callback_data=str(points))
        nmarkup.adjust(3)

        for guest in self.concern_list:
            key, hello_text = str(), str()
            old_points = (await guest.get_old_points())[0][0]
            if old_points == -3:
                key = "Very bad"
            elif old_points == -2:
                key = "Bad"
            elif old_points == -1:
                key = "Little bad"
            elif old_points == 1:
                key = "Little good"
            elif old_points == 2:
                key = "Good"
            elif old_points == 3:
                key = "Very good"
            hello_text = simple_answers[key]
            await bot.send_message(guest.id, hello_text, reply_markup=nmarkup.as_markup())
