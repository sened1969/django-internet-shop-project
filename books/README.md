# Приложение Books - Домашнее задание Тема #20

## Описание

Приложение `books` создано для выполнения домашнего задания по теме #20 "Запросы в Django ORM". Оно содержит модели для работы с книгами, издательствами, магазинами и отзывами, а также сложные запросы ORM с оптимизацией.

## Модели

### Publisher (Издательство)

**Поля:**
- `name` (CharField) - Название издательства
- `country` (CharField) - Страна, где находится издательство

**Связи:**
- Один ко многим с Book (одно издательство → много книг)

**Пример использования:**
```python
from books.models import Publisher

publisher = Publisher.objects.create(
    name='Эксмо',
    country='Россия'
)
```

### Store (Книжный магазин)

**Поля:**
- `name` (CharField) - Название магазина
- `city` (CharField) - Город, где находится магазин

**Связи:**
- Многие ко многим с Book (книга может продаваться в нескольких магазинах)

**Пример использования:**
```python
from books.models import Store

store = Store.objects.create(
    name='Читай-город',
    city='Москва'
)
```

### Book (Книга)

**Поля:**
- `title` (CharField) - Название книги
- `author` (CharField) - Автор книги
- `published_date` (DateField) - Дата публикации
- `description` (TextField) - Описание книги
- `publisher` (ForeignKey) - Издательство, опубликовавшее книгу
- `stores` (ManyToManyField) - Магазины, где продаётся книга

**Связи:**
- ForeignKey на Publisher (много книг → одно издательство)
- ManyToManyField с Store (книга может продаваться в нескольких магазинах)

**Пример использования:**
```python
from books.models import Book, Publisher, Store
from datetime import date

publisher = Publisher.objects.get(name='Эксмо')
store1 = Store.objects.get(name='Читай-город')
store2 = Store.objects.get(name='Буквоед')

book = Book.objects.create(
    title='Война и мир',
    author='Лев Толстой',
    published_date=date(1869, 1, 1),
    description='Роман-эпопея Льва Толстого',
    publisher=publisher
)
book.stores.add(store1, store2)
```

### Review (Отзыв на книгу)

**Поля:**
- `book` (ForeignKey) - Книга, на которую оставлен отзыв
- `rating` (IntegerField) - Оценка книги (от 1 до 5)
- `text` (TextField) - Текст отзыва
- `created_at` (DateTimeField) - Дата создания отзыва

**Связи:**
- ForeignKey на Book (много отзывов → одна книга)

**Пример использования:**
```python
from books.models import Review, Book

book = Book.objects.get(title='Война и мир')
review = Review.objects.create(
    book=book,
    rating=5,
    text='Отличная книга! Очень рекомендую.'
)
```

## Запросы (Задание 2)

Все запросы находятся в файле `books/queries.py`.

### 1. Книги издательств из определённой страны

```python
from books.queries import get_books_by_publisher_country

books = get_books_by_publisher_country('Россия')
```

### 2. Книги, продающиеся в магазинах определённого города

```python
from books.queries import get_books_by_store_city

books = get_books_by_store_city('Москва')
```

### 3. Книги со средней оценкой выше порога

```python
from books.queries import get_books_with_avg_rating_above

books = get_books_with_avg_rating_above(4.5)
```

### 4. Количество книг в каждом магазине

```python
from books.queries import get_store_books_count

stores = get_store_books_count()
for store in stores:
    print(f"{store.name}: {store.books_count} книг")
```

### 5. Магазины с книгами, опубликованными после даты

```python
from books.queries import get_stores_with_books_after_date
from datetime import date

stores = get_stores_with_books_after_date(date(2010, 1, 1))
```

## Оптимизация запросов (Задание 3)

### select_related() для ForeignKey

Используется для оптимизации запросов с ForeignKey (один ко многим):

```python
from books.queries import get_books_with_publisher_optimized

books = get_books_with_publisher_optimized()
# Все данные издательства загружаются одним запросом
for book in books:
    print(book.publisher.name)  # Не выполнит дополнительный запрос
```

### prefetch_related() для ManyToMany

Используется для оптимизации запросов с ManyToManyField:

```python
from books.queries import get_books_with_stores_optimized

books = get_books_with_stores_optimized()
# Все магазины загружаются одним запросом
for book in books:
    stores = list(book.stores.all())  # Не выполнит дополнительный запрос
```

### prefetch_related() для обратных связей

Используется для оптимизации запросов с обратными связями ForeignKey:

```python
from books.queries import get_books_with_reviews_optimized

books = get_books_with_reviews_optimized()
# Все отзывы загружаются одним запросом
for book in books:
    reviews = list(book.reviews.all())  # Не выполнит дополнительный запрос
```

### Полная оптимизация

Комбинирование select_related() и prefetch_related():

```python
from books.queries import get_books_fully_optimized

books = get_books_fully_optimized()
# Все связанные данные загружаются минимальным количеством запросов
for book in books:
    print(book.publisher.name)  # Издательство уже загружено
    stores = list(book.stores.all())  # Магазины уже загружены
    reviews = list(book.reviews.all())  # Отзывы уже загружены
```

## Административная панель

Все модели зарегистрированы в административной панели Django:

- **Publisher**: Управление издательствами
- **Book**: Управление книгами с инлайн-редактором отзывов
- **Store**: Управление магазинами
- **Review**: Управление отзывами

### Доступ к админ-панели

1. Запустите сервер: `python manage.py runserver`
2. Откройте http://127.0.0.1:8000/admin/
3. Войдите с учётными данными суперпользователя

## Создание тестовых данных

### Через административную панель

1. Войдите в админ-панель Django
2. Создайте несколько издательств (Publisher):
   - Название: "Эксмо", Страна: "Россия"
   - Название: "АСТ", Страна: "Россия"
   - Название: "Penguin", Страна: "Великобритания"
3. Создайте несколько магазинов (Store):
   - Название: "Читай-город", Город: "Москва"
   - Название: "Буквоед", Город: "Москва"
   - Название: "Лабиринт", Город: "Санкт-Петербург"
4. Создайте несколько книг (Book):
   - Укажите название, автора, дату публикации, описание
   - Выберите издательство
   - Выберите магазины, где продаётся книга
5. Создайте несколько отзывов (Review):
   - Выберите книгу
   - Укажите оценку (1-5) и текст отзыва

### Через Django Shell

```python
python manage.py shell

from books.models import Publisher, Store, Book, Review
from datetime import date

# Создание издательств
publisher1 = Publisher.objects.create(name='Эксмо', country='Россия')
publisher2 = Publisher.objects.create(name='АСТ', country='Россия')

# Создание магазинов
store1 = Store.objects.create(name='Читай-город', city='Москва')
store2 = Store.objects.create(name='Буквоед', city='Москва')

# Создание книг
book1 = Book.objects.create(
    title='Война и мир',
    author='Лев Толстой',
    published_date=date(1869, 1, 1),
    description='Роман-эпопея',
    publisher=publisher1
)
book1.stores.add(store1, store2)

book2 = Book.objects.create(
    title='Преступление и наказание',
    author='Фёдор Достоевский',
    published_date=date(1866, 1, 1),
    description='Роман',
    publisher=publisher2
)
book2.stores.add(store1)

# Создание отзывов
Review.objects.create(book=book1, rating=5, text='Отличная книга!')
Review.objects.create(book=book1, rating=4, text='Очень интересно')
Review.objects.create(book=book2, rating=5, text='Классика!')
```

## Тестирование запросов

### В Django Shell

```python
python manage.py shell

from books.queries import *

# Запрос 1: Книги издательств из России
print_books_by_publisher_country('Россия')

# Запрос 2: Книги в магазинах Москвы
print_books_by_store_city('Москва')

# Запрос 3: Книги со средней оценкой выше 4.5
print_books_with_avg_rating_above(4.5)

# Запрос 4: Количество книг в каждом магазине
print_store_books_count()

# Запрос 5: Магазины с книгами после 2010 года
from datetime import date
print_stores_with_books_after_date(date(2010, 1, 1))

# Демонстрация оптимизации
demonstrate_optimization()
```

## Структура файлов

```
books/
├── __init__.py
├── admin.py          # Регистрация моделей в админ-панели
├── apps.py
├── models.py         # Модели Publisher, Store, Book, Review
├── queries.py        # Запросы из Задания 2 и 3
├── tests.py
├── views.py
├── migrations/       # Миграции базы данных
└── README.md         # Этот файл
```

## Зависимости

- Django 3.2+
- Python 3.8+

## Автор

Создано для выполнения домашнего задания по теме #20 "Запросы в Django ORM".

