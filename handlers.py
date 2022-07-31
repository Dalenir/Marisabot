import asyncio

from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import bata
from DBs.DBuse import answer_writer, get_old_points
from resources.bunch_of_variables import simple_answers
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
    print(f"Answer is {query.data}")
    await state.set_state(MarisaStates.sleepmode)
    await query.answer()
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    await answer_writer(int(query.data), query.from_user.id)
    await query.message.answer('Серьезно? А я бы дала себе 10 баллов.\n\nПритворюсь, что не слышала этого.'
                               '\nБудем считать это твоим первым ответом о настроении. А теперь прости,'
                               ' мне пора спать 12 часов, чтобы спросить тебя вновь...')


@router.message(commands=['test'])
async def marisa_awaikens(message, bot: Bot):
    nmarkup = InlineKeyboardBuilder()
    for points in all_points:
        nmarkup.button(text=str(points), callback_data=str(points))
    nmarkup.adjust(3)
    if message:
        key, hello_text = str(), str()
        old_points = (await get_old_points(message.from_user.id))[0][0]
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
        await message.answer(hello_text, reply_markup=nmarkup.as_markup())
    else:
        for uid in bata.AllData().master:
            key, hello_text = str(), str()
            old_points = (await get_old_points(uid))[0][0]
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
            await bot.send_message(uid, hello_text, reply_markup=nmarkup.as_markup())


@router.callback_query((lambda call: int(call.data) in all_points))
async def marisa_answer(query: types.CallbackQuery, bot: Bot, state: FSMContext):
    print(f"Answer is {query.data}")
    await state.set_state(MarisaStates.sleepmode)
    await query.answer()
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    await answer_writer(int(query.data), query.from_user.id)
    await query.message.answer('Надеюсь, тебе нравится моя'
                               ' ведьминская визуализация твоих ответов, потому что я все еще не научилась нормально '
                               'реагировать в зависимости от того, как ты отвечал до этого... Но я стараюсь!')
