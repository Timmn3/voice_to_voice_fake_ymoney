from aiogram.dispatcher.filters.state import StatesGroup, State


class Audio(StatesGroup):
    voice = State()