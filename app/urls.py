from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, user_dashboard


urlpatterns= [
    path('',views.home,name="home"),
    path('collections/',views.collections,name="collections"),
    path('collections/<int:cid>/', views.collection_products, name="collection_products"),
    path("product/<int:pid>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<int:pid>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("remove-from-cart/<int:pid>/", views.remove_from_cart, name="remove_from_cart"),
    path("add-to-wishlist/<int:pid>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", views.view_wishlist, name="view_wishlist"),
    path("toggle-wishlist/<int:pid>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("checkout/", views.checkout_view, name="checkout_view"),
    path("order_success/", views.order_success, name="order_success"),
    path("delivery/", views.delivery_dashboard, name="delivery_dashboard"),
    path("delivery/mark/<int:order_id>/", views.mark_delivered, name="mark_delivered"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("search/", views.search_products, name="search_products"),
    path("live-search/", views.live_search, name="live_search"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("update-delivery/<int:order_id>/", views.update_delivery_status, name="update_delivery_status"),
    path('edit-profile/', views.edit_profile, name='edit_profile')







]