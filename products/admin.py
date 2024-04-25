from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import ShippingCost
# Register your models here.
class PictureInline(admin.TabularInline):
    model = Picture
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','product_cover', 'created_at', 'updated_at')
    inlines = [PictureInline]

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'image', 'descriptions')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','descriptions', 'created_at', 'updated_at')


class ShippingCostAdmin(admin.ModelAdmin):
    list_display = ['shipping_company', 'shipping_cost']
    search_fields = ['shipping_company']
    # สร้างฟอร์มที่สามารถแก้ไขข้อมูลได้
    fields = ['shipping_company', 'shipping_cost']

admin.site.register(ShippingCost, ShippingCostAdmin)

