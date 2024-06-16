from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.core.files.storage import default_storage
from cart.models import Order, OrderItem, AdminOrder
from .models import Cart, CartItem, PaymentUpload
from authenticate.models import Account, Address
from products.models import Product
from .forms import PaymentUploadForm, OrderUpdateForm, AdminOrderForm
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrderUpdateForm, AdminOrderForm
from authenticate.models import Address 
from .models import Order, PaymentUpload, AdminOrder, Cart, CartItem
from django.shortcuts import get_object_or_404, redirect, render
from .models import Account, Cart, Product, CartItem
import logging
from .models import Order, Review, Product
from .forms import ReviewForm
logger = logging.getLogger(__name__)



@login_required 
def cartdisplay(request):
    account = get_object_or_404(Account, user=request.user)
    cart, _ = Cart.objects.get_or_create(account=account)
    shipping_fee_per_item = 20 

    if request.method == 'POST': 
        delivery_method = request.POST.get('delivery_method', 'pickup')  # รับค่าจากฟอร์ม # รับค่าจากฟอร์มวิธีการจัดส่ง ค่าเริ่มต้นเป็น 'pickup' ถ้าไม่ได้ระบุ
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))

        if product_id and quantity:
            try:
                product = Product.objects.get(id=product_id)
                if product.stock_quantity >= quantity:
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                    if created:
                        cart_item.quantity = quantity
                    else:
                        cart_item.quantity += quantity
                    cart_item.save()
                    product.stock_quantity -= quantity
                    product.save()
            except Product.DoesNotExist:
                pass  
        else:
            cart.delivery_method = delivery_method
            cart.save()
        return redirect('cartdisplay')

    cart_items = cart.cart_items.all()
    total_price = 0  
    total_quantity = 0 
    for item in cart_items:
        item.total_price = item.quantity * item.product.price # คำนวณราคารวมของแต่ละสินค้า
        total_price += item.total_price # เพิ่มราคารวมของสินค้าเข้าในราคารวมของตะกร้า
        total_quantity += item.quantity # เพิ่มจำนวนสินค้าของสินค้าเข้าในจำนวนสินค้าทั้งหมดในตะกร้า

    delivery_method = cart.delivery_method if hasattr(cart, 'delivery_method') else 'pickup'
    shipping_fee = total_quantity * shipping_fee_per_item if delivery_method == 'delivery' else 0
    total_price += shipping_fee # เพิ่มค่าจัดส่งเข้าในราคารวม

    return render(request, 'cart/displaycart.html', {
        'cart_items': cart_items, 
        'total_price': total_price, 
        'shipping_fee': shipping_fee,
        'delivery_method': delivery_method
    })


@login_required
@require_POST
def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__account__user=request.user)
        quantity_to_delete = int(request.POST.get('quantity', 1))
        product = cart_item.product
        product.stock_quantity += quantity_to_delete
        product.save()
        
        if quantity_to_delete >= cart_item.quantity:
            cart_item.delete()
        else:
            cart_item.quantity -= quantity_to_delete
            cart_item.save()
        return redirect('cartdisplay')

    except CartItem.DoesNotExist:
        return redirect('cartdisplay')



@login_required 
def upload_payment(request):
    total_price = request.GET.get('total_price', 0)
    delivery_method = request.GET.get('delivery_method', 'pickup')
    order = Order.objects.create(user=request.user, delivery_method=delivery_method)

    if request.method == 'POST':
        print(f'DM :{delivery_method},\n P:{total_price}')
        form = PaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.amount = total_price
            new_payment.order = order
            new_payment.save()
            print(new_payment.id)
            send_payment_notification(new_payment)
            return redirect('success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PaymentUploadForm() 
    return render(request, 'cart/payment.html', {'form': form, 'total_price': total_price})



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
            return

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
        print(f"Failed to send email: {e}") 


@login_required
def success_view(request):
    with transaction.atomic():
        account = get_object_or_404(Account, user=request.user)
        cart, _ = Cart.objects.get_or_create(account=account)
        order = Order.objects.filter(user=request.user).latest('order_date')
        logger.debug(f'Order created with ID: {order.id}') 

        total_price = 0
        cart_items = list(cart.cart_items.all())

        for item in cart_items:
            order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            total_price += item.product.price * item.quantity

        cart.cart_items.all().delete()
        AdminOrder.objects.create(user=request.user, order=order, shipping_details='Your shipping details here')

        return redirect(reverse('order_details', args=[order.id]))


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()
    payment_uploads = PaymentUpload.objects.filter(order=order)
    admin_order, created = AdminOrder.objects.get_or_create(order=order, user=order.user)
    
    address = Address.objects.filter(account=order.user.account).first()
    user_role = request.user.account.role

    total_price = sum(item.product.price * item.quantity for item in order_items)
    shipping_fee = sum(item.quantity for item in order_items) * 20 if order.delivery_method == 'delivery' else 0
    total_price_with_shipping = total_price + shipping_fee

    if request.method == 'POST':
        order_form = OrderUpdateForm(request.POST, instance=order)
        admin_order_form = AdminOrderForm(request.POST, instance=admin_order)

        if order_form.is_valid() and admin_order_form.is_valid():
            order_form.save()
            admin_order_form.save()
            messages.success(request, 'Order updated successfully.')
            return redirect('sales_history')
    else:
        order_form = OrderUpdateForm(instance=order)
        admin_order_form = AdminOrderForm(instance=admin_order)

    context = {
        'order': order,
        'order_items': order_items,
        'payment_uploads': payment_uploads,
        'order_form': order_form,
        'admin_order_form': admin_order_form,
        'address': address,
        'user_role': user_role,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
        'total_price_with_shipping': total_price_with_shipping,
    }
    return render(request, 'cart/admin_order_detail.html', context)



@login_required
def sales_history(request):
    orders = Order.objects.filter(order_status__in=['SHIPPED', 'DELIVERED', 'CANCELLED', 'PREPARED', 'RECEIVED']).order_by('-order_date')
    order_details = []

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_status = request.POST.get('order_status')
        try:
            order = Order.objects.get(id=order_id)
            order.order_status = order_status
            order.save()
            messages.success(request, 'อัปเดตสถานะคำสั่งซื้อสำเร็จ.')
        except Order.DoesNotExist:
            messages.error(request, 'คำสั่งซื้อไม่ถูกต้อง.')

    for order in orders:
        total_price = sum(item.product.price * item.quantity for item in order.order_items.all())
        if order.delivery_method == 'delivery':
            shipping_fee = sum(item.quantity for item in order.order_items.all()) * 20
        else:
            shipping_fee = 0
        total_price += shipping_fee

        items = []
        for item in order.order_items.all():
            items.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price,
                'image_url': item.product.product_cover.url if item.product.product_cover else ''
            })

        order_details.append({
            'order': order,
            'total_price': total_price,
            'items': items,
            'delivery_method': order.get_delivery_method_display(),
        })

    order_status_choices = Order.order_status_choices

    return render(request, 'cart/sales_history.html', {
        'order_details': order_details,
        'order_status_choices': order_status_choices
    })

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        if new_status in ['DELIVERED', 'RECEIVED']:
            order.order_status = new_status
            order.save()
            messages.success(request, 'อัปเดตสถานะคำสั่งซื้อสำเร็จ.')
        else:
            messages.error(request, 'ไม่สามารถอัปเดตสถานะคำสั่งซื้อได้.')
    return redirect('purchase_history')

# ฟังก์ชันนี้แสดงประวัติการซื้อ
@login_required
def purchase_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    order_details = []
    for order in orders:
        total_price = sum(item.product.price * item.quantity for item in order.order_items.all())
        if order.delivery_method == 'delivery':
            shipping_fee = sum(item.quantity for item in order.order_items.all()) * 20
        else:
            shipping_fee = 0
        total_price += shipping_fee

        items = []
        for item in order.order_items.all():
            items.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price,
                'image_url': item.product.product_cover.url if item.product.product_cover else '',
                'review': Review.objects.filter(order=order, product=item.product).first(),
            })

        admin_order = AdminOrder.objects.filter(order=order).first()
        shipping_details = admin_order.get_shipping_details_display() if admin_order else 'N/A'

        order_details.append({
            'order': order,
            'total_price': total_price,
            'tracking_number': order.tracking_number,
            'delivery_method': order.get_delivery_method_display(),
            'shipping_details': shipping_details,
            'items': items,
        })

    return render(request, 'cart/purchase_history.html', {'order_details': order_details})


@login_required
def submit_review(request, order_id, product_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.order = order
            review.product = product
            review.save()
            return redirect('purchase_history')
    else:
        form = ReviewForm()

    return render(request, 'cart/review.html', {'form': form, 'order': order, 'product': product})































