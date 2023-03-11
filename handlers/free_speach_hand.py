from aiogram import Router
from aiogram.types import Message

from AI.ai_requests import ai_sentient_witch

router = Router()

@router.message()
async def witch_talking(message: Message):
    response = await ai_sentient_witch(new_text=message.text, user_id=message.from_user.id)
    await message.answer(response)
