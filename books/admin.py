"""
Настройка административной панели Django для моделей книг.

Позволяет управлять издательствами, книгами, магазинами и отзывами через административный интерфейс Django.
"""
from django.contrib import admin
from django.db.models import Count, Avg
from .models import Publisher, Book, Store, Review


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Publisher в админ-панели.
    """
    list_display = ('name', 'country', 'books_count')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'country')
        }),
    )
    
    def books_count(self, obj):
        """Возвращает количество книг издательства."""
        return obj.books.count()
    books_count.short_description = 'Количество книг'


class ReviewInline(admin.TabularInline):
    """Инлайн-редактор для отзывов на книги."""
    model = Review
    extra = 1
    fields = ('rating', 'text', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Book в админ-панели.
    """
    list_display = ('title', 'author', 'publisher', 'published_date', 'reviews_count', 'avg_rating')
    list_filter = ('publisher', 'published_date')
    search_fields = ('title', 'author', 'description')
    readonly_fields = ('published_date',)
    inlines = [ReviewInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'publisher', 'published_date')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Магазины', {
            'fields': ('stores',)
        }),
    )
    
    filter_horizontal = ('stores',)
    
    def reviews_count(self, obj):
        """Возвращает количество отзывов на книгу."""
        return obj.reviews.count()
    reviews_count.short_description = 'Количество отзывов'
    
    def avg_rating(self, obj):
        """Возвращает среднюю оценку книги."""
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return f'{avg:.2f}' if avg else 'Нет оценок'
    avg_rating.short_description = 'Средняя оценка'


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Store в админ-панели.
    """
    list_display = ('name', 'city', 'books_count')
    list_filter = ('city',)
    search_fields = ('name', 'city')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'city')
        }),
    )
    
    def books_count(self, obj):
        """Возвращает количество книг в магазине."""
        return obj.books.count()
    books_count.short_description = 'Количество книг'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Review в админ-панели.
    """
    list_display = ('book', 'rating', 'created_at', 'text_preview')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'book__author', 'text')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('book', 'rating')
        }),
        ('Отзыв', {
            'fields': ('text',)
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )
    
    def text_preview(self, obj):
        """Возвращает краткое описание отзыва."""
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        return obj.text
    text_preview.short_description = 'Предпросмотр отзыва'
