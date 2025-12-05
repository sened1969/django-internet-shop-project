from django.contrib import admin
from api_demo.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Article."""
    list_display = ['title', 'author', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'author']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'content')
        }),
        ('Публикация', {
            'fields': ('is_published',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

