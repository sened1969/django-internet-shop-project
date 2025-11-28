"""
Скрипт для создания тестовых данных для приложения books.

Использование:
    python manage.py shell
    >>> exec(open('books/create_test_data.py').read())
    
Или:
    python manage.py shell < books/create_test_data.py
"""
from books.models import Publisher, Store, Book, Review
from datetime import date

print("=" * 60)
print("СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ ДЛЯ ПРИЛОЖЕНИЯ BOOKS")
print("=" * 60)

# Очистка существующих данных (опционально)
# Book.objects.all().delete()
# Store.objects.all().delete()
# Publisher.objects.all().delete()
# Review.objects.all().delete()

# 1. Создание издательств
print("\n1. Создание издательств...")
publishers = {
    'Эксмо': Publisher.objects.get_or_create(
        name='Эксмо',
        defaults={'country': 'Россия'}
    )[0],
    'АСТ': Publisher.objects.get_or_create(
        name='АСТ',
        defaults={'country': 'Россия'}
    )[0],
    'Питер': Publisher.objects.get_or_create(
        name='Питер',
        defaults={'country': 'Россия'}
    )[0],
    'Penguin': Publisher.objects.get_or_create(
        name='Penguin',
        defaults={'country': 'Великобритания'}
    )[0],
    'HarperCollins': Publisher.objects.get_or_create(
        name='HarperCollins',
        defaults={'country': 'США'}
    )[0],
}

for name, publisher in publishers.items():
    print(f"   ✓ {publisher.name} ({publisher.country})")

# 2. Создание магазинов
print("\n2. Создание магазинов...")
stores = {
    'Читай-город Москва': Store.objects.get_or_create(
        name='Читай-город',
        city='Москва',
        defaults={}
    )[0],
    'Читай-город СПб': Store.objects.get_or_create(
        name='Читай-город',
        city='Санкт-Петербург',
        defaults={}
    )[0],
    'Буквоед Москва': Store.objects.get_or_create(
        name='Буквоед',
        city='Москва',
        defaults={}
    )[0],
    'Буквоед СПб': Store.objects.get_or_create(
        name='Буквоед',
        city='Санкт-Петербург',
        defaults={}
    )[0],
    'Лабиринт': Store.objects.get_or_create(
        name='Лабиринт',
        city='Москва',
        defaults={}
    )[0],
    'Московский Дом Книги': Store.objects.get_or_create(
        name='Московский Дом Книги',
        city='Москва',
        defaults={}
    )[0],
}

for name, store in stores.items():
    print(f"   ✓ {store.name} ({store.city})")

# 3. Создание книг
print("\n3. Создание книг...")
books_data = [
    {
        'title': 'Война и мир',
        'author': 'Лев Толстой',
        'published_date': date(1869, 1, 1),
        'description': 'Роман-эпопея Льва Толстого, описывающий русское общество в эпоху войн против Наполеона в 1805—1812 годах.',
        'publisher': publishers['Эксмо'],
        'stores': [stores['Читай-город Москва'], stores['Буквоед Москва'], stores['Лабиринт']]
    },
    {
        'title': 'Преступление и наказание',
        'author': 'Фёдор Достоевский',
        'published_date': date(1866, 1, 1),
        'description': 'Социально-психологический и социально-философский роман о преступлении и наказании.',
        'publisher': publishers['АСТ'],
        'stores': [stores['Читай-город Москва'], stores['Буквоед Москва'], stores['Московский Дом Книги']]
    },
    {
        'title': '1984',
        'author': 'Джордж Оруэлл',
        'published_date': date(1949, 6, 8),
        'description': 'Роман-антиутопия о тоталитарном обществе, где правительство контролирует каждый аспект жизни людей.',
        'publisher': publishers['Penguin'],
        'stores': [stores['Читай-город Москва'], stores['Буквоед СПб'], stores['Лабиринт']]
    },
    {
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
        'published_date': date(1967, 1, 1),
        'description': 'Философский роман о добре и зле, любви и предательстве, написанный в жанре магического реализма.',
        'publisher': publishers['АСТ'],
        'stores': [stores['Читай-город СПб'], stores['Буквоед Москва'], stores['Московский Дом Книги']]
    },
    {
        'title': 'Анна Каренина',
        'author': 'Лев Толстой',
        'published_date': date(1877, 1, 1),
        'description': 'Роман о трагической любви замужней дамы Анны Карениной и светского офицера Алексея Вронского.',
        'publisher': publishers['Эксмо'],
        'stores': [stores['Читай-город Москва'], stores['Лабиринт']]
    },
    {
        'title': 'Идиот',
        'author': 'Фёдор Достоевский',
        'published_date': date(1869, 1, 1),
        'description': 'Роман о князе Мышкине, который пытается принести добро в жестокий мир.',
        'publisher': publishers['Питер'],
        'stores': [stores['Буквоед Москва'], stores['Буквоед СПб']]
    },
    {
        'title': 'Скотный двор',
        'author': 'Джордж Оруэлл',
        'published_date': date(1945, 8, 17),
        'description': 'Аллегорическая повесть-сатира на сталинский режим в СССР.',
        'publisher': publishers['Penguin'],
        'stores': [stores['Читай-город Москва'], stores['Читай-город СПб']]
    },
    {
        'title': 'Гарри Поттер и философский камень',
        'author': 'Джоан Роулинг',
        'published_date': date(1997, 6, 26),
        'description': 'Первый роман в серии книг про юного волшебника Гарри Поттера.',
        'publisher': publishers['HarperCollins'],
        'stores': [stores['Читай-город Москва'], stores['Буквоед Москва'], stores['Лабиринт'], stores['Московский Дом Книги']]
    },
    {
        'title': 'Властелин колец: Братство Кольца',
        'author': 'Джон Рональд Руэл Толкин',
        'published_date': date(1954, 7, 29),
        'description': 'Первый том эпической трилогии о Средиземье и борьбе с тёмным властелином Сауроном.',
        'publisher': publishers['HarperCollins'],
        'stores': [stores['Буквоед Москва'], stores['Буквоед СПб'], stores['Лабиринт']]
    },
    {
        'title': 'Убить пересмешника',
        'author': 'Харпер Ли',
        'published_date': date(1960, 7, 11),
        'description': 'Роман о расовой несправедливости и потере невинности в американском Юге 1930-х годов.',
        'publisher': publishers['HarperCollins'],
        'stores': [stores['Читай-город СПб'], stores['Московский Дом Книги']]
    },
]

books = {}
for book_data in books_data:
    book = Book.objects.get_or_create(
        title=book_data['title'],
        defaults={
            'author': book_data['author'],
            'published_date': book_data['published_date'],
            'description': book_data['description'],
            'publisher': book_data['publisher']
        }
    )[0]
    # Обновляем магазины
    book.stores.set(book_data['stores'])
    books[book_data['title']] = book
    print(f"   ✓ {book.title} - {book.author} ({book.publisher.name})")

# 4. Создание отзывов
print("\n4. Создание отзывов...")
reviews_data = [
    # Война и мир
    {'book': books['Война и мир'], 'rating': 5, 'text': 'Великолепное произведение! Очень глубокий и многогранный роман. Обязательно к прочтению.'},
    {'book': books['Война и мир'], 'rating': 5, 'text': 'Классика русской литературы. Очень длинная, но стоит потраченного времени.'},
    {'book': books['Война и мир'], 'rating': 4, 'text': 'Отличная книга, но местами слишком затянуто. Тем не менее, рекомендую.'},
    
    # Преступление и наказание
    {'book': books['Преступление и наказание'], 'rating': 5, 'text': 'Потрясающий психологический роман! Достоевский - гений.'},
    {'book': books['Преступление и наказание'], 'rating': 5, 'text': 'Одно из лучших произведений русской литературы. Очень глубокое.'},
    {'book': books['Преступление и наказание'], 'rating': 4, 'text': 'Интересно, но мрачно. Хорошо написано.'},
    
    # 1984
    {'book': books['1984'], 'rating': 5, 'text': 'Актуально и по сей день. Пугающая антиутопия.'},
    {'book': books['1984'], 'rating': 5, 'text': 'Обязательно к прочтению! Очень пророческое произведение.'},
    {'book': books['1984'], 'rating': 4, 'text': 'Интересная антиутопия, но местами слишком мрачно.'},
    
    # Мастер и Маргарита
    {'book': books['Мастер и Маргарита'], 'rating': 5, 'text': 'Гениальное произведение! Очень необычный и интересный роман.'},
    {'book': books['Мастер и Маргарита'], 'rating': 5, 'text': 'Одна из моих любимых книг. Магический реализм на высшем уровне.'},
    {'book': books['Мастер и Маргарита'], 'rating': 4, 'text': 'Сложная, но очень интересная книга. Рекомендую.'},
    
    # Анна Каренина
    {'book': books['Анна Каренина'], 'rating': 5, 'text': 'Прекрасный роман о любви и страсти. Толстой - мастер слова.'},
    {'book': books['Анна Каренина'], 'rating': 4, 'text': 'Хорошая книга, но немного затянуто.'},
    
    # Идиот
    {'book': books['Идиот'], 'rating': 5, 'text': 'Глубокий философский роман. Достоевский показывает человеческую природу.'},
    {'book': books['Идиот'], 'rating': 4, 'text': 'Интересное произведение, но сложное для понимания.'},
    
    # Скотный двор
    {'book': books['Скотный двор'], 'rating': 5, 'text': 'Отличная сатира! Очень актуально и поучительно.'},
    {'book': books['Скотный двор'], 'rating': 4, 'text': 'Интересная аллегория. Хорошо написано.'},
    
    # Гарри Поттер
    {'book': books['Гарри Поттер и философский камень'], 'rating': 5, 'text': 'Любимая книга детства! Магия и приключения.'},
    {'book': books['Гарри Поттер и философский камень'], 'rating': 5, 'text': 'Отличная книга для всех возрастов. Очень увлекательно!'},
    {'book': books['Гарри Поттер и философский камень'], 'rating': 5, 'text': 'Начало великой истории. Обязательно к прочтению!'},
    
    # Властелин колец
    {'book': books['Властелин колец: Братство Кольца'], 'rating': 5, 'text': 'Эпическое фэнтези! Толкин создал целый мир.'},
    {'book': books['Властелин колец: Братство Кольца'], 'rating': 5, 'text': 'Классика жанра. Очень детально проработанный мир.'},
    
    # Убить пересмешника
    {'book': books['Убить пересмешника'], 'rating': 5, 'text': 'Важное произведение о справедливости и человечности.'},
    {'book': books['Убить пересмешника'], 'rating': 4, 'text': 'Хорошая книга с важным посылом.'},
]

for review_data in reviews_data:
    Review.objects.get_or_create(
        book=review_data['book'],
        rating=review_data['rating'],
        text=review_data['text'],
        defaults={}
    )
    print(f"   ✓ Отзыв на '{review_data['book'].title}' - оценка {review_data['rating']}/5")

print("\n" + "=" * 60)
print("ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
print("=" * 60)
print(f"\nСоздано:")
print(f"  - Издательств: {Publisher.objects.count()}")
print(f"  - Магазинов: {Store.objects.count()}")
print(f"  - Книг: {Book.objects.count()}")
print(f"  - Отзывов: {Review.objects.count()}")
print("\nТеперь вы можете:")
print("  1. Проверить данные в админ-панели: http://127.0.0.1:8000/admin/")
print("  2. Выполнить запросы из books/queries.py")
print("  3. Протестировать оптимизацию запросов")

