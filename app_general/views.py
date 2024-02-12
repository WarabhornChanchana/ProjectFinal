from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'app_general/home.html')

@login_required(login_url='login')
def history(request):
    return render(request,'app_general/history.html')