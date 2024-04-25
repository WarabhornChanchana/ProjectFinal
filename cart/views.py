from django.conf import settings
from django.shortcuts import render, redirect
from .models import Cart, Account, Product  # Make sure to import the necessary models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart

from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from authenticate.models import Account

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import ObjectDoesNotExist
from .models import Cart, CartItem
from authenticate.models import Account
from products.models import Product

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, CartItem, Cart, Account

def cartdisplay(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect('cartdisplay')

    try:
        cart = Cart.objects.get(account=account)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(account=account)
    except Cart.MultipleObjectsReturned:
        # Handle the case where multiple carts are found
        carts = Cart.objects.filter(account=account)
        cart = carts.first()  # Choose the first cart if multiple are found

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return redirect('cartdisplay')

    cart_items = cart.cart_items.all() if cart else []
    for item in cart_items:
        item.total_price = item.quantity * item.product.price

    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'cart/displaycart.html', {'cart_items': cart_items, 'total_price': total_price})

   

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CartItem

def remove_from_cart(request):
    if request.method == 'POST' and request.is_ajax():
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity not provided
        
        # Retrieve cart item
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Update quantity or delete item if quantity is zero or less
        if quantity > 0:
            cart_item.quantity -= quantity
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        else:
            cart_item.delete()
        
        # Calculate new total price
        total_price = 0
        cart_items = CartItem.objects.filter(account=request.user.account)
        for item in cart_items:
            total_price += item.total_price
        
        # Return JSON response indicating success and new total price
        return JsonResponse({'success': True, 'total_price': total_price}, status=200)
    
    # If request method is not POST or not AJAX, return error response
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from authenticate.models import Account
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags

from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def payment_view(request):
    if request.method == 'POST':
        # ตรวจสอบการโอนเงินและการแนบสลิป
        if 'paymentSlip' in request.FILES:
            # ดึงข้อมูลราคาสินค้าและค่าจัดส่งจากข้อมูลที่มีอยู่ เช่น request.POST หรือ request.session
            total_price = 1000  # ตัวอย่างราคาสินค้ารวม
            shipping_cost = 50  # ตัวอย่างค่าจัดส่ง
            grand_total = total_price + shipping_cost

            payment_slip = request.FILES['paymentSlip']

            # บันทึกข้อมูลการโอนเงิน และแนบสลิป
            # โค้ดการบันทึกข้อมูลจะอยู่ที่นี่

            # ส่งอีเมลแจ้งเตือน
            subject = 'แจ้งเตือนการโอนเงิน'
            from_email = settings.EMAIL_HOST_USER
            to_email = 'อีเมลของร้านค้า'
            qr_code_url = 'URL ของ QR Code ที่ส่งมาจากลูกค้า'

            # สร้างเนื้อหา HTML ของอีเมล
            html_message = render_to_string('email/payment_notification.html', {'qr_code_url': qr_code_url})
            plain_message = strip_tags(html_message)

            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            # ส่งอีเมลเสร็จแล้ว
            return JsonResponse({'message': 'ส่งอีเมลเรียบร้อยแล้ว', 'total_price': grand_total})
        else:
            return JsonResponse({'error': 'กรุณาแนบสลิปการโอนเงิน'}, status=400)
    else:
        # ดึงข้อมูลราคาสินค้าและค่าจัดส่งจากข้อมูลที่มีอยู่ เช่น request.POST หรือ request.session
        total_price = 1000  # ตัวอย่างราคาสินค้ารวม
        shipping_cost = 50  # ตัวอย่างค่าจัดส่ง
        grand_total = total_price + shipping_cost

        return render(request, 'cart/payment.html', {'total_price': grand_total, 'shipping_cost': shipping_cost})










