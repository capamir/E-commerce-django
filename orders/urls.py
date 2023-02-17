from django.urls import path, include
from . import views

app_name = 'orders'
order_url = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]

urlpatterns = [
    path('orders/', include(order_url)),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
]
