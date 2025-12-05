"""
Модели для демо-приложения API.

Простая модель Article для демонстрации создания API через APIView классы.
"""
from django.db import models
from django.core.validators import MinLengthValidator


class Article(models.Model):
    """
    Модель статьи.
    
    Простая модель для демонстрации работы с Django REST Framework
    через APIView классы (ListCreateAPIView, RetrieveUpdateDestroyAPIView).
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Заголовок статьи (максимум 200 символов)',
        validators=[MinLengthValidator(5)]
    )
    
    content = models.TextField(
        verbose_name='Содержание',
        help_text='Текст статьи'
    )
    
    author = models.CharField(
        max_length=100,
        verbose_name='Автор',
        help_text='Имя автора статьи (максимум 100 символов)'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время создания статьи'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
        help_text='Дата и время последнего обновления статьи'
    )
    
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Статья опубликована и доступна для просмотра'
    )
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
    
    def __str__(self):
        """Возвращает строковое представление статьи."""
        return f'{self.title} - {self.author}'

