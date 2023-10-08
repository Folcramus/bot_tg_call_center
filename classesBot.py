from aiogram.filters.state import State, StatesGroup


class MyDialog(StatesGroup):
    otvet = State()
    cool = State()
