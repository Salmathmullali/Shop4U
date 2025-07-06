from django.urls import path
from . import views

urlpatterns= [
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('collections/',views.collections,name="collections"),
    path('collections/<int:cid>/', views.collection_products, name="collection_products"),
     path("product/<int:pid>/", views.product_detail, name="product_detail"),
     path("add-to-cart/<int:pid>/", views.add_to_cart, name="add_to_cart"),
     path("cart/", views.view_cart, name="view_cart"),
     path("remove-from-cart/<int:pid>/", views.remove_from_cart, name="remove_from_cart")
]