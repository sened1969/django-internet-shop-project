"""
Формы для работы с книгами, издательствами, магазинами и отзывами.

Содержит формы для создания и редактирования всех моделей приложения books.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Publisher, Store, Review


class PublisherForm(forms.ModelForm):
    """
    Форма для создания и редактирования издательства.
    
    Поля:
        name: Название издательства
        country: Страна издательства
    """
    class Meta:
        model = Publisher
        fields = ['name', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название издательства',
                'required': True
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите страну',
                'required': True
            }),
        }
        labels = {
            'name': 'Название издательства',
            'country': 'Страна',
        }
        help_texts = {
            'name': 'Введите название издательства',
            'country': 'Введите страну, где находится издательство',
        }
    
    def clean_name(self):
        """Валидация названия издательства."""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise ValidationError('Название издательства должно содержать минимум 2 символа.')
        return name.strip()


class StoreForm(forms.ModelForm):
    """
    Форма для создания и редактирования магазина.
    
    Поля:
        name: Название магазина
        city: Город, где находится магазин
    """
    class Meta:
        model = Store
        fields = ['name', 'city']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название магазина',
                'required': True
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите город',
                'required': True
            }),
        }
        labels = {
            'name': 'Название магазина',
            'city': 'Город',
        }
        help_texts = {
            'name': 'Введите название книжного магазина',
            'city': 'Введите город, где находится магазин',
        }
    
    def clean_name(self):
        """Валидация названия магазина."""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise ValidationError('Название магазина должно содержать минимум 2 символа.')
        return name.strip()


class BookForm(forms.ModelForm):
    """
    Форма для создания и редактирования книги.
    
    Поля:
        title: Название книги
        author: Автор книги
        published_date: Дата публикации
        description: Описание книги
        publisher: Издательство (ForeignKey)
        stores: Магазины (ManyToMany)
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'description', 'publisher', 'stores']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название книги',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя автора',
                'required': True
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание книги',
                'rows': 5,
                'required': True
            }),
            'publisher': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'stores': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 5
            }),
        }
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'published_date': 'Дата публикации',
            'description': 'Описание',
            'publisher': 'Издательство',
            'stores': 'Магазины',
        }
        help_texts = {
            'title': 'Введите название книги',
            'author': 'Введите имя автора книги',
            'published_date': 'Выберите дату публикации книги',
            'description': 'Введите описание книги',
            'publisher': 'Выберите издательство',
            'stores': 'Выберите магазины, где продаётся книга (можно выбрать несколько, удерживая Ctrl)',
        }
    
    def clean_title(self):
        """Валидация названия книги."""
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 2:
            raise ValidationError('Название книги должно содержать минимум 2 символа.')
        return title.strip()
    
    def clean_author(self):
        """Валидация имени автора."""
        author = self.cleaned_data.get('author')
        if author and len(author.strip()) < 2:
            raise ValidationError('Имя автора должно содержать минимум 2 символа.')
        return author.strip()


class ReviewForm(forms.ModelForm):
    """
    Форма для создания и редактирования отзыва на книгу.
    
    Поля:
        book: Книга (ForeignKey)
        rating: Оценка (от 1 до 5)
        text: Текст отзыва
    """
    class Meta:
        model = Review
        fields = ['book', 'rating', 'text']
        widgets = {
            'book': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'required': True
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст отзыва',
                'rows': 5,
                'required': True
            }),
        }
        labels = {
            'book': 'Книга',
            'rating': 'Оценка',
            'text': 'Текст отзыва',
        }
        help_texts = {
            'book': 'Выберите книгу, на которую оставляете отзыв',
            'rating': 'Оценка книги от 1 до 5',
            'text': 'Введите текст отзыва о книге',
        }
    
    def clean_rating(self):
        """Валидация оценки."""
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise ValidationError('Оценка должна быть от 1 до 5.')
        return rating
    
    def clean_text(self):
        """Валидация текста отзыва."""
        text = self.cleaned_data.get('text')
        if text and len(text.strip()) < 10:
            raise ValidationError('Текст отзыва должен содержать минимум 10 символов.')
        return text.strip()

