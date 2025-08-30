import asyncio
import logging
import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from handlers import Handlers
from telegram import Update

# Настройка логирования для Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    """Основная функция запуска бота для Railway Worker"""
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", Handlers.start))
        application.add_handler(CallbackQueryHandler(Handlers.handle_callback))
        
        # Обработчик текстовых сообщений (включая админские)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Handlers.handle_text))
        
        # Обработчик фотографий
        application.add_handler(MessageHandler(filters.PHOTO, Handlers.handle_photo))
        
        # Запускаем бота в polling режиме для Railway Worker
        logger.info("Бот запускается на Railway Worker...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        logger.info("Бот успешно запущен и работает в polling режиме")
        
        # Ждем сигнала остановки
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
        finally:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
            
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
        raise

if __name__ == '__main__':
    try:
        # Создаем новый event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        sys.exit(1)
    finally:
        try:
            loop.close()
        except:
            pass
