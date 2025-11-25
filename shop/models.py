"""
Модели для интернет-магазина.

Модели для работы с товарами, категориями, заказами, отзывами и корзиной покупок.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class CustomUserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет обычного пользователя с указанным email и паролем."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя с указанным email и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Суперпользователь активен по умолчанию

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    
    Использует email в качестве основного поля для аутентификации.
    """
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Email адрес пользователя'
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Номер телефона',
        help_text='Номер телефона пользователя'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Адрес доставки',
        help_text='Адрес доставки пользователя'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Аккаунт активен',
        help_text='Указывает, подтвержден ли email пользователя'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Сотрудник',
        help_text='Указывает, является ли пользователь сотрудником'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации',
        help_text='Дата и время регистрации пользователя'
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.email
    
    def get_full_name(self):
        """Возвращает полное имя пользователя (email)."""
        return self.email
    
    def get_short_name(self):
        """Возвращает короткое имя пользователя (email)."""
        return self.email


class Category(models.Model):
    """
    Модель категории товаров.
    
    Поддерживает вложенные категории через self-referencing ForeignKey.
    
    Атрибуты:
        name (CharField): Название категории
        description (TextField): Описание категории (необязательное)
        parent (ForeignKey): Родительская категория для создания вложенных категорий
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание категории',
        help_text='Описание категории (необязательно)'
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория',
        help_text='Выберите родительскую категорию для создания вложенной категории'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        """Возвращает строковое представление категории."""
        if self.parent:
            return f'{self.parent.name} > {self.name}'
        return self.name


class Product(models.Model):
    """
    Модель товара в интернет-магазине.
    
    Атрибуты:
        name (CharField): Название товара
        description (TextField): Подробное описание товара
        price (DecimalField): Цена товара с валидацией минимального значения
        stock (IntegerField): Количество товара на складе
        image (ImageField): Изображение товара (опционально)
        category (ForeignKey): Связь с категорией товара
        created_at (DateTimeField): Дата и время создания записи
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название товара',
        help_text='Введите название товара'
    )
    
    description = models.TextField(
        verbose_name='Описание товара',
        help_text='Подробное описание товара'
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Цена товара',
        help_text='Цена товара в рублях'
    )
    
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Количество на складе',
        help_text='Количество товара на складе'
    )
    
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение товара',
        help_text='Загрузите изображение товара'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Категория товара',
        help_text='Выберите категорию товара'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время добавления товара'
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']  # Сортировка по дате создания (новые сначала)
        db_table = 'shop_products'  # Имя таблицы в базе данных
        unique_together = ['name', 'category']  # Уникальность названия в рамках категории
    
    def __str__(self):
        """Возвращает строковое представление товара."""
        return self.name


class Message(models.Model):
    """
    Модель сообщения от пользователя.
    
    Атрибуты:
        user (ForeignKey): Связь с пользователем (опционально, если не авторизован)
        name (CharField): Имя отправителя
        email (EmailField): Электронная почта отправителя
        message (TextField): Текст сообщения
        created_at (DateTimeField): Дата и время создания сообщения
    """
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь',
        help_text='Пользователь, отправивший сообщение (если авторизован)'
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        help_text='Имя отправителя сообщения'
    )
    
    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Email отправителя сообщения'
    )
    
    message = models.TextField(
        verbose_name='Сообщение',
        help_text='Текст сообщения'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время отправки сообщения'
    )
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']  # Сортировка по дате создания (новые сначала)
    
    def __str__(self):
        """Возвращает строковое представление сообщения."""
        return f'Сообщение от {self.name} ({self.email})'


class Order(models.Model):
    """
    Модель заказа в интернет-магазине.
    
    Атрибуты:
        user (ForeignKey): Пользователь, оформивший заказ
        created_at (DateTimeField): Дата и время создания заказа
        status (CharField): Статус заказа (в обработке, доставляется, доставлено)
    """
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('shipping', 'Доставляется'),
        ('delivered', 'Доставлено'),
    ]
    
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь',
        help_text='Пользователь, оформивший заказ'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа',
        help_text='Дата и время оформления заказа'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing',
        verbose_name='Статус заказа',
        help_text='Текущий статус заказа'
    )
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        """Возвращает строковое представление заказа."""
        return f'Заказ #{self.id} от {self.user.email} ({self.get_status_display()})'
    
    def total_price(self):
        """
        Вычисляет общую стоимость заказа.
        
        Суммирует стоимость всех товаров в заказе с учётом их количества.
        
        Returns:
            Decimal: Общая стоимость заказа
        """
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total
    
    total_price.short_description = 'Общая стоимость'


class OrderItem(models.Model):
    """
    Модель товара в заказе.
    
    Атрибуты:
        order (ForeignKey): Заказ, к которому относится товар
        product (ForeignKey): Товар
        quantity (IntegerField): Количество товара в заказе
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
        help_text='Заказ, к которому относится товар'
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Товар',
        help_text='Товар в заказе'
    )
    
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
        help_text='Количество товара в заказе'
    )
    
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'
    
    def __str__(self):
        """Возвращает строковое представление товара в заказе."""
        return f'{self.product.name} x{self.quantity} в заказе #{self.order.id}'


class Review(models.Model):
    """
    Модель отзыва о товаре.
    
    Атрибуты:
        product (ForeignKey): Товар, на который оставлен отзыв
        user (ForeignKey): Пользователь, оставивший отзыв
        rating (IntegerField): Оценка товара (от 1 до 5)
        text (TextField): Текст отзыва
        created_at (DateTimeField): Дата и время создания отзыва
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар',
        help_text='Товар, на который оставлен отзыв'
    )
    
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
        help_text='Пользователь, оставивший отзыв'
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка',
        help_text='Оценка товара от 1 до 5'
    )
    
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Текст отзыва о товаре'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время создания отзыва'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        """Возвращает строковое представление отзыва."""
        return f'Отзыв от {self.user.email} на {self.product.name} ({self.rating}/5)'


class Cart(models.Model):
    """
    Модель корзины покупок пользователя.
    
    Атрибуты:
        user (ForeignKey): Пользователь, владелец корзины
        created_at (DateTimeField): Дата и время создания корзины
        updated_at (DateTimeField): Дата и время последнего обновления корзины
    """
    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
        help_text='Владелец корзины'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время создания корзины'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
        help_text='Дата и время последнего обновления корзины'
    )
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        """Возвращает строковое представление корзины."""
        return f'Корзина пользователя {self.user.email}'


class CartItem(models.Model):
    """
    Модель товара в корзине покупок.
    
    Атрибуты:
        cart (ForeignKey): Корзина, к которой относится товар
        product (ForeignKey): Товар
        quantity (IntegerField): Количество товара в корзине
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина',
        help_text='Корзина, к которой относится товар'
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар',
        help_text='Товар в корзине'
    )
    
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
        help_text='Количество товара в корзине'
    )
    
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'
        unique_together = ['cart', 'product']  # Один товар может быть только один раз в корзине
    
    def __str__(self):
        """Возвращает строковое представление товара в корзине."""
        return f'{self.product.name} x{self.quantity} в корзине {self.cart.user.email}'

