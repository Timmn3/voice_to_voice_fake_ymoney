from aiogram import Dispatcher
from data.config import admins
from utils.db_api.user_commands import count_users
from loguru import logger


async def on_startup_notufy(dp: Dispatcher):
    for admin in admins:
        try:
            text = 'Бот запущен'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logger.error(err)


# отправляет сообщение админам о новом зарегистрированном пользователе
async def new_user_registration(dp: Dispatcher, user_id, first_name, username):
    count = await count_users()
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text=f'✅Зарегистрирован новый пользователь:\n'
                                                          f'user_id: {user_id}\n'
                                                          f'first_name: {first_name}\n'
                                                          f'username: {username}\n'
                                                          f'🚹Всего пользователей: <b>{count}</b>')
        except Exception as err:
            logger.error(err)


async def send_admins(dp: Dispatcher, text):
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logger.error(err)
