from django.conf import settings
from django.shortcuts import render, redirect
from .models import Cart, Account, Product  # Make sure to import the necessary models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
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

from django.shortcuts import render, redirect
from .forms import PaymentUploadForm
from .models import PaymentUpload
# from .views import send_payment_notification  # อย่าลืมนำเข้าฟังก์ชัน

from django.contrib import messages

def upload_payment(request):
    if request.method == 'POST':
        form = PaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_payment = form.save()
            send_payment_notification(new_payment)  # ส่งอีเมลการแจ้งเตือน
            messages.success(request, 'Your payment slip has been uploaded successfully!')
            return redirect('payment')  # Redirect กลับไปยังหน้าอัปโหลดเดิม
    else:
        form = PaymentUploadForm()
    return render(request, 'cart/payment.html', {'form': form})



# views.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import PaymentUpload
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.core.files.storage import default_storage
from django.conf import settings

def send_payment_notification(payment_upload):
    subject = 'New Payment Slip Uploaded'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['fanyny.shop01@gmail.com']
    
    # โหลดรูปภาพสลิปการชำระเงิน
    payment_slip_path = payment_upload.payment_slip.path
    with default_storage.open(payment_slip_path, 'rb') as image_file:
        image = MIMEImage(image_file.read())
        image.add_header('Content-ID', '<payment_slip_image>')

    # เรนเดอร์ HTML และสร้างอีเมล
    html_content = render_to_string('cart/emails/payment_notification.html', {
        'payment': payment_upload,
        # ส่งตัวแปรอื่น ๆ ที่ต้องการใช้ใน template
    })
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=email_from,
        to=recipient_list
    )
    email.content_subtype = "html"  # บอกว่าเนื้อหาเป็น HTML
    email.attach(image)  # แนบรูปภาพ
    email.send()

# views.py
from django.shortcuts import render, redirect
from .forms import PaymentUploadForm
from .models import PaymentUpload
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

# ส่วนอื่นๆ ของ views.py ของคุณ...

def success_view(request):
    return render(request, 'cart/success.html')

# views.py

from django.shortcuts import get_object_or_404, render
from .models import PaymentUpload

def payment_detail(request, id):
    payment = get_object_or_404(PaymentUpload, pk=id)
    return render(request, 'cart/payment_detail.html', {'payment': payment})













