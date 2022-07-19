import asyncio
import csv
from typing import Union
from datetime import timedelta, datetime

from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


import bata
from DBuse import answer_writer, time_watcher
from states import MarisaStates

router = Router()
all_points = (1, 2, 3, -1, -2, -3)


@router.message(commands=['start'])
async def commands_start(message: types.Message, state: FSMContext):
    if await state.get_state() == 'MarisaStates:sleepmode':
        return
    await state.set_state(MarisaStates.start)
    await message.answer('Здравствуй! С этого момента я каждый день буду дважды спрашивать'
                         ' тебя о том, как у тебя дела!')
    await asyncio.sleep(3)
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.add(types.KeyboardButton(text='А ты точно Мариса?'))
    await message.answer('Пожалуйста, не блокируй меня, и не злись, а просто нажимай на одну из кнопок — это'
                         'весь фидбек, который я прошу, и который могу принимать. Возможно, некая ленивая жопа допилит'
                         'меня чуть лучше, но пока что он предвкушает возню с базами данных, и поэтому решает не рас'
                         'ширять функционал.\n\nДавай потренируемся?', reply_markup=nmarkup.as_markup())


@router.message(F.text == 'А ты точно Мариса?')
async def trap(message: Message):
    nmarkup = InlineKeyboardBuilder()
    for points in all_points:
        nmarkup.button(text=str(points), callback_data=str(points))
    nmarkup.adjust(3)
    await message.answer('Конечно!', reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await message.answer('Неужели у тебя есть в этом хоть малейшее сомнение?.. А ну-ка \n'
                         '\nоцени, насколько я Мариса по шкале от -3 до 3:', reply_markup=nmarkup.as_markup())


@router.callback_query((lambda call: int(call.data) in all_points), state=MarisaStates.start)
async def trap_answer(query: types.CallbackQuery, bot: Bot, state: FSMContext):
    print(query.data)
    await state.set_state(MarisaStates.sleepmode)
    await query.answer()
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    await answer_writer(int(query.data))
    await query.message.answer('Серьезно? А я бы дала себе 10 баллов.\n\nПритворюсь, что не слышала этого.'
                         '\nБудем считать это твоим первым ответом о настроении. А теперь прости,'
                         ' мне пора спать 12 часов, чтобы спросить тебя вновь...')


@router.message(commands=['test'])
async def marisa_awaikens(message: Union[Message, None], bot: Bot):
    nmarkup = InlineKeyboardBuilder()
    for points in all_points:
        nmarkup.button(text=str(points), callback_data=str(points))
    nmarkup.adjust(3)
    for uid in bata.all_data().master:
        await bot.send_message(uid, 'Привет! Это я! Как ты себя чувствуешь?', reply_markup=nmarkup.as_markup())


@router.callback_query((lambda call: int(call.data) in all_points), state=MarisaStates.sleepmode)
async def marisa_answer(query: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MarisaStates.sleepmode)
    await query.answer()
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    await answer_writer(int(query.data), query.from_user.id)
    await query.message.answer('Я очень рада, что ты со мной поделился! Встретимся через 12 часов, а пока... '
                               '\nGambare!')
