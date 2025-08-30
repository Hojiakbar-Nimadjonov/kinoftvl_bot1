#!/usr/bin/env python3
"""
Скрипт для получения ID каналов Telegram
Используйте этот скрипт, чтобы получить правильные ID для config.py
"""

import asyncio
from telegram import Bot
from config import BOT_TOKEN

async def get_channel_info():
    """Получение информации о каналах"""
    bot = Bot(token=BOT_TOKEN)
    
    channels = [
        "@kinoftvl_1",
        "@kinoftvl_2", 
        "@kinoftvl_3"
    ]
    
    print("🔍 Получение информации о каналах...")
    print("=" * 50)
    
    for channel in channels:
        try:
            # Получаем информацию о чате
            chat = await bot.get_chat(channel)
            print(f"📺 Канал: {channel}")
            print(f"   Название: {chat.title}")
            print(f"   ID: {chat.id}")
            print(f"   Тип: {chat.type}")
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ Ошибка при получении информации о {channel}: {e}")
            print("-" * 30)
    
    await bot.close()

if __name__ == "__main__":
    print("🚀 Запуск скрипта получения ID каналов...")
    print("Убедитесь, что бот добавлен во все каналы как администратор!")
    print()
    
    try:
        asyncio.run(get_channel_info())
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n📝 Скопируйте полученные ID в config.py")
    print("Пример:")
    print("CHANNELS = [")
    print('    {"username": "@kinoftvl_1", "name": "Кино ФТВЛ 1", "id": РЕАЛЬНЫЙ_ID_1},')
    print('    {"username": "@kinoftvl_2", "name": "Кино ФТВЛ 2", "id": РЕАЛЬНЫЙ_ID_2},')
    print('    {"username": "@kinoftvl_3", "name": "Кино ФТВЛ 3", "id": РЕАЛЬНЫЙ_ID_3}')
    print("]")
