#!/usr/bin/env python3
"""
Простой тестовый бот для отладки поиска
"""

import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from database import Database

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db = Database()

async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет! Я тестовый бот. Отправь мне код фильма (например: #123)")

async def handle_text(update, context):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user_id = update.effective_user.id
    
    print(f"📨 Получено сообщение: '{text}' от пользователя {user_id}")
    
    if text.startswith('#'):
        print(f"🔍 Начинаем поиск фильма: {text}")
        
        try:
            # Ищем фильм в базе
            film = db.get_film_by_code(text)
            print(f"📽️ Результат поиска: {film}")
            
            if film:
                print(f"✅ Фильм найден: {film['title']}")
                
                # Отправляем информацию о фильме
                await update.message.reply_text(
                    f"🎬 Найден фильм!\n\n"
                    f"📽️ Название: {film['title']}\n"
                    f"🔗 Ссылка: {film['link']}\n"
                    f"🆔 Код: {film['code']}"
                )
                print(f"✅ Фильм отправлен пользователю {user_id}")
            else:
                print(f"❌ Фильм не найден")
                await update.message.reply_text(f"❌ Фильм с кодом {text} не найден")
                
        except Exception as e:
            print(f"❌ Ошибка при поиске: {e}")
            import traceback
            traceback.print_exc()
            await update.message.reply_text(f"❌ Ошибка при поиске: {e}")
    else:
        await update.message.reply_text("Отправь код фильма, начиная с # (например: #123)")

async def main():
    """Основная функция"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Запускаем бота
    logger.info("Тестовый бот запускается...")
    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
