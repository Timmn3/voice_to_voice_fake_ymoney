import wave
from mutagen.mp3 import MP3


async def get_duration_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration


async def get_duration_mp3(file_path):
    audio = MP3(file_path)
    duration = audio.info.length
    return duration
