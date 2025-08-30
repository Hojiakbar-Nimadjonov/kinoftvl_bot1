#!/usr/bin/env python3
"""
Скрипт для получения реальных ID каналов Telegram
"""

import asyncio
from telegram import Bot
from config import BOT_TOKEN

async def get_channel_info():
    """Получает информацию о каналах"""
    bot = Bot(token=BOT_TOKEN)
    
    # Список каналов для проверки
    channels = [
        "@kinoftvl_1",
        "@kinoftvl_2", 
        "@kinoftvl_3"
    ]
    
    print("🔍 Получаем информацию о каналах...")
    print("=" * 50)
    
    for channel in channels:
        try:
            # Получаем информацию о канале
            chat = await bot.get_chat(channel)
            print(f"📺 Канал: {channel}")
            print(f"   ID: {chat.id}")
            print(f"   Название: {chat.title}")
            print(f"   Тип: {chat.type}")
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ Ошибка при получении информации о {channel}: {e}")
            print("-" * 30)
    
    await bot.close()
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(get_channel_info())
