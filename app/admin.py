from django.contrib import admin
from .models import Catagory, Products, ProductReview, ProductImage

admin.site.register(Catagory)
admin.site.register(ProductReview)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

# Register your models here.
