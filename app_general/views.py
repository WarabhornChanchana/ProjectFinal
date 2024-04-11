from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Slide

def home(request):
    slides = Slide.objects.all()
    return render(request, 'app_general/home.html', {'slides': slides})


@login_required(login_url='login')
def history(request):
    return render(request,'app_general/history.html')

from django.shortcuts import render, redirect
from .forms import SlideForm
from .models import Slide

def add_slide(request):
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SlideForm()
    return render(request, 'app_general/add_slide.html', {'form': form})
