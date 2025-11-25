"""
Настройка административной панели Django для всех моделей интернет-магазина.

Позволяет управлять товарами, категориями, заказами, отзывами и корзиной через административный интерфейс Django.
"""
from django.contrib import admin
from .models import (
    Category, Product, Message, Order, OrderItem, 
    Review, Cart, CartItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Category в админ-панели.
    """
    list_display = ('name', 'parent', 'products_count')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'parent')
        }),
    )
    
    def products_count(self, obj):
        """Возвращает количество товаров в категории."""
        return obj.products.count()
    products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Product в админ-панели.
    """
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'has_image')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'price', 'stock')
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


class OrderItemInline(admin.TabularInline):
    """Инлайн-редактор для товаров в заказе."""
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Order в админ-панели.
    """
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'total_price')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status', 'created_at')
        }),
        ('Стоимость', {
            'fields': ('total_price',)
        }),
    )
    
    def total_price(self, obj):
        """Отображает общую стоимость заказа."""
        return f'{obj.total_price():.2f} руб.'
    total_price.short_description = 'Общая стоимость'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели OrderItem в админ-панели.
    """
    list_display = ('order', 'product', 'quantity', 'item_total')
    list_filter = ('order',)
    search_fields = ('product__name', 'order__user__username')
    
    def item_total(self, obj):
        """Вычисляет общую стоимость товара в заказе."""
        return f'{obj.product.price * obj.quantity:.2f} руб.'
    item_total.short_description = 'Стоимость'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Review в админ-панели.
    """
    list_display = ('product', 'user', 'rating', 'created_at', 'text_preview')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'text')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('product', 'user', 'rating')
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


class CartItemInline(admin.TabularInline):
    """Инлайн-редактор для товаров в корзине."""
    model = CartItem
    extra = 1
    fields = ('product', 'quantity')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Cart в админ-панели.
    """
    list_display = ('user', 'items_count', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Информация о корзине', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
    )
    
    def items_count(self, obj):
        """Возвращает количество товаров в корзине."""
        return obj.items.count()
    items_count.short_description = 'Количество товаров'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели CartItem в админ-панели.
    """
    list_display = ('cart', 'product', 'quantity', 'item_total')
    list_filter = ('cart',)
    search_fields = ('product__name', 'cart__user__username')
    
    def item_total(self, obj):
        """Вычисляет общую стоимость товара в корзине."""
        return f'{obj.product.price * obj.quantity:.2f} руб.'
    item_total.short_description = 'Стоимость'

