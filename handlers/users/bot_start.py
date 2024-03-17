from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from bot_send.notify_admins import new_user_registration
from loader import dp
from utils.db_api import user_commands as commands
from utils.misc import rate_limit
from keyboards.inline import ikb_subsriber, ikb_menu
from aiogram.types import CallbackQuery

@rate_limit(limit=3)
@dp.message_handler(CommandStart())  # создаем message, который ловит команду /start
async def command_start(message: types.Message):
    args = message.get_args()  # например пользователь пишет /start 1233124 с айди которого пригласил
    new_args = await commands.check_args(args, message.from_user.id)

    try:
        user = await commands.select_user(message.from_user.id)
        if user.status == 'active':
            await message.answer('Бот работает!')
        elif user.status == 'buned':
            await message.answer('Ты забанен')
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                status='active',
                                balance=0,
                                bill_id='')

        # отправляем админам нового пользователя
        await new_user_registration(dp=dp, user_id=message.from_user.id, first_name=message.from_user.first_name,
                                    username=message.from_user.username)

        await message.answer(f'Приветствую, дорогой друг!😜\n'
                             f'Этот бот дает возможность говорить голосами известных людей🤯\n'
                             f'Чтобы начать пользоваться ботом, тебе необходимо подписаться на наш канал, '
                             f'в нем будут собраны все актуальные новости голосового бота\n'
                             f'После чего, выберите в пункте меню команду /voices',
                             reply_markup=ikb_subsriber)


@rate_limit(limit=3)
@dp.message_handler(text="/profile")  # создаем message, который ловит команду /profile
async def get_unban(message: types.Message):  # создаем асинхронную функцию
    user = await commands.select_user(message.from_user.id)
    await message.answer(f'id - {user.user_id}\n'
                         f'first_name: {user.first_name}\n'
                         f'last_name: {user.last_name}\n'
                         f'username: {user.username}\n'
                         f'status: {user.status}')
