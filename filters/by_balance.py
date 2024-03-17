from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from keyboards.inline import ikb_balance
from keyboards.inline.ikb_balance import ikb_support_financially
from loader import dp
from utils.db_api import user_commands as commands


class PositiveBalance(BoundFilter):  # проверка достаточный ли баланс
    async def check(self, message: types.Message):
        # все пользователи из БД c позитивным балансом
        users = str(await commands.select_all_users_big_balance())
        # id пользователя
        user = str(message.from_user.id)

        if user in users:
            return True
        else:
            await dp.bot.send_message(chat_id=user,
                                      text='Чтобы получить свой запрос, необходимо пополнить баланс, '
                                           'вы можете выбрать один из нескольких вариантов👻',
                                      reply_markup=ikb_balance)
            await dp.bot.send_message(chat_id=user,  # Предоставьте аргумент chat_id, если это необходимо
                                      text='Также вы можете поддержать нас😎\n'
                                           'Благодаря донатам цены запросов💰 и время ожидания🕰️ '
                                           'будут становиться все меньше и меньше🎉',
                                      reply_markup=ikb_support_financially)
            return False
