from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from filters.by_balance import PositiveBalance
from filters import IsSubsriber
from keyboards.inline import ikb_menu
from loader import dp
import os

from states import Audio

# Путь к папке со звуковыми файлами
SOUNDS_FOLDER = 'examples of sounds'


# Если команда menu, то выводи инлайн клавиатуру
@dp.message_handler(IsSubsriber(), Command('voices'))
async def menu(message: types.Message):
    await message.answer('Поздравляем🎉'
                         'Теперь вам доступно множество голосов известных людей😎'
                         'Творите!', reply_markup=ikb_menu)


# Функция для отправки аудиофайла
async def send_audio_file(call: CallbackQuery, audio_name):
    audio_path = os.path.join(SOUNDS_FOLDER, audio_name)
    if os.path.exists(audio_path):
        name = audio_name.replace(".wav", "")
        # Передаем переменную name в состояние FSMContext
        await Audio.voice.set()
        await dp.storage.update_data(user=call.from_user.id,
                                     data={"name": name})  # Сохраняем переменную name в состояние
        with open(audio_path, 'rb') as audio_file:
            await dp.bot.send_audio(call.message.chat.id, audio=audio_file, title=f'Пример голоса: {name}🔊\n',
                                    caption=f'Отправьте мне аудиофайл длиной до 30 секунд (*.mp3 или *.wav) '
                                            f'или напишите слово "отмена"')
        # await call.message.answer('кидай файл')
    else:
        await call.message.answer(f'Файл с аудио {audio_name} не найден.')


def create_audio_handler(text, audio_file):
    @dp.callback_query_handler(PositiveBalance(), IsSubsriber(), text=text)
    async def send_message(call: CallbackQuery):
        await send_audio_file(call, audio_file)


create_audio_handler("Мориарти", "Мориарти.wav")
create_audio_handler("Моргенштерн", "Моргенштерн.wav")
create_audio_handler("Нолик", "Нолик.wav")
create_audio_handler("Иванзоло", "Иванзоло.wav")
create_audio_handler("Ева Элфи", "Ева Элфи.wav")
create_audio_handler("Kussia", "Kussia.wav")
