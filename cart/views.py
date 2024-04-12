from django.shortcuts import render, redirect
from .models import Cart, Account, Product  # Make sure to import the necessary models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart

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

        return redirect('cartdisplay')
    else:
        account = Account.objects.get(user=request.user)
        cart_items = Cart.objects.filter(account=account)
        
        for item in cart_items:
            item.total_price = item.quantity * item.product.price
        return render(request, 'cart/displaycart.html', {'cart_items': cart_items})


def remove_single_from_cart(request, product_id):
    cart = Cart.objects.filter(account__user=request.user).first()
    cart_item = get_object_or_404(Cart.objects.filter(account=request.user.account), product_id=product_id)
    if cart_item.quantity > 1:  # ตรวจสอบว่าจำนวนสินค้ามากกว่า 1 หรือไม่
        cart_item.quantity -= 1  # ลดจำนวนสินค้าลงทีละ 1
        cart_item.save()
    else:
        cart_item.delete()  # ถ้าเหลือแค่ 1 ชิ้น ให้ลบสินค้าออกจากตะกร้า

    return redirect('cartdisplay')

