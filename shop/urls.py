"""
URL-маршруты для приложения shop.

Определяет маршруты для отображения списка товаров,
детальной информации о товаре, а также для работы с формами
регистрации, авторизации и отправки сообщений.
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Маршрут для списка всех товаров
    path('', views.product_list, name='product_list'),
    
    # Маршрут для добавления нового товара
    path('product/add/', views.add_product, name='add_product'),
    
    # Маршрут для детальной информации о товаре
    # product_id - это ID товара в базе данных
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Маршруты для регистрации и авторизации
    path('register/', views.register, name='register'),
    path('email-confirmation-sent/', views.email_confirmation_sent, name='email_confirmation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Маршрут для главной страницы авторизованных пользователей
    path('home/', views.home, name='home'),
    
    # Маршруты для работы с сообщениями
    path('contact/', views.contact, name='contact'),
    path('contact/ajax/', views.contact_ajax, name='contact_ajax'),
    
    # Маршруты для профиля пользователя
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/password-change/', views.password_change, name='password_change'),
    
    # Маршруты для сброса пароля
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Маршруты для удаления аккаунта
    path('account-delete-request/', views.account_delete_request, name='account_delete_request'),
    path('account-delete-confirm/<uidb64>/<token>/', views.account_delete_confirm, name='account_delete_confirm'),
    
    # Маршруты для корзины
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

