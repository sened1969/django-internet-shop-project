"""
Представления для демо-приложения API.

Демонстрируют использование APIView классов:
- ListCreateAPIView для списка и создания
- RetrieveUpdateDestroyAPIView для детальной работы
"""
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema
from api_demo.models import Article
from api_demo.serializers import ArticleSerializer


@extend_schema(
    summary="Получение списка статей",
    description="Этот эндпоинт позволяет получить список всех статей в базе данных. "
                "Вы также можете добавить новую статью с помощью POST-запроса.",
    responses={200: ArticleSerializer(many=True)}
)
class ArticleListCreateAPIView(ListCreateAPIView):
    """
    Представление для работы со списком статей и создания новых статей.
    
    GET: возвращает список всех статей
    POST: создает новую статью
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@extend_schema(
    summary="Работа с конкретной статьей",
    description="Позволяет получить информацию о статье, обновить её данные или удалить.",
    responses={
        200: ArticleSerializer,
        204: None
    }
)
class ArticleDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Представление для работы с отдельной статьей: просмотр, обновление и удаление.
    
    GET: возвращает информацию о статье
    PUT: полностью обновляет статью
    PATCH: частично обновляет статью
    DELETE: удаляет статью
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

