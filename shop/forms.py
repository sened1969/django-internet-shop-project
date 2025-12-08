"""
Формы для интернет-магазина.

Содержит формы для регистрации, авторизации и отправки сообщений.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Message, Product

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    """
    Форма регистрации нового пользователя с кастомной моделью.
    
    Поля:
        email: Электронная почта (используется для входа)
        phone_number: Номер телефона
        address: Адрес доставки
        password1: Пароль
        password2: Подтверждение пароля
    """
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email',
            'required': True
        }),
        help_text='Введите действующий email адрес. Он будет использоваться для входа.'
    )
    
    phone_number = forms.CharField(
        max_length=15,
        label='Номер телефона',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите номер телефона (необязательно)'
        }),
        help_text='Номер телефона (необязательно)'
    )
    
    address = forms.CharField(
        max_length=255,
        label='Адрес доставки',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес доставки (необязательно)'
        }),
        help_text='Адрес доставки (необязательно)'
    )
    
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'required': True
        }),
        help_text='Пароль должен содержать минимум 8 символов.'
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'required': True
        }),
        help_text='Введите пароль еще раз для подтверждения.'
    )
    
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'address']
    
    def clean_email(self):
        """Проверка уникальности email."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email
    
    def clean_password2(self):
        """Проверка совпадения паролей."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        
        if password1 and len(password1) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
        
        return password2
    
    def save(self, commit=True):
        """Сохранение пользователя с хешированием пароля."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  # Аккаунт не активен до подтверждения email
        if commit:
            user.save()
        return user


# Для обратной совместимости
RegistrationForm = CustomUserCreationForm


class EmailAuthenticationForm(AuthenticationForm):
    """
    Форма авторизации пользователя по email.
    
    Наследуется от AuthenticationForm Django, но использует email вместо username.
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    
    def clean(self):
        """Проверка учетных данных и активности аккаунта."""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            # Используем email для поиска пользователя
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                raise ValidationError('Неверный email или пароль.')
            
            # Проверяем, активен ли аккаунт
            if not user.is_active:
                raise ValidationError(
                    'Ваш аккаунт не активирован. Пожалуйста, проверьте вашу почту '
                    'и перейдите по ссылке для активации.'
                )
            
            # Проверяем пароль
            if not user.check_password(password):
                raise ValidationError('Неверный email или пароль.')
        
        return self.cleaned_data


# Для обратной совместимости
LoginForm = EmailAuthenticationForm


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""
    
    class Meta:
        model = User
        fields = ['phone_number', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес доставки'
            }),
        }
        labels = {
            'phone_number': 'Номер телефона',
            'address': 'Адрес доставки',
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Форма изменения пароля с кастомными виджетами."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите текущий пароль'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        })


class CustomPasswordResetForm(PasswordResetForm):
    """Форма сброса пароля с кастомными виджетами."""
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    """Форма установки нового пароля с кастомными виджетами."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        })


class ContactForm(forms.ModelForm):
    """
    Форма отправки сообщения.
    
    Поля:
        name: Имя отправителя
        email: Электронная почта
        message: Текст сообщения
    """
    name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя',
            'required': True
        }),
        help_text='Введите ваше имя'
    )
    
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
            'required': True
        }),
        help_text='Введите ваш email адрес'
    )
    
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше сообщение (максимум 500 символов)',
            'rows': 5,
            'required': True
        }),
        help_text='Текст сообщения (максимум 500 символов)'
    )
    
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']
    
    def clean_message(self):
        """Валидация текста сообщения."""
        message = self.cleaned_data.get('message')
        
        if not message or not message.strip():
            raise ValidationError('Сообщение не может быть пустым.')
        
        if len(message) > 500:
            raise ValidationError('Сообщение не должно превышать 500 символов.')
        
        return message.strip()


class ProductForm(forms.ModelForm):
    """
    Форма для добавления нового товара.
    
    Поля:
        name: Название товара
        description: Описание товара
        price: Цена товара
        image: Изображение товара
        category: Категория товара
        stock: Количество на складе
    """
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите описание товара',
                'required': True
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00',
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0',
                'required': True
            }),
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание товара',
            'price': 'Цена товара',
            'image': 'Изображение товара',
            'category': 'Категория товара',
            'stock': 'Количество на складе',
        }
        help_texts = {
            'name': 'Введите название товара',
            'description': 'Введите подробное описание товара',
            'price': 'Цена товара в рублях',
            'image': 'Загрузите изображение товара (необязательно)',
            'category': 'Выберите категорию товара (необязательно)',
            'stock': 'Количество товара на складе',
        }

