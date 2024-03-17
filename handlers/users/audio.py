from aiogram import types

from keyboards.inline import ikb_menu
from loader import dp
from io import BytesIO
from aiogram.dispatcher import FSMContext
from loguru import logger
import os
from states import Audio
from utils.db_api.user_commands import change_balance
from utils.misc.audio_duration import get_duration_mp3, get_duration_wav

allowed_extensions = {types.ContentType.AUDIO: '.mp3', types.ContentType.DOCUMENT: '.wav'}
text = ('Файл должен иметь расширение .mp3 или .wav\n'
        'Вы можете сделать mp3 файл через диктофон своего телефона или любым другим способом, а потом отправить файл')


@dp.message_handler(state=Audio.voice, content_types=[types.ContentType.DOCUMENT, types.ContentType.AUDIO,
                                                      types.ContentType.TEXT])
async def handle_audio_message(message: types.Message, state: FSMContext):
    try:
        content = message.content_type
        # Проверяем, если текст сообщения - "отмена"
        if content == types.ContentType.TEXT:
            if message.text.lower() == 'отмена':
                await message.answer('Отменено')
                await state.finish()
                return
            else:
                await message.answer(text)
                return

        user_data = await dp.storage.get_data(user=message.from_user.id)
        voice_name = f'Голос: {user_data.get("name", "Неизвестный")}'
        name = user_data.get("name", "Неизвестный")
        file_extension = None
        if content == types.ContentType.DOCUMENT:
            file_extension = os.path.splitext(message.document.file_name)[1]
        elif content == types.ContentType.AUDIO:
            file_extension = os.path.splitext(message.audio.file_name)[1]

        if file_extension not in allowed_extensions.values(): # проверяем расширение файла
            await message.reply(text)
            await state.finish()
            return

        audio = BytesIO()
        length_audio = 0
        if content == types.ContentType.DOCUMENT:
            audio.name = message.document.file_name
            await message.document.download(destination_file=audio)
            length_audio = await get_duration_wav(audio)  # проверяем длительность файла wav
        elif content == types.ContentType.AUDIO:
            audio.name = message.audio.file_name
            await message.audio.download(destination_file=audio)
            length_audio = await get_duration_mp3(audio)  # проверяем длительность файла mp3

        if length_audio > 30:
            await message.answer('Длинна файла не должна быть больше 30 секунд, отправьте файл заново или напишите'
                                 ' "отмена"')
            return
        else:
            await message.answer('Отлично! Ваш запрос принят, ожидайте свою генерацию😁')
            await change_balance(message.chat.id, -1)  # снимаем баланс
            await save_voice(name, audio, message)
            await state.finish()

    except Exception as e:
        logger.exception(f'Ошибка wait_voice: {e}')
        await state.finish()


async def save_voice(name, audio, message):
    try:
        content = message.content_type
        # await message.answer('Подождите...')
        user_id = str(message.chat.id)
        # сохранить audio в коневую папку in в формате: name_audio.name_user_id
        file_name = f'{name}_{user_id}_{audio.name}'
        if content == types.ContentType.DOCUMENT:
            await message.document.download(destination_file=f'in/{file_name}')
        elif content == types.ContentType.AUDIO:
            await message.audio.download(destination_file=f'in/{file_name}')

    except Exception as e:
        logger.error(f'Ошибка save_voice: {e}')


@dp.message_handler(content_types=[types.ContentType.DOCUMENT, types.ContentType.AUDIO])
async def wait_audio(message: types.Message):
    """ если пользователь отправляет файл, не выбрав звуковую """
    await message.answer('Сначала выберите модель голоса', reply_markup=ikb_menu)
