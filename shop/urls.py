"""
URL-маршруты для приложения shop.

Определяет маршруты для отображения списка товаров
и детальной информации о товаре.
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
]

