from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from .models import User, Order, Product, OrderItem


def recent_orders_view(request):
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    
    # Аннотируем количество заказов за последние 30 дней для каждого пользователя
    users_with_recent_orders = User.objects.annotate(
        recent_order_count=Count('order', filter=Q(order__created_at__gte=thirty_days_ago))
    ).filter(recent_order_count__gt=0)

    return render(request, 'shop/recent_orders.html', {'users': users_with_recent_orders})


def product_filter_view(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    return render(request, 'shop/product_list.html', {'products': products})


def popular_products_view(request):
    products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')  # сортировка по количеству заказов в убывающем порядке

    return render(request, 'shop/popular_products.html', {'products': products})

def combined_filter_view(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', '-order_count')
    
    products = Product.objects.annotate(
        order_count=Count('orderitem')
    )
    
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    products = products.order_by(sort)
    
    return render(request, 'shop/combined_filter.html', {'products': products})