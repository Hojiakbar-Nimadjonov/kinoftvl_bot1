import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from handlers import Handlers
from telegram import Update

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", Handlers.start))
    application.add_handler(CallbackQueryHandler(Handlers.handle_callback))
    
    # Обработчик текстовых сообщений (включая админские)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Handlers.handle_text))
    
    # Обработчик фотографий
    application.add_handler(MessageHandler(filters.PHOTO, Handlers.handle_photo))
    
    # Запускаем бота
    logger.info("Бот запускается...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
