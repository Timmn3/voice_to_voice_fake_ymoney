from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Старт'),
        types.BotCommand('voices', 'Выбор голосов'),
        types.BotCommand('balance', 'Остаток запросов'),
        types.BotCommand('instruction', 'Инструкция'),
    ])
