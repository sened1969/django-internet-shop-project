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
    
    # Маршрут для детальной информации о товаре
    # product_id - это ID товара в базе данных
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Маршруты для регистрации и авторизации
    path('register/', views.register, name='register'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Маршрут для главной страницы авторизованных пользователей
    path('home/', views.home, name='home'),
    
    # Маршруты для работы с сообщениями
    path('contact/', views.contact, name='contact'),
    path('contact/ajax/', views.contact_ajax, name='contact_ajax'),
    
    # Маршрут для профиля пользователя
    path('profile/', views.profile, name='profile'),
]

