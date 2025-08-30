import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8394892914:AAHh4yiPaLCP7JVNEiCQHiqeccATJMXWUG4")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5970095251"))

# Каналы для подписки (реальные ID получены через get_channel_ids.py)
CHANNELS = [
    {"username": "@kinoftvl_1", "name": "Кино ФТВЛ 1", "id": -1002788187895},
    {"username": "@kinoftvl_2", "name": "Kino Top 2", "id": -1003054115835},
    {"username": "@kinoftvl_3", "name": "Kino Top 3", "id": -1003043710593}
]

# База данных
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot_database.db")
