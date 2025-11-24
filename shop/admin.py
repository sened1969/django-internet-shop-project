"""
Настройка административной панели Django для модели Product.

Позволяет управлять товарами через административный интерфейс Django.
"""
from django.contrib import admin
from .models import Product


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

