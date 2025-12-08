"""
Management команда для создания тестовых товаров.

Использование:
    python manage.py create_test_products
"""
from django.core.management.base import BaseCommand
from shop.models import Product, Category


class Command(BaseCommand):
    help = 'Создает 3 тестовых товара для тестирования и скриншотов'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Создание тестовых товаров...'))
        
        # Создаем или получаем категории
        category_electronics, created = Category.objects.get_or_create(
            name='Электроника',
            defaults={'description': 'Электронные устройства и гаджеты'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создана категория: {category_electronics.name}'))
        
        category_clothing, created = Category.objects.get_or_create(
            name='Одежда',
            defaults={'description': 'Одежда и аксессуары'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создана категория: {category_clothing.name}'))
        
        category_books, created = Category.objects.get_or_create(
            name='Книги',
            defaults={'description': 'Книги и литература'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создана категория: {category_books.name}'))
        
        # Товар 1: Смартфон
        product1, created1 = Product.objects.get_or_create(
            name='Смартфон Samsung Galaxy S21',
            defaults={
                'description': (
                    'Флагманский смартфон Samsung с 6.2-дюймовым экраном, '
                    'процессором Exynos 2100, тройной камерой 64+12+12 МП и '
                    'батареей на 4000 мАч. Поддержка 5G, защита от воды IP68.'
                ),
                'price': 59999.00,
                'stock': 15,
                'category': category_electronics
            }
        )
        if created1:
            self.stdout.write(self.style.SUCCESS(f'[OK] Создан товар: {product1.name} (ID: {product1.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'[SKIP] Товар уже существует: {product1.name} (ID: {product1.id})'))
        
        # Товар 2: Футболка
        product2, created2 = Product.objects.get_or_create(
            name='Футболка хлопковая',
            defaults={
                'description': (
                    'Классическая футболка из 100% хлопка. Удобная посадка, '
                    'мягкая ткань, не выцветает после стирки. Доступна в '
                    'разных цветах и размерах.'
                ),
                'price': 1299.00,
                'stock': 50,
                'category': category_clothing
            }
        )
        if created2:
            self.stdout.write(self.style.SUCCESS(f'[OK] Создан товар: {product2.name} (ID: {product2.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'[SKIP] Товар уже существует: {product2.name} (ID: {product2.id})'))
        
        # Товар 3: Книга
        product3, created3 = Product.objects.get_or_create(
            name='Книга "Python для начинающих"',
            defaults={
                'description': (
                    'Подробное руководство по программированию на Python для '
                    'начинающих. Включает основы синтаксиса, работу с данными, '
                    'ООП, работу с файлами и базами данных. Множество примеров '
                    'и практических заданий.'
                ),
                'price': 2499.00,
                'stock': 8,
                'category': category_books
            }
        )
        if created3:
            self.stdout.write(self.style.SUCCESS(f'[OK] Создан товар: {product3.name} (ID: {product3.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'[SKIP] Товар уже существует: {product3.name} (ID: {product3.id})'))
        
        # Итоговая информация
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Тестовые товары созданы успешно!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write('Созданные товары:')
        self.stdout.write(f'  1. {product1.name} - {product1.price} руб. (ID: {product1.id})')
        self.stdout.write(f'  2. {product2.name} - {product2.price} руб. (ID: {product2.id})')
        self.stdout.write(f'  3. {product3.name} - {product3.price} руб. (ID: {product3.id})')
        self.stdout.write('')
        self.stdout.write('URL адреса для просмотра:')
        self.stdout.write(f'  - Список товаров: http://127.0.0.1:8000/')
        self.stdout.write(f'  - Товар 1: http://127.0.0.1:8000/product/{product1.id}/')
        self.stdout.write(f'  - Товар 2: http://127.0.0.1:8000/product/{product2.id}/')
        self.stdout.write(f'  - Товар 3: http://127.0.0.1:8000/product/{product3.id}/')
        self.stdout.write('')
