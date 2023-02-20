from django.urls import path
from api.views import product_views as views

urlpatterns = [
    path('', views.get_products, name='get-products'),
    path('<int:product_id>/', views.get_product_details, name='get-product-details'),
    path('<int:product_id>/reviews/', views.create_product_review, name='create-product-review'),
    
    # Admin
    path('create/', views.create_product, name='admin-create-product'),
    path('update/<int:product_id>/', views.update_product, name='admin-update-product'),
    path('delete/<int:product_id>/', views.delete_product, name='admin-delete-product'),

    path('upload/', views.upload_product_image, name='admin-upload-product-image'),
]
