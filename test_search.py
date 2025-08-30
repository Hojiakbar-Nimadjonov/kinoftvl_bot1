#!/usr/bin/env python3
"""
Скрипт для тестирования поиска фильмов
"""

from database import Database

def test_search():
    """Тестирует поиск фильмов"""
    db = Database()
    
    print("🔍 Тестируем поиск фильмов...")
    print("=" * 50)
    
    # Тестовые коды
    test_codes = ["#123", "#666", "#999", "#000", "123", "#abc"]
    
    for code in test_codes:
        print(f"🔍 Ищем фильм с кодом: {code}")
        
        try:
            film = db.get_film_by_code(code)
            
            if film:
                print(f"✅ Найден фильм:")
                print(f"   ID: {film['id']}")
                print(f"   Код: {film['code']}")
                print(f"   Название: {film['title']}")
                print(f"   Обложка: {film['cover']}")
                print(f"   Ссылка: {film['link']}")
            else:
                print(f"❌ Фильм не найден")
                
        except Exception as e:
            print(f"❌ Ошибка при поиске: {e}")
        
        print("-" * 30)
    
    print("=" * 50)

if __name__ == "__main__":
    test_search()
