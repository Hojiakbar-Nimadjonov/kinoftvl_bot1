import sqlite3
import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица фильмов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                cover TEXT NOT NULL,
                link TEXT NOT NULL
            )
        ''')
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                is_subscribed BOOLEAN DEFAULT FALSE,
                date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица просмотров
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                film_id INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (film_id) REFERENCES films (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id):
        """Добавление нового пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                (user_id,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return False
        finally:
            conn.close()
    
    def update_subscription_status(self, user_id, is_subscribed):
        """Обновление статуса подписки пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE users SET is_subscribed = ? WHERE user_id = ?",
                (is_subscribed, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении статуса подписки: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_subscription_status(self, user_id):
        """Получение статуса подписки пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT is_subscribed FROM users WHERE user_id = ?",
                (user_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else False
        except Exception as e:
            print(f"Ошибка при получении статуса подписки: {e}")
            return False
        finally:
            conn.close()
    
    def add_film(self, code, title, cover, link):
        """Добавление нового фильма"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO films (code, title, cover, link) VALUES (?, ?, ?, ?)",
                (code, title, cover, link)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении фильма: {e}")
            return False
        finally:
            conn.close()
    
    def get_film_by_code(self, code):
        """Получение фильма по коду"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM films WHERE code = ?",
                (code,)
            )
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'code': result[1],
                    'title': result[2],
                    'cover': result[3],
                    'link': result[4]
                }
            return None
        except Exception as e:
            print(f"Ошибка при получении фильма: {e}")
            return None
        finally:
            conn.close()
    
    def update_film(self, code, field, value):
        """Обновление поля фильма"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                f"UPDATE films SET {field} = ? WHERE code = ?",
                (value, code)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении фильма: {e}")
            return False
        finally:
            conn.close()
    
    def delete_film(self, code):
        """Удаление фильма"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM films WHERE code = ?", (code,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении фильма: {e}")
            return False
        finally:
            conn.close()
    
    def add_view(self, user_id, film_id):
        """Добавление просмотра фильма"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO views (user_id, film_id) VALUES (?, ?)",
                (user_id, film_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении просмотра: {e}")
            return False
        finally:
            conn.close()
    
    def get_today_stats(self):
        """Получение статистики за сегодня"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.date.today().strftime('%Y-%m-%d')
        
        try:
            # Количество просмотров за сегодня
            cursor.execute(
                "SELECT COUNT(*) FROM views WHERE DATE(date) = ?",
                (today,)
            )
            views_today = cursor.fetchone()[0]
            
            # Количество новых пользователей за сегодня
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE DATE(date_joined) = ?",
                (today,)
            )
            new_users_today = cursor.fetchone()[0]
            
            return {
                'views_today': views_today,
                'new_users_today': new_users_today
            }
        except Exception as e:
            print(f"Ошибка при получении статистики: {e}")
            return {'views_today': 0, 'new_users_today': 0}
        finally:
            conn.close()
    
    def get_all_films(self):
        """Получение всех фильмов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM films ORDER BY code")
            results = cursor.fetchall()
            films = []
            for result in results:
                films.append({
                    'id': result[0],
                    'code': result[1],
                    'title': result[2],
                    'cover': result[3],
                    'link': result[4]
                })
            return films
        except Exception as e:
            print(f"Ошибка при получении фильмов: {e}")
            return []
        finally:
            conn.close()
