import os

from dotenv import load_dotenv

# запускаем функцию, которая загружает переменное окружение из файла .env
load_dotenv()

# Токен бота
bot_token = str(os.getenv('BOT_TOKEN'))

# список администраторов бота
admins = [os.getenv('ADMINS')]

chat_ids = [os.getenv('CHAT_IDS')]
url_chat = str(os.getenv('URL_CHAT'))

ip = os.getenv('IP')

PG_USER = str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{ip}/{DATABASE}'

YOOMONEY_TOKEN = str(os.getenv('YOOMONEY_TOKEN'))

wallet_number = str(os.getenv('WALLET_NUMBER'))