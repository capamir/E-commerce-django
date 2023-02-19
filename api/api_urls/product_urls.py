from django.urls import path
from api.views import product_views as views

urlpatterns = [
    path('', views.get_products, name='get-products'),
    path('<int:product_id>/', views.get_product_details, name='get-product-details'),

]
