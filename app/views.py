from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
    wishlist = request.session.get('wishlist', [])

    context = {
        "catagory": catagory,
        "products": products,
        "wishlist": wishlist
    }
    return render(request, "products_by_catagory.html", context)
# views.py
def product_detail(request, pid):
    product = get_object_or_404(Products, id=pid)
    reviews = ProductReview.objects.filter(product=product)
    form = None
    can_review = False

    if request.user.is_authenticated:
        # Check if this user bought this product
        has_bought = OrderItem.objects.filter(
            order__user=request.user,
            order__is_completed=True,
            product=product
        ).exists()

        if has_bought:
            can_review = True
            form = ReviewForm()

            if request.method == "POST":
                form = ReviewForm(request.POST, request.FILES)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.product = product
                    review.save()
                    return redirect('product_detail', pid=product.id)

    context = {
        "product": product,
        "form": form,
        "reviews": reviews,
        "can_review": can_review,
    }
    return render(request, "product_detail.html", context)


def add_to_cart(request, pid):
    product = get_object_or_404(Products, id=pid)

    cart = request.session.get('cart', {})

    if str(pid) in cart:
        cart[str(pid)] += 1
    else:
        cart[str(pid)] = 1

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Products, id=pid)
        subtotal = product.selling_price * qty
        items.append({
            "product": product,
            "qty": qty,
            "subtotal": subtotal
        })
        total += subtotal

    context = {
        "items": items,
        "total": total
    }
    return render(request, "add_to_cart.html", context)

def remove_from_cart(request, pid):
    cart = request.session.get('cart', {})
    
    if str(pid) in cart:
        del cart[str(pid)]
        request.session['cart'] = cart

    return redirect('view_cart')
def add_to_wishlist(request, pid):
    wishlist = request.session.get('wishlist', [])
    if pid not in wishlist:
        wishlist.append(pid)
        request.session['wishlist'] = wishlist
    return redirect('view_wishlist')


def view_wishlist(request):
    wishlist = request.session.get('wishlist', [])
    products = Products.objects.filter(id__in=wishlist)
    return render(request, "wishlist.html", {"products": products})
def toggle_wishlist(request, pid):
    wishlist = request.session.get('wishlist', [])
    action = ''

    if pid in wishlist:
        wishlist.remove(pid)
        action = 'removed'
    else:
        wishlist.append(pid)
        action = 'added'

    request.session['wishlist'] = wishlist
    return JsonResponse({'status': 'ok', 'action': action})