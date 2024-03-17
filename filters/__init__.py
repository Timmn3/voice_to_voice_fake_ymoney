from aiogram import Dispatcher
from .subscription import IsSubsriber
from .admins import Admins_message


# функция, которая выполняет установку кастомных фильтов
def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsSubsriber)  # проверка подписки на канал
    dp.filters_factory.bind(Admins_message)  # сообщения только для админов