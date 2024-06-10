from django.contrib import admin
from .models import Category, Product, Picture

class PictureInline(admin.TabularInline):
    model = Picture

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_cover', 'created_at', 'updated_at')
    inlines = [PictureInline]

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'descriptions')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'created_at', 'updated_at')
