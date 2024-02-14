from django.shortcuts import get_object_or_404, render, redirect
from products.forms import AddproductForm
from .models import * 
from authenticate.models import Account
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
def product(request):
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
    product = Product.objects.all()
    return render(request,'products/product.html',{'products':product,'accounts':account}) #สร้างปุ่ม 2 ปุ่ม 1 ซื้อสินค้าสำหรับcustomer เท่านั้น 2.เพิ่มสินค้า emp/admin

def addProduct(request):
    category = Category.objects.all()
    if request.method=='POST':
        form = AddproductForm(request.POST,request.FILES)
        cat = Category.objects.get(name=request.POST.get('cat'))
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.category = cat
            product_instance.save()
            return redirect('products')
    else:
        form = AddproductForm()
    return render(request, 'products/addproduct.html',{'productform':form, 'categorys':category })

def editProduct(request, pk):
    product = Product.objects.get(id=pk) 
    if request.method == 'POST':
        form = AddproductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = AddproductForm(instance=product)
    return render(request, 'products/addproduct.html',{'productform':form})

def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('products')

def product_list(request):
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
    product = Product.objects.all()
    return render(request,'products/product.html',{'products':product,'accounts':account})

from django.shortcuts import render
from .models import Product

def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)  # Adjust the filter according to your needs
    return render(request, 'products/product.html', {'products': products})

# from django.shortcuts import redirect

# def addcart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.POST.get('quantity', 1))

#     if product.stock_quantity < quantity:
#         return HttpResponse('ไม่สามารถเพิ่มสินค้าได้ เนื่องจากปริมาณสินค้าไม่เพียงพอ', status=400)

#     cart, _ = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartProduct.objects.get_or_create(
#         cart=cart,
#         product=product,
#         defaults={'quantity': quantity}
#     )

#     if not created:
#         cart_item.quantity += quantity
#         cart_item.save()

#     # ลดปริมาณสินค้าใน stock โดยใช้ F expression
#     Product.objects.filter(id=product_id).update(stock_quantity=F('stock_quantity') - quantity)

#     return redirect('cart_detail')

# def cart_detail(request):
#     cart, _ = Cart.objects.get_or_create(user=request.user)  # ตรวจสอบว่ามีการสร้าง Cart สำหรับ user หรือไม่
#     cart_items = CartProduct.objects.filter(cart=cart)  # ดึงสินค้าในตะกร้าของ user นั้น
#     for item in cart_items:
#         item.total_price = item.quantity * item.product.price
#     return render(request, 'products/cart_detail.html', {'cart_items': cart_items})


# def remove_from_cart(request, product_id):
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_item = get_object_or_404(CartProduct, product_id=product_id, cart=cart)

#     # รับค่าจำนวนที่ต้องการลบจากฟอร์ม
#     quantity_to_remove = int(request.POST.get('quantity', 1))

#     # ตรวจสอบและลบจำนวนสินค้า
#     if cart_item.quantity > quantity_to_remove:
#         cart_item.quantity -= quantity_to_remove
#         cart_item.save()
#     else:
#         cart_item.delete()

#     return HttpResponseRedirect(reverse('cart_detail'))