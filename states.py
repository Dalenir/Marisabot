from aiogram.dispatcher.fsm.state import State, StatesGroup


class MarisaStates(StatesGroup):
    start = State()
    sleepmode = State()
    awakemode = State()
    garden = State()
    alcove = State()


class SmTestState(StatesGroup):
    smoke = State()
