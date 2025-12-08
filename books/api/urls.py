"""
URL маршруты для REST API приложения books.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from books.api import views

# Создаем router для ViewSets
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'publishers', views.PublisherViewSet, basename='publisher')
router.register(r'stores', views.StoreViewSet, basename='store')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    # Маршруты для ViewSets
    path('', include(router.urls)),
    
    # Маршрут для детального просмотра категории с вложенными книгами
    path('categories/<int:pk>/detail/', views.CategoryDetailView.as_view(), name='category-detail-books'),
    
    # Маршруты для JWT токенов
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # OAuth 2.0 защищенный ресурс (Тема 25)
    path('oauth2/protected/', views.OAuth2ProtectedView.as_view(), name='oauth2-protected'),
]

