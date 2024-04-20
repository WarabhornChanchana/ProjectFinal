from django.shortcuts import render,redirect
from . forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from formtools.wizard.views import SessionWizardView


class RegistrationWizard(SessionWizardView): #เป็นคลาสที่มาจากการลงทะเบีบนของผู้ใช้งาน
    form_list = [RegisterForm,AddressForm] #ฟอร์มแต่ละขั้นตอน
    template_name = "authenticate/register.html" 

    def done(self, form_list, **kwargs):
        user_form = form_list[0]
        address_form = form_list[1]
        user = user_form.save(commit=False)
        user.email = user_form.cleaned_data['email']
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        user.save()

        phone_number = user_form.cleaned_data['phone_number']
        role = user_form.cleaned_data['role']
        account = Account.objects.create(user=user, phone_number=phone_number, role=role)

        address = address_form.save(commit=False)
        address.account = account
        address.save()
        return redirect('home')
    
def register(request):
    wizard_view = RegistrationWizard.as_view()
    return wizard_view(request)
  

def login_user(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'authenticate/login.html', {'loginform': form})

def logout_user(request):
    auth.logout(request)
    return redirect('home')

from django.shortcuts import render, redirect
from .forms import  AddressForm
from django.contrib.auth.models import User
from .models import Account, Address

def edit_profile(request, pk):
    account = Account.objects.get(pk=pk)
    address_instance = account.address.first()  # Get the first address instance associated with the account

    if request.method == 'POST':
        account_form = ProfileForm(request.POST, instance=account)
        address_form = AddressForm(request.POST, instance=address_instance)
        
        if account_form.is_valid() and address_form.is_valid():
            account_form.save()
            address_form.save()
            return redirect('home')
    else:
        account_form = ProfileForm(instance=account)
        address_form = AddressForm(instance=address_instance)

    return render(request, 'edit_profile.html', {'account_form': account_form, 'address_form': address_form})






