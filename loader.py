from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.db_gino import db

# создаем переменную бота с токеном нашего бота
bot = Bot(token=config.bot_token, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

# создаем диспетчер
dp = Dispatcher(bot, storage=storage)


__all__ = ['bot', 'storage', 'dp', 'db']
