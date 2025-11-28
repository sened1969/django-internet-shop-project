"""
Простой скрипт для создания тестовых данных.

Использование:
    python manage.py shell
    >>> exec(open('books/run_create_data.py').read())
    
Или напрямую:
    python books/run_create_data.py
"""
import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
django.setup()

# Импорт и выполнение основного скрипта
from books.create_test_data import *

# Выполнение создания данных
if __name__ == '__main__':
    from books.models import Publisher, Store, Book, Review
    from datetime import date
    
    print("=" * 60)
    print("СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ ДЛЯ ПРИЛОЖЕНИЯ BOOKS")
    print("=" * 60)
    
    # Импорт функций из create_test_data.py
    exec(open('books/create_test_data.py', encoding='utf-8').read())

