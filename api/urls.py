from django.urls import path, include
from . import main_views
from .api_urls import product_urls, user_urls

urlpatterns = [
    path('users/', include(user_urls)),
    path('products/', include(product_urls)),
]
