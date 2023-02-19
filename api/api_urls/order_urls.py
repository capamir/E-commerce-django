from django.urls import path
from api.views import order_views as views


urlpatterns = [
    path('add/', views.add_order_items, name='add-order'),
    path('myorders/', views.get_my_orders, name='my-order'),

    path('<int:order_id>/', views.get_order_by_id, name='user-order'),
    path('<int:order_id>/pay/', views.update_order_to_paid, name='pay-order'),

    # Admin
    path('', views.get_orders, name='admin-orders'),

]