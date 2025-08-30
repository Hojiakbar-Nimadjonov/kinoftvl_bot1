import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8394892914:AAHh4yiPaLCP7JVNEiCQHiqeccATJMXWUG4")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5970095251"))

# Каналы для подписки
CHANNELS = [
    {"username": "@kinoftvl_1", "name": "Кино ФТВЛ 1", "id": int(os.getenv("CHANNEL_1_ID", "-1001234567890"))},
    {"username": "@kinoftvl_2", "name": "Кино ФТВЛ 2", "id": int(os.getenv("CHANNEL_2_ID", "-1001234567891"))},
    {"username": "@kinoftvl_3", "name": "Кино ФТВЛ 3", "id": int(os.getenv("CHANNEL_3_ID", "-1001234567892"))}
]

# База данных
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot_database.db")
