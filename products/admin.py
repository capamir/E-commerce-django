from django.contrib import admin
from .models import Product, Category
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ['category',]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
