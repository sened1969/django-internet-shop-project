"""
Представления для интернет-магазина.

Этот модуль содержит представления для отображения списка товаров,
детальной информации о конкретном товаре, а также для работы с формами
регистрации, авторизации и отправки сообщений.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import Product, Message, Order, Cart, CartItem, Category
from .forms import (
    CustomUserCreationForm, EmailAuthenticationForm, ContactForm,
    ProfileEditForm, CustomPasswordChangeForm, CustomPasswordResetForm,
    CustomSetPasswordForm
)

User = get_user_model()


def product_list(request):
    """
    Представление для отображения списка товаров с фильтрацией, сортировкой и пагинацией.
    
    Поддерживает:
    - Фильтрацию по категории, цене и дате добавления
    - Сортировку по популярности, цене и дате
    - Пагинацию (10 товаров на странице)
    - AJAX-подгрузку данных без перезагрузки страницы
    
    Args:
        request: HTTP-запрос от пользователя
        
    Returns:
        HttpResponse: HTML-страница со списком товаров или JSON-ответ для AJAX
    """
    # Получаем параметры фильтрации из GET-запроса
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    date_filter = request.GET.get('date_filter', 'all')  # '7days', '30days', 'all'
    
    # Получаем параметр сортировки
    sort = request.GET.get('sort', '-created_at')  # По умолчанию новые сначала
    
    # Начинаем с аннотации для подсчёта популярности (количество заказов)
    products = Product.objects.select_related('category').annotate(
        order_count=Count('order_items')
    )
    
    # Применяем фильтры
    if category_id:
        try:
            products = products.filter(category_id=int(category_id))
        except (ValueError, TypeError):
            pass  # Игнорируем неверные значения
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Фильтрация по дате добавления
    if date_filter == '7days':
        seven_days_ago = timezone.now() - timedelta(days=7)
        products = products.filter(created_at__gte=seven_days_ago)
    elif date_filter == '30days':
        thirty_days_ago = timezone.now() - timedelta(days=30)
        products = products.filter(created_at__gte=thirty_days_ago)
    # Если 'all' или другое значение - не фильтруем по дате
    
    # Применяем сортировку
    if sort == 'popularity':
        products = products.order_by('-order_count', '-created_at')
    elif sort == 'price':
        products = products.order_by('price', '-created_at')
    elif sort == '-price':
        products = products.order_by('-price', '-created_at')
    elif sort == 'created_at':
        products = products.order_by('created_at')
    elif sort == '-created_at':
        products = products.order_by('-created_at')
    else:
        # По умолчанию сортируем по дате создания (новые сначала)
        products = products.order_by('-created_at')
    
    # Пагинация: 10 товаров на странице
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)
    
    # Получаем все категории для формы фильтрации
    categories = Category.objects.all()
    
    # Проверяем, это AJAX-запрос?
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Возвращаем JSON для AJAX
        products_data = []
        for product in page_obj:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'description': product.description[:100] + '...' if len(product.description) > 100 else product.description,
                'image_url': product.image.url if product.image else '',
                'category': product.category.name if product.category else 'Без категории',
                'created_at': product.created_at.strftime('%d.%m.%Y %H:%M'),
                'order_count': product.order_count,
                'url': f'/product/{product.id}/',
            })
        
        return JsonResponse({
            'success': True,
            'products': products_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
        })
    
    # Обычный HTTP-запрос - возвращаем HTML
    context = {
        'products': page_obj,
        'categories': categories,
        'page_title': 'Каталог товаров',
        'current_category': category_id,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_date_filter': date_filter,
        'current_sort': sort,
    }
    
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
    - POST: обрабатывает данные формы, создает пользователя и отправляет письмо для подтверждения email
    """
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Генерация токена для подтверждения email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirmation_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')
            
            # Отправка email с подтверждением
            try:
                send_mail(
                    'Подтверждение регистрации',
                    f'Здравствуйте!\n\n'
                    f'Спасибо за регистрацию в нашем интернет-магазине.\n\n'
                    f'Для активации вашего аккаунта перейдите по следующей ссылке:\n'
                    f'{confirmation_link}\n\n'
                    f'Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.\n\n'
                    f'С уважением,\n'
                    f'Команда интернет-магазина',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    'Регистрация прошла успешно! Пожалуйста, проверьте вашу почту '
                    'и перейдите по ссылке для активации аккаунта.'
                )
            except Exception as e:
                messages.error(
                    request,
                    f'Ошибка при отправке письма: {str(e)}. '
                    'Пожалуйста, свяжитесь с администратором.'
                )
            
            return redirect('shop:email_confirmation_sent')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
        'page_title': 'Регистрация',
    }
    return render(request, 'shop/register.html', context)


def email_confirmation_sent(request):
    """
    Страница с информацией об отправке письма для подтверждения email.
    """
    context = {
        'page_title': 'Подтверждение email отправлено',
    }
    return render(request, 'shop/email_confirmation_sent.html', context)


def activate(request, uidb64, token):
    """
    Активация аккаунта пользователя по токену из email.
    
    Args:
        uidb64: Закодированный ID пользователя
        token: Токен для подтверждения
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт успешно активирован! Теперь вы можете войти.')
        return redirect('shop:login')
    else:
        messages.error(request, 'Ссылка активации недействительна или истек срок её действия.')
        return render(request, 'shop/activation_invalid.html', {
            'page_title': 'Ошибка активации'
        })


def login_view(request):
    """
    Представление для авторизации пользователя по email.
    
    Обрабатывает GET и POST запросы:
    - GET: отображает форму авторизации
    - POST: проверяет учетные данные и авторизует пользователя
    Также переносит корзину из сессии в корзину пользователя при входе.
    """
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # В форме это поле называется username, но содержит email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Переносим корзину из сессии в корзину пользователя перед входом
                merge_session_cart_to_user_cart(request, user)
                
                login(request, user)
                messages.success(request, f'Добро пожаловать, {email}!')
                return redirect('shop:home')
            else:
                messages.error(request, 'Неверный email или пароль.')
        else:
            # Ошибки валидации уже обработаны в форме
            pass
    else:
        form = EmailAuthenticationForm()
    
    context = {
        'form': form,
        'page_title': 'Авторизация',
    }
    return render(request, 'shop/login.html', context)


def merge_session_cart_to_user_cart(request, user):
    """
    Переносит товары из сессионной корзины в корзину пользователя.
    
    Args:
        request: HTTP-запрос
        user: Пользователь, в корзину которого переносятся товары
    """
    if 'cart' in request.session and request.session['cart']:
        # Получаем или создаем корзину пользователя
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Переносим товары из сессии
        session_cart = request.session['cart']
        for item_data in session_cart:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity', 1)
            
            try:
                product = Product.objects.get(id=product_id)
                # Проверяем, есть ли уже такой товар в корзине
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': quantity}
                )
                if not created:
                    # Если товар уже есть, увеличиваем количество
                    cart_item.quantity += quantity
                    cart_item.save()
            except Product.DoesNotExist:
                continue
        
        # Очищаем сессионную корзину
        del request.session['cart']
        request.session.modified = True


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
    
    Отображает данные пользователя, историю заказов и список отправленных сообщений.
    """
    user_messages = Message.objects.filter(user=request.user).order_by('-created_at')[:10]
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    context = {
        'page_title': 'Профиль пользователя',
        'user': request.user,
        'user_messages': user_messages,
        'orders': orders,
    }
    return render(request, 'shop/profile.html', context)


@login_required
def profile_edit(request):
    """
    Редактирование профиля пользователя.
    """
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('shop:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    context = {
        'form': form,
        'page_title': 'Редактирование профиля',
    }
    return render(request, 'shop/profile_edit.html', context)


@login_required
def password_change(request):
    """
    Изменение пароля пользователя.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('shop:profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Изменение пароля',
    }
    return render(request, 'shop/password_change.html', context)


def password_reset(request):
    """
    Сброс пароля - отправка письма с ссылкой для восстановления.
    """
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Генерация токена для сброса пароля
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/password-reset-confirm/{uid}/{token}/')
                
                send_mail(
                    'Сброс пароля',
                    f'Здравствуйте!\n\n'
                    f'Вы запросили сброс пароля для вашего аккаунта.\n\n'
                    f'Для установки нового пароля перейдите по следующей ссылке:\n'
                    f'{reset_link}\n\n'
                    f'Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.\n\n'
                    f'С уважением,\n'
                    f'Команда интернет-магазина',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    'Письмо с инструкциями по сбросу пароля отправлено на ваш email.'
                )
            except User.DoesNotExist:
                # Не сообщаем, что пользователь не найден (безопасность)
                messages.success(
                    request,
                    'Если пользователь с таким email существует, '
                    'письмо с инструкциями отправлено.'
                )
            except Exception as e:
                messages.error(
                    request,
                    f'Ошибка при отправке письма: {str(e)}. '
                    'Пожалуйста, свяжитесь с администратором.'
                )
            return redirect('shop:password_reset_done')
    else:
        form = CustomPasswordResetForm()
    
    context = {
        'form': form,
        'page_title': 'Сброс пароля',
    }
    return render(request, 'shop/password_reset.html', context)


def password_reset_done(request):
    """
    Страница подтверждения отправки письма для сброса пароля.
    """
    context = {
        'page_title': 'Письмо отправлено',
    }
    return render(request, 'shop/password_reset_done.html', context)


def password_reset_confirm(request, uidb64, token):
    """
    Подтверждение сброса пароля и установка нового пароля.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пароль успешно изменен! Теперь вы можете войти.')
                return redirect('shop:login')
        else:
            form = CustomSetPasswordForm(user=user)
        
        context = {
            'form': form,
            'page_title': 'Установка нового пароля',
        }
        return render(request, 'shop/password_reset_confirm.html', context)
    else:
        messages.error(request, 'Ссылка для сброса пароля недействительна или истек срок её действия.')
        return render(request, 'shop/password_reset_invalid.html', {
            'page_title': 'Ошибка сброса пароля'
        })


@login_required
def account_delete_request(request):
    """
    Запрос на удаление аккаунта - отправка письма с подтверждением.
    """
    if request.method == 'POST':
        # Генерация токена для подтверждения удаления
        token = default_token_generator.make_token(request.user)
        uid = urlsafe_base64_encode(force_bytes(request.user.pk))
        delete_link = request.build_absolute_uri(f'/account-delete-confirm/{uid}/{token}/')
        
        try:
            send_mail(
                'Подтверждение удаления аккаунта',
                f'Здравствуйте!\n\n'
                f'Вы запросили удаление вашего аккаунта.\n\n'
                f'Для подтверждения удаления перейдите по следующей ссылке:\n'
                f'{delete_link}\n\n'
                f'ВНИМАНИЕ: Это действие необратимо! Все ваши данные будут удалены.\n\n'
                f'Если вы не запрашивали удаление аккаунта, просто проигнорируйте это письмо.\n\n'
                f'С уважением,\n'
                f'Команда интернет-магазина',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            messages.success(
                request,
                'Письмо с подтверждением удаления аккаунта отправлено на ваш email.'
            )
        except Exception as e:
            messages.error(
                request,
                f'Ошибка при отправке письма: {str(e)}. '
                'Пожалуйста, свяжитесь с администратором.'
            )
        
        return redirect('shop:profile')
    
    context = {
        'page_title': 'Удаление аккаунта',
    }
    return render(request, 'shop/account_delete_request.html', context)


def account_delete_confirm(request, uidb64, token):
    """
    Подтверждение и выполнение удаления аккаунта.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Удаляем пользователя (каскадное удаление удалит связанные данные)
            user_email = user.email
            user.delete()
            messages.success(request, f'Аккаунт {user_email} успешно удален.')
            return redirect('shop:product_list')
        
        context = {
            'page_title': 'Подтверждение удаления аккаунта',
            'user': user,
        }
        return render(request, 'shop/account_delete_confirm.html', context)
    else:
        messages.error(request, 'Ссылка для удаления аккаунта недействительна или истек срок её действия.')
        return render(request, 'shop/account_delete_invalid.html', {
            'page_title': 'Ошибка удаления аккаунта'
        })


def logout_view(request):
    """
    Представление для выхода из системы.
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('shop:product_list')


def add_to_cart(request, product_id):
    """
    Добавление товара в корзину.
    
    Для авторизованных пользователей - добавляет в корзину пользователя.
    Для анонимных пользователей - сохраняет в сессии.
    """
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if request.user.is_authenticated:
        # Для авторизованных пользователей
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        messages.success(request, f'{product.name} добавлен в корзину.')
    else:
        # Для анонимных пользователей - сохраняем в сессии
        if 'cart' not in request.session:
            request.session['cart'] = []
        
        # Проверяем, есть ли уже такой товар в сессионной корзине
        cart = request.session['cart']
        found = False
        for item in cart:
            if item.get('product_id') == product_id:
                item['quantity'] = item.get('quantity', 1) + quantity
                found = True
                break
        
        if not found:
            cart.append({
                'product_id': product_id,
                'quantity': quantity
            })
        
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product.name} добавлен в корзину.')
    
    return redirect('shop:product_detail', product_id=product_id)


def view_cart(request):
    """
    Просмотр корзины покупок.
    """
    cart_items = []
    total = 0
    
    if request.user.is_authenticated:
        # Для авторизованных пользователей
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                total += item.product.price * item.quantity
        except Cart.DoesNotExist:
            pass
    else:
        # Для анонимных пользователей - читаем из сессии
        if 'cart' in request.session:
            session_cart = request.session['cart']
            for item_data in session_cart:
                try:
                    product = Product.objects.get(id=item_data['product_id'])
                    quantity = item_data.get('quantity', 1)
                    cart_items.append({
                        'product': product,
                        'quantity': quantity
                    })
                    total += product.price * quantity
                except Product.DoesNotExist:
                    continue
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'page_title': 'Корзина покупок',
    }
    return render(request, 'shop/cart.html', context)

