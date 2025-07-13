from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import CheckoutForm
from .models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.db.models import Avg
from django.db.models import Q
from django.http import JsonResponse
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

    # Sort filter
    sort_by = request.GET.get('sort')
    if sort_by == 'low_to_high':
        products = products.order_by('selling_price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-selling_price')

    # Price range filter
    price_filter = request.GET.get('price')
    if price_filter == 'below_100':
        products = products.filter(selling_price__lt=100)
    elif price_filter == '100_500':
        products = products.filter(selling_price__gte=100, selling_price__lte=500)
    elif price_filter == 'above_1000':
        products = products.filter(selling_price__gt=1000)

    wishlist = request.session.get('wishlist', [])

    context = {
        "catagory": catagory,
        "products": products,
        "wishlist": wishlist,
        "sort_by": sort_by,
        "price_filter": price_filter,
    }
    return render(request, "products_by_catagory.html", context)
# views.py
from django.db.models import Avg

def product_detail(request, pid):
    product = get_object_or_404(Products, id=pid)
    reviews = ProductReview.objects.filter(product=product)
    images = product.images.all()  # ← Add this line

    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    avg_rating = round(avg_rating, 1)

    form = None
    can_review = False

    if request.user.is_authenticated:
        has_bought = OrderItem.objects.filter(
            order__user=request.user,
            order__is_completed=True,
            product=product
        ).exists()

        if has_bought:
            can_review = True
            form = ProductReview()

            if request.method == "POST":
                form = ProductReview(request.POST)
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
        "avg_rating": avg_rating,
        "images": images,  # ← Add this to pass to template
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


def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')  # If cart is empty, go back

    items = []
    total_price = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Products, id=pid)
        subtotal = product.selling_price * qty
        items.append({
            "product": product,
            "qty": qty,
            "subtotal": subtotal
        })
        total_price += subtotal

    form = CheckoutForm()
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total_price=total_price,
                payment_method="COD",
                is_completed=True
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["qty"],
                    price=item["product"].selling_price
                )

            request.session['cart'] = {}  # Clear cart after order
            return redirect('order_success')

    return render(request, "checkout.html", {
        "form": form,
        "cart_items": items,
        "total": total_price
    })
def order_success(request):
    return render(request, "order_success.html")
#@staff_member_required
def delivery_dashboard(request):
    orders = Order.objects.filter(is_completed=True, delivered=False)
    return render(request, "delivery_dashboard.html", {"orders": orders})

#@staff_member_required
def mark_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delivered = True
    order.save()
    return redirect('delivery_dashboard')

#@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, delivered=True)
    return render(request, "my_orders.html", {"orders": orders})

def search_products(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        category_matches = Catagory.objects.filter(name__icontains=query)
        product_matches = Products.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(vendor__icontains=query)
        )

        if category_matches.exists():
            results = Products.objects.filter(catagory__in=category_matches)
        elif product_matches.exists():
            results = product_matches

    return render(request, 'search_results.html', {"products": results, "query": query})


def live_search(request):
    query = request.GET.get("term", "")
    suggestions = []

    if query:
        product_matches = Products.objects.filter(name__icontains=query)[:10]
        category_matches = Catagory.objects.filter(name__icontains=query)[:5]

        for p in product_matches:
            suggestions.append({
                "label": p.name,
                "value": p.name,
                "image": p.product_image.url,
                "url": f"/product/{p.id}/"
            })

        for c in category_matches:
            suggestions.append({
                "label": f"Category: {c.name}",
                "value": c.name,
                "image": "",  # or optional category image
                "url": f"/collections/{c.id}/"
            })

    return JsonResponse(suggestions, safe=False)