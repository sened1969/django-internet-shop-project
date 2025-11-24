"""
Представления для интернет-магазина.

Этот модуль содержит представления для отображения списка товаров
и детальной информации о конкретном товаре.
"""
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Product


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

