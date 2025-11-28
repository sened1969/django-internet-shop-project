"""
Файл с запросами Django ORM для работы с книгами, издательствами, магазинами и отзывами.

Содержит запросы из Задания 2 (сложные запросы) и Задания 3 (оптимизация запросов)
домашнего задания по теме #20 "Запросы в Django ORM".
"""
from django.db.models import Count, Avg, Q
from .models import Book, Publisher, Store, Review


# ============================================================================
# ЗАДАНИЕ 2: Выполнение сложных запросов
# ============================================================================

def get_books_by_publisher_country(country):
    """
    Запрос 1: Найти все книги, опубликованные издательствами из определённой страны.
    
    Например, найти все книги, выпущенные издательствами, находящимися в России.
    
    Args:
        country (str): Название страны
        
    Returns:
        QuerySet: Набор книг, опубликованных издательствами из указанной страны
    """
    books = Book.objects.filter(publisher__country=country)
    return books


def get_books_by_store_city(city):
    """
    Запрос 2: Получить список всех книг, которые продаются в магазине в определённом городе.
    
    Например, найти все книги, которые продаются в магазинах города Москва.
    Это запрос с использованием связи "многие ко многим" между книгами и магазинами.
    
    Args:
        city (str): Название города
        
    Returns:
        QuerySet: Набор книг, продающихся в магазинах указанного города
    """
    books = Book.objects.filter(stores__city=city).distinct()
    return books


def get_books_with_avg_rating_above(rating_threshold):
    """
    Запрос 3: Найти все книги, которые имеют среднюю оценку выше определённого значения.
    
    Например, найти все книги со средней оценкой выше 4.5.
    Запрос учитывает отзывы, связанные с книгами, и вычисляет среднее значение оценок.
    
    Args:
        rating_threshold (float): Пороговое значение средней оценки
        
    Returns:
        QuerySet: Набор книг со средней оценкой выше указанного значения
    """
    books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(
        avg_rating__gt=rating_threshold
    )
    return books


def get_store_books_count():
    """
    Запрос 4: Подсчитать количество книг, продающихся в каждом магазине.
    
    Выполняет агрегатный запрос, который подсчитывает количество книг для каждого магазина.
    
    Returns:
        QuerySet: Набор магазинов с аннотацией количества книг
    """
    stores = Store.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count')
    return stores


def get_stores_with_books_after_date(date, min_books=None):
    """
    Запрос 5: Найти магазины, где продаются книги, опубликованные после определённой даты.
    
    Затем отсортировать эти магазины по количеству книг, продающихся в них.
    
    Args:
        date: Дата (datetime.date или datetime.datetime)
        min_books (int, optional): Минимальное количество книг в магазине
        
    Returns:
        QuerySet: Набор магазинов с книгами после указанной даты, отсортированных по количеству книг
    """
    stores = Store.objects.filter(
        books__published_date__gt=date
    ).annotate(
        books_count=Count('books')
    ).distinct().order_by('-books_count')
    
    if min_books is not None:
        stores = stores.filter(books_count__gte=min_books)
    
    return stores


# ============================================================================
# ЗАДАНИЕ 3: Оптимизация запросов
# ============================================================================

def get_books_with_publisher_optimized():
    """
    Оптимизированный запрос: Получить книги с данными об издательстве.
    
    Использует select_related() для оптимизации запросов с ForeignKey.
    Без select_related() для каждой книги будет выполняться отдельный запрос
    к таблице Publisher. С select_related() все данные загружаются одним запросом.
    
    Returns:
        QuerySet: Набор книг с предзагруженными данными издательства
    """
    books = Book.objects.select_related('publisher').all()
    return books


def get_books_with_stores_optimized():
    """
    Оптимизированный запрос: Получить книги с данными о магазинах.
    
    Использует prefetch_related() для оптимизации запросов с ManyToManyField.
    Без prefetch_related() для каждой книги будет выполняться отдельный запрос
    к промежуточной таблице ManyToMany. С prefetch_related() все связи загружаются
    одним дополнительным запросом.
    
    Returns:
        QuerySet: Набор книг с предзагруженными данными магазинов
    """
    books = Book.objects.prefetch_related('stores').all()
    return books


def get_books_with_reviews_optimized():
    """
    Оптимизированный запрос: Получить книги с отзывами.
    
    Использует prefetch_related() для оптимизации запросов с обратной связью ForeignKey.
    Без prefetch_related() для каждой книги будет выполняться отдельный запрос
    к таблице Review. С prefetch_related() все отзывы загружаются одним запросом.
    
    Returns:
        QuerySet: Набор книг с предзагруженными отзывами
    """
    books = Book.objects.prefetch_related('reviews').all()
    return books


def get_books_fully_optimized():
    """
    Полностью оптимизированный запрос: Получить книги со всеми связанными данными.
    
    Комбинирует select_related() для ForeignKey и prefetch_related() для ManyToMany
    и обратных связей ForeignKey. Это позволяет загрузить все необходимые данные
    минимальным количеством запросов к базе данных.
    
    Returns:
        QuerySet: Набор книг с предзагруженными данными издательства, магазинов и отзывов
    """
    books = Book.objects.select_related('publisher').prefetch_related(
        'stores',
        'reviews'
    ).all()
    return books


def get_stores_with_books_optimized():
    """
    Оптимизированный запрос: Получить магазины с книгами.
    
    Использует prefetch_related() для оптимизации запросов с ManyToManyField.
    
    Returns:
        QuerySet: Набор магазинов с предзагруженными данными книг
    """
    stores = Store.objects.prefetch_related('books').all()
    return stores


# ============================================================================
# Вспомогательные функции для демонстрации и тестирования
# ============================================================================

def print_books_by_publisher_country(country):
    """Вывести книги издательств из определённой страны."""
    books = get_books_by_publisher_country(country)
    print(f"\nКниги издательств из страны '{country}':")
    print("-" * 60)
    for book in books:
        print(f"- {book.title} ({book.author}) - Издательство: {book.publisher.name}")
    print(f"\nВсего найдено: {books.count()} книг")


def print_books_by_store_city(city):
    """Вывести книги, продающиеся в магазинах определённого города."""
    books = get_books_by_store_city(city)
    print(f"\nКниги, продающиеся в магазинах города '{city}':")
    print("-" * 60)
    for book in books:
        stores = book.stores.filter(city=city)
        store_names = ', '.join([store.name for store in stores])
        print(f"- {book.title} ({book.author}) - Магазины: {store_names}")
    print(f"\nВсего найдено: {books.count()} книг")


def print_books_with_avg_rating_above(rating_threshold):
    """Вывести книги со средней оценкой выше порога."""
    books = get_books_with_avg_rating_above(rating_threshold)
    print(f"\nКниги со средней оценкой выше {rating_threshold}:")
    print("-" * 60)
    for book in books:
        print(f"- {book.title} ({book.author}) - Средняя оценка: {book.avg_rating:.2f}")
    print(f"\nВсего найдено: {books.count()} книг")


def print_store_books_count():
    """Вывести количество книг в каждом магазине."""
    stores = get_store_books_count()
    print("\nКоличество книг в каждом магазине:")
    print("-" * 60)
    for store in stores:
        print(f"- {store.name} ({store.city}): {store.books_count} книг")
    print(f"\nВсего магазинов: {stores.count()}")


def print_stores_with_books_after_date(date):
    """Вывести магазины с книгами, опубликованными после даты."""
    stores = get_stores_with_books_after_date(date)
    print(f"\nМагазины с книгами, опубликованными после {date}:")
    print("-" * 60)
    for store in stores:
        print(f"- {store.name} ({store.city}): {store.books_count} книг")
    print(f"\nВсего магазинов: {stores.count()}")


def demonstrate_optimization():
    """
    Демонстрация оптимизации запросов.
    
    Показывает разницу в количестве SQL-запросов при использовании
    select_related() и prefetch_related().
    """
    from django.db import connection
    from django.db import reset_queries
    
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ОПТИМИЗАЦИИ ЗАПРОСОВ")
    print("=" * 60)
    
    # Без оптимизации
    reset_queries()
    books = Book.objects.all()
    for book in books:
        _ = book.publisher.name  # Доступ к издательству
        _ = list(book.stores.all())  # Доступ к магазинам
        _ = list(book.reviews.all())  # Доступ к отзывам
    
    queries_without_opt = len(connection.queries)
    print(f"\nБез оптимизации: {queries_without_opt} SQL-запросов")
    
    # С оптимизацией
    reset_queries()
    books = get_books_fully_optimized()
    for book in books:
        _ = book.publisher.name  # Доступ к издательству
        _ = list(book.stores.all())  # Доступ к магазинам
        _ = list(book.reviews.all())  # Доступ к отзывам
    
    queries_with_opt = len(connection.queries)
    print(f"С оптимизацией: {queries_with_opt} SQL-запросов")
    print(f"\nУлучшение: {queries_without_opt - queries_with_opt} запросов меньше "
          f"({(1 - queries_with_opt/queries_without_opt)*100:.1f}% улучшение)")


if __name__ == "__main__":
    """
    Примеры использования запросов.
    
    Для запуска выполните в Django Shell:
    python manage.py shell
    >>> from books.queries import *
    >>> print_books_by_publisher_country('Россия')
    """
    print("Импортируйте функции из этого модуля в Django Shell для использования.")
    print("Пример: from books.queries import get_books_by_publisher_country")

