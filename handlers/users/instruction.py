from aiogram import types

from keyboards.inline import ikb_menu
from loader import dp
from aiogram.dispatcher.filters import Command
from filters import IsSubsriber

instruction = (f'<b>❗️Инструкция❗️</b>\n'
               f'Выберите из списка голос известного человека/персонажа😎!\n'
               f'Отправьте аудиосообщение формата .WAV или .mp3 (не голосовое, а именно .WAV или .mp3)🔈\n'
               f'Если вы передумаете и захотите изменить персонажа, то напишите "отмена"🔇\n'
               f'Через некоторое время бот пришлет готовую речь!')


@dp.message_handler(Command('instruction'))
async def menu(message: types.Message):
    await message.answer(instruction, reply_markup=ikb_menu)
