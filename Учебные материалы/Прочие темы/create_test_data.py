"""
Скрипт для создания тестовых данных товаров.

Использование:
    python manage.py shell < create_test_data.py
    или
    python manage.py shell
    >>> exec(open('create_test_data.py').read())
"""

from shop.models import Product
from decimal import Decimal

# Очистка существующих товаров (опционально)
# Product.objects.all().delete()

# Создание тестовых товаров
products_data = [
    {
        'name': 'Ноутбук Dell XPS 15',
        'description': 'Мощный ноутбук для работы и творчества. Процессор Intel Core i7 12-го поколения, 16GB RAM, SSD 512GB, дисплей 15.6" 4K UHD. Идеально подходит для профессиональной работы, программирования и дизайна.',
        'price': Decimal('89999.99')
    },
    {
        'name': 'Смартфон iPhone 15 Pro',
        'description': 'Новейший смартфон от Apple с процессором A17 Pro, камерой 48 МП и дисплеем Super Retina XDR 6.1". Поддержка 5G, аккумулятор на весь день, защита от воды IP68.',
        'price': Decimal('99999.00')
    },
    {
        'name': 'Наушники Sony WH-1000XM5',
        'description': 'Беспроводные наушники с активным шумоподавлением и превосходным качеством звука. Автономность до 30 часов, быстрая зарядка, поддержка Hi-Res Audio.',
        'price': Decimal('24999.50')
    },
    {
        'name': 'Планшет iPad Pro 12.9"',
        'description': 'Профессиональный планшет с дисплеем Liquid Retina XDR 12.9", процессором M2, поддержкой Apple Pencil и Magic Keyboard. Идеален для творчества и работы.',
        'price': Decimal('129999.00')
    },
    {
        'name': 'Умные часы Apple Watch Series 9',
        'description': 'Современные умные часы с дисплеем Always-On Retina, GPS, пульсометром, ЭКГ и множеством функций для здоровья и фитнеса. Водонепроницаемость до 50 метров.',
        'price': Decimal('39999.00')
    },
    {
        'name': 'Игровая консоль PlayStation 5',
        'description': 'Новейшая игровая консоль от Sony с поддержкой 4K и 120 FPS, SSD накопителем для быстрой загрузки игр, поддержкой ray tracing и 3D аудио.',
        'price': Decimal('59999.99')
    },
    {
        'name': 'Беспроводная клавиатура Logitech MX Keys',
        'description': 'Эргономичная беспроводная клавиатура с подсветкой клавиш, поддержкой нескольких устройств, долгим временем работы от батареи и удобными клавишами для Mac и Windows.',
        'price': Decimal('8999.00')
    },
    {
        'name': 'Веб-камера Logitech C920',
        'description': 'Профессиональная веб-камера с разрешением Full HD 1080p, автофокусом, стерео микрофоном и отличным качеством изображения для видеозвонков и стриминга.',
        'price': Decimal('6999.50')
    }
]

# Создание товаров
created_count = 0
for product_data in products_data:
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults={
            'description': product_data['description'],
            'price': product_data['price']
        }
    )
    if created:
        created_count += 1
        print(f"✓ Создан товар: {product.name} - {product.price} ₽")
    else:
        print(f"⊘ Товар уже существует: {product.name}")

print(f"\nВсего создано новых товаров: {created_count}")
print(f"Всего товаров в базе: {Product.objects.count()}")

