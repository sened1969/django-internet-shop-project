"""
Модели для интернет-магазина.

Модели Product и Message для работы с товарами и сообщениями пользователей.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from decimal import Decimal


class Product(models.Model):
    """
    Модель товара в интернет-магазине.
    
    Атрибуты:
        name (CharField): Название товара
        description (TextField): Подробное описание товара
        price (DecimalField): Цена товара с валидацией минимального значения
        image (ImageField): Изображение товара (опционально)
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
    
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение товара',
        help_text='Загрузите изображение товара'
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
        User,
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
        max_length=500,
        verbose_name='Сообщение',
        help_text='Текст сообщения (максимум 500 символов)'
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

