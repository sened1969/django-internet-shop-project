"""
Настройка административной панели Django для моделей Product и Message.

Позволяет управлять товарами и сообщениями через административный интерфейс Django.
"""
from django.contrib import admin
from .models import Product, Message


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Product в админ-панели.
    """
    list_display = ('name', 'price', 'created_at', 'has_image')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )
    
    def has_image(self, obj):
        """Проверяет, есть ли у товара изображение."""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Есть изображение'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Message в админ-панели.
    """
    list_display = ('name', 'email', 'user', 'created_at', 'message_preview')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Информация об отправителе', {
            'fields': ('user', 'name', 'email')
        }),
        ('Сообщение', {
            'fields': ('message',)
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )
    
    def message_preview(self, obj):
        """Возвращает краткое описание сообщения."""
        if len(obj.message) > 50:
            return obj.message[:50] + '...'
        return obj.message
    message_preview.short_description = 'Предпросмотр сообщения'

