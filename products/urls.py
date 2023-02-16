from django.urls import path, include
from . import views

app_name = 'products'

bucket_url = [
    path('', views.AdminHomeView.as_view(), name='bucket'),
    path('delete/<int:product_id>/', views.AdminProductDelete.as_view(), name='delete-product-admin'),
]

urlpatterns = [
    path('', views.ProductView.as_view(), name='products'),
    path('bucket/', include(bucket_url)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    
]
