from django.shortcuts import render, get_object_or_404
from .models import *

def home(request):
    return render(request, "index.html")

def register(request):
    return render(request, "register.html")

def collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request, "collections.html", {"catagory": catagory})
def collection_products(request, cid):
    catagory = get_object_or_404(Catagory, id=cid, status=0)
    products = Products.objects.filter(catagory=catagory, status=0)

    context = {
        "catagory": catagory,
        "products": products
    }
    return render(request, "products_by_catagory.html", context)
def product_detail(request, pid):
    product = get_object_or_404(Products, id=pid, status=0)
    return render(request, "product_detail.html", {"product": product})
