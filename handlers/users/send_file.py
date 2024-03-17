import os
import asyncio
from loader import dp, bot


async def send_audio_to_user(chat_id, file_path, original_filename):
    try:
        # Открываем файл и отправляем его пользователю с исходным именем
        with open(file_path, 'rb') as audio_file:
            await bot.send_audio(chat_id, audio_file, title=original_filename)
    except Exception as e:
        print(f"Не удалось отправить аудио: {e}")


async def check_and_send_audio():
    try:
        out_folder = 'out'
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        while True:
            # Получаем список файлов в папке "out"
            files = os.listdir(out_folder)
            for file in files:
                # Проверяем, является ли файл аудиофайлом формата .mp3 или .wav
                if file.endswith('.mp3') or file.endswith('.wav'):
                    file_path = os.path.join(out_folder, file)
                    # Извлекаем ID пользователя и оригинальное имя файла из имени файла
                    user_id, original_filename = file.split('_')[1:3]
                    # Отправляем аудио пользователю
                    await send_audio_to_user(user_id, file_path, original_filename)
                    # Удаляем отправленный файл
                    os.remove(file_path)

            # Пауза в 5 секунд перед следующей проверкой
            await asyncio.sleep(5)

    except Exception as e:
        print(f"Ошибка в функции check_and_send_audio: {e}")


async def start_background_tasks(dp):
    asyncio.create_task(check_and_send_audio())
