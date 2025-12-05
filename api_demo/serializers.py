"""
Сериализаторы для демо-приложения API.

Демонстрируют использование ModelSerializer с extra_kwargs для документации.
"""
from rest_framework import serializers
from api_demo.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Article."""
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {
                'help_text': 'Заголовок статьи (минимум 5 символов, максимум 200 символов)'
            },
            'content': {
                'help_text': 'Текст статьи. Может содержать любое количество символов.'
            },
            'author': {
                'help_text': 'Имя автора статьи (максимум 100 символов)'
            },
            'is_published': {
                'help_text': 'Установите True, чтобы опубликовать статью. По умолчанию False.'
            },
            'created_at': {
                'help_text': 'Дата и время создания статьи (автоматически устанавливается при создании)'
            },
            'updated_at': {
                'help_text': 'Дата и время последнего обновления статьи (автоматически обновляется)'
            },
        }

