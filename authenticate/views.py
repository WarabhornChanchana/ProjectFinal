from django.shortcuts import render,redirect
from authenticate.models import Account
from . forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileEditForm, AddressEditForm

class RegistrationWizard(SessionWizardView):
    form_list = [RegisterForm, AddressForm]
    template_name = "authenticate/register.html" 

    def done(self, form_list, **kwargs):
        user_form = form_list[0]
        user = user_form.save(commit=False)
        user.email = user_form.cleaned_data['email']
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        password = user_form.cleaned_data['password1'] 
        user.set_password(password) 

        user.save()

        phone_number = user_form.cleaned_data['phone_number']
        role = user_form.cleaned_data['role']
        account = Account.objects.create(user=user, phone_number=phone_number, role=role)

        address_form = form_list[1]
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
            else:
                form.add_error(None, "Invalid username or password")
    return render(request, 'authenticate/login.html', {'loginform': form})

def logout_user(request):
    auth.logout(request)
    return redirect('home')


@login_required
def edit_profile(request):
    user = request.user
    address_instance = user.account.address.first() if hasattr(user, 'account') and user.account.address.exists() else None

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=user)
        address_form = AddressEditForm(request.POST, instance=address_instance)
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            return redirect('home')
    else:
        user_form = ProfileEditForm(instance=user)
        address_form = AddressEditForm(instance=address_instance)

    return render(request, 'authenticate/edit_profile.html', {
        'user_form': user_form,
        'address_form': address_form
    })















