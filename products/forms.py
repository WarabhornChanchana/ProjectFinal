from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from . models import *

class AddproductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_cover','name','descriptions','price','stock_quantity']
