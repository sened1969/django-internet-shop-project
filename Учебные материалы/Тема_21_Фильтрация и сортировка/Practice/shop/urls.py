from django.urls import path
from . import views

urlpatterns = [
    path('', views.recent_orders_view),
    path('recent-orders/', views.recent_orders_view, name='recent_orders'),
    path('product-filter/', views.product_filter_view, name='product_filter'),
    path('popular-products/', views.popular_products_view, name='popular_products'),
    path('combined-filter/', views.combined_filter_view, name='combined_filter'),
]