from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'get_product_name', 'quantity']  # เปลี่ยน 'product' เป็น 'get_product_name'
    search_fields = ['account__user__username', 'product__name']

    def get_product_name(self, obj):
        return obj.product.name  # อ้างอิงชื่อสินค้าจาก ForeignKey Product

    get_product_name.short_description = 'Product'  # ตั้งชื่อแสดงในหัวตาราง


# Register your models with customized admin options
admin.site.register(Cart, CartAdmin)
