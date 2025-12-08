"""
Модели для работы с книгами, издательствами, магазинами и отзывами.

Модели для выполнения домашнего задания по теме #20 "Запросы в Django ORM".
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Publisher(models.Model):
    """
    Модель издательства.
    
    Представляет издательство, которое публикует книги.
    Одно издательство может опубликовать несколько книг (связь один ко многим).
    
    Атрибуты:
        name (CharField): Название издательства
        country (CharField): Страна, где находится издательство
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название издательства',
        help_text='Введите название издательства'
    )
    
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        help_text='Введите страну, где находится издательство'
    )
    
    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'
        ordering = ['name']
    
    def __str__(self):
        """Возвращает строковое представление издательства."""
        return f'{self.name} ({self.country})'


class Store(models.Model):
    """
    Модель книжного магазина.
    
    Представляет книжный магазин, где продаются книги.
    Один магазин может продавать несколько книг, и одна книга может продаваться 
    в нескольких магазинах (связь многие ко многим).
    
    Атрибуты:
        name (CharField): Название магазина
        city (CharField): Город, где находится магазин
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название магазина',
        help_text='Введите название книжного магазина'
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        help_text='Введите город, где находится магазин'
    )
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['city', 'name']
    
    def __str__(self):
        """Возвращает строковое представление магазина."""
        return f'{self.name} ({self.city})'


class Category(models.Model):
    """
    Модель категории книг.
    
    Представляет категорию, к которой относятся книги.
    Одна категория может содержать несколько книг (связь один ко многим).
    
    Атрибуты:
        name (CharField): Название категории
        description (TextField): Описание категории
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории',
        help_text='Введите название категории книг'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание категории',
        help_text='Описание категории (необязательно)'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        """Возвращает строковое представление категории."""
        return self.name


class Book(models.Model):
    """
    Модель книги.
    
    Представляет книгу с информацией об авторе, дате публикации и описании.
    Книга связана с издательством (один ко многим), категорией (один ко многим) 
    и магазинами (многие ко многим).
    
    Атрибуты:
        title (CharField): Название книги
        author (CharField): Автор книги
        published_date (DateField): Дата публикации
        description (TextField): Описание книги
        publisher (ForeignKey): Издательство, опубликовавшее книгу
        category (ForeignKey): Категория книги
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Название книги',
        help_text='Введите название книги'
    )
    
    author = models.CharField(
        max_length=100,
        verbose_name='Автор',
        help_text='Введите имя автора книги'
    )
    
    published_date = models.DateField(
        verbose_name='Дата публикации',
        help_text='Дата публикации книги'
    )
    
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание книги'
    )
    
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Издательство',
        help_text='Издательство, опубликовавшее книгу'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='books',
        null=True,
        blank=True,
        verbose_name='Категория',
        help_text='Категория книги'
    )
    
    stores = models.ManyToManyField(
        Store,
        related_name='books',
        blank=True,
        verbose_name='Магазины',
        help_text='Магазины, где продаётся книга'
    )
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-published_date', 'title']
    
    def __str__(self):
        """Возвращает строковое представление книги."""
        return f'{self.title} - {self.author}'


class Review(models.Model):
    """
    Модель отзыва на книгу.
    
    Представляет отзыв пользователя на книгу с оценкой и комментарием.
    Одна книга может иметь много отзывов (связь один ко многим).
    
    Атрибуты:
        book (ForeignKey): Книга, на которую оставлен отзыв
        rating (IntegerField): Оценка книги (от 1 до 5)
        text (TextField): Текст отзыва
        created_at (DateTimeField): Дата создания отзыва
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Книга',
        help_text='Книга, на которую оставлен отзыв'
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка',
        help_text='Оценка книги от 1 до 5'
    )
    
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Текст отзыва о книге'
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
        return f'Отзыв на "{self.book.title}" - {self.rating}/5'
