from django.contrib import admin
from .models import *
from .models import ProductReview

# class CatagoryAdmin(admin.ModelAdmin):
#     list_display = ('name','image','description')
admin.site.register(Catagory)
admin.site.register(Products)
admin.site.register(ProductReview)

# Register your models here.
