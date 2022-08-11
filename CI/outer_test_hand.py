from aiogram import Router
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message()
@router.callback_query()
async def smoketesting(update: Message | CallbackQuery | None):
    raise Exception('MESSAGE WAS NOT HANDLED RIGHT')
