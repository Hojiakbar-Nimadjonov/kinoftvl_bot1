import asyncio
import logging
import os
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
    """Основная функция запуска бота для Railway"""
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
    logger.info("Бот запускается на Railway...")
    
    # Для Railway используем webhook если есть URL, иначе polling
    if os.getenv('RAILWAY_STATIC_URL'):
        # Webhook режим для Railway
        webhook_url = f"{os.getenv('RAILWAY_STATIC_URL')}/webhook"
        await application.initialize()
        await application.bot.set_webhook(url=webhook_url)
        await application.start()
        logger.info(f"Webhook установлен на {webhook_url}")
        
        # Ждем сигнала остановки
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
        finally:
            await application.bot.delete_webhook()
            await application.stop()
            await application.shutdown()
    else:
        # Polling режим для локальной разработки
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
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
    finally:
        try:
            loop.close()
        except:
            pass
