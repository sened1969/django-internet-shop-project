"""
ViewSets для REST API приложения books.

Предоставляют CRUD операции для всех моделей через REST API.
"""
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from drf_spectacular.utils import extend_schema, extend_schema_view
from books.models import Book, Publisher, Store, Review
from books.api.serializers import (
    BookSerializer, BookDetailSerializer,
    PublisherSerializer,
    StoreSerializer,
    ReviewSerializer
)
from books.api.permissions import IsAdminOrReadOnly, IsManagerOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="Получение списка книг",
        description="Возвращает список всех книг с возможностью фильтрации и поиска. "
                    "Поддерживает поиск по названию, автору и описанию. "
                    "Поддерживает сортировку по названию, автору и дате публикации.",
        responses={200: BookSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получение детальной информации о книге",
        description="Возвращает подробную информацию о конкретной книге, включая отзывы.",
        responses={200: BookDetailSerializer}
    ),
    create=extend_schema(
        summary="Создание новой книги",
        description="Создает новую книгу. Требуется роль администратора или менеджера.",
        responses={201: BookSerializer}
    ),
    update=extend_schema(
        summary="Полное обновление книги",
        description="Полностью обновляет данные книги. Требуется роль администратора или менеджера.",
        responses={200: BookSerializer}
    ),
    partial_update=extend_schema(
        summary="Частичное обновление книги",
        description="Частично обновляет данные книги. Требуется роль администратора или менеджера.",
        responses={200: BookSerializer}
    ),
    destroy=extend_schema(
        summary="Удаление книги",
        description="Удаляет книгу из базы данных. Требуется роль администратора.",
        responses={204: None}
    ),
)
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
    
    @extend_schema(
        summary="Топ книг по рейтингу",
        description="Возвращает топ-10 книг с наивысшим рейтингом. "
                    "Учитываются только книги с минимум 3 отзывами.",
        responses={200: BookSerializer(many=True)}
    )
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
    
    @extend_schema(
        summary="Статистика по книгам",
        description="Возвращает общую статистику: количество книг, количество отзывов и средний рейтинг.",
        responses={200: {
            'type': 'object',
            'properties': {
                'total_books': {'type': 'integer'},
                'total_reviews': {'type': 'integer'},
                'average_rating': {'type': 'number', 'format': 'float'}
            }
        }}
    )
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


@extend_schema_view(
    list=extend_schema(
        summary="Получение списка издательств",
        description="Возвращает список всех издательств с количеством опубликованных книг.",
        responses={200: PublisherSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получение информации об издательстве",
        description="Возвращает информацию о конкретном издательстве.",
        responses={200: PublisherSerializer}
    ),
    create=extend_schema(
        summary="Создание нового издательства",
        description="Создает новое издательство. Требуется роль администратора или менеджера.",
        responses={201: PublisherSerializer}
    ),
    update=extend_schema(
        summary="Обновление издательства",
        description="Обновляет данные издательства. Требуется роль администратора или менеджера.",
        responses={200: PublisherSerializer}
    ),
    destroy=extend_schema(
        summary="Удаление издательства",
        description="Удаляет издательство. Требуется роль администратора.",
        responses={204: None}
    ),
)
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
    
    @extend_schema(
        summary="Книги издательства",
        description="Возвращает список всех книг, опубликованных данным издательством.",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Возвращает список книг издательства."""
        publisher = self.get_object()
        books = publisher.books.select_related('publisher').prefetch_related('stores', 'reviews').all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Получение списка магазинов",
        description="Возвращает список всех книжных магазинов с количеством книг в наличии.",
        responses={200: StoreSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получение информации о магазине",
        description="Возвращает информацию о конкретном магазине.",
        responses={200: StoreSerializer}
    ),
    create=extend_schema(
        summary="Создание нового магазина",
        description="Создает новый книжный магазин. Требуется роль администратора или менеджера.",
        responses={201: StoreSerializer}
    ),
    update=extend_schema(
        summary="Обновление магазина",
        description="Обновляет данные магазина. Требуется роль администратора или менеджера.",
        responses={200: StoreSerializer}
    ),
    destroy=extend_schema(
        summary="Удаление магазина",
        description="Удаляет магазин. Требуется роль администратора.",
        responses={204: None}
    ),
)
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
    
    @extend_schema(
        summary="Книги в магазине",
        description="Возвращает список всех книг, которые продаются в данном магазине.",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Возвращает список книг в магазине."""
        store = self.get_object()
        books = store.books.select_related('publisher').prefetch_related('stores', 'reviews').all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Получение списка отзывов",
        description="Возвращает список всех отзывов с возможностью фильтрации и поиска.",
        responses={200: ReviewSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получение информации об отзыве",
        description="Возвращает информацию о конкретном отзыве.",
        responses={200: ReviewSerializer}
    ),
    create=extend_schema(
        summary="Создание нового отзыва",
        description="Создает новый отзыв на книгу. Требуется авторизация.",
        responses={201: ReviewSerializer}
    ),
    update=extend_schema(
        summary="Обновление отзыва",
        description="Обновляет отзыв. Требуется роль администратора.",
        responses={200: ReviewSerializer}
    ),
    destroy=extend_schema(
        summary="Удаление отзыва",
        description="Удаляет отзыв. Требуется роль администратора.",
        responses={204: None}
    ),
)
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

