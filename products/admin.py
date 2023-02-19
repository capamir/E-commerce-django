from django.contrib import admin
from .models import Product, Category, Review
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('sub_category',)

class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ['category',]

class ReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ['product', 'user']
    list_display = ('product', 'user', 'rating')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)