from aiogram import Router, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from states import SmTestState

router = Router()


@router.message(commands=['smoke_test'])
async def smoketesting(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(SmTestState.smoke)
    msg = await message.answer('Smoketesting was successfull')
    await state.clear()
    await bot.session.close()
    return msg.text
