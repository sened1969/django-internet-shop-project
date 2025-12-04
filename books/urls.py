"""
URL-маршруты для приложения books.

Определяет маршруты для всех CRUD операций с книгами, издательствами, магазинами и отзывами.
"""
from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # ==================== BOOK URLs ====================
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/update/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # ==================== PUBLISHER URLs ====================
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publisher/<int:pk>/', views.publisher_detail, name='publisher_detail'),
    path('publisher/create/', views.publisher_create, name='publisher_create'),
    path('publisher/<int:pk>/update/', views.publisher_update, name='publisher_update'),
    path('publisher/<int:pk>/delete/', views.publisher_delete, name='publisher_delete'),
    
    # ==================== STORE URLs ====================
    path('stores/', views.store_list, name='store_list'),
    path('store/<int:pk>/', views.store_detail, name='store_detail'),
    path('store/create/', views.store_create, name='store_create'),
    path('store/<int:pk>/update/', views.store_update, name='store_update'),
    path('store/<int:pk>/delete/', views.store_delete, name='store_delete'),
    
    # ==================== REVIEW URLs ====================
    path('reviews/', views.review_list, name='review_list'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('review/create/', views.review_create, name='review_create'),
    path('review/<int:pk>/update/', views.review_update, name='review_update'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    
    # ==================== ANALYTICS ====================
    path('analytics/', views.analytics, name='analytics'),
]

