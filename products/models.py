from django.db import models
from django.conf import settings
from django.db import models
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    def __srt__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_cover = models.ImageField(upload_to='product_pictures', blank=True)
    stock_quantity = models.IntegerField()
    category = models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Picture(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='pictures', default=1)
    image = models.ImageField(upload_to='product_pictures')
    descriptions = models.TextField(blank=True)
    def __str__(self):
        return f"Picture {self.id} for Product {self.product.name}"
    
from django.db import models

class ShippingCost(models.Model):
    shipping_company = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.shipping_company




