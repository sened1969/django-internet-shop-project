"""
Представления для работы с книгами, издательствами, магазинами и отзывами.

Реализует CRUD операции для всех моделей приложения books.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Avg, Sum, Max, Min, Q
from django.core.paginator import Paginator
from .models import Book, Publisher, Store, Review
from .forms import BookForm, PublisherForm, StoreForm, ReviewForm


# ==================== BOOK CRUD ====================

def book_list(request):
    """
    Отображение списка всех книг с фильтрацией и сортировкой.
    
    Поддерживает:
    - Фильтрацию по издательству и дате публикации
    - Сортировку по названию, автору, дате публикации
    - Поиск по названию и автору
    - Пагинацию (10 книг на странице)
    """
    books = Book.objects.select_related('publisher').prefetch_related('stores', 'reviews').all()
    
    # Фильтрация по издательству
    publisher_id = request.GET.get('publisher')
    if publisher_id:
        books = books.filter(publisher_id=publisher_id)
    
    # Фильтрация по году публикации
    year = request.GET.get('year')
    if year:
        try:
            books = books.filter(published_date__year=int(year))
        except ValueError:
            pass
    
    # Поиск по названию или автору
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )
    
    # Сортировка
    sort = request.GET.get('sort', '-published_date')
    valid_sorts = {
        'title': 'title',
        '-title': '-title',
        'author': 'author',
        '-author': '-author',
        'published_date': 'published_date',
        '-published_date': '-published_date',
    }
    if sort in valid_sorts:
        books = books.order_by(valid_sorts[sort])
    
    # Пагинация
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Получаем все издательства для фильтра
    publishers = Publisher.objects.all()
    
    context = {
        'books': page_obj,
        'publishers': publishers,
        'current_publisher': publisher_id,
        'current_year': year,
        'current_search': search_query,
        'current_sort': sort,
        'page_title': 'Список книг',
    }
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    """
    Отображение детальной информации о книге.
    
    Показывает:
    - Полную информацию о книге
    - Список отзывов на книгу
    - Среднюю оценку книги
    """
    book = get_object_or_404(
        Book.objects.select_related('publisher').prefetch_related('stores', 'reviews'),
        pk=pk
    )
    
    # Вычисляем среднюю оценку
    avg_rating = book.reviews.aggregate(Avg('rating'))['rating__avg']
    reviews_count = book.reviews.count()
    
    context = {
        'book': book,
        'avg_rating': avg_rating,
        'reviews_count': reviews_count,
        'page_title': f'{book.title} - Детали книги',
    }
    return render(request, 'books/book_detail.html', context)


def book_create(request):
    """
    Создание новой книги.
    
    Обрабатывает GET и POST запросы:
    - GET: отображает форму создания книги
    - POST: сохраняет новую книгу и перенаправляет на список книг
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно создана!')
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'page_title': 'Создание новой книги',
    }
    return render(request, 'books/book_create.html', context)


def book_update(request, pk):
    """
    Редактирование существующей книги.
    
    Обрабатывает GET и POST запросы:
    - GET: отображает форму редактирования с текущими данными
    - POST: сохраняет изменения и перенаправляет на детальную страницу
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно обновлена!')
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'page_title': f'Редактирование книги "{book.title}"',
    }
    return render(request, 'books/book_update.html', context)


def book_delete(request, pk):
    """
    Удаление книги с подтверждением.
    
    Обрабатывает GET и POST запросы:
    - GET: отображает страницу подтверждения удаления
    - POST: удаляет книгу и перенаправляет на список книг
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Книга "{title}" успешно удалена!')
        return redirect('books:book_list')
    
    context = {
        'book': book,
        'page_title': f'Удаление книги "{book.title}"',
    }
    return render(request, 'books/book_delete.html', context)


# ==================== PUBLISHER CRUD ====================

def publisher_list(request):
    """
    Отображение списка всех издательств.
    
    Показывает количество книг для каждого издательства.
    """
    publishers = Publisher.objects.annotate(
        books_count=Count('books')
    ).order_by('name')
    
    # Поиск по названию или стране
    search_query = request.GET.get('search')
    if search_query:
        publishers = publishers.filter(
            Q(name__icontains=search_query) | Q(country__icontains=search_query)
        )
    
    context = {
        'publishers': publishers,
        'current_search': search_query,
        'page_title': 'Список издательств',
    }
    return render(request, 'books/publisher_list.html', context)


def publisher_detail(request, pk):
    """
    Отображение детальной информации об издательстве.
    
    Показывает:
    - Информацию об издательстве
    - Список всех книг издательства
    - Статистику (количество книг, средняя оценка)
    """
    publisher = get_object_or_404(
        Publisher.objects.prefetch_related('books__reviews'),
        pk=pk
    )
    
    books = publisher.books.all()
    
    # Статистика
    books_count = books.count()
    avg_rating = Review.objects.filter(book__publisher=publisher).aggregate(
        Avg('rating')
    )['rating__avg']
    
    context = {
        'publisher': publisher,
        'books': books,
        'books_count': books_count,
        'avg_rating': avg_rating,
        'page_title': f'{publisher.name} - Детали издательства',
    }
    return render(request, 'books/publisher_detail.html', context)


def publisher_create(request):
    """Создание нового издательства."""
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            messages.success(request, f'Издательство "{publisher.name}" успешно создано!')
            return redirect('books:publisher_detail', pk=publisher.pk)
    else:
        form = PublisherForm()
    
    context = {
        'form': form,
        'page_title': 'Создание нового издательства',
    }
    return render(request, 'books/publisher_create.html', context)


def publisher_update(request, pk):
    """Редактирование существующего издательства."""
    publisher = get_object_or_404(Publisher, pk=pk)
    
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            publisher = form.save()
            messages.success(request, f'Издательство "{publisher.name}" успешно обновлено!')
            return redirect('books:publisher_detail', pk=publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    
    context = {
        'form': form,
        'publisher': publisher,
        'page_title': f'Редактирование издательства "{publisher.name}"',
    }
    return render(request, 'books/publisher_update.html', context)


def publisher_delete(request, pk):
    """Удаление издательства с подтверждением."""
    publisher = get_object_or_404(Publisher, pk=pk)
    
    if request.method == 'POST':
        name = publisher.name
        publisher.delete()
        messages.success(request, f'Издательство "{name}" успешно удалено!')
        return redirect('books:publisher_list')
    
    context = {
        'publisher': publisher,
        'page_title': f'Удаление издательства "{publisher.name}"',
    }
    return render(request, 'books/publisher_delete.html', context)


# ==================== STORE CRUD ====================

def store_list(request):
    """
    Отображение списка всех магазинов.
    
    Показывает количество книг для каждого магазина.
    """
    stores = Store.objects.annotate(
        books_count=Count('books')
    ).order_by('city', 'name')
    
    # Фильтрация по городу
    city = request.GET.get('city')
    if city:
        stores = stores.filter(city__icontains=city)
    
    # Поиск по названию
    search_query = request.GET.get('search')
    if search_query:
        stores = stores.filter(name__icontains=search_query)
    
    context = {
        'stores': stores,
        'current_city': city,
        'current_search': search_query,
        'page_title': 'Список магазинов',
    }
    return render(request, 'books/store_list.html', context)


def store_detail(request, pk):
    """
    Отображение детальной информации о магазине.
    
    Показывает:
    - Информацию о магазине
    - Список всех книг в магазине
    - Статистику (количество книг)
    """
    store = get_object_or_404(
        Store.objects.prefetch_related('books'),
        pk=pk
    )
    
    books = store.books.all()
    books_count = books.count()
    
    context = {
        'store': store,
        'books': books,
        'books_count': books_count,
        'page_title': f'{store.name} - Детали магазина',
    }
    return render(request, 'books/store_detail.html', context)


def store_create(request):
    """Создание нового магазина."""
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save()
            messages.success(request, f'Магазин "{store.name}" успешно создан!')
            return redirect('books:store_detail', pk=store.pk)
    else:
        form = StoreForm()
    
    context = {
        'form': form,
        'page_title': 'Создание нового магазина',
    }
    return render(request, 'books/store_create.html', context)


def store_update(request, pk):
    """Редактирование существующего магазина."""
    store = get_object_or_404(Store, pk=pk)
    
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            store = form.save()
            messages.success(request, f'Магазин "{store.name}" успешно обновлен!')
            return redirect('books:store_detail', pk=store.pk)
    else:
        form = StoreForm(instance=store)
    
    context = {
        'form': form,
        'store': store,
        'page_title': f'Редактирование магазина "{store.name}"',
    }
    return render(request, 'books/store_update.html', context)


def store_delete(request, pk):
    """Удаление магазина с подтверждением."""
    store = get_object_or_404(Store, pk=pk)
    
    if request.method == 'POST':
        name = store.name
        store.delete()
        messages.success(request, f'Магазин "{name}" успешно удален!')
        return redirect('books:store_list')
    
    context = {
        'store': store,
        'page_title': f'Удаление магазина "{store.name}"',
    }
    return render(request, 'books/store_delete.html', context)


# ==================== REVIEW CRUD ====================

def review_list(request):
    """
    Отображение списка всех отзывов.
    
    Поддерживает фильтрацию по оценке и книге.
    """
    reviews = Review.objects.select_related('book').order_by('-created_at')
    
    # Фильтрация по оценке
    rating = request.GET.get('rating')
    if rating:
        try:
            reviews = reviews.filter(rating=int(rating))
        except ValueError:
            pass
    
    # Фильтрация по книге
    book_id = request.GET.get('book')
    if book_id:
        reviews = reviews.filter(book_id=book_id)
    
    # Пагинация
    paginator = Paginator(reviews, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Получаем все книги для фильтра
    books = Book.objects.all()
    
    context = {
        'reviews': page_obj,
        'books': books,
        'current_rating': rating,
        'current_book': book_id,
        'page_title': 'Список отзывов',
    }
    return render(request, 'books/review_list.html', context)


def review_detail(request, pk):
    """Отображение детальной информации об отзыве."""
    review = get_object_or_404(Review.objects.select_related('book'), pk=pk)
    
    context = {
        'review': review,
        'page_title': f'Отзыв на "{review.book.title}"',
    }
    return render(request, 'books/review_detail.html', context)


def review_create(request):
    """Создание нового отзыва."""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Отзыв успешно создан!')
            return redirect('books:review_detail', pk=review.pk)
    else:
        form = ReviewForm()
        # Если передан параметр book в GET запросе, устанавливаем его в форме
        book_id = request.GET.get('book')
        if book_id:
            try:
                book = Book.objects.get(pk=book_id)
                form.fields['book'].initial = book
            except Book.DoesNotExist:
                pass
    
    context = {
        'form': form,
        'page_title': 'Создание нового отзыва',
    }
    return render(request, 'books/review_create.html', context)


def review_update(request, pk):
    """Редактирование существующего отзыва."""
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Отзыв успешно обновлен!')
            return redirect('books:review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'page_title': 'Редактирование отзыва',
    }
    return render(request, 'books/review_update.html', context)


def review_delete(request, pk):
    """Удаление отзыва с подтверждением."""
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        book_title = review.book.title
        review.delete()
        messages.success(request, f'Отзыв на книгу "{book_title}" успешно удален!')
        return redirect('books:review_list')
    
    context = {
        'review': review,
        'page_title': 'Удаление отзыва',
    }
    return render(request, 'books/review_delete.html', context)


# ==================== ANALYTICS ====================

def analytics(request):
    """
    Страница аналитики с агрегатными данными.
    
    Показывает:
    - Общую статистику по книгам
    - Статистику по издательствам
    - Статистику по магазинам
    - Топ книги по рейтингу
    - Книги с наибольшим количеством отзывов
    """
    # Общая статистика по книгам
    total_books = Book.objects.count()
    total_reviews = Review.objects.count()
    avg_rating_all = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Статистика по издательствам
    publishers_stats = Publisher.objects.annotate(
        books_count=Count('books'),
        avg_rating=Avg('books__reviews__rating')
    ).order_by('-books_count')
    
    # Статистика по магазинам
    stores_stats = Store.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count')
    
    # Топ книги по рейтингу (минимум 3 отзыва)
    top_rated_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    ).filter(
        reviews_count__gte=3
    ).order_by('-avg_rating')[:10]
    
    # Книги с наибольшим количеством отзывов
    most_reviewed_books = Book.objects.annotate(
        reviews_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).filter(
        reviews_count__gt=0
    ).order_by('-reviews_count')[:10]
    
    # Статистика по годам публикации
    books_by_year = Book.objects.values('published_date__year').annotate(
        count=Count('id')
    ).order_by('-published_date__year')
    
    context = {
        'total_books': total_books,
        'total_reviews': total_reviews,
        'avg_rating_all': avg_rating_all,
        'publishers_stats': publishers_stats,
        'stores_stats': stores_stats,
        'top_rated_books': top_rated_books,
        'most_reviewed_books': most_reviewed_books,
        'books_by_year': books_by_year,
        'page_title': 'Аналитика книжного каталога',
    }
    return render(request, 'books/analytics.html', context)
