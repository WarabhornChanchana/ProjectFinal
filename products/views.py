from django.shortcuts import render, redirect
from products.forms import AddproductForm
from . models import *
from authenticate.models import Account

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
    if request.method=='POST':
        form = AddproductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = AddproductForm()
    return render(request, 'products/addproduct.html',{'productform':form})

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

def buyProduct(request, pk):
    # โค้ดจัดการการซื้อสินค้าที่นี่...
    return redirect('products')