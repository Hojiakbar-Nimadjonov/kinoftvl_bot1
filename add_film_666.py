#!/usr/bin/env python3
"""
Скрипт для добавления фильма #666 в базу данных
"""

from database import Database

def add_film_666():
    """Добавляет фильм #666 в базу данных"""
    db = Database()
    
    # Фильм #666
    film_666 = {
        'code': '#666',
        'title': 'Тестовый фильм 2',
        'cover': 'https://via.placeholder.com/300x400/FF0000/FFFFFF?text=Test+Film+2',
        'link': 'https://example.com/test-film-2'
    }
    
    try:
        # Добавляем фильм
        if db.add_film(film_666['code'], film_666['title'], film_666['cover'], film_666['link']):
            print(f"✅ Фильм {film_666['code']} успешно добавлен!")
            print(f"Название: {film_666['title']}")
            print(f"Ссылка: {film_666['link']}")
        else:
            print("❌ Ошибка при добавлении фильма")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    add_film_666()
