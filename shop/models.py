"""
Модель Product для интернет-магазина.

Эта модель представляет товар в интернет-магазине и содержит
всю необходимую информацию о товаре: название, описание, цену,
изображение и дату создания.
"""
from django.db import models
from django.core.validators import MinValueValidator
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

