from django.urls import path, include
from .api_urls import product_urls, user_urls, order_urls

urlpatterns = [
    path('users/', include(user_urls)),
    path('products/', include(product_urls)),
    path('orders/', include(order_urls)),
]
