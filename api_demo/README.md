# API Demo - Демо-приложение для темы #24

Демо-приложение для демонстрации использования APIView классов в Django REST Framework.

## Описание

Это приложение создано для демонстрации:
- Использования `ListCreateAPIView` для списка и создания объектов
- Использования `RetrieveUpdateDestroyAPIView` для детальной работы с объектами
- Настройки сериализаторов с `extra_kwargs` и `help_text`
- Использования `@extend_schema` для документации

## Установка

1. Убедитесь, что установлены все зависимости:
```bash
pip install -r requirements.txt
```

2. Примените миграции:
```bash
python manage.py makemigrations api_demo
python manage.py migrate
```

3. Создайте суперпользователя (опционально):
```bash
python manage.py createsuperuser
```

## Использование

### URL эндпоинты

- `GET /api/demo/articles/` - список всех статей
- `POST /api/demo/articles/` - создание новой статьи
- `GET /api/demo/articles/{id}/` - получение статьи по ID
- `PUT /api/demo/articles/{id}/` - полное обновление статьи
- `PATCH /api/demo/articles/{id}/` - частичное обновление статьи
- `DELETE /api/demo/articles/{id}/` - удаление статьи

### Примеры запросов

**Создание статьи:**
```bash
curl -X POST http://127.0.0.1:8000/api/demo/articles/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Моя первая статья",
    "content": "Содержание статьи...",
    "author": "Иван Иванов",
    "is_published": true
  }'
```

**Получение списка статей:**
```bash
curl http://127.0.0.1:8000/api/demo/articles/
```

**Получение статьи по ID:**
```bash
curl http://127.0.0.1:8000/api/demo/articles/1/
```

## Документация

Полная документация API доступна в Swagger UI:
- `http://127.0.0.1:8000/api/docs/`

## Отличия от ViewSets

Это приложение демонстрирует использование APIView классов вместо ViewSets:
- Явные маршруты вместо Router
- Отдельные классы для списка и детальной работы
- Больше контроля над каждым методом
- Проще для понимания новичкам

