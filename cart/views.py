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
from .models import Order, OrderItem, PaymentUpload, AdminOrder
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Cart, Order, OrderItem, AdminOrder, CartItem
from products.models import Product  # Ensure this import is correct

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

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentUploadForm
from .models import Order


def upload_payment(request, order_id=None):
    order = get_object_or_404(Order, id=order_id) if order_id else None

    if request.method == 'POST':
        form = PaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.order = order  # เชื่อมการชำระเงินกับออเดอร์
            new_payment.save()
            send_payment_notification(new_payment)
            return redirect('success')
    else:
        form = PaymentUploadForm(initial={'order': order.id if order else None})
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



@login_required
def success_view(request):
    with transaction.atomic():
        account = get_object_or_404(Account, user=request.user)
        cart, _ = Cart.objects.get_or_create(account=account)
        order = Order.objects.create(user=request.user)  # Create a new order
        total_price = 0
        cart_items = list(cart.cart_items.all())  # Capture cart items before deleting

        for item in cart_items:
            order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            total_price += item.product.price * item.quantity

        cart.cart_items.all().delete()  # Clear the cart after checkout
        AdminOrder.objects.create(user=request.user, order=order, shipping_details='Your shipping details here')

        context = {
            'total_price': total_price,
            'cart_items': cart_items,  # Pass the list of items to the template
            'order': order,  # Pass the order to access order details like date
        }
        return render(request, 'cart/success.html', context)


def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    payment_details = get_object_or_404(PaymentUpload, order=order)
    admin_order = get_object_or_404(AdminOrder, order=order)

    context = {
        'order': order,
        'order_items': order_items,
        'payment_details': payment_details,
        'admin_order': admin_order,
    }
    return render(request, 'cart/admin_order_detail.html', context)














