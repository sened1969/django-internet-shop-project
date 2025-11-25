"""
Представления для интернет-магазина.

Этот модуль содержит представления для отображения списка товаров,
детальной информации о конкретном товаре, а также для работы с формами
регистрации, авторизации и отправки сообщений.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Product, Message
from .forms import RegistrationForm, LoginForm, ContactForm


def product_list(request):
    """
    Представление для отображения списка всех товаров.
    
    Получает все товары из базы данных и передает их в шаблон
    для отображения на странице списка товаров.
    
    Args:
        request: HTTP-запрос от пользователя
        
    Returns:
        HttpResponse: HTML-страница со списком товаров
    """
    # Получаем все товары из базы данных
    products = Product.objects.all()
    
    # Формируем контекст для передачи в шаблон
    context = {
        'products': products,
        'page_title': 'Каталог товаров',
    }
    
    # Рендерим шаблон с контекстом
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_id):
    """
    Представление для отображения детальной информации о товаре.
    
    Получает товар по его ID и передает в шаблон для отображения
    детальной информации. Если товар не найден, возвращает 404.
    
    Args:
        request: HTTP-запрос от пользователя
        product_id (int): ID товара для отображения
        
    Returns:
        HttpResponse: HTML-страница с детальной информацией о товаре
        Http404: Если товар не найден
    """
    try:
        # Получаем товар по ID или возвращаем 404, если не найден
        product = get_object_or_404(Product, id=product_id)
        
        # Формируем контекст для передачи в шаблон
        context = {
            'product': product,
            'page_title': f'{product.name} - Детали товара',
        }
        
        # Рендерим шаблон с контекстом
        return render(request, 'shop/product_detail.html', context)
    
    except Http404:
        # Если товар не найден, передаем информацию об ошибке в шаблон
        context = {
            'error_message': 'Товар не найден',
            'product_id': product_id,
        }
        return render(request, 'shop/product_detail.html', context, status=404)


def register(request):
    """
    Представление для регистрации нового пользователя.
    
    Обрабатывает GET и POST запросы:
    - GET: отображает форму регистрации
    - POST: обрабатывает данные формы и создает нового пользователя
    """
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('shop:registration_success')
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Регистрация',
    }
    return render(request, 'shop/register.html', context)


def registration_success(request):
    """
    Страница успешной регистрации.
    """
    context = {
        'page_title': 'Регистрация успешна',
    }
    return render(request, 'shop/registration_success.html', context)


def login_view(request):
    """
    Представление для авторизации пользователя.
    
    Обрабатывает GET и POST запросы:
    - GET: отображает форму авторизации
    - POST: проверяет учетные данные и авторизует пользователя
    """
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('shop:home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'page_title': 'Авторизация',
    }
    return render(request, 'shop/login.html', context)


@login_required
def home(request):
    """
    Главная страница для авторизованных пользователей.
    """
    context = {
        'page_title': 'Главная страница',
        'user': request.user,
    }
    return render(request, 'shop/home.html', context)


def contact(request):
    """
    Представление для отправки сообщения.
    
    Обрабатывает GET и POST запросы:
    - GET: отображает форму отправки сообщения
    - POST: обрабатывает данные формы и сохраняет сообщение
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            # Если пользователь авторизован, связываем сообщение с ним
            if request.user.is_authenticated:
                message.user = request.user
            message.save()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('shop:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Связаться с нами',
    }
    return render(request, 'shop/contact.html', context)


@require_http_methods(["POST"])
def contact_ajax(request):
    """
    Ajax-обработчик для отправки сообщения без перезагрузки страницы.
    
    Возвращает JSON-ответ с результатом обработки формы.
    """
    form = ContactForm(request.POST)
    
    if form.is_valid():
        message = form.save(commit=False)
        # Если пользователь авторизован, связываем сообщение с ним
        if request.user.is_authenticated:
            message.user = request.user
        message.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Ваше сообщение успешно отправлено!'
        })
    else:
        # Формируем список ошибок валидации
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list
        
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)


@login_required
def profile(request):
    """
    Страница профиля пользователя.
    
    Отображает данные пользователя и список отправленных им сообщений.
    """
    user_messages = Message.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'page_title': 'Профиль пользователя',
        'user': request.user,
        'user_messages': user_messages,
    }
    return render(request, 'shop/profile.html', context)


def logout_view(request):
    """
    Представление для выхода из системы.
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('shop:product_list')

