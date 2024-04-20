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

def cartdisplay(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        account = Account.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)
        
        try:
            cart = Cart.objects.get(account=account, product=product)
            cart.quantity += quantity
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(account=account, product=product, quantity=quantity)

        return redirect('cart_display')
    else:
        account = Account.objects.get(user=request.user)
        cart_items = Cart.objects.filter(account=account)
        
        total_price = 0
        for item in cart_items:
            item.total_price = item.quantity * item.product.price
            total_price += item.total_price  # นับราคารวมสุทธิทั้งหมด
        return render(request, 'cart/displaycart.html', {'cart_items': cart_items, 'total_price': total_price})



# def cartdisplay(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         quantity = int(request.POST.get('quantity', 1))

#         account = Account.objects.get(user=request.user)
#         product = Product.objects.get(id=product_id)

#         try:
#             cart = Cart.objects.get(account=account, product=product)
#             cart.quantity += quantity
#             cart.save()
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(account=account, product=product, quantity=quantity)

#         return redirect('cartdisplay')
#     else:
#         account = Account.objects.get(user=request.user)
#         cart_items = Cart.objects.filter(account=account)

#         for item in cart_items:
#             item.total_price = item.quantity * item.product.price
#         return render(request, 'cart/displaycart.html', {'cart_items': cart_items})
    
from django.shortcuts import redirect, get_object_or_404
from .models import Cart

def checkout(request):
    # ดำเนินการต่อเพื่อทำการชำระเงิน หรือสั่งซื้อสินค้าตามที่คุณต้องการ
    return render(request, 'cart/checkout.html')

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






