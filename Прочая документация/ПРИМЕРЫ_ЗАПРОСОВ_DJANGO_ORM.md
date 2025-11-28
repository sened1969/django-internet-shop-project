# Примеры запросов Django ORM для ДЗ "Тема #19"

Этот файл содержит примеры запросов Django ORM для выполнения Части 3 домашнего задания.

## Запуск Django Shell

```bash
python manage.py shell
```

---

## Часть 1: Создание категорий и товаров

### Создание категорий

```python
from shop.models import Category, Product, Order, OrderItem, Review
from django.contrib.auth.models import User

# Создание основных категорий
electronics = Category.objects.create(
    name='Электроника',
    description='Электронные устройства и гаджеты'
)

clothing = Category.objects.create(
    name='Одежда',
    description='Одежда и аксессуары'
)

books = Category.objects.create(
    name='Книги',
    description='Книги и литература'
)

# Создание вложенных категорий
smartphones = Category.objects.create(
    name='Смартфоны',
    description='Мобильные телефоны',
    parent=electronics
)

laptops = Category.objects.create(
    name='Ноутбуки',
    description='Портативные компьютеры',
    parent=electronics
)

mens_clothing = Category.objects.create(
    name='Мужская одежда',
    parent=clothing
)

womens_clothing = Category.objects.create(
    name='Женская одежда',
    parent=clothing
)
```

### Создание товаров

```python
# Создание товаров в категории Электроника > Смартфоны
iphone = Product.objects.create(
    name='iPhone 15 Pro',
    description='Новейший смартфон от Apple с процессором A17 Pro',
    price=99999.00,
    stock=15,
    category=smartphones
)

samsung = Product.objects.create(
    name='Samsung Galaxy S24',
    description='Флагманский смартфон от Samsung',
    price=89999.00,
    stock=20,
    category=smartphones
)

# Создание товаров в категории Электроника > Ноутбуки
macbook = Product.objects.create(
    name='MacBook Pro 16"',
    description='Профессиональный ноутбук от Apple',
    price=249999.00,
    stock=5,
    category=laptops
)

# Создание товаров в категории Одежда
t_shirt = Product.objects.create(
    name='Футболка классическая',
    description='Хлопковая футболка',
    price=1999.00,
    stock=50,
    category=mens_clothing
)

# Создание товаров в категории Книги
python_book = Product.objects.create(
    name='Изучаем Python',
    description='Книга по программированию на Python',
    price=1299.00,
    stock=30,
    category=books
)
```

---

## Часть 2: Запросы к базе данных

### 1. Получить все товары из определённой категории

```python
# Все товары из категории "Смартфоны"
smartphones_products = Product.objects.filter(category=smartphones)
for product in smartphones_products:
    print(f"{product.name} - {product.price} руб.")

# Или по имени категории
smartphones_products = Product.objects.filter(category__name='Смартфоны')

# Все товары из категории "Электроника" (включая вложенные)
electronics_products = Product.objects.filter(category__parent=electronics)
# Или все товары, которые относятся к категории или её дочерним категориям
from django.db.models import Q
electronics_all = Product.objects.filter(
    Q(category=electronics) | Q(category__parent=electronics)
)
```

### 2. Получить все заказы пользователя

```python
# Получить пользователя (предположим, что он существует)
user = User.objects.first()  # или User.objects.get(username='username')

# Все заказы пользователя
user_orders = Order.objects.filter(user=user)
for order in user_orders:
    print(f"Заказ #{order.id} - {order.get_status_display()} - {order.total_price()} руб.")

# Или через related_name
user_orders = user.orders.all()
```

### 3. Найти все отзывы для определённого товара

```python
# Все отзывы для iPhone
iphone_reviews = Review.objects.filter(product=iphone)
for review in iphone_reviews:
    print(f"{review.user.username}: {review.rating}/5 - {review.text[:50]}...")

# Или через related_name
iphone_reviews = iphone.reviews.all()

# Отзывы с оценкой 5
five_star_reviews = Review.objects.filter(product=iphone, rating=5)
```

### 4. Получить все товары, у которых количество на складе больше 10

```python
# Товары со складом > 10
products_in_stock = Product.objects.filter(stock__gt=10)
for product in products_in_stock:
    print(f"{product.name} - в наличии: {product.stock} шт.")

# Товары со складом >= 10
products_in_stock = Product.objects.filter(stock__gte=10)

# Товары со складом от 10 до 50
products_range = Product.objects.filter(stock__gte=10, stock__lte=50)
```

---

## Дополнительные полезные запросы

### Создание заказа с товарами

```python
# Создание заказа
order = Order.objects.create(
    user=user,
    status='processing'
)

# Добавление товаров в заказ
OrderItem.objects.create(
    order=order,
    product=iphone,
    quantity=1
)

OrderItem.objects.create(
    order=order,
    product=macbook,
    quantity=1
)

# Проверка общей стоимости заказа
print(f"Общая стоимость заказа: {order.total_price()} руб.")
```

### Создание отзывов

```python
# Создание отзыва
review1 = Review.objects.create(
    product=iphone,
    user=user,
    rating=5,
    text='Отличный телефон! Очень доволен покупкой.'
)

review2 = Review.objects.create(
    product=iphone,
    user=user,
    rating=4,
    text='Хороший телефон, но цена завышена.'
)
```

### Работа с корзиной

```python
from shop.models import Cart, CartItem

# Создание корзины для пользователя
cart, created = Cart.objects.get_or_create(user=user)

# Добавление товара в корзину
cart_item, created = CartItem.objects.get_or_create(
    cart=cart,
    product=iphone,
    defaults={'quantity': 1}
)

# Если товар уже есть в корзине, увеличиваем количество
if not created:
    cart_item.quantity += 1
    cart_item.save()

# Просмотр товаров в корзине
for item in cart.items.all():
    print(f"{item.product.name} x{item.quantity} = {item.product.price * item.quantity} руб.")
```

### Сложные запросы

```python
from django.db.models import Count, Avg, Sum, Q

# Количество товаров в каждой категории
categories_with_count = Category.objects.annotate(
    products_count=Count('products')
)
for cat in categories_with_count:
    print(f"{cat.name}: {cat.products_count} товаров")

# Средняя оценка товара
iphone_avg_rating = Review.objects.filter(product=iphone).aggregate(
    avg_rating=Avg('rating')
)
print(f"Средняя оценка iPhone: {iphone_avg_rating['avg_rating']}")

# Товары с отзывами
products_with_reviews = Product.objects.annotate(
    reviews_count=Count('reviews')
).filter(reviews_count__gt=0)

# Товары отсортированные по количеству отзывов
popular_products = Product.objects.annotate(
    reviews_count=Count('reviews')
).order_by('-reviews_count')

# Общая стоимость всех заказов пользователя
total_spent = Order.objects.filter(user=user).aggregate(
    total=Sum('items__product__price')
)
```

### Фильтрация по связанным объектам

```python
# Товары из категории "Электроника" и её подкатегорий
electronics_categories = Category.objects.filter(
    Q(id=electronics.id) | Q(parent=electronics)
)
electronics_products = Product.objects.filter(category__in=electronics_categories)

# Заказы, содержащие определённый товар
orders_with_iphone = Order.objects.filter(items__product=iphone).distinct()

# Пользователи, оставившие отзывы на товар
users_who_reviewed = User.objects.filter(reviews__product=iphone).distinct()
```

---

## Проверка данных

### Просмотр всех категорий с иерархией

```python
def print_categories(category, indent=0):
    """Рекурсивный вывод категорий с иерархией."""
    print('  ' * indent + f"- {category.name} ({category.products.count()} товаров)")
    for child in category.children.all():
        print_categories(child, indent + 1)

# Вывод всех корневых категорий
root_categories = Category.objects.filter(parent=None)
for cat in root_categories:
    print_categories(cat)
```

### Статистика по товарам

```python
# Общее количество товаров
total_products = Product.objects.count()
print(f"Всего товаров: {total_products}")

# Товары на складе
in_stock = Product.objects.filter(stock__gt=0).count()
print(f"Товаров на складе: {in_stock}")

# Товары без категории
no_category = Product.objects.filter(category=None).count()
print(f"Товаров без категории: {no_category}")
```

---

## Важные замечания

1. **Уникальность**: Название товара должно быть уникальным в рамках категории (благодаря `unique_together`).
2. **Каскадное удаление**: При удалении категории товары не удаляются (используется `SET_NULL`).
3. **Метод total_price()**: Автоматически вычисляет стоимость заказа на основе товаров в OrderItem.
4. **Корзина**: Каждый пользователь имеет одну корзину (OneToOneField).
5. **Оценка отзыва**: Должна быть от 1 до 5 (валидация в модели).

---

**Готово!** Теперь вы можете использовать эти примеры для выполнения Части 3 домашнего задания.

