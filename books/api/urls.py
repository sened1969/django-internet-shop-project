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

urlpatterns = [
    # Маршруты для ViewSets
    path('', include(router.urls)),
    
    # Маршруты для JWT токенов
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

