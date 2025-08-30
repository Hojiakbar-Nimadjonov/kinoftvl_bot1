#!/usr/bin/env python3
"""
Скрипт для добавления тестового фильма в базу данных
"""

from database import Database

def add_test_film():
    """Добавляет тестовый фильм в базу данных"""
    db = Database()
    
    # Тестовый фильм
    test_film = {
        'code': '#123',
        'title': 'Тестовый фильм',
        'cover': 'https://via.placeholder.com/300x400/000000/FFFFFF?text=Test+Film',
        'link': 'https://example.com/test-film'
    }
    
    try:
        # Добавляем фильм
        if db.add_film(test_film['code'], test_film['title'], test_film['cover'], test_film['link']):
            print(f"✅ Тестовый фильм {test_film['code']} успешно добавлен!")
            print(f"Название: {test_film['title']}")
            print(f"Ссылка: {test_film['link']}")
        else:
            print("❌ Ошибка при добавлении тестового фильма")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    add_test_film()
