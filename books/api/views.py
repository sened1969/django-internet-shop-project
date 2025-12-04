"""
ViewSets для REST API приложения books.

Предоставляют CRUD операции для всех моделей через REST API.
"""
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from books.models import Book, Publisher, Store, Review
from books.api.serializers import (
    BookSerializer, BookDetailSerializer,
    PublisherSerializer,
    StoreSerializer,
    ReviewSerializer
)
from books.api.permissions import IsAdminOrReadOnly, IsManagerOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с книгами.
    
    Доступ:
    - GET: все пользователи
    - POST, PUT, PATCH: администраторы и менеджеры
    - DELETE: только администраторы
    """
    queryset = Book.objects.select_related('publisher').prefetch_related('stores', 'reviews').all()
    permission_classes = [IsManagerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['title', 'author', 'published_date']
    ordering = ['-published_date']
    
    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от действия."""
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer
    
    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """Возвращает топ книг по рейтингу."""
        books = self.get_queryset().annotate(
            avg_rating=Avg('reviews__rating'),
            reviews_count=Count('reviews')
        ).filter(
            reviews_count__gte=3
        ).order_by('-avg_rating')[:10]
        
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Возвращает статистику по книгам."""
        total_books = Book.objects.count()
        total_reviews = Review.objects.count()
        avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        
        return Response({
            'total_books': total_books,
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2)
        })


class PublisherViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с издательствами.
    
    Доступ:
    - GET: все пользователи
    - POST, PUT, PATCH: администраторы и менеджеры
    - DELETE: только администраторы
    """
    queryset = Publisher.objects.annotate(
        books_count=Count('books')
    ).all()
    serializer_class = PublisherSerializer
    permission_classes = [IsManagerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'country']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Возвращает список книг издательства."""
        publisher = self.get_object()
        books = publisher.books.select_related('publisher').prefetch_related('stores', 'reviews').all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class StoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с магазинами.
    
    Доступ:
    - GET: все пользователи
    - POST, PUT, PATCH: администраторы и менеджеры
    - DELETE: только администраторы
    """
    queryset = Store.objects.annotate(
        books_count=Count('books')
    ).all()
    serializer_class = StoreSerializer
    permission_classes = [IsManagerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city']
    ordering_fields = ['name', 'city']
    ordering = ['city', 'name']
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Возвращает список книг в магазине."""
        store = self.get_object()
        books = store.books.select_related('publisher').prefetch_related('stores', 'reviews').all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    
    Доступ:
    - GET: все пользователи
    - POST: все авторизованные пользователи
    - PUT, PATCH, DELETE: только администраторы
    """
    queryset = Review.objects.select_related('book').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'book__title']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Настраивает разрешения в зависимости от действия."""
        if self.action == 'create':
            # Создание разрешено всем авторизованным пользователям
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Для остальных действий используем стандартные разрешения
            permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]

