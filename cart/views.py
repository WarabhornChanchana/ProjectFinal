from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.core.files.storage import default_storage
from cart.models import Order, OrderItem, AdminOrder
from .models import Cart, CartItem, PaymentUpload
from authenticate.models import Account
from products.models import Product
from .forms import PaymentUploadForm

@login_required
def cartdisplay(request):
    account = get_object_or_404(Account, user=request.user)
    cart, _ = Cart.objects.get_or_create(account=account)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        # ทำการแปลงเป็น int โดยตรงและใช้ค่า default เป็น 0
        quantity = int(request.POST.get('quantity', 0))

        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            # ตรวจสอบว่า cart_item เป็นครั้งแรกที่สร้างหรือไม่
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

        return redirect('cartdisplay')

    cart_items = cart.cart_items.all()
    for item in cart_items:
        item.total_price = item.quantity * item.product.price

    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'cart/displaycart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
@require_POST
def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__account__user=request.user)
        
        # Get the quantity to delete from the request
        quantity_to_delete = int(request.POST.get('quantity', 1))

        if quantity_to_delete >= cart_item.quantity:
            cart_item.delete()
        else:
            cart_item.quantity -= quantity_to_delete
            cart_item.save()

        # Re-calculate the total price after the item has been removed/updated
        total_price = sum(item.quantity * item.product.price for item in CartItem.objects.filter(cart__account__user=request.user))

        return JsonResponse({
            'success': True,
            'total_price': total_price,
            'message': 'Item removed successfully.'
        })

    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Item not found.'
        }, status=404)

def upload_payment(request):
    if request.method == 'POST':
        form = PaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_payment = form.save()
            send_payment_notification(new_payment)
            messages.success(request, 'Your payment slip has been uploaded successfully!')
            return redirect('success')
    else:
        form = PaymentUploadForm()
    return render(request, 'cart/payment.html', {'form': form})

def send_payment_notification(payment_upload):
    subject = 'New Payment Slip Uploaded'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['fanyny.shop01@gmail.com']
    context = {
        'name': payment_upload.name,
        'amount': payment_upload.amount,
        'phone': payment_upload.phone,
        'transfer_time': payment_upload.transfer_time.strftime('%H:%M %d-%m-%Y'),
    }

    payment_slip_path = payment_upload.payment_slip.path
    with default_storage.open(payment_slip_path, 'rb') as image_file:
        image_data = image_file.read()
        if not image_data:
            print("Image file is empty.")
            return  # Consider adding more robust notification or error handling here

    try:
        image = MIMEImage(image_data)
        image.add_header('Content-ID', '<payment_slip_image>')
        html_content = render_to_string('cart/emails/payment_notification.html', context)
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=email_from,
            to=recipient_list
        )
        email.content_subtype = "html"
        email.attach(image)
        email.send()
    except Exception as e:
        print(f"Failed to send email: {e}")  # Consider more robust error handling or logging


def success_view(request):
    account = get_object_or_404(Account, user=request.user)
    cart, _ = Cart.objects.get_or_create(account=account)
    order = Order.objects.create(user=request.user)  # Create a new order
    total_price = 0

    for item in cart.cart_items.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        total_price += item.product.price * item.quantity

    cart.cart_items.all().delete()  # Clear the cart after checkout

    # Create AdminOrder
    AdminOrder.objects.create(user=request.user, order=order, shipping_details='Your shipping details here')

    return render(request, 'cart/success.html', {'total_price': total_price})

from django.shortcuts import render, get_object_or_404
from .models import PaymentUpload
from cart.models import OrderItem


def payment_detail(request, id):
    payment = get_object_or_404(PaymentUpload, pk=id)
    order_items = OrderItem.objects.filter(order__payment__id=id)
    return render(request, 'cart/order_detail.html', {'payment': payment, 'order_items': order_items})



