from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Category
from utils import IsAdminUserMixing


# Create your views here.
class ProductView(View):
    template_name = 'products/products.html'

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, self.template_name, context)


class ProductDetailView(View):
    template_name = 'products/product_dtail.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['slug'])
        return render(request, self.template_name, {'product': product})


class AdminHomeView(IsAdminUserMixing, View):
    template_name = 'products/bucket_home.html'

    def get(self, request):
        products = Product.objects.all()
        return render(request, self.template_name, {'objects': products})


class AdminProductDelete(IsAdminUserMixing, View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        product.delete()
        messages.success(request, 'Product deleted successfully', 'success')
        
        return redirect('products:bucket')
