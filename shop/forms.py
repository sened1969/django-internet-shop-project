"""
Формы для интернет-магазина.

Содержит формы для регистрации, авторизации и отправки сообщений.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Message


class RegistrationForm(forms.ModelForm):
    """
    Форма регистрации нового пользователя.
    
    Поля:
        username: Имя пользователя
        email: Электронная почта
        password1: Пароль
        password2: Подтверждение пароля
    """
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
            'required': True
        }),
        help_text='Обязательное поле. Не более 150 символов.'
    )
    
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email',
            'required': True
        }),
        help_text='Введите действующий email адрес.'
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
        fields = ['username', 'email']
    
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
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Форма авторизации пользователя.
    
    Наследуется от AuthenticationForm Django.
    """
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
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

