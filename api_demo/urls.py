"""
URL маршруты для демо-приложения API.

Демонстрируют использование явных маршрутов вместо Router.
"""
from django.urls import path
from api_demo.views import ArticleListCreateAPIView, ArticleDetailAPIView


urlpatterns = [
    # Список статей и создание новой статьи
    path('articles/', ArticleListCreateAPIView.as_view(), name='article-list-create'),
    
    # Детальная работа с конкретной статьей
    path('articles/<int:pk>/', ArticleDetailAPIView.as_view(), name='article-detail'),
]

