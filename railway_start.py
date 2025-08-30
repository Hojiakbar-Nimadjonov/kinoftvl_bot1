import asyncio
import logging
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, ADMIN_ID
from database import Database

# Настройка логирования для Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db = Database()

async def start(update, context):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    
    if user_id == ADMIN_ID:
        # Админ-панель
        keyboard = [
            [InlineKeyboardButton("➕ Добавить фильм", callback_data="admin_add_film")],
            [InlineKeyboardButton("✏️ Редактировать фильм", callback_data="admin_edit_film")],
            [InlineKeyboardButton("🗑 Удалить фильм", callback_data="admin_delete_film")],
            [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton("🔍 Поиск фильма", callback_data="search_film")]
        ]
        text = "🎬 Добро пожаловать в админ-панель!\n\n👑 Вы вошли как администратор"
    else:
        # Обычное меню
        keyboard = [
            [InlineKeyboardButton("🔍 Поиск фильма", callback_data="search_film")]
        ]
        text = "🎬 Добро пожаловать в бот для просмотра фильмов!\n\nВведите код фильма (например: #123) или используйте меню"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_text(update, context):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user_id = update.effective_user.id
    
    print(f"📨 Получено сообщение: '{text}' от пользователя {user_id}")
    
    # Проверяем, не является ли это админским сообщением
    if user_id == ADMIN_ID and 'admin_action' in context.user_data:
        await handle_admin_text(update, context)
        return
    
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

async def handle_callback(update, context):
    """Обработчик callback запросов"""
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    await query.answer()
    
    if data == "search_film":
        await query.edit_message_text(
            "🔍 Введите код фильма, начиная с символа # (например: #123)"
        )
    
    elif data == "admin_add_film":
        if user_id == ADMIN_ID:
            await start_add_film(update, context)
        else:
            await query.edit_message_text("❌ Доступ запрещен")
    
    elif data == "admin_edit_film":
        if user_id == ADMIN_ID:
            await start_edit_film(update, context)
        else:
            await query.edit_message_text("❌ Доступ запрещен")
    
    elif data == "admin_delete_film":
        if user_id == ADMIN_ID:
            await start_delete_film(update, context)
        else:
            await query.edit_message_text("❌ Доступ запрещен")
    
    elif data == "admin_stats":
        if user_id == ADMIN_ID:
            await show_stats(update, context)
        else:
            await query.edit_message_text("❌ Доступ запрещен")
    
    elif data == "back_to_admin":
        if user_id == ADMIN_ID:
            await start(update, context)
        else:
            await query.edit_message_text("❌ Доступ запрещен")

async def start_add_film(update, context):
    """Начало процесса добавления фильма"""
    query = update.callback_query
    
    # Сохраняем состояние
    context.user_data['admin_action'] = 'add_film'
    context.user_data['step'] = 'code'
    
    await query.edit_message_text(
        "➕ Добавление нового фильма\n\n"
        "Введите код фильма (например: #123):"
    )

async def start_edit_film(update, context):
    """Начало процесса редактирования фильма"""
    query = update.callback_query
    
    # Сохраняем состояние
    context.user_data['admin_action'] = 'edit_film'
    context.user_data['step'] = 'code'
    
    await query.edit_message_text(
        "✏️ Редактирование фильма\n\n"
        "Введите код фильма для редактирования:"
    )

async def start_delete_film(update, context):
    """Начало процесса удаления фильма"""
    query = update.callback_query
    
    # Сохраняем состояние
    context.user_data['admin_action'] = 'delete_film'
    context.user_data['step'] = 'code'
    
    await query.edit_message_text(
        "🗑 Удаление фильма\n\n"
        "Введите код фильма для удаления:"
    )

async def show_stats(update, context):
    """Показать статистику"""
    query = update.callback_query
    
    try:
        stats = db.get_today_stats()
        
        keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_admin")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📊 Статистика за сегодня\n\n"
            f"👀 Просмотров фильмов: {stats['views_today']}\n"
            f"👥 Новых пользователей: {stats['new_users_today']}",
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка при получении статистики: {e}")

async def handle_admin_text(update, context):
    """Обработчик текстовых сообщений для админа"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        return
    
    if 'admin_action' not in context.user_data:
        return
    
    action = context.user_data['admin_action']
    step = context.user_data.get('step', '')
    text = update.message.text
    
    if action == 'add_film':
        await process_add_film(update, context, step, text)
    elif action == 'edit_film':
        await process_edit_film(update, context, step, text)
    elif action == 'delete_film':
        await process_delete_film(update, context, step, text)

async def process_add_film(update, context, step, text):
    """Обработка добавления фильма пошагово"""
    if step == 'code':
        if not text.startswith('#'):
            await update.message.reply_text("❌ Код должен начинаться с символа #")
            return
        
        context.user_data['film_code'] = text
        context.user_data['step'] = 'title'
        
        await update.message.reply_text("Введите название фильма:")
    
    elif step == 'title':
        context.user_data['film_title'] = text
        context.user_data['step'] = 'cover'
        
        await update.message.reply_text(
            "Отправьте обложку фильма (фото):"
        )
    
    elif step == 'link':
        context.user_data['film_link'] = text
        
        # Сохраняем фильм в базу
        code = context.user_data['film_code']
        title = context.user_data['film_title']
        cover = context.user_data['film_cover']
        link = text
        
        if db.add_film(code, title, cover, link):
            await update.message.reply_text(
                f"✅ Фильм {code} успешно добавлен!\n\n"
                f"Название: {title}\n"
                f"Ссылка: {link}"
            )
        else:
            await update.message.reply_text("❌ Ошибка при добавлении фильма")
        
        # Очищаем состояние
        context.user_data.clear()
        
        # Возвращаемся в админ-меню
        keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_admin")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def process_edit_film(update, context, step, text):
    """Обработка редактирования фильма пошагово"""
    if step == 'code':
        film = db.get_film_by_code(text)
        if not film:
            await update.message.reply_text("❌ Фильм не найден")
            return
        
        context.user_data['film_code'] = text
        context.user_data['step'] = 'choose_field'
        
        keyboard = [
            [InlineKeyboardButton("Название", callback_data="edit_title")],
            [InlineKeyboardButton("Обложку", callback_data="edit_cover")],
            [InlineKeyboardButton("Ссылку", callback_data="edit_link")],
            [InlineKeyboardButton("Код", callback_data="edit_code")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_admin")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"✏️ Редактирование фильма {text}\n\n"
            f"Выберите, что хотите изменить:",
            reply_markup=reply_markup
        )

async def process_delete_film(update, context, step, text):
    """Обработка удаления фильма"""
    if step == 'code':
        film = db.get_film_by_code(text)
        if not film:
            await update.message.reply_text("❌ Фильм не найден")
            return
        
        if db.delete_film(text):
            await update.message.reply_text(
                f"✅ Фильм {text} успешно удален"
            )
        else:
            await update.message.reply_text("❌ Ошибка при удалении фильма")
        
        # Очищаем состояние
        context.user_data.clear()
        
        # Возвращаемся в админ-меню
        keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_admin")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def handle_photo(update, context):
    """Обработчик фотографий"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID or 'admin_action' not in context.user_data:
        return
    
    action = context.user_data['admin_action']
    step = context.user_data.get('step', '')
    
    if action == 'add_film' and step == 'cover':
        photo = update.message.photo[-1]  # Берем самое большое фото
        file_id = photo.file_id
        
        context.user_data['film_cover'] = file_id
        context.user_data['step'] = 'link'
        
        await update.message.reply_text("Введите ссылку на фильм:")

async def main():
    """Основная функция для Railway"""
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        
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
        import traceback
        traceback.print_exc()
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
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        try:
            loop.close()
        except:
            pass
