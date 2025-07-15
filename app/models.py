from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}_{filename}"
    return os.path.join('uploads/', new_filename)

class Catagory(models.Model):  # (you can rename to Category if needed)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    vendor = models.CharField(max_length=150)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField()
    original_price = models.FloatField()
    selling_price = models.FloatField()
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductReview(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)  # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.username} ({self.rating}★)"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default="Unknown")
    phone = models.CharField(max_length=15)
    address = models.TextField(default='N/A')
    total_price = models.FloatField()
    payment_method = models.CharField(max_length=20, default="COD")  # COD or Online
    is_completed = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    
    DELIVERY_CHOICES = [
        ("Processing", "Processing"),
        ("Dispatched", "Dispatched"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
    ]
    delivery_status = models.CharField(max_length=30, choices=DELIVERY_CHOICES, default="Processing")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)

    def __str__(self):
        return f"Image of {self.product.name}"
