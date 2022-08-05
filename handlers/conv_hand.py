import asyncio

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DBs.DBuse import redis_get
from Filters.alchemic_filters import AlcoveFilter
from states import MarisaStates

router = Router()


@router.message(F.text == 'В ведьминский сад')
async def garden_start(message: Message, state: FSMContext):
    await state.set_state(MarisaStates.garden)
    path = await redis_get('garden_path')
    print(path)
    if path is None:
        await message.answer('<i>Сад на заднем дворе дома Марисы.\n\nМогучие деревья со стволами, закрученными '
                             'спиралью, стоят среди непроходимых зарослей бурьяна. Где-то за ними виднеется белая '
                             'беседка, но пока что к ней никак не подобраться...</i>')
        await asyncio.sleep(10)
        await message.answer('<i>Шаги за спиной. Мариса тоже выглядывает в сад.</i>')
        await asyncio.sleep(3)
        await message.answer('— Ну да. Я не особо за ним следила, вот он и зарос. А было бы так приятно посидеть '
                             'в моей беседке... Она всегда наводила меня на итересные мысли.')
        await asyncio.sleep(5)
        await message.answer('— Чтобы попасть в беседку, нам всего лишь нужен какой-то путь. '
                             '<a href="https://nevercode.jetbrains.space/p/mar/issues/22">Любой</a>, в общем-то.\n\n'
                             'Ну или можно пробраться туда секретной тропой, но я совсем не помню где ее искать. '
                             'Думаю, что след этой тропы можно найти там, где сотворялся мой мир и этот сад.',
                             disable_web_page_preview=True)
    else:
        markup = ReplyKeyboardBuilder()
        markup.row(types.KeyboardButton(text="В ведьминскую беседку"))
        await message.answer('<i>Сад на заднем дворе дома Марисы.\n\nМогучие деревья со стволами, закрученными '
                             'спиралью, стоят среди непроходимых зарослей бурьяна. Где-то за ними виднеется белая '
                             f'беседка.\n\nК ней ведет {path}</i>', reply_markup=markup.as_markup(resize_keyboard=True))


@router.message(F.text == 'Воспользоваться секретным путем: перепрыгнуть через кусты ежевики, проползти под ядовитым '
                          'плющом, избежать укуса тех странных цветов из марио, и устало рухнуть на ступени беседки!')
# Похоже, что строка выше позволит пробраться в беседку, не создавая в нее путь. Но ее придется вводить каждый раз.
@router.message(AlcoveFilter(), (F.text.contains('беседку')), state=MarisaStates.garden)
async def alcove_start(message: Message, state: FSMContext):
    await state.set_state(MarisaStates.alcove)
    await message.answer('<i>Мариса заходит в беседку, садится на уютную лавочку и начинает тихонько напевать, '
                         'рассеянно поглядывая наружу. Похоже, что через некоторое время она захочет поговорить.</i>')
