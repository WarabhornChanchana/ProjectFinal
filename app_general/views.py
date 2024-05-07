from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Slide
from cart.models import PaymentUpload
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .forms import SlideForm
from .models import Slide
from cart.models import PaymentUpload, Account
from django.http import HttpResponseForbidden


def home(request):
    slides = Slide.objects.all()
    return render(request, 'app_general/home.html', {'slides': slides})


@login_required(login_url='login')
def history(request):
    payments = PaymentUpload.objects.filter(name=request.user.username)
    return render(request,'app_general/history.html', {'payments': payments})

@login_required
def admin_payment_history(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if account.role != Account.ADMIN:
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Sort payments by 'transfer_time' in descending order
    payments = PaymentUpload.objects.all().order_by('-transfer_time')
    return render(request, 'app_general/admin_order.html', {'payments': payments})


def add_slide(request):
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SlideForm()
    return render(request, 'app_general/add_slide.html', {'form': form})
