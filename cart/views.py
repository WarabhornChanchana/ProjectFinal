from django.shortcuts import render, redirect
from .models import Cart
from authenticate.models import Account
from products.models import Product

def cartdisplay(request):
    if request.method == 'POST':
        # Assuming you have a form to add products to the cart
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Get the logged-in user's account
        account = Account.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)
        
        # Retrieve or create the user's cart
        try:
            cart = Cart.objects.get(account=account, product=product)
            cart.quantity += quantity
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(account=account, product=product, quantity=quantity)

        return redirect('cartdisplay')
    else:
        # If request method is not POST, render the template
        account = Account.objects.get(user=request.user)
        cart_items = Cart.objects.filter(account=account)
        return render(request, 'cart/displaycart.html', {'cart_items': cart_items})