from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from config import CHANNELS, ADMIN_ID
import re

db = Database()

class Handlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        
        # Добавляем пользователя в базу
        db.add_user(user_id)
        
        # Проверяем подписку
        if await Handlers.check_subscription(update, context):
            await Handlers.show_main_menu(update, context)
        else:
            await Handlers.show_subscription_request(update, context)
    
    @staticmethod
    async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Проверка подписки на каналы"""
        user_id = update.effective_user.id
        
        try:
            # Проверяем подписку на каждый канал
            for channel in CHANNELS:
                member = await context.bot.get_chat_member(channel["id"], user_id)
                if member.status in ['left', 'kicked']:
                    db.update_subscription_status(user_id, False)
                    return False
            
            # Если подписан на все каналы
            db.update_subscription_status(user_id, True)
            return True
            
        except Exception as e:
            print(f"Ошибка при проверке подписки: {e}")
            return False
    
    @staticmethod
    async def show_subscription_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать запрос на подписку"""
        keyboard = []
        for channel in CHANNELS:
            keyboard.append([InlineKeyboardButton(
                f"📺 {channel['name']}", 
                url=f"https://t.me/{channel['username'][1:]}"
            )])
        
        keyboard.append([InlineKeyboardButton("✅ Проверить подписку", callback_data="check_sub")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🔐 Для доступа к боту необходимо подписаться на следующие каналы:\n\n"
            "После подписки нажмите кнопку 'Проверить подписку'",
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать главное меню"""
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
        else:
            # Обычное меню
            keyboard = [
                [InlineKeyboardButton("🔍 Поиск фильма", callback_data="search_film")],
                [InlineKeyboardButton("📺 Проверить подписку", callback_data="check_sub")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = "🎬 Добро пожаловать в бот для просмотра фильмов!\n\n"
        if user_id == ADMIN_ID:
            text += "👑 Вы вошли как администратор"
        else:
            text += "Введите код фильма (например: #123) или используйте меню"
        
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(text, reply_markup=reply_markup)
    
    @staticmethod
    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user_id = update.effective_user.id
        text = update.message.text
        
        # Сначала проверяем, не является ли это админским сообщением
        if user_id == ADMIN_ID and 'admin_action' in context.user_data:
            await Handlers.handle_admin_text(update, context)
            return
        
        # Временно отключаем проверку подписки для тестирования
        # if not await Handlers.check_subscription(update, context):
        #     await Handlers.show_subscription_request(update, context)
        #     return
        
        # Проверяем, является ли сообщение кодом фильма
        if text.startswith('#'):
            await Handlers.search_film_by_code(update, context, text)
        else:
            await update.message.reply_text(
                "Введите код фильма, начиная с символа # (например: #123)"
            )
    
    @staticmethod
    async def search_film_by_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Поиск фильма по коду"""
        user_id = update.effective_user.id
        code = update.message.text
        
        film = db.get_film_by_code(code)
        
        if film:
            # Фиксируем просмотр
            db.add_view(user_id, film['id'])
            
            # Отправляем информацию о фильме
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=film['cover'],
                caption=f"🎬 {film['title']}\n\n🔗 Ссылка: {film['link']}"
            )
        else:
            await update.message.reply_text(
                f"❌ Фильм с кодом {code} не найден.\n"
                "Проверьте правильность кода или обратитесь к администратору."
            )
    
    @staticmethod
    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик callback запросов"""
        query = update.callback_query
        data = query.data
        user_id = query.from_user.id
        
        await query.answer()
        
        if data == "check_sub":
            if await Handlers.check_subscription(update, context):
                await Handlers.show_main_menu(update, context)
            else:
                await query.edit_message_text(
                    "❌ Вы не подписаны на все необходимые каналы.\n"
                    "Пожалуйста, подпишитесь и попробуйте снова.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔄 Проверить снова", callback_data="check_sub")
                    ]])
                )
        
        elif data == "search_film":
            await query.edit_message_text(
                "🔍 Введите код фильма, начиная с символа # (например: #123)"
            )
        
        elif data == "admin_add_film":
            if user_id == ADMIN_ID:
                await Handlers.start_add_film(update, context)
            else:
                await query.edit_message_text("❌ Доступ запрещен")
        
        elif data == "admin_edit_film":
            if user_id == ADMIN_ID:
                await Handlers.start_edit_film(update, context)
            else:
                await query.edit_message_text("❌ Доступ запрещен")
        
        elif data == "admin_delete_film":
            if user_id == ADMIN_ID:
                await Handlers.start_delete_film(update, context)
            else:
                await query.edit_message_text("❌ Доступ запрещен")
        
        elif data == "admin_stats":
            if user_id == ADMIN_ID:
                await Handlers.show_stats(update, context)
            else:
                await query.edit_message_text("❌ Доступ запрещен")
        
        elif data == "back_to_admin":
            if user_id == ADMIN_ID:
                await Handlers.show_main_menu(update, context)
            else:
                await query.edit_message_text("❌ Доступ запрещен")
        
        elif data.startswith("edit_"):
            if user_id == ADMIN_ID:
                await Handlers.handle_edit_field(update, context, data)
            else:
                await query.edit_message_text("❌ Доступ запрещен")
    
    @staticmethod
    async def start_add_film(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало процесса добавления фильма"""
        query = update.callback_query
        
        # Сохраняем состояние
        context.user_data['admin_action'] = 'add_film'
        context.user_data['step'] = 'code'
        
        await query.edit_message_text(
            "➕ Добавление нового фильма\n\n"
            "Введите код фильма (например: #123):"
        )
    
    @staticmethod
    async def start_edit_film(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало процесса редактирования фильма"""
        query = update.callback_query
        
        # Сохраняем состояние
        context.user_data['admin_action'] = 'edit_film'
        context.user_data['step'] = 'code'
        
        await query.edit_message_text(
            "✏️ Редактирование фильма\n\n"
            "Введите код фильма для редактирования:"
        )
    
    @staticmethod
    async def start_delete_film(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало процесса удаления фильма"""
        query = update.callback_query
        
        # Сохраняем состояние
        context.user_data['admin_action'] = 'delete_film'
        context.user_data['step'] = 'code'
        
        await query.edit_message_text(
            "🗑 Удаление фильма\n\n"
            "Введите код фильма для удаления:"
        )
    
    @staticmethod
    async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статистику"""
        query = update.callback_query
        
        stats = db.get_today_stats()
        
        keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_admin")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📊 Статистика за сегодня\n\n"
            f"👀 Просмотров фильмов: {stats['views_today']}\n"
            f"👥 Новых пользователей: {stats['new_users_today']}",
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await Handlers.process_add_film(update, context, step, text)
        elif action == 'edit_film':
            await Handlers.process_edit_film(update, context, step, text)
        elif action == 'delete_film':
            await Handlers.process_delete_film(update, context, step, text)
    
    @staticmethod
    async def process_add_film(update: Update, context: ContextTypes.DEFAULT_TYPE, step: str, text: str):
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
    
    @staticmethod
    async def process_edit_film(update: Update, context: ContextTypes.DEFAULT_TYPE, step: str, text: str):
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
        
        elif step == 'edit_value':
            field = context.user_data.get('edit_field')
            film_code = context.user_data.get('film_code')
            
            if field and film_code:
                if db.update_film(film_code, field, text):
                    await update.message.reply_text(f"✅ {field} обновлен")
                else:
                    await update.message.reply_text("❌ Ошибка при обновлении")
                
                # Очищаем состояние
                context.user_data.clear()
                
                # Возвращаемся в админ-меню
                keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_admin")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    
    @staticmethod
    async def process_delete_film(update: Update, context: ContextTypes.DEFAULT_TYPE, step: str, text: str):
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
    
    @staticmethod
    async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        
        elif action == 'edit_film' and step == 'cover':
            photo = update.message.photo[-1]
            file_id = photo.file_id
            
            film_code = context.user_data.get('film_code')
            if film_code and db.update_film(film_code, 'cover', file_id):
                await update.message.reply_text("✅ Обложка обновлена")
            else:
                await update.message.reply_text("❌ Ошибка при обновлении обложки")
            
            context.user_data.clear()
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_admin")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    
    @staticmethod
    async def handle_edit_field(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
        """Обработка выбора поля для редактирования"""
        query = update.callback_query
        field = data.replace("edit_", "")
        
        context.user_data['edit_field'] = field
        context.user_data['step'] = 'edit_value'
        
        field_names = {
            'title': 'название',
            'cover': 'обложку',
            'link': 'ссылку',
            'code': 'код'
        }
        
        field_name = field_names.get(field, field)
        
        if field == 'cover':
            await query.edit_message_text(
                f"✏️ Редактирование {field_name}\n\n"
                f"Отправьте новую обложку фильма (фото):"
            )
        else:
            await query.edit_message_text(
                f"✏️ Редактирование {field_name}\n\n"
                f"Введите новое значение:"
            )
