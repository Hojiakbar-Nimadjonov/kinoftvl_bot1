#!/usr/bin/env python3
"""
Скрипт для добавления тестовых фильмов в базу данных
"""

from database import Database

def add_test_films():
    """Добавляет тестовые фильмы в базу данных"""
    db = Database()
    
    # Тестовые фильмы
    test_films = [
        {
            'code': '#123',
            'title': 'Тестовый фильм 1',
            'cover': 'https://via.placeholder.com/300x400/000000/FFFFFF?text=Test+Film+1',
            'link': 'https://example.com/test-film-1'
        },
        {
            'code': '#666',
            'title': 'Тестовый фильм 2',
            'cover': 'https://via.placeholder.com/300x400/FF0000/FFFFFF?text=Test+Film+2',
            'link': 'https://example.com/test-film-2'
        },
        {
            'code': '#999',
            'title': 'Тестовый фильм 3',
            'cover': 'https://via.placeholder.com/300x400/00FF00/FFFFFF?text=Test+Film+3',
            'link': 'https://example.com/test-film-3'
        }
    ]
    
    for film in test_films:
        try:
            # Добавляем фильм
            if db.add_film(film['code'], film['title'], film['cover'], film['link']):
                print(f"✅ Фильм {film['code']} успешно добавлен!")
                print(f"Название: {film['title']}")
                print(f"Ссылка: {film['link']}")
                print("-" * 40)
            else:
                print(f"❌ Ошибка при добавлении фильма {film['code']}")
                
        except Exception as e:
            print(f"❌ Ошибка при добавлении {film['code']}: {e}")

if __name__ == "__main__":
    add_test_films()
