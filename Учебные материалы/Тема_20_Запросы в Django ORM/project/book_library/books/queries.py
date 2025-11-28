from .models import Author, Book
from django.db.models import Count, Sum

def run_queries():
    # Получение всех книг
    books = Book.objects.all()
    for book in books:
        print(f"Book: {book.title}, Author: {book.author.name}")

    # Получение всех книг, опубликованных после 2020 года
    recent_books = Book.objects.filter(published_date__year__gt=2020)
    print("Books published after 2020:")
    for book in recent_books:
        print(book.title)

    # Подсчет общего количества книг
    total_books = Book.objects.count()
    print(f"Total number of books: {total_books}")

    # Получение всех авторов с количеством книг
    authors = Author.objects.annotate(book_count=Count('books'))
    for author in authors:
        print(f"Author: {author.name}, Number of Books: {author.book_count}")

    # Использование select_related для оптимизации
    books_with_authors = Book.objects.select_related('author').all()
    for book in books_with_authors:
        print(f"{book.title} by {book.author.name}")

if __name__ == "__main__":
    run_queries()
