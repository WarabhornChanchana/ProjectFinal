from .forms import SlideForm
from cart.models import PaymentUpload, Account
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from .models import Slide
from cart.models import Review, Order
from datetime import timedelta
from cart.models import Order, Review
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from authenticate.models import Account
from django.db import models
import json
from decimal import Decimal

@login_required
def admin_dashboard(request):
    if request.user.account.role != Account.ADMIN:
        messages.error(request, 'คุณไม่มีสิทธิ์ในการเข้าดูหน้านี้.')
        return redirect('home')

    delivered_orders = Order.objects.filter(order_status__in=['DELIVERED', 'RECEIVED']).order_by('-order_date')
    total_sales = sum(order.total_price() for order in delivered_orders)
    total_reviews = Review.objects.count()
    reviews = Review.objects.order_by('-created_at')[:10]
    recent_orders = delivered_orders[:10]

    start_date = make_aware(datetime.now() - timedelta(days=365))
    monthly_sales_data = delivered_orders.filter(order_date__gte=start_date)
    monthly_sales = {}
    for order in monthly_sales_data:
        month = order.order_date.strftime('%Y-%m')
        if month not in monthly_sales:
            monthly_sales[month] = Decimal(0)
        monthly_sales[month] += order.total_price()

    monthly_sales = [{'year': k.split('-')[0], 'month': k.split('-')[1], 'total': float(v)} for k, v in monthly_sales.items()]

    product_ratings = list(Review.objects.values('product__name').annotate(average_rating=models.Avg('rating')))
    
    context = {
        'total_sales': total_sales,
        'total_reviews': total_reviews,
        'reviews': reviews,
        'recent_orders': recent_orders,
        'monthly_sales': json.dumps(monthly_sales),
        'product_ratings': json.dumps(product_ratings),
    }
    return render(request, 'app_general/admin_dashboard.html', context)




def home(request):
    slides = Slide.objects.all()
    reviews = Review.objects.order_by('-created_at')[:10]
    return render(request, 'app_general/home.html', {'slides': slides, 'reviews': reviews})


@login_required
def admin_order(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if account.role != Account.ADMIN:
        return HttpResponseForbidden("You do not have permission to view this page.")
    payments = PaymentUpload.objects.filter(order__order_status__in=['PENDING', 'PROCESSING']).order_by('-transfer_time') 
    if 'delete' in request.POST:
        payment_id = request.POST.get('delete')
        try:
            payment_to_delete = PaymentUpload.objects.get(id=payment_id) 
            payment_to_delete.delete()
            messages.success(request, 'Order has been successfully deleted.')
        except ObjectDoesNotExist:
            messages.error(request, "No such payment exists.")
        return redirect('admin_order') 

    return render(request, 'app_general/admin_order.html', {'payments': payments})



@login_required
def add_slide(request):
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SlideForm()
    return render(request, 'app_general/add_slide.html', {'form': form})

@login_required
def edit_slide(request, slide_id):
    slide = get_object_or_404(Slide, id=slide_id)
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SlideForm(instance=slide)
    return render(request, 'app_general/edit_slide.html', {'form': form})

@login_required
def delete_slide(request, slide_id):
    slide = get_object_or_404(Slide, id=slide_id)
    if request.method == 'POST':
        slide.delete()
        return redirect('home') 
    return render(request, 'app_general/confirm_delete.html', {'slide': slide})
