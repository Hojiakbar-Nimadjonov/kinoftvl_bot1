#!/usr/bin/env python3
"""
Скрипт для проверки содержимого базы данных
"""

from database import Database

def check_database():
    """Проверяет содержимое базы данных"""
    db = Database()
    
    print("🔍 Проверяем базу данных...")
    print("=" * 50)
    
    # Получаем все фильмы
    films = db.get_all_films()
    
    if films:
        print(f"📽️ Найдено фильмов: {len(films)}")
        print("-" * 30)
        for film in films:
            print(f"Код: {film['code']}")
            print(f"Название: {film['title']}")
            print(f"Обложка: {film['cover']}")
            print(f"Ссылка: {film['link']}")
            print("-" * 30)
    else:
        print("❌ Фильмы не найдены")
    
    print("=" * 50)

if __name__ == "__main__":
    check_database()
