from django.shortcuts import render,redirect
from . forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from formtools.wizard.views import SessionWizardView


class RegistrationWizard(SessionWizardView):
    form_list = [RegisterForm,AddressForm]
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

        # Save address information
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
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user =  authenticate(request,username=username,password=password)
            if user  is not None:
                login(request,user)
                return redirect('home')
    return render(request,'authenticate/login.html',{'loginform':form})

def logout_user(request):
    auth.logout(request)
    return redirect('home')