from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from . models import *
from django.forms.widgets import PasswordInput,TextInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
  
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role_choices = [('admin', 'Admin'), ('customer', 'Customer'), ('employee', 'Employee')]
    role = forms.ChoiceField(choices=role_choices, required=True)
    first_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username","email","password1","password2", "role", "phone_number"]

        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'district', 'city' , 'postal_code']