from django.urls import path
from . import views

urlpatterns= [
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('collections/',views.collections,name="collections"),
    path('collections/<int:cid>/', views.collection_products, name="collection_products")
]