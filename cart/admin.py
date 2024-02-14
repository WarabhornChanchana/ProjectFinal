from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'product', 'quantity']
    search_fields = ['account__user__username','product__name']

# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'cart', 'product', 'quantity']
#     list_filter = ['cart', 'product']
#     search_fields = ['cart__account__user__username', 'product__name']

# Register your models with customized admin options
admin.site.register(Cart, CartAdmin)