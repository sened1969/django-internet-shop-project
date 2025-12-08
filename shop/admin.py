"""
Настройка административной панели Django для всех моделей интернет-магазина.

Позволяет управлять товарами, категориями, заказами, отзывами и корзиной через административный интерфейс Django.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    CustomUser, Category, Product, Message, Order, OrderItem, 
    Review, Cart, CartItem
)

# Импорт для кастомизации OAuth2 админки
try:
    from oauth2_provider.models import Application
    from oauth2_provider.admin import ApplicationAdmin as BaseApplicationAdmin
    OAUTH2_AVAILABLE = True
except ImportError:
    OAUTH2_AVAILABLE = False


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Административный интерфейс для кастомной модели пользователя."""
    
    list_display = ('email', 'phone_number', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'phone_number')
    ordering = ('-date_joined',)
    
    # Важно: метод __str__ в CustomUser возвращает email, что используется виджетом для отображения
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Персональная информация'), {
            'fields': ('phone_number', 'address')
        }),
        (_('Роль и права доступа'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Важные даты'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone_number', 'address'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined')


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
    search_fields = ('user__email',)
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
    search_fields = ('product__name', 'order__user__email')
    
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
    search_fields = ('product__name', 'user__email', 'text')
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
    search_fields = ('user__email',)
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
    search_fields = ('product__name', 'cart__user__email')
    
    def item_total(self, obj):
        """Вычисляет общую стоимость товара в корзине."""
        return f'{obj.product.price * obj.quantity:.2f} руб.'
    item_total.short_description = 'Стоимость'


# Кастомизация админки OAuth2 Application для работы с CustomUser
if OAUTH2_AVAILABLE:
    # Отменяем автоматическую регистрацию и регистрируем заново с кастомным admin
    try:
        admin.site.unregister(Application)
    except admin.sites.NotRegistered:
        pass  # Модель еще не была зарегистрирована
    
    @admin.register(Application)
    class CustomApplicationAdmin(BaseApplicationAdmin):
        """
        Кастомный admin для OAuth2 Application, который правильно работает с CustomUser.
        
        Исправляет проблему с выбором пользователя в форме создания OAuth2 приложения,
        когда используется кастомная модель пользователя с email вместо username.
        
        Проблема: виджет выбора пользователя может показывать неправильное значение
        (например, "admin" из поля role вместо email). Это решается правильной настройкой
        queryset и использованием метода __str__ модели CustomUser (который возвращает email).
        """
        # Убеждаемся, что поле user НЕ использует raw_id_fields (RawIdWidget)
        # Это важно для правильной работы с CustomUser
        raw_id_fields = tuple(f for f in getattr(BaseApplicationAdmin, 'raw_id_fields', ()) if f != 'user')
        
        # Настройка отображения списка приложений
        # list_display уже наследуется от BaseApplicationAdmin: ('pk', 'name', 'user', 'client_type', 'authorization_grant_type')
        # Добавляем ссылки для редактирования (кликабельные поля)
        list_display_links = ('pk', 'name')  # Можно кликнуть на PK или Name для редактирования
        
        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            """Переопределяем поле выбора пользователя для работы с CustomUser."""
            if db_field.name == "user":
                # Используем правильную модель пользователя из настроек
                from django.contrib.auth import get_user_model
                from django import forms
                User = get_user_model()
                
                # Создаем queryset с правильной моделью пользователя
                # Важно: используем все объекты CustomUser, отсортированные по email
                queryset = User.objects.all().order_by('email')
                kwargs["queryset"] = queryset
                
                # ВАЖНО: Явно указываем использование обычного Select виджета вместо RawIdWidget
                # RawIdWidget требует ввода ID вручную, что может вызывать проблемы с валидацией
                # Обычный Select виджет использует метод __str__ модели для отображения (email)
                kwargs["widget"] = forms.Select(attrs={'class': 'form-control'})
                
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
        def get_form(self, request, obj=None, **kwargs):
            """Переопределяем форму для правильной работы с CustomUser."""
            form = super().get_form(request, obj, **kwargs)
            # Убеждаемся, что поле user использует правильный queryset
            if 'user' in form.base_fields:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                # Устанавливаем правильный queryset с правильной моделью
                # Важно: используем все объекты CustomUser, отсортированные по email
                form.base_fields['user'].queryset = User.objects.all().order_by('email')
                # Убеждаемся, что поле использует правильную модель для валидации
                form.base_fields['user'].queryset.model = User
                # Убеждаемся, что поле использует правильный to_field (по умолчанию pk)
                # Это важно для правильной валидации выбранного значения при сохранении
            return form

