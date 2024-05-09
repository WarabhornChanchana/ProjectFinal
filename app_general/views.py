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
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    slides = Slide.objects.all()
    return render(request, 'app_general/home.html', {'slides': slides})


@login_required(login_url='login')
def history(request):
    payments = PaymentUpload.objects.filter(name=request.user.username)
    return render(request,'app_general/history.html', {'payments': payments})

@login_required
def admin_order(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if account.role != Account.ADMIN:
        return HttpResponseForbidden("You do not have permission to view this page.")
    payments = PaymentUpload.objects.all().order_by('-transfer_time')

    if 'delete' in request.POST:
        payment_id = request.POST.get('delete')
        try:
            payment_to_delete = PaymentUpload.objects.get(id=payment_id)
            payment_to_delete.delete()
            messages.success(request, 'Order has been successfully deleted.')
        except ObjectDoesNotExist:
            messages.error(request, "No such payment exists.")
        return redirect('admin_order')  # Redirect back to the same page to refresh the list

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
