from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Product

# Create your views here.
class ProductView(View):
    template_name = 'products/products.html'
    def get(self, request):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})


class ProductDetailView(View):
    template_name = 'products/product_dtail.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['slug'])
        return render(request, self.template_name, {'product': product})


class AdminHomeView(View):
    template_name = 'products/bucket_home.html'

    def get(self, request):
        products = Product.objects.all()
        return render(request, self.template_name, {'objects': products})


class AdminProductDelete(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        if request.user.is_admin:
            product.delete()
            messages.success(request, 'Product deleted successfully', 'success')
        else:
            messages.error(request, 'you are not authorized to delete product', 'danger')
        return redirect('products:products')
