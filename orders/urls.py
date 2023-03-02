from django.urls import path, include
from . import views

app_name = 'orders'
order_url = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<str:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('pay/<str:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('address/<str:order_id>/', views.ShippingAddressView.as_view(), name='order_address'),
    path('apply/<str:order_id>/', views.CouponApplyView.as_view(), name='apply_coupon'),
]

urlpatterns = [
    path('', include(order_url)),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/<str:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<str:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
]
