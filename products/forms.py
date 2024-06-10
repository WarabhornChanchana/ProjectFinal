from django import forms
from .models import Product, Category

class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a Category", label="หมวดหมู่")

    class Meta:
        model = Product
        fields = ['name', 'descriptions', 'price', 'product_cover', 'stock_quantity', 'category']
