"""
Сериализаторы для REST API приложения books.

Преобразуют модели Django в JSON формат и обратно.
"""
from rest_framework import serializers
from books.models import Book, Publisher, Store, Review


class PublisherSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Publisher."""
    
    books_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'books_count']
        read_only_fields = ['id', 'books_count']
        extra_kwargs = {
            'name': {
                'help_text': 'Название издательства (максимум 200 символов)'
            },
            'country': {
                'help_text': 'Страна, где находится издательство (максимум 100 символов)'
            },
        }


class StoreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Store."""
    
    books_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Store
        fields = ['id', 'name', 'city', 'books_count']
        read_only_fields = ['id', 'books_count']
        extra_kwargs = {
            'name': {
                'help_text': 'Название книжного магазина (максимум 200 символов)'
            },
            'city': {
                'help_text': 'Город, где находится магазин (максимум 100 символов)'
            },
        }


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'book_title', 'rating', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'book': {
                'help_text': 'ID книги, на которую оставлен отзыв'
            },
            'rating': {
                'help_text': 'Оценка книги от 1 до 5'
            },
            'text': {
                'help_text': 'Текст отзыва о книге'
            },
        }


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Book."""
    
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    publisher_country = serializers.CharField(source='publisher.country', read_only=True)
    stores = StoreSerializer(many=True, read_only=True)
    store_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Store.objects.all(),
        source='stores',
        write_only=True,
        required=False
    )
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    avg_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'published_date', 'description',
            'publisher', 'publisher_name', 'publisher_country',
            'stores', 'store_ids', 'reviews_count', 'avg_rating'
        ]
        read_only_fields = ['id', 'publisher_name', 'publisher_country', 'stores', 'reviews_count', 'avg_rating']
        extra_kwargs = {
            'title': {
                'help_text': 'Название книги (максимум 200 символов)'
            },
            'author': {
                'help_text': 'Автор книги (максимум 100 символов)'
            },
            'published_date': {
                'help_text': 'Дата публикации книги (формат YYYY-MM-DD)'
            },
            'description': {
                'help_text': 'Описание книги'
            },
            'publisher': {
                'help_text': 'ID издательства, опубликовавшего книгу'
            },
            'store_ids': {
                'help_text': 'Список ID магазинов, где продаётся книга (для записи)'
            },
        }
    
    def get_avg_rating(self, obj):
        """Вычисляет среднюю оценку книги."""
        from django.db.models import Avg
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None


class BookDetailSerializer(BookSerializer):
    """Расширенный сериализатор для детального представления книги."""
    
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['reviews']

